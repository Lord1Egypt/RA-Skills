# BitoPro API Endpoints Reference

> Base URL: `https://api.bitopro.com/v3`
> Trading pair format: lowercase with underscore, e.g. `btc_twd`, `eth_twd`, `usdt_twd`

---

## Public Endpoints (No Authentication Required)

---

### 1. GET `/tickers/{pair}`

Get real-time ticker data for one or all trading pairs.

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Path | `pair` | string | No | Trading pair (e.g. `btc_twd`). Omit to return all pairs. |

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `pair` | string | Trading pair |
| `lastPrice` | string | Latest trade price |
| `high24hr` | string | 24-hour high price |
| `low24hr` | string | 24-hour low price |
| `volume24hr` | string | 24-hour trading volume |
| `priceChange24hr` | string | 24-hour price change (%) |
| `isBuyer` | boolean | Whether the last trade was a buy |

**Example Response:**

```json
{
  "data": [
    {
      "pair": "btc_twd",
      "lastPrice": "2850000.00000000",
      "high24hr": "2890000.00000000",
      "low24hr": "2810000.00000000",
      "volume24hr": "156.78901234",
      "priceChange24hr": "1.42",
      "isBuyer": true
    }
  ]
}
```

---

### 2. GET `/order-book/{pair}`

Get the order book (bid/ask depth) for a trading pair.

| Location | Parameter | Type | Required | Default | Description |
|----------|-----------|------|----------|---------|-------------|
| Path | `pair` | string | Yes | — | Trading pair (e.g. `btc_twd`) |
| Query | `limit` | int | No | 5 | Number of depth levels: `1, 5, 10, 20, 30, 50` |
| Query | `scale` | int | No | 0 | Price aggregation precision (varies by pair) |

**Response Fields (asks / bids arrays):**

| Field | Type | Description |
|-------|------|-------------|
| `price` | string | Price level |
| `amount` | string | Quantity at this level |
| `count` | int | Number of orders at this price level |
| `total` | string | Cumulative quantity |

**Example Response:**

```json
{
  "asks": [
    { "price": "2851000", "amount": "0.12", "count": 3, "total": "0.12" }
  ],
  "bids": [
    { "price": "2849000", "amount": "0.08", "count": 1, "total": "0.08" }
  ]
}
```

---

### 3. GET `/trades/{pair}`

Get recent trade records for a trading pair.

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Path | `pair` | string | Yes | Trading pair (e.g. `btc_twd`) |

**Response Fields (data array):**

| Field | Type | Description |
|-------|------|-------------|
| `price` | string | Trade price |
| `amount` | string | Trade quantity |
| `isBuyer` | boolean | Whether the buyer was the maker |
| `timestamp` | integer | Unix timestamp (seconds) |

**Example Response:**

```json
{
  "data": [
    {
      "price": "2850000.00000000",
      "amount": "0.01200000",
      "isBuyer": false,
      "timestamp": 1696000000
    }
  ]
}
```

---

### 4. GET `/trading-history/{pair}`

Get OHLCV candlestick data.

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Path | `pair` | string | Yes | Trading pair (e.g. `btc_twd`) |
| Query | `resolution` | string | Yes | Candlestick interval: `1m, 5m, 15m, 30m, 1h, 3h, 4h, 6h, 12h, 1d, 1w, 1M` |
| Query | `from` | int64 | Yes | Start time (Unix timestamp in **seconds**) |
| Query | `to` | int64 | Yes | End time (Unix timestamp in **seconds**) |

> `1m` and `5m` resolutions only provide data for the last 365 days.

**Response Fields (data array):**

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | number | Unix timestamp (**milliseconds**) |
| `open` | string | Open price |
| `high` | string | High price |
| `low` | string | Low price |
| `close` | string | Close price |
| `volume` | string | Trading volume |

**Example Response:**

```json
{
  "data": [
    {
      "timestamp": 1551052800000,
      "open": "2840000",
      "high": "2855000",
      "low": "2835000",
      "close": "2850000",
      "volume": "12.34567890"
    }
  ]
}
```

---

### 5. GET `/provisioning/trading-pairs`

Get a list of all available trading pairs and their configuration.

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| (none) | — | — | — | No parameters |

**Response Fields (data array):**

| Field | Type | Description |
|-------|------|-------------|
| `pair` | string | Trading pair (e.g. `btc_twd`) |
| `base` | string | Base currency |
| `quote` | string | Quote currency |
| `basePrecision` | string | Base currency decimal precision |
| `quotePrecision` | string | Quote currency decimal precision |
| `minLimitBaseAmount` | string | Minimum order amount (base) |
| `maxLimitBaseAmount` | string | Maximum order amount (base) |
| `minMarketBuyQuoteAmount` | string | Minimum market buy amount (quote) |
| `orderOpenLimit` | string | Max number of open orders |
| `maintain` | boolean | Whether the pair is under maintenance |
| `amountPrecision` | string | Amount decimal precision |

**Example Response:**

```json
{
  "data": [
    {
      "pair": "btc_twd",
      "base": "btc",
      "quote": "twd",
      "basePrecision": "8",
      "quotePrecision": "3",
      "minLimitBaseAmount": "0.0001",
      "maxLimitBaseAmount": "1000",
      "minMarketBuyQuoteAmount": "3",
      "orderOpenLimit": "200",
      "maintain": false,
      "amountPrecision": "2"
    }
  ]
}
```

---

### 6. GET `/provisioning/currencies`

Get the list of currencies and their deposit/withdrawal info.

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| (none) | — | — | — | No parameters |

**Response Fields (data array):**

| Field | Type | Description |
|-------|------|-------------|
| `currency` | string | Currency name (e.g. `TWD`, `USDT (ETH-ERC20)`) |
| `withdrawFee` | string | Withdrawal fee |
| `minWithdraw` | string | Minimum withdrawal amount |
| `maxWithdraw` | string | Maximum withdrawal amount |
| `maxDailyWithdraw` | string | Daily withdrawal limit |
| `withdraw` | boolean | Whether withdrawal is enabled |
| `deposit` | boolean | Whether deposit is enabled |
| `depositConfirmation` | string | Required blockchain confirmations |

**Example Response:**

```json
{
  "data": [
    {
      "currency": "TWD",
      "withdrawFee": "15",
      "minWithdraw": "100",
      "maxWithdraw": "1000000",
      "maxDailyWithdraw": "2000000",
      "withdraw": true,
      "deposit": true,
      "depositConfirmation": "0"
    },
    {
      "currency": "USDT (ETH-ERC20)",
      "withdrawFee": "10",
      "minWithdraw": "10",
      "maxWithdraw": "300000",
      "maxDailyWithdraw": "500000",
      "withdraw": true,
      "deposit": true,
      "depositConfirmation": "64"
    }
  ]
}
```

---

### 7. GET `/provisioning/limitations-and-fees`

Get VIP trading fee rates, withdrawal fees, deposit confirmations, and TTCheck limitations.

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| (none) | — | — | — | No parameters |

**Response Sections:**

- `tradingFeeRate[]` — VIP tier fee rates with `rank`, `twdVolume`, `bitoAmount`, `makerFee`, `takerFee`, `makerBitoFee`, `takerBitoFee`, `gridBotMakerFee`, `gridBotTakerFee`
- `restrictionsOfWithdrawalFees[]` — per-currency withdrawal fees and limits with `currency`, `fee`, `minimumTradingAmount`, `maximumTradingAmount`, `dailyCumulativeMaximumAmount`, `protocol`, `twdWithdrawMonthly`
- `cryptocurrencyDepositFeeAndConfirmation[]` — deposit fees and confirmation counts
- `ttCheckFeesAndLimitationsLevel1[]` / `ttCheckFeesAndLimitationsLevel2[]` — TTCheck limits

---

### 8. GET `/price/otc/{currency}`

Get OTC buy and sell price for a currency in TWD.

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Path | `currency` | string | Yes | Currency (e.g. `btc`, `eth`) |

**Example Response:**

```json
{
  "currency": "btc",
  "buySwapQuotation": {
    "twd": {
      "pricingCurrency": "TWD",
      "exchangeRate": "1130752.513945"
    }
  },
  "sellSwapQuotation": {
    "twd": {
      "pricingCurrency": "TWD",
      "exchangeRate": "1107699.219"
    }
  }
}
```

---

## Private Endpoints (Authentication Required)

All private endpoints require authentication headers. See [authentication.md](./authentication.md) for details.

**Header rules summary:**
- GET: all three headers included
- POST/PUT: all three headers included
- DELETE: `X-BITOPRO-APIKEY` + `X-BITOPRO-PAYLOAD` + `X-BITOPRO-SIGNATURE`

---

### 9. GET `/accounts/balance`

Get account balances for all currencies.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| (none) | — | — | No path or query parameters |

**Payload:** `{ "identity": email, "nonce": timestamp_ms }`

**Response Fields (data array):**

| Field | Type | Description |
|-------|------|-------------|
| `currency` | string | Currency symbol (e.g. `btc`, `twd`) |
| `amount` | string | Total balance |
| `available` | string | Available balance |
| `stake` | string | Staked amount |
| `tradable` | boolean | Whether the currency is tradable |

**Example Response:**

```json
{
  "data": [
    { "currency": "twd", "amount": "100000", "available": "85000", "stake": "0", "tradable": true },
    { "currency": "btc", "amount": "0.5", "available": "0.3", "stake": "0.2", "tradable": true }
  ]
}
```

---

### 10. POST `/orders/{pair}`

Create a new order (limit / market / stop-limit).

**Rate Limit:** 1200 req / min / UID

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Path | `pair` | string | Yes | Trading pair (e.g. `btc_twd`) |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | string | Yes | `BUY` or `SELL` |
| `amount` | string | Yes | Order quantity. For market BUY, this is the quote currency amount (e.g. TWD). |
| `price` | string | Conditional | Required for `LIMIT` and `STOP_LIMIT`. Not required for `MARKET`. |
| `type` | string | Yes | `LIMIT`, `MARKET`, or `STOP_LIMIT` |
| `timestamp` | integer | Yes | Current timestamp in milliseconds |
| `stopPrice` | string | Conditional | Trigger price (only for `STOP_LIMIT`) |
| `condition` | string | Conditional | `>=` or `<=` (only for `STOP_LIMIT`) |
| `timeInForce` | string | No | `GTC` (default) or `POST_ONLY` |
| `clientId` | uint64 | No | Custom order ID (1–2147483647) |
| `percentage` | uint64 | No | Percentage of available balance to sell (1–100) |

**Payload:** `{ action, amount, price, type, timestamp, nonce }` (actual body + nonce, **no `identity`**)

**Example Request Body:**

```json
{
  "action": "BUY",
  "amount": "0.001",
  "price": "2800000",
  "type": "LIMIT",
  "timestamp": 1696000000000
}
```

**Example Response:**

```json
{
  "orderId": 1234567890,
  "action": "BUY",
  "amount": "0.001",
  "price": "2800000",
  "timestamp": 1696000000000,
  "timeInForce": "GTC"
}
```

---

### 11. DELETE `/orders/{pair}/{orderId}`

Cancel an existing order.

**Rate Limit:** 900 req / min / UID

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Path | `pair` | string | Yes | Trading pair (e.g. `btc_twd`) |
| Path | `orderId` | string | Yes | Order ID to cancel |

**Payload (used for signature computation, but NOT sent as header):** `{ "identity": email, "nonce": timestamp_ms }`

**Headers:** `X-BITOPRO-APIKEY` + `X-BITOPRO-PAYLOAD` + `X-BITOPRO-SIGNATURE`

**Example Response:**

```json
{
  "action": "BUY",
  "amount": "0.001",
  "orderId": "1234567890",
  "price": "2800000",
  "timestamp": 1696000000000
}
```

---

### 12. GET `/orders/open`

Get all open (unfilled or partially filled) orders.

**Rate Limit:** 5 req / sec / UID

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Query | `pair` | string | No | Filter by trading pair. Omit to return all pairs. |

**Payload:** `{ "identity": email, "nonce": timestamp_ms }`

**Response Fields (data array):**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Order ID |
| `pair` | string | Trading pair |
| `action` | string | `BUY` / `SELL` |
| `type` | string | `LIMIT` / `MARKET` / `STOP_LIMIT` |
| `price` | string | Order price |
| `originalAmount` | string | Original order quantity |
| `remainingAmount` | string | Unfilled quantity |
| `executedAmount` | string | Filled quantity |
| `avgExecutionPrice` | string | Average fill price |
| `status` | int | Order status code |
| `fee` | string | Fee amount |
| `feeSymbol` | string | Fee currency |
| `bitoFee` | string | BITO token fee |
| `timeInForce` | string | `GTC` / `POST_ONLY` |
| `createdTimestamp` | int64 | Creation time (ms) |
| `updatedTimestamp` | int64 | Last update time (ms) |

**Example Response:**

```json
{
  "data": [
    {
      "id": "1234567890",
      "pair": "btc_twd",
      "action": "BUY",
      "type": "LIMIT",
      "price": "2800000",
      "originalAmount": "0.001",
      "remainingAmount": "0.001",
      "executedAmount": "0",
      "avgExecutionPrice": "0",
      "status": 0,
      "fee": "0",
      "feeSymbol": "btc",
      "bitoFee": "0",
      "timeInForce": "GTC",
      "createdTimestamp": 1696000000000,
      "updatedTimestamp": 1696000000000
    }
  ]
}
```

---

### 13. GET `/orders/all/{pair}`

Get order history for a trading pair.

| Location | Parameter | Type | Required | Default | Description |
|----------|-----------|------|----------|---------|-------------|
| Path | `pair` | string | Yes | — | Trading pair (e.g. `btc_twd`) |
| Query | `startTimestamp` | int64 | No | 90 days ago | Start time (milliseconds) |
| Query | `endTimestamp` | int64 | No | Now | End time (milliseconds) |
| Query | `statusKind` | string | No | `ALL` | Filter: `OPEN`, `DONE`, `ALL` |
| Query | `status` | int32 | No | — | Specific status code |
| Query | `orderId` | string | No | — | Pagination cursor (returns orders with id <= this value) |
| Query | `limit` | int32 | No | 100 | Results per page (1–1000) |
| Query | `clientId` | int32 | No | — | Filter by custom client ID |

**Payload:** `{ "identity": email, "nonce": timestamp_ms }`

**Response:** Same fields as open orders (see above), ordered by creation time descending. Maximum query window is 90 days.

---

### 14. POST `/orders/batch`

Create up to 10 limit or market orders at a time.

**Rate Limit:** 90 req / min / IP & UID

**Payload:** The request body array + nonce (no `identity`).

**Request Body:** Array of order objects:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pair` | string | Yes | Trading pair (e.g. `btc_twd`) |
| `action` | string | Yes | `BUY` or `SELL` |
| `type` | string | Yes | `LIMIT` or `MARKET` |
| `amount` | string | Yes | Order quantity (for market buy: quote currency amount) |
| `price` | string | Yes | Order price |
| `timestamp` | int64 | Yes | Current timestamp (ms) |
| `timeInForce` | string | No | `GTC` (default) or `POST_ONLY` |
| `clientId` | uint64 | No | Custom order ID (1–2147483647) |

**Example Request:**

```json
[
  {
    "pair": "btc_twd",
    "action": "BUY",
    "type": "LIMIT",
    "price": "2800000",
    "amount": "0.001",
    "timestamp": 1696000000000,
    "clientId": 2147483647
  },
  {
    "pair": "eth_twd",
    "action": "SELL",
    "type": "MARKET",
    "amount": "0.1",
    "timestamp": 1696000000000
  }
]
```

**Example Response:**

```json
{
  "data": [
    {
      "orderId": 1234567890,
      "action": "BUY",
      "price": "2800000",
      "amount": "0.001",
      "timestamp": 1696000000000,
      "timeInForce": "GTC",
      "clientId": 2147483647
    },
    {
      "orderId": 3234567891,
      "action": "SELL",
      "amount": "0.1",
      "timestamp": 1696000000000,
      "timeInForce": "GTC"
    }
  ]
}
```

---

### 15. PUT `/orders`

Cancel multiple orders by given order IDs, grouped by pair.

**Rate Limit:** 2 req / sec / IP

**Payload:** The request body + nonce (no `identity`).

**Request Body:** JSON object keyed by pair, values are arrays of order ID strings.

**Example Request:**

```json
{
  "btc_usdt": ["12234566", "12234567"],
  "eth_usdt": ["44566712", "24552212"]
}
```

**Example Response:**

```json
{
  "data": {
    "btc_usdt": ["12234566", "12234567"],
    "eth_usdt": ["44566712", "24552212"]
  }
}
```

---

### 16. DELETE `/orders/all` or `/orders/{pair}`

Cancel all open orders. Use `/orders/all` to cancel all pairs, or `/orders/{pair}` to cancel a specific pair.

**Rate Limit:** 1 req / sec / IP & UID

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Path | `pair` | string | No | Trading pair. Omit (use `/orders/all`) to cancel all pairs. |

**Payload:** `{ "identity": email, "nonce": timestamp_ms }`

**Example Response:**

```json
{
  "data": {
    "btc_usdt": ["12234566", "12234567"],
    "eth_usdt": ["44566712", "24552212"]
  }
}
```

---

### 17. GET `/orders/{pair}/{orderId}`

Get detailed information for a single order by ID.

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Path | `pair` | string | Yes | Trading pair (e.g. `btc_twd`) |
| Path | `orderId` | string | Yes | Order ID |

**Payload:** `{ "identity": email, "nonce": timestamp_ms }`

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Order ID |
| `pair` | string | Trading pair |
| `price` | string | Order price |
| `avgExecutionPrice` | string | Average fill price |
| `action` | string | `BUY` / `SELL` |
| `type` | string | `LIMIT` / `MARKET` / `STOP_LIMIT` |
| `status` | int | Order status code |
| `originalAmount` | string | Original order quantity |
| `remainingAmount` | string | Unfilled quantity |
| `executedAmount` | string | Filled quantity |
| `fee` | string | Fee amount |
| `feeSymbol` | string | Fee currency |
| `bitoFee` | string | BITO token fee |
| `total` | string | Total value |
| `stopPrice` | string | Stop trigger price (STOP_LIMIT only) |
| `condition` | string | `>=` or `<=` (STOP_LIMIT only) |
| `timeInForce` | string | `GTC` / `POST_ONLY` |
| `createdTimestamp` | int64 | Creation time (ms) |
| `updatedTimestamp` | int64 | Last update time (ms) |

> History available only for the past 90 days.

**Example Response:**

```json
{
  "id": "1234567890",
  "pair": "btc_twd",
  "price": "2800000",
  "avgExecutionPrice": "2799500",
  "action": "BUY",
  "type": "LIMIT",
  "status": 2,
  "originalAmount": "0.001",
  "remainingAmount": "0",
  "executedAmount": "0.001",
  "fee": "0.000001",
  "feeSymbol": "btc",
  "bitoFee": "0",
  "total": "2799.5",
  "timeInForce": "GTC",
  "createdTimestamp": 1696000000000,
  "updatedTimestamp": 1696000100000
}
```

---

### 18. GET `/orders/trades/{pair}`

Get trade fill history for a trading pair (your executed trades).

| Location | Parameter | Type | Required | Default | Description |
|----------|-----------|------|----------|---------|-------------|
| Path | `pair` | string | Yes | — | Trading pair (e.g. `btc_twd`) |
| Query | `startTimestamp` | int64 | No | 90 days ago | Start time (ms) |
| Query | `endTimestamp` | int64 | No | Now | End time (ms) |
| Query | `orderId` | string | No | — | Filter by order ID |
| Query | `tradeId` | string | No | — | Pagination cursor (returns trades with ID <= this value) |
| Query | `limit` | int64 | No | 100 | Results per page (1–1000) |

**Payload:** `{ "identity": email, "nonce": timestamp_ms }`

**Response Fields (data array):**

| Field | Type | Description |
|-------|------|-------------|
| `tradeId` | string | Trade ID |
| `orderId` | string | Associated order ID |
| `price` | string | Execution price |
| `action` | string | `BUY` / `SELL` |
| `baseAmount` | string | Base currency amount |
| `quoteAmount` | string | Quote currency amount |
| `fee` | string | Fee amount |
| `feeSymbol` | string | Fee currency |
| `isTaker` | boolean | Whether this trade was a taker |
| `createdTimestamp` | int64 | Trade time (ms) |

**Example Response:**

```json
{
  "data": [
    {
      "tradeId": "3109362209",
      "orderId": "7977988235",
      "price": "2800000",
      "action": "BUY",
      "baseAmount": "0.001",
      "quoteAmount": "2800",
      "fee": "0.000001",
      "feeSymbol": "btc",
      "isTaker": true,
      "createdTimestamp": 1696000000000
    }
  ]
}
```

---

## Wallet Endpoints

---

### 19. GET `/wallet/depositHistory/{currency}`

Get deposit history for a specific currency.

| Location | Parameter | Type | Required | Default | Description |
|----------|-----------|------|----------|---------|-------------|
| Path | `currency` | string | Yes | — | Currency (e.g. `twd`, `btc`, `usdt`) |
| Query | `startTimestamp` | int64 | No | 90 days ago | Start time (ms) |
| Query | `endTimestamp` | int64 | No | Now | End time (ms) |
| Query | `limit` | int64 | No | 20 | Results per page (1–100) |
| Query | `id` | string | No | — | Pagination cursor |
| Query | `statuses` | string | No | — | Comma-separated status filter |
| Query | `txID` | string | No | — | Filter by transaction ID (crypto only, not for TWD) |

**Payload:** `{ "identity": email, "nonce": timestamp_ms }`

> Max query window: 90 days. `txID` is not unique and may return multiple records.

**Response Fields (data array):**

| Field | Type | Description |
|-------|------|-------------|
| `serial` | string | Deposit serial number |
| `timestamp` | string | Deposit time (ms) |
| `address` | string | Deposit address |
| `amount` | string | Deposit amount |
| `fee` | string | Fee |
| `total` | string | Total credited |
| `status` | string | Deposit status |
| `txid` | string | Blockchain transaction ID |
| `protocol` | string | Network protocol |
| `id` | string | Record ID |
| `message` | string | Attached message (may not be included) |

**Example Response:**

```json
{
  "data": [
    {
      "serial": "20210126BW05262128",
      "timestamp": "1611660419000",
      "address": "0x1234...abcd",
      "amount": "1000",
      "fee": "0",
      "total": "1000",
      "status": "COMPLETE",
      "txid": "00d618f6ecb5697c...",
      "protocol": "ERC20",
      "id": "3255779687"
    }
  ]
}
```

---

### 20. GET `/wallet/withdrawHistory/{currency}`

Get withdrawal history for a specific currency.

| Location | Parameter | Type | Required | Default | Description |
|----------|-----------|------|----------|---------|-------------|
| Path | `currency` | string | Yes | — | Currency (e.g. `twd`, `btc`, `usdt`) |
| Query | `startTimestamp` | int64 | No | 90 days ago | Start time (ms) |
| Query | `endTimestamp` | int64 | No | Now | End time (ms) |
| Query | `limit` | int64 | No | 20 | Results per page (1–100) |
| Query | `id` | string | No | — | Pagination cursor |
| Query | `statuses` | string | No | — | Comma-separated status filter |
| Query | `txID` | string | No | — | Filter by transaction ID (crypto only, not for TWD) |

**Payload:** `{ "identity": email, "nonce": timestamp_ms }`

> Max query window: 90 days.

**Response Fields (data array):**

Same as deposit history fields: `serial`, `timestamp`, `address`, `amount`, `fee`, `total`, `status`, `txid`, `protocol`, `id`, `message`.

---

### 21. GET `/wallet/withdraw/{currency}/{serial}` or `/wallet/withdraw/{currency}/id/{id}`

Get details of a single withdrawal by serial number or by ID.

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Path | `currency` | string | Yes | Currency (e.g. `twd`, `btc`) |
| Path | `serial` | string | Conditional | Withdraw serial (use one of serial or id) |
| Path | `id` | string | Conditional | Withdraw ID (use one of serial or id) |

**Payload:** `{ "identity": email, "nonce": timestamp_ms }`

**Example Response:**

```json
{
  "data": {
    "serial": "20200417TW51258295",
    "protocol": "MAIN",
    "address": "64382xx3234",
    "amount": "12353",
    "fee": "15",
    "total": "12368",
    "status": "COMPLETE",
    "id": "3994629320",
    "timestamp": "1601951443123"
  }
}
```

---

### 22. POST `/wallet/withdraw/{currency}`

Submit a withdrawal request. Withdraw addresses must be pre-configured at https://www.bitopro.com/address.

**Rate Limit:** 60 req / min / IP

| Location | Parameter | Type | Required | Description |
|----------|-----------|------|----------|-------------|
| Path | `currency` | string | Yes | Currency name without protocol (e.g. `twd`, `usdt`, `btc`) |

**Payload:** The request body + nonce (no `identity`).

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol` | string | No | `MAIN` (default), `ERC20`, `OMNI`, `TRX`, `BSC`, `POLYGON` |
| `address` | string | Conditional | Destination address (required for non-TWD) |
| `amount` | string | Yes | Amount to withdraw |
| `message` | string | No | Note/memo (required for EOS, BNB) |
| `bankAccountSerial` | string | No | Bank account number (TWD only) |
| `bankSerial` | string | No | Bank code (TWD only) |

**Example Request (Crypto):**

```json
{
  "protocol": "ERC20",
  "address": "0x1234567890abcdef...",
  "amount": "100"
}
```

**Example Request (TWD):**

```json
{
  "amount": "50000",
  "bankAccountSerial": "1020000286850710",
  "bankSerial": "805"
}
```

**Example Response:**

```json
{
  "data": {
    "serial": "20200417TW51258295",
    "currency": "TWD",
    "protocol": "MAIN",
    "address": "64382xx3234",
    "amount": "12353",
    "fee": "15",
    "total": "12368",
    "id": "12368"
  }
}
```

---

## Order Status Codes

| Code | Status |
|------|--------|
| -1 | Not Triggered (stop-limit pending) |
| 0 | In Progress (unfilled) |
| 1 | In Progress (partially filled) |
| 2 | Completed (fully filled) |
| 3 | Completed (partially filled, then cancelled) |
| 4 | Cancelled |
| 6 | Post-Only Cancelled |
