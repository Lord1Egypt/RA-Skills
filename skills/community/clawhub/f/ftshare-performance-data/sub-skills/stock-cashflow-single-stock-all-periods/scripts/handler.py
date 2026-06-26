#!/usr/bin/env python3
"""查询单只股票所有报告期的现金流量表"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = "https://market.ft.tech"


def main():
    parser = argparse.ArgumentParser(description="查询单只股票历期现金流量表")
    parser.add_argument("--stock-code", required=True, help="股票代码，含市场后缀，如 603323.SH")
    args = parser.parse_args()

    params = {"stock_code": args.stock_code}
    url = f"{BASE_URL}/data/api/v1/market/data/finance/cashflow?" + urllib.parse.urlencode(params)

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
