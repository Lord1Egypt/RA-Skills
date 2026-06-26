# BigCommerce API Reference

Base URL: `https://api.bigcommerce.com/stores/{store_hash}/v3/`
Auth header: `X-Auth-Token: {access_token}`, `Content-Type: application/json`

---

## Inventory — Get products with stock

GET `/catalog/products?include=variants&limit=50`

Key fields: `id`, `name`, `sku`, `inventory_level`, `inventory_tracking`, `price`

## Inventory — Update stock

PUT `/catalog/products/{product_id}/variants/{variant_id}`
```json
{ "inventory_level": 50 }
```

---

## Orders — List orders

GET `/v2/orders?limit=20&sort=date_created:desc`

Key fields: `id`, `status`, `total_inc_tax`, `billing_address`, `date_created`

Status values: `0`=Incomplete, `1`=Pending, `2`=Shipped, `3`=Partially Shipped, `10`=Completed, `5`=Declined, `4`=Refunded

## Orders — Update order status

PUT `/v2/orders/{id}`
```json
{ "status_id": 2 }
```

---

## Products — Create

POST `/catalog/products`
```json
{
  "name": "My Product",
  "type": "physical",
  "price": 29.99,
  "weight": 1,
  "sku": "SKU-001",
  "inventory_level": 100,
  "description": "Description here"
}
```

## Products — Update

PUT `/catalog/products/{id}`
```json
{ "price": 39.99, "inventory_level": 75 }
```

## Products — Delete

DELETE `/catalog/products/{id}`

---

## Customers — Get customers

GET `/v2/customers?limit=20&email=test@example.com`

## Customers — Update

PUT `/v2/customers/{id}`
```json
{ "first_name": "Jane", "last_name": "Doe" }
```
