#!/usr/bin/env python3
"""查询单只 ETF 分钟级分时价格（market.ft.tech）"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Optional
SAFE_URLOPENER = urllib.request.build_opener()

BEIJING_TZ = timezone(timedelta(hours=8))

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



def tm_ms_to_iso(ms: Optional[int]) -> Optional[str]:
    """将毫秒时间戳转为北京时间 ISO 字符串（YYYY-MM-DDTHH:mm:ss）。"""
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000.0, tz=BEIJING_TZ).strftime("%Y-%m-%dT%H:%M:%S")


def main():
    parser = argparse.ArgumentParser(description="查询单只 ETF 分时价格（一分钟级别）")
    parser.add_argument(
        "--etf",
        required=True,
        help="ETF 标的键，带市场后缀，如 510050.XSHG、159915.XSHE、920036.BJ",
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
        raise ValueError("since 与 since_ts_ms 二选一，必须提供其一")
    if args.since is not None and args.since_ts_ms is not None:
        raise ValueError("since 与 since_ts_ms 二选一，不能同时传递")

    params = {}
    if args.since is not None:
        params["since"] = args.since
    else:
        params["since_ts_ms"] = args.since_ts_ms

    path = f"/app/api/v2/etfs/{args.etf}/prices?" + urllib.parse.urlencode(params)
    url = BASE_URL + path

    req = urllib.request.Request(url, method="GET")
    req.add_header("X-Client-Name", "ft-claw")
    req.add_header("Content-Type", "application/json")

    try:
        with safe_urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        for rec in data.get("prices", []):
            if "tm" in rec:
                rec["tm"] = tm_ms_to_iso(rec["tm"])
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
