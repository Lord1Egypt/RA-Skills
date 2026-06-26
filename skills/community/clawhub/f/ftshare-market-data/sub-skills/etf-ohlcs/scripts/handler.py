#!/usr/bin/env python3
"""查询单只 ETF OHLC K 线（market.ft.tech）"""
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


SPAN_CHOICES = ("DAY1", "WEEK1", "MONTH1", "YEAR1")


def ms_to_iso(ms: Optional[int]) -> Optional[str]:
    """将毫秒时间戳转为北京时间 ISO 字符串（YYYY-MM-DDTHH:mm:ss）。"""
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000.0, tz=BEIJING_TZ).strftime("%Y-%m-%dT%H:%M:%S")


def with_iso_timestamps(data: dict) -> dict:
    """将 ohlcs 的 otm/ctm、ma5/ma10/ma20 的 ctm 转为北京时间 ISO 字符串（原地修改）。"""
    for o in data.get("ohlcs", []):
        if "otm" in o:
            o["otm"] = ms_to_iso(o["otm"])
        if "ctm" in o:
            o["ctm"] = ms_to_iso(o["ctm"])
    for key in ("ma5", "ma10", "ma20"):
        for m in data.get(key, []):
            if "ctm" in m:
                m["ctm"] = ms_to_iso(m["ctm"])
    return data


def main():
    parser = argparse.ArgumentParser(description="查询单只 ETF OHLC K 线")
    parser.add_argument(
        "--etf",
        required=True,
        help="ETF 标的键，带市场后缀，如 510050.XSHG、159915.XSHE、920036.BJ",
    )
    parser.add_argument(
        "--span",
        required=True,
        choices=SPAN_CHOICES,
        help="K 线周期：DAY1（日线）、WEEK1（周线）、MONTH1（月线）、YEAR1（年线）",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="返回 K 线根数上限，建议不超过 2000",
    )
    parser.add_argument(
        "--until_ts_ms",
        type=int,
        default=None,
        help="截止时间戳（毫秒），不传则截止到当前",
    )
    args = parser.parse_args()

    params = {"span": args.span}
    if args.limit is not None:
        params["limit"] = args.limit
    if args.until_ts_ms is not None:
        params["until_ts_ms"] = args.until_ts_ms

    path = f"/app/api/v2/etfs/{args.etf}/ohlcs?" + urllib.parse.urlencode(params)
    url = BASE_URL + path

    req = urllib.request.Request(url, method="GET")
    req.add_header("X-Client-Name", "ft-claw")
    req.add_header("Content-Type", "application/json")

    try:
        with safe_urlopen(req) as resp:
            data = json.loads(resp.read().decode())
        with_iso_timestamps(data)
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
