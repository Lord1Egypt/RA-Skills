#!/usr/bin/env python3
"""查询单只股票所有报告期的业绩快报（分页）"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = "https://market.ft.tech"


def main():
    parser = argparse.ArgumentParser(description="查询单只股票历期业绩快报（分页）")
    parser.add_argument("--stock-code", required=True, help="股票代码，含市场后缀，如 603323.SH")
    parser.add_argument("--page", type=int, default=1, help="页码，从 1 开始（默认 1）")
    parser.add_argument("--page-size", type=int, default=50, help="每页记录数（默认 50）")
    args = parser.parse_args()

    params = {"stock_code": args.stock_code, "page": args.page, "page_size": args.page_size}
    url = f"{BASE_URL}/data/api/v1/market/data/finance/stock-performance-express?" + urllib.parse.urlencode(params)

    try:
        with SAFE_URLOPENER.open(url) as resp:
            data = json.loads(resp.read().decode())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
