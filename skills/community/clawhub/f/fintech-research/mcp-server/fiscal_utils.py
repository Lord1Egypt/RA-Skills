"""Fiscal calendar utilities."""
import json
import os
from datetime import datetime, timedelta

FISCAL_CALENDAR_PATH = os.path.join(os.path.dirname(__file__), "..", "docs", "fiscal_calendar.json")


def load_fiscal_calendar():
    """Load fiscal calendar from JSON."""
    try:
        with open(FISCAL_CALENDAR_PATH) as f:
            return json.load(f).get("fiscal_calendars", {})
    except Exception:
        return {}


def get_fiscal_year_end(ticker):
    """Return fiscal year end month-day string (e.g. '12-31')."""
    cal = load_fiscal_calendar()
    return cal.get(ticker, {}).get("fiscal_year_end", "12-31")


def get_quarter_end(ticker, fiscal_year, quarter):
    """Return quarter end date string (YYYY-MM-DD)."""
    fy_end = get_fiscal_year_end(ticker)
    month, day = map(int, fy_end.split("-"))
    # Calculate quarter end based on fiscal year end
    q_months = {
        1: (month - 9) % 12 or 12,
        2: (month - 6) % 12 or 12,
        3: (month - 3) % 12 or 12,
        4: month,
    }
    q_month = q_months.get(quarter, month)
    q_month = q_month if q_month > 0 else q_month + 12
    year = fiscal_year if q_month <= month else fiscal_year - 1
    from calendar import monthrange

    last_day = monthrange(year, q_month)[1]
    return f"{year}-{q_month:02d}-{last_day:02d}"


def get_next_earnings_estimate(ticker):
    """Estimate next earnings date based on fiscal calendar."""
    from datetime import date

    today = date.today()
    fy_end = get_fiscal_year_end(ticker)
    month, _ = map(int, fy_end.split("-"))
    current_q = ((today.month - month) % 12) // 3 + 1
    q_end = get_quarter_end(ticker, today.year, current_q)
    # Earnings typically 4-6 weeks after quarter end
    q_date = datetime.strptime(q_end, "%Y-%m-%d").date()
    est = q_date + timedelta(weeks=5)
    return est.strftime("%Y-%m-%d")


def fiscal_calendar_tool(action, ticker=None, fiscal_year=None, quarter=None):
    """MCP-facing fiscal calendar tool."""
    if action == "get_quarter_end":
        return {
            "ticker": ticker,
            "quarter_end_date": get_quarter_end(ticker, fiscal_year, quarter),
        }
    elif action == "get_fiscal_year_end":
        return {"ticker": ticker, "fiscal_year_end": get_fiscal_year_end(ticker)}
    elif action == "get_next_earnings":
        return {
            "ticker": ticker,
            "earnings_date_estimate": get_next_earnings_estimate(ticker),
        }
    return {"error": "Unknown action"}
