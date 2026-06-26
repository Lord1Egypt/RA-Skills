# Wix API Reference

Base URL: `https://www.wixapis.com/`
Auth headers: `Authorization: {api_key}`, `wix-site-id: {site_id}`

---

## Products — List products

GET `stores/v1/products/query`
```json
{ "query": { "paging": { "limit": 50 } } }
```

## Products — Update product

PATCH `stores/v1/products/{productId}`
```json
{ "product": { "name": "New Name", "price": { "amount": "29.99" } } }
```

## Products — Create product

POST `stores/v1/products`
```json
{
  "product": {
    "name": "My Product",
    "productType": "physical",
    "price": { "amount": "29.99" },
    "stock": { "quantity": 100, "trackInventory": true }
  }
}
```

---

## Orders — List orders

GET `ecom/v1/orders/search`
```json
{ "search": { "paging": { "limit": 20 } } }
```

## Orders — Update fulfillment status

POST `ecom/v1/orders/{orderId}/fulfillments`
```json
{ "fulfillment": { "lineItems": [{ "id": "ITEM_ID", "quantity": 1 }], "status": "FULFILLED" } }
```

---

## Inventory — Get inventory

GET `stores/v1/inventoryItems/query`

## Inventory — Update

POST `stores/v1/inventoryItems/update`
```json
{
  "inventoryItem": {
    "externalId": "VARIANT_ID",
    "variants": [{ "variantId": "VARIANT_ID", "quantity": 50 }]
  }
}
```

---

## Customers — Get contacts

POST `contacts/v4/contacts/query`
```json
{ "query": { "filter": { "info.emails.email": { "$eq": "test@example.com" } } } }
```
