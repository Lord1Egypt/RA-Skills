#!/usr/bin/env python3
"""查询期货 K 线（market.ft.tech）"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

SAFE_URLOPENER = urllib.request.build_opener()
BASE_URL = "https://market.ft.tech"
ENDPOINT = "/data/api/v1/market/data/futures/kline"


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
    parser = argparse.ArgumentParser(description="查询期货 K 线")
    parser.add_argument(
        "--symbol",
        required=True,
        help="WIND 合约全码，如 A2605.DCE（大小写不敏感）",
    )
    parser.add_argument(
        "--interval",
        default=None,
        help="K 线周期，如 1min/5min/15min/30min/60min/daily/weekly/monthly/quarterly/yearly",
    )
    parser.add_argument(
        "--start",
        type=int,
        default=None,
        help="起始时间（毫秒时间戳）",
    )
    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="结束时间（毫秒时间戳，闭区间）",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="最大返回条数（默认 500）",
    )
    args = parser.parse_args()

    if (args.start is None) ^ (args.end is None):
        print("start 和 end 需同时传入，禁止只传一个", file=sys.stderr)
        sys.exit(1)
    if args.start is not None:
        if args.start < 0 or args.end < 0:
            print("start/end 需为非负毫秒时间戳", file=sys.stderr)
            sys.exit(1)
        if args.start > args.end:
            print("start 不能大于 end", file=sys.stderr)
            sys.exit(1)
        # 与其他 skill 保持一致，约束为毫秒级时间戳（至少 13 位）
        if len(str(args.start)) < 13 or len(str(args.end)) < 13:
            print("start/end 需为毫秒时间戳（建议 13 位）", file=sys.stderr)
            sys.exit(1)

    params = {"symbol": args.symbol.strip().upper()}
    if not params["symbol"]:
        print("symbol 不能为空", file=sys.stderr)
        sys.exit(1)

    if args.interval is not None and args.interval.strip() != "":
        params["interval"] = args.interval.strip()
    if args.start is not None:
        params["start"] = args.start
        params["end"] = args.end
    if args.limit is not None:
        if args.limit <= 0:
            print("limit 必须为正整数", file=sys.stderr)
            sys.exit(1)
        params["limit"] = args.limit

    url = BASE_URL + ENDPOINT + "?" + urllib.parse.urlencode(params)
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
