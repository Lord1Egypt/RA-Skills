#!/usr/bin/env python3
"""
CN/HK stock quote helper for yahoo-finance skill.

For A-shares and HK stocks, try in order:
1) Tencent行情 (qt.gtimg.cn)
2) 东方财富 Push2 (A-shares only)
3) AkShare (A-shares, if installed)

Stop at the first provider that returns usable data.

Usage:
  python3 cn_quote.py 600519.SS
  python3 cn_quote.py 000001.SZ
  python3 cn_quote.py 600519
  python3 cn_quote.py 0700.HK
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from typing import Optional, Tuple
from urllib import error, request

RETRIES = 2  # 最多重试 2 次，共 3 次请求


def _http_get(url: str, encoding: str = "utf-8") -> Optional[str]:
  req = request.Request(url, headers={"User-Agent": "OpenClaw/1.0"})
  for attempt in range(1 + RETRIES):
    try:
      with request.urlopen(req, timeout=10) as r:
        return r.read().decode(encoding, errors="ignore")
    except (error.HTTPError, error.URLError, OSError):
      if attempt < RETRIES:
        time.sleep(0.5 * (attempt + 1))
        continue
      return None
  return None


@dataclass
class Quote:
  symbol: str
  name: str
  currency: str
  price: float
  previous_close: Optional[float]
  change: Optional[float]
  change_percent: Optional[float]


def _parse_symbol(raw: str) -> Tuple[str, str, str]:
  """
  Return (market, code, display_symbol)
  market: 'sh' | 'sz' | 'hk' | 'unknown'
  """
  s = raw.strip().upper()
  display = raw.strip()

  if s.endswith(".SS") or s.startswith("SH"):
    # Normalize variants: 600519.SS, SH600519
    if s.endswith(".SS"):
      code = s[:-3]
    else:
      code = s[2:]
    return "sh", code, display
  if s.endswith(".SZ") or s.startswith("SZ"):
    # Normalize variants: 000001.SZ, SZ000001
    if s.endswith(".SZ"):
      code = s[:-3]
    else:
      code = s[2:]
    return "sz", code, display
  if s.endswith(".HK") or s.startswith("HK"):
    # Normalize variants: 0700.HK, HK00700
    if s.endswith(".HK"):
      code = s[:-3]
    else:
      code = s[2:]
    return "hk", code.zfill(5), display

  # pure digits: guess A-share
  if s.isdigit() and len(s) in (6, 5):
    code = s.zfill(6)
    market = "sh" if code.startswith("6") else "sz"
    return market, code, display

  return "unknown", s, display


def fetch_from_tencent(symbol: str) -> Optional[Quote]:
  market, code, display = _parse_symbol(symbol)
  if market not in ("sh", "sz", "hk"):
    return None

  if market == "hk":
    t_code = f"hk{code.zfill(5)}"
  else:
    t_code = f"{market}{code}"

  url = f"http://qt.gtimg.cn/q={t_code}"
  text = _http_get(url, encoding="gbk")
  if not text:
    return None

  for line in text.split(";"):
    if "=" not in line:
      continue
    key, value = line.split("=", 1)
    if not value or value == '"1";':
      continue
    parts = value.strip('"').split("~")
    if len(parts) <= 32:
      continue

    name = parts[1]
    try:
      price = float(parts[3])
      change = float(parts[31]) if parts[31] else 0.0
      pct = float(parts[32]) if parts[32] else 0.0
    except ValueError:
      continue

    prev = price - change if change is not None else None
    currency = "HKD" if market == "hk" else "CNY"
    return Quote(
      symbol=display,
      name=name,
      currency=currency,
      price=price,
      previous_close=prev,
      change=change,
      change_percent=pct,
    )
  return None


def fetch_from_eastmoney(symbol: str) -> Optional[Quote]:
  market, code, display = _parse_symbol(symbol)
  # EastMoney: only A-shares
  if market not in ("sh", "sz"):
    return None

  secid_prefix = "1" if market == "sh" else "0"
  url = (
    "https://push2.eastmoney.com/api/qt/stock/get"
    f"?secid={secid_prefix}.{code}"
    "&fields=f43,f58,f57,f60&fltt=2&invt=2"
  )
  text = _http_get(url, encoding="utf-8")
  if not text:
    return None
  try:
    data = json.loads(text)
  except json.JSONDecodeError:
    return None
  data = data.get("data") or {}
  if not data:
    return None

  try:
    price = float(data.get("f43"))
  except (TypeError, ValueError):
    return None

  name = data.get("f58") or display
  prev = data.get("f60")
  try:
    prev_f = float(prev) if prev is not None else None
  except (TypeError, ValueError):
    prev_f = None

  change = pct = None
  if prev_f is not None:
    change = price - prev_f
    if prev_f:
      pct = (change / prev_f) * 100.0

  return Quote(
    symbol=display,
    name=name,
    currency="CNY",
    price=price,
    previous_close=prev_f,
    change=change,
    change_percent=pct,
  )


def fetch_from_akshare(symbol: str) -> Optional[Quote]:
  # Optional dependency; A-shares only. Try single-stock history first (one request).
  try:
    import akshare as ak  # type: ignore
  except Exception:
    return None

  market, code, display = _parse_symbol(symbol)
  if market not in ("sh", "sz"):
    return None

  try:
    from datetime import datetime, timedelta
    end_d = datetime.now().date()
    start_d = end_d - timedelta(days=10)
    # Prefer single-stock API (stock_zh_a_hist_em or stock_zh_a_hist depending on akshare version)
    fn = getattr(ak, "stock_zh_a_hist_em", None) or getattr(ak, "stock_zh_a_hist", None)
    df = fn(symbol=code, period="daily", start_date=start_d.strftime("%Y%m%d"), end_date=end_d.strftime("%Y%m%d"), adjust="") if fn else None
  except Exception:
    df = None
  if df is not None and not df.empty:
    try:
      row = df.iloc[-1]
      price = float(row["收盘"])
      prev = float(df.iloc[-2]["收盘"]) if len(df) >= 2 else price
      change = price - prev
      pct = (change / prev * 100.0) if prev else None
      name = str(row.get("名称", display))
      return Quote(
        symbol=display,
        name=name,
        currency="CNY",
        price=price,
        previous_close=prev,
        change=change,
        change_percent=pct,
      )
    except (KeyError, IndexError, TypeError, ValueError):
      pass

  # Fallback: full A-share spot then filter (heavier).
  try:
    df = ak.stock_zh_a_spot_em()
  except Exception:
    return None
  try:
    row = df.loc[df["代码"] == code].iloc[0]
  except Exception:
    return None
  try:
    price = float(row["最新价"])
  except Exception:
    return None
  name = str(row.get("名称", display))
  prev = row.get("昨收")
  try:
    prev_f = float(prev) if prev is not None else None
  except Exception:
    prev_f = None
  change = pct = None
  if prev_f is not None:
    change = price - prev_f
    if prev_f:
      pct = (change / prev_f) * 100.0
  return Quote(
    symbol=display,
    name=name,
    currency="CNY",
    price=price,
    previous_close=prev_f,
    change=change,
    change_percent=pct,
  )


def format_quote(q: Quote) -> str:
  lines = [
    f"**{q.name}** ({q.symbol})",
    f"  {q.currency} {q.price:.2f}",
  ]
  if q.change is not None and q.change_percent is not None:
    sign = "+" if q.change >= 0 else ""
    lines.append(
      f"  涨跌: {sign}{q.change:.2f} ({sign}{q.change_percent:.2f}%)"
    )
  if q.previous_close is not None:
    lines.append(f"  昨收: {q.previous_close:.2f}")
  return "\n".join(lines)


def quote_to_dict(q: Quote) -> dict:
  """Convert to dict for JSON output (same shape as quote.py)."""
  return {
    "symbol": q.symbol,
    "shortName": q.name,
    "currency": q.currency,
    "price": q.price,
    "previousClose": q.previous_close,
    "change": q.change,
    "changePercent": q.change_percent,
    "volume": None,
    "fiftyTwoWeekHigh": None,
    "fiftyTwoWeekLow": None,
  }


def quote_one(symbol: str) -> Optional[Quote]:
  """Try Tencent -> EastMoney -> AkShare; return first success or None."""
  for fn in [fetch_from_tencent, fetch_from_eastmoney, fetch_from_akshare]:
    q = fn(symbol)
    if q:
      return q
  return None


def main() -> None:
  ap = argparse.ArgumentParser(
    description=(
      "CN/HK quotes via Tencent -> EastMoney -> AkShare (best-effort, no keys)."
    )
  )
  ap.add_argument("symbol", help="A/HK symbol, e.g. 600519.SS, 000001.SZ, 0700.HK")
  args = ap.parse_args()

  symbol = args.symbol.strip()

  for provider, fn in [
    ("Tencent", fetch_from_tencent),
    ("EastMoney", fetch_from_eastmoney),
    ("AkShare", fetch_from_akshare),
  ]:
    q = fn(symbol)
    if q:
      print(format_quote(q))
      return

  print(f"{symbol}: 没有从 腾讯/东方财富/AkShare 拿到有效行情。（A 股可尝试安装 akshare。）")
  sys.exit(1)


if __name__ == "__main__":
  main()
  sys.exit(0)

