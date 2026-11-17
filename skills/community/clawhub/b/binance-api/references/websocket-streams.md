# Binance WebSocket Market Streams

Free, key-less real-time market data push. Use WebSocket instead of REST
polling whenever data is needed continuously (live dashboards, bots,
monitoring) — one connection replaces thousands of weight-costing REST calls.

Base endpoints (spot):

- `wss://stream.binance.com:9443` (or `:443`)
- `wss://data-stream.binance.vision` — market-data-only mirror (like
  `data-api.binance.vision` for REST); no user-data streams.

Official reference: https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md

## Connecting

- **Raw stream** (one stream per connection): `/ws/<streamName>`
- **Combined streams**: `/stream?streams=<name1>/<name2>/<name3>` — events are
  wrapped as `{"stream": "<name>", "data": <payload>}`
- Stream names use **lowercase** symbols: `btcusdt@trade`, not `BTCUSDT@trade`.
- Timestamps are ms by default; add `?timeUnit=MICROSECOND` for μs.

Verified example (Node ≥ 22 has WebSocket built in — no dependency):

```javascript
const ws = new WebSocket(
  "wss://stream.binance.com:9443/stream?streams=btcusdt@kline_1m/ethusdt@bookTicker");
ws.onmessage = (e) => {
  const { stream, data } = JSON.parse(e.data);
  if (stream === "ethusdt@bookTicker") console.log("ETH bid", data.b, "ask", data.a);
  if (stream === "btcusdt@kline_1m") console.log("BTC 1m close", data.k.c, "final?", data.k.x);
};
```

Python equivalent needs a library (`pip install websockets`):

```python
import asyncio, json, websockets

async def main():
    url = "wss://stream.binance.com:9443/ws/btcusdt@miniTicker"
    async with websockets.connect(url) as ws:   # library auto-replies to pings
        async for msg in ws:
            print(json.loads(msg)["c"])         # latest close price

asyncio.run(main())
```

## Common streams

| Stream name | Pushes | Update speed |
|---|---|---|
| `<symbol>@trade` | Every raw trade | real-time |
| `<symbol>@aggTrade` | Aggregated trades | real-time |
| `<symbol>@kline_<interval>` | Candlestick updates (`1s`…`1M`, same as REST) | 1s–2s |
| `<symbol>@miniTicker` | 24h OHLCV mini-ticker | 1s |
| `<symbol>@ticker` | Full 24h ticker stats | 1s |
| `<symbol>@bookTicker` | Best bid/ask changes | real-time |
| `<symbol>@avgPrice` | 5-min average price | 1s |
| `<symbol>@depth<levels>` | Top 5/10/20 book levels snapshot | 1s (append `@100ms` for 100ms) |
| `<symbol>@depth` | Order book diff updates | 1s (or `@100ms`) |
| `!miniTicker@arr` | All symbols' mini-tickers (changed ones) | 1s |
| `!ticker@arr` | All symbols' full tickers (changed ones) | 1s |

Verified payload samples:

```json
// btcusdt@miniTicker — c=close, o/h/l, v=base volume, q=quote volume
{"e":"24hrMiniTicker","E":1783308140035,"s":"BTCUSDT","c":"63392.09000000",
 "o":"62761.99000000","h":"63999.00000000","l":"62436.59000000",
 "v":"9764.64604000","q":"616323621.21380810"}

// ethusdt@bookTicker — b/B=bid price/qty, a/A=ask price/qty
{"u":78453078117,"s":"ETHUSDT","b":"1779.44000000","B":"54.89420000",
 "a":"1779.45000000","A":"1.92140000"}
```

Kline events arrive continuously while the candle forms; `k.x` is `true` only
on the final update of a candle — filter on it to act once per closed bar.

## Subscribing on an open connection

Instead of encoding streams in the URL, send JSON control messages:

```json
{"method": "SUBSCRIBE", "params": ["btcusdt@aggTrade", "btcusdt@depth"], "id": 1}
{"method": "UNSUBSCRIBE", "params": ["btcusdt@depth"], "id": 2}
{"method": "LIST_SUBSCRIPTIONS", "id": 3}
```

The server acks with `{"result": null, "id": 1}`. Data events have no `id`.

## Connection rules and limits

- The server pings every 20s; **reply with a pong** or be disconnected within
  a minute (browser WebSocket, Node, and the Python `websockets` library all
  do this automatically).
- A connection lives at most **24 hours** — plan to reconnect.
- Max **5 incoming messages/sec** per connection (subscribes, pings, pongs),
  **1024 streams** per connection, **300 connection attempts per 5 min per IP**.
- A `{"e": "serverShutdown"}` event means reconnect now.

## Keeping a local order book

The `@depth` diff stream alone is not enough — you must seed from REST:
buffer diff events, `GET /api/v3/depth?symbol=...&limit=5000` for a snapshot,
drop buffered events with `u` ≤ snapshot's `lastUpdateId`, then apply the rest
and every following event in order (each event's `U`…`u` range must chain
without gaps; on a gap, resync from a new snapshot). Full procedure: "How to
manage a local order book correctly" in the official web-socket-streams.md.

## Futures WebSocket

Futures have separate hosts with the same protocol: USDⓈ-M at
`wss://fstream.binance.com`, COIN-M at `wss://dstream.binance.com`. Notable
futures-only streams: `<symbol>@markPrice` (mark price + funding rate, 3s or
`@1s`), plus the usual `aggTrade`, `kline_<interval>`, `bookTicker`,
`!markPrice@arr`.

Caveat from testing: some networks/regions that can reach the spot streams
fine can connect and subscribe to `fstream` yet receive no data events. If
futures streams stay silent, fall back to polling the REST equivalents
(`/fapi/v1/premiumIndex` etc. — see `futures.md`).
