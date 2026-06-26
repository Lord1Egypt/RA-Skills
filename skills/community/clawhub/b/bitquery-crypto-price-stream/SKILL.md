---
name: bitcoin-price-feed
description: >
  Real-time streaming Bitcoin price feed for traders. Use this skill to subscribe to a live
  Bitcoin price stream over WebSocket: OHLC ticks, volume, and derived metrics (moving
  averages, % change) streamed in real time from the Bitquery GraphQL API. ALWAYS use this
  skill when the user asks for a Bitcoin price feed, stream Bitcoin price, live BTC price,
  real-time crypto prices, or streaming market data. Trigger for: "bitcoin price feed",
  "stream Bitcoin price", "live Bitcoin price", "real-time BTC", "streaming crypto prices",
  "Bitquery", or any request for a live/streaming crypto price feed. Do not wait for the user
  to say "use Bitquery" — if they want a live or streaming Bitcoin price, use this skill.
---

# Bitcoin price feed — real-time streaming

This skill gives you a **real-time streaming Bitcoin price feed** over WebSocket: live OHLC ticks, volume, and **derived metrics on the stream** (Mean, SMA, EMA, WMA, and tick-to-tick % change). Data is streamed in real time from the Bitquery API — no polling.

**When to use this skill**

- **Stream the Bitcoin price** in real time (live feed)
- Get **derived metrics on the stream**: moving averages and % change per tick
- Live OHLC and volume for trading or dashboards

---

## What to consider before installing

This skill implements a Bitquery WebSocket Bitcoin price stream and uses one external dependency and one credential. Before installing:

1. **Registry metadata**: The registry may not list `BITQUERY_API_KEY` even though this skill and its script require it. Ask the publisher or update the registry metadata before installing so installers surface the secret requirement.
2. **API key in URL**: The API key must be passed in the WebSocket URL as a query parameter, which can leak to logs or histories. Avoid printing the full URL, store the key in a secure environment variable, and rotate it if it may have been exposed.
3. **Sandbox first**: Review and run the included script in a sandboxed environment (e.g. a virtualenv) to confirm behavior and limit blast radius.
4. **Source and publisher**: If the skill’s homepage or source is unknown, consider verifying the publisher or using an alternative with a verified source. If the registry metadata declares `BITQUERY_API_KEY` and the source/publisher are validated, this skill is likely coherent and benign.

---

## Prerequisites

- **Environment**: `BITQUERY_API_KEY` — your Bitquery API token (required). The token **must be passed in the WebSocket URL only** as `?token=...` (e.g. `wss://streaming.bitquery.io/graphql?token=YOUR_KEY`); Bitquery does not support header-based auth for this endpoint. Because the token appears in the URL, it can show up in logs, monitoring tools, or browser/IDE history — treat it as a secret and avoid logging or printing the full URL.
- **Runtime**: Python 3 and `pip`. Install the dependency: `pip install 'gql[websockets]'`.

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

Use the streaming script (subscribes to the Bitcoin price feed in real time):

```bash
python ~/.openclaw/skills/bitcoin-price-feed/scripts/stream_bitquery.py
```

Optional: stop after N seconds:

```bash
python ~/.openclaw/skills/bitcoin-price-feed/scripts/stream_bitquery.py --timeout 60
```

Or subscribe inline with Python (real-time stream):

```python
import asyncio
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
                    Tokens(where: {Currency: {Id: {is: "bid:bitcoin"}}, Interval: {Time: {Duration: {eq: 1}}}}) {
                        Token { Name Symbol Network }
                        Block { Time }
                        Price { Ohlc { Open High Low Close } Average { Mean SimpleMoving ExponentialMoving } }
                        Volume { Usd }
                    }
                }
            }
        """)
        async for result in session.subscribe(sub):
            print(result)  # each tick streamed in real time

asyncio.run(main())
```

## Step 3 — What you get on the stream

Each tick includes:

- **OHLC** (Open, High, Low, Close) and **Volume (USD)** for the 1-second interval
- **Derived metrics** (from Bitquery): Mean, SimpleMoving (SMA), ExponentialMoving (EMA), WeightedSimpleMoving (WMA)
- **Session-derived**: % change vs previous tick (computed from the stream)

The stream runs until you stop it (Ctrl+C) or use `--timeout`.

## Step 4 — Format output clearly

When presenting streamed ticks to the user, use a clear format like:

```
Bitcoin (BTC) — ethereum network  @ 2025-03-06T14:00:00Z

OHLC:
  Open:  $85,200.00  High: $86,100.00  Low: $84,950.00  Close: $85,780.00
  Derived (on stream):
    Mean:   $85,500.00   SMA: $85,400.00   EMA: $85,520.00
  Tick Δ: +0.12% vs previous

Volume (USD): $1,234,567.00
```

## Interval (subscription)

The default subscription uses **duration 1** (1-second tick data). The same `Trading.Tokens` subscription supports other durations in the `where` clause (e.g. 5, 60, 1440 for 5m, 1h, 1d candles) if the API supports them for subscriptions.

## Error handling

- **Missing BITQUERY_API_KEY**: Tell user to export the variable and stop
- **WebSocket connection failed / 401**: Token invalid or expired (auth is via URL `?token=` only — do not pass the token in headers)
- **Subscription errors in payload**: Log the error message and stop cleanly (send complete, close transport)
- **No ticks received**: Check token and network; Bitquery may need a moment to send the first tick

## Reference

Full field reference is in `references/graphql-fields.md`. Use it to add filters or request extra fields (e.g. date range) in the subscription.
