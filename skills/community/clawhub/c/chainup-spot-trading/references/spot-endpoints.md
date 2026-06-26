# ChainUp Spot Endpoints (OpenAPI V2)

Source:
- https://exchangedocsv2.gitbook.io/open-api-doc-v2/jian-ti-zhong-wen-v2/bi-bi-jiao-yi

Notes:
- The following are common spot endpoints. Treat the live gateway behavior as the final authority for paths and authentication rules.
- The example domain in the documentation is a placeholder: `https://openapi.xxx.xx`

## Public

- `GET /sapi/v2/ping` connectivity test
- `GET /sapi/v2/time` server time
- `GET /sapi/v2/symbols` symbols plus precision/minimum-order constraints
- `GET /sapi/v2/depth` order book
- `GET /sapi/v2/ticker` 24h ticker
- `GET /sapi/v2/trades` recent trades
- `GET /sapi/v2/klines` candlesticks

## Trade (Signed)

- `POST /sapi/v2/order` create order
- `POST /sapi/v2/order/test` test order
- `POST /sapi/v2/batchOrders` batch create orders (max 10)
- `GET /sapi/v2/order` query order
- `POST /sapi/v2/cancel` cancel order
- `POST /sapi/v2/batchCancel` batch cancel orders (max 10)
- `GET /sapi/v2/openOrders` open orders
- `GET /sapi/v2/myTrades` trade history

## Account (Signed)

- `GET /sapi/v1/account` spot account balances
- Recommended practical output: filter `balances` to non-zero assets (`free != 0` or `locked != 0`) by default, and return full `balances` only when the user needs reconciliation
- `POST /sapi/v1/asset/transfer` account transfer
- `POST /sapi/v1/asset/transferQuery` transfer history

## Order Fields

Common fields for `POST /sapi/v2/order`:
- `symbol` for example `BTC/USDT` (some implementations also support `BTCUSDT`)
- `volume` order quantity; the meaning for `MARKET` orders depends on side
- `side` `BUY` / `SELL`
- `type` `LIMIT` / `MARKET` / `FOK` / `POST_ONLY` / `IOC` / `STOP`
- `price` required for `LIMIT`
- `triggerPrice` for `STOP`-related orders
- `recvwindow` optional
- `newClientOrderId` optional

Observed behavior:
- On the current Coobit gateway, when `type=MARKET` and `side=BUY`, `volume` means quote quantity.
- For example, for `ETH/USDT`, `volume=1` with `side=BUY` means buying ETH at market using `1 USDT`.
- On the current Coobit gateway, when `type=MARKET` and `side=SELL`, `volume` means base quantity.
- For example, for `ETH/USDT`, `volume=0.1` with `side=SELL` means selling `0.1 ETH` at market.
- For non-market orders such as `LIMIT`, `volume` is still interpreted as the base asset quantity.

## Practical Checklist

Before sending a trading request:
- Fetch `pricePrecision`, `quantityPrecision`, and minimum-order constraints from `/sapi/v2/symbols`.
- Truncate `price` and `volume` to the allowed precision.
- For live mainnet trading, require the user to reply with `CONFIRM` first.

Default follow-up after order placement:
- After `POST /sapi/v2/order` succeeds, call `GET /sapi/v2/order` immediately.
- Prefer `symbol` and `orderId` from the order receipt for the follow-up query.
- Return order details to the user by default instead of stopping at the order receipt.
