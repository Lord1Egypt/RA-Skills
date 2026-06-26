#!/usr/bin/env python3
"""获取可转债全量列表（market.ft.tech）"""
import json
import sys
import urllib.error
import urllib.request

BASE_URL = "https://market.ft.tech"


def main():
    url = BASE_URL + "/data/api/v1/market/data/cb/cb-lists"
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
