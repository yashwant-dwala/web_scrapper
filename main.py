import requests
from bs4 import BeautifulSoup
import urllib.parse


def find_search_form(url, headers=None):
    """
    Tries to detect the site's search form and return (base_url, param_name or querry_param_key).
    """
    if headers is None:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/116.0 Safari/537.36"
            )
        }

    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    search_url = ""
    param_name = None

    # Try to locate a search form
    try:
        form = soup.find("form")

        if form:
            action = form.get("action", "")
            search_url = urllib.parse.urljoin(url, action)

            # Find text input
            input_tag = form.find("input", {"type": "text"})
            param_name = input_tag.get("name") if input_tag else None
            if not param_name:
                raise Exception("Could not detect search parameter name")
    except Exception as e:
        print(f"[Exception] while fetching param_name from form: {e}")

    return search_url, param_name


def search_site(homepage_url, keyword):
    """
    Auto-detect search parameter from homepage and run a query.
    """
    base_url, param_name = find_search_form(homepage_url)
    print(f"base_url and qurry_param_key : {base_url}, {param_name} \n" )

    if not param_name:
        print("[ERROR] Could not detect search parameter")
        return

    query = urllib.parse.quote_plus(keyword)
    print(f"query: {query}")
    search_url = f"{base_url}?{param_name}={query}"

    print(f"[INFO] Searching: {search_url}\n")

    headers = {
        "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/116.0 Safari/537.36"
            )
    }

    page_text = None
    try:
        res = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        page_text = soup.get_text(separator="\n", strip=True)
    except Exception as e:
        print(f"exception while scrapping text: {e}")

    return page_text


if __name__ == "__main__":

    with open("Output.json","w", encoding="utf-8") as f:
        try:
            # data = search_site("https://www.amazon.in", "iphone 14")
            data = search_site("https://www.flipkart.com", "charger")
            # data = search_site("https://www.myntra.com", "Tshirt")
            f.write(data)
        except Exception as e:
            print(f"[Exception] while searching site: {e}")

    print("\n" + "="*80 + "\n")

