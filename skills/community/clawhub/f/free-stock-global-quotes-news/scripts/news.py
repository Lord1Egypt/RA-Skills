#!/usr/bin/env python3
"""
Company news: A股/港股 依次 东方财富→AkShare；美股 用 Finnhub (需 FINNHUB_API_KEY).
Usage:
  python3 news.py AAPL
  python3 news.py 600519.SS --limit 5
  python3 news.py 贵州茅台
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
import time
from urllib import request, error

BASE = "https://finnhub.io/api/v1/company-news"
NEWS_RETRIES = 2


def _is_cn_hk_symbol(symbol: str) -> bool:
  s = symbol.strip().upper()
  if s.endswith(".SS") or s.endswith(".SZ") or s.endswith(".HK"):
    return True
  if s.startswith("SH") or s.startswith("SZ") or s.startswith("HK"):
    return True
  if s.isdigit() and len(s) in (5, 6):
    return True
  if any("\u4e00" <= c <= "\u9fff" for c in symbol):
    return True
  return False


def fetch_news(symbol: str, from_date: str, to_date: str) -> list[dict] | None:
    key = os.environ.get("FINNHUB_API_KEY")
    if not key:
        print("FINNHUB_API_KEY not set", file=sys.stderr)
        return None
    url = f"{BASE}?symbol={symbol}&from={from_date}&to={to_date}&token={key}"
    req = request.Request(url, headers={"User-Agent": "OpenClaw/1.0"})
    for attempt in range(1 + NEWS_RETRIES):
        try:
            with request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode())
                return data if isinstance(data, list) else None
        except (error.HTTPError, error.URLError, json.JSONDecodeError, OSError) as e:
            if attempt < NEWS_RETRIES:
                time.sleep(0.5 * (attempt + 1))
                continue
            print(f"Request failed: {e}", file=sys.stderr)
            return None
    return None


def format_item(item: dict, index: int) -> str:
    headline = item.get("headline") or item.get("title") or "(no title)"
    source = item.get("source") or ""
    dt = item.get("datetime")
    if isinstance(dt, (int, float)):
        try:
            dt = datetime.fromtimestamp(dt, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
        except Exception:
            dt = str(dt)
    time_str = f" [{dt}]" if dt else ""
    line = f"{index}. **{headline}**{time_str}"
    if source:
        line += f" — {source}"
    summary = item.get("summary")
    if summary:
        line += f"\n   {summary[:200]}{'…' if len(summary) > 200 else ''}"
    url_link = item.get("url")
    if url_link:
        line += f"\n   {url_link}"
    return line


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Company news: A股/港股 东方财富→AkShare；美股 Finnhub"
    )
    ap.add_argument("symbol", help="Symbol: AAPL, 600519.SS, 贵州茅台, 0700.HK")
    ap.add_argument("--from", dest="from_", metavar="DATE", help="From date (US only)")
    ap.add_argument("--to", dest="to_", metavar="DATE", help="To date (US only)")
    ap.add_argument("--limit", type=int, default=10, help="Max items (default 10)")
    ap.add_argument("--json", action="store_true", help="Output raw JSON")
    args = ap.parse_args()

    # A股/港股：东方财富 → AkShare，直到某个可用即停
    if _is_cn_hk_symbol(args.symbol):
        import importlib.util
        _dir = os.path.dirname(os.path.abspath(__file__))
        _spec = importlib.util.spec_from_file_location("cn_news", os.path.join(_dir, "cn_news.py"))
        _mod = importlib.util.module_from_spec(_spec)
        if _spec and _spec.loader:
            _spec.loader.exec_module(_mod)
        else:
            import cn_news as _mod  # type: ignore
        provider, items = _mod.fetch_cn_news(args.symbol, limit=args.limit)
        if args.json:
            print(json.dumps(items, ensure_ascii=False, indent=2, default=str))
            return
        if not items:
            print(f"{args.symbol}: 未从 东方财富/AkShare 获取到新闻。（A 股/港股可尝试安装 akshare；港股个股新闻可能为空。）")
            sys.exit(1)
        print(f"**{args.symbol}** 新闻 (来源: {provider})\n")
        for i, item in enumerate(items, 1):
            print(_mod.format_item(item, i))
            print()
        return

    # 美股：Finnhub
    today = datetime.now(timezone.utc).date()
    from_date = args.from_ or (today - timedelta(days=7)).strftime("%Y-%m-%d")
    to_date = args.to_ or today.strftime("%Y-%m-%d")

    items = fetch_news(args.symbol, from_date, to_date)
    if items is None:
        sys.exit(1)
    items = items[: args.limit]

    if args.json:
        print(json.dumps(items, indent=2, default=str))
        return
    if not items:
        print(f"No news for {args.symbol} between {from_date} and {to_date}.")
        return
    print(f"**{args.symbol}** 新闻 ({from_date} ~ {to_date})\n")
    for i, item in enumerate(items, 1):
        print(format_item(item, i))
        print()


if __name__ == "__main__":
    main()
    sys.exit(0)
