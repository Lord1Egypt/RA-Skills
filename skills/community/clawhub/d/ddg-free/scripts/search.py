#!/usr/bin/env python3
import requests
import sys
import json
import argparse
from urllib.parse import quote_plus, unquote
from bs4 import BeautifulSoup


def search(query, max_results=5):
    url = f"https://cn.bing.com/search?q={quote_plus(query)}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        results = []

        for item in soup.select(".b_algo"):
            title_elem = item.select_one("h2 a")
            snippet_elem = item.select_one(".b_caption p")

            if title_elem:
                title = title_elem.get_text(strip=True)
                url = title_elem.get("href", "")

                snippet = ""
                if snippet_elem:
                    snippet = snippet_elem.get_text(strip=True)

                if title and url and not url.startswith("http"):
                    url = "https://www.bing.com" + url

                if url.startswith("http"):
                    results.append({"title": title, "url": url, "snippet": snippet})

                    if len(results) >= max_results:
                        break

        output = {"query": query, "results": results}

        print(json.dumps(output, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--max-results", type=int, default=5)
    args = parser.parse_args()
    search(args.query, args.max_results)
