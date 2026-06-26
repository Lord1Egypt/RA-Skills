# pyright: reportMissingImports=false

import yfinance as yf

from utils import format_iso_date


def get_next_earnings_date(symbol: str) -> dict:
    """Fetch the next upcoming earnings date for a stock ticker from Yahoo Finance.

    Returns a dict with ticker, company_name, and next_earnings_date (ISO string),
    or an error key on failure.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info or {}
        company_name = info.get("longName") or info.get("shortName") or symbol

        calendar = ticker.calendar
        if calendar is None:
            return {
                "error": f"No calendar data available for {symbol}. "
                f"The ticker may not be supported or Yahoo Finance has no earnings data."
            }

        earnings_date_raw = calendar.get("Earnings Date")
        if not earnings_date_raw:
            return {
                "error": f"No upcoming earnings date found for {symbol} ({company_name}). "
                f"The company may not have a scheduled earnings call."
            }

        # 'Earnings Date' from yfinance is typically a list of upcoming dates
        if isinstance(earnings_date_raw, (list, tuple)):
            earnings_date_raw = earnings_date_raw[0]

        if earnings_date_raw is None:
            return {
                "error": f"No upcoming earnings date found for {symbol} ({company_name})."
            }

        next_date_str = format_iso_date(earnings_date_raw)

        return {
            "ticker": symbol.upper(),
            "company_name": company_name,
            "next_earnings_date": next_date_str,
        }

    except Exception as exc:
        return {"error": f"Could not fetch earnings data for {symbol}: {str(exc)}"}


def format_output(data: dict) -> str:
    """Format the earnings date result into human-readable output."""
    if "error" in data:
        return f"Error: {data['error']}"

    return (
        f"Ticker: {data['ticker']}\n"
        f"Company: {data['company_name']}\n"
        f"Next Earnings Date: {data['next_earnings_date']}"
    )
