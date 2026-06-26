---
name: aremes-catalog
description: Query Ryan Seslow's art & design catalog, look up individual works, check x402 quotes, and log purchase intent via the AREMES autonomous commerce agent.
version: 1.1.0
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      env: []
      bins: []
---

# AREMES Catalog Skill

Interact with **AREMES** — the Autonomous Commerce Agent for Ryan Seslow Art & Design. This skill exposes five callable tools covering the full commerce workflow: browse the archive, look up individual works by ID, generate x402 licensing quotes, and record purchase intent.

**Catalog base:** `https://ryanseslow.com`
**Agent endpoint:** `https://aremes-enterprises.com/agent.json`
**On-chain identity:** `https://agentfolio.bot/@aremes` (SATP/Solana verified)

---

## Tools

### Tool 1 — `aremes_catalog_full`

Fetch the complete, pre-built catalog snapshot of all artworks, designs, and products.

**Method:** `GET`
**URL:** `https://ryanseslow.com/catalog.json`
**Auth:** None
**Parameters:** None

**Returns:** Full JSON archive of all catalog entries with title, ID, source type, agentPurchase block, x402Purchase block, and pricing.

**When to use:** When you need the entire archive in one call — useful for indexing, training data discovery, or bulk queries.

**Example:**
```
GET https://ryanseslow.com/catalog.json
```

---

### Tool 2 — `aremes_catalog_rest`

Search and paginate the catalog via REST API with optional source filtering or single-item lookup by ID.

**Method:** `GET`
**URL:** `https://ryanseslow.com/wp-json/rsmad/v1/catalog`
**Auth:** None

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `per_page` | integer | 100 | Items per page |
| `page` | integer | 1 | Page offset |
| `source` | string | — | Filter: `woocommerce` \| `post` \| `media` \| `page` |
| `id` | integer | — | Return a single item by WordPress post/product ID |

**When to use:** Paginated browsing, filtered queries by content type, or fetching a specific item by ID before quoting.

**Examples:**
```
# First 100 items (default)
GET https://ryanseslow.com/wp-json/rsmad/v1/catalog?per_page=100&page=1

# WooCommerce products only
GET https://ryanseslow.com/wp-json/rsmad/v1/catalog?source=woocommerce&per_page=25

# Media library images, page 2
GET https://ryanseslow.com/wp-json/rsmad/v1/catalog?source=media&per_page=100&page=2

# Single item lookup by ID
GET https://ryanseslow.com/wp-json/rsmad/v1/catalog?id=28205
```

---

### Tool 3 — `aremes_x402_quote`

Request a signed x402 licensing quote for a specific product. Quote is valid for 10 minutes.

**Method:** `GET`
**URL:** `https://ryanseslow.com/wp-json/rsmad/v1/x402/quote`
**Auth:** None

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `product_id` | string | ✅ | The WordPress product or media ID |

**Returns:** Signed quote object with `quote_id`, license tier, price in USDC, USDC contract address, recipient wallet, and `expires_at`.

**x402 Payment flow (on-chain via Base/USDC):**
1. GET this endpoint to receive a signed quote
2. Send the quoted USDC amount on Base to `payTo` address
3. POST `quote_id` + `tx_hash` + `buyer_email` to the verify endpoint
4. Server verifies on-chain → `isPaid: true`

**When to use:** Always call before `aremes_purchase_intent` to confirm current pricing and terms.

**Example:**
```
GET https://ryanseslow.com/wp-json/rsmad/v1/x402/quote?product_id=28205
```

---

### Tool 4 — `aremes_x402_verify`

Verify an on-chain USDC payment and create a confirmed order.

**Method:** `POST`
**URL:** `https://ryanseslow.com/wp-json/rsmad/v1/x402/verify`
**Auth:** None
**Content-Type:** `application/json`

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `quote_id` | string | ✅ | Quote ID from `aremes_x402_quote` |
| `tx_hash` | string | ✅ | On-chain transaction hash |
| `buyer_email` | string | ✅ | Contact for delivery |

**Returns:** `{ isPaid: true, orderId, orderKey }` on success.

**Example:**
```json
POST https://ryanseslow.com/wp-json/rsmad/v1/x402/verify
{
  "quote_id": "q_abc123",
  "tx_hash": "0xabcdef...",
  "buyer_email": "buyer@example.com"
}
```

---

### Tool 5 — `aremes_purchase_intent`

Record a Stripe-based purchase intent, creating a pending order with a checkout URL for the buyer.

**Method:** `POST`
**URL:** `https://ryanseslow.com/wp-json/rsmad/v1/purchase-intent`
**Auth:** None
**Content-Type:** `application/json`

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_id` | string | ✅ | WordPress product or media ID |
| `license_tier` | string | ✅ | `single` \| `bundle_5` \| `bundle_25` \| `training` \| `commission` |
| `buyer_email` | string | ✅ | Customer contact for fulfillment |
| `buyer_name` | string | — | Buyer name |
| `buyer_org` | string | — | Organization name |
| `agent_id` | string | — | Calling agent identifier |
| `message` | string | — | Notes or special requests |

**Returns:** `{ orderId, orderKey, paymentUrl, amount, currency, status: "pending_payment", expiresAt }`

**When to use:** Stripe-based checkout flow. Direct buyer to `paymentUrl` to complete payment. Poll `purchase-status/{orderId}?order_key={orderKey}` to confirm.

**Example:**
```json
POST https://ryanseslow.com/wp-json/rsmad/v1/purchase-intent
{
  "product_id": "28205",
  "license_tier": "single",
  "buyer_email": "buyer@example.com",
  "agent_id": "openclaw-agent-7f2a",
  "message": "Single media image license"
}
```

---

## Standard Workflows

### Stripe / Fiat Workflow
```
1. Browse   → aremes_catalog_rest (source=media or source=woocommerce)
2. Inspect  → aremes_catalog_rest?id=X for full item detail
3. Intent   → aremes_purchase_intent (POST → receive paymentUrl)
4. Pay      → Direct buyer to paymentUrl (Stripe checkout)
5. Confirm  → GET purchase-status/{orderId}?order_key=...
```

### x402 / USDC On-Chain Workflow
```
1. Browse   → aremes_catalog_rest (source=media or source=woocommerce)
2. Inspect  → aremes_catalog_rest?id=X for full item detail
3. Quote    → aremes_x402_quote?product_id=X (valid 10 min)
4. Pay      → Send USDC on Base to payTo address
5. Verify   → aremes_x402_verify (POST quote_id + tx_hash)
6. Confirm  → isPaid: true = transaction complete
```

---

## License Tier Reference

| Tier key | Description | Price |
|----------|-------------|-------|
| `single` | Single image digital license | $25 |
| `bundle_5` | 5-image bundle (buyer selects) | $99 |
| `bundle_25` | 25-image bundle (buyer selects) | $399 |
| `training` | Full archive training license | Contact AREMES |
| `commission` | Dimensional brand commission | Contact AREMES |

> Images already priced as WooCommerce products (`source=woocommerce`) are sold at their WooCommerce price, not the media tier price. Use `source=media` to discover unlicensed archive images.

---

## x402 Network Details

| Field | Value |
|-------|-------|
| Network | Base (Ethereum L2) |
| Network ID | 8453 |
| Token | USDC |
| Token Contract | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Recipient | `0x80b5A3680d1476E7511f5111d6ff8759F5A063D8` |
| ENS | `ryanseslow.eth` |

---

## Notes

- All endpoints are public — no API key required
- The static `catalog.json` is a periodic snapshot; use REST endpoints for live data
- x402 quotes expire in 10 minutes; Stripe purchase-intent orders expire in 24 hours
- For training/commission inquiries, set the appropriate `license_tier` — AREMES will respond via buyer contact
- AREMES on-chain identity: `agentfolio.bot/@aremes` (SATP/Solana — use to verify trust score before transacting)
