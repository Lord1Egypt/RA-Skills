# ChainUp Margin Endpoints (OpenAPI V2)

Source:
- https://exchangedocsv2.gitbook.io/open-api-doc-v2/jian-ti-zhong-wen-v2/gang-gan-jiao-yi

Notes:
- The following are common margin trading endpoints. All require API-key authentication and signing.
- Signature headers: `X-CH-APIKEY`, `X-CH-TS`, `X-CH-SIGN`
- The example domain in the documentation is a placeholder: `https://openapi.xxx.xx`

## Margin Trade (Signed)

- `POST /sapi/v1/margin/order` create margin order
- `GET /sapi/v1/margin/order` query margin order
- `POST /sapi/v1/margin/cancel` cancel margin order
- `GET /sapi/v1/margin/openOrders` margin open orders
- `GET /sapi/v1/margin/myTrades` margin trade history

## Order Fields

Common fields for `POST /sapi/v1/margin/order`:
- `type`: `LIMIT` / `MARKET`
- `price`: required for `LIMIT`
- `newClientOrderId`: client order identifier (`<= 32`)
- `side`: `BUY` / `SELL`
- `volume`: order quantity
- `symbol`: for example `BTC/USDT`

Common query parameters for `GET /sapi/v1/margin/order`:
- `orderId`
- `newClientOrderId`
- `symbol`

Common fields for `POST /sapi/v1/margin/cancel`:
- `orderId`
- `newClientOrderId`
- `symbol`

## Practical Checklist

- Confirm whether the user wants spot or margin before sending anything, to avoid trading in the wrong market.
- Validate `symbol`, `volume`, and `price` precision/minimum constraints before placing the order.
- Require a second confirmation (`CONFIRM`) before any live trading action.
