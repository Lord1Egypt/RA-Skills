#!/usr/bin/env python3
"""查询 A 股指定日期全市场公告（分页）"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://market.ft.tech"


def main():
    parser = argparse.ArgumentParser(description="查询指定日期全市场公告（分页）")
    parser.add_argument("--start-date", required=True, help="查询日期，格式 YYYYMMDD，仅支持单日查询")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始（默认 1）")
    parser.add_argument("--page-size", type=int, default=20, help="每页记录数（默认 20）")
    args = parser.parse_args()

    params = {
        "start_date": args.start_date,
        "end_date": args.start_date,
        "type": "stock",
        "page": args.page,
        "page_size": args.page_size,
    }
    url = f"{BASE_URL}/data/api/v1/market/data/announcements/stock-announcements?" + urllib.parse.urlencode(params)

    try:
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read().decode())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
