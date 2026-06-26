# Worked example: stock check

**Customer says:** "Stock check the Daily Shirt in olive, my size, online and at any store within 25 miles."

## 1. Resolve the item

From `profile.md`:
```yaml
gender: m
shirt: L
home_zip: 94110
favorites: [olive, indigo, navy, oat]
```

Search the Pima catalog (gender + name + color, one call):

```
GET /mcp/buckmason/products?gender=m&q=daily+shirt&color=olive&per_page=5
```

Response (truncated):

```json
{
  "products": [
    {
      "id": 101, "code": "DAILY-OLIVE-001", "slug": "daily-shirt-olive",
      "name": "Daily Shirt — Olive", "gender": "m",
      "category": "Tops", "color": "Olive",
      "price_cents": 9800, "price": "$98.00",
      "url": "https://www.buckmason.com/products/daily-shirt-olive",
      "image_url": "https://cdn.../daily-olive.jpg",
      "sizes": ["XS","S","M","L","XL","XXL"]
    }
  ]
}
```

If multiple `Daily Shirt` matches come back (Long Sleeve, Short Sleeve, Heavyweight…), present 2–3 with thumbnails and ask the customer to pick.

## 2. Get product detail with per-store stock

```
GET /mcp/buckmason/products/daily-shirt-olive?near_zip=94110&radius_mi=25
```

Response (truncated):

```json
{
  "id": 101, "slug": "daily-shirt-olive", "name": "Daily Shirt — Olive",
  "url": "https://www.buckmason.com/products/daily-shirt-olive",
  "online_in_stock": true, "nearby_in_stock": true,
  "variants": [
    {
      "sku": "DAILY-OLIVE-L", "size": "L",
      "shopify_variant_id": "gid://shopify/ProductVariant/9999",
      "online_count": 12,
      "locations": [
        { "id": 7, "name": "Hayes Valley", "distance_mi": 0.8,
          "pickup_enabled": true, "in_stock": true, "count": 4 },
        { "id": 8, "name": "Marina", "distance_mi": 2.4,
          "pickup_enabled": true, "in_stock": true, "count": 2 }
      ]
    }
  ]
}
```

## 3. Present

```
Daily Shirt — Olive — Size L
Online: ✓ in stock (12 available) — https://www.buckmason.com/products/daily-shirt-olive

Nearby stores (within 25 mi of 94110):
  ✓ Hayes Valley     0.8 mi  pickup ready (4 in stock)
  ✓ Marina           2.4 mi  pickup ready (2 in stock)
```

## 4. Optional: start MPP checkout

```
POST /mcp/buckmason/checkout
Content-Type: application/json

{
  "line_items": [{ "sku": "DAILY-OLIVE-L", "quantity": 1 }],
  "buyer": { "name": "...", "email": "...", "phone": "..." },
  "fulfillment_address": { "line1": "...", "city": "...", "state": "...", "postal_code": "...", "country": "US" }
}
```

Response:

```json
{
  "payment_required": true,
  "totals": { "charge_cents": 9800, "charge": "$98.00" },
  "payment_options": [{ "type": "shared_payment_token", "provider": "stripe" }]
}
```

Read the total back, request Link approval with `link-cli`, then re-POST with `Authorization: Payment <SPT>` and `acknowledged_total_cents`.

## Edge cases

- **Multiple "Daily Shirt" matches**: present 2–3 with thumbnails (`image_url`), ask the customer to pick. Don't guess.
- **Customer specifies a store by name** ("the Hayes Valley one"): you can skip the radius and read directly off the location list returned by `/mcp/buckmason/locations`.
- **Customer doesn't have a `home_zip` in profile**: ask once, save it, then proceed.
- **Variant out of stock everywhere**: list available sizes for the same color (from the `variants[]` array), then offer a restock notification:
  ```
  POST /api/restock_notifications
    product_code=DAILY-OLIVE-001
    size_name=L
    email=jane@example.com    # if guest
  ```
- **Color resolution failure** ("army green" but only "olive" exists): ask whether olive matches or list all colors from the `/mcp/buckmason/products?q=daily+shirt` results.
