#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "akshare>=1.0.0",
#     "pandas>=2.0.0",
#     "mplfinance>=0.12.0",
# ]
# ///
"""
Stock analysis for HK and A-share markets using akshare data.

Usage:
    uv run analyze.py TICKER [TICKER2 ...] [--output text|json] [--verbose]

Ticker format:
    5-digit → HK stock (e.g., 00700 for Tencent)
    6-digit → A-share  (e.g., 600519 for Moutai)
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Literal

import akshare as ak
import pandas as pd

# Add scripts dir to path for sibling imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indicators import (
    calc_rsi, calc_kdj, calc_adx, calc_obv, calc_mfi, calc_atr, calc_cci,
    calc_bb_bandwidth, calc_hist_volatility, calc_pivot_points, detect_candlestick,
)
from horizons import (
    HorizonSignal, MultiHorizonSignal,
    analyze_short_term, analyze_medium_term, analyze_long_term,
)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class StockData:
    ticker: str
    market: Literal["hk", "a"]
    name: str
    current_price: float
    price_history: pd.DataFrame  # columns: Date, Open, Close, High, Low, Volume
    financials: dict  # normalized key metrics
    analyst_forecasts: list[dict] | None  # HK only


# ---------------------------------------------------------------------------
# Market detection
# ---------------------------------------------------------------------------

def detect_market(ticker: str) -> Literal["hk", "a"]:
    t = ticker.strip()
    if len(t) == 5 and t.isdigit():
        return "hk"
    if len(t) == 6 and t.isdigit():
        return "a"
    raise ValueError(f"Unknown ticker format: {ticker}. Use 5-digit for HK (00700) or 6-digit for A-share (600519)")


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------

def fetch_hk_data(ticker: str, verbose: bool = False) -> StockData | None:
    try:
        if verbose:
            print(f"Fetching HK data for {ticker}...", file=sys.stderr)

        end = datetime.now().strftime("%Y%m%d")
        start = (datetime.now() - timedelta(days=730)).strftime("%Y%m%d")
        hist = ak.stock_hk_hist(symbol=ticker, period="daily", start_date=start, end_date=end, adjust="qfq")
        if hist.empty:
            return None

        hist = hist.rename(columns={
            "日期": "Date", "开盘": "Open", "收盘": "Close",
            "最高": "High", "最低": "Low", "成交量": "Volume", "换手率": "Turnover",
        })
        hist["Date"] = pd.to_datetime(hist["Date"])
        hist = hist.set_index("Date")
        current_price = float(hist["Close"].iloc[-1])

        # Financial indicators via fast valuation API (per-ticker, no full-market crawl)
        financials = {}
        try:
            for indicator, key in [("市盈率(TTM)", "pe"), ("市净率", "pb"), ("股息率(TTM)", "dividend_yield")]:
                df = ak.stock_hk_valuation_baidu(symbol=ticker, indicator=indicator, period="近一年")
                if df is not None and not df.empty and "value" in df.columns:
                    financials[key] = _safe_float(df["value"].iloc[-1])
        except Exception as e:
            if verbose:
                print(f"  Valuation data failed: {e}", file=sys.stderr)

        # ROE, net margin from stock_financial_hk_analysis_indicator_em (per-ticker, faster than financial_indicator_em)
        try:
            fin = ak.stock_financial_hk_analysis_indicator_em(symbol=ticker)
            if not fin.empty:
                row = fin.iloc[0]
                financials.update({
                    "roe": _safe_float(row.get("ROE_AVG")),
                    "net_margin": _safe_float(row.get("NET_PROFIT_RATIO")),
                    "profit_growth": _safe_float(row.get("HOLDER_PROFIT_YOY")),
                    "revenue_growth": _safe_float(row.get("OPERATE_INCOME_YOY")),
                })
        except Exception as e:
            if verbose:
                print(f"  Financial analysis indicators failed: {e}", file=sys.stderr)

        # Analyst forecasts (HK only)
        forecasts = None
        try:
            fc = ak.stock_hk_profit_forecast_et(symbol=ticker)
            if fc is not None and not fc.empty:
                forecasts = []
                for _, r in fc.head(10).iterrows():
                    forecasts.append({
                        "broker": str(r.get("证券商", "")),
                        "rating": str(r.get("评级", "")),
                        "target_price": _safe_float(r.get("目标价")),
                        "date": str(r.get("更新日期", "")),
                    })
        except Exception as e:
            if verbose:
                print(f"  Analyst forecasts failed: {e}", file=sys.stderr)

        # Get name from individual info (fast, per-ticker)
        name = ticker
        try:
            info = ak.stock_individual_basic_info_hk_xq(symbol=ticker)
            if info is not None and not info.empty:
                info_dict = dict(zip(info["item"], info["value"]))
                raw_name = str(info_dict.get("comcnname", ticker))
                # Clean up common suffixes
                for suffix in ["有限公司", "Limited", "Corporation", "Group", "Holdings", "Investment"]:
                    raw_name = raw_name.replace(suffix, "").replace(suffix.lower(), "")
                name = raw_name.strip()
        except Exception:
            pass

        return StockData(
            ticker=ticker, market="hk", name=name,
            current_price=current_price, price_history=hist,
            financials=financials, analyst_forecasts=forecasts,
        )
    except Exception as e:
        if verbose:
            print(f"Failed to fetch HK data for {ticker}: {e}", file=sys.stderr)
        return None


def fetch_a_data(ticker: str, verbose: bool = False) -> StockData | None:
    try:
        if verbose:
            print(f"Fetching A-share data for {ticker}...", file=sys.stderr)

        end = datetime.now().strftime("%Y%m%d")
        start = (datetime.now() - timedelta(days=730)).strftime("%Y%m%d")
        hist = ak.stock_zh_a_hist(symbol=ticker, period="daily", start_date=start, end_date=end, adjust="qfq")
        if hist.empty:
            return None

        hist = hist.rename(columns={
            "日期": "Date", "开盘": "Open", "收盘": "Close",
            "最高": "High", "最低": "Low", "成交量": "Volume", "换手率": "Turnover",
        })
        hist["Date"] = pd.to_datetime(hist["Date"])
        hist = hist.set_index("Date")
        current_price = float(hist["Close"].iloc[-1])

        # Financial indicators from individual info (fast, per-ticker)
        financials = {}
        name = ticker
        try:
            info = ak.stock_individual_info_em(symbol=ticker)
            if not info.empty:
                info_dict = dict(zip(info["item"], info["value"]))
                name = str(info_dict.get("股票简称", ticker))
                # P/E and P/B not in individual_info_em, get from realtime quote
        except Exception as e:
            if verbose:
                print(f"  Individual info failed: {e}", file=sys.stderr)

        # Detailed financials (fast, per-ticker, ~2s)
        try:
            fin = ak.stock_financial_abstract_ths(symbol=ticker, indicator="按年度")
            if not fin.empty:
                row = fin.iloc[-1]  # most recent year

                def parse_pct(v) -> float | None:
                    if v is None or v is False or (isinstance(v, float) and pd.isna(v)):
                        return None
                    s = str(v).replace("%", "").strip()
                    try:
                        return float(s)
                    except ValueError:
                        return None

                financials.update({
                    "net_margin": parse_pct(row.get("销售净利率")),
                    "gross_margin": parse_pct(row.get("销售毛利率")),
                    "roe": parse_pct(row.get("净资产收益率")),
                    "profit_growth": parse_pct(row.get("净利润同比增长率")),
                    "debt_ratio": parse_pct(row.get("资产负债率")),
                })
        except Exception as e:
            if verbose:
                print(f"  Financial abstract failed: {e}", file=sys.stderr)

        return StockData(
            ticker=ticker, market="a", name=name,
            current_price=current_price, price_history=hist,
            financials=financials, analyst_forecasts=None,
        )
    except Exception as e:
        if verbose:
            print(f"Failed to fetch A-share data for {ticker}: {e}", file=sys.stderr)
        return None


def fetch_data(ticker: str, verbose: bool = False) -> StockData | None:
    market = detect_market(ticker)
    if market == "hk":
        return fetch_hk_data(ticker, verbose)
    return fetch_a_data(ticker, verbose)


def _safe_float(val) -> float | None:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None



# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

_REC_LABEL = {"BUY": "买入 ▲", "HOLD": "持有 —", "SELL": "卖出 ▼"}


def format_text(signal: MultiHorizonSignal) -> str:
    market_label = "HK" if signal.market == "hk" else "A-Share"
    lines = [
        "=" * 77,
        f"STOCK ANALYSIS: {signal.ticker} ({signal.name}) [{market_label}]",
        f"Generated: {signal.timestamp}",
        "=" * 77,
        "",
    ]
    for hs in [signal.short, signal.medium, signal.long]:
        horizon_cn = {"short": "短期 (≤2周)", "medium": "中期 (2周~6月)", "long": "长期 (6月+)"}[hs.horizon]
        label = _REC_LABEL[hs.recommendation]
        lines.append(f"  {horizon_cn:16s}  {label}  (置信度 {hs.confidence:.0f}%)")
        for p in hs.points:
            lines.append(f"    · {p}")
        lines.append("")
    lines.append("=" * 77)
    lines.append("DISCLAIMER: NOT FINANCIAL ADVICE. For informational purposes only.")
    lines.append("=" * 77)
    return "\n".join(lines)


def format_json(signal: MultiHorizonSignal) -> str:
    d = asdict(signal)
    d["disclaimer"] = "NOT FINANCIAL ADVICE. For informational purposes only."
    return json.dumps(d, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def analyze_one(ticker: str, verbose: bool = False) -> tuple[MultiHorizonSignal, StockData] | None:
    data = fetch_data(ticker, verbose=verbose)
    if data is None:
        print(f"Error: Failed to fetch data for {ticker}", file=sys.stderr)
        return None

    short = analyze_short_term(data.current_price, data.price_history)
    medium = analyze_medium_term(data.current_price, data.price_history)
    long = analyze_long_term(data.current_price, data.price_history, data.financials, data.analyst_forecasts)

    if verbose:
        for hs in [short, medium, long]:
            print(f"  {hs.horizon}: {hs.recommendation} ({hs.score:+.2f}) — {'; '.join(hs.points)}", file=sys.stderr)

    signal = MultiHorizonSignal(
        ticker=data.ticker, name=data.name, market=data.market,
        short=short, medium=medium, long=long,
        timestamp=datetime.now().isoformat(),
    )
    return signal, data


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_charts(data: StockData, report_dir: str, verbose: bool = False) -> dict:
    """Generate chart_data.json for lightweight-charts rendering."""
    hist = data.price_history.copy()
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if col not in hist.columns:
            return {}

    # Use last 180 trading days
    hist = hist.iloc[-180:]
    close = hist["Close"]

    def _series(s):
        return [{"time": t.strftime("%Y-%m-%d"), "value": round(float(v), 4)}
                for t, v in s.items() if pd.notna(v)]

    def _ohlcv():
        rows = []
        for t, row in hist.iterrows():
            rows.append({
                "time": t.strftime("%Y-%m-%d"),
                "open": round(float(row["Open"]), 4),
                "high": round(float(row["High"]), 4),
                "low": round(float(row["Low"]), 4),
                "close": round(float(row["Close"]), 4),
                "volume": int(row["Volume"]),
            })
        return rows

    # Indicators
    ma20 = close.rolling(20).mean()
    std20 = close.rolling(20).std()
    ema50 = close.ewm(span=50, adjust=False).mean()
    ema200 = data.price_history["Close"].ewm(span=200, adjust=False).mean().iloc[-180:]

    delta = close.diff()
    gains = delta.where(delta > 0, 0).rolling(14).mean()
    losses = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rsi = 100 - (100 / (1 + gains / losses))

    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    sig = macd.ewm(span=9, adjust=False).mean()
    macd_hist = macd - sig

    low_9 = hist["Low"].rolling(9).min()
    high_9 = hist["High"].rolling(9).max()
    rsv = (close - low_9) / (high_9 - low_9 + 1e-9) * 100
    kdj_k = rsv.ewm(com=2, adjust=False).mean()
    kdj_d = kdj_k.ewm(com=2, adjust=False).mean()
    kdj_j = 3 * kdj_k - 2 * kdj_d

    chart_data = {
        "ohlcv": _ohlcv(),
        "ma20": _series(ma20),
        "bb_upper": _series(ma20 + 2 * std20),
        "bb_lower": _series(ma20 - 2 * std20),
        "ema50": _series(ema50),
        "ema200": _series(ema200),
        "rsi": _series(rsi),
        "macd": _series(macd),
        "macd_signal": _series(sig),
        "macd_hist": _series(macd_hist),
        "kdj_k": _series(kdj_k),
        "kdj_d": _series(kdj_d),
        "kdj_j": _series(kdj_j),
    }

    path = f"{report_dir}/chart_data.json"
    with open(path, "w") as f:
        json.dump(chart_data, f)

    if verbose:
        print(f"  Chart data saved: {path}", file=sys.stderr)
    return {"chart_data": "chart_data.json"}


def generate_report(signal: MultiHorizonSignal, data: StockData, verbose: bool = False) -> str:
    """Create report directory, generate charts, write data.json. Returns report dir path."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = f"/data/stock-reports/{signal.ticker}/{ts}"
    os.makedirs(report_dir, exist_ok=True)

    if verbose:
        print(f"Report dir: {report_dir}", file=sys.stderr)

    charts = generate_charts(data, report_dir, verbose=verbose)

    hist = data.price_history
    close = hist["Close"]

    ma5 = float(close.rolling(5).mean().iloc[-1]) if len(close) >= 5 else None
    ma20 = float(close.rolling(20).mean().iloc[-1]) if len(close) >= 20 else None
    ma60 = float(close.rolling(60).mean().iloc[-1]) if len(close) >= 60 else None
    ema50 = float(close.ewm(span=50, adjust=False).mean().iloc[-1]) if len(close) >= 50 else None
    ema200 = float(close.ewm(span=200, adjust=False).mean().iloc[-1]) if len(close) >= 200 else None
    high_52w = float(hist["High"].max())
    low_52w = float(hist["Low"].min())
    change_1m = float((close.iloc[-1] - close.iloc[-22]) / close.iloc[-22] * 100) if len(close) >= 22 else None
    change_3m = float((close.iloc[-1] - close.iloc[-66]) / close.iloc[-66] * 100) if len(close) >= 66 else None

    kdj = calc_kdj(hist)
    obv_result = calc_obv(hist)
    pattern = detect_candlestick(hist)

    report_data = {
        "ticker": signal.ticker,
        "name": signal.name,
        "market": signal.market,
        "generated_at": signal.timestamp,
        "current_price": data.current_price,
        "signal": {
            "short": asdict(signal.short),
            "medium": asdict(signal.medium),
            "long": asdict(signal.long),
        },
        "financials": data.financials,
        "technicals": {
            "ma5": ma5, "ma20": ma20, "ma60": ma60,
            "ema50": ema50, "ema200": ema200,
            "high_52w": high_52w, "low_52w": low_52w,
            "change_1m_pct": round(change_1m, 2) if change_1m else None,
            "change_3m_pct": round(change_3m, 2) if change_3m else None,
            "rsi_14": calc_rsi(close),
            "adx_14": calc_adx(hist),
            "kdj": {"k": kdj[0], "d": kdj[1], "j": kdj[2]} if kdj else None,
            "obv_trend": obv_result[1] if obv_result else None,
            "mfi_14": calc_mfi(hist),
            "cci_20": calc_cci(hist),
            "atr_14": calc_atr(hist),
            "bb_bandwidth": calc_bb_bandwidth(close),
            "hist_volatility_20": calc_hist_volatility(close),
            "pivot_points": calc_pivot_points(hist),
            "candlestick_pattern": pattern[0] if pattern else None,
        },
        "analyst_forecasts": data.analyst_forecasts,
        "charts": charts,
        "ai_analysis": None,
    }

    data_path = f"{report_dir}/data.json"
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2, default=str)

    print(f"Report saved: {report_dir}", file=sys.stderr)
    return report_dir


def main():
    parser = argparse.ArgumentParser(description="Analyze HK and A-share stocks using akshare")
    parser.add_argument("tickers", nargs="+", help="Stock tickers (5-digit HK, 6-digit A-share)")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--report", action="store_true", help="Generate report directory with charts and data.json")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    results = []
    for ticker in args.tickers:
        try:
            detect_market(ticker)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(2)

        result = analyze_one(ticker, verbose=args.verbose)
        if result:
            results.append(result)
        else:
            sys.exit(2)

    signals = [r[0] for r in results]

    if args.report:
        from render_report import render
        for signal, data in results:
            report_dir = generate_report(signal, data, verbose=args.verbose)
            render(report_dir)

    if args.output == "json":
        if len(signals) == 1:
            print(format_json(signals[0]))
        else:
            print(json.dumps([json.loads(format_json(s)) for s in signals], ensure_ascii=False, indent=2))
    else:
        for i, s in enumerate(signals):
            if i > 0:
                print()
            print(format_text(s))


if __name__ == "__main__":
    main()
