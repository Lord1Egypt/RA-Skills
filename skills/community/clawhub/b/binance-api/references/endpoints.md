# Binance Spot Public Market Data — Endpoint Reference

Base URL: `https://data-api.binance.vision` (or `https://api.binance.com`).
All endpoints are `GET`, security type `NONE` (no API key). Parameters go in
the query string. Prices/quantities are strings; timestamps are Unix
milliseconds. Response examples below were verified against the live API.

Source of truth: https://github.com/binance/binance-spot-api-docs (rest-api.md)

## Contents

- [General: ping, time, exchangeInfo, executionRules, referencePrice](#general-endpoints)
- [Order book: depth](#order-book)
- [Trades: trades, historicalTrades, aggTrades, historicalBlockTrades](#trades)
- [Klines: klines, uiKlines](#klines--candlestick-data)
- [Average price: avgPrice](#current-average-price)
- [Tickers: 24hr, tradingDay, price, bookTicker, rolling window](#tickers)
- [Rate limits](#rate-limits)
- [Error codes](#common-error-codes)

---

## General endpoints

### Test connectivity — `GET /api/v3/ping`

Weight: 1. No parameters. Returns `{}`.

### Server time — `GET /api/v3/time`

Weight: 1. No parameters.

```json
{"serverTime": 1783307169512}
```

### Exchange information — `GET /api/v3/exchangeInfo`

Weight: 20. Current trading rules and symbol metadata. All parameters optional:

| Name | Type | Description |
|---|---|---|
| `symbol` | STRING | One symbol, e.g. `BTCUSDT`. Invalid symbol → error `-1121`. |
| `symbols` | JSON array | e.g. `["BTCUSDT","BNBBTC"]` (URL-encode or use `curl -g`). |
| `permissions` | ENUM | e.g. `SPOT`. Cannot combine with `symbol`/`symbols`. |
| `symbolStatus` | ENUM | Filter by `TRADING`, `HALT`, or `BREAK`. Cannot combine with `symbol`/`symbols`. |

Response (heavily trimmed — the full unfiltered response covers ~3,000 symbols
and is large; filter by `symbol`/`symbols` whenever possible):

```json
{
  "timezone": "UTC",
  "serverTime": 1783307169512,
  "rateLimits": [
    {"rateLimitType": "REQUEST_WEIGHT", "interval": "MINUTE", "intervalNum": 1, "limit": 6000},
    {"rateLimitType": "ORDERS", "interval": "SECOND", "intervalNum": 10, "limit": 100},
    {"rateLimitType": "ORDERS", "interval": "DAY", "intervalNum": 1, "limit": 200000},
    {"rateLimitType": "RAW_REQUESTS", "interval": "MINUTE", "intervalNum": 5, "limit": 300000}
  ],
  "symbols": [
    {
      "symbol": "BTCUSDT",
      "status": "TRADING",
      "baseAsset": "BTC",
      "baseAssetPrecision": 8,
      "quoteAsset": "USDT",
      "quoteAssetPrecision": 8,
      "orderTypes": ["LIMIT", "LIMIT_MAKER", "MARKET", "STOP_LOSS", "..."],
      "isSpotTradingAllowed": true,
      "filters": [
        {"filterType": "PRICE_FILTER", "minPrice": "...", "maxPrice": "...", "tickSize": "..."},
        {"filterType": "LOT_SIZE", "minQty": "...", "maxQty": "...", "stepSize": "..."},
        {"filterType": "NOTIONAL", "...": "..."}
      ]
    }
  ]
}
```

Useful for: listing all tradable pairs, checking a symbol exists, reading
price/quantity precision (`tickSize`, `stepSize`) and min order size (`NOTIONAL`).

### Execution rules — `GET /api/v3/executionRules`

Weight: 2 with `symbol` (up to 40 otherwise). Niche: per-symbol matching-engine
rules such as price-range limits. **Only on `api.binance.com`** — not served by
`data-api.binance.vision` (404). Parameters: `symbol`, `symbols`, or
`symbolStatus` (no combinations).

```json
{"symbolRules": [{"symbol": "BTCUSDT", "rules": [{"ruleType": "PRICE_RANGE",
  "bidLimitMultUp": "1.1500", "bidLimitMultDown": "0.8500",
  "askLimitMultUp": "1.1500", "askLimitMultDown": "0.8500"}]}]}
```

### Reference price — `GET /api/v3/referencePrice`

Weight: 2. Parameter: `symbol` (required). **Only on `api.binance.com`** (404
on the data-api mirror). Returns `referencePrice: null` if none is set, or
error `-2043` if the symbol never had one. A companion
`GET /api/v3/referencePrice/calculation` describes how it's computed.

```json
{"symbol": "BTCUSDT", "referencePrice": "63397.52656780", "timestamp": 1783308104001}
```

---

## Order book

### `GET /api/v3/depth`

| Name | Type | Mandatory | Description |
|---|---|---|---|
| `symbol` | STRING | YES | |
| `limit` | INT | NO | Default 100; max 5000. |

Weight scales with `limit`: 1–100 → 5, 101–500 → 25, 501–1000 → 50,
1001–5000 → 250.

```json
{
  "lastUpdateId": 96996803668,
  "bids": [["63450.00000000", "1.17996000"], ["63449.99000000", "0.00088000"]],
  "asks": [["63450.01000000", "4.68879000"], ["63450.02000000", "0.00327000"]]
}
```

Each level is `[price, quantity]`. Bids are sorted best (highest) first, asks
best (lowest) first.

---

## Trades

### Recent trades — `GET /api/v3/trades`

Weight: 25.

| Name | Type | Mandatory | Description |
|---|---|---|---|
| `symbol` | STRING | YES | |
| `limit` | INT | NO | Default 500; max 1000. |

```json
[
  {
    "id": 6480413289,
    "price": "63433.99000000",
    "qty": "0.03292000",
    "quoteQty": "2088.24695080",
    "time": 1783307224775,
    "isBuyerMaker": false,
    "isBestMatch": true
  }
]
```

`isBuyerMaker: true` means the buyer was the passive side (i.e. the trade was a
sell into the bid — often read as "sell pressure").

### Old trade lookup — `GET /api/v3/historicalTrades`

Weight: 25. Same response shape as `/trades`. Extra parameter `fromId` (LONG) —
trade ID to fetch from; default returns the most recent trades. Data source is
the database, so it can page arbitrarily far back.

**Base URL caveat (verified):** this endpoint is **not served by
`data-api.binance.vision`** (plain nginx 404). Call it on
`https://api.binance.com` instead — it still needs no API key there.

### Block trades — `GET /api/v3/historicalBlockTrades`

Weight: 25. Privately negotiated large trades (rare; distinct from the regular
tape). Parameters: `symbol` (required), `fromId` (required — block trade ID to
fetch from), `limit` (default 500, max 1000). **Only on `api.binance.com`**
(404 on the data-api mirror). Rows look like `/trades` without `isBestMatch`.

### Aggregate trades — `GET /api/v3/aggTrades`

Weight: 4 — much cheaper than `/trades`. Trades from the same taker order at
the same price are merged into one row.

| Name | Type | Mandatory | Description |
|---|---|---|---|
| `symbol` | STRING | YES | |
| `fromId` | LONG | NO | Aggregate trade ID to fetch from (inclusive). |
| `startTime` / `endTime` | LONG | NO | ms timestamps (inclusive). |
| `limit` | INT | NO | Default 500; max 1000. |

```json
[
  {
    "a": 4006980383,        // aggregate trade ID
    "p": "63433.99000000",  // price
    "q": "0.03292000",      // quantity
    "f": 6480413289,        // first trade ID
    "l": 6480413289,        // last trade ID
    "T": 1783307224775,     // timestamp (ms)
    "m": false,             // was the buyer the maker?
    "M": true               // best price match (always true; ignore)
  }
]
```

To page a time range: request with `startTime`/`endTime`, then continue with
`fromId = last "a" + 1`.

---

## Klines / Candlestick data

### `GET /api/v3/klines`

Weight: 2. Klines are uniquely identified by open time.

| Name | Type | Mandatory | Description |
|---|---|---|---|
| `symbol` | STRING | YES | |
| `interval` | ENUM | YES | See table below. |
| `startTime` / `endTime` | LONG | NO | ms, always interpreted in UTC. Without them, returns the most recent klines. |
| `timeZone` | STRING | NO | Default `0` (UTC). e.g. `8`, `-1:00`, `05:45`; range [-12:00, +14:00]. Shifts the day/week/month bucketing only. |
| `limit` | INT | NO | Default 500; max 1000. |

Intervals (case-sensitive — `1m` is one minute, `1M` is one month):

| Unit | Values |
|---|---|
| seconds | `1s` |
| minutes | `1m`, `3m`, `5m`, `15m`, `30m` |
| hours | `1h`, `2h`, `4h`, `6h`, `8h`, `12h` |
| days | `1d`, `3d` |
| weeks | `1w` |
| months | `1M` |

Response — array of positional arrays:

```json
[
  [
    1783209600000,          // 0  open time (ms)
    "63144.01000000",       // 1  open
    "63999.00000000",       // 2  high
    "62436.59000000",       // 3  low
    "63650.00000000",       // 4  close
    "9172.07758000",        // 5  volume (base asset)
    1783295999999,          // 6  close time (ms)
    "577866444.60744400",   // 7  quote asset volume
    1790183,                // 8  number of trades
    "4565.93641000",        // 9  taker buy base asset volume
    "287772291.72139260",   // 10 taker buy quote asset volume
    "0"                     // 11 unused, ignore
  ]
]
```

The final kline is usually the current, still-forming candle (its close time is
in the future). Drop it when analyzing completed bars.

### UIKlines — `GET /api/v3/uiKlines`

Same parameters, weight, and response as `/klines`, but values are adjusted for
chart presentation (e.g. smoothing outlier prints). Use `/klines` for analysis;
`/uiKlines` only when replicating what Binance's own chart shows.

---

## Current average price

### `GET /api/v3/avgPrice`

Weight: 2. Parameter: `symbol` (required).

```json
{
  "mins": 5,                     // averaging window (minutes)
  "price": "63468.92471969",
  "closeTime": 1783307165880     // last trade time
}
```

---

## Tickers

### 24hr statistics — `GET /api/v3/ticker/24hr`

Rolling 24-hour window, recomputed continuously.

| Name | Type | Mandatory | Description |
|---|---|---|---|
| `symbol` | STRING | NO | Single symbol → returns one object. |
| `symbols` | JSON array | NO | e.g. `["BTCUSDT","ETHUSDT"]` → returns array. Cannot combine with `symbol`. |
| `type` | ENUM | NO | `FULL` (default) or `MINI`. |

**If both `symbol` and `symbols` are omitted, every symbol is returned** (array
of ~3,000 objects). Weight: 2 for one symbol; 2 for up to 20 `symbols`; 40 for
21–100; 80 for 101+ or omitted.

FULL response (single symbol):

```json
{
  "symbol": "BTCUSDT",
  "priceChange": "672.00000000",
  "priceChangePercent": "1.071",
  "weightedAvgPrice": "63117.87550688",
  "prevClosePrice": "62762.00000000",
  "lastPrice": "63433.99000000",
  "lastQty": "0.03292000",
  "bidPrice": "63433.98000000",
  "bidQty": "1.20000000",
  "askPrice": "63433.99000000",
  "askQty": "4.60000000",
  "openPrice": "62761.99000000",
  "highPrice": "63999.00000000",
  "lowPrice": "62436.59000000",
  "volume": "9764.64604000",
  "quoteVolume": "616323621.21380810",
  "openTime": 1783220825009,
  "closeTime": 1783307225009,
  "firstId": 6478459099,
  "lastId": 6480413289,
  "count": 1954191
}
```

MINI drops the bid/ask/prevClose/weightedAvg fields, keeping symbol + OHLC +
volume + times + trade count.

### Trading-day statistics — `GET /api/v3/ticker/tradingDay`

Stats for the current calendar trading day (00:00 in `timeZone`) rather than a
rolling window. Weight: 4 per symbol, capped at 200 for >50 symbols.

| Name | Type | Mandatory | Description |
|---|---|---|---|
| `symbol` / `symbols` | STRING | YES | One of the two required; max 100 symbols. |
| `timeZone` | STRING | NO | Default `0` (UTC). |
| `type` | ENUM | NO | `FULL` (default) or `MINI`. |

Response shape matches `ticker/24hr` FULL/MINI (minus `prevClosePrice`,
`lastQty`, bid/ask fields).

### Price ticker — `GET /api/v3/ticker/price`

Weight: 2 with `symbol`, 4 with `symbols` or when omitted (all symbols).

```json
{"symbol": "BTCUSDT", "price": "63450.01000000"}
```

With `symbols` (or omitted): an array of such objects. This is the cheapest
"what's the price" call.

### Book ticker — `GET /api/v3/ticker/bookTicker`

Best bid/ask. Weight: 2 with `symbol`, 4 with `symbols` or when omitted.

```json
{
  "symbol": "BTCUSDT",
  "bidPrice": "63450.00000000",
  "bidQty": "1.03510000",
  "askPrice": "63450.01000000",
  "askQty": "4.69848000"
}
```

### Rolling-window statistics — `GET /api/v3/ticker`

Like `ticker/24hr` but with a chosen window. Weight: 4 per symbol, capped at
200 for >50 symbols.

| Name | Type | Mandatory | Description |
|---|---|---|---|
| `symbol` / `symbols` | STRING | YES | One of the two required; max 100 symbols. |
| `windowSize` | ENUM | NO | Default `1d`. `1m`–`59m`, `1h`–`23h`, `1d`–`7d`. Units cannot be combined. |
| `type` | ENUM | NO | `FULL` (default) or `MINI`. |

The actual window opens on a whole minute, so it can be up to 59,999 ms wider
than requested — read `openTime`/`closeTime` in the response. Response shape
matches `ticker/24hr` (minus `prevClosePrice`, `lastQty`, bid/ask fields).

---

## Rate limits

- **6,000 request weight per minute per IP** (`REQUEST_WEIGHT` in
  `exchangeInfo.rateLimits`), plus a raw-request cap of 300,000 per 5 minutes.
  Limits are per IP, not per key.
- Every response carries `X-MBX-USED-WEIGHT-1M` (current usage). Check it when
  making many calls.
- HTTP **429**: limit exceeded — wait `Retry-After` seconds before retrying.
  Continuing to send after 429s triggers HTTP **418**: an automatic IP ban
  scaling from 2 minutes to 3 days (`Retry-After` gives the ban duration).
- HTTP **403**: blocked by the Web Application Firewall (e.g. SQL keywords in
  parameters). HTTP **451**/connection failures usually mean regional
  geo-restriction.

## Common error codes

Errors are `{"code": <negative int>, "msg": "..."}` with HTTP 4xx:

| Code | Meaning |
|---|---|
| -1121 | Invalid symbol (check spelling/pair exists — try `exchangeInfo`). |
| -1120 | Invalid interval (check kline interval spelling and case). |
| -1105 | A parameter was sent but empty. |
| -1102 | Mandatory parameter missing / malformed. |
| -1100 | Illegal characters in a parameter. |
| -1003 | Too many requests (rate limit / IP ban warning). |
| -1220 | Symbol doesn't match the requested `symbolStatus`. |

Full list: https://github.com/binance/binance-spot-api-docs/blob/master/errors.md
