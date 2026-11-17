#!/usr/bin/env python3
"""Fetch Altair market breadth and factor indicators through the public MCP server.

Standard library only (Python 3.8+). No API key, no MCP client setup.

  python3 altair_market.py breadth                   # latest index and sector breadth
  python3 altair_market.py breadth --days 5          # also show recent trading sessions
  python3 altair_market.py indicators                # SPX NDX SOX, including TD Sequential 9
  python3 altair_market.py indicators NDX SOX         # selected indices
  python3 altair_market.py ticker NVDA                # one Yahoo Finance symbol

Set ALTAIR_MCP_URL to an HTTPS deployment; HTTP is allowed only for localhost/127.0.0.1.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ENDPOINT = os.environ.get("ALTAIR_MCP_URL", "https://altairworld.com/mcp/free")
INDICES = {"SPX": ("S&P 500", "all"), "NDX": ("Nasdaq-100", "nasdaq100"),
           "SOX": ("PHLX Semiconductor", "sox")}
ATTEMPTS = 3
DISCLAIMER = ("Market readings for information and AI testing only. They are not financial or investment "
              "advice and may contain errors; do not use them to make investment or trading decisions.")
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    # The endpoint sits behind Cloudflare, which rejects the default Python-urllib agent.
    "User-Agent": "altair-market-skill/1.0",
}


class ToolError(Exception):
    pass


class Transient(Exception):
    pass


def post(body):
    request = urllib.request.Request(ENDPOINT, data=body, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            text = response.read().decode("utf-8")
            streamed = "text/event-stream" in response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as error:
        if error.code in (429, 500, 502, 503, 504):
            raise Transient("HTTP {}".format(error.code))
        raise ToolError("{} returned HTTP {}".format(ENDPOINT, error.code))
    except (urllib.error.URLError, OSError) as error:
        raise Transient(str(getattr(error, "reason", error)))
    if streamed:
        events = [line[5:].strip() for line in text.splitlines() if line.startswith("data:")]
        if not events:
            raise Transient("empty event stream")
        text = events[-1]
    return json.loads(text)


def call_tool(name, arguments):
    body = json.dumps(
        {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": name, "arguments": arguments}}
    ).encode()
    # The server is a Cloudflare Worker that sometimes drops a request under load; reads are idempotent.
    for attempt in range(ATTEMPTS):
        try:
            message = post(body)
            break
        except Transient as error:
            if attempt == ATTEMPTS - 1:
                raise ToolError("{} failed after {} attempts: {}".format(name, ATTEMPTS, error))
            time.sleep(2 ** attempt)
    if not isinstance(message, dict):
        raise ToolError("invalid server response: expected a JSON object")
    if "error" in message:
        detail = message["error"]
        raise ToolError("{}: {}".format(name, detail.get("message", detail) if isinstance(detail, dict) else detail))
    result = message["result"]
    if not isinstance(result, dict):
        raise ToolError("invalid server response: expected a tool result object")
    if result.get("isError"):
        detail = " ".join(part.get("text", "") for part in result.get("content", []))
        raise ToolError(detail.strip() or "{}: tool error".format(name))
    if result.get("structuredContent") is not None:
        data = result["structuredContent"]
    else:
        data = json.loads(result["content"][0]["text"])
    if not isinstance(data, dict):
        raise ToolError("invalid server response: expected tool data object")
    if "error" in data:
        raise ToolError("{}: {}".format(name, data["error"]))
    return data


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def percent(value):
    return "n/a" if value is None else "{:g}%".format(value)


def number(value):
    return "n/a" if value is None else "{:,.2f}".format(value)


def breadth(args):
    data = call_tool("get_market_breadth", {"days": args.days or 1})
    latest = data["latest"]
    out = [
        "# Altair market breadth · reading date {}".format(latest["date"]), "",
        "Source: https://altairworld.com/indicators through the public MCP server {}. "
        "Values are from the last available close, not live quotes. "
        "Breadth is the percentage of eligible constituents above their {}-session SMA, not a stock count. "
        "SPX, NDX and SOX are price-only indices (no dividends).".format(ENDPOINT, data["movingAverage"]), "",
        "| Index | Above SMA{} | Price-index close |".format(data["movingAverage"]),
        "| --- | --- | --- |",
    ]
    for symbol, (name, key) in INDICES.items():
        out.append("| {} ({}) | {} | {} |".format(
            symbol, name, percent(latest[key]), number(latest["benchmarks"][symbol])))
    out.extend(["", "## S&P 500 sector breadth", "",
                "| Sector | Constituents | Above SMA{} |".format(data["movingAverage"]),
                "| --- | --- | --- |"])
    for sector in latest["sectors"]:
        out.append("| {} | {} | {} |".format(cell(sector["name"]), sector["stocks"], percent(sector["above"])))
    if args.days is not None:
        out.extend(["", "## Recent breadth ({} trading sessions returned)".format(len(data["history"])), "",
                    "| Session | S&P 500 | Nasdaq-100 | SOX |", "| --- | --- | --- | --- |"])
        for row in data["history"]:
            out.append("| {} | {} | {} | {} |".format(
                row["date"], percent(row["all"]), percent(row["nasdaq100"]), percent(row["sox"])))
        out.extend(["", "History uses the loader's constituent lists, not point-in-time membership."])
    out.extend(["", "Disclaimer: " + DISCLAIMER])
    print("\n".join(out))


def indicators(args):
    data = call_tool("get_market_indicators", {})
    selected = list(dict.fromkeys(args.indices or INDICES))
    by_symbol = {index["symbol"]: index for index in data["indices"]}
    missing = [symbol for symbol in selected if symbol not in by_symbol]
    if missing:
        raise ToolError("No indicator data for {}".format(", ".join(missing)))
    dates = sorted({by_symbol[symbol]["date"] for symbol in selected})
    out = [
        "# Altair market indicators · reading date {}".format(", ".join(dates)), "",
        "Source: https://altairworld.com/indicators through the public MCP server {}. "
        "Values are from the last available close, not live quotes; during trading hours the server "
        "can include the current session, so its close may not be final. "
        "SPX, NDX and SOX are price-only indices (no dividends). "
        "Bullish/neutral/bearish labels are rule readings, not forecasts or buy/sell instructions; "
        "several rules are contrarian. SOX implied volatility uses the semiconductor ETF index VXSMH.".format(ENDPOINT), "",
    ]
    for symbol in selected:
        index = by_symbol[symbol]
        out.extend(["## {} · reading date {} · {} · close {}".format(
            symbol, index["date"], cell(index["name"]), number(index["close"])), "",
            "| Indicator | Value | Reading | Signal |", "| --- | --- | --- | --- |"])
        out.extend(indicator_row(indicator, indicator["readings"].get(symbol)) for indicator in data["indicators"])
        out.append("")
    out.extend(rules_table(data["indicators"]))
    out.extend(["", "Disclaimer: " + DISCLAIMER])
    print("\n".join(out))


def indicator_row(indicator, reading):
    """One table row; a missing reading is unavailable, never zero."""
    if reading is None:
        return "| {} | n/a | unavailable | n/a |".format(cell(indicator["name"]))
    value = "{:.2%}".format(reading["value"]) if indicator["unit"] == "percent" else "{:g}".format(reading["value"])
    return "| {} | {} | {} | {} |".format(cell(indicator["name"]), value, cell(reading["reading"]), cell(reading["signal"]))


def rules_table(indicators):
    out = ["## Rules and sources", "", "| Indicator | Rule | Source |", "| --- | --- | --- |"]
    for indicator in indicators:
        source = indicator["source"]
        citation = cell(source["label"])
        if source["url"]:
            citation = "[{}]({})".format(citation, source["url"])
        out.append("| {} | {} | {} |".format(cell(indicator["name"]), cell(indicator["rule"]), citation))
    return out


def session_count(value):
    try:
        days = int(value)
        if 1 <= days <= 252:
            return days
    except ValueError:
        pass
    raise argparse.ArgumentTypeError("expected 1–252 trading sessions, got {!r}".format(value))


def ticker_symbol(value):
    symbol = value.strip().upper()
    if not re.fullmatch(r"[A-Z0-9^][A-Z0-9.=^-]{0,19}", symbol):
        raise argparse.ArgumentTypeError("expected a Yahoo Finance symbol, such as NVDA or BRK-B")
    return symbol


def ticker(args):
    data = call_tool("get_ticker_indicators", {"ticker": args.symbol})
    instrument = data["instrument"]
    if instrument["symbol"] != args.symbol:
        raise ToolError("invalid server response: ticker does not match requested symbol")
    out = [
        "# Altair ticker indicators · {} · reading date {}".format(args.symbol, instrument["date"]), "",
        "{} · close {}".format(cell(instrument["name"]), number(instrument["close"])), "",
        "Source: https://altairworld.com/indicators through the public MCP server {}. "
        "Not live quotes; the latest session can still be open and its close may not be final. "
        "Labels describe rules, not forecasts or buy/sell instructions. Shared macro readings are "
        "market context, not measurements of this stock. Historical S&P 500/Nasdaq-100 evidence "
        "does not validate returns for this instrument.".format(ENDPOINT), "",
        "| Indicator | Value | Reading | Signal |", "| --- | --- | --- | --- |",
    ]
    out.extend(indicator_row(indicator, indicator["reading"]) for indicator in data["indicators"])
    out.append("")
    out.extend(rules_table(data["indicators"]))
    out.extend(["", "Server disclaimer: " + cell(data["disclaimer"]), "", "Disclaimer: " + DISCLAIMER])
    print("\n".join(out))


def index_symbol(value):
    symbol = value.upper()
    if symbol not in INDICES:
        raise argparse.ArgumentTypeError("expected SPX, NDX or SOX, got {!r}".format(value))
    return symbol


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    breadth_parser = commands.add_parser("breadth", help="latest index and S&P 500 sector breadth")
    breadth_parser.add_argument("--days", type=session_count, help="also show 1–252 recent trading sessions")
    breadth_parser.set_defaults(run=breadth)
    indicators_parser = commands.add_parser("indicators", help="factor indicators and daily/weekly TD Sequential 9")
    indicators_parser.add_argument("indices", nargs="*", type=index_symbol, metavar="INDEX",
                                   help="indices to display (default: SPX NDX SOX)")
    indicators_parser.set_defaults(run=indicators)
    ticker_parser = commands.add_parser("ticker", help="latest indicators for one stock, ETF or Yahoo Finance symbol")
    ticker_parser.add_argument("symbol", type=ticker_symbol, help="e.g. NVDA, BRK-B or 0700.HK")
    ticker_parser.set_defaults(run=ticker)
    args = parser.parse_args()
    try:
        endpoint = urllib.parse.urlsplit(ENDPOINT)
        valid_endpoint = bool(endpoint.hostname) and (
            endpoint.scheme == "https" or
            (endpoint.scheme == "http" and endpoint.hostname in ("localhost", "127.0.0.1"))
        )
    except ValueError:
        valid_endpoint = False
    if not valid_endpoint:
        print("altair_market: ALTAIR_MCP_URL must use HTTPS (HTTP only for localhost/127.0.0.1)", file=sys.stderr)
        sys.exit(2)
    try:
        args.run(args)
    except ToolError as error:
        sys.exit("altair_market: {}".format(error))
    except (ValueError, KeyError, IndexError, TypeError) as error:
        sys.exit("altair_market: invalid server response: {}".format(error))


if __name__ == "__main__":
    main()
