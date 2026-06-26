#!/usr/bin/env python3
"""指数分页列表（market.ft.tech）：分页、排序、筛选"""
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
    parser = argparse.ArgumentParser(description="指数分页列表，支持排序、筛选、分页")
    parser.add_argument(
        "--order_by",
        default=None,
        help="排序方式，如 change_rate desc、name asc",
    )
    parser.add_argument(
        "--ob",
        default=None,
        help="与 order_by 同义",
    )
    parser.add_argument(
        "--filter",
        default=None,
        help="过滤条件表达式，如 change_rate != null、name ~ \"上证\"",
    )
    parser.add_argument(
        "--masks",
        default=None,
        help="字段掩码，逗号分隔，如 name,symkey,latest,change_rate",
    )
    parser.add_argument(
        "--page_size",
        type=int,
        default=None,
        help="每页条数，不传则不分页",
    )
    parser.add_argument(
        "--page_no",
        type=int,
        default=None,
        help="页码，从 1 开始",
    )
    args = parser.parse_args()

    params = {}
    if args.order_by is not None:
        params["order_by"] = args.order_by
    elif args.ob is not None:
        params["ob"] = args.ob
    if args.filter is not None:
        params["filter"] = args.filter
    if args.masks is not None:
        params["masks"] = args.masks
    if args.page_size is not None:
        params["page_size"] = args.page_size
    if args.page_no is not None:
        params["page_no"] = args.page_no

    path = "/app/api/v2/indices"
    if params:
        path += "?" + urllib.parse.urlencode(params)
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
