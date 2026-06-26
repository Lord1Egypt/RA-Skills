---
name: bou-wallet
description: >
  Use this skill when an external agent already has an agent API key and needs
  to call this backend directly with curl for three capability groups:
  (1) `POST /agent/pay-and-call` for x402-paid upstream requests.
  (2) `GET /agent/me` to inspect the current agent wallet/profile.
  (3) the `/hyperliquid` endpoints for status, balances, markets, asset data,
  funding, orderbook, positions, fills, ticker, order placement, cancellation,
  leverage updates, transfers, and withdrawals.
---

# BOU Wallet

Use direct HTTP requests with `curl`. Prefer this skill when the task is to operate this backend through an existing agent bearer key instead of building a separate SDK or CLI first.

## First-time setup after install

If the user has installed this skill but does not have an agent API key yet, walk them through this setup first:

1. Open `https://app.bankofuniverse.org/`
2. Sign in, then create an agent in the app
3. Generate the agent API key, then copy it and use it as `AGENT_KEY` in requests

If the user has not completed these steps yet, do not pretend the skill can run successfully. First help them obtain a valid `ak_...` key.

## Required inputs

Collect these values before making any request:

- `BASE_URL`: use `https://api.bankofuniverse.org/` unless the user explicitly gives a different backend
- `AGENT_KEY`: bearer token in `ak_...` format

Treat the agent key as secret. Do not print, commit, or store it in repo files.

## Common request pattern

Use the same bearer auth for all three capability groups.

```sh
curl -sS "$BASE_URL/..." \
  -H "Authorization: Bearer $AGENT_KEY" \
  -H "Accept: application/json"
```

For JSON request bodies, also add:

```sh
-H "Content-Type: application/json"
```

Most responses use the shared wrapper:

```json
{
  "code": 0,
  "message": "",
  "data": {}
}
```

## Capability 1: x402 pay-and-call

Use `POST /agent/pay-and-call` when the agent needs to access an x402-protected upstream URL through this backend. Call this backend endpoint, not the merchant directly.

Body shape:

```json
{
  "url": "https://merchant.example.com/path",
  "method": "GET",
  "headers": {
    "X-Custom-Header": "value"
  },
  "body": {
    "query": "ETH price"
  }
}
```

Rules:

- Send a full upstream `http://` or `https://` URL in `url`
- Use the upstream HTTP verb in `method`
- Pass merchant headers as a JSON object when needed
- Pass `body` only when the upstream endpoint expects one
- The backend enforces agent status and USDC payment limits before paying
- The backend rejects requests when the required payment is `>= 0.1` USDC

Example:

```sh
curl -sS -X POST "$BASE_URL/agent/pay-and-call" \
  -H "Authorization: Bearer $AGENT_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://api.example.com/search",
    "method": "POST",
    "body": {
      "query": "BTC"
    }
  }'
```

### x402 test cases

Use these upstream URLs to quickly test the `pay-and-call` flow.

#### Test case 1: random number

Upstream endpoint:

- `GET /cos/crypto/chainlink/random`

Expected response body:

```json
{
  "number": 42
}
```

Example:

```sh
curl -sS -X POST "https://api.bankofuniverse.org/agent/pay-and-call" \
  -H "Authorization: Bearer $AGENT_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://skills.bankofuniverse.org/cos/crypto/chainlink/random",
    "method": "GET"
  }'
```

#### Test case 2: crypto price

Upstream endpoint:

- `GET /cos/crypto/price/:symbol`

Supported symbols:

- `ETH`
- `BTC`
- `USDC`
- `USDT`
- `TRX`
- `BNB`

Expected response body:

```json
{
  "symbol": "BTC",
  "supportedSymbols": ["ETH", "BTC", "USDC", "USDT", "TRX", "BNB"],
  "price": 84000.12,
  "timestamp": 1710000000000
}
```

Example:

```sh
curl -sS -X POST "https://api.bankofuniverse.org/agent/pay-and-call" \
  -H "Authorization: Bearer $AGENT_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://skills.bankofuniverse.org/cos/crypto/price/BTC",
    "method": "GET"
  }'
```

## Capability 2: current agent info

Use `GET /agent/me` to inspect the current agent resolved by the bearer key.

This endpoint returns the resolved agent, matched API key metadata, cumulative spent USDC, and a best-effort Base USDC balance lookup.

Example:

```sh
curl -sS "$BASE_URL/agent/me" \
  -H "Authorization: Bearer $AGENT_KEY"
```

## Capability 3: Hyperliquid operations

Use the `/hyperliquid` endpoints when the agent needs to inspect or trade through the backend's Hyperliquid integration. All requests use the same bearer auth pattern.

### Read endpoints

- `GET /hyperliquid/status`
  Purpose: verify the current agent is authorized to use Hyperliquid for the resolved account.
  Key return fields: `address` is the resolved Hyperliquid account address. In agent mode, the response may also include signer-related identity information returned by the backend.
  Use it when: you want to confirm the bearer key is valid and Hyperliquid access is ready before reading balances or sending orders.
- `GET /hyperliquid/balances`
  Purpose: fetch the latest account balance snapshot from Hyperliquid.
  Key return fields: `data` contains the balance payload returned by Hyperliquid for the resolved account, including available funds and account balance details.
  Use it when: you need to check available funds before trading, transferring, or withdrawing.
- `GET /hyperliquid/open-orders?coin=BTC`
  Purpose: list current open orders, optionally filtered by one symbol.
  Key return fields: each item is normalized to include readable `coin`, `side`, and `marketType`; the rest of the item is the underlying open-order data.
  Use it when: you want to inspect working orders before canceling or placing another order.
- `GET /hyperliquid/markets?marketType=perp`
  Purpose: list supported spot or perp markets.
  Key return fields: spot markets include fields such as `coin`, `pairId`, `base`, `quote`, `szDecimals`, `weiDecimals`, and `marketType`; perp markets include fields such as `coin`, `base`, `quote`, `dexName`, `maxLeverage`, `szDecimals`, `onlyIsolated`, `marginMode`, and `marketType`.
  Use it when: you need to discover valid symbols, decimals, supported dex markets, or leverage-related metadata before trading.
- `GET /hyperliquid/active-asset-data?coin=BTC`
  Purpose: inspect the current account trading state for one perp coin.
  Key return fields: `coin`, `leverage`, `isCross`, `leverageType`, `maxTradeSzs`, `availableToTrade`, and `markPx`.
  `maxTradeSzs` and `availableToTrade` are two-element arrays: index `0` is the `BUY` value and index `1` is the `SELL` value.
  Use it when: you need the current leverage mode, tradeable size, or mark price for a perp coin before placing or sizing an order.
- `GET /hyperliquid/funding?coin=BTC`
  Purpose: fetch current and next funding information for one perp market.
  Key return fields: `coin`, `fundingRate`, `nextFundingRate`, `nextFundingTimestamp`, `markPrice`, and `indexPrice`.
  Use it when: you want to evaluate funding cost, expected next funding, or compare mark price with oracle/index price.
- `GET /hyperliquid/orderbook?coin=BTC`
  Purpose: fetch the live L2 order book for one market.
  Key return fields: `data` is the raw Hyperliquid order book snapshot, including bid and ask levels plus the snapshot time.
  Use it when: you need market depth, best bid/ask context, or raw book levels for quoting and execution logic.
- `GET /hyperliquid/positions`
  Purpose: list current perp positions across available dex contexts for the account.
  Key return fields: each position includes `dexName`, `marketType`, `coin`, `szi`, `leverage`, `isCross`, `leverageType`, `entryPx`, `positionValue`, `unrealizedPnl`, `returnOnEquity`, `liquidationPx`, `marginUsed`, `maxLeverage`, and `cumFunding`.
  Use it when: you want a full view of current exposure, PnL, liquidation risk, and leverage usage.
- `GET /hyperliquid/fills?coin=BTC&since=1710000000000&limit=100`
  Purpose: list historical fills for the account, optionally filtered by symbol, start time, and result count.
  Key return fields: each fill is normalized to include readable `coin`, `side`, and `marketType`; the rest of the fill fields come from Hyperliquid's fill history.
  Use it when: you want recent execution history for trade reconciliation, reporting, or strategy logic.
- `GET /hyperliquid/ticker?coin=BTC&marketType=perp`
  Purpose: fetch a compact ticker-style market snapshot for one symbol.
  Key return fields: `coin`, `marketType`, `last`, `bid`, `ask`, `open`, `close`, `change`, `percentage`, `volume`, `quoteVolume`, and `timestamp`.
  Use it when: you need a lightweight summary of current price, spread, daily move, and volume without reading the full order book.

Query rules:

- `marketType`: `perp` or `spot`
- `coin`: short asset symbol such as `BTC` or `ETH`
- `limit` for fills: `1` to `500`
- `nSigFigs` for orderbook: `2`, `3`, `4`, or `5`
- `mantissa` for orderbook: `2` or `5`

### Write endpoints

- `POST /hyperliquid/order`
- `POST /hyperliquid/cancel`
- `POST /hyperliquid/cancel-all`
- `POST /hyperliquid/set-leverage`
- `POST /hyperliquid/transfer`
- `POST /hyperliquid/withdraw`

#### Place order

Request body:

```json
{
  "coin": "BTC",
  "marketType": "perp",
  "orderType": "limit",
  "side": "BUY",
  "size": "0.001",
  "price": "50000",
  "reduceOnly": false,
  "timeInForce": "Gtc"
}
```

Field rules:

- `orderType`: `market`, `limit`, `stop_limit`, `stop_market`, or `twap`
- `side`: `BUY` or `SELL`
- `size`: numeric string
- `price`: optional in the DTO, but required for limit-style orders such as `limit` and `stop_limit`
- `triggerPrice`: optional in the DTO, but use it for stop orders such as `stop_limit` and `stop_market`
- `tpPrice` and `slPrice`: optional take-profit and stop-loss values
- `timeInForce`: `Gtc`, `Ioc`, or `Alo`
- `durationMinutes`: optional in the DTO, min `5`, max `1440`; use it for TWAP-style flows when required by the backend logic
- `randomizeSlices`: optional boolean for TWAP-style flows

Example:

```sh
curl -sS -X POST "$BASE_URL/hyperliquid/order" \
  -H "Authorization: Bearer $AGENT_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "coin": "BTC",
    "marketType": "perp",
    "orderType": "limit",
    "side": "BUY",
    "size": "0.001",
    "price": "50000"
  }'
```

#### Cancel selected orders

Request body:

```json
{
  "orders": [
    {
      "coin": "BTC",
      "orderId": 123456
    }
  ]
}
```

Field rules:

- `orders`: required array with at most `100` items
- `coin`: required string for each item
- `orderId`: required integer for each item, minimum `0`

#### Cancel all orders

Request body:

```json
{
  "coin": "BTC"
}
```

Omit `coin` to cancel all open orders across supported assets.

#### Set leverage

Request body:

```json
{
  "coin": "BTC",
  "leverage": 5,
  "isCross": true
}
```

#### Transfer asset

Request body:

```json
{
  "amount": "10",
  "dex": "",
  "fromPerp": true
}
```

Field rules:

- `amount`: required numeric string
- `dex`: optional dex name string; omit it to use the primary dex.
- `fromPerp`: optional boolean, `true` means transfer from perp side

#### Withdraw asset

Use this endpoint to withdraw Perps USDC to the Arbitrum network.

Request body:

```json
{
  "destination": "0x1234567890abcdef1234567890abcdef12345678",
  "amount": "10"
}
```

Field rules:

- `destination`: required EVM address
- `amount`: required numeric string

## Execution checklist

Before running requests:

- Verify `BASE_URL` is correct
- Verify the token looks like `ak_...`
- Verify JSON is valid
- Verify Hyperliquid enum values match the accepted casing exactly
- Prefer the two built-in x402 test cases above when validating a new agent key
- Use `-i` when you need status codes or headers for debugging

If a request fails, inspect the wrapped JSON `message` plus the HTTP status first.
