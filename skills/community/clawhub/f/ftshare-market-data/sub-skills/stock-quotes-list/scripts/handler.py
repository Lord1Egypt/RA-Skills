#!/usr/bin/env python3
"""查询 A 股行情列表（分页）"""
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

ENDPOINT = "/app/api/v2/stocks"


def main():
    parser = argparse.ArgumentParser(description="查询 A 股行情列表（分页）")
    parser.add_argument("--order_by", required=True, help='排序规则，如 change_rate desc')
    parser.add_argument("--page_no", type=int, required=True, help="页码，从 1 开始")
    parser.add_argument("--page_size", type=int, required=True, help="每页记录数")
    parser.add_argument("--filter", default="", help="筛选条件表达式，可选")
    parser.add_argument("--masks", default="", help="返回字段掩码，可选")
    args = parser.parse_args()

    params = {
        "order_by": args.order_by,
        "page_no": args.page_no,
        "page_size": args.page_size,
    }
    if args.filter:
        params["filter"] = args.filter
    if args.masks:
        params["masks"] = args.masks

    url = f"{BASE_URL}{ENDPOINT}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"X-Client-Name": "ft-claw"})

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
