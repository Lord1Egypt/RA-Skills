#!/usr/bin/env python3
"""
CryptoLens — AI-driven multi-coin crypto analysis tool.
Multi-coin comparison + Technical indicator candlestick charts.
Billing is pre-configured via SkillPay.me — no setup needed.

Usage:
  python3 crypto_lens.py compare BTC ETH SOL [--duration 7d] [--user-id UID]
  python3 crypto_lens.py chart BTC [--duration 24h] [--user-id UID]
  python3 crypto_lens.py analyze BTC [--duration 24h] [--user-id UID]
"""
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CACHE_TTL_SEC = 300
COINGECKO_PRICE_URL = "https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies={currency}"
COINGECKO_SEARCH_URL = "https://api.coingecko.com/api/v3/search?query={query}"
COINGECKO_MARKET_CHART_URL = "https://api.coingecko.com/api/v3/coins/{id}/market_chart?vs_currency={currency}&days={days}"
HYPERLIQUID_INFO_URL = "https://api.hyperliquid.xyz/info"

BILLING_URL = "https://skillpay.me/api/v1/billing"
BILLING_API_KEY = "sk_fbda2cd31455722ee28f08aebbf77af5f0002f21d1832f1b2102b756e20f2981"
SKILL_ID = "73d7f580-817c-4df2-a0fb-0572f93e4b97"

TOKEN_ID_MAP = {
    "HYPE": "hyperliquid",
    "HYPERLIQUID": "hyperliquid",
    "BTC": "bitcoin",
    "BITCOIN": "bitcoin",
    "ETH": "ethereum",
    "ETHEREUM": "ethereum",
    "SOL": "solana",
    "SOLANA": "solana",
    "BNB": "binancecoin",
    "DOGE": "dogecoin",
    "XRP": "ripple",
    "ADA": "cardano",
    "AVAX": "avalanche-2",
    "DOT": "polkadot",
    "MATIC": "matic-network",
    "LINK": "chainlink",
    "UNI": "uniswap",
    "ATOM": "cosmos",
    "LTC": "litecoin",
    "NEAR": "near",
    "ARB": "arbitrum",
    "OP": "optimism",
    "APT": "aptos",
    "SUI": "sui",
    "SEI": "sei-network",
    "TIA": "celestia",
    "INJ": "injective-protocol",
    "FET": "fetch-ai",
    "RENDER": "render-token",
    "PEPE": "pepe",
    "WIF": "dogwifcoin",
    "BONK": "bonk",
    "SHIB": "shiba-inu",
}

# ---------------------------------------------------------------------------
# Helpers: HTTP
# ---------------------------------------------------------------------------
UA = "cryptolens/1.0"


def _fetch_json(url, headers=None):
    hdrs = {"User-Agent": UA}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError) as exc:
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            raise RuntimeError(str(exc)) from exc
    raise RuntimeError("max retries")


def _post_json(url, payload, headers=None):
    hdrs = {"Content-Type": "application/json", "User-Agent": UA}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=hdrs)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError) as exc:
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            raise RuntimeError(str(exc)) from exc
    raise RuntimeError("max retries")


# ---------------------------------------------------------------------------
# Helpers: Cache
# ---------------------------------------------------------------------------
def _cache_path(prefix, key):
    safe = key.replace("/", "-").replace(" ", "_")
    return f"/tmp/cryptolens_{prefix}_{safe}.json"


def _read_cache(path, max_age=CACHE_TTL_SEC):
    try:
        if time.time() - os.stat(path).st_mtime > max_age:
            return None
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return None


def _write_cache(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f)
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Billing (SkillPay)
# ---------------------------------------------------------------------------
def charge_user(user_id):
    """Charge user via SkillPay. Returns (ok, balance, payment_url).
    Price per call is set on SkillPay Dashboard, not in API request."""
    if not BILLING_API_KEY:
        return False, None, None  # no API key — block usage
    if not user_id:
        return False, None, None  # no user_id — cannot charge
    try:
        data = _post_json(
            f"{BILLING_URL}/charge",
            {"user_id": user_id, "skill_id": SKILL_ID},
            headers={"X-API-Key": BILLING_API_KEY},
        )
        if data.get("success"):
            return True, data.get("balance"), None
        return False, data.get("balance"), data.get("payment_url")
    except RuntimeError:
        # billing service down — fail close (block usage in production)
        return False, None, None  # billing service down — block usage


# ---------------------------------------------------------------------------
# Data Sources
# ---------------------------------------------------------------------------
def _resolve_token_id(symbol):
    """Resolve symbol to CoinGecko token ID."""
    upper = symbol.upper()
    if upper in TOKEN_ID_MAP:
        return TOKEN_ID_MAP[upper]
    # search CoinGecko
    cache = _cache_path("search", upper)
    data = _read_cache(cache)
    if data is None:
        try:
            data = _fetch_json(COINGECKO_SEARCH_URL.format(query=urllib.parse.quote(symbol)))
            _write_cache(cache, data)
        except RuntimeError:
            return symbol.lower()
    coins = data.get("coins", [])
    matches = [c for c in coins if c.get("symbol", "").upper() == upper]
    if not matches:
        return symbol.lower()
    matches.sort(key=lambda c: c.get("market_cap_rank") or 10**9)
    return matches[0].get("id", symbol.lower())


def _normalize_hl_symbol(symbol):
    sym = symbol.upper()
    for sep in ("-", "/", "_"):
        if sep in sym:
            sym = sym.split(sep)[0]
            break
    for suf in ("USDC", "USDH", "USDE", "USD", "USDT"):
        if sym.endswith(suf) and len(sym) > len(suf):
            sym = sym[: -len(suf)]
            break
    return sym


def _get_hyperliquid_meta():
    cache = _cache_path("hl_meta", "meta")
    data = _read_cache(cache)
    if data is not None:
        return data
    data = _post_json(HYPERLIQUID_INFO_URL, {"type": "metaAndAssetCtxs"})
    _write_cache(cache, data)
    return data


def _hl_lookup(symbol):
    """Return (meta_entry, ctx) for symbol on Hyperliquid, or (None, None)."""
    try:
        meta, ctxs = _get_hyperliquid_meta()
    except (RuntimeError, ValueError):
        return None, None
    universe = meta.get("universe", [])
    mapping = {}
    for idx, entry in enumerate(universe):
        name = str(entry.get("name", "")).upper()
        if name:
            mapping[name] = idx
    norm = _normalize_hl_symbol(symbol)
    idx = mapping.get(norm)
    if idx is None or idx >= len(ctxs):
        return None, None
    return universe[idx], ctxs[idx]


def _interval_str(minutes):
    if minutes < 60:
        return f"{int(minutes)}m"
    h = int(minutes / 60)
    if h < 24:
        return f"{h}h"
    return f"{int(h / 24)}d"


def _pick_hl_interval(total_minutes):
    if total_minutes <= 180:
        return 1
    if total_minutes <= 360:
        return 3
    if total_minutes <= 720:
        return 5
    if total_minutes <= 1440:
        return 15
    if total_minutes <= 4320:
        return 30
    if total_minutes <= 10080:
        return 60
    if total_minutes <= 20160:
        return 120
    if total_minutes <= 40320:
        return 240
    if total_minutes <= 80640:
        return 480
    return 1440


def get_candles(symbol, total_minutes):
    """Get OHLCV candles for symbol. Returns list of (ts_ms, o, h, l, c, v)."""
    hl_sym = _normalize_hl_symbol(symbol)
    _, ctx = _hl_lookup(hl_sym)
    source = "coingecko"

    candles = []
    if ctx:
        source = "hyperliquid"
        interval = _pick_hl_interval(total_minutes)
        now_ms = int(time.time() * 1000)
        start_ms = now_ms - int(total_minutes * 60 * 1000)
        try:
            data = _post_json(HYPERLIQUID_INFO_URL, {
                "type": "candleSnapshot",
                "req": {
                    "coin": hl_sym,
                    "interval": _interval_str(interval),
                    "startTime": start_ms,
                    "endTime": now_ms,
                },
            })
            for row in data:
                try:
                    candles.append((
                        int(row["t"]),
                        float(row["o"]),
                        float(row["h"]),
                        float(row["l"]),
                        float(row["c"]),
                        float(row.get("v", 0)),
                    ))
                except (KeyError, TypeError, ValueError):
                    continue
        except RuntimeError:
            pass

    if not candles:
        source = "coingecko"
        token_id = _resolve_token_id(symbol)
        days = max(1, int(math.ceil(total_minutes / 1440.0)))
        if days > 365:
            days = 365
        try:
            cache = _cache_path(f"mc_{days}", token_id)
            chart_data = _read_cache(cache)
            if chart_data is None:
                chart_data = _fetch_json(
                    COINGECKO_MARKET_CHART_URL.format(id=token_id, currency="usd", days=days)
                )
                _write_cache(cache, chart_data)
            prices = chart_data.get("prices", [])
            # build candles from price points
            if total_minutes <= 360:
                bucket_min = 5
            elif total_minutes <= 1440:
                bucket_min = 15
            elif total_minutes <= 4320:
                bucket_min = 30
            else:
                bucket_min = 60
            bucket_ms = bucket_min * 60 * 1000
            prices.sort(key=lambda r: r[0])
            cutoff = prices[-1][0] - total_minutes * 60 * 1000 if prices else 0
            bucket = None
            for ts, price in prices:
                if ts < cutoff:
                    continue
                bs = (int(ts) // bucket_ms) * bucket_ms
                if bucket is None or bucket["s"] != bs:
                    if bucket:
                        candles.append((bucket["s"], bucket["o"], bucket["h"], bucket["l"], bucket["c"], 0))
                    bucket = {"s": bs, "o": price, "h": price, "l": price, "c": price}
                else:
                    bucket["h"] = max(bucket["h"], price)
                    bucket["l"] = min(bucket["l"], price)
                    bucket["c"] = price
            if bucket:
                candles.append((bucket["s"], bucket["o"], bucket["h"], bucket["l"], bucket["c"], 0))
        except RuntimeError:
            pass

    candles.sort(key=lambda r: r[0])
    return candles, source


def get_current_price(symbol):
    """Get current price for symbol. Returns (price_usd, source)."""
    hl_sym = _normalize_hl_symbol(symbol)
    _, ctx = _hl_lookup(hl_sym)
    if ctx:
        try:
            price = float(ctx.get("markPx") or ctx.get("midPx"))
            return price, "hyperliquid"
        except (TypeError, ValueError):
            pass
    token_id = _resolve_token_id(symbol)
    try:
        data = _fetch_json(COINGECKO_PRICE_URL.format(ids=token_id, currency="usd"))
        price = data.get(token_id, {}).get("usd")
        if price is not None:
            return float(price), "coingecko"
    except RuntimeError:
        pass
    return None, None


def get_prices_batch(symbols):
    """Get current prices for multiple symbols. Returns dict {SYMBOL: price_usd}."""
    result = {}
    # try Hyperliquid first
    for sym in symbols:
        p, _ = get_current_price(sym)
        if p is not None:
            result[sym.upper()] = p
    return result


# ---------------------------------------------------------------------------
# Technical Indicators
# ---------------------------------------------------------------------------
def _ma(closes, period):
    """Simple Moving Average."""
    import numpy as np
    arr = np.array(closes, dtype=float)
    if len(arr) < period:
        return [None] * len(arr)
    out = [None] * (period - 1)
    cumsum = np.cumsum(arr)
    out += list((cumsum[period - 1:] - np.concatenate(([0], cumsum[:-period]))) / period)
    return out


def _ema(closes, period):
    """Exponential Moving Average."""
    import numpy as np
    arr = np.array(closes, dtype=float)
    ema = np.full(len(arr), np.nan)
    if len(arr) < period:
        return [None] * len(arr)
    ema[period - 1] = np.mean(arr[:period])
    k = 2.0 / (period + 1)
    for i in range(period, len(arr)):
        ema[i] = arr[i] * k + ema[i - 1] * (1 - k)
    return [None if math.isnan(v) else v for v in ema]


def calc_rsi(closes, period=14):
    """RSI indicator."""
    import numpy as np
    arr = np.array(closes, dtype=float)
    if len(arr) < period + 1:
        return [None] * len(arr)
    deltas = np.diff(arr)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    rsi = [None] * period
    if avg_loss == 0:
        rsi.append(100.0)
    else:
        rs = avg_gain / avg_loss
        rsi.append(100.0 - 100.0 / (1.0 + rs))

    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        if avg_loss == 0:
            rsi.append(100.0)
        else:
            rs = avg_gain / avg_loss
            rsi.append(100.0 - 100.0 / (1.0 + rs))
    return rsi


def calc_macd(closes, fast=12, slow=26, signal=9):
    """MACD line, signal line, histogram."""
    ema_fast = _ema(closes, fast)
    ema_slow = _ema(closes, slow)
    macd_line = []
    for f, s in zip(ema_fast, ema_slow):
        if f is not None and s is not None:
            macd_line.append(f - s)
        else:
            macd_line.append(None)
    # signal line = EMA of MACD line
    valid_macd = [v for v in macd_line if v is not None]
    if len(valid_macd) < signal:
        return macd_line, [None] * len(macd_line), [None] * len(macd_line)
    sig = _ema(valid_macd, signal)
    # align signal with macd_line
    signal_line = [None] * (len(macd_line) - len(valid_macd))
    signal_line.extend(sig)
    histogram = []
    for m, s in zip(macd_line, signal_line):
        if m is not None and s is not None:
            histogram.append(m - s)
        else:
            histogram.append(None)
    return macd_line, signal_line, histogram


def calc_bollinger(closes, period=20, std_mult=2.0):
    """Bollinger Bands: upper, middle (SMA), lower."""
    import numpy as np
    arr = np.array(closes, dtype=float)
    upper, middle, lower = [], [], []
    for i in range(len(arr)):
        if i < period - 1:
            upper.append(None)
            middle.append(None)
            lower.append(None)
        else:
            window = arr[i - period + 1: i + 1]
            m = np.mean(window)
            s = np.std(window)
            middle.append(m)
            upper.append(m + std_mult * s)
            lower.append(m - std_mult * s)
    return upper, middle, lower


# ---------------------------------------------------------------------------
# Parse args
# ---------------------------------------------------------------------------
def _parse_duration(args):
    for arg in args:
        cleaned = arg.strip().lower().lstrip("-")
        if cleaned.startswith("duration="):
            cleaned = cleaned.split("=", 1)[1]
        m = re.match(r"^(\d+(?:\.\d+)?)([mhd])?$", cleaned)
        if not m:
            continue
        val = float(m.group(1))
        unit = m.group(2) or "h"
        if unit == "m":
            return max(1.0, val), f"{int(val)}m"
        if unit == "d":
            return max(1.0, val * 1440), f"{int(val)}d"
        return max(1.0, val * 60), f"{int(val)}h"
    return 1440.0, "24h"  # default 24h


def _validate_symbol(symbol):
    """Validate symbol format: alphanumeric, 1-20 chars."""
    return bool(re.match(r'^[A-Za-z0-9]{1,20}$', symbol))


def _auto_user_id():
    """Generate a deterministic user_id from machine identity.
    Each OpenClaw instance gets a unique billing identity."""
    import hashlib
    import socket
    raw = f"{socket.gethostname()}:{os.environ.get('USER', 'default')}:{os.path.expanduser('~')}"
    return f"oc_{hashlib.sha256(raw.encode()).hexdigest()[:16]}"


def _parse_user_id(args):
    for i, arg in enumerate(args):
        if arg == "--user-id" and i + 1 < len(args):
            return args[i + 1]
        if arg.startswith("--user-id="):
            return arg.split("=", 1)[1]
    return None  # no user_id provided


def _format_price(v):
    if v is None:
        return "n/a"
    if v >= 1000:
        return f"{v:,.2f}"
    if v >= 1:
        return f"{v:.2f}"
    if v >= 0.01:
        return f"{v:.4f}"
    return f"{v:.6f}"


# ---------------------------------------------------------------------------
# Command: compare
# ---------------------------------------------------------------------------
def cmd_compare(symbols, args):
    """Multi-coin comparison: price table, ranking, correlation, overlay chart."""
    import numpy as np

    for sym in symbols:
        if not _validate_symbol(sym):
            return _err(f"invalid symbol format: {sym} — alphanumeric only, max 20 chars")

    total_minutes, label = _parse_duration(args)
    user_id = _parse_user_id(args)

    if len(symbols) < 2:
        return _err("compare requires at least 2 symbols")
    if len(symbols) > 5:
        return _err("compare supports max 5 symbols")

    # Billing: compare = 5 tokens
    ok, balance, pay_url = charge_user(user_id)
    if not ok:
        return _billing_fail(balance, pay_url)

    # Fetch data for all symbols
    all_candles = {}
    prices = {}
    sources = {}
    for sym in symbols:
        sym_up = sym.upper()
        candles, source = get_candles(sym_up, total_minutes)
        if not candles:
            return _err(f"no data for {sym_up}")
        all_candles[sym_up] = candles
        sources[sym_up] = source
        prices[sym_up] = candles[-1][4]  # last close

    # Build comparison table
    table = []
    for sym_up in [s.upper() for s in symbols]:
        c = all_candles[sym_up]
        first_close = c[0][4]
        last_close = c[-1][4]
        change_pct = ((last_close - first_close) / first_close * 100) if first_close else 0
        high = max(r[2] for r in c)
        low = min(r[3] for r in c)
        volatility = ((high - low) / low * 100) if low else 0
        table.append({
            "symbol": sym_up,
            "price": last_close,
            "change_pct": round(change_pct, 2),
            "high": high,
            "low": low,
            "volatility_pct": round(volatility, 2),
            "source": sources[sym_up],
        })

    # Rank by change
    ranked = sorted(table, key=lambda r: r["change_pct"], reverse=True)
    for i, r in enumerate(ranked):
        r["rank"] = i + 1

    # Correlation matrix
    sym_list = [s.upper() for s in symbols]
    # align time series: use closes, resample to common timestamps
    close_series = {}
    for sym_up in sym_list:
        close_series[sym_up] = {r[0]: r[4] for r in all_candles[sym_up]}

    # find common timestamps (within 1-minute tolerance)
    all_ts = set()
    for sym_up in sym_list:
        all_ts.update(close_series[sym_up].keys())
    all_ts = sorted(all_ts)

    # build aligned arrays using nearest available price
    aligned = {s: [] for s in sym_list}
    common_ts = []
    for ts in all_ts:
        vals = {}
        for s in sym_list:
            if ts in close_series[s]:
                vals[s] = close_series[s][ts]
        if len(vals) == len(sym_list):
            common_ts.append(ts)
            for s in sym_list:
                aligned[s].append(vals[s])

    corr_matrix = None
    if len(common_ts) >= 5:
        # compute returns
        returns = {}
        for s in sym_list:
            arr = np.array(aligned[s])
            ret = np.diff(arr) / arr[:-1]
            returns[s] = ret
        n = len(sym_list)
        corr_matrix = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if len(returns[sym_list[i]]) > 0 and len(returns[sym_list[j]]) > 0:
                    c = np.corrcoef(returns[sym_list[i]], returns[sym_list[j]])[0, 1]
                    corr_matrix[i][j] = round(float(c), 3) if not math.isnan(c) else 0.0
                else:
                    corr_matrix[i][j] = 0.0

    # Build chart
    chart_path = _build_compare_chart(sym_list, all_candles, corr_matrix, label)

    # Text summary
    lines = [f"📊 CryptoLens Compare ({label})"]
    lines.append("")
    lines.append("Rank | Symbol | Price | Change | Volatility")
    lines.append("-----|--------|-------|--------|----------")
    for r in ranked:
        emoji = "🟢" if r["change_pct"] >= 0 else "🔴"
        lines.append(
            f"  {r['rank']}  | {r['symbol']:>6} | ${_format_price(r['price'])} | "
            f"{emoji} {r['change_pct']:+.2f}% | {r['volatility_pct']:.1f}%"
        )

    if corr_matrix:
        lines.append("")
        lines.append("Correlation Matrix:")
        header = "       " + "  ".join(f"{s:>6}" for s in sym_list)
        lines.append(header)
        for i, s in enumerate(sym_list):
            row_str = f"{s:>6} " + "  ".join(f"{corr_matrix[i][j]:>6.3f}" for j in range(len(sym_list)))
            lines.append(row_str)

    text = "\n".join(lines)

    result = {
        "command": "compare",
        "symbols": sym_list,
        "duration": label,
        "comparison": ranked,
        "correlation": {"symbols": sym_list, "matrix": corr_matrix} if corr_matrix else None,
        "chart_path": chart_path,
        "text_plain": text,
    }
    print(json.dumps(result, ensure_ascii=True))


def _build_compare_chart(sym_list, all_candles, corr_matrix, label):
    """Build comparison chart: normalized overlay + correlation heatmap."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        import matplotlib.font_manager as fm
        import numpy as np

        font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts", "Tomorrow.ttf")
        if os.path.exists(font_path):
            fm.fontManager.addfont(font_path)
            plt.rcParams["font.family"] = fm.FontProperties(fname=font_path).get_name()
    except Exception:
        return None

    has_corr = corr_matrix is not None and len(sym_list) >= 2

    if has_corr:
        fig, (ax_overlay, ax_corr) = plt.subplots(
            1, 2, figsize=(14, 7), facecolor="#121212",
            gridspec_kw={"width_ratios": [2.5, 1], "wspace": 0.3}
        )
    else:
        fig, ax_overlay = plt.subplots(figsize=(10, 7), facecolor="#121212")
        ax_corr = None

    ax_overlay.set_facecolor("#121212")

    colors = ["#00BFFF", "#FF6B6B", "#50FA7B", "#FFB86C", "#BD93F9"]

    # Normalized price overlay
    for i, sym in enumerate(sym_list):
        candles = all_candles[sym]
        times = [datetime.fromtimestamp(r[0] / 1000.0, tz=timezone.utc) for r in candles]
        closes = [r[4] for r in candles]
        base = closes[0] if closes[0] else 1
        normalized = [(c / base - 1) * 100 for c in closes]
        color = colors[i % len(colors)]
        ax_overlay.plot(times, normalized, color=color, linewidth=1.8, label=sym, zorder=3)
        # annotate last value
        if normalized:
            last_val = normalized[-1]
            ax_overlay.annotate(
                f"{sym} {last_val:+.1f}%",
                xy=(times[-1], last_val),
                fontsize=9, color=color, fontweight="bold",
                ha="left", va="center",
                xytext=(5, 0), textcoords="offset points",
            )

    ax_overlay.axhline(y=0, color="#555555", linestyle="--", linewidth=0.8, zorder=2)
    ax_overlay.set_title(f"Relative Performance ({label})", color="white", fontsize=13, fontweight="bold")
    ax_overlay.set_ylabel("Change %", color="#8b949e", fontsize=10)
    ax_overlay.tick_params(axis="x", colors="#8b949e")
    ax_overlay.tick_params(axis="y", colors="#8b949e")
    for spine in ax_overlay.spines.values():
        spine.set_color("#2a2f38")
    ax_overlay.grid(True, linestyle="-", linewidth=0.5, color="#1f2630", alpha=0.8, zorder=1)
    ax_overlay.legend(loc="upper left", fontsize=9, facecolor="#1a1a2e", edgecolor="#333",
                      labelcolor="white", framealpha=0.9)

    locator = mdates.AutoDateLocator(minticks=4, maxticks=8)
    ax_overlay.xaxis.set_major_locator(locator)
    ax_overlay.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

    # Correlation heatmap
    if has_corr and ax_corr is not None:
        import numpy as np
        ax_corr.set_facecolor("#121212")
        matrix = np.array(corr_matrix)
        n = len(sym_list)
        im = ax_corr.imshow(matrix, cmap="RdYlGn", vmin=-1, vmax=1, aspect="auto")
        ax_corr.set_xticks(range(n))
        ax_corr.set_yticks(range(n))
        ax_corr.set_xticklabels(sym_list, color="#8b949e", fontsize=9, rotation=45, ha="right")
        ax_corr.set_yticklabels(sym_list, color="#8b949e", fontsize=9)
        ax_corr.set_title("Correlation", color="white", fontsize=12, fontweight="bold")
        # annotate cells
        for i in range(n):
            for j in range(n):
                val = matrix[i, j]
                text_color = "black" if abs(val) > 0.5 else "white"
                ax_corr.text(j, i, f"{val:.2f}", ha="center", va="center",
                             color=text_color, fontsize=10, fontweight="bold")
        for spine in ax_corr.spines.values():
            spine.set_color("#2a2f38")

    # add right margin for labels
    ax_overlay.margins(x=0.08)

    ts = int(time.time())
    chart_path = f"/tmp/cryptolens_compare_{ts}.png"
    fig.subplots_adjust(left=0.06, right=0.94, top=0.94, bottom=0.08)
    fig.savefig(chart_path, dpi=150)
    plt.close(fig)
    return chart_path


# ---------------------------------------------------------------------------
# Command: chart (technical analysis)
# ---------------------------------------------------------------------------
def cmd_chart(symbol, args):
    """Single-coin candlestick chart with MA + RSI + MACD + Bollinger Bands."""
    if not _validate_symbol(symbol):
        return _err("invalid symbol format — alphanumeric only, max 20 chars")

    total_minutes, label = _parse_duration(args)
    user_id = _parse_user_id(args)

    sym_up = symbol.upper()

    # Billing: chart = 1 token
    ok, balance, pay_url = charge_user(user_id)
    if not ok:
        return _billing_fail(balance, pay_url)

    candles, source = get_candles(sym_up, total_minutes)
    if not candles:
        return _err(f"no data for {sym_up}")

    closes = [r[4] for r in candles]
    price = closes[-1]
    first_close = closes[0]
    change_pct = ((price - first_close) / first_close * 100) if first_close else 0

    # Calculate indicators
    ma7 = _ma(closes, 7)
    ma25 = _ma(closes, 25)
    ma99 = _ma(closes, 99)
    rsi = calc_rsi(closes, 14)
    macd_line, signal_line, histogram = calc_macd(closes)
    bb_upper, bb_middle, bb_lower = calc_bollinger(closes, 20)

    # Build chart
    chart_path = _build_ta_chart(sym_up, candles, ma7, ma25, ma99, rsi,
                                  macd_line, signal_line, histogram,
                                  bb_upper, bb_middle, bb_lower, label)

    # Current RSI value
    rsi_val = None
    for v in reversed(rsi):
        if v is not None:
            rsi_val = v
            break

    # Current MACD
    macd_val = None
    for v in reversed(macd_line):
        if v is not None:
            macd_val = v
            break

    emoji = "🟢" if change_pct >= 0 else "🔴"
    text_lines = [
        f"📊 {sym_up} Technical Analysis ({label})",
        f"Price: ${_format_price(price)} {emoji} {change_pct:+.2f}%",
        f"RSI(14): {rsi_val:.1f}" if rsi_val else "RSI(14): n/a",
        f"MACD: {macd_val:.4f}" if macd_val else "MACD: n/a",
        f"Source: {source}",
    ]
    text = "\n".join(text_lines)

    result = {
        "command": "chart",
        "symbol": sym_up,
        "duration": label,
        "price": price,
        "change_pct": round(change_pct, 2),
        "rsi": round(rsi_val, 2) if rsi_val else None,
        "macd": round(macd_val, 6) if macd_val else None,
        "source": source,
        "chart_path": chart_path,
        "text_plain": text,
    }
    print(json.dumps(result, ensure_ascii=True))


def _build_ta_chart(symbol, candles, ma7, ma25, ma99, rsi,
                     macd_line, signal_line, histogram,
                     bb_upper, bb_middle, bb_lower, label):
    """Build technical analysis chart: candlesticks + MA + BB | RSI | MACD."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from matplotlib.patches import Rectangle
        from matplotlib.lines import Line2D
        import matplotlib.font_manager as fm
        import numpy as np

        font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts", "Tomorrow.ttf")
        if os.path.exists(font_path):
            fm.fontManager.addfont(font_path)
            plt.rcParams["font.family"] = fm.FontProperties(fname=font_path).get_name()
    except Exception:
        return None

    fig, (ax_price, ax_rsi, ax_macd) = plt.subplots(
        3, 1, figsize=(12, 10), facecolor="#121212",
        gridspec_kw={"height_ratios": [3, 1, 1], "hspace": 0.12},
        sharex=True
    )

    for ax in (ax_price, ax_rsi, ax_macd):
        ax.set_facecolor("#121212")
        for spine in ax.spines.values():
            spine.set_color("#2a2f38")
        ax.tick_params(axis="x", colors="#8b949e")
        ax.tick_params(axis="y", colors="#8b949e")
        ax.grid(True, linestyle="-", linewidth=0.5, color="#1f2630", alpha=0.8, zorder=1)

    times = [datetime.fromtimestamp(r[0] / 1000.0, tz=timezone.utc) for r in candles]
    x_vals = mdates.date2num(times)

    if len(x_vals) > 1:
        delta = min(x_vals[i + 1] - x_vals[i] for i in range(len(x_vals) - 1))
    else:
        delta = 0.02
    width = delta * 0.7

    # --- Candlesticks ---
    lows_list = []
    highs_list = []
    for idx, row in enumerate(candles):
        _, o, h, l, c = row[:5]
        is_bull = c >= o
        color = "#26A69A" if is_bull else "#EF5350"  # green / red
        wick_color = "#555555"
        x = x_vals[idx]
        body_low = min(o, c)
        body_h = max(abs(c - o), 1e-9)

        wick = Line2D([x, x], [l, h], color=wick_color, linewidth=0.8, zorder=3)
        ax_price.add_line(wick)
        rect = Rectangle((x - width / 2, body_low), width, body_h,
                          facecolor=color, edgecolor="#000", linewidth=0.4, zorder=4)
        ax_price.add_patch(rect)
        lows_list.append(l)
        highs_list.append(h)

    # --- MA lines ---
    def _plot_ma(ax, x, ma_vals, color, lbl):
        xs, ys = [], []
        for i, v in enumerate(ma_vals):
            if v is not None:
                xs.append(x[i])
                ys.append(v)
        if xs:
            ax.plot(xs, ys, color=color, linewidth=1.0, label=lbl, zorder=5)

    _plot_ma(ax_price, x_vals, ma7, "#FFD54F", "MA7")
    _plot_ma(ax_price, x_vals, ma25, "#42A5F5", "MA25")
    _plot_ma(ax_price, x_vals, ma99, "#AB47BC", "MA99")

    # --- Bollinger Bands ---
    bb_x, bb_u, bb_l = [], [], []
    for i in range(len(bb_upper)):
        if bb_upper[i] is not None:
            bb_x.append(x_vals[i])
            bb_u.append(bb_upper[i])
            bb_l.append(bb_lower[i])
    if bb_x:
        ax_price.fill_between(bb_x, bb_l, bb_u, alpha=0.05, color="#42A5F5", zorder=2)
        ax_price.plot(bb_x, bb_u, color="#42A5F5", linewidth=0.6, linestyle="--", alpha=0.4, zorder=5, label="BB(20)")
        ax_price.plot(bb_x, bb_l, color="#42A5F5", linewidth=0.6, linestyle="--", alpha=0.4, zorder=5)

    # last price line
    last_close = candles[-1][4]
    ax_price.axhline(y=last_close, color="white", linestyle="--", linewidth=0.7, alpha=0.4, zorder=2)
    ax_price.annotate(
        f"${_format_price(last_close)}",
        xy=(max(x_vals) + delta * 0.3, last_close),
        fontsize=8, color="white", fontweight="bold", ha="left", va="center",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="#121212", edgecolor="white", linewidth=0.8),
        zorder=6, clip_on=False,
    )

    ax_price.set_title(f"{symbol} Technical Analysis ({label})",
                       color="white", fontsize=14, fontweight="bold", pad=10)
    ax_price.set_ylabel("USD", color="#8b949e", fontsize=10)
    handles, labels = ax_price.get_legend_handles_labels()
    if handles:
        ax_price.legend(loc="upper left", fontsize=8, facecolor="#1a1a2e", edgecolor="#333",
                        labelcolor="white", framealpha=0.9)

    if lows_list and highs_list:
        ymin, ymax = min(lows_list), max(highs_list)
        pad = (ymax - ymin) * 0.05
        ax_price.set_ylim(ymin - pad, ymax + pad)
    ax_price.set_xlim(min(x_vals) - delta, max(x_vals) + delta)

    # --- RSI ---
    rsi_x, rsi_y = [], []
    for i, v in enumerate(rsi):
        if v is not None:
            rsi_x.append(x_vals[i])
            rsi_y.append(v)
    if rsi_x:
        ax_rsi.plot(rsi_x, rsi_y, color="#E040FB", linewidth=1.2, zorder=3)
        ax_rsi.axhline(y=70, color="#EF5350", linestyle="--", linewidth=0.7, alpha=0.7)
        ax_rsi.axhline(y=30, color="#26A69A", linestyle="--", linewidth=0.7, alpha=0.7)
        ax_rsi.fill_between(rsi_x, 30, 70, alpha=0.05, color="#888", zorder=1)
    ax_rsi.set_ylabel("RSI(14)", color="#8b949e", fontsize=10)
    ax_rsi.set_ylim(0, 100)

    # --- MACD ---
    macd_x, macd_y = [], []
    sig_x, sig_y = [], []
    hist_x, hist_y = [], []
    for i, v in enumerate(macd_line):
        if v is not None:
            macd_x.append(x_vals[i])
            macd_y.append(v)
    for i, v in enumerate(signal_line):
        if v is not None:
            sig_x.append(x_vals[i])
            sig_y.append(v)
    for i, v in enumerate(histogram):
        if v is not None:
            hist_x.append(x_vals[i])
            hist_y.append(v)
    if macd_x:
        ax_macd.plot(macd_x, macd_y, color="#42A5F5", linewidth=1.0, label="MACD", zorder=3)
    if sig_x:
        ax_macd.plot(sig_x, sig_y, color="#FF7043", linewidth=1.0, label="Signal", zorder=3)
    if hist_x:
        hist_colors = ["#26A69A" if v >= 0 else "#EF5350" for v in hist_y]
        ax_macd.bar(hist_x, hist_y, width=width, color=hist_colors, alpha=0.6, zorder=2)
    ax_macd.axhline(y=0, color="#888", linewidth=0.8, zorder=1)
    ax_macd.set_ylabel("MACD(12,26,9)", color="#8b949e", fontsize=10)
    handles, labels = ax_macd.get_legend_handles_labels()
    if handles:
        ax_macd.legend(loc="upper left", fontsize=7, facecolor="#1a1a2e", edgecolor="#333",
                       labelcolor="white", framealpha=0.9)

    locator = mdates.AutoDateLocator(minticks=4, maxticks=10)
    ax_macd.xaxis.set_major_locator(locator)
    ax_macd.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

    # hide x-axis labels on price and RSI panels (only show on MACD)
    ax_price.tick_params(axis="x", labelbottom=False)
    ax_rsi.tick_params(axis="x", labelbottom=False)

    ts = int(time.time())
    chart_path = f"/tmp/cryptolens_chart_{symbol}_{ts}.png"
    fig.subplots_adjust(left=0.08, right=0.92, top=0.95, bottom=0.06)
    fig.savefig(chart_path, dpi=150)
    plt.close(fig)
    return chart_path


# ---------------------------------------------------------------------------
# Command: analyze (AI scoring engine)
# ---------------------------------------------------------------------------
def _score_label(score):
    if score >= 80:
        return "强烈看涨", "🟢🟢"
    if score >= 60:
        return "看涨", "🟢"
    if score >= 40:
        return "中性", "⚪"
    if score >= 20:
        return "看跌", "🔴"
    return "强烈看跌", "🔴🔴"


def _analyze_signals(closes, candles):
    """Run scoring engine on indicator data. Returns (score 0-100, signals list)."""
    signals = []
    raw_score = 0  # accumulate in range roughly -100..+100, then map to 0-100

    n = len(closes)
    if n < 30:
        return 50, [{"name": "Data", "signal": "⚠️ 数据不足（<30根K线），评分不可靠", "points": 0}]

    # --- 1. RSI ---
    rsi = calc_rsi(closes, 14)
    rsi_val = None
    for v in reversed(rsi):
        if v is not None:
            rsi_val = v
            break
    if rsi_val is not None:
        if rsi_val < 20:
            pts = 25
            sig = f"RSI={rsi_val:.1f} 极度超卖 → 强反弹信号"
        elif rsi_val < 30:
            pts = 20
            sig = f"RSI={rsi_val:.1f} 超卖区 → 看涨"
        elif rsi_val < 45:
            pts = 5
            sig = f"RSI={rsi_val:.1f} 偏弱但未超卖"
        elif rsi_val <= 55:
            pts = 0
            sig = f"RSI={rsi_val:.1f} 中性区间"
        elif rsi_val <= 70:
            pts = -5
            sig = f"RSI={rsi_val:.1f} 偏强但未超买"
        elif rsi_val <= 80:
            pts = -20
            sig = f"RSI={rsi_val:.1f} 超买区 → 看跌"
        else:
            pts = -25
            sig = f"RSI={rsi_val:.1f} 极度超买 → 回调风险大"
        raw_score += pts
        signals.append({"name": "RSI(14)", "signal": sig, "points": pts})

    # --- 2. MACD ---
    macd_line, signal_line, histogram = calc_macd(closes)
    # find last valid MACD and signal
    macd_val, sig_val = None, None
    hist_val, prev_hist = None, None
    for i in range(len(macd_line) - 1, -1, -1):
        if macd_line[i] is not None and macd_val is None:
            macd_val = macd_line[i]
        if signal_line[i] is not None and sig_val is None:
            sig_val = signal_line[i]
        if macd_val is not None and sig_val is not None:
            break
    for i in range(len(histogram) - 1, -1, -1):
        if histogram[i] is not None:
            if hist_val is None:
                hist_val = histogram[i]
            elif prev_hist is None:
                prev_hist = histogram[i]
                break

    if macd_val is not None and sig_val is not None:
        # golden cross / death cross
        # check if MACD just crossed signal (compare last 2 valid points)
        macd_prev, sig_prev = None, None
        for i in range(len(macd_line) - 2, -1, -1):
            if macd_line[i] is not None and signal_line[i] is not None:
                macd_prev = macd_line[i]
                sig_prev = signal_line[i]
                break

        if macd_prev is not None and sig_prev is not None:
            was_below = macd_prev < sig_prev
            is_above = macd_val > sig_val
            if was_below and is_above:
                pts = 15
                sig = "MACD 金叉（MACD上穿Signal）→ 看涨"
            elif not was_below and not is_above:
                pts = -15
                sig = "MACD 死叉（MACD下穿Signal）→ 看跌"
            elif is_above:
                pts = 8
                sig = f"MACD 在 Signal 上方（{macd_val:.4f} > {sig_val:.4f}）→ 偏多"
            else:
                pts = -8
                sig = f"MACD 在 Signal 下方（{macd_val:.4f} < {sig_val:.4f}）→ 偏空"
        else:
            pts = 5 if macd_val > sig_val else -5
            sig = f"MACD {'>' if macd_val > sig_val else '<'} Signal"
        raw_score += pts
        signals.append({"name": "MACD", "signal": sig, "points": pts})

    # MACD histogram momentum
    if hist_val is not None and prev_hist is not None:
        if hist_val > 0 and hist_val > prev_hist:
            pts = 5
            sig = "MACD柱 正且放大 → 多头动能增强"
        elif hist_val > 0 and hist_val < prev_hist:
            pts = 2
            sig = "MACD柱 正但缩小 → 多头动能减弱"
        elif hist_val < 0 and hist_val < prev_hist:
            pts = -5
            sig = "MACD柱 负且放大 → 空头动能增强"
        elif hist_val < 0 and hist_val > prev_hist:
            pts = -2
            sig = "MACD柱 负但缩小 → 空头动能减弱"
        else:
            pts = 0
            sig = "MACD柱 无明显变化"
        raw_score += pts
        signals.append({"name": "MACD柱", "signal": sig, "points": pts})

    # --- 3. MA alignment ---
    ma7 = _ma(closes, 7)
    ma25 = _ma(closes, 25)
    ma99 = _ma(closes, 99)
    ma7_val = next((v for v in reversed(ma7) if v is not None), None)
    ma25_val = next((v for v in reversed(ma25) if v is not None), None)
    ma99_val = next((v for v in reversed(ma99) if v is not None), None)

    if ma7_val and ma25_val and ma99_val:
        if ma7_val > ma25_val > ma99_val:
            pts = 15
            sig = f"MA7>MA25>MA99 多头排列 → 强势趋势"
        elif ma7_val < ma25_val < ma99_val:
            pts = -15
            sig = f"MA7<MA25<MA99 空头排列 → 弱势趋势"
        elif ma7_val > ma25_val:
            pts = 5
            sig = "MA7>MA25 短期偏多"
        elif ma7_val < ma25_val:
            pts = -5
            sig = "MA7<MA25 短期偏空"
        else:
            pts = 0
            sig = "MA 交织 → 方向不明"
        raw_score += pts
        signals.append({"name": "MA趋势", "signal": sig, "points": pts})

    # --- 4. Price vs MA ---
    last_price = closes[-1]
    if ma25_val:
        pct_from_ma25 = (last_price - ma25_val) / ma25_val * 100
        if pct_from_ma25 > 5:
            pts = -5
            sig = f"价格高于MA25 {pct_from_ma25:.1f}% → 短期过热"
        elif pct_from_ma25 > 0:
            pts = 3
            sig = f"价格在MA25上方 +{pct_from_ma25:.1f}% → 偏强"
        elif pct_from_ma25 > -5:
            pts = -3
            sig = f"价格在MA25下方 {pct_from_ma25:.1f}% → 偏弱"
        else:
            pts = 5
            sig = f"价格远低于MA25 {pct_from_ma25:.1f}% → 超跌"
        raw_score += pts
        signals.append({"name": "价格/MA25", "signal": sig, "points": pts})

    # --- 5. Bollinger Band position ---
    bb_upper, bb_middle, bb_lower = calc_bollinger(closes, 20)
    bb_u = next((v for v in reversed(bb_upper) if v is not None), None)
    bb_l = next((v for v in reversed(bb_lower) if v is not None), None)
    if bb_u is not None and bb_l is not None and bb_u != bb_l:
        bb_pct = (last_price - bb_l) / (bb_u - bb_l)  # 0=lower, 1=upper
        if bb_pct <= 0.05:
            pts = 15
            sig = f"价格触及BB下轨（{bb_pct:.0%}）→ 超卖反弹信号"
        elif bb_pct <= 0.2:
            pts = 10
            sig = f"价格接近BB下轨（{bb_pct:.0%}）→ 偏看涨"
        elif bb_pct >= 0.95:
            pts = -15
            sig = f"价格触及BB上轨（{bb_pct:.0%}）→ 超买回调信号"
        elif bb_pct >= 0.8:
            pts = -10
            sig = f"价格接近BB上轨（{bb_pct:.0%}）→ 偏看跌"
        else:
            pts = 0
            sig = f"价格在BB中间区域（{bb_pct:.0%}）→ 中性"
        raw_score += pts
        signals.append({"name": "布林带", "signal": sig, "points": pts})

    # --- 6. Volume trend (if available) ---
    volumes = [r[5] for r in candles if len(r) >= 6]
    if len(volumes) >= 10:
        recent_vol = sum(volumes[-5:]) / 5
        older_vol = sum(volumes[-10:-5]) / 5
        if older_vol > 0:
            vol_change = (recent_vol - older_vol) / older_vol * 100
            # volume increase with price increase = bullish confirmation
            price_up = closes[-1] > closes[-6] if len(closes) >= 6 else True
            if vol_change > 30 and price_up:
                pts = 8
                sig = f"成交量放大{vol_change:.0f}% + 价格上涨 → 量价齐升看涨"
            elif vol_change > 30 and not price_up:
                pts = -8
                sig = f"成交量放大{vol_change:.0f}% + 价格下跌 → 放量下跌看跌"
            elif vol_change < -30:
                pts = -3
                sig = f"成交量萎缩{vol_change:.0f}% → 观望情绪浓"
            else:
                pts = 0
                sig = f"成交量变化{vol_change:+.0f}% → 正常"
            raw_score += pts
            signals.append({"name": "成交量", "signal": sig, "points": pts})

    # --- 7. Short-term momentum ---
    if len(closes) >= 6:
        momentum = (closes[-1] - closes[-6]) / closes[-6] * 100
        if momentum > 5:
            pts = 5
            sig = f"短期动量 {momentum:+.2f}% → 强势"
        elif momentum > 0:
            pts = 2
            sig = f"短期动量 {momentum:+.2f}% → 温和上涨"
        elif momentum > -5:
            pts = -2
            sig = f"短期动量 {momentum:+.2f}% → 温和下跌"
        else:
            pts = -5
            sig = f"短期动量 {momentum:+.2f}% → 弱势"
        raw_score += pts
        signals.append({"name": "动量", "signal": sig, "points": pts})

    # --- Normalize to 0-100 ---
    # raw_score theoretical range: roughly -100 to +100
    # map to 0-100 with center at 50
    score = max(0, min(100, 50 + raw_score * 0.5))
    score = round(score)

    return score, signals


def cmd_analyze(symbol, args):
    """AI market analysis with scoring engine."""
    if not _validate_symbol(symbol):
        return _err("invalid symbol format — alphanumeric only, max 20 chars")

    total_minutes, label = _parse_duration(args)
    user_id = _parse_user_id(args)
    sym_up = symbol.upper()

    # Billing: analyze = 1 token (same as chart)
    ok, balance, pay_url = charge_user(user_id)
    if not ok:
        return _billing_fail(balance, pay_url)

    candles, source = get_candles(sym_up, total_minutes)
    if not candles:
        return _err(f"no data for {sym_up}")

    closes = [r[4] for r in candles]
    price = closes[-1]
    first_close = closes[0]
    change_pct = ((price - first_close) / first_close * 100) if first_close else 0

    # Run scoring engine
    score, signals = _analyze_signals(closes, candles)
    label_text, label_emoji = _score_label(score)

    # Generate TA chart (reuse chart logic)
    ma7 = _ma(closes, 7)
    ma25 = _ma(closes, 25)
    ma99 = _ma(closes, 99)
    rsi = calc_rsi(closes, 14)
    macd_line, signal_line, histogram = calc_macd(closes)
    bb_upper, bb_middle, bb_lower = calc_bollinger(closes, 20)
    chart_path = _build_ta_chart(sym_up, candles, ma7, ma25, ma99, rsi,
                                  macd_line, signal_line, histogram,
                                  bb_upper, bb_middle, bb_lower, label)

    # Build action suggestion
    if score >= 80:
        action = "多头信号强烈，可考虑建仓/加仓，止损设在MA25下方"
    elif score >= 65:
        action = "偏多格局，轻仓试多，关注MA7支撑"
    elif score >= 55:
        action = "略偏多但信号不强，建议观望或小仓位"
    elif score >= 45:
        action = "多空分歧，暂时观望等待方向明确"
    elif score >= 35:
        action = "略偏空但未确认，谨慎持有，注意止损"
    elif score >= 20:
        action = "偏空格局，减仓或做空，阻力位在MA25附近"
    else:
        action = "空头信号强烈，建议离场或做空，反弹做空优先"

    # RSI value for output
    rsi_val = next((v for v in reversed(rsi) if v is not None), None)

    # Text output
    price_emoji = "🟢" if change_pct >= 0 else "🔴"
    lines = [
        f"📊 {sym_up} AI 市场分析 ({label})",
        f"",
        f"💰 价格: ${_format_price(price)} {price_emoji} {change_pct:+.2f}%",
        f"🎯 综合评分: {score}/100 {label_emoji} {label_text}",
        f"",
        f"📝 逐项分析:",
    ]
    for s in signals:
        arrow = "↑" if s["points"] > 0 else ("↓" if s["points"] < 0 else "→")
        lines.append(f"  {arrow} [{s['name']}] {s['signal']} ({s['points']:+d})")
    lines.append(f"")
    lines.append(f"💡 操作建议: {action}")

    text = "\n".join(lines)

    result = {
        "command": "analyze",
        "symbol": sym_up,
        "duration": label,
        "price": price,
        "change_pct": round(change_pct, 2),
        "score": score,
        "label": label_text,
        "signals": signals,
        "action": action,
        "rsi": round(rsi_val, 2) if rsi_val else None,
        "source": source,
        "chart_path": chart_path,
        "text_plain": text,
    }
    print(json.dumps(result, ensure_ascii=True))


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------
def _err(msg):
    print(json.dumps({"error": msg}))


def _billing_fail(balance, payment_url):
    result = {
        "error": "insufficient_balance",
        "message": "Insufficient balance. Please top up to continue.",
        "balance": balance,
        "payment_url": payment_url,
    }
    print(json.dumps(result))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        _err("Usage: crypto_lens.py <compare|chart> <SYMBOL(S)> [options]")
        return 1

    cmd = sys.argv[1].lower()

    if cmd == "compare":
        if len(sys.argv) < 4:
            _err("Usage: crypto_lens.py compare SYM1 SYM2 [SYM3...] [--duration 7d] [--user-id UID]")
            return 1
        # collect symbols (non-flag args after 'compare')
        symbols = []
        rest = []
        for arg in sys.argv[2:]:
            if arg.startswith("--"):
                rest.append(arg)
            elif rest:
                rest.append(arg)
            else:
                symbols.append(arg)
        cmd_compare(symbols, rest + sys.argv[2:])

    elif cmd == "chart":
        if len(sys.argv) < 3:
            _err("Usage: crypto_lens.py chart SYMBOL [--duration 24h] [--user-id UID]")
            return 1
        symbol = sys.argv[2]
        cmd_chart(symbol, sys.argv[3:])

    elif cmd == "analyze":
        if len(sys.argv) < 3:
            _err("Usage: crypto_lens.py analyze SYMBOL [--duration 24h] [--user-id UID]")
            return 1
        symbol = sys.argv[2]
        cmd_analyze(symbol, sys.argv[3:])

    else:
        _err(f"Unknown command: {cmd}. Use 'compare', 'chart', or 'analyze'.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
