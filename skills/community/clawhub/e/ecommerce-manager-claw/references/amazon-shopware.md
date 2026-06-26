# Amazon SP-API Reference

Base URL: `https://sellingpartnerapi-na.amazon.com` (North America)
- EU: `https://sellingpartnerapi-eu.amazon.com`
- FE: `https://sellingpartnerapi-fe.amazon.com`

Auth: OAuth2 LWA (Login with Amazon). Exchange refresh token for access token first:

POST `https://api.amazon.com/auth/o2/token`
```json
{
  "grant_type": "refresh_token",
  "refresh_token": "{refresh_token}",
  "client_id": "{client_id}",
  "client_secret": "{client_secret}"
}
```

Use returned `access_token` in header: `x-amz-access-token: {access_token}`

---

## Inventory — Get FBA inventory

GET `/fba/inventory/v1/summaries?details=true&granularityType=Marketplace&granularityId={marketplace_id}&marketplaceIds={marketplace_id}`

## Inventory — Get listings inventory

GET `/listings/2021-08-01/items/{sellerId}/{sku}?marketplaceIds={marketplace_id}&includedData=summaries,attributes,issues,offers,fulfillmentAvailability`

---

## Orders — List orders

GET `/orders/v0/orders?MarketplaceIds={marketplace_id}&CreatedAfter=2024-01-01T00:00:00Z&MaxResultsPerPage=20`

Key fields: `AmazonOrderId`, `OrderStatus`, `PurchaseDate`, `OrderTotal`, `BuyerInfo`

## Orders — Get order items

GET `/orders/v0/orders/{orderId}/orderItems`

## Orders — Confirm shipment

POST `/orders/v0/orders/{orderId}/shipmentConfirmation`
```json
{
  "marketplaceId": "{marketplace_id}",
  "packageDetail": {
    "purchaseOrderNumber": "{orderId}",
    "packageReferenceId": "1",
    "carrierCode": "UPS",
    "trackingId": "TRACK123",
    "shipDate": "2024-01-15T10:00:00Z",
    "orderItems": [{ "orderItemId": "ITEM_ID", "quantity": 1 }]
  }
}
```

---

## Products — Get catalog item

GET `/catalog/2022-04-01/items/{asin}?marketplaceIds={marketplace_id}&includedData=summaries,images,productTypes`

## Products — Update listing price/quantity

PATCH `/listings/2021-08-01/items/{sellerId}/{sku}?marketplaceIds={marketplace_id}`
```json
{
  "productType": "PRODUCT",
  "patches": [
    { "op": "replace", "path": "/attributes/fulfillment_availability", "value": [{ "fulfillment_channel_code": "DEFAULT", "quantity": 50 }] }
  ]
}
```

---

## Customers

Amazon does not expose full customer PII via API. You can view buyer name and email (if shared) within order data. Direct customer management is not available through SP-API.

---

# Shopware API Reference

Base URL: `https://{store}/api/`
Auth: POST `/api/oauth/token` to get bearer token
```json
{ "client_id": "administration", "client_secret": "{secret}", "grant_type": "client_credentials" }
```

Header: `Authorization: Bearer {access_token}`

---

## Products — List

GET `/api/product?limit=50`

## Products — Create

POST `/api/product`
```json
{
  "name": "My Product", "productNumber": "SKU-001", "price": [{ "currencyId": "CURRENCY_ID", "gross": 29.99, "net": 25.0, "linked": false }],
  "stock": 100, "taxId": "TAX_ID"
}
```

## Products — Update

PATCH `/api/product/{id}`
```json
{ "stock": 75, "price": [{ "currencyId": "CURRENCY_ID", "gross": 39.99, "net": 33.6, "linked": false }] }
```

## Products — Delete

DELETE `/api/product/{id}`

---

## Orders — List

GET `/api/order?limit=20&sort=-orderDateTime`

## Orders — Update status

POST `/api/_action/order/{id}/state/{transition}`
Transitions: `process`, `complete`, `cancel`, `reopen`

---

## Customers — List

GET `/api/customer?limit=20`

## Customers — Search by email

GET `/api/customer?filter[email]=test@example.com`

## Customers — Update

PATCH `/api/customer/{id}`
```json
{ "firstName": "Jane", "lastName": "Doe" }
```

---

## Inventory

Shopware manages stock directly on the product (`stock` field). Update via PATCH `/api/product/{id}` with `{ "stock": 50 }`.
