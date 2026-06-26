#!/usr/bin/env python3
"""查询单标的历史 K 线（支持可转债，market.ft.tech）"""
import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from typing import Optional

BASE_URL = "https://market.ft.tech"
BEIJING_TZ = timezone(timedelta(hours=8))


def ms_to_iso(ms: Optional[int]) -> Optional[str]:
    """将毫秒时间戳转为北京时间 ISO 字符串（YYYY-MM-DDTHH:mm:ss）。"""
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000.0, tz=BEIJING_TZ).strftime("%Y-%m-%dT%H:%M:%S")


def with_iso_timestamps(result: list) -> list:
    """将每根 K 线的 ts_millis、ts_millis_open 转为北京时间 ISO 字符串（原地修改）。"""
    for o in result:
        if "ts_millis" in o:
            o["ts_millis"] = ms_to_iso(o["ts_millis"])
        if "ts_millis_open" in o:
            o["ts_millis_open"] = ms_to_iso(o["ts_millis_open"])
    return result


def main():
    parser = argparse.ArgumentParser(description="查询单标的历史 K 线（支持可转债）")
    parser.add_argument(
        "--symbol",
        required=True,
        help="标的代码，带交易所后缀，如 110070.XSHG、113050.XSHG、123045.XSHE",
    )
    parser.add_argument(
        "--interval-unit",
        required=True,
        choices=["Minute", "Minute5", "Day", "Week", "Month", "Year"],
        help="K 线周期单位（首字母大写）",
    )
    parser.add_argument(
        "--since-ts-millis",
        required=True,
        type=int,
        help="开始时间戳（毫秒）；若用北京时间，请求前先转为毫秒（东八区）",
    )
    parser.add_argument(
        "--until-ts-millis",
        required=True,
        type=int,
        help="结束时间戳（毫秒，闭区间）",
    )
    parser.add_argument(
        "--interval-value",
        type=int,
        default=None,
        help="间隔数值，与 interval_unit 配合（可选）",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="返回 K 线根数上限（可选）",
    )
    parser.add_argument(
        "--adjust-kind",
        choices=["null", "None", "Forward", "Backward"],
        default="null",
        help="复权类型：null/None=除权，Forward=前复权，Backward=后复权（默认 null）",
    )
    args = parser.parse_args()

    body = {
        "symbol": args.symbol,
        "interval_unit": args.interval_unit,
        "since_ts_millis": args.since_ts_millis,
        "until_ts_millis": args.until_ts_millis,
    }
    if args.interval_value is not None:
        body["interval_value"] = args.interval_value
    if args.limit is not None:
        body["limit"] = args.limit
    if args.adjust_kind in ("null", "None"):
        body["adjust_kind"] = None
    else:
        body["adjust_kind"] = args.adjust_kind

    url = BASE_URL + "/data/api/v1/market/data/stock-candlesticks"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
        if isinstance(result, list):
            with_iso_timestamps(result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except urllib.error.HTTPError as e:
        body_read = e.read().decode()
        print(body_read, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
