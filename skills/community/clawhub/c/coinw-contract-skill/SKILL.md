---
{
  "name": 'Coinw Contract Skill',
  "description": 'Coinw Contract REST API skill: covers market data, order placement/cancellation, TP/SL, position and order queries, account assets, position modes, and leverage queries.',
  "metadata": {"version": "1.5.0","author": "Coinw","openclaw":{"always": true,"requires":{"env":["COINW_API_KEY","COINW_SECRET_KEY"]}}}
}
---

# Coinw Contract Skill

Coinw Contract REST API skill: covers market data, order placement/cancellation, TP/SL, position and order queries, account assets, position modes, and leverage.


### Setup Credentials
CoinW private endpoints require `api_key` and a request signature (`sign`).

> Signing note: Contract endpoints must use Contract signing (HMAC-SHA256 + Base64 + `timestamp` headers). Do not use Spot MD5 signing for Contract APIs.

1. Environment variables:
```bash
export COINW_API_KEY="your_api_key"
export COINW_SECRET_KEY="your_secret_key"
```
2. In chat: provide `api_key`/`secret_key` (and an account name). The agent will mask secrets when showing them back and store them securely in OpenClaw's credential storage (not inside skill markdown files).

## Key Features
- Market data: contract instruments, order book, K-line data, trades, margin requirements
- Trading and risk control: place orders, close/reverse positions, TP/SL (including trailing)
- Queries and positions: order history, TP/SL info, margin rate, and position queries
- Account and general: transferable balance, deal records, account assets and fee rates, almighty-gold, unit conversion, position mode, user available size, leverage query


## Quick Reference

### Market Information

| No. | name | Endpoint | Description | Method | Authentication | Input Parameters | Output Parameters | Detailed Doc URL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.1 | Get instrument info | `/v1/perpum/instruments` | Queries basic information for all instruments, including leverage, margin, TP/SL ratios, maker/taker fee, funding rate, max position size, etc. | GET | Public | name | base, defaultLeverage, defaultStopLossRate, defaultStopProfitRate, indexId, leverage, makerFee, maxLeverage, minLeverage, and 37 total fields | `https://www.coinw.com/api-doc/futures-trading/market/get-instrument-information` |
| 1.2 | Get batch instrument info | `/v1/perpum/instrumentList` | Batch query basic information for multiple instruments in one request, including leverage, margin requirements, fee parameters, and max position size. | GET | Public | symbols | base, defaultLeverage, defaultStopLossRate, defaultStopProfitRate, indexId, leverage, makerFee, maxLeverage, minLeverage, and 38 total fields | `https://www.coinw.com/api-doc/futures-trading/market/get-batch-instrument-information` |
| 1.3 | Get latest ticker for one instrument | `/v1/perpumPublic/ticker` | Returns latest ticker summary for one instrument, including high/low, max leverage, volume, last price, and contract size. | GET | Public | instrument | contract_id, name, base_coin, quote_coin, price_coin, max_leverage, contract_size, last_price, high, and 13 total fields | `https://www.coinw.com/api-doc/futures-trading/market/get-last-trade-summary-of-an-instrument` |
| 1.4 | Get latest ticker summary in batch | `/v1/perpumPublic/ticker/list` | Batch query latest ticker summary for multiple instruments. | GET | Public | symbols | contract_id, name, base_coin, quote_coin, price_coin, max_leverage, contract_size, last_price, high, and 13 total fields | `https://www.coinw.com/api-doc/futures-trading/market/get-batch-last-trade-summary` |
| 1.5 | Get latest ticker summary for all instruments | `/v1/perpumPublic/tickers` | Returns latest ticker summary for all instruments on the exchange. | GET | Public | — | contract_id, name, base_coin, quote_coin, price_coin, max_leverage, contract_size, last_price, high, and 13 total fields | `https://www.coinw.com/api-doc/futures-trading/market/get-last-trade-summary-of-all-instruments` |
| 1.6 | Get historical K-line data by instrument | `/v1/perpumPublic/klines` | Queries historical and latest K-line data for one instrument, including OHLC, timestamp, and volume. | GET | Public | See api-doc 1.6 (for example granularity, klineType, limit, reporting coin, and time-range params) | K-line array: each item includes timestamp, high/open/low/close, and volume | `https://www.coinw.com/api-doc/futures-trading/market/get-k-line-of-an-instrument` |
| 1.7 | Get latest settled funding rate | `/v1/perpum/fundingRate` | Returns the funding rate at the most recent settlement time. It is not necessarily related to the next settlement rate. | GET | Public | instrument | data | `https://www.coinw.com/api-doc/futures-trading/market/get-last-settelment-funding-fee-rate` |
| 1.8 | Get order book by instrument | `/v1/perpumPublic/depth` | Queries order book depth for a specified instrument, including bids and asks. | GET | Public | base | asks, bids, m, p, n | `https://www.coinw.com/api-doc/futures-trading/market/get-order-book-of-an-instrument` |
| 1.9 | Get trade data by instrument | `/v1/perpumPublic/trades` | Queries recent trade data for a specified instrument, including size, side, ID, timestamp, and price. Returns the latest 20 trades by default. | GET | Public | base | createdDate, piece, direction, price, quantity, id | `https://www.coinw.com/api-doc/futures-trading/market/get-trade-data-of-an-instrument` |
| 1.10 | Get margin requirements for all instruments | `/v1/perpum/ladders` | Queries tiered margin requirements for all instruments, including initial/maintenance margin and max leverage. | GET | Private | api_key, sign | id, instrument, ladder, lastLadder, marginKeepRate, maxLeverage, marginStartRate, maxPiece | `https://www.coinw.com/api-doc/futures-trading/market/get-margin-requirements-of-all-instruments` |
| 1.11 | Get historical public trades | `/v1/perpum/orders/trades` | Queries historical public trade records for a specified instrument. Historical public trades are available via RESTful API only. | GET | Private | api_key, sign, instrument, pageSize | closedPiece, createdDate, dealPrice, direction, id | `https://www.coinw.com/api-doc/futures-trading/market/get-historical-public-trades` |

### Place Orders

| No. | name | Endpoint | Description | Method | Authentication | Input Parameters | Output Parameters | Detailed Doc URL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2.1 | Place order | `/v1/perpum/order` | Places a contract order. Supports market, limit, and trigger order types. | POST | Private | api_key, sign, instrument, direction, leverage, quantityUnit, quantity, positionModel, positionType, openPrice, stopProfitPrice, stopLossPrice, thirdOrderId | code, data | `https://www.coinw.com/api-doc/futures-trading/trade/place-an-order` |
| 2.2 | Batch place orders | `/v1/perpum/batchOrders` | Batch places contract orders with support for market, limit, and trigger order types. | POST | Private | api_key, sign, instrument, direction, leverage, quantityUnit, quantity, positionModel, positionType, openPrice, stopProfitPrice, stopLossPrice, triggerPrice, triggerType, thirdOrderId | code, openId, thirdOrderId | `https://www.coinw.com/api-doc/futures-trading/trade/place-batch-orders` |
| 2.3 | Close position | `/v1/perpum/positions` | Partially or fully closes an open contract position (filled order). Supports closing by fixed size or by position percentage. | DELETE | Private | api_key, sign, id, positionType, closeNum, orderPrice | data | `https://www.coinw.com/api-doc/futures-trading/trade/close-a-position` |
| 2.4 | Batch close positions | `/v1/perpum/batchClose` | Closes multiple positions at market price in batch using `thirdOrderId` values. | DELETE | Private | api_key, sign, thirdOrderId | openId, thirdOrderId | `https://www.coinw.com/api-doc/futures-trading/trade/close-batch-positions` |
| 2.5 | Market close all positions | `/v1/perpum/allpositions` | Closes all positions for the specified instrument at market price. | DELETE | Private | api_key, sign | — | `https://www.coinw.com/api-doc/futures-trading/trade/close-positions-at-market-price` |
| 2.6 | Reverse position | `/v1/perpum/positions/reverse` | Instantly reverses an existing perpetual position by closing it and opening the same size in the opposite direction. | POST | Private | api_key, sign, id | data | `https://www.coinw.com/api-doc/futures-trading/trade/reverse-a-position` |
| 2.7 | Adjust margin | `/v1/perpum/positions/margin` | Adjusts margin for an existing position (filled order) by increasing or decreasing margin amount. | POST | Private | api_key, sign, id, addMargin | msg | `https://www.coinw.com/api-doc/futures-trading/trade/adjust-margin` |
| 2.8 | Set TP/SL | `/v1/perpum/TPSL` | Sets take-profit (TP) and stop-loss (SL) for filled or unfilled orders. | POST | Private | api_key, sign, id, instrument, stopProfitPrice, stopLossPrice | msg | `https://www.coinw.com/api-doc/futures-trading/trade/set-stop-loss-take-profit` |
| 2.9 | Set trailing TP/SL | `/v1/perpum/moveTPSL` | Configures trailing TP/SL by callback rate. Applies to filled orders only. | POST | Private | api_key, sign, openId, callbackRate, quantity, quantityUnit | — | `https://www.coinw.com/api-doc/futures-trading/trade/set-trailing-stop-loss-take-profit` |
| 2.10 | Batch set TP/SL | `/v1/perpum/addTpsl` | Batch sets TP/SL for contract trading orders. | POST | Private | api_key, sign, id, instrument, stopLossPrice, stopProfitPrice, priceType, stopFrom, stopType, closePiece | msg | `https://www.coinw.com/api-doc/futures-trading/trade/set-stop-loss-take-profit-in-batches` |
| 2.11 | Batch update TP/SL | `/v1/perpum/updateTpsl` | Batch modifies TP/SL orders for contract trading. | POST | Private | api_key, sign, id, instrument, stopLossPrice, stopProfitPrice, priceType, stopFrom, stopType, closePiece | msg | `https://www.coinw.com/api-doc/futures-trading/trade/modify-stop-loss-take-profit-in-batches` |
| 2.12 | Modify order | `/v1/perpum/order` | Modifies an unfilled order. Some fields (for example margin and leverage) cannot be changed via this endpoint. | PUT | Private | api_key, sign, id, instrument, direction, leverage, quantityUnit, quantity, positionModel, positionType, openPrice, stopProfitPrice, stopLossPrice, triggerPrice, triggerType | originId, editId | `https://www.coinw.com/api-doc/futures-trading/trade/modify-an-order` |
| 2.13 | Cancel order | `/v1/perpum/order` | Cancels an unfilled order by order ID. | DELETE | Private | api_key, sign, id | msg | `https://www.coinw.com/api-doc/futures-trading/trade/cancel-an-order` |
| 2.14 | Cancel batch orders | `/v1/perpum/batchOrders` | Cancels multiple unfilled orders in batch. | DELETE | Private | api_key, sign, sourceIds | — | `https://www.coinw.com/api-doc/futures-trading/trade/cancel-batch-orders` |

### Query Orders

| No. | name | Endpoint | Description | Method | Authentication | Input Parameters | Output Parameters | Detailed Doc URL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3.1 | Get open orders | `/v1/perpum/orders/open` | Queries unfilled orders by instrument and order type, including direction, quantity, margin, leverage, fees, and timestamps. | GET | Private | api_key, sign, instrument, positionType | id, userId, baseSize, createdDate, currentPiece, direction, frozenFee, indexPrice, instrument, and 28 total fields | `https://www.coinw.com/api-doc/futures-trading/check/get-current-orders` |
| 3.2 | Get open order count | `/v1/perpum/orders/openQuantity` | Returns total number of unfilled (pending) orders. Pending order data is available via RESTful API only. | GET | Private | api_key, sign | data | `https://www.coinw.com/api-doc/futures-trading/check/get-pending-order-count` |
| 3.3 | Get TP/SL info | `/v1/perpum/TPSL` | Queries TP/SL information for both filled and unfilled contract orders. | GET | Private | api_key, sign, openId, stopFrom | currentPiece, closePiece, direction, createdDate, updatedDate, id, indexPrice, instrument, leverage, and 24 total fields | `https://www.coinw.com/api-doc/futures-trading/check/get-stop-loss-take-profit-information` |
| 3.4 | Get trailing TP/SL info | `/v1/perpum/moveTPSL` | Queries trailing TP/SL details for contract trading. | GET | Private | api_key, sign | baseSize, callbackRate, createdDate, currentPiece, direction, fee, instrument, leverage, margin, and 31 total fields | `https://www.coinw.com/api-doc/futures-trading/check/get-trailing-stop-loss-take-profit-information` |
| 3.5 | Get history orders (7 days) | `/v1/perpum/orders/history` | Returns historical order records from the last 7 days with pagination and filters. | GET | Private | api_key, sign, page, pageSize, originType, instrument | userId, baseSize, completeUsdt, createdDate, currentPiece, direction, entrustUsdt, havShortfall, hedgeId, and 37 total fields | `https://www.coinw.com/api-doc/futures-trading/check/get-historical-orders-7days` |
| 3.6 | Batch get history orders (7 days) | `/v1/perpum/orders/batchInsHistory` | Returns historical order records from the last 7 days with batch query via `symbols`. | GET | Private | api_key, sign, page, pageSize, originType, symbols | userId, baseSize, completeUsdt, createdDate, currentPiece, direction, entrustUsdt, havShortfall, hedgeId, and 37 total fields | `https://www.coinw.com/api-doc/futures-trading/check/get-batch-historical-orders-7days` |
| 3.7 | Get history orders (3 months) | `/v1/perpum/orders/archive` | Returns historical order records from the last 3 months with pagination and filters. | GET | Private | api_key, sign, page, pageSize, originType, instrument | userId, baseSize, completeUsdt, createdDate, currentPiece, direction, entrustUsdt, havShortfall, hedgeId, and 37 total fields | `https://www.coinw.com/api-doc/futures-trading/check/get-historical-orders-3months` |
| 3.8 | Batch get history orders (3 months) | `/v1/perpum/orders/batchInsArchive` | Returns historical order records from the last 3 months with batch query via `symbols`. | GET | Private | api_key, sign, page, pageSize, originType, symbols | userId, baseSize, completeUsdt, createdDate, currentPiece, direction, entrustUsdt, havShortfall, hedgeId, and 37 total fields | `https://www.coinw.com/api-doc/futures-trading/check/get-batch-historical-orders-3months` |
| 3.9 | Get order info | `/v1/perpum/order` | Returns current unfilled order information. You can query by order ID list; if no instrument/order IDs are specified, all orders under the given order type are returned. | GET | Private | api_key, sign, positionType, sourceIds | id, baseSize, contractType, userId, fee, createdDate, currentPiece, direction, frozenFee, and 35 total fields | `https://www.coinw.com/api-doc/futures-trading/check/get-order-information` |

### Position Information

| No. | name | Endpoint | Description | Method | Authentication | Input Parameters | Output Parameters | Detailed Doc URL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4.1 | Get current positions | `/v1/perpum/positions` | Queries currently open positions (filled orders) by instrument. You can also query specific positions using one or more position IDs. | GET | Private | api_key, sign, instrument | id, base, baseSize, createdDate, currentPiece, direction, fee, fundingSettle, indexPrice, and 37 total fields | `https://www.coinw.com/api-doc/futures-trading/position/get-current-position-information` |
| 4.2 | Get historical positions | `/v1/perpum/positions/history` | Queries all historical positions (filled orders), with optional filtering by base/instrument and position margin mode. | GET | Private | api_key, sign, instrument, positionModel | avgOpenPrice, completeUsdt, direction, entrustUsdt, fee, havShortfall, indexPrice, instrument, leverage, and 22 total fields | `https://www.coinw.com/api-doc/futures-trading/position/get-historical-position-information` |
| 4.3 | Get position margin rate | `/v1/perpum/positions/marginRate` | Queries margin rate for a position (filled order) by position ID. | GET | Private | api_key, sign, positionId | data | `https://www.coinw.com/api-doc/futures-trading/position/get-position-margin-rate` |
| 4.4 | Get max contract size | `/v1/perpum/orders/maxSize` | Queries max available contract size (long/short) by instrument, leverage, and position mode. Optional opening price can be provided. | GET | Private | api_key, sign, leverage, instrument, positionModel, orderPrice | maxBuy, maxSell | `https://www.coinw.com/api-doc/futures-trading/position/get-max-contract-size` |
| 4.5 | Get all current positions | `/v1/perpum/positions/all` | Queries all currently open positions (filled orders). | GET | Private | api_key, sign | id, base, baseSize, createdDate, currentPiece, closedPiece, direction, fee, fundingSettle, and 30 total fields | `https://www.coinw.com/api-doc/futures-trading/position/get-current-positions` |

### Account and Assets

| No. | name | Endpoint | Description | Method | Authentication | Input Parameters | Output Parameters | Detailed Doc URL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5.1 | Get max transferable balance | `/v1/perpum/account/available` | Queries max amount transferable out from the contract account. | GET | Private | api_key, sign | data.value | `https://www.coinw.com/api-doc/futures-trading/assets/get-max-transferable-balance` |
| 5.2 | Get deal details (3 days) | `/v1/perpum/orders/deals` | Deal/funding details for the recent 3 days (see api-doc notes). | GET | Private | api_key, sign, instrument, page, pageSize, originType, positionModel | data.rows, nextId, prevId, total | `https://www.coinw.com/api-doc/futures-trading/assets/get-transaction-details-3days` |
| 5.3 | Get deal details (3 months) | `/v1/perpum/orders/deals/history` | Deal/funding details for the recent 3 months (same fields as 5.2). | GET | Private | api_key, sign, instrument, page, pageSize, originType, positionModel | data.rows, nextId, prevId, total | `https://www.coinw.com/api-doc/futures-trading/assets/get-transaction-details-3months` |
| 5.4 | Get contract account assets | `/v1/perpum/account/getUserAssets` | Returns available margin, USDT, frozen amounts, almighty-gold, and related fields (note meaning of `availableMargin`). | GET | Private | api_key, sign | availableMargin, availableUsdt, alMargin, alFreeze, almightyGold, userId, time | `https://www.coinw.com/api-doc/futures-trading/assets/get-futures-account-assets` |
| 5.5 | Get contract account fees | `/v1/perpum/account/fees` | Queries maker/taker fee rates. | GET | Private | api_key, sign | makerFee, takerFee, userId | `https://www.coinw.com/api-doc/futures-trading/assets/get-futures-account-fees` |
| 5.6 | Get almighty-gold balance | `/v1/perpum/account/almightyGoldInfo` | Filters almighty-gold records by status and other criteria (GET). | GET | Private | api_key, sign, type, startTime?, endTime? | data[] (id, currentAmount, totalAmount, type, etc.) | `https://www.coinw.com/api-doc/futures-trading/assets/get-mega-coupon-balance` |
| 5.7 | Unit conversion | `/v1/perpum/pieceConvert` | Converts between contract pieces and coin amount. | POST | Private | api_key, sign, convertType, faceValue, dealPiece?/baseSize? | data.value | `https://www.coinw.com/api-doc/futures-trading/assets/coin-conversion` |
| 5.8 | Get position mode | `/v1/perpum/positions/type` | Queries isolated/cross mode and merged/split layout (GET). | GET | Private | api_key, sign | layout, positionModel | `https://www.coinw.com/api-doc/futures-trading/assets/get-margin-mode` |
| 5.9 | Set position mode | `/v1/perpum/positions/type` | Sets isolated/cross mode and layout (POST); there must be no open orders before switching. | POST | Private | api_key, sign, positionModel, layout | data (TRANSACTION_SUCCESS) | `https://www.coinw.com/api-doc/futures-trading/assets/set-margin-mode` |
| 5.10 | Enable/disable almighty-gold | `/v1/perpum/account/almightyGoldInfo` | Enables or disables almighty-gold (POST on same path as 5.6). | POST | Private | api_key, sign, status | code, msg | `https://www.coinw.com/api-doc/futures-trading/assets/enable-disable-mega-coupon` |
| 5.11 | Get user max available contract size | `/v1/perpum/orders/availSize` | Returns available buy/sell size from the filled-position perspective (different from 4.4 maxSize use case). | GET | Private | api_key, sign, instrument | availBuy, availSell | `https://www.coinw.com/api-doc/futures-trading/assets/get-max-users-contract-size` |

### General

| No. | name | Endpoint | Description | Method | Authentication | Input Parameters | Output Parameters | Detailed Doc URL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6.1 | Get leverage info | `/v1/perpum/positions/leverage` | Queries leverage for one filled position (`positionId`) or one unfilled order (`orderId`), choose one. | GET | Private | api_key, sign, positionId or orderId | data.value | `https://www.coinw.com/api-doc/futures-trading/common/get-leverage-information` |

## Common Parameters and Enums

### Auth and URL
- Base URL: `https://api.coinw.com`.
- Public market endpoints are mostly `GET https://api.coinw.com/v1/perpum/...` or `.../v1/perpumPublic/...`.
- Private endpoints require header-based auth: `api_key`, `timestamp`, `sign` (HMAC-SHA256 then Base64, see Reference).
### Common request fields
- **instrument** / **name**: contract identifier (often mixed in docs; means underlying/contract name).
- **symbols**: comma-separated list for batch endpoints.
- **direction** (`String`, required = `true`): trade direction, `long` (open long) or `short` (open short).
- **layout**: `0` merged positions, `1` split positions (used with **positionModel** on `/v1/perpum/positions/type` GET/POST).
- **convertType**: `1` piece -> coin, `2` coin -> piece (`pieceConvert`).
- **almighty-gold type (GET almightyGoldInfo)**: `0` pending to effective through `4` issuance failed; **status (POST)**: `1` on / `0` off.
### Standard response wrapper (common in REST)
- Common top-level fields: `code`, `msg` / `message`, `success`, `failed`, `data` (actual response varies by endpoint).
### Common enums and values
- **contractType**: common value `1`: USDT-margined perpetual contract (see api-doc).
- **positionModel**: position mode: `0` isolated, `1` cross (follow api-doc wording).
- **quantityUnit**: quantity unit for orders: 0 = quote currency (for example USDT); 1 = contract piece; 2 = base currency (for example BTC).
- **status**: contract status examples: `offline`, `online`, `pretest`, `settlement`, `preOffline`.
- **priceType**: TP/SL trigger price type: 1 = index price, 2 = last price, 3 = mark price.
- **processStatus**: matching-engine process status: 0 = waiting, 1 = processing, 2 = success, 3 = failed.
- **selected**: default selected status: 0 = no, 1 = yes.
- **stopType**: TP/SL order type: 1 = limit, 2 = market, 3 = planned order.
- **triggerStatus**: TP/SL trigger status: 0 = not triggered, 1 = triggered, 2 = canceled.
- **triggerType**: order type when `triggerPrice` condition is met: 0 = limit, 1 = market.


## Examples
### GET (public endpoint)
```bash
curl "https://api.coinw.com/v1/perpumPublic/tickers"
```
### Auth required (private endpoint)
```bash
timestamp=$(($(date +%s%N)/1000000))
method="DELETE"
api_url="/v1/perpum/allpositions"
payload="${timestamp}${method}${api_url}"
sign=$(printf "%s" "$payload" | openssl dgst -sha256 -hmac "$COINW_SECRET_KEY" -binary | openssl base64)
curl -X DELETE "https://api.coinw.com${api_url}" \
  -H "api_key: $COINW_API_KEY" \
  -H "timestamp: ${timestamp}" \
  -H "sign: ${sign}" \
  -H "Content-type: application/json"
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

* Ask for account name, api_key, secret_key
* Store the provided credentials in OpenClaw's secure credential store with masked display confirmation 

## Reference
- Authentication`./references/Authentication.md`
- errorcode: `./references/error-codes.md`
- notes: `./references/notes.md`
- api-key create steps: `./references/api-key-creation-steps.md`

