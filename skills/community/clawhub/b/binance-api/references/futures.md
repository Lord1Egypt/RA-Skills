# Binance Futures Public Market Data — Endpoint Reference

Free, key-less market data for Binance derivatives:

- **USDⓈ-M futures** (settled in USDT/USDC, symbols like `BTCUSDT`):
  base URL `https://fapi.binance.com`, paths `/fapi/v1/*`
- **COIN-M futures** (settled in the coin, symbols like `BTCUSD_PERP`):
  base URL `https://dapi.binance.com`, paths `/dapi/v1/*`

Most endpoints exist on both; examples below use USDⓈ-M, with COIN-M
differences noted at the end. Same conventions as spot: `GET` requests, prices
as strings, timestamps in ms, errors as `{"code": ..., "msg": "..."}`.
Response examples were verified against the live API.

**Rate limit: 2,400 request weight per minute per IP** (less than half of
spot's 6,000) — watch the `x-mbx-used-weight-1m` response header.

One key-required exception: unlike spot, futures `/fapi/v1/historicalTrades`
returns 401 without an API key. Use `aggTrades` or `trades` instead.

## Contents

- [Prices and tickers](#prices-and-tickers)
- [Mark price and funding rate](#mark-price-and-funding-rate)
- [Open interest and sentiment](#open-interest-and-sentiment)
- [Klines (5 flavors)](#klines)
- [Order book and trades](#order-book-and-trades)
- [exchangeInfo](#exchange-information)
- [COIN-M differences](#coin-m-differences-dapibinancecom)

---

## Prices and tickers

### Latest price — `GET /fapi/v2/ticker/price` (weight 1; 2 without symbol)

Prefer v2 over v1 (higher precision timestamps, same shape).

```json
{"symbol": "BTCUSDT", "price": "63391.80", "time": 1783307788457}
```

Omit `symbol` for all ~500 USDⓈ-M symbols (array).

### Best bid/ask — `GET /fapi/v1/ticker/bookTicker` (weight 2; 5 without symbol)

```json
{
  "symbol": "BTCUSDT",
  "bidPrice": "63396.20", "bidQty": "0.482",
  "askPrice": "63396.30", "askQty": "16.595",
  "time": 1783307787783,
  "lastUpdateId": 10977561056660
}
```

### 24hr statistics — `GET /fapi/v1/ticker/24hr` (weight 1; 40 without symbol)

Same fields as spot's FULL ticker minus bid/ask/prevClose:

```json
{
  "symbol": "BTCUSDT",
  "priceChange": "642.10",
  "priceChangePercent": "1.023",
  "weightedAvgPrice": "63163.38",
  "lastPrice": "63385.10",
  "lastQty": "0.001",
  "openPrice": "62743.00",
  "highPrice": "63990.70",
  "lowPrice": "62410.10",
  "volume": "98084.543",
  "quoteVolume": "6195351476.72",
  "openTime": 1783221360000,
  "closeTime": 1783307783694,
  "firstId": 7868194208,
  "lastId": 7870504128,
  "count": 2304792
}
```

---

## Mark price and funding rate

### Current mark price + funding — `GET /fapi/v1/premiumIndex` (weight 1)

The one-call snapshot of a perpetual's state:

```json
{
  "symbol": "BTCUSDT",
  "markPrice": "63392.81973913",       // used for liquidations/PnL
  "indexPrice": "63415.27130435",      // basket of spot exchanges
  "estimatedSettlePrice": "63434.99268253",
  "lastFundingRate": "0.00009007",     // current period's funding rate
  "interestRate": "0.00010000",
  "nextFundingTime": 1783324800000,    // funding is exchanged every 8h
  "time": 1783307788007
}
```

Positive funding rate → longs pay shorts (bullish crowding); negative → shorts
pay longs. `0.0001` = 0.01% per 8h period.

### Funding rate history — `GET /fapi/v1/fundingRate` (weight 1)

| Name | Type | Mandatory | Description |
|---|---|---|---|
| `symbol` | STRING | NO | Omit for all symbols. |
| `startTime` / `endTime` | LONG | NO | ms. |
| `limit` | INT | NO | Default 100; max 1000. |

```json
[
  {
    "symbol": "BTCUSDT",
    "fundingTime": 1783296000000,
    "fundingRate": "0.00007700",
    "markPrice": "63625.51176812"
  }
]
```

---

## Open interest and sentiment

### Current open interest — `GET /fapi/v1/openInterest` (weight 1)

```json
{"symbol": "BTCUSDT", "openInterest": "104935.279", "time": 1783307783695}
```

Open interest is in contracts = base asset units for USDⓈ-M (here: BTC).

### Statistics endpoints — `GET /futures/data/*`

These live under `/futures/data/` (not `/fapi/v1/`) on `fapi.binance.com`.
Common parameters: `symbol` (required), `period` (required: `5m`, `15m`, `30m`,
`1h`, `2h`, `4h`, `6h`, `12h`, `1d`), `limit` (default 30, max 500),
`startTime`/`endTime`. **Only the most recent 1 month of data is available.**

| Path | Meaning | Sample row (verified) |
|---|---|---|
| `openInterestHist` | OI history (contracts + notional value) | `{"symbol":"BTCUSDT","sumOpenInterest":"104882.705","sumOpenInterestValue":"6653666199.09","timestamp":1783306800000}` |
| `globalLongShortAccountRatio` | All accounts: % long vs short | `{"longAccount":"0.5906","longShortRatio":"1.4426","shortAccount":"0.4094","timestamp":...}` |
| `topLongShortAccountRatio` | Top traders, by account | same shape |
| `topLongShortPositionRatio` | Top traders, by position size | same shape |
| `takerlongshortRatio` | Taker buy/sell volume ratio | `{"buySellRatio":"0.9544","buyVol":"2456.862","sellVol":"2574.252","timestamp":...}` |
| `basis` | Futures-spot basis | `pair` + `contractType` params instead of `symbol` |

---

## Klines

### `GET /fapi/v1/klines` (weight 1–10 by limit)

Same positional-array format and intervals as spot klines (`1m`…`1M`; no `1s`
on futures). Default limit 500, max 1500. Weight: ≤100 → 1, ≤500 → 2,
≤1000 → 5, >1000 → 10.

```json
[[1783296000000, "63617.20", "63900.00", "63308.30", "63385.20",
  "18287.752", 1783382399999, "1162507083.27340", 516386,
  "9527.179", "605691518.47920", "0"]]
```

Variants with the same parameters/format:

- `GET /fapi/v1/markPriceKlines` — mark price OHLC (volume fields are `"0"`)
- `GET /fapi/v1/indexPriceKlines` — index price OHLC; takes `pair=BTCUSDT`
  instead of `symbol`
- `GET /fapi/v1/premiumIndexKlines` — premium (futures vs index) OHLC
- `GET /fapi/v1/continuousKlines` — takes `pair` + `contractType`
  (`PERPETUAL`, `CURRENT_QUARTER`, `NEXT_QUARTER`); stitches contract rolls

---

## Order book and trades

### Depth — `GET /fapi/v1/depth`

`limit` must be one of 5, 10, 20, 50, 100 (default), 500, 1000. Weight: 2 for
≤50, 5 for 100, 10 for 500, 20 for 1000. Same `bids`/`asks` shape as spot,
plus message timestamps (`E`, `T`).

### Trades — `GET /fapi/v1/trades` (weight 5) and `GET /fapi/v1/aggTrades` (weight 20)

Same shapes as the spot equivalents. `historicalTrades` **requires an API
key on futures** — for key-free history, page `aggTrades` with
`startTime`/`endTime`/`fromId`.

---

## Exchange information

### `GET /fapi/v1/exchangeInfo` (weight 1)

No parameters; returns all ~800 contracts. Per-symbol fields worth reading:
`contractType` (`PERPETUAL`, `CURRENT_QUARTER`, ...), `status`,
`pricePrecision`, `quantityPrecision`, `filters`, and `onboardDate` (listing
time). The `rateLimits` array confirms the live 2,400/min weight budget.

---

## COIN-M differences (dapi.binance.com)

- Paths are `/dapi/v1/*`; statistics endpoints are under `/futures/data/*`
  with `pair` instead of `symbol`.
- Symbols: `BTCUSD_PERP` (perpetual), `BTCUSD_260327` (quarterly). The
  underlying `pair` is `BTCUSD`.
- **Single-`symbol` queries still return arrays** for `premiumIndex`,
  `ticker/price`, etc. (verified) — don't assume an object like on fapi:

```json
// GET /dapi/v1/ticker/price?symbol=BTCUSD_PERP
[{"price": "63334.2", "ps": "BTCUSD", "symbol": "BTCUSD_PERP", "time": 1783307768735}]
```

- Contracts are inverse: each contract is a fixed USD notional ($100 for BTC,
  $10 for most alts); volume/openInterest are in contracts, not coins. Kline
  field 7 is **base-asset volume** and field 5 is contracts (reversed meaning
  vs USDⓈ-M) — check against a known value before trusting a sum.
- Rate limit is also 2,400 weight/min per IP.
