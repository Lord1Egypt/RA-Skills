# Odoo `agent_api` endpoint surface

All endpoints are served by the Odoo `agent_api` addon, authenticated with the
`X-Agent-API-Key` header. Responses are JSON. The client unwraps a top-level
`{"success": true, "data": {...}}` envelope when present and raises on
`success: false` or non-2xx status.

Base URL = `ODOO_URL` (no trailing slash). All paths below are relative to it.

## Sales / eBay — `scripts/sales.py`

| Method | Path                                              | Action         |
| ------ | ------------------------------------------------- | -------------- |
| GET    | `/agent_api/v1/ebay/products`                     | `list-products` |
| GET    | `/agent_api/v1/ebay/inventory?skus=A,B`           | `inventory`    |
| POST   | `/agent_api/v1/ebay/orders`                       | `create-order` |
| GET    | `/agent_api/v1/ebay/orders/<odoo_order_id>/tracking` | `tracking`  |

### Product shape (from `list-products`)

```json
{
  "sku": "ABC-1", "title": "...", "description": "...", "brand": "...",
  "mpn": "...", "condition": "NEW", "category_id": "...",
  "images": ["https://..."], "aspects": {"Color": ["Navy"]},
  "cost": 12.50, "quantity": 7, "weight_oz": 6.0,
  "package_length_in": 0, "package_width_in": 0, "package_height_in": 0
}
```

### Order-create payload (POST body built by `create-order`)

The `create-order` action accepts an eBay order object and maps it to:

```json
{
  "ebay_order_id": "...", "ebay_legacy_order_id": "...", "creation_date": "...",
  "buyer_username": "...", "buyer_email": "...", "currency": "USD",
  "subtotal": 0.0, "tax": 0.0, "shipping": 0.0, "total": 0.0,
  "line_items": [
    {"line_item_id": "...", "sku": "...", "title": "...", "quantity": 1,
     "unit_price": 0.0, "line_total": 0.0, "tax": 0.0}
  ],
  "shipping_address": {"name": "...", "address_line_1": "...", "address_line_2": "...",
     "city": "...", "state": "...", "postal_code": "...", "country": "US",
     "phone": "...", "email": "..."},
  "billing_address": { ... }
}
```

Response: `{odoo_order_id, odoo_order_name, already_existed, confirmed,
partner_id, shipping_partner_id, invoice_partner_id, confirm_error}`.
`already_existed: true` ⇒ idempotent skip (Odoo already had this eBay order).

### Tracking response

`{"shipped": true|false, "tracking": {"carrier", "tracking_number",
"shipped_date"} | null}`. `tracking` is null until the order ships.

## Accounts Payable — `scripts/ap.py`

| Method | Path                                              | Action            |
| ------ | ------------------------------------------------- | ----------------- |
| GET    | `/agent_api/v1/ap/purchase_orders`                | `search-pos`      |
| GET    | `/agent_api/v1/ap/purchase_orders/<po_id>`        | `get-po`          |
| PUT    | `/agent_api/v1/ap/purchase_orders/<po_id>/lines`  | `update-po-lines` |
| POST   | `/agent_api/v1/ap/invoices`                       | `create-bill`     |
| GET    | `/agent_api/v1/ap/invoices/<bill_id>`             | `get-bill`        |
| GET    | `/agent_api/v1/ap/vendors`                        | `search-vendors`  |

- `search-pos` query params: `search`, `vendor`, `state`, `limit`.
- `update-po-lines` body: `{"lines": [{"line_id", "price_unit"}],
  "freight_cost"?, "fees_cost"?}`.
- `create-bill` body: `{"po_id", "vendor_bill_number"?, "invoice_date"?,
  "line_ids"?, "reviewer_user_id"?, "review_note"?, "expected_total"?,
  "tolerance"?}`. The bill is created in **draft**; Odoo's create() override
  auto-adds buying-group fee lines, a freight line (if `freight_cost > 0`), a
  misc-fees line (if `fees_cost > 0`), and partner-level purchase fee lines.

## Production scheduling — `scripts/production.py`

| Method | Path                                                   | Action               |
| ------ | ------------------------------------------------------ | -------------------- |
| GET    | `/agent_api/v1/production/overview`                    | `overview`           |
| GET    | `/agent_api/v1/production/batches`                     | `list-batches`       |
| GET    | `/agent_api/v1/production/batches/<id>`                | `get-batch`          |
| PUT    | `/agent_api/v1/production/batches/<id>/schedule`       | `schedule`           |
| POST   | `/agent_api/v1/production/batches/<id>/plan`           | `plan`               |
| POST   | `/agent_api/v1/production/batches/bulk_schedule`       | `bulk-schedule`      |
| GET    | `/agent_api/v1/production/workcenters`                 | `list-workcenters`   |
| GET    | `/agent_api/v1/production/workcenters/<id>`            | `get-workcenter`     |
| GET    | `/agent_api/v1/production/production_centers`          | `production-centers` |
| GET    | `/agent_api/v1/production/decoration_methods`          | `decoration-methods` |

See [`production_scheduling.md`](production_scheduling.md) for the data model
and field semantics.
