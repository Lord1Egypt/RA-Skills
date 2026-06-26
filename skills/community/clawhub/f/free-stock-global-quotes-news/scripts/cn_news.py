#!/usr/bin/env python3
"""
A-share / HK stock news: try 东方财富 (direct API if available) then AkShare.
Data source is 东方财富; AkShare wraps it. Stops at first provider that returns data.

Usage:
  python3 cn_news.py 600519.SS
  python3 cn_news.py 000001.SZ
  python3 cn_news.py 贵州茅台
  python3 cn_news.py 0700.HK --limit 5
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, List, Optional, Tuple


def _parse_symbol(raw: str) -> Tuple[str, str]:
  """Return (market, code_or_name). market: 'sh'|'sz'|'hk'|'name'."""
  s = raw.strip().upper()
  if s.endswith(".SS") or s.startswith("SH"):
    code = s[:-3] if s.endswith(".SS") else s[2:]
    return "sh", code
  if s.endswith(".SZ") or s.startswith("SZ"):
    code = s[:-3] if s.endswith(".SZ") else s[2:]
    return "sz", code
  if s.endswith(".HK") or s.startswith("HK"):
    code = (s[:-3] if s.endswith(".HK") else s[2:]).zfill(5)
    return "hk", code
  if s.isdigit() and len(s) in (5, 6):
    code = s.zfill(6)
    return ("sh" if code.startswith("6") else "sz", code)
  return "name", raw.strip()


def _fetch_from_akshare(symbol: str, limit: int) -> List[dict]:
  """Fetch A-share news via AkShare (东方财富 data). HK may not be supported."""
  try:
    import akshare as ak  # type: ignore
  except Exception:
    return []

  market, code_or_name = _parse_symbol(symbol)
  # AkShare stock_news_em(symbol=) accepts 股票代码 or 名称
  try:
    df = ak.stock_news_em(symbol=code_or_name)
  except Exception:
    return []

  if df is None or df.empty:
    return []

  # Normalize to common shape: title, summary, time, source, url
  out: List[dict] = []
  for _, row in df.head(limit).iterrows():
    out.append({
      "headline": row.get("新闻标题") or row.get("title", ""),
      "summary": row.get("新闻内容") or row.get("summary", ""),
      "datetime": row.get("发布时间") or row.get("showTime", ""),
      "source": row.get("文章来源") or row.get("mediaName", ""),
      "url": row.get("新闻链接") or row.get("url", ""),
    })
  return out


def fetch_cn_news(symbol: str, limit: int = 10) -> Tuple[str, List[dict]]:
  """
  Try 东方财富 then AkShare. Returns (provider_used, list of items).
  Each item: headline, summary, datetime, source, url.
  """
  # 1) 东方财富 direct API: no stable public API found for 个股新闻; skip.
  # 2) AkShare (东方财富 data)
  items = _fetch_from_akshare(symbol, limit)
  if items:
    return ("AkShare(东方财富)", items)
  return ("", [])


def format_item(item: dict, index: int) -> str:
  headline = item.get("headline") or item.get("title") or "(无标题)"
  source = item.get("source") or ""
  dt = item.get("datetime") or ""
  time_str = f" [{dt}]" if dt else ""
  line = f"{index}. **{headline}**{time_str}"
  if source:
    line += f" — {source}"
  summary = item.get("summary") or item.get("新闻内容") or ""
  if summary:
    line += f"\n   {summary[:200]}{'…' if len(summary) > 200 else ''}"
  url = item.get("url") or item.get("新闻链接") or ""
  if url:
    line += f"\n   {url}"
  return line


def main() -> None:
  ap = argparse.ArgumentParser(
    description="A股/港股新闻：东方财富 → AkShare，直到某个可用即停。"
  )
  ap.add_argument("symbol", help="标的：600519.SS、000001.SZ、贵州茅台、0700.HK")
  ap.add_argument("--limit", type=int, default=10, help="最多条数 (默认 10)")
  ap.add_argument("--json", action="store_true", help="输出原始 JSON")
  args = ap.parse_args()

  provider, items = fetch_cn_news(args.symbol, limit=args.limit)

  if args.json:
    print(json.dumps(items, ensure_ascii=False, indent=2, default=str))
    return

  if not items:
    print(f"{args.symbol}: 未从 东方财富/AkShare 获取到新闻。（可尝试安装 akshare；港股个股新闻可能不支持。）")
    sys.exit(1)

  print(f"**{args.symbol}** 新闻 (来源: {provider})\n")
  for i, item in enumerate(items, 1):
    print(format_item(item, i))
    print()


if __name__ == "__main__":
  main()
  sys.exit(0)
