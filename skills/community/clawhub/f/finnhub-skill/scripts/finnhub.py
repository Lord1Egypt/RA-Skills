#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

DEFAULT_BASE_URL = os.environ.get("FINNHUB_BASE_URL", "https://finnhub.io/api/v1")
ALLOWED_HOSTS = {"finnhub.io", "www.finnhub.io"}


def fail(msg: str, code: int = 1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def redact(text: str) -> str:
    return re.sub(r"token=[^&\s]+", "token=REDACTED", text)


def get_api_key() -> str:
    api_key = os.environ.get("FINNHUB_API_KEY")
    if not api_key:
        fail("FINNHUB_API_KEY is not set")
    return api_key


def get_base_url() -> str:
    base_url = os.environ.get("FINNHUB_BASE_URL", DEFAULT_BASE_URL)
    parsed = urllib.parse.urlparse(base_url)
    if parsed.scheme != "https":
        fail("FINNHUB_BASE_URL must use https")
    if parsed.hostname not in ALLOWED_HOSTS:
        fail("FINNHUB_BASE_URL host is not allowed; use official Finnhub domain only")
    return base_url.rstrip("/")


def request_json(path: str, params: dict):
    api_key = get_api_key()
    base_url = get_base_url()
    params = {k: v for k, v in params.items() if v is not None and v != ""}
    params["token"] = api_key
    url = f"{base_url}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "finnhub-skill/0.2"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        fail(f"Finnhub HTTP error {e.code}: {redact(body or str(e))}")
    except urllib.error.URLError as e:
        fail(f"Finnhub network error: {redact(str(e))}")
    except json.JSONDecodeError:
        fail("Finnhub returned non-JSON response")


def dump(data, raw=False):
    if raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))


def fmt_ts(ts):
    if not ts:
        return "N/A"
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def cmd_quote(args):
    data = request_json("/quote", {"symbol": args.symbol})
    if args.raw:
        return dump(data, raw=True)
    print(f"{args.symbol} quote")
    print(f"- current: {data.get('c')}")
    print(f"- change: {data.get('d')} ({data.get('dp')}%)")
    print(f"- high / low: {data.get('h')} / {data.get('l')}")
    print(f"- open / prev close: {data.get('o')} / {data.get('pc')}")
    print(f"- time: {fmt_ts(data.get('t'))}")


def cmd_candles(args):
    data = request_json(
        "/stock/candle",
        {
            "symbol": args.symbol,
            "resolution": args.resolution,
            "from": args.from_ts,
            "to": args.to_ts,
        },
    )
    if args.raw:
        return dump(data, raw=True)
    closes = data.get("c") or []
    opens = data.get("o") or []
    highs = data.get("h") or []
    lows = data.get("l") or []
    volumes = data.get("v") or []
    timestamps = data.get("t") or []
    print(f"{args.symbol} candles")
    print(f"- resolution: {args.resolution}")
    print(f"- window: {fmt_ts(args.from_ts)} -> {fmt_ts(args.to_ts)}")
    print(f"- candles returned: {len(closes)}")
    if closes:
        print("- latest candle:")
        print(f"  - time: {fmt_ts(timestamps[-1])}")
        print(f"  - open/high/low/close: {opens[-1]} / {highs[-1]} / {lows[-1]} / {closes[-1]}")
        print(f"  - volume: {volumes[-1]}")


def cmd_profile(args):
    data = request_json("/stock/profile2", {"symbol": args.symbol})
    if args.raw:
        return dump(data, raw=True)
    print(f"{args.symbol} company profile")
    print(f"- name: {data.get('name')}")
    print(f"- exchange: {data.get('exchange')}")
    print(f"- country / currency: {data.get('country')} / {data.get('currency')}")
    print(f"- industry: {data.get('finnhubIndustry')}")
    print(f"- market cap: {data.get('marketCapitalization')}")
    print(f"- IPO date: {data.get('ipo')}")
    print(f"- website: {data.get('weburl')}")


def cmd_company_news(args):
    data = request_json(
        "/company-news",
        {"symbol": args.symbol, "from": args.date_from, "to": args.date_to},
    )
    if args.raw:
        return dump(data, raw=True)
    print(f"{args.symbol} company news")
    print(f"- range: {args.date_from} -> {args.date_to}")
    print(f"- articles: {len(data)}")
    for item in data[:5]:
        print(f"  - {item.get('headline')} | {item.get('source')} | {fmt_ts(item.get('datetime'))}")
        print(f"    {item.get('url')}")


def cmd_market_news(args):
    data = request_json("/news", {"category": args.category})
    if args.raw:
        return dump(data, raw=True)
    print(f"market news ({args.category})")
    print(f"- articles: {len(data)}")
    for item in data[:5]:
        print(f"  - {item.get('headline')} | {item.get('source')} | {fmt_ts(item.get('datetime'))}")
        print(f"    {item.get('url')}")


def cmd_earnings(args):
    data = request_json(
        "/calendar/earnings",
        {"from": args.date_from, "to": args.date_to, "symbol": args.symbol},
    )
    if args.raw:
        return dump(data, raw=True)
    earnings = data.get("earningsCalendar") or []
    print("earnings calendar")
    print(f"- range: {args.date_from} -> {args.date_to}")
    print(f"- items: {len(earnings)}")
    for item in earnings[:10]:
        print(f"  - {item.get('symbol')} | {item.get('date')} | EPS est: {item.get('epsEstimate')} | revenue est: {item.get('revenueEstimate')}")


def cmd_economic(args):
    data = request_json(
        "/calendar/economic",
        {"from": args.date_from, "to": args.date_to},
    )
    if args.raw:
        return dump(data, raw=True)
    items = data.get("economicCalendar") or []
    print("economic calendar")
    print(f"- range: {args.date_from} -> {args.date_to}")
    print(f"- items: {len(items)}")
    for item in items[:10]:
        print(f"  - {item.get('event')} | {item.get('country')} | {item.get('time')} | actual: {item.get('actual')} | estimate: {item.get('estimate')}")


def build_parser():
    parser = argparse.ArgumentParser(description="Finnhub read-only client")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("quote")
    p.add_argument("--symbol", required=True)
    p.add_argument("--raw", action="store_true")
    p.set_defaults(func=cmd_quote)

    p = sub.add_parser("candles")
    p.add_argument("--symbol", required=True)
    p.add_argument("--resolution", required=True)
    p.add_argument("--from-ts", required=True, type=int)
    p.add_argument("--to-ts", required=True, type=int)
    p.add_argument("--raw", action="store_true")
    p.set_defaults(func=cmd_candles)

    p = sub.add_parser("profile")
    p.add_argument("--symbol", required=True)
    p.add_argument("--raw", action="store_true")
    p.set_defaults(func=cmd_profile)

    p = sub.add_parser("company-news")
    p.add_argument("--symbol", required=True)
    p.add_argument("--date-from", required=True)
    p.add_argument("--date-to", required=True)
    p.add_argument("--raw", action="store_true")
    p.set_defaults(func=cmd_company_news)

    p = sub.add_parser("market-news")
    p.add_argument("--category", default="general")
    p.add_argument("--raw", action="store_true")
    p.set_defaults(func=cmd_market_news)

    p = sub.add_parser("earnings")
    p.add_argument("--date-from", required=True)
    p.add_argument("--date-to", required=True)
    p.add_argument("--symbol")
    p.add_argument("--raw", action="store_true")
    p.set_defaults(func=cmd_earnings)

    p = sub.add_parser("economic")
    p.add_argument("--date-from", required=True)
    p.add_argument("--date-to", required=True)
    p.add_argument("--raw", action="store_true")
    p.set_defaults(func=cmd_economic)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
