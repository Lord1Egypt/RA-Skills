---
{
  "name": 'Coinw Spot Skill',
  "description": 'Coinw Spot REST API skill: covers market data, order placement/cancellation, order queries, account balances, and asset transfers.',
  "metadata": {"version": "1.5.0","author": "Coinw","openclaw":{"always": true,"requires":{"env":["COINW_API_KEY","COINW_SECRET_KEY"]}}}
}
---

# Coinw Spot Skill

Coinw Spot REST API skill: covers market data, order placement/cancellation, order queries, account balances, and asset transfers.

### Setup Credentials
CoinW private endpoints require `api_key` and a request signature (`sign`).

> Signing note: Spot endpoints use Spot MD5 uppercase signing. Do not use Contract HMAC-SHA256 signing for Spot APIs.

1. Environment variables:
```bash
export COINW_API_KEY="your_api_key"
export COINW_SECRET_KEY="your_secret_key"
```
2. In chat: provide `api_key`/`secret_key` (and an account name). The agent will mask secrets when showing them back and store them securely in OpenClaw's credential storage (not inside skill markdown files).

## Key Features
- Market data: trading pairs, 24h summary, order book, recent trades, K-line data, hot volume stats
- Trading actions: place order, cancel order / cancel all orders
- Query and account: order query, trade history, spot balances, asset transfer

## Quick Reference

### Market Information

| No. | name | Endpoint | Description | Method | Authentication | Input Parameters | Output Parameters | Detailed Doc URL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.1 | Get trading pair information | `/api/v1/public?command=returnSymbol` | Returns detailed information for all spot pairs, including min/max order price, quantity limits, and precision. | GET | Public | — | currencyPair, currencyBase, currencyQuote, maxBuyCount, minBuyCount, pricePrecision, countPrecision, minBuyAmount, maxBuyAmount, and 12 total fields | `https://www.coinw.com/api-doc/spot-trading/market/get-trading-pair-information` |
| 1.2 | Get 24h ticker summary for all pairs | `/api/v1/public?command=returnTicker` | Returns 24h summary metrics for all available pairs, including last price, best bid/ask, and volume. | GET | Public | — | id, last, lowestAsk, highestBid, percentChange, isFrozen, high24hr, low24hr, baseVolume | `https://www.coinw.com/api-doc/spot-trading/market/get-24h-trade-summary-for-all-instruments` |
| 1.4 | Get order book | `/api/v1/public?command=returnOrderBook` | Queries spot order book data for a specified pair. Supports 5-level or 20-level depth. | GET | Public | size, symbol | asks, quantity, price, bids, quantity, price, pair | `https://www.coinw.com/api-doc/spot-trading/market/get-order-book` |
| 1.5 | Get recent trades | `/api/v1/public?command=returnTradeHistory` | Queries recent trade records for a specified pair, including amount, price, total, time, side, and trade ID. | GET | Public | symbol | id, type, price, amount, total, time, pair | `https://www.coinw.com/api-doc/spot-trading/market/get-recent-trades` |
| 1.6 | Get K-line data | `/api/v1/public?command=returnChartData` | Queries K-line (candlestick) data for a specified pair, including OHLC and volume. | GET | Public | currencyPair, period | date, high, low, open, close, volume, pair | `https://www.coinw.com/api-doc/spot-trading/market/get-k-line` |
| 1.7 | Get 24h volume for hot pairs | `/api/v1/public?command=return24hVolume` | Returns 24h volume summary for popular pairs and market totals (such as BTC/ETH/USDT-related metrics). | GET | Public | — | data, totalETH, totalUSDT, totalBTC, ETH_USDT, ETH, USDT, LTC_CNYT, LTC, and 28 total fields | `https://www.coinw.com/api-doc/spot-trading/market/get-24h-volume-for-popular-instruments` |

### Place Orders

| No. | name | Endpoint | Description | Method | Authentication | Input Parameters | Output Parameters | Detailed Doc URL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2.1 | Place order | `/api/v1/private?command=doTrade` | Places a spot order by specifying order type, amount, price, and external order ID. | POST | Private | api_key, sign, symbol, type, amount, rate, isMarket, out_trade_no | orderNumber | `https://www.coinw.com/api-doc/spot-trading/trade/place-order` |
| 2.2 | Cancel order | `/api/v1/private?command=cancelOrder` | Cancels an unfilled spot order by order ID. | POST | Private | api_key, sign, orderNumber | clientOrderId | `https://www.coinw.com/api-doc/spot-trading/trade/cancel-order` |
| 2.3 | Cancel all orders | `/api/v1/private?command=cancelAllOrder` | Cancels all unfilled orders for a specified trading pair. | POST | Private | api_key, sign, currencyPair | msg | `https://www.coinw.com/api-doc/spot-trading/trade/cancel-all-orders` |

### Query Orders

| No. | name | Endpoint | Description | Method | Authentication | Input Parameters | Output Parameters | Detailed Doc URL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3.1 | Get open orders | `/api/v1/private?command=returnOpenOrders` | Returns all current unfilled orders for a specified pair, including order ID, time, amount, and status. | POST | Private | api_key, sign, currencyPair, startAt, endAt | orderNumber, date, startingAmount, total, type, prize, success_count, success_amount, status | `https://www.coinw.com/api-doc/spot-trading/check/get-current-orders` |
| 3.2 | Get historical orders | `/api/v1/private?command=getUserTrades` | Retrieves historical orders across pairs, with optional symbol filtering. Up to 100 records per request. | POST | Private | api_key, sign, symbol | tradeId, orderId, price, size, side, orderType, time, fee, before, and 10 total fields | `https://www.coinw.com/api-doc/spot-trading/check/get-historical-orders` |
| 3.3 | Batch get historical orders | `/v1/private?command=getBatchHistoryOrders` | Batch query historical orders (last 3 months) by order ID list (see api-doc 3.3 for details). | POST | Private | api_key, sign, orderIds | data, orderId, date, side, type, dealSize, dealFunds, dealAvgPrice, fee, and 16 total fields | `https://www.coinw.com/api-doc/spot-trading/check/get-batch-historical-orders` |
| 3.4 | Get order details | `/api/v1/private?command=returnOrderTrades` | Returns detailed information for a specified order ID. | POST | Private | api_key, sign, orderNumber | tradeID, currencyPair, type, amount, success_amount, total, success_total, fee, date, and 10 total fields | `https://www.coinw.com/api-doc/spot-trading/check/get-order-details` |
| 3.5 | Get order status | `/api/v1/private?command=returnOrderStatus` | Queries order status by order ID, including pair, side, amount, execution status, and timestamp. | POST | Private | api_key, sign, orderNumber | currencyPair, type, total, startingAmount, status, date | `https://www.coinw.com/api-doc/spot-trading/check/get-order-status` |
| 3.6 | Get trade history | `/api/v1/private?command=returnUTradeHistory` | Returns trade history records for a specified pair. | POST | Private | api_key, sign, currencyPair | tradeID, type, amount, success_amount, total, success_count, fee, prize, date, and 11 total fields | `https://www.coinw.com/api-doc/spot-trading/check/get-transaction-history` |

### Account Information

| No. | name | Endpoint | Description | Method | Authentication | Input Parameters | Output Parameters | Detailed Doc URL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4.1 | Get spot account balance | `/api/v1/private?command=returnBalances` | Retrieves available balances in the user's spot account across supported assets. | POST | Private | api_key, sign | data, msg | `https://www.coinw.com/api-doc/spot-trading/account/get-spot-account-balance` |
| 4.2 | Get complete spot balances | `/api/v1/private?command=returnCompleteBalances` | Retrieves full spot balance details, including available balances and order-frozen balances. | POST | Private | api_key, sign | data, available, onOrders | `https://www.coinw.com/api-doc/spot-trading/account/get-total-spot-account-balance` |
| 4.7 | Asset transfer | `/api/v1/private?command=spotWealthTransfer` | Transfers assets between the spot account and funding account for fund management. | POST | Private | api_key, sign, accountType, targetAccountType, bizType, coinCode, amount | data, msg | `https://www.coinw.com/api-doc/spot-trading/account/transfer-assets` |

## Common Parameters and Enums

### Auth and URL
- Base URL: `https://api.coinw.com`.
- Public REST: `GET/POST https://api.coinw.com/api/v1/public?command=...`.
- Private REST: usually `POST https://api.coinw.com/api/v1/private?command=...`, with `api_key` and `sign` (MD5, see Reference) in query/body.
- Some docs show `/v1/private?command=...` alongside `/api/v1/private`; follow actual implementation.
### `command` values (private/public endpoints covered in this file)
`cancelAllOrder`, `cancelOrder`, `doTrade`, `getBatchHistoryOrders`, `getUserTrades`, `return24hVolume`, `returnBalances`, `returnChartData`, `returnCompleteBalances`, `returnOpenOrders`, `returnOrderBook`, `returnOrderStatus`, `returnOrderTrades`, `returnSymbol`, `returnTicker`, `returnTradeHistory`, `returnUTradeHistory`, `spotWealthTransfer`
### Common request fields
- **symbol / currencyPair**: trading pair, for example `BTC_USDT` (field names vary by endpoint).
- **isMarket**: market-order related; **type**: order type; **rate / amount / funds**: price, quantity, or amount (see order placement section).
### Standard response wrapper (common in REST)
- Common top-level fields: `code`, `msg` / `message`, `success`, `failed`, `data` (actual response varies by endpoint).
### Common enums
- **failed**: true/false; indicates whether request failed.
- **isFrozen**: freeze status: 0 = no, 1 = yes.
- **side**：BUY/SELL
- **state**: pair status: 1 = active, 2 = disabled.
- **status**: 1 = unfilled, 2 = partially filled, 3 = fully filled, 4 = user canceled; order status may also include 5 = triggered, 6 = trigger failed.
- **success**: true/false; indicates whether request succeeded.
- **type** (orders, such as in batch history): `LIMIT`, `MARKET`, `HL_LIMIT`, `PLANNING`, `STOP_LIMIT_ORDER`, `SMART_MARKET_ORDER`, `ICEBERG`, etc.

## Examples
### GET (public endpoint)
```bash
curl "https://api.coinw.com/api/v1/public?command=returnSymbol"
```
### Auth required (private endpoint)
```bash
params="api_key=$COINW_API_KEY&amount=0.001&funds=1&isMarket=1&out_trade_no=1&rate=40000&symbol=BTC_USDT"
sign_string="$params&secret_key=$COINW_SECRET_KEY"
sign=$(echo -n "$sign_string" | openssl md5 | cut -d' ' -f2 | tr '[:lower:]' '[:upper:]')
curl -X POST "https://api.coinw.com/api/v1/private?command=doTrade&$params&sign=$sign"
```
## Security
When showing credentials to users:
- **API Key:** Show first 4 + last 5 characters: `12&*1...198I`
- **Secret Key:** Always mask, show only last 4: `***...isf1`
- Ask for user confirmation before any trade action.
- Store user `api_key` and `secret_key` in a secure location.

## Agent Behavior

1. Credentials requested: Mask secrets (show last 5 chars only)
2. Listing accounts: Show names never keys
3. New credentials: Prompt for name, signing mode

## Adding New Accounts

When user provides new credentials:

* Ask for account name 
* Store the provided credentials in OpenClaw's secure credential store with masked display confirmation 

## Reference
- Authentication`./references/Authentication.md`
- errorcode: `./references/error-codes.md`
- notes: `./references/notes.md`
- api-key create steps: `./references/api-key-creation-steps.md`
