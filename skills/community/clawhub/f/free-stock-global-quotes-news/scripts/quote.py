#!/usr/bin/env python3
"""
Fetch quote from Yahoo Finance (no API key). On server 403: tries quoteSummary,
then FINNHUB_API_KEY fallback (free at finnhub.io). Supports HTTPS_PROXY.
Usage:
  python quote.py AAPL
  FINNHUB_API_KEY=xxx python quote.py AAPL   # fallback when Yahoo 403
  HTTPS_PROXY=http://proxy:port python quote.py AAPL
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.client import RemoteDisconnected
import urllib.error
import urllib.request

# Env: OPENCLAW_QUOTE_TIMEOUT (default 12), OPENCLAW_QUOTE_RETRY_DELAY (default 0.4),
#      OPENCLAW_QUOTE_CACHE_TTL (0=off), OPENCLAW_QUOTE_PARALLEL (1=on), OPENCLAW_QUOTE_MAX_WORKERS (6)
def _timeout() -> int:
    return int(os.environ.get("OPENCLAW_QUOTE_TIMEOUT", "12"))
def _retry_delay() -> float:
    return float(os.environ.get("OPENCLAW_QUOTE_RETRY_DELAY", "0.4"))
def _cache_ttl() -> int:
    return int(os.environ.get("OPENCLAW_QUOTE_CACHE_TTL", "0"))
def _parallel() -> bool:
    return os.environ.get("OPENCLAW_QUOTE_PARALLEL", "1").strip() in ("1", "true", "yes")
def _max_workers() -> int:
    return min(12, max(1, int(os.environ.get("OPENCLAW_QUOTE_MAX_WORKERS", "6"))))
def _retries() -> int:
    return max(0, int(os.environ.get("OPENCLAW_QUOTE_RETRIES", "2")))
_cache: dict[tuple[str, str], tuple[dict, float]] = {}

# Browser-like headers to avoid Yahoo 403 (blocked for bot-like User-Agent or missing headers)
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://finance.yahoo.com/",
}

CHART_BASES = [
    "https://query1.finance.yahoo.com/v8/finance/chart",
    "https://query2.finance.yahoo.com/v8/finance/chart",
]
QUOTE_SUMMARY_BASE = "https://query2.finance.yahoo.com/v10/finance/quoteSummary"


def _build_opener():
    """Use HTTPS_PROXY/HTTP_PROXY if set (e.g. to bypass datacenter IP blocks)."""
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
    if proxy:
        return urllib.request.build_opener(urllib.request.ProxyHandler({"https": proxy, "http": proxy}))
    return urllib.request.build_opener()


def _fetch_url(url: str) -> tuple[dict | None, str | None]:
    req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
    last_err: str | None = None
    for attempt in range(1 + _retries()):
        try:
            opener = _build_opener()
            with opener.open(req, timeout=_timeout()) as r:
                return json.loads(r.read().decode()), None
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.reason}"
            if e.code >= 500 and attempt < _retries():
                time.sleep(0.5 * (attempt + 1))
                continue
            return None, last_err
        except (urllib.error.URLError, json.JSONDecodeError, RemoteDisconnected, TimeoutError, OSError) as e:
            last_err = str(e)
            if attempt < _retries():
                time.sleep(0.5 * (attempt + 1))
                continue
            return None, last_err
    return None, last_err or "Unknown error"


def fetch_chart(symbol: str, range_: str = "1d", interval: str = "1d") -> dict | None:
    for base in CHART_BASES:
        url = f"{base}/{symbol}?range={range_}&interval={interval}"
        data, err = _fetch_url(url)
        if data is not None:
            return data
        if err and "403" in err:
            time.sleep(0.5)
            continue
        return {"error": err} if err else None
    return {"error": "Chart API returned 403 from all hosts (try HTTPS_PROXY)"}


def fetch_quote_summary(symbol: str) -> dict | None:
    """Fallback: quoteSummary has price/summaryDetail; sometimes allowed when chart is 403."""
    url = f"{QUOTE_SUMMARY_BASE}/{symbol}?modules=price,summaryDetail&formatted=true"
    data, err = _fetch_url(url)
    if data is None:
        return {"error": err or "quoteSummary failed"}
    return data


def fetch_finnhub(symbol: str) -> dict | None:
    """Fallback when Yahoo 403 (e.g. datacenter IP). Free key at https://finnhub.io."""
    key = os.environ.get("FINNHUB_API_KEY")
    if not key:
        return None
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={key}"
    data, err = _fetch_url(url)
    if data is None or data.get("c") is None:
        return {"error": err or "Finnhub no data"}
    return data


def _parse_finnhub(data: dict, symbol: str) -> dict | None:
    try:
        c = data.get("c")
        pc = data.get("pc") or c
        d = data.get("d")
        dp = data.get("dp")
        if c is None:
            return None
        if d is None and pc is not None:
            d = c - pc
        if dp is None and pc and pc != 0:
            dp = ((c - pc) / pc) * 100
        return {
            "symbol": symbol,
            "shortName": symbol,
            "currency": "USD",
            "price": c,
            "previousClose": pc,
            "change": d,
            "changePercent": dp,
            "volume": None,
            "fiftyTwoWeekHigh": data.get("h"),
            "fiftyTwoWeekLow": data.get("l"),
        }
    except (KeyError, TypeError):
        return None


def _parse_chart(data: dict, symbol: str) -> dict | None:
    try:
        result = data["chart"]["result"][0]
        meta = result["meta"]
        cur = meta.get("regularMarketPrice") or meta.get("previousClose")
        prev = meta.get("previousClose") or cur
        if prev and cur:
            chg = cur - prev
            pct = (chg / prev) * 100
        else:
            chg = pct = None
        return {
            "symbol": meta.get("symbol", symbol),
            "shortName": meta.get("shortName", symbol),
            "currency": meta.get("currency", ""),
            "price": cur,
            "previousClose": prev,
            "change": chg,
            "changePercent": pct,
            "volume": meta.get("regularMarketVolume"),
            "fiftyTwoWeekHigh": meta.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow": meta.get("fiftyTwoWeekLow"),
        }
    except (KeyError, IndexError, TypeError):
        return None


def _num(v) -> float | None:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, dict) and "raw" in v:
        return v["raw"]
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _parse_quote_summary(data: dict, symbol: str) -> dict | None:
    try:
        res = data["quoteSummary"]["result"][0]
        price = res.get("price", {}) or {}
        summary = res.get("summaryDetail", {}) or {}
        cur = _num(price.get("regularMarketPrice"))
        prev = _num(summary.get("previousClose"))
        if prev is None:
            prev = cur
        if cur is not None and prev is not None:
            chg = cur - prev
            pct = (chg / prev) * 100
        else:
            chg = pct = None
        return {
            "symbol": price.get("symbol") or symbol,
            "shortName": price.get("shortName") or symbol,
            "currency": price.get("currency") or "",
            "price": cur,
            "previousClose": prev,
            "change": chg,
            "changePercent": pct,
            "volume": _num(summary.get("regularMarketVolume")),
            "fiftyTwoWeekHigh": _num(summary.get("fiftyTwoWeekHigh")),
            "fiftyTwoWeekLow": _num(summary.get("fiftyTwoWeekLow")),
        }
    except (KeyError, IndexError, TypeError):
        return None


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


def quote_one(symbol: str, range_: str = "1d") -> dict | None:
    ttl = _cache_ttl()
    if ttl > 0:
        key = (symbol.strip(), range_)
        if key in _cache:
            res, exp = _cache[key]
            if time.time() < exp:
                return res
    interval = "1m" if range_ == "1d" else "1d"
    data = fetch_chart(symbol, range_=range_, interval=interval)
    if data and "error" not in data:
        parsed = _parse_chart(data, symbol)
        if parsed:
            if ttl > 0:
                key = (symbol.strip(), range_)
                _cache[key] = (parsed, time.time() + ttl)
            return parsed
    err_msg = data.get("error", "") if isinstance(data, dict) else ""
    if "403" in err_msg or not data:
        time.sleep(0.5)
        qs = fetch_quote_summary(symbol)
        if qs and "error" not in qs:
            parsed = _parse_quote_summary(qs, symbol)
            if parsed:
                if ttl > 0:
                    key = (symbol.strip(), range_)
                    _cache[key] = (parsed, time.time() + ttl)
                return parsed
        fh = fetch_finnhub(symbol)
        if fh and "error" not in fh:
            parsed = _parse_finnhub(fh, symbol)
            if parsed:
                if ttl > 0:
                    _cache[key] = (parsed, time.time() + ttl)
                return parsed
        # Clear error message by case
        if not os.environ.get("FINNHUB_API_KEY"):
            err_msg = "Yahoo 403; set FINNHUB_API_KEY for US fallback or HTTPS_PROXY for Yahoo"
        elif isinstance(fh, dict) and "Finnhub no data" in (fh.get("error") or ""):
            err_msg = "Yahoo 403; Finnhub had no data for this symbol (US symbols work best)"
        else:
            err_msg = err_msg or "Yahoo 403 (set FINNHUB_API_KEY or HTTPS_PROXY)"
    res = {"symbol": symbol, "error": err_msg or "No data"}
    if ttl > 0:
        key = (symbol.strip(), range_)
        _cache[key] = (res, time.time() + min(ttl, 30))  # cache errors briefly
    return res


def format_quote(info: dict) -> str:
    if info.get("error"):
        return f"{info['symbol']}: {info['error']}"
    price = info.get("price")
    lines = [
        f"**{info.get('shortName', info['symbol'])}** ({info['symbol']})",
        f"  {info.get('currency', '')} {price:.2f}" if price is not None else "",
    ]
    if info.get("change") is not None and info.get("changePercent") is not None:
        sign = "+" if info["change"] >= 0 else ""
        lines.append(f"  涨跌: {sign}{info['change']:.2f} ({sign}{info['changePercent']:.2f}%)")
    if info.get("volume") is not None:
        lines.append(f"  成交量: {info['volume']:,}")
    if info.get("fiftyTwoWeekHigh") is not None and info.get("fiftyTwoWeekLow") is not None:
        lines.append(f"  52周: {info['fiftyTwoWeekLow']:.2f} - {info['fiftyTwoWeekHigh']:.2f}")
    return "\n".join(l for l in lines if l).strip()


def _fetch_one(sym: str, range_: str, do_json: bool = False):
    """Fetch one symbol; return (sym, dict) for unified output."""
    sym = sym.strip()
    if _is_cn_hk_symbol(sym) and range_ == "1d":
        _dir = os.path.dirname(os.path.abspath(__file__))
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("cn_quote", os.path.join(_dir, "cn_quote.py"))
            mod = importlib.util.module_from_spec(spec)
            if spec and spec.loader:
                spec.loader.exec_module(mod)
            else:
                import cn_quote as mod  # type: ignore
        except Exception:
            mod = None
        if mod:
            q_cn = mod.quote_one(sym)
            if q_cn:
                return (sym, mod.quote_to_dict(q_cn))
    q = quote_one(sym, range_=range_)
    return (sym, q)


def main() -> None:
    ap = argparse.ArgumentParser(description="Yahoo Finance quote (no API key). One script for US + A-share/HK.")
    ap.add_argument("symbols", nargs="+", help="Symbols e.g. AAPL 0700.HK 000001.SZ")
    ap.add_argument("--range", default="1d", help="Range: 1d,5d,1mo,3mo,6mo,1y,2y,5y (default: 1d, A/HK use 1d)")
    ap.add_argument("--json", action="store_true", help="Output raw JSON")
    args = ap.parse_args()

    symbols = [s.strip() for s in args.symbols]
    do_parallel = _parallel() and len(symbols) > 1
    out_list: list[tuple[str, dict]] = []

    if do_parallel:
        order = {s: i for i, s in enumerate(symbols)}
        with ThreadPoolExecutor(max_workers=min(_max_workers(), len(symbols))) as ex:
            futures = {ex.submit(_fetch_one, sym, args.range, args.json): sym for sym in symbols}
            for fut in as_completed(futures):
                try:
                    sym, data = fut.result()
                    out_list.append((sym, data))
                except Exception as e:
                    sym = futures.get(fut, "?")
                    out_list.append((sym, {"symbol": sym, "error": str(e)}))
        out_list.sort(key=lambda x: order.get(x[0], 999))
    else:
        delay = _retry_delay()
        for i, sym in enumerate(symbols):
            if i > 0:
                time.sleep(delay)
            _, data = _fetch_one(sym, args.range, args.json)
            out_list.append((sym, data))

    if args.json:
        out = [d for _, d in out_list]
        print(json.dumps(out if len(out) != 1 else out[0], indent=2, default=str))
    else:
        for _, data in out_list:
            print(format_quote(data))
            print()


if __name__ == "__main__":
    main()
    sys.exit(0)
