#!/usr/bin/env python3
"""中国货币供应量 M0/M1/M2（月度）"""
import json
import sys
import urllib.error
import urllib.request

BASE_URL = "https://market.ft.tech"


def main():
    url = f"{BASE_URL}/data/api/v1/market/data/economic/china-money-supply"

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
