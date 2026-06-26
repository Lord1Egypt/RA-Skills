# Adobe Commerce (Magento) API Reference

Base URL: `https://{store}/rest/V1/`
Auth header: `Authorization: Bearer {access_token}`

---

## Products — List products

GET `/products?searchCriteria[pageSize]=50&searchCriteria[sortOrders][0][field]=created_at&searchCriteria[sortOrders][0][direction]=DESC`

## Products — Get single product

GET `/products/{sku}`

## Products — Create product

POST `/products`
```json
{
  "product": {
    "sku": "SKU-001", "name": "My Product", "price": 29.99,
    "status": 1, "type_id": "simple", "attribute_set_id": 4,
    "weight": 1,
    "extension_attributes": { "stock_item": { "qty": 100, "is_in_stock": true } }
  }
}
```

## Products — Update product

PUT `/products/{sku}`
```json
{ "product": { "price": 39.99 } }
```

## Products — Delete product

DELETE `/products/{sku}`

---

## Inventory — Get stock

GET `/stockItems/{sku}`

## Inventory — Update stock

PUT `/products/{sku}/stockItems/{itemId}`
```json
{ "stockItem": { "qty": 50, "is_in_stock": true } }
```

---

## Orders — List orders

GET `/orders?searchCriteria[pageSize]=20&searchCriteria[sortOrders][0][field]=created_at&searchCriteria[sortOrders][0][direction]=DESC`

## Orders — Update order status

POST `/orders/{id}/ship` — to create a shipment
POST `/orders/{id}/invoice` — to create an invoice
POST `/orders/{id}/cancel` — to cancel

---

## Customers — Search customers

GET `/customers/search?searchCriteria[filterGroups][0][filters][0][field]=email&searchCriteria[filterGroups][0][filters][0][value]=test@example.com`

## Customers — Update customer

PUT `/customers/{id}`
```json
{ "customer": { "id": 123, "firstname": "Jane", "lastname": "Doe", "email": "jane@example.com" } }
```
