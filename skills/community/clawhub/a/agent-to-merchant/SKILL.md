---
name: synapseai-merchant
description: SynapseAI Merchant — AI agent payment receiving layer. Register as merchant, create wallets, generate payment links & QR codes, receive on-chain payments, and manage receiving status.
homepage: https://wallet.synapseai.pro
metadata: {"clawdbot":{"emoji":"🏪","requires":{"services":["supabase"]}}}
---

# SynapseAI Merchant

Give your AI agent the ability to **receive payments** via dedicated merchant wallets, shareable payment links, and QR codes.

## Authentication

All requests use Bearer token (same token from wallet registration):

```
Authorization: Bearer <registration_token>
```

## URLs

| Service | URL |
|---------|-----|
| Merchant API | `https://wallet.synapseai.pro/api/merchant` |
| Agent Toggle | `https://wallet.synapseai.pro/api/agent/{agentId}/toggle` |

## Flow

```
1. Register Merchant     → POST /register          → merchant_enabled = true + first wallet created
2. Create More Wallets   → POST /wallet/create      → additional receiving addresses
3. Create Payment Link   → POST /payment/link       → shareable payment URL
4. Share Link / QR       → Customer pays via /pay/{id} page
5. Receive Webhook       → POST /webhook            → get notified on payment.success
6. Query Payments        → GET  /wallets            → check incoming payments
7. Disable/Enable        → POST /agent/{id}/toggle  → pause or resume receiving
```

## Commands

### Register as merchant (Bearer token) — One-time

Enable merchant capability for the agent. This sets `merchant_enabled = true` on the agent record and auto-creates the first merchant wallet.

**This is a one-time action.** Once registered, the agent is a merchant permanently (until disabled via toggle).

```http
POST {MERCHANT_URL}/register
Authorization: Bearer <registration_token>
{
  "agent_id": "agt_abc123",
  "label": "My SaaS API Store",
  "network": "TRON",
  "currency": "USDT"
}
```

Response:

```json
{
  "merchant_enabled": true,
  "wallet": {
    "id": "mw_7f8a9b0c1d2e",
    "address": "T1A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P7",
    "network": "TRON",
    "label": "My SaaS API Store",
    "currency": "USDT"
  }
}
```

If already registered, returns `409 Conflict`.

### Toggle merchant receiving (Bearer token)

Pause or resume merchant receiving capability. When disabled:
- Payment pages return `403 "Merchant is not accepting payments"`
- Webhooks stop firing
- Existing data (wallets, links, history) is preserved

```http
POST {AGENT_TOGGLE_URL}/{agentId}/toggle
Authorization: Bearer <registration_token>
{
  "merchant_enabled": false
}
```

Response: updated agent object with `merchant_enabled` field.

> **Note**: You can also toggle agent spending status by passing `{ "status": "DISABLED" }` in the same endpoint. Both fields can be toggled independently.

### Create merchant wallet (Bearer token)

Each merchant wallet is an independent receiving address. One agent can have multiple merchant wallets for different purposes (e.g. one per product, one per client).

```http
POST {MERCHANT_URL}/wallet/create
Authorization: Bearer <registration_token>
{
  "agent_id": "agt_abc123",
  "label": "My SaaS API Store",
  "network": "TRON",
  "currency": "USDT"
}
```

Response:

```json
{
  "wallet_id": "mw_7f8a9b0c1d2e",
  "address": "T1A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P7",
  "network": "TRON",
  "label": "My SaaS API Store"
}
```

Supported networks: `TRON`, `BASE`, `ETHEREUM`, `SOLANA`
Supported currencies: `USDT`, `USDC`

### Create payment link (Bearer token)

Generate a shareable payment URL that customers can visit to pay. Each link has a unique URL at `https://wallet.synapseai.pro/pay/{id}`.

```http
POST {MERCHANT_URL}/payment/link
Authorization: Bearer <registration_token>
{
  "merchant_wallet_id": "mw_7f8a9b0c1d2e",
  "agent_id": "agt_abc123",
  "amount": 10.0,
  "currency": "USDT",
  "description": "Premium API Access - 30 days"
}
```

Response:

```json
{
  "id": "pl_3e4f5a6b7c8d",
  "payment_url": "https://wallet.synapseai.pro/pay/pl_3e4f5a6b7c8d",
  "qr_code_url": null,
  "amount": 10.0,
  "currency": "USDT"
}
```

Share the `payment_url` with your customer. They will see a branded payment page with QR code and wallet address.

### Configure webhook (Bearer token)

Receive HTTP notifications when payments are confirmed.

```http
POST {MERCHANT_URL}/webhook
Authorization: Bearer <registration_token>
{
  "agent_id": "agt_abc123",
  "url": "https://your-api.com/payment-callback",
  "events": ["payment.success"]
}
```

Response:

```json
{
  "id": "wh_9a0b1c2d3e4f",
  "url": "https://your-api.com/payment-callback",
  "events": ["payment.success"],
  "secret": "whsec_a1b2c3d4e5f6g7h8i9j0...",
  "active": true
}
```

Available events: `payment.success`, `payment.failed`, `payment.pending`

Keep the `secret` safe — use it to verify webhook signatures.

### Query merchant data (Bearer token)

Fetch all merchant wallets, payment links, incoming payments, and ledger entries.

```http
GET {MERCHANT_URL}/wallets?agent_id=agt_abc123
Authorization: Bearer <registration_token>
```

```json
{
  "merchantWallets": [...],
  "paymentLinks": [...],
  "payments": [...],
  "ledger": [...],
  "webhooks": [...]
}
```

### Get payment link info (public, no auth)

Fetch public info about a payment link. Used by the payment page.

Returns `403` if the owning agent has `merchant_enabled = false`.

```http
GET {MERCHANT_URL}/payment/{payId}
```

```json
{
  "id": "pl_3e4f5a6b7c8d",
  "amount": 10.0,
  "currency": "USDT",
  "description": "Premium API Access - 30 days",
  "status": "ACTIVE",
  "merchant_label": "My SaaS API Store",
  "merchant_address": "T1A2B3C4D5...",
  "network": "TRON"
}
```

## Webhook payload

When a payment is confirmed, your webhook URL receives:

```json
{
  "event": "payment.success",
  "payment": {
    "id": "pay_x1y2z3",
    "merchant_wallet_id": "mw_7f8a9b0c1d2e",
    "payment_link_id": "pl_3e4f5a6b7c8d",
    "tx_hash": "0x...",
    "amount": 10.0,
    "currency": "USDT",
    "payer": "0x...",
    "status": "CONFIRMED",
    "confirmations": 6,
    "created_at": "2026-03-15T..."
  }
}
```

## Typical agent flow

```
1. Register as merchant  → POST /register
2. Agent receives customer request
   → Create payment link with amount + description
   → Return payment_url to customer
   → Wait for payment.success webhook
   → Deliver product/service to customer
3. If agent goes offline  → POST /agent/{id}/toggle { merchant_enabled: false }
   → All payment pages show "not accepting payments"
4. When agent returns     → POST /agent/{id}/toggle { merchant_enabled: true }
```

## Error handling

All errors return `{"error": "..."}` with appropriate HTTP status:

| Code | Meaning |
|------|---------|
| 400  | Bad request (missing fields, invalid amount) |
| 401  | Missing or invalid Bearer token |
| 403  | Merchant is disabled (`merchant_enabled = false`) |
| 404  | Wallet or payment link not found |
| 409  | Already registered as merchant |
| 500  | Server error |

## Architecture

```
AI Agent (Merchant)
  └── Agent API
        ├── /merchant/register      ← one-time merchant activation
        ├── /merchant/wallet/create  ← create receiving wallet
        ├── /merchant/payment/link   ← create payment link
        ├── /merchant/payment/{id}   ← public payment info (403 if disabled)
        ├── /merchant/wallets        ← query all merchant data
        ├── /merchant/webhook        ← configure notifications
        └── /agent/{id}/toggle       ← enable/disable merchant + agent
              ↓
        Payment Page (/pay/{id})
              ↓
        Customer pays → On-chain TX
              ↓
        Webhook → Agent notified → Delivers service
```

## Database

Merchant status is persisted as `merchant_enabled` boolean on the `aiwallet_agents` table. This is the single source of truth for whether an agent can receive payments.

## Notes

- **Registration is one-time** — once registered, the agent is a merchant permanently (until disabled).
- **Disabling is reversible** — toggle `merchant_enabled` to pause/resume without losing data.
- Each merchant wallet is a separate address — use different wallets for different products or clients.
- Payment links are shareable URLs with QR codes — customers don't need a crypto wallet app to see the details.
- Always verify webhook signatures using the `secret` returned during webhook creation.
- Payment links can expire — set `expires_at` if you want time-limited offers.
- Use clear `description` strings — customers see these on the payment page.
- The merchant receiving feature is integrated into the wallet dashboard — Enable Merchant in the header, manage wallets and links inline.
