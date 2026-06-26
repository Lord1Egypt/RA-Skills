#!/usr/bin/env python3
"""
Fintech Research MCP Server
100% free, self-hosted. Consolidates institutional-grade data into a single local MCP.
Data: yfinance (HK+US), HKEX, FRED, NewsAPI, RSS, SEC EDGAR.
"""
import os
import sys
import json

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, DIR)

from data_cache import Cache
from data_sources import UnifiedDataSource
from hkex_scraper import search_disclosures
from fred_client import get_series as fred_get_series
from news_client import get_news
from sec_client import search_filings
from fiscal_utils import fiscal_calendar_tool

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("ERROR: mcp package not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

mcp = FastMCP("fintech-data")
cache = Cache(db_path=os.path.join(DIR, "cache.db"))
ds = UnifiedDataSource(cache)


@mcp.tool()
def run_sql(query: str, params: list = None) -> dict:
    """Execute read-only SQL against cached data. Max 20 rows returned."""
    import sqlite3

    try:
        conn = sqlite3.connect(os.path.join(DIR, "cache.db"))
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(query, params or [])
        rows = c.fetchmany(20)
        columns = [d[0] for d in c.description] if c.description else []
        result = [{k: r[k] for k in columns} for r in rows]
        return {"columns": columns, "rows": result, "row_count": len(result)}
    except Exception as e:
        return {"error": str(e), "mock": True, "rows": [], "row_count": 0}


@mcp.tool()
def get_ticker_info(ticker: str) -> dict:
    """Get company fundamentals for a ticker. Supports .HK for HK equities."""
    return ds.get_ticker_info(ticker)


@mcp.tool()
def get_price_history(ticker: str, period: str = "1y", interval: str = "1d") -> dict:
    """Get OHLCV price history. Max 100 rows for token efficiency."""
    return ds.get_price_history(ticker, period, interval)


@mcp.tool()
def get_sec_filings(ticker: str, form_types: list = None, limit: int = 5) -> dict:
    """Search SEC EDGAR filings. US equities only."""
    return search_filings(ticker, form_types, limit)


@mcp.tool()
def get_hkex_disclosures(
    stock_code: str, category: str = "announcements", since: str = None, limit: int = 5
) -> dict:
    """Search HKEX disclosure announcements. Free public access."""
    return search_disclosures(stock_code, category, since, limit)


@mcp.tool()
def get_macro_data(series_id: str, start_date: str = None) -> dict:
    """Get FRED macroeconomic data. Free official API."""
    return fred_get_series(series_id, start_date)


@mcp.tool()
def get_news_signals(query: str, source: str = "newsapi", limit: int = 5) -> dict:
    """Get news with sentiment analysis. Free tier."""
    return get_news(query, source, limit)


@mcp.tool()
def fiscal_calendar(
    action: str, ticker: str = None, fiscal_year: int = None, quarter: int = None
) -> dict:
    """Fiscal calendar utility."""
    return fiscal_calendar_tool(action, ticker, fiscal_year, quarter)


@mcp.tool()
def batch_ticker_info(tickers: list) -> dict:
    """Batch query up to 10 tickers. Token-optimized."""
    results = []
    for t in tickers[:10]:
        results.append(ds.get_ticker_info(t))
    return {"results": results, "count": len(results)}


@mcp.tool()
def get_ah_spread(h_ticker: str) -> dict:
    """Calculate A-H share premium/discount. Requires .HK ticker."""
    return ds.get_ah_spread(h_ticker)


if __name__ == "__main__":
    mcp.run(transport="stdio")
