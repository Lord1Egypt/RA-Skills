# Etsy API Reference

Base URL: `https://openapi.etsy.com/v3/`
Auth header: `x-api-key: {api_key}`, Bearer token for write operations

---

## Products (Listings) — Get listings

GET `/application/shops/{shop_id}/listings/active?limit=25`

Key fields: `listing_id`, `title`, `price`, `quantity`, `state`

## Products — Update listing

PATCH `/application/listings/{listing_id}`
```json
{ "title": "New Title", "price": 29.99, "quantity": 50 }
```

## Products — Create listing

POST `/application/shops/{shop_id}/listings`
```json
{
  "quantity": 10, "title": "My Product", "description": "Description",
  "price": 29.99, "who_made": "i_did", "when_made": "2020_2024",
  "taxonomy_id": 1, "shipping_profile_id": 12345
}
```

## Products — Delete listing

DELETE `/application/listings/{listing_id}`

---

## Orders — Get orders

GET `/application/shops/{shop_id}/receipts?limit=25`

## Orders — Mark order shipped

POST `/application/shops/{shop_id}/receipts/{receipt_id}/tracking`
```json
{ "tracking_code": "TRACK123", "carrier_name": "dhl", "send_bcc": true }
```

---

## Inventory — Update inventory

PUT `/application/listings/{listing_id}/inventory`
```json
{
  "products": [{ "property_values": [], "offerings": [{ "price": { "amount": 2999, "divisor": 100, "currency_code": "USD" }, "quantity": 50, "is_enabled": true }] }]
}
```

---

## Customers — Get buyer info (from order)

GET `/application/shops/{shop_id}/receipts/{receipt_id}` — buyer info is embedded in the receipt.
