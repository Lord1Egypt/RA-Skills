---
name: crypto-chart-usd
description: >
  Real-time streaming crypto token feed for charting with 1-second OHLC ticks and USD pricing
  across Arbitrum, Base, Matic, Ethereum, Solana, Binance Smart Chain, Tron, and Optimism — all
  tokens on these chains. Subscribe to a live multi-token, multi-chain stream over WebSocket:
  OHLC, volume (Base/Quote/USD), and USD pricing (OHLC, moving averages) from the Bitquery
  Trading.Tokens API.
requires:
  env:
    - name: BITQUERY_API_KEY
      required: true
      description: Your Bitquery API token (required for WebSocket connection)
---

# Crypto charting with USD pricing (1s)

This skill gives you a **real-time streaming multi-token, multi-chain crypto feed** over WebSocket for charting: **1-second** OHLC ticks, volume (Base, Quote, USD), and USD pricing (OHLC, moving averages) for **all tokens** on the supported chains. Data is streamed in real time from the Bitquery Trading.Tokens API — no polling. Default interval is **1 second** (duration 1).

**Supported networks:** Arbitrum, Base, Matic (Polygon), Ethereum, Solana, Binance Smart Chain, Tron, Optimism. The subscription returns tokens across all of these; use the `Token.Network` field to filter or group by chain.

**When to use this skill**

- **Chart multiple tokens** across chains with 1-second OHLC and USD volume
- Get **USD pricing** where available (`Price.IsQuotedInUsd`); OHLC and averages in USD
- Live multi-token, multi-chain feed for dashboards and charting (no single-token or single-network filter)

---

## What to consider before installing

This skill implements a Bitquery WebSocket Trading.Tokens stream and uses one external dependency and one credential. Before installing:

1. **Required credential**: This skill requires `BITQUERY_API_KEY` (your Bitquery API token). The registry metadata **must** declare this credential so installers are prompted to provide it. Verify the registry entry lists `BITQUERY_API_KEY` as a required environment variable.

2. **⚠️ Critical security risk — Token in WebSocket URL**: Bitquery's API does **not** support header-based auth or any method other than embedding the token in the WebSocket URL as `?token=...`. This is an **inherent design limitation** of the API, not a bug in this skill. However, it creates a **significant leakage risk**:
   - The token will **always** be present in the connection URL in memory and in any logs or captured network traffic
   - If the URL is printed, logged, captured in shell history, IDE history, proxy logs, firewall logs, or monitoring systems, the token is **exposed**
   - Once exposed, anyone with the token can impersonate your account and consume your quota
   - **Mitigation**: Store the key **only** in a secure environment variable; never print or log the full URL; rotate the key **immediately** if you suspect exposure; run in a sandboxed environment (virtualenv/container) to limit logging surface

3. **Sandbox first**: Before using this skill in production or in shared environments, test it in an isolated environment (virtualenv, container, or dedicated machine) to confirm the logging behavior and ensure the URL is not captured by system monitoring or logging tools you have enabled.

4. **Source and publisher**: Verify the publisher's identity and source control access. Review the code in `scripts/stream_crypto_chart.py` to confirm the script does not log the full URL before use.

---

## Prerequisites

- **Environment**: `BITQUERY_API_KEY` — your Bitquery API token (required).

**⚠️ URL-only authentication (Bitquery API limitation):** Bitquery's streaming endpoint accepts the token **only in the WebSocket URL** as a query parameter (`?token=...`). It does **not** support header-based auth or Bearer tokens. This design choice means:
  - The token is embedded in the connection URL and will be present in memory, network traces, and any logs that capture the full URL
  - **Never print, log, or emit the full WebSocket URL in any context**
  - Always construct the URL from the environment variable and pass it only to the WebSocket transport
  - If the URL appears in shell history, logs, IDE debugger, or network monitoring, the token is compromised
  - **Rotate your API key immediately** if you suspect it was logged or captured
  - Run this script only in controlled environments where logging and monitoring are configured securely

- **Runtime**: Python 3.8+ and `pip`. Install the dependency: `pip install 'gql[websockets]'`.

---

## Security Checklist

**Before running this skill, confirm:**

- [ ] You have set `BITQUERY_API_KEY` in your environment: `export BITQUERY_API_KEY=your_token_here`
- [ ] You are running in a **sandboxed or isolated environment** (virtualenv, Docker, or dedicated machine)
- [ ] **Logging and shell history are disabled or monitored** to prevent URL capture: check `HISTFILE`, `.bash_history`, system logs, IDE debug output
- [ ] You understand that the WebSocket URL will contain your API token in plaintext in memory
- [ ] You have a plan to rotate your key if it is ever exposed
- [ ] You will **not** print, log, or commit the full URL to any file or logging system

If any of these cannot be confirmed, do not proceed with this skill until those conditions are met.

---

## Step 1 — Check API Key

```python
import os
api_key = os.getenv("BITQUERY_API_KEY")
if not api_key:
    print("ERROR: BITQUERY_API_KEY environment variable is not set.")
    print("Run: export BITQUERY_API_KEY=your_token")
    exit(1)
```

If the key is missing, tell the user and stop. Do not proceed without it.

## Step 2 — Run the stream

Install the WebSocket dependency once:

```bash
pip install 'gql[websockets]'
```

Use the streaming script (subscribes to the multi-token 1-second chart feed in real time):

```bash
python ~/.openclaw/skills/crypto-chart-usd/scripts/stream_crypto_chart.py
```

Optional: stop after N seconds:

```bash
python ~/.openclaw/skills/crypto-chart-usd/scripts/stream_crypto_chart.py --timeout 60
```

Or subscribe inline with Python (real-time stream, 1s ticks):

```python
import asyncio, os
from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport

async def main():
    token = os.environ["BITQUERY_API_KEY"]
    url = f"wss://streaming.bitquery.io/graphql?token={token}"
    transport = WebsocketsTransport(
        url=url,
        headers={"Sec-WebSocket-Protocol": "graphql-ws"},
    )
    async with Client(transport=transport) as session:
        sub = gql("""
            subscription {
              Trading {
                Tokens(where: { Interval: { Time: { Duration: { eq: 1 } } } }) {
                  Token { Address Id IsNative Name Network Symbol TokenId }
                  Block { Date Time Timestamp }
                  Interval { Time { Start Duration End } }
                  Volume { Base Quote Usd }
                  Price {
                    IsQuotedInUsd
                    Ohlc { Close High Low Open }
                    Average { ExponentialMoving Mean SimpleMoving WeightedSimpleMoving }
                  }
                }
              }
            }
        """)
        async for result in session.subscribe(sub):
            tokens = (result.get("Trading") or {}).get("Tokens") or []
            for t in tokens:
                ohlc = (t.get("Price") or {}).get("Ohlc") or {}
                vol = t.get("Volume") or {}
                print(
                    f"{t.get('Token', {}).get('Symbol', '?')} | "
                    f"Close: ${float(ohlc.get('Close') or 0):,.4f} | "
                    f"Vol USD: ${float(vol.get('Usd') or 0):,.2f}"
                )

asyncio.run(main())
```

## Step 3 — What you get on the stream

Each tick can contain **multiple tokens** from any of the supported chains (Arbitrum, Base, Matic, Ethereum, Solana, Binance Smart Chain, Tron, Optimism). For each token you get **1-second** OHLC and interval data:

- **Token**: Address, Id, IsNative, Name, Network, Symbol, TokenId
- **Block**: Date, Time, Timestamp
- **Interval**: Time.Start, Duration (1), End
- **Volume**: Base, Quote, Usd
- **Price**: IsQuotedInUsd, Ohlc (Open, High, Low, Close), Average (Mean, SimpleMoving, ExponentialMoving, WeightedSimpleMoving)

Not all tokens are quoted in USD; check `Price.IsQuotedInUsd` and use USD fields when true. The stream runs until you stop it (Ctrl+C) or use `--timeout`.

## Step 4 — Format output clearly

When presenting streamed ticks to the user, use a clear format like:

```
ETH (Ethereum) — ethereum  @ 2025-03-16T12:00:01Z  (1s candle)
OHLC:  Open: $3,450.00  High: $3,460.00  Low: $3,445.00  Close: $3,455.00
  Mean: $3,452.00  SMA: $3,451.00  EMA: $3,453.00
Volume (USD): $1,234,567.00
```

## Interval (subscription)

The default subscription uses **duration 1** (1-second tick/candle data). The same `Trading.Tokens` subscription supports other durations in the `where` clause (e.g. 5, 60, 1440 for 5m, 1h, 1d candles) if the API supports them for subscriptions.

## Error handling

- **Missing BITQUERY_API_KEY**: Tell user to export the variable and stop
- **WebSocket connection failed / 401**: Token invalid or expired (auth is via URL `?token=` only — do not pass the token in headers)
- **Subscription errors in payload**: Log the error message and stop cleanly (send complete, close transport)
- **No ticks received**: Check token and network; Bitquery may need a moment to send the first tick; multi-token stream can be bursty

## Supported networks

The feed includes tokens from: **Arbitrum**, **Base**, **Matic** (Polygon), **Ethereum**, **Solana**, **Binance Smart Chain**, **Tron**, **Optimism**. Filter by network in the subscription `where` clause (e.g. `Token: { Network: { is: "ethereum" } }`) or use `Token.Network` in your code to group or filter results. See `references/graphql-fields.md` for filter options.

## Reference

Full field reference is in `references/graphql-fields.md`. Use it to add filters (e.g. by Currency, Network) or request extra fields in the subscription.
