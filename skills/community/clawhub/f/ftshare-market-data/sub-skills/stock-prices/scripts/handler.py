#!/usr/bin/env python3
"""查询单只 A 股股票分时价格（一分钟级别）"""
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

BASE_URL = "https://market.ft.tech/app"

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

ENDPOINT = "/api/v2/stocks/{stock}/prices"
HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}


def tm_ms_to_iso(ms: Optional[int]) -> Optional[str]:
    """将毫秒时间戳转为北京时间 ISO 字符串（YYYY-MM-DDTHH:mm:ss）。"""
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000.0, tz=BEIJING_TZ).strftime("%Y-%m-%dT%H:%M:%S")


def fetch(stock: str, since: Optional[str], since_ts_ms: Optional[int]) -> dict:
    if since is None and since_ts_ms is None:
        raise ValueError("since 与 since_ts_ms 二选一，必须提供其一")
    if since is not None and since_ts_ms is not None:
        raise ValueError("since 与 since_ts_ms 二选一，不能同时传递")

    params: dict = {}
    if since is not None:
        params["since"] = since
    else:
        params["since_ts_ms"] = since_ts_ms

    url = f"{BASE_URL}{ENDPOINT.format(stock=stock)}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with safe_urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="查询单只 A 股股票分时价格（一分钟级别）")
    parser.add_argument(
        "--stock",
        required=True,
        help="股票标的键，需携带市场后缀，如 688295.XSHG / 000001.SZ / 920036.BJ",
    )
    parser.add_argument(
        "--since",
        default=None,
        help="时间范围起点（语义）：TODAY、FIVE_DAYS_AGO、TRADE_DAYS_AGO(n)；与 since_ts_ms 二选一",
    )
    parser.add_argument(
        "--since_ts_ms",
        type=int,
        default=None,
        help="时间范围起点（毫秒时间戳）；不传 since 时必传；与 since 二选一",
    )
    args = parser.parse_args()

    try:
        result = fetch(args.stock, args.since, args.since_ts_ms)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    for rec in result.get("prices", []):
        if "tm" in rec:
            rec["tm"] = tm_ms_to_iso(rec["tm"])
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
