#!/usr/bin/env python3
import json
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from html import unescape


def fetch_json(query: str):
    params = urllib.parse.urlencode(
        {
            "q": query,
            "format": "json",
            "no_redirect": 1,
            "no_html": 1,
            "skip_disambig": 0,
        }
    )
    url = f"https://api.duckduckgo.com/?{params}"
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.loads(r.read().decode("utf-8", errors="replace"))


def strip_tags(text: str) -> str:
    return unescape(re.sub(r"<.*?>", "", text or "")).strip()


def extract_uddg(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    if "uddg" in qs and qs["uddg"]:
        return urllib.parse.unquote(qs["uddg"][0])
    return url


def fetch_html_results(query: str, max_results: int = 8):
    q = urllib.parse.quote_plus(query)
    url = f"https://duckduckgo.com/html/?q={q}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        html = r.read().decode("utf-8", errors="replace")

    pattern = re.compile(r'<a rel="nofollow" class="result__a" href="(.*?)">(.*?)</a>')
    out = []
    for href, title_html in pattern.findall(html):
        title = strip_tags(title_html)
        real_url = extract_uddg(href)
        if title and real_url:
            out.append((title, real_url))
        if len(out) >= max_results:
            break
    return out


def open_url(url: str):
    cmds = [
        ["brave-browser", url],
        ["xdg-open", url],
    ]
    for cmd in cmds:
        try:
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return cmd[0]
        except Exception:
            continue
    return None


def parse_args(argv):
    open_first = False
    parts = []
    for a in argv:
        if a == "--open":
            open_first = True
        else:
            parts.append(a)
    return open_first, " ".join(parts).strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: ddg_search.py [--open] <query>")
        sys.exit(1)

    open_first, query = parse_args(sys.argv[1:])
    if not query:
        print("Usage: ddg_search.py [--open] <query>")
        sys.exit(1)

    print(f"Query: {query}\n")

    data = fetch_json(query)

    abstract = (data.get("AbstractText") or "").strip()
    abstract_url = (data.get("AbstractURL") or "").strip()
    heading = (data.get("Heading") or "").strip()

    if heading:
        print(f"Top: {heading}")
    if abstract:
        print(abstract)
    if abstract_url:
        print(f"Source: {abstract_url}")

    related = data.get("RelatedTopics") or []
    flattened = []
    for item in related:
        if isinstance(item, dict) and "Topics" in item:
            flattened.extend(item.get("Topics") or [])
        else:
            flattened.append(item)

    shown_related = 0
    if flattened:
        print("\nRelated:")
    for item in flattened:
        if shown_related >= 5:
            break
        text = (item.get("Text") or "").strip() if isinstance(item, dict) else ""
        first_url = (item.get("FirstURL") or "").strip() if isinstance(item, dict) else ""
        if not text:
            continue
        shown_related += 1
        print(f"{shown_related}. {text}")
        if first_url:
            print(f"   {first_url}")

    weak = not abstract and shown_related == 0
    if weak:
        print("No strong instant-answer result found.")
        try:
            html_results = fetch_html_results(query, max_results=8)
            if html_results:
                print("\nWeb results (fallback):")
                for i, (title, link) in enumerate(html_results, 1):
                    print(f"{i}. {title}")
                    print(f"   {link}")
                if open_first:
                    opener = open_url(html_results[0][1])
                    if opener:
                        print(f"\nOpened top result via: {opener}")
                    else:
                        print("\nCould not auto-open browser.")
            else:
                print("No fallback results found.")
        except Exception as e:
            print(f"Fallback search failed: {e}")
    elif open_first and abstract_url:
        opener = open_url(abstract_url)
        if opener:
            print(f"\nOpened source via: {opener}")
        else:
            print("\nCould not auto-open browser.")


if __name__ == "__main__":
    main()
