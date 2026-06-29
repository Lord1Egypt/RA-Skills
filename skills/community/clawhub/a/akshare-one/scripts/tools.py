from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_hist_data(
    symbol: str,
    interval: Optional[str] = "day",
    interval_multiplier: Optional[int] = 1.0,
    start_date: Optional[str] = "1970-01-01",
    end_date: Optional[str] = "2030-12-31",
    adjust: Optional[str] = "none",
    source: Optional[str] = "eastmoney",
    indicators_list: Optional[null] = None,
    recent_n: Optional[null] = 100.0
) -> Dict[str, Any]:
    """
    Get historical stock market data. 'eastmoney_direct' support all A,B,H shares
    
    Args:
        symbol: Stock symbol/ticker (e.g. '000001')
        interval: Time interval
        interval_multiplier: Interval multiplier
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        adjust: Adjustment type
        source: Data source
        indicators_list: Technical indicators to add
        recent_n: Number of most recent records to return
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol,
        "interval": interval,
        "interval_multiplier": interval_multiplier,
        "start_date": start_date,
        "end_date": end_date,
        "adjust": adjust,
        "source": source,
        "indicators_list": indicators_list,
        "recent_n": recent_n
    }
    
    return call_api("1777419077870595", "get_hist_data", arguments)

def get_realtime_data(
    symbol: Optional[null] = None,
    source: Optional[str] = "eastmoney_direct"
) -> Dict[str, Any]:
    """
    Get real-time stock market data. 'eastmoney_direct' support all A,B,H shares
    
    Args:
        symbol: Stock symbol/ticker (e.g. '000001')
        source: Data source
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol,
        "source": source
    }
    
    return call_api("1777419077870595", "get_realtime_data", arguments)

def get_news_data(
    symbol: str,
    recent_n: Optional[null] = 10.0
) -> Dict[str, Any]:
    """
    Get stock-related news data.
    
    Args:
        symbol: Stock symbol/ticker (e.g. '000001')
        recent_n: Number of most recent records to return
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol,
        "recent_n": recent_n
    }
    
    return call_api("1777419077870595", "get_news_data", arguments)

def get_balance_sheet(
    symbol: str,
    recent_n: Optional[null] = 10.0
) -> Dict[str, Any]:
    """
    Get company balance sheet data.
    
    Args:
        symbol: Stock symbol/ticker (e.g. '000001')
        recent_n: Number of most recent records to return
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol,
        "recent_n": recent_n
    }
    
    return call_api("1777419077870595", "get_balance_sheet", arguments)

def get_income_statement(
    symbol: str,
    recent_n: Optional[null] = 10.0
) -> Dict[str, Any]:
    """
    Get company income statement data.
    
    Args:
        symbol: Stock symbol/ticker (e.g. '000001')
        recent_n: Number of most recent records to return
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol,
        "recent_n": recent_n
    }
    
    return call_api("1777419077870595", "get_income_statement", arguments)

def get_cash_flow(
    symbol: str,
    source: Optional[str] = "sina",
    recent_n: Optional[null] = 10.0
) -> Dict[str, Any]:
    """
    Get company cash flow statement data.
    
    Args:
        symbol: Stock symbol/ticker (e.g. '000001')
        source: Data source
        recent_n: Number of most recent records to return
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol,
        "source": source,
        "recent_n": recent_n
    }
    
    return call_api("1777419077870595", "get_cash_flow", arguments)

def get_inner_trade_data(
    symbol: str
) -> Dict[str, Any]:
    """
    Get company insider trading data.
    
    Args:
        symbol: Stock symbol/ticker (e.g. '000001')
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol
    }
    
    return call_api("1777419077870595", "get_inner_trade_data", arguments)

def get_financial_metrics(
    symbol: str,
    recent_n: Optional[null] = 10.0
) -> Dict[str, Any]:
    """
    Get key financial metrics from the three major financial statements.
    
    Args:
        symbol: Stock symbol/ticker (e.g. '000001')
        recent_n: Number of most recent records to return
    
    Returns:
        null
    """
    arguments = {
        "symbol": symbol,
        "recent_n": recent_n
    }
    
    return call_api("1777419077870595", "get_financial_metrics", arguments)

def get_time_info(
) -> Dict[str, Any]:
    """
    Get current time with ISO format, timestamp, and the last trading day.
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419077870595", "get_time_info", arguments)

