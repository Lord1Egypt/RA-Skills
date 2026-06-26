"""Data fetch helpers for FusionAlpha A&Crypto Desk.

These helpers are designed to be called by any agent/tooling layer and return JSON.

Dependencies:
    pip install -r requirements.txt

Notes:
- Public endpoints can intermittently fail; return partial data + keep schema stable.
- CryptoPanic news requires user token via CRYPTOPANIC_TOKEN env (optional).
- Do not print secrets; JSON goes to stdout, diagnostics should be handled by caller.
"""

import contextlib
import sys
import os
import json
import datetime as dt
import time

from typing import Any, Dict, List, Optional, cast

import akshare as ak  # type: ignore
import ccxt  # type: ignore
import pandas as pd  # type: ignore
import requests

sys.dont_write_bytecode = True

JSONDict = Dict[str, Any]
JSONList = List[JSONDict]


def to_jsonable(obj: Any) -> Any:
    """Convert common non-JSON types (numpy/pandas) into JSON-safe builtins."""

    if obj is None:
        return None

    if isinstance(obj, (str, int, bool)):
        return obj

    if isinstance(obj, float):
        # JSON has no NaN/Inf; convert to null
        if obj != obj or obj in (float("inf"), float("-inf")):
            return None
        return obj

    if isinstance(obj, (dt.datetime, dt.date)):
        return obj.isoformat()

    # pandas Timestamp, numpy scalar, etc.
    if hasattr(obj, "to_pydatetime"):
        try:
            return obj.to_pydatetime().isoformat()
        except Exception:
            pass

    if hasattr(obj, "item"):
        try:
            return to_jsonable(obj.item())
        except Exception:
            pass

    if isinstance(obj, dict):
        return {str(k): to_jsonable(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple)):
        return [to_jsonable(v) for v in obj]

    return str(obj)


def fetch_crypto(symbol: str = "BTC/USDT") -> JSONDict:
    ex = ccxt.binanceusdm({"enableRateLimit": True})
    meta: JSONDict = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "errors": [],
    }
    try:
        ex.load_markets()
    except Exception as exc:
        meta["errors"].append(f"load_markets: {type(exc).__name__}: {exc}")

    normalized_symbol = _normalize_binanceusdm_symbol(ex, symbol)
    data: JSONDict = {
        "symbol": normalized_symbol,
        "symbol_input": symbol,
    }

    ohlcv_frames: dict[str, pd.DataFrame] = {}

    # ticker
    try:
        ticker = ex.fetch_ticker(normalized_symbol)
        data["current_price"] = ticker.get("last")
    except Exception as exc:
        meta["errors"].append(f"ticker: {type(exc).__name__}: {exc}")
        data["current_price"] = None

    # 5m ema20
    try:
        ohlcv_5m = ex.fetch_ohlcv(normalized_symbol, "5m", limit=300)
        df_5m = pd.DataFrame(ohlcv_5m, columns=["ts", "o", "h", "l", "c", "v"])
        if not df_5m.empty:
            close5 = pd.to_numeric(cast(pd.Series, df_5m["c"]), errors="coerce")
            data["ema20_on_5m_chart"] = cast(
                Any, close5.ewm(span=20, adjust=False).mean()
            ).iloc[-1]
    except Exception as exc:
        meta["errors"].append(f"ohlcv_5m: {type(exc).__name__}: {exc}")
        data["ema20_on_5m_chart"] = None

    # indicators
    for tf, key in [("15m", "indicators_15m"), ("1h", "indicators_1h")]:
        try:
            ohlcv = ex.fetch_ohlcv(normalized_symbol, tf, limit=200)
            df = pd.DataFrame(ohlcv, columns=["ts", "o", "h", "l", "c", "v"])
            ind: JSONDict = {}
            if not df.empty:
                ohlcv_frames[tf] = df
                close = cast(
                    pd.Series, pd.to_numeric(cast(pd.Series, df["c"]), errors="coerce")
                )
                ind["rsi"] = _rsi(close, 14)
                ind["macd"] = {"histogram": _macd_hist(close)}
                ind["kdj"] = _kdj(df)
                if tf == "1h":
                    ema200 = close.ewm(span=200, adjust=False).mean()
                    ind["ema200"] = cast(Any, ema200).iloc[-1]
            data[key] = ind
        except Exception as exc:
            meta["errors"].append(f"ohlcv_{tf}: {type(exc).__name__}: {exc}")
            data[key] = {}

    # market cycle + vpvr (derived)
    try:
        data["market_cycle_indicators"] = {}
        data["vpvr_analysis"] = {}
        for tf, df in ohlcv_frames.items():
            data["market_cycle_indicators"][tf] = _market_cycle_from_ohlcv(df)
            data["vpvr_analysis"][tf] = _vpvr_from_ohlcv(df)
    except Exception as exc:
        meta["errors"].append(f"derived_cycle_vpvr: {type(exc).__name__}: {exc}")

    # order book snapshot (top3 levels)
    try:
        ob: JSONDict = ex.fetch_l2_order_book(normalized_symbol, limit=100)
        bid_sum = _sum_depth(ob.get("bids", []), depth=20)
        ask_sum = _sum_depth(ob.get("asks", []), depth=20)
        data["order_book_analysis"] = {
            "pressure_ratio": (bid_sum / ask_sum) if ask_sum else None,
            "top_support_levels": {str(p): v for p, v in ob.get("bids", [])[:3]},
            "top_resistance_levels": {str(p): v for p, v in ob.get("asks", [])[:3]},
        }
    except Exception as exc:
        meta["errors"].append(f"order_book: {type(exc).__name__}: {exc}")
        data["order_book_analysis"] = {}

    # derivatives
    try:
        funding_any = ex.fetch_funding_rate(normalized_symbol)
        funding = cast(JSONDict, funding_any) if isinstance(funding_any, dict) else {}
        derivatives: JSONDict = {"funding_rate": funding.get("fundingRate")}
        try:
            oi_any = ex.fetch_open_interest(normalized_symbol)
            oi = cast(JSONDict, oi_any) if isinstance(oi_any, dict) else {}
            oi_amount = oi.get("openInterestAmount")
            derivatives["open_interest_amount"] = oi_amount

            oi_amount_f = _to_float(oi_amount)
            price_f = _to_float(data.get("current_price"))
            if oi_amount_f is not None and price_f is not None:
                derivatives["open_interest_usd"] = oi_amount_f * price_f
            else:
                derivatives["open_interest_usd"] = oi.get("openInterestValue")
        except Exception:
            pass
        try:
            oi_hist = ex.fetch_open_interest_history(
                normalized_symbol, timeframe="1h", limit=25
            )
            if isinstance(oi_hist, list) and len(oi_hist) >= 2:
                oi0 = _to_float(cast(JSONDict, oi_hist[0]).get("openInterestAmount"))
                oi1 = _to_float(cast(JSONDict, oi_hist[-1]).get("openInterestAmount"))
                derivatives["open_interest_change_24h_percent"] = (
                    ((oi1 - oi0) / oi0 * 100)
                    if (oi0 is not None and oi1 is not None and oi0 != 0)
                    else None
                )
        except Exception:
            pass

        # Binance public long/short ratio (best-effort)
        try:
            raw = _binance_fapi_symbol(normalized_symbol)
            derivatives.update(_binance_fapi_long_short_ratio(raw, period="5m"))
        except Exception:
            pass
        data["derivatives_data"] = derivatives
    except Exception as exc:
        meta["errors"].append(f"derivatives: {type(exc).__name__}: {exc}")
        data["derivatives_data"] = {}

    # trades / microstructure (optional but useful)
    try:
        trades = ex.fetch_trades(normalized_symbol, limit=500)
        ms = _microstructure_from_trades(trades)
        if ms:
            data.update(ms)
    except Exception as exc:
        meta["errors"].append(f"trades: {type(exc).__name__}: {exc}")
        pass

    # news (optional)
    token = os.getenv("CRYPTOPANIC_TOKEN")
    if token:
        try:
            data["news"] = fetch_cryptopanic(token, _base_symbol(normalized_symbol))
        except Exception:
            data["news"] = []
    else:
        data["news"] = []

    data["meta"] = meta

    return data


def _normalize_binanceusdm_symbol(ex: Any, symbol: str) -> str:
    """Accept common spot-style symbols and map to binanceusdm unified symbols."""

    if not symbol:
        return symbol

    markets = getattr(ex, "markets", None) or {}
    if symbol in markets:
        return symbol

    if ":" in symbol:
        return symbol

    if "/" in symbol:
        base, quote = symbol.split("/", 1)
        candidate = f"{base}/{quote}:{quote}"
        if candidate in markets:
            return candidate

    if symbol.isalnum() and symbol.upper().endswith("USDT"):
        raw = symbol.upper()
        base = raw[:-4]
        quote = "USDT"
        candidate = f"{base}/{quote}:{quote}"
        if candidate in markets:
            return candidate

    return symbol


def _base_symbol(symbol: str) -> str:
    if not symbol:
        return symbol
    if "/" in symbol:
        return symbol.split("/", 1)[0]
    raw = symbol.upper()
    if raw.endswith("USDT") and len(raw) > 4:
        return raw[:-4]
    return symbol


def _sum_depth(levels: Any, depth: int = 20) -> float:
    total = 0.0
    if not isinstance(levels, list):
        return total
    for lvl in levels[:depth]:
        try:
            total += float(lvl[1])
        except Exception:
            continue
    return total


def _microstructure_from_trades(trades: Any) -> JSONDict:
    if not isinstance(trades, list) or not trades:
        return {}

    now_ms = int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000)
    cutoff_10m = now_ms - 10 * 60 * 1000

    buy_usd_500 = 0.0
    sell_usd_500 = 0.0

    buy_usd_10m = 0.0
    sell_usd_10m = 0.0

    large_buy_10m = 0.0
    large_sell_10m = 0.0
    large_threshold = 100_000.0

    trades_10m = []
    for t in trades:
        side = t.get("side")
        cost = t.get("cost")
        ts = t.get("timestamp")
        try:
            cost_f = float(cost) if cost is not None else None
        except Exception:
            cost_f = None

        if cost_f is not None:
            if side == "buy":
                buy_usd_500 += cost_f
            elif side == "sell":
                sell_usd_500 += cost_f

        if isinstance(ts, (int, float)) and ts >= cutoff_10m:
            trades_10m.append(t)
            if cost_f is not None:
                if side == "buy":
                    buy_usd_10m += cost_f
                    if cost_f >= large_threshold:
                        large_buy_10m += cost_f
                elif side == "sell":
                    sell_usd_10m += cost_f
                    if cost_f >= large_threshold:
                        large_sell_10m += cost_f

    taker_total_500 = buy_usd_500 + sell_usd_500
    taker_ratio_500 = (buy_usd_500 / taker_total_500) if taker_total_500 else None

    cvd_10m = buy_usd_10m - sell_usd_10m
    dominant = "neutral"
    if buy_usd_10m > sell_usd_10m:
        dominant = "buy"
    elif sell_usd_10m > buy_usd_10m:
        dominant = "sell"

    cvd_dir = "flat"
    if cvd_10m > 0:
        cvd_dir = "upward"
    elif cvd_10m < 0:
        cvd_dir = "downward"

    absorption: JSONDict = {"status": "none", "strength": "none"}
    if len(trades_10m) >= 10:
        try:
            p0 = float(trades_10m[0].get("price"))
            p1 = float(trades_10m[-1].get("price"))
            dp = p1 - p0
            strength = (
                abs(cvd_10m) / (buy_usd_10m + sell_usd_10m)
                if (buy_usd_10m + sell_usd_10m)
                else 0.0
            )
            strength_label = "weak"
            if strength >= 0.25:
                strength_label = "strong"
            elif strength <= 0.05:
                strength_label = "weak"
            if dp > 0 and cvd_10m < 0:
                absorption = {
                    "status": "Sell Absorption (Bullish)",
                    "strength": strength_label,
                }
            elif dp < 0 and cvd_10m > 0:
                absorption = {
                    "status": "Buy Absorption (Bearish)",
                    "strength": strength_label,
                }
        except Exception:
            pass

    return {
        "taker_volume_analysis": {
            "taker_buy_volume_usd_500trades": buy_usd_500,
            "taker_sell_volume_usd_500trades": sell_usd_500,
            "taker_ratio_500trades": taker_ratio_500,
        },
        "micro_structure_analysis": {
            "cvd_analysis": {
                "cvd_10m_usd": cvd_10m,
                "cvd_slope_direction": cvd_dir,
            },
            "large_trade_flow": {
                "net_large_trade_flow_usd_10m": large_buy_10m - large_sell_10m,
                "dominant_side": dominant,
            },
            "absorption_analysis": absorption,
        },
    }


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        return None


def _bollinger_width(close: pd.Series, window: int = 20) -> Optional[float]:
    if close is None or close.empty:
        return None
    mean = close.rolling(window=window).mean()
    std = close.rolling(window=window).std()
    m = mean.iloc[-1]
    s = std.iloc[-1]
    if pd.isna(m) or pd.isna(s) or m == 0:
        return None
    upper = m + 2 * s
    lower = m - 2 * s
    return float((upper - lower) / m)


def _atr(
    high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14
) -> Optional[float]:
    if high is None or low is None or close is None:
        return None
    if high.empty or low.empty or close.empty:
        return None
    prev_close = close.shift(1)
    tr = pd.concat(
        [
            (high - low).abs(),
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    atr_val = tr.rolling(window=period).mean().iloc[-1]
    if pd.isna(atr_val):
        return None
    return float(atr_val)


def _market_cycle_from_ohlcv(df: pd.DataFrame) -> JSONDict:
    if df is None or df.empty:
        return {}
    try:
        close = df["c"].astype(float)
        high = df["h"].astype(float)
        low = df["l"].astype(float)
    except Exception:
        return {}

    bb_width = _bollinger_width(close, window=20)
    atr_val = _atr(high, low, close, period=14)

    phase = None
    if bb_width is not None:
        if bb_width < 0.02:
            phase = "range"
        elif bb_width > 0.06:
            phase = "breakout"
        else:
            phase = "broad_channel"

    return {"bb_width": bb_width, "atr": atr_val, "phase": phase}


def _vpvr_from_ohlcv(df: pd.DataFrame, bins: int = 48) -> JSONDict:
    if df is None or df.empty:
        return {}
    if bins < 10:
        bins = 10

    try:
        highs = df["h"].astype(float).tolist()
        lows = df["l"].astype(float).tolist()
        closes = df["c"].astype(float).tolist()
        vols = df["v"].astype(float).tolist()
    except Exception:
        return {}

    lo = min(lows) if lows else None
    hi = max(highs) if highs else None
    if lo is None or hi is None or hi <= lo:
        return {}

    step = (hi - lo) / float(bins)
    if step <= 0:
        return {}

    vol_bins = [0.0 for _ in range(bins)]
    for h, l, c, v in zip(highs, lows, closes, vols):
        tp = (h + l + c) / 3.0
        qv = v * tp
        idx = int((tp - lo) / step)
        if idx < 0:
            idx = 0
        elif idx >= bins:
            idx = bins - 1
        vol_bins[idx] += qv

    total = sum(vol_bins)
    if total <= 0:
        return {}

    poc_idx = max(range(bins), key=lambda i: vol_bins[i])
    poc = lo + (poc_idx + 0.5) * step

    # value area (70% of volume) via contiguous expansion around POC
    target = total * 0.7
    start = end = poc_idx
    cum = vol_bins[poc_idx]
    while cum < target and (start > 0 or end < bins - 1):
        left = vol_bins[start - 1] if start > 0 else -1.0
        right = vol_bins[end + 1] if end < bins - 1 else -1.0
        if right > left:
            end += 1
            cum += vol_bins[end]
        else:
            start -= 1
            cum += vol_bins[start]

    val = lo + start * step
    vah = lo + (end + 1) * step

    nonzero = [(v, i) for i, v in enumerate(vol_bins) if v > 0]
    hvn = [lo + (i + 0.5) * step for v, i in sorted(nonzero, reverse=True)[:3]]
    lvn = [lo + (i + 0.5) * step for v, i in sorted(nonzero, key=lambda x: x[0])[:3]]

    return {
        "poc": poc,
        "hvn": hvn,
        "lvn": lvn,
        "value_area": {"vah": vah, "val": val},
    }


def _binance_fapi_symbol(symbol: str) -> str:
    if not symbol:
        return symbol
    s = symbol
    if ":" in s:
        s = s.split(":", 1)[0]
    return s.replace("/", "").upper()


def _binance_fapi_long_short_ratio(raw_symbol: str, period: str = "5m") -> JSONDict:
    """Best-effort long/short ratio from Binance public futures endpoints."""

    if not raw_symbol:
        return {}

    url = "https://fapi.binance.com/futures/data/globalLongShortAccountRatio"
    params = {"symbol": raw_symbol, "period": period, "limit": 1}
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            return {}
        payload = resp.json()
        if not isinstance(payload, list) or not payload:
            return {}
        item = payload[-1]
        if not isinstance(item, dict):
            return {}
        return {
            "long_short_ratio": _to_float(item.get("longShortRatio")),
            "long_account": _to_float(item.get("longAccount")),
            "short_account": _to_float(item.get("shortAccount")),
            "long_short_ratio_timestamp": item.get("timestamp"),
        }
    except Exception:
        return {}


def fetch_cryptopanic(
    token: str, base_symbol: str, kind: str = "news", limit: int = 5
) -> JSONList:
    url = (
        "https://cryptopanic.com/api/developer/v2/posts/?"
        f"auth_token={token}&public=true&currencies={base_symbol}&kind={kind}"
    )
    try:
        resp = requests.get(url, timeout=10)
    except requests.RequestException:
        raise RuntimeError("CryptoPanic request failed") from None

    if resp.status_code != 200:
        raise RuntimeError(f"CryptoPanic HTTP {resp.status_code}")

    try:
        results = resp.json().get("results", [])
    except ValueError:
        raise RuntimeError("CryptoPanic invalid JSON") from None
    items: JSONList = []
    for item in results[:limit]:
        votes: JSONDict = item.get("votes", {})
        items.append(
            {
                "title": item.get("title"),
                "published_at": item.get("published_at"),
                "source_name": item.get("source", {}).get("title"),
                "votes": {
                    "positive": votes.get("positive", 0),
                    "negative": votes.get("negative", 0),
                    "important": votes.get("important", 0),
                },
            }
        )
    return items


def _financial_abstract_latest(df: Optional[pd.DataFrame]) -> JSONDict:
    """Extract a small, latest-period snapshot from ak.stock_financial_abstract."""

    if df is None or df.empty:
        return {}
    if "指标" not in df.columns:
        return {}

    date_cols = [
        c for c in df.columns if isinstance(c, str) and c.isdigit() and len(c) == 8
    ]
    if not date_cols:
        return {}

    latest = max(date_cols)
    want = [
        "营业总收入",
        "归母净利润",
        "毛利率",
        "资产负债率",
        "净资产收益率(ROE)",
        "经营现金流量净额",
    ]

    out: JSONDict = {"report_date": latest}
    for ind in want:
        row_df = cast(pd.DataFrame, df.loc[df["指标"].astype(str) == ind])
        if row_df.empty:
            continue
        try:
            out[ind] = row_df.iloc[0][latest]
        except Exception:
            continue

    return out


def fetch_ashare(code: str = "600519") -> JSONDict:
    full: JSONDict = {"stock_code": code}
    meta: JSONDict = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "errors": [],
    }

    info_map: JSONDict = {}
    try:
        info = _retry_call(lambda: ak.stock_individual_info_em(symbol=code), retries=1)
        info_map = {
            str(row["item"]): row["value"]
            for _, row in info.iterrows()
            if "item" in info.columns and "value" in info.columns
        }
    except Exception as exc:
        meta["errors"].append(f"quote_data: {type(exc).__name__}: {exc}")
        info_map = {}

    stock_name = info_map.get("股票简称") or info_map.get("股票名称") or code
    full["stock_name"] = stock_name
    full["quote_data"] = info_map

    try:
        ba = _retry_call(lambda: ak.stock_bid_ask_em(symbol=code), retries=1)
        full["order_book_data"] = {
            str(row["item"]): row["value"]
            for _, row in ba.iterrows()
            if "item" in ba.columns and "value" in ba.columns
        }
    except Exception as exc:
        meta["errors"].append(f"order_book_data: {type(exc).__name__}: {exc}")
        full["order_book_data"] = {}

    try:
        end = dt.datetime.now().strftime("%Y%m%d")
        start = (dt.datetime.now() - dt.timedelta(days=365)).strftime("%Y%m%d")
        hist = _retry_call(
            lambda: ak.stock_zh_a_hist(
                symbol=code,
                period="daily",
                start_date=start,
                end_date=end,
                adjust="qfq",
            ),
            retries=1,
        )
        full["technical_indicators"] = _ta_from_hist(hist)
    except Exception as exc:
        meta["errors"].append(f"technical_indicators: {type(exc).__name__}: {exc}")
        full["technical_indicators"] = {}

    try:
        ff = _retry_call(
            lambda: ak.stock_individual_fund_flow(
                stock=code, market="sh" if code.startswith("6") else "sz"
            ),
            retries=1,
        )
        if ff is None:
            full["fund_flow_data"] = []
        else:
            if "日期" in ff.columns:
                ff = ff.sort_values("日期", ascending=False)
            full["fund_flow_data"] = ff.head(5).to_dict("records")
    except Exception as exc:
        meta["errors"].append(f"fund_flow_data: {type(exc).__name__}: {exc}")
        full["fund_flow_data"] = []

    fundamental: JSONDict = {
        "industry": info_map.get("行业"),
        "listing_date": info_map.get("上市时间"),
        "market_cap": info_map.get("总市值"),
        "float_market_cap": info_map.get("流通市值"),
        "total_shares": info_map.get("总股本"),
        "float_shares": info_map.get("流通股"),
    }

    # financial snapshot (best-effort)
    try:
        fa = _retry_call(lambda: ak.stock_financial_abstract(symbol=code), retries=1)
        fundamental["financial_abstract_latest"] = _financial_abstract_latest(fa)
    except Exception as exc:
        meta["errors"].append(f"financial_abstract: {type(exc).__name__}: {exc}")
        fundamental["financial_abstract_latest"] = {}

    full["fundamental_data"] = fundamental

    # news + research (best-effort)
    latest_news = []
    try:
        df_news = _retry_call(lambda: ak.stock_news_em(symbol=code), retries=1)
        latest_news = df_news.head(10).to_dict("records") if df_news is not None else []
        for item in latest_news:
            content = item.get("新闻内容")
            if isinstance(content, str) and len(content) > 800:
                item["新闻内容"] = content[:800] + "..."
    except Exception as exc:
        meta["errors"].append(f"latest_news: {type(exc).__name__}: {exc}")
        latest_news = []

    research_reports = []
    try:
        df_rr = _retry_call(lambda: ak.stock_research_report_em(symbol=code), retries=1)
        if df_rr is not None:
            if "日期" in df_rr.columns:
                df_rr = df_rr.sort_values("日期", ascending=False)
            keep = [
                c
                for c in [
                    "日期",
                    "机构",
                    "报告名称",
                    "东财评级",
                    "行业",
                    "报告PDF链接",
                ]
                if c in df_rr.columns
            ]
            research_reports = (
                df_rr[keep].head(10).to_dict("records")
                if keep
                else df_rr.head(10).to_dict("records")
            )
    except Exception as exc:
        meta["errors"].append(f"research_reports: {type(exc).__name__}: {exc}")
        research_reports = []

    full["news_and_reports_data"] = {
        "latest_news": latest_news,
        "research_reports": research_reports,
    }

    full["meta"] = meta

    return full


def fetch_morning(
    date: Optional[str] = None,
    top_n_industries: int = 10,
    top_n_limitups: int = 30,
    top_n_lhb: int = 20,
    top_n_breakfast: int = 10,
) -> JSONDict:
    """Fetch A-share morning briefing inputs.

    Returns the JSON shape documented in references/data_sources.md.
    """

    target_date = _parse_yyyymmdd(date) or dt.date.today()
    date_yyyymmdd = target_date.strftime("%Y%m%d")
    prev_trade_date = _previous_trade_date_yyyymmdd(date_yyyymmdd)

    meta: JSONDict = {
        "trade_date": date_yyyymmdd,
        "previous_trade_date": prev_trade_date,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "errors": [],
    }

    index_rows: list = []
    # Prefer Sina index spot (more stable). EM endpoint is flaky and may hang.
    try:
        df_idx = _retry_call(lambda: ak.stock_zh_index_spot_sina(), retries=1)
        index_rows = _format_index_rows(df_idx)
    except Exception as exc:
        meta["errors"].append(f"index_opening(sina): {type(exc).__name__}: {exc}")
        try:
            df_idx = _retry_call(
                lambda: ak.stock_zh_index_spot_em(symbol="沪深重要指数"), retries=0
            )
            index_rows = _format_index_rows(df_idx)
        except Exception as exc2:
            meta["errors"].append(f"index_opening(em): {type(exc2).__name__}: {exc2}")
            index_rows = []

    industries: list = []
    try:
        df_flow = _retry_call(
            lambda: ak.stock_fund_flow_industry(symbol="即时"), retries=1
        )
        if "净额" in df_flow.columns:
            df_flow = df_flow.sort_values("净额", ascending=False)
        industries = df_flow.head(top_n_industries).to_dict("records")
    except Exception as exc:
        meta["errors"].append(f"hot_industries_flow: {type(exc).__name__}: {exc}")
        industries = []

    limitups: list = []
    try:
        date_for_pool = prev_trade_date or date_yyyymmdd
        df_zt = _retry_call(
            lambda: ak.stock_zt_pool_previous_em(date=date_for_pool), retries=1
        )
        limitups = df_zt.head(top_n_limitups).to_dict("records")
    except Exception as exc:
        meta["errors"].append(f"previous_limit_up_stocks: {type(exc).__name__}: {exc}")
        try:
            df_zt = _retry_call(
                lambda: ak.stock_zt_pool_em(date=date_yyyymmdd), retries=1
            )
            limitups = df_zt.head(top_n_limitups).to_dict("records")
        except Exception as exc2:
            meta["errors"].append(f"limit_up_fallback: {type(exc2).__name__}: {exc2}")
            limitups = []

    lhb: list = []
    try:
        df_lhb = _retry_call(lambda: ak.stock_lhb_jgzz_sina(symbol="5"), retries=1)
        if "净额" in df_lhb.columns:
            df_lhb = df_lhb.sort_values("净额", ascending=False)
        lhb = df_lhb.head(top_n_lhb).to_dict("records")
    except Exception as exc:
        meta["errors"].append(f"institutional_LHB_buy: {type(exc).__name__}: {exc}")
        lhb = []

    breakfast: list = []
    try:
        df_bf = _retry_call(lambda: ak.stock_info_cjzc_em(), retries=1)
        breakfast = df_bf.head(top_n_breakfast).to_dict("records")
    except Exception as exc:
        meta["errors"].append(f"financial_breakfast: {type(exc).__name__}: {exc}")
        breakfast = []

    return {
        "index_opening": index_rows,
        "hot_industries_flow": industries,
        "previous_limit_up_stocks": limitups,
        "institutional_LHB_buy": lhb,
        "financial_breakfast": breakfast,
        "meta": meta,
    }


def _parse_yyyymmdd(value: Optional[str]) -> Optional[dt.date]:
    if not value:
        return None
    try:
        return dt.datetime.strptime(value, "%Y%m%d").date()
    except Exception:
        return None


def _previous_trade_date_yyyymmdd(date_yyyymmdd: str) -> Optional[str]:
    try:
        df = ak.tool_trade_date_hist_sina()
        dates = [str(d).replace("-", "") for d in df["trade_date"].astype(str).tolist()]
        candidates = [d for d in dates if d < date_yyyymmdd]
        return max(candidates) if candidates else None
    except Exception:
        return None


def _retry_call(fn, retries: int = 1, backoff_s: float = 0.6):
    last_exc = None
    for i in range(retries + 1):
        try:
            with _suppress_output():
                return fn()
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if i < retries:
                time.sleep(backoff_s * (2**i))
    if last_exc is not None:
        raise last_exc
    raise RuntimeError("retry_call failed")


@contextlib.contextmanager
def _suppress_output():
    """Suppress noisy library output (e.g., tqdm progress bars).

    Many agent runtimes capture stderr+stdout together; keep CLI stdout pure JSON.
    """

    with open(os.devnull, "w", encoding="utf-8") as devnull:
        with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
            yield


def _format_index_rows(df: Any) -> list:
    if df is None:
        return []
    if not hasattr(df, "columns"):
        return []

    want_order = [
        "上证指数",
        "深证成指",
        "创业板指",
        "沪深300",
        "上证50",
        "中证500",
        "中证1000",
        "科创50",
    ]

    cols = list(getattr(df, "columns", []))
    if "名称" in cols:
        try:
            df2 = df.copy()
            df2["名称"] = df2["名称"].astype(str)

            picked = []
            for name in want_order:
                sub_df = cast(pd.DataFrame, df2.loc[df2["名称"] == name])
                if not sub_df.empty:
                    picked.append(sub_df.iloc[0].to_dict())

            return picked if picked else df.head(8).to_dict("records")
        except Exception:
            return df.head(8).to_dict("records")

    # best-effort mapping for other schemas
    return df.head(8).to_dict("records")


def _rsi(series: Any, period: int = 14) -> Optional[float]:
    s = pd.to_numeric(cast(pd.Series, series), errors="coerce")
    delta = s.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    if cast(Any, loss).iloc[-1] == 0 or pd.isna(cast(Any, loss).iloc[-1]):
        return None
    rs = cast(Any, gain).iloc[-1] / cast(Any, loss).iloc[-1]
    return 100 - (100 / (1 + rs))


def _macd_hist(series: Any) -> float:
    s = pd.to_numeric(cast(pd.Series, series), errors="coerce")
    ema12 = s.ewm(span=12, adjust=False).mean()
    ema26 = s.ewm(span=26, adjust=False).mean()
    dif = ema12 - ema26
    dea = dif.ewm(span=9, adjust=False).mean()
    return cast(Any, (dif - dea)).iloc[-1]


def _kdj(df: Any) -> JSONDict:
    dff = cast(pd.DataFrame, df)
    low_min = cast(pd.Series, dff["l"]).rolling(window=9).min()
    high_max = cast(pd.Series, dff["h"]).rolling(window=9).max()
    close = pd.to_numeric(cast(pd.Series, dff["c"]), errors="coerce")
    rsv = (close - low_min) / (high_max - low_min) * 100
    k = rsv.ewm(com=2, adjust=False).mean()
    d = k.ewm(com=2, adjust=False).mean()
    j = 3 * k - 2 * d
    return {
        "k": cast(Any, k).iloc[-1],
        "d": cast(Any, d).iloc[-1],
        "j": cast(Any, j).iloc[-1],
    }


def _ta_from_hist(df: Optional[pd.DataFrame]) -> JSONDict:
    if df is None or df.empty:
        return {}
    close = pd.to_numeric(cast(pd.Series, df["收盘"]), errors="coerce").copy()
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rsi_val = (
        None
        if cast(Any, loss).iloc[-1] == 0 or pd.isna(cast(Any, loss).iloc[-1])
        else 100 - (100 / (1 + cast(Any, gain).iloc[-1] / cast(Any, loss).iloc[-1]))
    )
    boll_mean = close.rolling(window=20).mean()
    boll_std = close.rolling(window=20).std()
    bb_status = "中轨附近"
    if not pd.isna(cast(Any, boll_std).iloc[-1]):
        upper = cast(Any, boll_mean).iloc[-1] + 2 * cast(Any, boll_std).iloc[-1]
        lower = cast(Any, boll_mean).iloc[-1] - 2 * cast(Any, boll_std).iloc[-1]
        cur = cast(Any, close).iloc[-1]
        if cur > upper:
            bb_status = "上轨"
        elif cur < lower:
            bb_status = "下轨"
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    dif = ema12 - ema26
    dea = dif.ewm(span=9, adjust=False).mean()
    macd_hist = cast(Any, (dif - dea)).iloc[-1]
    volume_ratio = None
    if "成交量" in df.columns:
        vol = pd.to_numeric(cast(pd.Series, df["成交量"]), errors="coerce")
        avg5 = cast(Any, vol.rolling(window=5).mean()).iloc[-1]
        curv = cast(Any, vol).iloc[-1]
        volume_ratio = curv / avg5 if avg5 else None
    return {
        "rsi_14": rsi_val,
        "bollinger_bands": {"status": bb_status},
        "kdj": _kdj(pd.DataFrame({"h": df["最高"], "l": df["最低"], "c": df["收盘"]})),
        "macd": {
            "dif": cast(Any, dif).iloc[-1],
            "dea": cast(Any, dea).iloc[-1],
            "macd_hist": macd_hist,
        },
        "volume_ratio": volume_ratio,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch JSON for the skill")
    parser.add_argument(
        "--mode", choices=["crypto", "ashare", "morning", "news"], default="crypto"
    )
    parser.add_argument(
        "--symbol", default="BTC/USDT", help="crypto symbol, e.g., BTC/USDT"
    )
    parser.add_argument("--code", default="600519", help="A-share code, e.g., 600519")
    parser.add_argument("--date", help="target date YYYYMMDD (for morning)")
    parser.add_argument("--base", default="BTC", help="news base symbol, e.g., BTC")
    parser.add_argument("--kind", choices=["news", "media"], default="news")
    parser.add_argument("--limit", type=int, default=5, help="news items limit")
    args = parser.parse_args()

    if args.mode == "crypto":
        payload = fetch_crypto(args.symbol)
    elif args.mode == "ashare":
        payload = fetch_ashare(args.code)
    elif args.mode == "morning":
        payload = fetch_morning(date=args.date)
    else:
        token = os.getenv("CRYPTOPANIC_TOKEN")
        payload = (
            fetch_cryptopanic(token, args.base, kind=args.kind, limit=args.limit)
            if token
            else []
        )

    print(json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2))
