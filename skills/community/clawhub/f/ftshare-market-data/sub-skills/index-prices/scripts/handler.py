#!/usr/bin/env python3
"""查询单只指数分钟级分时价格（market.ft.tech）"""
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
    parser = argparse.ArgumentParser(description="查询单只指数分时价格（一分钟级别）")
    parser.add_argument(
        "--index",
        required=True,
        help="指数标的键，带市场后缀，如 000001.XSHG、399001.XSHE、920036.BJ",
    )
    parser.add_argument(
        "--since",
        default=None,
        help="时间范围起点：TODAY、FIVE_DAYS_AGO、TRADE_DAYS_AGO(n)；与 --since_ts_ms 二选一",
    )
    parser.add_argument(
        "--since_ts_ms",
        type=int,
        default=None,
        help="时间范围起点（毫秒时间戳）；不传 since 时必传",
    )
    args = parser.parse_args()

    if args.since is None and args.since_ts_ms is None:
        print("错误：必须指定 --since 或 --since_ts_ms 其一", file=sys.stderr)
        sys.exit(1)
    if args.since is not None and args.since_ts_ms is not None:
        print("错误：--since 与 --since_ts_ms 二选一", file=sys.stderr)
        sys.exit(1)

    params = {}
    if args.since is not None:
        params["since"] = args.since
    else:
        params["since_ts_ms"] = args.since_ts_ms

    path = f"/app/api/v2/indices/{args.index}/prices?" + urllib.parse.urlencode(params)
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
