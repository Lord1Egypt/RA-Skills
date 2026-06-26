# WooCommerce API Reference

Base URL: `https://{site}/wp-json/wc/v3/`
Auth: Basic Auth using Consumer Key (username) and Consumer Secret (password)

All requests use standard REST with JSON bodies.

---

## Inventory / Products — Get all products with stock

GET `/products?per_page=50&stock_status=instock`

Key fields in response: `id`, `name`, `sku`, `stock_quantity`, `stock_status`, `price`, `regular_price`

## Inventory — Update stock

PUT `/products/{id}`
```json
{ "stock_quantity": 50, "manage_stock": true }
```

---

## Orders — List recent orders

GET `/orders?per_page=20&orderby=date&order=desc`

Key fields: `id`, `status`, `total`, `billing.first_name`, `billing.email`, `line_items`, `date_created`

Order statuses: `pending`, `processing`, `on-hold`, `completed`, `cancelled`, `refunded`

## Orders — Update order status

PUT `/orders/{id}`
```json
{ "status": "completed" }
```

## Orders — Add note to order

POST `/orders/{id}/notes`
```json
{ "note": "Shipped via DHL, tracking: XYZ123", "customer_note": true }
```

---

## Products — Create product

POST `/products`
```json
{
  "name": "My Product",
  "type": "simple",
  "regular_price": "29.99",
  "description": "Full description here",
  "short_description": "Short blurb",
  "sku": "SKU-001",
  "manage_stock": true,
  "stock_quantity": 100,
  "categories": [{ "id": 9 }]
}
```

## Products — Update product

PUT `/products/{id}`
```json
{ "regular_price": "39.99", "stock_quantity": 75 }
```

## Products — Delete product

DELETE `/products/{id}?force=true`

---

## Customers — Get customers

GET `/customers?per_page=20&search=email@example.com`

Key fields: `id`, `first_name`, `last_name`, `email`, `orders_count`, `total_spent`, `billing`

## Customers — Update customer

PUT `/customers/{id}`
```json
{ "first_name": "Jane", "last_name": "Doe", "email": "jane@example.com" }
```

---

## Error handling

WooCommerce returns standard HTTP codes:
- `400` — Bad request (check your JSON)
- `401` — Invalid credentials
- `404` — Product/order not found
- `500` — Server error on the WordPress site

Display as: "I couldn't connect to your store. Please double-check your Consumer Key and Secret."
