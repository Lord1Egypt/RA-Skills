#!/usr/bin/env python3
"""查询指定交易日期货合约列表（market.ft.tech）"""
import argparse
from datetime import datetime
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

SAFE_URLOPENER = urllib.request.build_opener()
BASE_URL = "https://market.ft.tech"
ENDPOINT = "/data/api/v1/market/data/futures/futures-lists"


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
    parser = argparse.ArgumentParser(description="查询指定交易日期货合约列表")
    parser.add_argument(
        "--trade-date",
        dest="trade_date",
        type=int,
        default=None,
        help="交易日（YYYYMMDD），不传默认前一交易日（CST）",
    )
    args = parser.parse_args()
    if args.trade_date is not None:
        td = str(args.trade_date)
        if len(td) != 8:
            print("trade-date 格式错误，需为 YYYYMMDD", file=sys.stderr)
            sys.exit(1)
        try:
            datetime.strptime(td, "%Y%m%d")
        except ValueError:
            print("trade-date 非法日期，需为真实 YYYYMMDD", file=sys.stderr)
            sys.exit(1)

    params = {}
    if args.trade_date is not None:
        params["trade_date"] = args.trade_date

    if params:
        url = BASE_URL + ENDPOINT + "?" + urllib.parse.urlencode(params)
    else:
        url = BASE_URL + ENDPOINT

    req = urllib.request.Request(url, method="GET")

    try:
        with safe_urlopen(req) as resp:
            raw = resp.read().decode(errors="replace")
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                print(raw, file=sys.stderr)
                sys.exit(1)
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"请求失败: {e.reason}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
