#!/usr/bin/env python3
"""查询指定基金的基础信息"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = "https://market.ft.tech"


def main():
    parser = argparse.ArgumentParser(description="查询指定基金基础信息")
    parser.add_argument("--institution-code", required=True, help="6 位数字基金代码，如 000001")
    args = parser.parse_args()

    params = {"institution_code": args.institution_code}
    url = f"{BASE_URL}/data/api/v1/market/data/fund/fund-basicinfo?" + urllib.parse.urlencode(params)

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
