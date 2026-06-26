#!/usr/bin/env python3
"""查询单只 A 股股票 OHLC K 线数据（含 MA5/MA10/MA20）"""
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

ENDPOINT = "/api/v2/stocks/{stock}/ohlcs"
HEADERS = {
    "X-Client-Name": "ft-claw",
    "Content-Type": "application/json",
}


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


def fetch(stock: str, span: str, limit: Optional[int], until_ts_ms: Optional[int]) -> dict:
    params: dict = {"span": span}
    if limit is not None:
        params["limit"] = limit
    if until_ts_ms is not None:
        params["until_ts_ms"] = until_ts_ms

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
    parser = argparse.ArgumentParser(description="查询单只 A 股股票 OHLC K 线数据")
    parser.add_argument(
        "--stock",
        required=True,
        help="股票标的键，需携带市场后缀，如 688295.XSHG / 000001.SZ / 920036.BJ",
    )
    parser.add_argument(
        "--span",
        required=True,
        choices=["DAY1", "WEEK1", "MONTH1", "YEAR1"],
        help="K 线周期：DAY1（日线）、WEEK1（周线）、MONTH1（月线）、YEAR1（年线）",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="返回 K 线根数上限，建议不超过 2000；不传则返回全部",
    )
    parser.add_argument(
        "--until_ts_ms",
        type=int,
        default=None,
        help="截止时间戳（毫秒），返回该时间点及之前的 K 线；不传则截止到当前",
    )
    args = parser.parse_args()

    result = fetch(args.stock, args.span, args.limit, args.until_ts_ms)
    with_iso_timestamps(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
