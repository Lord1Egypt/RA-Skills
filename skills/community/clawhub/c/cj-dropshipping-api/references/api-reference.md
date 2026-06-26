# CJ Dropshipping API Reference

This document contains the full list of CJ Dropshipping API endpoints, request/response schemas, and error codes.

## Authentication
- `GET /auth/token` – Retrieve OAuth token (handled via `accio-mcp-cli`).

## Product Endpoints
- `GET /api2.0/v1/product/getCategory` – Category tree.
- `GET /api2.0/v1/product/listV2` – Search products.
- `GET /api2.0/v1/product/query` – Product detail.
- `GET /api2.0/v1/product/variant/query` – All variants.
- `GET /api2.0/v1/product/variant/queryByVid` – Variant detail.
- `GET /api2.0/v1/product/stock/queryByVid` – Stock by variant ID.
- `GET /api2.0/v1/product/stock/queryBySku` – Stock by SKU.
- `GET /api2.0/v1/product/stock/getInventoryByPid` – Stock by product ID.
- `POST /api2.0/v1/product/addToMyProduct` – Add to My Products.
- `GET /api2.0/v1/product/myProduct/query` – Query My Products.
- `GET /api2.0/v1/product/productComments` – Product reviews.
- `POST /api2.0/v1/product/listed/listedByPids` – Batch listing.
- `POST /api2.0/v1/product/listed/getPlatformCategoryTree` – Platform categories.
- `POST /api2.0/v1/product/listed/queryVendors` – Vendors.
- `POST /api2.0/v1/product/listed/getCjDefaultDeliveryProfile` – Default delivery profile.
- `POST /api2.0/v1/product/listed/createDeliveryProfile` – Create delivery profile.
- `POST /api2.0/v1/product/listed/updateDeliveryProfile` – Update delivery profile.
- `POST /api2.0/v1/product/listed/removeDeliveryProfile` – Remove delivery profile.
- `POST /api2.0/v1/shop/location/queryList` – Shop locations.
- `POST /api2.0/v1/shop/property/queryCountries` – Countries & provinces.

## Order Endpoints
- `POST /api2.0/v1/shopping/order/createOrderV2` – Create order.
- `GET /api2.0/v1/shopping/order/list` – List orders.
- `POST /api2.0/v1/shopping/pay/payBalance` – Pay order balance.

## Logistics
- `POST /api2.0/v1/logistic/freightCalculate` – Freight calculator.
- `GET /api2.0/v1/logistic/trackInfo` – Track shipment.

## Webhooks
- `POST /api2.0/v1/webhook/set` – Configure webhooks.

## Settings
- `GET /api2.0/v1/setting/get` – Account settings.
- `POST /api2.0/v1/setting/setCallback` – Set webhook callbacks.

## Shop API (Partner Mode)
- `GET /shop/getShops` – List authorized shops.
- `POST /shop/getShops` – (alternative endpoint) Same as above.

## Error Codes
- `200` – Success.
- `1600100` – Parameter error.
- `1601000` – User not found.
- `500` – System error, retry later.
- `7001001` – Missing delivery profile (Shopify).
- `7001003` – Delivery profile lacks CJ location.

*All requests must include the header `CJ-Access-Token: <token>` obtained from `accio-mcp-cli`.*