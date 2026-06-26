#!/usr/bin/env python3
"""查询单只可转债基础信息（market.ft.tech）"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://market.ft.tech"


def main():
    parser = argparse.ArgumentParser(description="查询可转债基础信息")
    parser.add_argument(
        "--symbol_code",
        required=True,
        help="转债代码，可带交易所后缀，如 110070.SH 或 110070",
    )
    args = parser.parse_args()

    path = "/data/api/v1/market/data/cb/cb-base-data"
    url = BASE_URL + path + "?" + urllib.parse.urlencode({"symbol_code": args.symbol_code})

    req = urllib.request.Request(url, method="GET")

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
