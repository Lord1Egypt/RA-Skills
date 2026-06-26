# /// script
# dependencies = ["rich", "httpx"]
# ///

"""
stock-quote: Real-time stock/ETF/crypto prices via Yahoo Finance.
Usage: uv run quote.py AAPL [MSFT GOOG ...] [--detail]
"""

import sys
import argparse
import httpx
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.text import Text

console = Console()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}


def fetch_quote(ticker: str) -> dict | None:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5d"
    try:
        r = httpx.get(url, headers=HEADERS, timeout=10, follow_redirects=True)
        r.raise_for_status()
        data = r.json()
        result = data.get("chart", {}).get("result")
        if not result:
            return None
        meta = result[0].get("meta", {})
        # Map meta fields to expected price/summary structure
        price = {
            "shortName": meta.get("shortName") or meta.get("instrumentType", ticker),
            "exchangeName": meta.get("exchangeName", ""),
            "regularMarketPrice": meta.get("regularMarketPrice"),
            "regularMarketPreviousClose": meta.get("previousClose") or meta.get("chartPreviousClose"),
            "regularMarketChange": (meta.get("regularMarketPrice", 0) or 0) - (meta.get("previousClose") or meta.get("chartPreviousClose") or meta.get("regularMarketPrice") or 0),
            "regularMarketChangePercent": 0,
            "regularMarketVolume": meta.get("regularMarketVolume"),
            "marketCap": meta.get("marketCap"),
            "marketState": meta.get("marketState", "CLOSED"),
        }
        prev = meta.get("previousClose") or meta.get("chartPreviousClose")
        cur = meta.get("regularMarketPrice")
        if prev and cur and prev != 0:
            price["regularMarketChange"] = cur - prev
            price["regularMarketChangePercent"] = (cur - prev) / prev
        summary = {
            "fiftyTwoWeekHigh": meta.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow": meta.get("fiftyTwoWeekLow"),
            "averageVolume": meta.get("averageVolume") or meta.get("regularMarketVolume"),
        }
        return {"price": price, "summary": summary}
    except httpx.HTTPStatusError:
        return None
    except Exception:
        return None


def fmt_number(val, prefix="$", suffix=""):
    if val is None:
        return "N/A"
    if val >= 1e12:
        return f"{prefix}{val/1e12:.2f}T{suffix}"
    if val >= 1e9:
        return f"{prefix}{val/1e9:.2f}B{suffix}"
    if val >= 1e6:
        return f"{prefix}{val/1e6:.2f}M{suffix}"
    if val >= 1e3:
        return f"{prefix}{val/1e3:.2f}K{suffix}"
    return f"{prefix}{val:.2f}{suffix}"


def fmt_price(val):
    if val is None:
        return "N/A"
    if val >= 1000:
        return f"${val:,.2f}"
    return f"${val:.2f}"


def get_raw(d, key):
    """Extract raw float from Yahoo Finance wrapped value."""
    v = d.get(key, {})
    if isinstance(v, dict):
        return v.get("raw")
    return v if isinstance(v, (int, float)) else None


def build_52w_bar(current, low, high, width=20):
    """Build a simple ASCII range bar."""
    if None in (current, low, high) or high == low:
        return "N/A"
    pct = max(0.0, min(1.0, (current - low) / (high - low)))
    pos = int(pct * width)
    bar = "─" * pos + "●" + "─" * (width - pos)
    return bar


def show_single(ticker: str, data: dict, detail: bool = False):
    p = data["price"]
    s = data["summary"]

    name = p.get("shortName") or p.get("longName") or ticker
    exchange = p.get("exchangeName", "")
    current = get_raw(p, "regularMarketPrice")
    prev_close = get_raw(p, "regularMarketPreviousClose")
    change = get_raw(p, "regularMarketChange")
    change_pct = get_raw(p, "regularMarketChangePercent")
    volume = get_raw(p, "regularMarketVolume")
    avg_volume = get_raw(s, "averageVolume")
    mkt_cap = get_raw(p, "marketCap")
    week52_high = get_raw(s, "fiftyTwoWeekHigh")
    week52_low = get_raw(s, "fiftyTwoWeekLow")
    market_state = p.get("marketState", "UNKNOWN")

    # Market state label
    if market_state == "REGULAR":
        state_label = "[green]● Market Open[/green]"
    elif market_state in ("PRE", "PREPRE"):
        state_label = "[yellow]● Pre-Market[/yellow]"
    elif market_state in ("POST", "POSTPOST"):
        state_label = "[cyan]● After-Hours[/cyan]"
    else:
        state_label = "[dim]● Market Closed[/dim]"

    # Price + change
    if change is not None and change >= 0:
        change_str = f"[green]▲ +{fmt_price(change)[1:]} (+{change_pct*100:.2f}%)[/green]"
    elif change is not None:
        change_str = f"[red]▼ {fmt_price(change)[1:]} ({change_pct*100:.2f}%)[/red]"
    else:
        change_str = "[dim]N/A[/dim]"

    price_str = fmt_price(current)
    header = f"[bold]{name} ({ticker})[/bold]  [dim]{exchange}[/dim]"
    price_line = f"[bold white]{price_str}[/bold white]  {change_str}  {state_label}"

    # 52W range bar
    bar = build_52w_bar(current, week52_low, week52_high)
    range_line = f"52W  {fmt_price(week52_low)} [dim]{bar}[/dim] {fmt_price(week52_high)}"

    vol_str = fmt_number(volume, prefix="")
    avg_vol_str = fmt_number(avg_volume, prefix="")
    vol_line = f"Volume  {vol_str}  [dim](avg {avg_vol_str})[/dim]"

    cap_line = f"Market Cap  {fmt_number(mkt_cap)}"

    body = Text.from_markup(
        f"{price_line}\n\n{range_line}\n{vol_line}\n{cap_line}"
    )

    console.print(Panel(body, title=Text.from_markup(header), expand=False))

    if detail and prev_close is not None:
        console.print(f"  [dim]Previous Close:[/dim] {fmt_price(prev_close)}")


def show_table(tickers: list[str], quotes: dict):
    table = Table(
        title="📈 Stock Quotes",
        box=box.ROUNDED,
        show_lines=False,
        header_style="bold white",
    )
    table.add_column("Ticker", style="bold cyan", no_wrap=True)
    table.add_column("Name", max_width=28)
    table.add_column("Price", justify="right")
    table.add_column("Change", justify="right")
    table.add_column("% Change", justify="right")
    table.add_column("Market Cap", justify="right")
    table.add_column("Status", justify="center")

    for t in tickers:
        data = quotes.get(t)
        if data is None:
            table.add_row(t, "[red]Not found[/red]", "-", "-", "-", "-", "-")
            continue
        p = data["price"]
        s = data["summary"]
        name = (p.get("shortName") or p.get("longName") or t)[:28]
        current = get_raw(p, "regularMarketPrice")
        change = get_raw(p, "regularMarketChange")
        change_pct = get_raw(p, "regularMarketChangePercent")
        mkt_cap = get_raw(p, "marketCap")
        market_state = p.get("marketState", "")

        color = "green" if (change or 0) >= 0 else "red"
        arrow = "▲" if (change or 0) >= 0 else "▼"

        price_cell = fmt_price(current)
        change_cell = f"[{color}]{arrow} {fmt_price(abs(change or 0))}[/{color}]"
        pct_cell = f"[{color}]{(change_pct or 0)*100:+.2f}%[/{color}]"
        cap_cell = fmt_number(mkt_cap)

        if market_state == "REGULAR":
            status = "[green]Open[/green]"
        elif market_state in ("PRE", "PREPRE"):
            status = "[yellow]Pre[/yellow]"
        elif market_state in ("POST", "POSTPOST"):
            status = "[cyan]AH[/cyan]"
        else:
            status = "[dim]Closed[/dim]"

        table.add_row(t, name, price_cell, change_cell, pct_cell, cap_cell, status)

    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="Real-time stock/ETF/crypto quotes")
    parser.add_argument("tickers", nargs="+", help="Ticker symbols (e.g. AAPL BTC-USD)")
    parser.add_argument("--detail", action="store_true", help="Show extra detail for single ticker")
    args = parser.parse_args()

    tickers = [t.upper() for t in args.tickers]

    if len(tickers) == 1:
        ticker = tickers[0]
        with console.status(f"Fetching {ticker}..."):
            data = fetch_quote(ticker)
        if data is None:
            console.print(f"[red]Ticker {ticker} not found or could not be fetched.[/red]")
            sys.exit(1)
        show_single(ticker, data, detail=args.detail)
    else:
        quotes = {}
        with console.status(f"Fetching {len(tickers)} quotes..."):
            for t in tickers:
                quotes[t] = fetch_quote(t)
        show_table(tickers, quotes)


if __name__ == "__main__":
    main()
