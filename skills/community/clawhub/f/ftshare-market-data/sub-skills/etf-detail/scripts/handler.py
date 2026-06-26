#!/usr/bin/env python3
"""查询单只 ETF 详情（market.ft.tech）"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
SAFE_URLOPENER = urllib.request.build_opener()

BASE_URL = "https://market.ft.tech"

def safe_urlopen(req_or_url):
    if isinstance(req_or_url, urllib.request.Request):
        url = req_or_url.full_url
    else:
        url = str(req_or_url)
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.netloc != "market.ft.tech":
        print(f"Invalid URL for safe_urlopen: {url}", file=sys.stderr)
        sys.exit(1)
    return SAFE_URLOPENER.open(req_or_url)



def main():
    parser = argparse.ArgumentParser(description="查询单只 ETF 详情")
    parser.add_argument(
        "--etf",
        required=True,
        help="ETF 标的键，带市场后缀，如 510050.XSHG、159915.XSHE、920036.BJ",
    )
    parser.add_argument(
        "--masks",
        default=None,
        help="可选，字段掩码，逗号分隔，如 name,symkey,latest,change_rate",
    )
    args = parser.parse_args()

    path = f"/app/api/v2/etfs/{args.etf}"
    if args.masks:
        path += "?" + urllib.parse.urlencode({"masks": args.masks})
    url = BASE_URL + path

    req = urllib.request.Request(url, method="GET")
    req.add_header("X-Client-Name", "ft-claw")
    req.add_header("Content-Type", "application/json")

    try:
        with safe_urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
