#!/usr/bin/env python3
"""获取 A 股 IPO 列表，支持分页与全量拉取"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://market.ft.tech"
ENDPOINT = "/data/api/v1/market/data/stock-ipos"


def fetch_page(page: int, page_size: int) -> dict:
    params = urllib.parse.urlencode({"page": page, "page_size": page_size})
    url = f"{BASE_URL}{ENDPOINT}?{params}"
    try:
        with urllib.request.urlopen(url) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="获取 A 股 IPO 列表")
    parser.add_argument("--page", type=int, default=1, help="页码（从 1 开始）")
    parser.add_argument("--page_size", type=int, default=20, help="每页记录数")
    parser.add_argument("--all", action="store_true", dest="fetch_all", help="自动翻页获取全量数据")
    args = parser.parse_args()

    if args.fetch_all:
        first = fetch_page(1, args.page_size)
        all_items = list(first.get("items", []))
        total_pages = first.get("total_pages", 1)
        for p in range(2, total_pages + 1):
            page_data = fetch_page(p, args.page_size)
            all_items.extend(page_data.get("items", []))
        result = {
            "items": all_items,
            "total_pages": total_pages,
            "total_items": first.get("total_items", len(all_items)),
        }
    else:
        result = fetch_page(args.page, args.page_size)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
