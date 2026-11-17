---
name: binance-api
description: Fetch live and historical cryptocurrency market data (prices, klines/candlesticks, order books, trades, 24h stats, futures funding rates, open interest) with the free Binance public REST API (no API key). Use for any crypto price lookup, BTC/ETH/altcoin quote, candlestick or OHLCV data, trading volume, order book, perpetual/futures data, or crypto market analysis task, even if Binance isn't mentioned.
---

# Binance Public Market Data API

Binance exposes its Spot market data through a free public REST API — **no API
key, no signup**. Every endpoint in this skill has security type `NONE` (public);
only account/trading endpoints need keys, and those are out of scope here.

Base URL: **`https://data-api.binance.vision`** — a market-data-only mirror of
`https://api.binance.com`. Prefer it for public data: same paths, same responses,
and it isolates you from the main exchange's stricter traffic policing.
(`api.binance.com` and `api1`–`api4.binance.com` also work if it's unavailable.)

Symbols are concatenated pairs in uppercase with no separator: `BTCUSDT`,
`ETHBTC`, `BNBUSDT`. When a user says "the price of Bitcoin", they almost always
mean `BTCUSDT` (quote in USDT ≈ USD).

## Quick reference

All are `GET` requests. Weight = rate-limit cost (budget: 6,000/min per IP).

| Task | Request | Weight |
|---|---|---|
| Latest price, one symbol | `/api/v3/ticker/price?symbol=BTCUSDT` | 2 |
| Latest price, several symbols | `/api/v3/ticker/price?symbols=["BTCUSDT","ETHUSDT"]` | 4 |
| Best bid/ask | `/api/v3/ticker/bookTicker?symbol=BTCUSDT` | 2 |
| 24h stats (change %, high/low, volume) | `/api/v3/ticker/24hr?symbol=BTCUSDT` | 2 |
| Candlesticks / OHLCV | `/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=100` | 2 |
| Order book depth | `/api/v3/depth?symbol=BTCUSDT&limit=100` | 5–250 |
| Recent trades | `/api/v3/trades?symbol=BTCUSDT&limit=100` | 25 |
| Aggregated trades (cheaper) | `/api/v3/aggTrades?symbol=BTCUSDT` | 4 |
| 5-min average price | `/api/v3/avgPrice?symbol=BTCUSDT` | 2 |
| Rolling-window stats (custom window) | `/api/v3/ticker?symbol=BTCUSDT&windowSize=4h` | 4/symbol |
| Trading-day stats | `/api/v3/ticker/tradingDay?symbol=BTCUSDT` | 4/symbol |
| List all symbols / trading rules | `/api/v3/exchangeInfo?symbol=BTCUSDT` | 20 |
| Server time / connectivity | `/api/v3/time`, `/api/v3/ping` | 1 |

Kline `interval` values (case-sensitive): `1s`, `1m`, `3m`, `5m`, `15m`, `30m`,
`1h`, `2h`, `4h`, `6h`, `8h`, `12h`, `1d`, `3d`, `1w`, `1M` (`1m` = minute,
`1M` = month).

## Response conventions

- **Prices and quantities are JSON strings**, not numbers (`"63450.01000000"`)
  — parse with `float()`/`Number()`, or `Decimal` when precision matters.
- **Timestamps are Unix milliseconds** (divide by 1000 for seconds).
- Errors return `{"code": -1121, "msg": "Invalid symbol."}` with an HTTP 4xx.

```json
// GET /api/v3/ticker/price?symbol=BTCUSDT
{"symbol": "BTCUSDT", "price": "63450.01000000"}
```

## Klines (candlesticks) — the workhorse

Each kline is a positional array; map it to named fields immediately:

```python
import requests

def get_klines(symbol: str, interval: str = "1d", limit: int = 100, **params):
    r = requests.get(
        "https://data-api.binance.vision/api/v3/klines",
        params={"symbol": symbol, "interval": interval, "limit": limit, **params},
        timeout=10,
    )
    r.raise_for_status()
    return [
        {
            "open_time": k[0],            # ms; kline's unique ID
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5]),        # in base asset (BTC for BTCUSDT)
            "close_time": k[6],
            "quote_volume": float(k[7]),  # in quote asset (USDT for BTCUSDT)
            "trades": k[8],
        }
        for k in r.json()
    ]
```

Max 1,000 klines per request. For longer history, page forward with `startTime`:

```python
def get_klines_range(symbol, interval, start_ms, end_ms):
    out = []
    while start_ms < end_ms:
        batch = get_klines(symbol, interval, limit=1000,
                           startTime=start_ms, endTime=end_ms)
        if not batch:
            break
        out.extend(batch)
        start_ms = batch[-1]["close_time"] + 1
    return out
```

The last kline in a response is usually the **still-open, unfinished candle**
(its `close_time` is in the future) — drop it for completed-bar analysis.

## Futures (derivatives) market data

Binance's futures markets have their own free, key-less market data APIs:
USDⓈ-M perpetuals/futures at `https://fapi.binance.com` (`/fapi/v1/*`, symbols
like `BTCUSDT`) and COIN-M at `https://dapi.binance.com` (`BTCUSD_PERP`).
Beyond the spot-style endpoints (klines, depth, tickers), they add
derivatives-only data:

| Task | Request |
|---|---|
| Mark price + current funding rate | `/fapi/v1/premiumIndex?symbol=BTCUSDT` |
| Funding rate history | `/fapi/v1/fundingRate?symbol=BTCUSDT` |
| Open interest (current) | `/fapi/v1/openInterest?symbol=BTCUSDT` |
| Open interest history, long/short ratios | `/futures/data/openInterestHist?symbol=BTCUSDT&period=1h` |

When a user asks about funding rates, open interest, liquidation-relevant mark
prices, long/short sentiment, or "the perp", read `references/futures.md` —
futures have a smaller rate budget (2,400 weight/min) and several format traps
(COIN-M returns arrays for single symbols; inverse-contract volume units).

## Rate limits

- Budget: **6,000 request weight per minute per IP** (not per key). Each
  response includes header `X-MBX-USED-WEIGHT-1M` with your current usage.
- HTTP **429** = over the limit; stop and wait the `Retry-After` header's
  seconds. Ignoring 429s escalates to HTTP **418** — an IP ban of 2 minutes
  up to 3 days.
- Normal usage never gets close: 6,000/min allows ~3,000 price checks. Only
  tight polling loops or all-symbols scans need care.

## Practical tips

- **Always pass `symbol` or `symbols`** to the ticker endpoints. Omitting it
  returns every symbol on the exchange (~3,000 entries, weight 80 for
  `ticker/24hr`). If you truly need a market-wide scan, one all-symbols call
  is still better than many single calls.
- Add `type=MINI` to `ticker/24hr`, `ticker/tradingDay`, or `ticker` to get
  just OHLC + volume without the bid/ask noise.
- `symbols` takes a JSON array in the query string — quote it in the shell:
  `curl -g 'https://data-api.binance.vision/api/v3/ticker/price?symbols=["BTCUSDT","ETHUSDT"]'`
- Not sure a symbol exists? `/api/v3/exchangeInfo?symbol=...` errors with
  `-1121` if it doesn't; without parameters it lists every tradable pair.
- One exception to the base URL: `/api/v3/historicalTrades` (old trade lookup)
  is missing from `data-api.binance.vision` (404) — call it on
  `api.binance.com`, still key-free.
- Binance is geo-restricted in a few jurisdictions (e.g. the US, where
  binance.us is a separate exchange/API). An HTTP 451 or connection block
  means regional restriction, not a bug in the request.
- For **bulk history** (years of klines/trades), don't loop over the REST API —
  Binance publishes free ZIP/CSV archives of complete history at
  `https://data.binance.vision`. Read `references/bulk-data.md` for the URL
  patterns and two CSV format traps (spot files: no header, microsecond
  timestamps).
- For **real-time data** (dashboards, bots, watching prices continuously),
  use the key-free WebSocket streams instead of polling REST — read
  `references/websocket-streams.md`. For occasional checks, REST is simpler.
- Account balances, placing orders, and trade history require a signed request
  with an API key (security types `USER_DATA`/`TRADE`) — not covered by this
  skill. If asked, point the user to the official docs:
  https://github.com/binance/binance-spot-api-docs

For complete references with all parameters, weights, and verified
request/response examples, read:

- `references/endpoints.md` — spot REST endpoints
- `references/futures.md` — USDⓈ-M and COIN-M futures REST (funding, open interest)
- `references/websocket-streams.md` — real-time WebSocket streams
- `references/bulk-data.md` — full-history ZIP/CSV archive for backtesting
