"""
Tencent Finance data source.

Scope:
 - Daily K-line (OHLCV + turnover_rate + amount) for individual stocks
 - Daily K-line for indices (CSI 300 = sh000300, SSE = sh000001, SZSE = sz399001)
 - Realtime quote (current price, change %, total mv hint)
 - Code normalization helper (002418 → sz002418, 600519 → sh600519, etc)

No API key needed. Robust to 6-digit variations.
"""
from __future__ import annotations
import json
import re
import time
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
import urllib.request
import urllib.parse


KLINE_URL = "https://web.ifzq.gtimg.cn/appstock/app/newfqkline/get"
REALTIME_URL = "http://qt.gtimg.cn/q="

_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120"


def _http_get(url: str, timeout: int = 10, retries: int = 3) -> bytes:
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": _UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:
            last_err = e
            # exponential-ish backoff: 0.5s, 1.5s, 3.5s
            time.sleep(0.5 + attempt * 1.0 + attempt * attempt * 0.5)
    raise last_err if last_err else RuntimeError("http_get failed")


def to_tencent_code(code: str) -> str:
    """
    Convert any input into Tencent format: 'sz002418', 'sh600519', 'bj430047', etc.
    Accepts: 002418, 002418.SZ, sz002418, SH600519.
    Raises ValueError if can't determine market.
    """
    s = code.strip().lower()
    m = re.match(r"^(sz|sh|bj)(\d{6})$", s)
    if m:
        return m.group(1) + m.group(2)
    m = re.match(r"^(\d{6})\.(sz|sh|bj)$", s)
    if m:
        return m.group(2) + m.group(1)
    m = re.match(r"^\d{6}$", s)
    if m:
        prefix = s[:2]
        if prefix in ("60", "68", "51", "58") or s[0] == "9":
            return "sh" + s
        elif prefix in ("00", "30", "20") or prefix.startswith("3"):
            return "sz" + s
        elif s.startswith(("43", "83", "87", "92", "4", "8")):
            return "bj" + s
        else:
            # default to SZ
            return "sz" + s
    raise ValueError(f"Cannot parse Tencent code from: {code}")


def to_tushare_code(tcode: str) -> str:
    """Inverse: sz002418 -> 002418.SZ"""
    tcode = tcode.strip().lower()
    m = re.match(r"^(sz|sh|bj)(\d{6})$", tcode)
    if m:
        return m.group(2) + "." + m.group(1).upper()
    return tcode


# ---------- K-line ----------

def get_daily_kline(code: str, days: int = 320, adjust: str = "qfq") -> pd.DataFrame:
    """
    Fetch daily K-line from Tencent. Returns a DataFrame with:
        trade_date (YYYYMMDD str), open, high, low, close, vol (手), amount (元), turnover_rate (%)

    Args:
        code: any format accepted by to_tencent_code, or index code like 'sh000300'.
        days: how many trading days to return from Tencent's side (Tencent's limit).
        adjust: 'qfq' (前复权), 'hfq' (后复权), '' (不复权).
    """
    tcode = to_tencent_code(code) if not code.startswith(("sh00", "sz39", "sh39", "bj")) else code
    # Special-case indices: they use sh000300, sz399001, etc. which are already full
    if code.startswith(("sh", "sz", "bj")) and len(code) == 8:
        tcode = code.lower()

    # Build URL
    params = {
        "_var": "kline_day",
        "param": f"{tcode},day,,,{days},{adjust}",
        "r": str(time.time()),
    }
    url = KLINE_URL + "?" + urllib.parse.urlencode(params)
    raw = _http_get(url).decode("utf-8", errors="ignore")

    # Response is JSONP: kline_day={...};
    m = re.search(r"=\s*(\{.*\})\s*;?$", raw, re.DOTALL)
    if not m:
        raise RuntimeError(f"Unexpected Tencent response: {raw[:200]}")
    payload = json.loads(m.group(1))

    data = payload.get("data", {})
    stock_data = data.get(tcode, {})
    # Individual stocks: key is 'qfqday' / 'hfqday' / 'day'
    # Indices: key is 'day'
    candle_key = {"qfq": "qfqday", "hfq": "hfqday", "": "day"}.get(adjust, "qfqday")
    rows = stock_data.get(candle_key) or stock_data.get("day") or []
    if not rows:
        # Some indices return under 'day' even when qfq requested
        rows = stock_data.get("day", [])
    if not rows:
        raise RuntimeError(f"Tencent returned no candles for {tcode}")

    # Row format (newfqkline):
    # [date, open, close, high, low, vol, {}, turnover_rate, amount_wan, ""]
    # Index may have fewer fields: [date, open, close, high, low, vol]
    records = []
    for row in rows:
        if len(row) < 6:
            continue
        rec = {
            "trade_date": row[0].replace("-", ""),
            "open": float(row[1]),
            "close": float(row[2]),
            "high": float(row[3]),
            "low": float(row[4]),
            "vol": float(row[5]),  # 手
        }
        # Optional turnover & amount
        if len(row) >= 9:
            try:
                rec["turnover_rate"] = float(row[7])
            except (TypeError, ValueError):
                rec["turnover_rate"] = None
            try:
                # amount returned in 万元, convert to 元
                rec["amount"] = float(row[8]) * 1e4
            except (TypeError, ValueError):
                rec["amount"] = None
        else:
            rec["turnover_rate"] = None
            # Estimate amount from vol * close * 100 (vol is 手)
            rec["amount"] = rec["vol"] * rec["close"] * 100
        records.append(rec)

    df = pd.DataFrame(records)
    df = df.sort_values("trade_date").reset_index(drop=True)
    return df


# ---------- Realtime quote ----------

def get_realtime_quote(code: str) -> dict:
    """
    Fetch realtime quote from qt.gtimg.cn. Returns a dict with:
        name, code, price, pre_close, today_open, high, low, change, change_pct,
        vol_手, amount_万元, turnover_rate, pe_ttm, pb, total_mv_亿, float_mv_亿
    """
    tcode = to_tencent_code(code) if not code.startswith(("sh", "sz", "bj")) else code
    url = REALTIME_URL + tcode
    raw = _http_get(url)
    # Response is GBK encoded: v_sz002418="51~康盛股份~002418~6.81~...";
    try:
        txt = raw.decode("gbk")
    except UnicodeDecodeError:
        txt = raw.decode("utf-8", errors="ignore")

    m = re.search(r'"([^"]+)"', txt)
    if not m:
        raise RuntimeError(f"Unexpected Tencent realtime response: {txt[:200]}")
    parts = m.group(1).split("~")
    if len(parts) < 50:
        raise RuntimeError(f"Tencent realtime has too few fields: {len(parts)}")

    def _f(idx, default=None):
        try:
            v = parts[idx]
            return float(v) if v not in ("", "-", "~") else default
        except (ValueError, IndexError):
            return default

    quote = {
        "name": parts[1],
        "code": parts[2],
        "price": _f(3),
        "pre_close": _f(4),
        "today_open": _f(5),
        "volume_手": _f(6),
        "bid_vol": _f(7),
        "ask_vol": _f(8),
        "high": _f(33),
        "low": _f(34),
        "change": _f(31),
        "change_pct": _f(32),
        "amount_万元": _f(37),       # 总成交额（万元）
        "turnover_rate": _f(38),    # 换手率 %
        "pe_ttm": _f(39),
        "wavg_price": None,
        "pb": _f(46),
        "total_mv_亿": _f(45),       # 总市值（亿元）
        "float_mv_亿": _f(44),       # 流通市值（亿元）
        "timestamp": parts[30] if len(parts) > 30 else "",
    }
    return quote


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("usage: tencent.py <code>")
        sys.exit(1)
    code = sys.argv[1]
    print("--- realtime ---")
    print(json.dumps(get_realtime_quote(code), ensure_ascii=False, indent=2))
    print("--- kline last 5 ---")
    df = get_daily_kline(code, days=252)
    print(df.tail(5).to_string())
