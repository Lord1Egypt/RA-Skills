#!/usr/bin/env python3
"""查询所有基金概览信息（分页）"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = "https://market.ft.tech"


def main():
    parser = argparse.ArgumentParser(description="查询所有基金概览信息（分页）")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始（默认 1）")
    parser.add_argument("--page-size", type=int, default=20, help="每页记录数，最大 1000（默认 20）")
    args = parser.parse_args()

    params = {"page": args.page, "page_size": args.page_size}
    url = f"{BASE_URL}/data/api/v1/market/data/fund/fund-overview?" + urllib.parse.urlencode(params)

    try:
        with SAFE_URLOPENER.open(url) as resp:
            data = json.loads(resp.read().decode())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(body, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
