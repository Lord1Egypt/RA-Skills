"""
Bitquery Bitcoin Price Feed — Real-time streaming
==================================================
Subscribe to the Bitquery WebSocket API for a live Bitcoin price feed with
OHLC, volume, and derived metrics (moving averages, % change) on the stream.

Usage:
    python scripts/stream_bitquery.py

    Streams Bitcoin ticks until interrupted (Ctrl+C) or optional --timeout seconds.

Environment:
    BITQUERY_API_KEY — Your Bitquery token (required). Passed as ?token= in WebSocket URL.
"""

import asyncio
import os
import sys
from urllib.parse import urlencode

from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport


BITQUERY_WS_BASE = "wss://streaming.bitquery.io/graphql"

BITCOIN_PRICE_SUBSCRIPTION = gql("""
subscription BitcoinPriceFeed {
  Trading {
    Tokens(
      where: { Currency: { Id: { is: "bid:bitcoin" } }, Interval: { Time: { Duration: { eq: 1 } } } }
    ) {
      Token {
        Address
        Id
        IsNative
        Name
        Network
        Symbol
        TokenId
      }
      Block {
        Date
        Time
        Timestamp
      }
      Interval {
        Time {
          Start
          Duration
          End
        }
      }
      Volume {
        Base
        Quote
        Usd
      }
      Price {
        IsQuotedInUsd
        Ohlc {
          Close
          High
          Low
          Open
        }
        Average {
          ExponentialMoving
          Mean
          SimpleMoving
          WeightedSimpleMoving
        }
      }
    }
  }
}
""")


def get_api_key() -> str:
    """Read the Bitquery API key from the environment. Raises if not set."""
    key = os.getenv("BITQUERY_API_KEY")
    if not key:
        raise EnvironmentError(
            "BITQUERY_API_KEY is not set. "
            "Please export your Bitquery token:\n"
            "  export BITQUERY_API_KEY=your_token_here"
        )
    return key


def _fmt_price(value) -> str:
    if value is None:
        return "N/A"
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return str(value)


def format_tick(data: dict, prev_close: float | None) -> str:
    """Format one subscription tick and compute derived metrics."""
    trading = (data or {}).get("Trading") or {}
    tokens = trading.get("Tokens") or []
    if not tokens:
        return ""

    t = tokens[0]
    token = t.get("Token", {})
    block = t.get("Block", {})
    volume = t.get("Volume", {})
    price = t.get("Price", {})
    ohlc = price.get("Ohlc", {})
    avg = price.get("Average", {})

    name = token.get("Name", "Bitcoin")
    symbol = token.get("Symbol", "BTC")
    network = token.get("Network", "?")
    ts = block.get("Time", block.get("Date", "?"))

    close = ohlc.get("Close")
    try:
        close_f = float(close) if close is not None else None
    except (ValueError, TypeError):
        close_f = None

    lines = [
        f"{name} ({symbol}) — {network}  @ {ts}",
        "",
        "OHLC:",
        f"  Open:  {_fmt_price(ohlc.get('Open'))}  High: {_fmt_price(ohlc.get('High'))}  Low: {_fmt_price(ohlc.get('Low'))}  Close: {_fmt_price(close)}",
    ]

    # Derived metrics from the stream (Bitquery-provided)
    if avg:
        lines.append("  Derived (on stream):")
        if avg.get("Mean") is not None:
            lines.append(f"    Mean:   {_fmt_price(avg.get('Mean'))}")
        if avg.get("SimpleMoving") is not None:
            lines.append(f"    SMA:    {_fmt_price(avg.get('SimpleMoving'))}")
        if avg.get("ExponentialMoving") is not None:
            lines.append(f"    EMA:    {_fmt_price(avg.get('ExponentialMoving'))}")
        if avg.get("WeightedSimpleMoving") is not None:
            lines.append(f"    WMA:    {_fmt_price(avg.get('WeightedSimpleMoving'))}")

    # Session-derived: % change from previous tick
    if prev_close is not None and close_f is not None and prev_close != 0:
        pct = ((close_f - prev_close) / prev_close) * 100
        lines.append(f"  Tick Δ: {pct:+.4f}% vs previous")

    vol_usd = volume.get("Usd")
    if vol_usd is not None:
        lines.append(f"\nVolume (USD): ${float(vol_usd):,.2f}")

    lines.append("")
    return "\n".join(lines)


async def run_stream(timeout_seconds: int | None = None) -> None:
    api_key = get_api_key()
    url = f"{BITQUERY_WS_BASE}?{urlencode({'token': api_key})}"
    transport = WebsocketsTransport(
        url=url,
        headers={"Sec-WebSocket-Protocol": "graphql-ws"},
    )

    prev_close: float | None = None
    tick_count = 0

    async with Client(transport=transport) as session:
        print("Connected. Streaming Bitcoin price feed (1s ticks). Ctrl+C to stop.\n")

        async def consume():
            nonlocal prev_close, tick_count
            try:
                async for result in session.subscribe(BITCOIN_PRICE_SUBSCRIPTION):
                    tick_count += 1
                    out = format_tick(result, prev_close)
                    if out:
                        print(out)
                        # Track close for next tick % change
                        trading = (result or {}).get("Trading") or {}
                        tokens = trading.get("Tokens") or []
                        if tokens:
                            close = (tokens[0].get("Price") or {}).get("Ohlc") or {}
                            c = close.get("Close")
                            if c is not None:
                                try:
                                    prev_close = float(c)
                                except (ValueError, TypeError):
                                    pass
            except asyncio.CancelledError:
                pass

        if timeout_seconds is not None:
            try:
                await asyncio.wait_for(consume(), timeout=float(timeout_seconds))
            except asyncio.TimeoutError:
                print(f"\nStopped after {timeout_seconds}s ({tick_count} ticks).")
        else:
            await consume()


def main() -> None:
    timeout: int | None = None
    if len(sys.argv) > 1 and sys.argv[1] == "--timeout" and len(sys.argv) > 2:
        try:
            timeout = int(sys.argv[2])
        except ValueError:
            print("Usage: python stream_bitquery.py [--timeout SECONDS]", file=sys.stderr)
            sys.exit(2)

    try:
        asyncio.run(run_stream(timeout_seconds=timeout))
    except EnvironmentError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStream stopped by user.")


if __name__ == "__main__":
    main()
