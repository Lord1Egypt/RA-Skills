# pyright: reportMissingImports=false
from datetime import datetime, timedelta

import yfinance as yf

from constants import HISTORY_PERIOD, NEWS_FETCH_LIMIT, MAX_RELEVANT_NEWS, RANGE_WINDOWS
from utils import format_range, format_number, format_volume_summary


def get_price_range(history, days: int) -> dict:
    cutoff = datetime.now() - timedelta(days=days)
    filtered = history[history.index >= cutoff.strftime("%Y-%m-%d")]
    if filtered.empty:
        return {"high": None, "low": None}
    return {"high": float(filtered["High"].max()), "low": float(filtered["Low"].min())}


def filter_relevant_news(news_list: list, symbol: str) -> list:
    if not news_list:
        return []

    filtered = []
    for article in news_list:
        if not isinstance(article, dict):
            continue

        content = article.get("content", {})
        if not isinstance(content, dict):
            continue

        title = content.get("title", "")
        summary = content.get("summary", "")
        if symbol.replace('=','').upper() in (title + summary).upper():
            filtered.append(article)

        if len(filtered) >= MAX_RELEVANT_NEWS:
            break

    return filtered


def get_commodity_price(symbol: str) -> dict:
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info or {}

        current_price = info.get("currentPrice") or info.get("regularMarketPrice")
        previous_close = info.get("previousClose")
        change = (current_price - previous_close) if current_price is not None and previous_close is not None else None
        change_percent = ((change / previous_close) * 100) if change is not None and previous_close not in (None, 0) else None

        history = ticker.history(period=HISTORY_PERIOD)
        raw_news = ticker.news[:NEWS_FETCH_LIMIT] if ticker.news else []
        commodity_name = info.get("shortName") or info.get("longName") or symbol

        ranges = {window["key"]: get_price_range(history, window["days"]) for window in RANGE_WINDOWS}

        return {
            "symbol": symbol,
            "commodity_name": commodity_name,
            "price": current_price,
            "change": change,
            "change_percent": change_percent,
            "previous_close": previous_close,
            "volume": info.get("volume"),
            "avg_volume": info.get("averageVolume"),
            "day_high": info.get("dayHigh"),
            "day_low": info.get("dayLow"),
            "news": filter_relevant_news(raw_news, symbol),
            **ranges,
        }
    except Exception as exc:
        return {"error": f"Could not get commodity price for {symbol}: {str(exc)}"}


def format_recent_news(news: list) -> str:
    if not news:
        return "Recent News: No relevant news available"

    news_lines = ["Recent News:"]
    for index, article in enumerate(news[:MAX_RELEVANT_NEWS], 1):
        title = "No title"
        url = ""
        content = article.get("content", {})
        if isinstance(content, dict):
            title = content.get("title", "No title")
            click_url = content.get("clickThroughUrl", {})
            if isinstance(click_url, dict):
                url = click_url.get("url", "")

        news_lines.append(f"{index}. {title}")
        if url:
            news_lines.append(f"   Link: {url}")

    return "\n".join(news_lines)


def format_output(data: dict) -> str:
    if "error" in data:
        return f"Error: {data['error']}"

    price_str = f"${format_number(data['price'])}"
    if data['change'] is not None and data['change'] > 0:
        change_str = f"▲${format_number(data['change'])}"
    elif data['change'] is not None and data['change'] < 0:
        change_str = f"▼${format_number(abs(data['change']))}"
    else:
        change_str = "—"

    change_percent_str = (f"({format_number(data['change_percent'])}%)") if data['change_percent'] is not None else "(—)"
    prev_close_str = f"${format_number(data['previous_close'])}" if data['previous_close'] is not None else "N/A"
    day_high_str = f"${format_number(data.get('day_high'))}" if data.get('day_high') is not None else "N/A"
    day_low_str = f"${format_number(data.get('day_low'))}" if data.get('day_low') is not None else "N/A"

    range_blocks = "\n\n".join(format_range(window['label'], data[window['key']]) for window in RANGE_WINDOWS)

    return (
        f"{data['symbol']}: {data['commodity_name']}\n"
        f"{price_str} {change_str} {change_percent_str}, Prev Close: {prev_close_str}\n"
        f"{format_volume_summary(data.get('volume'), data.get('avg_volume'))}\n"
        f"\n"
        f"Today Low: {day_low_str}, High: {day_high_str}\n"
        f"\n"
        f"{range_blocks}\n"
        f"\n"
        f"{format_recent_news(data['news'])}"
    )
