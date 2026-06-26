---
name: cashapp-pay
version: 1.4.0
updated: 2026-03-04
description: "Cash App Pay integration skill. Accept payments via Cash App — the #1 personal finance app in the U.S. Covers the Network API, Customer Request API, Management API, Pay Kit SDK, sandbox testing, webhooks, and dispute handling."
homepage: https://developers.cash.app
api_base: https://api.cash.app
credentials: [CASHAPP_CLIENT_ID, CASHAPP_API_KEY]
metadata: {"openclaw":{"requires":{"env":["CASHAPP_CLIENT_ID","CASHAPP_API_KEY"]},"primaryEnv":"CASHAPP_API_KEY"}}
---

# Cash App Pay — Accept Payments from Cash App

Cash App Pay is a checkout solution by Block, Inc. that lets U.S. consumers pay
directly from their Cash App balance, linked bank account, or card. It eliminates
manual card entry and is optimized for mobile-first commerce.

Cash App is the **#1 personal finance app in the U.S.** by monthly active users.
Cash App Pay is available for e-commerce (web and mobile) and point-of-sale (POS)
integrations.

**Developer Docs:** [developers.cash.app](https://developers.cash.app)
**Production Base URL:** `https://api.cash.app`
**Sandbox Base URL:** `https://sandbox.api.cash.app`

---

## Architecture Overview

Cash App Pay integrations have two components:

```
┌─────────────────────────────────────────────────┐
│                   FRONT END                      │
│  Pay Kit SDK (Web / iOS / Android)               │
│  - Renders QR code (desktop) or redirect (mobile)│
│  - Handles customer authentication flow          │
│  - Uses Customer Request API under the hood      │
└───────────────────────┬─────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│                   BACK END                       │
│  Network API     — Payments, merchants, disputes │
│  Management API  — Credentials, webhooks, keys   │
│  Batch Reporting — Settlements, dispute reports   │
│  (All server-side only — never call from browser)│
└─────────────────────────────────────────────────┘
```

---

## APIs

### Customer Request API (Client-side)

Handles linking a customer to a merchant. This is what Pay Kit uses under the hood.
Can also be called directly for API-only integrations.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/customer-request/v1/requests` | Create a customer request |
| GET | `/customer-request/v1/requests/{id}` | Retrieve a customer request (poll for status) |

**Actions** (specify one or more per request):

| Action | Description |
|--------|-------------|
| `ONE_TIME_PAYMENT` | Single payment |
| `ON_FILE_PAYMENT` | Store payment method for future charges |
| `LINK_ACCOUNT` | Link customer's Cash App account |

**Channels** (specify exactly one):

| Channel | Use Case |
|---------|----------|
| `ONLINE` | E-commerce web checkout |
| `IN_APP` | Mobile app checkout |
| `IN_PERSON` | Point-of-sale devices |

**Authorization flow:**
1. Create a customer request → receive `auth_flow_triggers` (QR code URL, mobile URL, desktop URL)
2. Customer scans QR code (desktop) or is redirected to Cash App (mobile) to approve
3. Poll the request (1x/sec recommended) or use webhooks (`customer_request.state.updated`)
4. When state = `approved`, save the `grant_id` from the `grants` array
5. Use the `grant_id` to create a payment via the Network API

QR codes **rotate every 30 seconds** and **expire every 60 seconds** — always
fetch the latest from the polling response.

### Network API (Server-side)

Server-to-server API for core payment operations. All requests must be **signed**
(see Signatures section below).

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/network/v1/brands` | Create a brand |
| GET | `/network/v1/brands` | List brands |
| POST | `/network/v1/merchants` | Create a merchant under a brand |
| GET | `/network/v1/merchants/{id}` | Retrieve a merchant |
| POST | `/network/v1/payments` | Create a payment |
| GET | `/network/v1/payments/{id}` | Retrieve a payment |
| POST | `/network/v1/payments/{id}/void` | Void a payment |
| POST | `/network/v1/payments/{id}/capture` | Capture a payment |
| POST | `/network/v1/refunds` | Create a refund |
| GET | `/network/v1/refunds/{id}` | Retrieve a refund |
| POST | `/network/v1/refunds/{id}/void` | Void a refund |
| GET | `/network/v1/disputes` | List disputes |
| POST | `/network/v1/disputes/{id}/evidence` | Submit dispute evidence (text or file) |

**Required headers:**
- `Authorization: <api_creds>`
- `Content-Type: application/json`
- `Accept: application/json`
- `X-Region: PDX`
- `X-Signature: <signature>` (or `sandbox:skip-signature-check` in sandbox)

**Idempotency:** All write operations require an `idempotency_key` (UUID) in the
request body to prevent duplicate operations.

### Management API (Server-side)

Automates integration management:

- Secure credential rotation
- Webhook subscription management
- Creating scoped API keys (for microservices with least-privilege access)

---

## Quick Start — API Integration

### Step 1: Create a Brand and Merchant

```bash
# Create a brand
curl -X POST https://sandbox.api.cash.app/network/v1/brands \
  -H "Authorization: {{api_creds}}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "X-Region: PDX" \
  -d '{
    "brand": {
      "name": "My Store",
      "reference_id": "external-id"
    },
    "idempotency_key": "unique-uuid-here"
  }'

# Create a merchant under the brand
curl -X POST https://sandbox.api.cash.app/network/v1/merchants \
  -H "Authorization: {{api_creds}}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "X-Region: PDX" \
  -d '{
    "merchant": {
      "name": "My Store - Main",
      "brand_id": "BRAND_xxxxx",
      "address": {
        "address_line_1": "1 Market Street",
        "locality": "San Francisco",
        "administrative_district_level_1": "CA",
        "postal_code": "94105",
        "country": "US"
      },
      "country": "US",
      "currency": "USD",
      "category": "5500",
      "reference_id": "external-id"
    },
    "idempotency_key": "unique-uuid-here"
  }'
```

### Step 2: Create a Customer Request

```bash
curl -X POST https://sandbox.api.cash.app/customer-request/v1/requests \
  -H "Authorization: Client {{client_id}}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "request": {
      "actions": [
        {
          "type": "ONE_TIME_PAYMENT",
          "amount": 1234,
          "currency": "USD",
          "scope_id": "{{merchant_id}}"
        }
      ],
      "channel": "ONLINE",
      "reference_id": "order-12345"
    },
    "idempotency_key": "unique-uuid-here"
  }'
```

The response contains `auth_flow_triggers` with QR code URL, mobile URL, and
desktop URL. Poll the retrieve endpoint until `state` = `approved`, then save the
`grant_id`.

### Step 3: Create a Payment

```bash
curl -X POST https://sandbox.api.cash.app/network/v1/payments \
  -H "Authorization: {{api_creds}}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "X-Region: PDX" \
  -d '{
    "payment": {
      "amount": 1234,
      "currency": "USD",
      "merchant_id": "{{merchant_id}}",
      "grant_id": "{{grant_id}}",
      "capture": true,
      "reference_id": "order-12345"
    },
    "idempotency_key": "unique-uuid-here"
  }'
```

Set `"capture": false` for auth-only, then capture later via the capture endpoint.

---

## Pay Kit SDK (Front End)

Pay Kit is Cash App's JavaScript SDK for embedding payment UI. It handles the
Customer Request flow automatically.

| Platform | Resources |
|----------|-----------|
| **Web** | [Pay Kit Web Guide](https://developers.cash.app/cash-app-pay-partner-api/guides/pay-kit-sdk/pay-kit-web-overview/getting-started) |
| **iOS** | [Pay Kit iOS Guide](https://developers.cash.app/cash-app-pay-partner-api/guides/pay-kit-sdk/pay-kit-i-os) |
| **Android** | [Pay Kit Android Guide](https://developers.cash.app/cash-app-pay-partner-api/guides/pay-kit-sdk/pay-kit-android) |

Pay Kit adapts to the user's device:
- **Desktop** → Displays a QR code for scanning with Cash App
- **Mobile** → Redirects to Cash App for authentication, then back to merchant

For advanced control over when and how the authorization flow starts, use Pay Kit's
**advanced controls** mode.

---

## Webhooks

Subscribe to webhook events for real-time updates instead of polling.

| Event | Trigger |
|-------|---------|
| `customer_request.state.updated` | Customer request state changes (approved, declined, etc.) |

Webhook subscriptions are managed through the Management API. There is **no webhook
event for QR code rotation** — use polling or check the `refreshes_at` timestamp
to fetch the latest QR code.

---

## Sandbox

Cash App provides a full sandbox environment for testing without moving real money.

| Item | Value |
|------|-------|
| **Sandbox host** | `sandbox.api.cash.app` |
| **Sandbox App** | Available for testing customer approval flows |
| **Sandbox Web** | Web-based approval simulator |
| **Credentials** | Separate from production — obtain from Cash App Partner Engineering |
| **Signature bypass** | Set `X-Signature: sandbox:skip-signature-check` |
| **Backwards compatibility** | 5-year guarantee on sandbox magic values |

### Magic Values (Payment Amounts)

Use these amounts in the `amount` field to trigger specific outcomes:

| Amount | Result |
|--------|--------|
| `6670` | Connection error (HTTP error returned, payment still created) |
| `7770` | Decline: compliance failure |
| `7771` | Decline: insufficient funds |
| `7772` | Decline: other |
| `7773` | Decline: risk |
| `7774` | Decline: amount too large |
| `7775` | Decline: amount too small |
| `8801` | Creates payment + dispute (reason CD10) |
| `8802` | Creates payment + dispute (reason CD11) |
| `8803` | Creates payment + dispute (reason CD12) |
| `8804` | Creates payment + dispute (reason CD13) |
| `8811` | Creates payment + dispute (reason FR10 — fraud) |
| `8812` | Creates payment + dispute (reason FR11 — fraud) |
| `8821`–`8823` | Creates payment + dispute (PE10–PE12 — processing error) |
| `8901` | Creates payment + dispute with differing disputed amount |

### Magic Grant IDs

| Grant ID | Result |
|----------|--------|
| `GRG_sandbox:active` | Payment created successfully |
| `GRG_sandbox:consumed` | Decline: grant consumed |
| `GRG_sandbox:expired` | Decline: grant expired |
| `GRG_sandbox:missing` | Decline: grant not found |
| `GRG_sandbox:revoked` | Decline: grant revoked |

### Magic Merchant IDs

| Merchant ID | Result |
|-------------|--------|
| `MMI_sandbox:disabled` | Error: merchant disabled |
| `MMI_sandbox:pending` | Error: merchant pending |
| `MMI_sandbox:missing` | Error: merchant not found |

---

## Request Signatures

All Network API and Management API requests must be **signed** in production.
Signatures are provided via the `X-Signature` header.

In sandbox, bypass signing by setting:
```
X-Signature: sandbox:skip-signature-check
```

For production signing implementation details, see the
[Making Requests](https://developers.cash.app/cash-app-pay-partner-api/guides/technical-guides/api-fundamentals/requests/making-requests)
documentation.

---

## Settlements & Disputes

### Settlements

Cash App uses **net settlement** — refund and dispute amounts are deducted from
settlement payouts. Reconciliation reports are uploaded **daily** via SFTP to a
PSP-hosted server, regardless of whether there was payment activity.

### Disputes

Dispute reports are also uploaded daily via SFTP. Use the Network API's dispute
endpoints to retrieve dispute details and submit evidence (text or file-based).

**Dispute evidence magic values** (sandbox):

| Metadata Value | Result |
|----------------|--------|
| `{"sandbox:set_dispute_state": "PROCESSING"}` | Dispute moves to PROCESSING |
| `{"sandbox:set_dispute_state": "WON"}` | Dispute resolved — won |
| `{"sandbox:set_dispute_state": "PARTIALLY_WON"}` | Dispute resolved — partially won |
| `{"sandbox:set_dispute_state": "LOST"}` | Dispute resolved — lost |

---

## Integration Paths

| Path | Best For | Docs |
|------|----------|------|
| **Cash App Afterpay (Sellers)** | Merchants adding Cash App Pay or Afterpay to their checkout | [Seller Docs](https://developers.cash.app/cash-app-afterpay/guides/welcome/getting-started) |
| **Cash App Pay Partner API (PSPs)** | Payment service providers building platform-level integrations | [PSP Docs](https://developers.cash.app/cash-app-pay-partner-api/guides/welcome) |

---

## Resources

| Resource | URL |
|----------|-----|
| Developer Documentation | [developers.cash.app](https://developers.cash.app) |
| API Reference (Network) | [Network API Reference](https://developers.cash.app/cash-app-pay-partner-api/api-reference/network-api/list-brands) |
| Cash App Pay Status | [Status Page](https://developers.cash.app/cash-app-pay-partner-api/guides/resources/cash-app-pay-status) |
| Brand Assets | [Cash App Pay Assets](https://developers.cash.app/cash-app-pay-partner-api/guides/resources/cash-app-pay-assets) |
| Glossary | [Glossary of Terms](https://developers.cash.app/cash-app-pay-partner-api/guides/resources/glossary-of-terms) |
| Postman Collection | [Postman Collection](https://developers.cash.app/cash-app-pay-partner-api/guides/technical-guides/sandbox/postman-collection) |

---

## Important Notes

- **Cash App Pay is U.S. only.** Both merchants and customers must be in the United
  States. Currency is USD.
- **All Network/Management API requests must be signed in production.** Use the
  `X-Signature` header. In sandbox, set it to `sandbox:skip-signature-check`.
- **All write operations require an idempotency key.** Use a unique UUID for each
  request to prevent duplicate charges, refunds, or merchant registrations.
- **QR codes rotate every 30 seconds and expire every 60 seconds.** Always fetch
  the latest from polling responses. Do not cache QR code URLs.
- **Sandbox credentials are separate from production.** Never use production
  credentials in the sandbox or vice versa.
- **Partner onboarding requires approval.** Contact the Cash App Pay Partner
  Engineering team to confirm the right integration path and obtain API credentials.
- **Never expose API credentials client-side.** The Network API and Management API
  are server-side only. Only the Customer Request API and Pay Kit SDK are used on
  the client.
- **Cash App Pay is a product of Block, Inc.** (formerly Square, Inc.). It is not
  affiliated with CreditClaw.
