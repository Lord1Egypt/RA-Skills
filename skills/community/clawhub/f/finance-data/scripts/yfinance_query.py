#!/usr/bin/env python3
"""Fetch stock data from Yahoo Finance via yfinance.

Usage:
    python yfinance_query.py <command> <ticker> [options]

Commands:
    quote       Current price, volume, market cap, P/E, etc.
    history     Historical OHLCV data
    financials  Income statement, balance sheet, cash flow
    info        Full company profile and key statistics
    holders     Institutional and insider holders
    analysts    Analyst recommendations and price targets
    dividends   Dividend history
    options     Options chain (calls and puts)
    earnings    Quarterly and annual earnings
    news        Recent news headlines
"""
import argparse
import json
import sys
from datetime import datetime

try:
    import yfinance as yf
except ImportError:
    print("Error: yfinance not installed. Run: pip install yfinance", file=sys.stderr)
    sys.exit(2)


def _df_to_json(df, orient="records", date_format="iso"):
    if df is None or (hasattr(df, "empty") and df.empty):
        return []
    return json.loads(df.to_json(orient=orient, date_format=date_format))


def _series_to_dict(s):
    if s is None:
        return {}
    if hasattr(s, "to_dict"):
        d = s.to_dict()
        return {str(k): _serialize(v) for k, v in d.items()}
    return {}


def _serialize(obj):
    if obj is None:
        return None
    if isinstance(obj, (int, float, bool, str)):
        if isinstance(obj, float) and (obj != obj):
            return None
        return obj
    if isinstance(obj, datetime):
        return obj.isoformat()
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    return str(obj)


def cmd_quote(ticker: yf.Ticker) -> dict:
    info = ticker.info or {}
    keys = [
        "symbol", "shortName", "longName", "currency", "exchange",
        "currentPrice", "previousClose", "open", "dayLow", "dayHigh",
        "regularMarketVolume", "averageVolume", "averageVolume10days",
        "marketCap", "fiftyTwoWeekLow", "fiftyTwoWeekHigh",
        "fiftyDayAverage", "twoHundredDayAverage",
        "trailingPE", "forwardPE", "priceToBook", "priceToSalesTrailing12Months",
        "trailingEps", "forwardEps", "pegRatio",
        "dividendYield", "dividendRate",
        "beta", "enterpriseValue", "enterpriseToRevenue", "enterpriseToEbitda",
        "profitMargins", "returnOnEquity", "returnOnAssets",
        "revenueGrowth", "earningsGrowth",
    ]
    return {k: _serialize(info.get(k)) for k in keys if info.get(k) is not None}


def cmd_history(ticker: yf.Ticker, period: str, interval: str) -> list:
    df = ticker.history(period=period, interval=interval)
    return _df_to_json(df.reset_index())


def cmd_financials(ticker: yf.Ticker, statement: str, quarterly: bool) -> dict:
    statements = {
        "income": (ticker.quarterly_income_stmt if quarterly else ticker.income_stmt),
        "balance": (ticker.quarterly_balance_sheet if quarterly else ticker.balance_sheet),
        "cashflow": (ticker.quarterly_cashflow if quarterly else ticker.cashflow),
    }
    if statement == "all":
        return {k: _df_to_json(v.T.reset_index()) for k, v in statements.items()}
    df = statements.get(statement)
    if df is None:
        return {"error": f"Unknown statement type: {statement}"}
    return _df_to_json(df.T.reset_index())


def cmd_info(ticker: yf.Ticker) -> dict:
    info = ticker.info or {}
    return {k: _serialize(v) for k, v in info.items()}


def cmd_holders(ticker: yf.Ticker) -> dict:
    result = {}
    try:
        inst = ticker.institutional_holders
        result["institutional"] = _df_to_json(inst)
    except Exception:
        result["institutional"] = []
    try:
        major = ticker.major_holders
        result["major"] = _df_to_json(major)
    except Exception:
        result["major"] = []
    try:
        insider = ticker.insider_transactions
        result["insider_transactions"] = _df_to_json(insider)
    except Exception:
        result["insider_transactions"] = []
    return result


def cmd_analysts(ticker: yf.Ticker) -> dict:
    result = {}
    try:
        recs = ticker.recommendations
        result["recommendations"] = _df_to_json(recs.reset_index()) if recs is not None else []
    except Exception:
        result["recommendations"] = []
    info = ticker.info or {}
    target_keys = [
        "targetHighPrice", "targetLowPrice", "targetMeanPrice",
        "targetMedianPrice", "numberOfAnalystOpinions", "recommendationKey",
        "recommendationMean",
    ]
    result["price_targets"] = {k: _serialize(info.get(k)) for k in target_keys if info.get(k) is not None}
    return result


def cmd_dividends(ticker: yf.Ticker) -> list:
    divs = ticker.dividends
    if divs is None or divs.empty:
        return []
    return _df_to_json(divs.reset_index())


def cmd_options(ticker: yf.Ticker, expiry: str) -> dict:
    try:
        dates = ticker.options
    except Exception:
        return {"error": "No options data available"}
    if not dates:
        return {"error": "No options expiration dates available"}
    if expiry and expiry in dates:
        chain = ticker.option_chain(expiry)
    elif expiry:
        return {"error": f"Expiry {expiry} not found. Available: {list(dates)}"}
    else:
        chain = ticker.option_chain(dates[0])
        expiry = dates[0]
    return {
        "expiry": expiry,
        "available_expiries": list(dates),
        "calls": _df_to_json(chain.calls),
        "puts": _df_to_json(chain.puts),
    }


def cmd_earnings(ticker: yf.Ticker) -> dict:
    result = {}
    try:
        eq = ticker.quarterly_earnings
        result["quarterly"] = _df_to_json(eq.reset_index()) if eq is not None else []
    except Exception:
        result["quarterly"] = []
    try:
        ea = ticker.earnings
        result["annual"] = _df_to_json(ea.reset_index()) if ea is not None else []
    except Exception:
        result["annual"] = []
    return result


def cmd_news(ticker: yf.Ticker) -> list:
    try:
        news = ticker.news
    except Exception:
        return []
    if not news:
        return []
    return [
        {
            "title": n.get("title"),
            "publisher": n.get("publisher"),
            "link": n.get("link"),
            "published": n.get("providerPublishTime"),
            "type": n.get("type"),
        }
        for n in news
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch stock data via yfinance.")
    ap.add_argument("command", choices=[
        "quote", "history", "financials", "info", "holders",
        "analysts", "dividends", "options", "earnings", "news",
    ])
    ap.add_argument("ticker", help="Stock ticker symbol (e.g. AAPL, MSFT, 600519.SS)")
    ap.add_argument("--period", default="1mo", help="History period: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max")
    ap.add_argument("--interval", default="1d", help="History interval: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo")
    ap.add_argument("--statement", default="all", choices=["all", "income", "balance", "cashflow"])
    ap.add_argument("--quarterly", action="store_true", help="Use quarterly data for financials/earnings")
    ap.add_argument("--expiry", default="", help="Options expiry date (YYYY-MM-DD)")
    args = ap.parse_args()

    ticker = yf.Ticker(args.ticker)
    handlers = {
        "quote": lambda: cmd_quote(ticker),
        "history": lambda: cmd_history(ticker, args.period, args.interval),
        "financials": lambda: cmd_financials(ticker, args.statement, args.quarterly),
        "info": lambda: cmd_info(ticker),
        "holders": lambda: cmd_holders(ticker),
        "analysts": lambda: cmd_analysts(ticker),
        "dividends": lambda: cmd_dividends(ticker),
        "options": lambda: cmd_options(ticker, args.expiry),
        "earnings": lambda: cmd_earnings(ticker),
        "news": lambda: cmd_news(ticker),
    }
    try:
        result = handlers[args.command]()
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
