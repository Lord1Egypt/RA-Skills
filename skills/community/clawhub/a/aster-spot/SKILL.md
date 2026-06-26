---
name: aster-spot
description: Aster Spot request using the Aster API. Authentication requires API key and secret key (HMAC SHA256). Supports mainnet.
metadata:
  version: 1.0.0
  author: Aster
license: MIT
---

# Aster Spot Skill

Spot request on Aster using authenticated API endpoints. Requires API key and secret key for certain endpoints. Return the result in JSON format.

## Data Fetching Guidelines (CRITICAL)

**NEVER truncate JSON responses** with `head -c`, `head -n`, or similar — truncated JSON is corrupted and will produce wrong results.

### Mandatory Rules

1. **Always specify `symbol` parameter** when querying a specific trading pair. Many endpoints return ALL symbols when `symbol` is omitted, producing responses of 100KB+.
2. **Always use `limit` parameter** to constrain result size. Use the smallest limit that satisfies the request (e.g., `limit=5` instead of default 500).
3. **Use `jq` to extract fields** — never parse raw mega-JSON visually. Pipe through `jq` to select only needed data.

### Progressive Data Exploration Strategy

When the user asks a broad question (e.g., "what spot pairs are available?"), use a **layered approach**:

1. **Step 1 — Get lightweight summary first:**
   ```bash
   # Get just the symbol list, not full exchangeInfo
   curl -s "https://sapi.asterdex.com/api/v1/exchangeInfo" | jq '[.symbols[].symbol]'
   ```

2. **Step 2 — Confirm scope with user** before fetching detailed data for many symbols.

3. **Step 3 — Fetch details for specific symbols only:**
   ```bash
   # Get price for ONE symbol, not all
   curl -s "https://sapi.asterdex.com/api/v1/ticker/price?symbol=BTCUSDT"
   ```

### Endpoints That Return Dangerously Large Data (without symbol filter)

| Endpoint | Without `symbol` | With `symbol` |
|----------|------------------|---------------|
| `/api/v1/exchangeInfo` | ALL symbols + filters (100KB+) | N/A — use `jq` to filter |
| `/api/v1/ticker/24hr` | ALL symbols (50KB+) | Single object (~500B) |
| `/api/v1/ticker/price` | ALL symbols (10KB+) | Single object (~80B) |
| `/api/v1/ticker/bookTicker` | ALL symbols (20KB+) | Single object (~150B) |
| `/api/v1/depth` | N/A (symbol required) | Varies by `limit`: use `limit=5` for overview |
| `/api/v1/klines` | N/A (symbol required) | Default 500 candles — always set `limit` |
| `/api/v1/trades` | N/A (symbol required) | Default 500 trades — always set `limit` |

### Example: Safe vs Unsafe

```bash
# BAD — returns ALL symbols, then truncates = corrupted JSON
curl -s ".../api/v1/ticker/price" | head -c 5000

# GOOD — returns single symbol, complete JSON
curl -s ".../api/v1/ticker/price?symbol=BTCUSDT"

# BAD — 500 candles by default
curl -s ".../api/v1/klines?symbol=BTCUSDT&interval=1h"

# GOOD — only 5 candles
curl -s ".../api/v1/klines?symbol=BTCUSDT&interval=1h&limit=5"

# GOOD — extract just symbol names from exchangeInfo
curl -s ".../api/v1/exchangeInfo" | jq '[.symbols[] | {symbol, status}]'
```

---

## Quick Reference

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/api/v1/ping` (GET) | Test server connectivity | None | None | No |
| `/api/v1/time` (GET) | Get server time | None | None | No |
| `/api/v1/exchangeInfo` (GET) | Trading specification information | None | None | No |
| `/api/v1/depth` (GET) | Order book depth | symbol | limit | No |
| `/api/v1/trades` (GET) | Recent trades list | symbol | limit | No |
| `/api/v1/historicalTrades` (GET) | Query historical trades | symbol | limit, fromId | Yes |
| `/api/v1/aggTrades` (GET) | Compressed/Aggregate trades list | symbol | fromId, startTime, endTime, limit | No |
| `/api/v1/klines` (GET) | K-line/Candlestick data | symbol, interval | startTime, endTime, limit | No |
| `/api/v1/ticker/24hr` (GET) | 24-hour price change statistics | None | symbol | No |
| `/api/v1/ticker/price` (GET) | Latest price ticker | None | symbol | No |
| `/api/v1/ticker/bookTicker` (GET) | Best bid/ask price ticker | None | symbol | No |
| `/api/v1/commissionRate` (GET) | Get symbol commission rate | symbol, timestamp | recvWindow | Yes |
| `/api/v1/order` (POST) | Place new order | symbol, side, type, timestamp | timeInForce, quantity, quoteOrderQty, price, newClientOrderId, stopPrice, recvWindow | Yes |
| `/api/v1/order` (DELETE) | Cancel order | symbol, timestamp | orderId, origClientOrderId, recvWindow | Yes |
| `/api/v1/order` (GET) | Query order | symbol, timestamp | orderId, origClientOrderId, recvWindow | Yes |
| `/api/v1/allOpenOrders` (DELETE) | Cancel all open orders on a symbol | symbol, timestamp | orderIdList, origClientOrderIdList, recvWindow | Yes |
| `/api/v1/openOrders` (GET) | Current open orders | timestamp | symbol, recvWindow | Yes |
| `/api/v1/allOrders` (GET) | Query all orders | symbol, timestamp | orderId, startTime, endTime, limit, recvWindow | Yes |
| `/api/v1/account` (GET) | Account information | timestamp | recvWindow | Yes |
| `/api/v1/userTrades` (GET) | Account trade history | timestamp | symbol, orderId, startTime, endTime, fromId, limit, recvWindow | Yes |
| `/api/v1/asset/wallet/transfer` (POST) | Perp-Spot transfer | amount, asset, clientTranId, kindType, timestamp | None | Yes |
| `/api/v1/asset/sendToAddress` (POST) | Transfer asset to other address | amount, asset, toAddress, timestamp | clientTranId, recvWindow | Yes |
| `/api/v1/aster/withdraw/estimateFee` (GET) | Get withdrawal fee estimate | chainId, asset | None | No |
| `/api/v1/aster/user-withdraw` (POST) | Withdraw funds | chainId, asset, amount, fee, receiver, nonce, userSignature, timestamp | recvWindow | Yes |
| `/api/v1/getNonce` (POST) | Get nonce for API key creation | address, userOperationType | network | No |
| `/api/v1/createApiKey` (POST) | Create API key | address, userOperationType, userSignature, desc, timestamp | network, apikeyIP, recvWindow | No |
| `/api/v1/listenKey` (POST) | Generate user data stream listen key | None | None | Yes (API key only) |
| `/api/v1/listenKey` (PUT) | Extend listen key validity | listenKey | None | Yes (API key only) |
| `/api/v1/listenKey` (DELETE) | Close user data stream | listenKey | None | Yes (API key only) |

---

## Parameters

### Common Parameters

* **symbol**: Trading pair (e.g., BTCUSDT)
* **limit**: Default 500; maximum 1000 (depth endpoint supports: 5, 10, 20, 50, 100, 500, 1000; klines max 1500)
* **fromId**: Return starting from trade ID (e.g., 1)
* **startTime**: Timestamp in ms to get data from INCLUSIVE (e.g., 1735693200000)
* **endTime**: Timestamp in ms to get data until INCLUSIVE (e.g., 1735693200000)
* **recvWindow**: The value cannot be greater than `60000`. Default 5000. (e.g., 5000)
* **timestamp**: Unix timestamp in milliseconds (e.g., 1735693200000)
* **quantity**: Order quantity (e.g., 1)
* **quoteOrderQty**: Quote order quantity (e.g., 100)
* **price**: Order price (e.g., 50000)
* **stopPrice**: Required for STOP, STOP_MARKET, TAKE_PROFIT, TAKE_PROFIT_MARKET orders (e.g., 49000)
* **newClientOrderId**: Client-customized unique order ID. Automatically generated if not sent.
* **orderId**: Order ID (e.g., 1)
* **origClientOrderId**: Original client order ID
* **orderIdList**: Order ID array string (for batch cancel)
* **origClientOrderIdList**: Client order ID array string (for batch cancel)
* **amount**: Transfer/withdrawal quantity (e.g., 1.5)
* **asset**: Asset type (e.g., USDT, BTC)
* **clientTranId**: Client transaction ID (minimum 20 characters if provided)
* **kindType**: Transfer direction: FUTURE_SPOT or SPOT_FUTURE
* **toAddress**: Target EVM address for transfers
* **chainId**: Chain ID for withdrawals: 1 (ETH), 56 (BSC), 42161 (Arbi)
* **fee**: Withdrawal fee
* **receiver**: Current account address (for withdrawals)
* **nonce**: Current time in microseconds (for withdrawals)
* **userSignature**: EVM wallet signature
* **address**: Wallet address (for API key creation)
* **userOperationType**: Operation type: CREATE_API_KEY
* **network**: Network type (SOL for Solana network only)
* **apikeyIP**: Comma-separated IP addresses for whitelist
* **desc**: API key description (max 20 characters; no duplicates per account)
* **listenKey**: Listen key for user data streams

### Enums

* **side**: BUY | SELL
* **type** (order type): LIMIT | MARKET | STOP | TAKE_PROFIT | STOP_MARKET | TAKE_PROFIT_MARKET
* **timeInForce**: GTC | IOC | FOK | GTX
* **interval**: 1m | 3m | 5m | 15m | 30m | 1h | 2h | 4h | 6h | 8h | 12h | 1d | 3d | 1w | 1M
* **kindType**: FUTURE_SPOT | SPOT_FUTURE
* **orderStatus**: NEW | PARTIALLY_FILLED | FILLED | CANCELED | REJECTED | EXPIRED


## Authentication

For endpoints that require authentication, you will need to provide Aster API credentials.
Required credentials:

* apiKey: Your Aster API key (for header)
* secretKey: Your Aster API secret (for signing)

Base URL:
* Mainnet: https://sapi.asterdex.com

WebSocket:
* Market Streams: wss://sstream.asterdex.com

See [`references/authentication.md`](./references/authentication.md) for implementation details.

## Security

### Share Credentials

Users can provide Aster API credentials by sending a file where the content is in the following format:

```bash
abc123...xyz
secret123...key
```

### Never Display Full Secrets

When showing credentials to users:
- **API Key:** Show first 5 + last 4 characters: `bb3b2...02ae`
- **Secret Key:** Always mask, show only last 5: `***...ae1c`

Example response when asked for credentials:
Account: main
API Key: bb3b2...02ae
Secret: ***...ae1c
Environment: Mainnet

### Listing Accounts

When listing accounts, show names and environment only — never keys:
Aster Accounts:
* main (Mainnet)
* trading (Mainnet)

### Transactions in Mainnet

When performing transactions in mainnet, always confirm with the user before proceeding by asking them to write "CONFIRM" to proceed.

---

## Aster Accounts

### main
- API Key: your_mainnet_api_key
- Secret: your_mainnet_secret
- Testnet: false

### TOOLS.md Structure

```bash
## Aster Accounts

### main
- API Key: abc123...xyz
- Secret: secret123...key
- Testnet: false
- Description: Primary trading account

### trading
- API Key: trade456...abc
- Secret: tradesecret...xyz
- Testnet: false
- Description: Secondary trading account
```

## Agent Behavior

1. Credentials requested: Mask secrets (show last 5 chars only)
2. Listing accounts: Show names and environment, never keys
3. Account selection: Ask if ambiguous, default to main
4. When doing a transaction in mainnet, confirm with user before by asking to write "CONFIRM" to proceed
5. New credentials: Prompt for name, environment, signing mode

## Adding New Accounts

When user provides new credentials:

* Ask for account name
* Ask: Mainnet?
* Store in `TOOLS.md` with masked display confirmation

## Signing Requests

All trading endpoints require HMAC SHA256 signature:

1. Build query string with all params + timestamp (Unix ms)
2. Sign query string with secretKey using HMAC SHA256
3. Append signature to query string
4. Include `X-MBX-APIKEY` header

See [`references/authentication.md`](./references/authentication.md) for implementation details.
