#!/usr/bin/env python3
"""查询单只股票/基金/指数信息（ftai.chat）"""
import argparse
import json
import sys
import urllib.error
import urllib.request

BASE_URL = "https://ftai.chat"


def main():
    parser = argparse.ArgumentParser(description="查询单只股票/基金/指数信息")
    parser.add_argument("--symbol", required=True, help="标的代码，带市场后缀，如 600519.SH")
    args = parser.parse_args()

    url = f"{BASE_URL}/api/v1/market/security/{args.symbol}/info"

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
