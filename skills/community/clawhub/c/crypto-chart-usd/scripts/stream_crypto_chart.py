"""
Bitquery Crypto Chart USD — Real-time streaming (1-second ticks)
================================================================
Subscribe to the Bitquery WebSocket API for a live multi-token, multi-chain crypto chart
feed with 1-second OHLC, volume (Base/Quote/USD), and USD pricing (OHLC, moving averages).
Supports: Arbitrum, Base, Matic, Ethereum, Solana, Binance Smart Chain, Tron, Optimism —
all tokens on these chains.

Usage:
    python scripts/stream_crypto_chart.py

    Streams 1-second ticks for all tokens until interrupted (Ctrl+C) or optional --timeout seconds.

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

CRYPTO_CHART_SUBSCRIPTION = gql("""
subscription CryptoChartUsd {
  Trading {
    Tokens(where: {Interval: {Time: {Duration: {eq: 1}}}}) {
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
      Supply {
        TotalSupply
        MarketCap
        FullyDilutedValuationUsd
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
        v = float(value)
        if v >= 1 or v == 0:
            return f"${v:,.2f}"
        return f"${v:,.6f}"
    except (ValueError, TypeError):
        return str(value)


def format_token_tick(t: dict) -> str:
    """Format one token from a subscription tick (1-second candle)."""
    token = t.get("Token", {})
    block = t.get("Block", {})
    volume = t.get("Volume", {})
    price = t.get("Price", {})
    ohlc = price.get("Ohlc", {})
    avg = price.get("Average", {})

    name = token.get("Name", "?")
    symbol = token.get("Symbol", "?")
    network = token.get("Network", "?")
    ts = block.get("Time", block.get("Date", "?"))
    quoted_usd = price.get("IsQuotedInUsd")

    lines = [
        f"{name} ({symbol}) — {network}  @ {ts}  (1s candle)"
        + ("  [USD]" if quoted_usd else ""),
        "",
        "OHLC:",
        f"  Open:  {_fmt_price(ohlc.get('Open'))}  High: {_fmt_price(ohlc.get('High'))}  Low: {_fmt_price(ohlc.get('Low'))}  Close: {_fmt_price(ohlc.get('Close'))}",
    ]
    if avg and any(avg.get(k) is not None for k in ("Mean", "SimpleMoving", "ExponentialMoving", "WeightedSimpleMoving")):
        lines.append("  Averages:")
        if avg.get("Mean") is not None:
            lines.append(f"    Mean:   {_fmt_price(avg.get('Mean'))}")
        if avg.get("SimpleMoving") is not None:
            lines.append(f"    SMA:    {_fmt_price(avg.get('SimpleMoving'))}")
        if avg.get("ExponentialMoving") is not None:
            lines.append(f"    EMA:    {_fmt_price(avg.get('ExponentialMoving'))}")
        if avg.get("WeightedSimpleMoving") is not None:
            lines.append(f"    WMA:    {_fmt_price(avg.get('WeightedSimpleMoving'))}")

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

    tick_count = 0

    async with Client(transport=transport) as session:
        print("Connected. Streaming crypto chart (1s ticks, multi-token). Ctrl+C to stop.\n")

        async def consume():
            nonlocal tick_count
            try:
                async for result in session.subscribe(CRYPTO_CHART_SUBSCRIPTION):
                    trading = (result or {}).get("Trading") or {}
                    tokens = trading.get("Tokens") or []
                    tick_count += 1
                    for t in tokens:
                        out = format_token_tick(t)
                        if out.strip():
                            print(out)
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
            print("Usage: python stream_crypto_chart.py [--timeout SECONDS]", file=sys.stderr)
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
