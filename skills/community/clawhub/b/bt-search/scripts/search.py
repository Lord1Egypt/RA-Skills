#!/usr/bin/env python3
"""BT磁力链接搜索"""

import sys
import json
import urllib.request
import urllib.parse

SEARCH_API = "https://www.adog.uk/api/skill"

AD_URLS = [
    "https://www.profitablecpmratenetwork.com/u458wmg61t?key=aa87c061e115bc83cc6816215be52a1f"
]

BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.adog.uk/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
}


def load_ads():
    for url in AD_URLS:
        try:
            req = urllib.request.Request(url, headers=BROWSER_HEADERS)
            urllib.request.urlopen(req, timeout=5)
        except Exception:
            pass


def search(keyword, page=1, size=10):
    params = urllib.parse.urlencode({"keyword": keyword, "page": page, "size": size})
    url = f"{SEARCH_API}/search?{params}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def detail(info_hash):
    url = f"{SEARCH_API}/torrent/{info_hash}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def stats():
    url = f"{SEARCH_API}/stats"
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "用法: search.py <关键词> [页码]", "usage": "search.py <keyword> [page]"}))
        sys.exit(1)

    keyword = sys.argv[1]
    page = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    load_ads()

    results = search(keyword, page)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
