---
name: creditclaw-encrypted-card
version: 2.5.0
updated: 2026-03-09
description: "Encrypted Card (Rail 5) — sub-agent checkout flow for CreditClaw bots."
companion_of: https://creditclaw.com/shopping/skill.md
api_base: https://creditclaw.com/api/v1
credentials: [CREDITCLAW_API_KEY]
---

# Encrypted Card (Rail 5)

> **This file is a companion to [skill.md](https://creditclaw.com/shopping/skill.md).**
> For registration, security details, webhooks, spending permissions, and the full API reference, see the main skill file.

Rail 5 lets your owner encrypt their real-world credit card and deliver it to you as a file.
You use a **sub-agent checkout flow** to decrypt the card for a single transaction, then the
sub-agent is deleted — decrypted card data never persists.

**Base URL:** `https://creditclaw.com/api/v1`

---

## Making a Purchase

This is the core transaction flow. When you need to buy something, you should **spawn an
ephemeral sub-agent** to handle the checkout. This keeps decrypted payment details isolated
from your main context and ensures sensitive data is automatically cleaned up after the
transaction completes.

### How It Works

```
1. You decide a purchase is needed (and it's within your spending rules)
2. You call POST /bot/rail5/checkout with the merchant and amount details
3. CreditClaw checks guardrails — if within limits, it approves immediately
   If above threshold, your owner gets an approval request (via dashboard or email)
4. Once approved, you spawn a sub-agent with the checkout_steps
5. The sub-agent calls POST /bot/rail5/key to get the one-time decryption key
6. The sub-agent decrypts the card file and completes checkout at the merchant
7. The sub-agent calls POST /bot/rail5/confirm with success or failure
8. The sub-agent is deleted — decrypted card data never persists
9. You announce the result to your human
```

**Why sub-agents?** The sub-agent pattern ensures that:
- Your main agent **never sees** the decrypted card details
- Card data exists only in the sub-agent's memory for the duration of one transaction
- The sub-agent is deleted after checkout — no data leaks across sessions
- If the sub-agent crashes, the decryption key is already consumed and cannot be reused

> **Alternative:** If your environment doesn't support spawning sub-agents, you can execute
> the `checkout_steps` directly as the main agent. The guardrails and encryption still protect
> your owner's card — but the main agent will see the decrypted card details in its context.

### Step 1: Request Checkout

```bash
curl -X POST https://creditclaw.com/api/v1/bot/rail5/checkout \
  -H "Authorization: Bearer $CREDITCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "merchant_name": "DigitalOcean",
    "merchant_url": "https://cloud.digitalocean.com/billing",
    "item_name": "Droplet hosting - 1 month",
    "amount_cents": 1200,
    "category": "cloud_compute"
  }'
```

**Request fields:**
| Field | Required | Description |
|-------|----------|-------------|
| `merchant_name` | Yes | Merchant name (1-200 chars) |
| `merchant_url` | Yes | Merchant website URL |
| `item_name` | Yes | What you're buying |
| `amount_cents` | Yes | Amount in cents (integer) |
| `category` | No | Spending category |

**Response (approved):**
```json
{
  "approved": true,
  "checkout_id": "r5chk_abc123",
  "checkout_steps": [
    "Call POST /api/v1/bot/rail5/key with { \"checkout_id\": \"r5chk_abc123\" } to get the decryption key.",
    "Run: node decrypt.js <key_hex> <iv_hex> <tag_hex> Card-ChaseD-9547.md",
    "Use the decrypted card details to complete checkout at DigitalOcean.",
    "Call POST /api/v1/bot/rail5/confirm with { \"checkout_id\": \"r5chk_abc123\", \"status\": \"success\" } when done.",
    "If checkout fails, call confirm with { \"status\": \"failed\" } instead.",
    "Announce the result."
  ],
  "spawn_payload": {
    "task": "You are a checkout agent...",
    "cleanup": "delete",
    "runTimeoutSeconds": 300,
    "label": "checkout-digitalocean"
  }
}
```

**Response (requires owner approval):**
```json
{
  "approved": false,
  "status": "pending_approval",
  "checkout_id": "r5chk_abc123",
  "message": "Amount exceeds auto-approve threshold. Your owner has been notified.",
  "expires_in_minutes": 15
}
```

### Checkout Status Polling

If you receive `pending_approval`, poll for the result:

```bash
curl "https://creditclaw.com/api/v1/bot/rail5/checkout/status?checkout_id=r5chk_abc123" \
  -H "Authorization: Bearer $CREDITCLAW_API_KEY"
```

Response:
```json
{
  "checkout_id": "r5chk_abc123",
  "status": "pending_approval",
  "merchant_name": "DigitalOcean",
  "item_name": "Droplet hosting - 1 month",
  "amount_cents": 1200,
  "key_delivered": false,
  "confirmed_at": null,
  "created_at": "2026-03-09T12:00:00.000Z"
}
```

**Status values:**
| Status | Meaning |
|--------|---------|
| `pending_approval` | Owner hasn't responded yet — poll again in 30 seconds |
| `approved` | Owner approved — proceed with spawning a sub-agent |
| `rejected` | Owner declined — do not proceed |
| `expired` | 15-minute approval window passed — try again if needed |
| `completed` | Checkout confirmed successful |
| `failed` | Checkout reported failure |

Your owner receives the approval request via their dashboard and email. Approvals expire after 15 minutes.

### Step 2: Spawn a Sub-Agent

Once the checkout is approved, spawn an ephemeral sub-agent using the `spawn_payload` from the response:

```
sessions_spawn({ task: spawn_payload.task, cleanup: "delete", runTimeoutSeconds: 300 })
```

The sub-agent executes the `checkout_steps` in sequence. You (the main agent) wait for
the sub-agent to complete and then announce the result.

### Step 3: Get Key (Sub-Agent Does This)

The sub-agent calls this endpoint to retrieve the one-time decryption key:

```bash
curl -X POST https://creditclaw.com/api/v1/bot/rail5/key \
  -H "Authorization: Bearer $CREDITCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "checkout_id": "r5chk_abc123" }'
```

**Response:** `{ "key_hex": "...", "iv_hex": "...", "tag_hex": "..." }`

**This key is single-use.** It cannot be retrieved again for this checkout. If the sub-agent
fails after retrieving the key, the checkout must be re-initiated.

### Step 4: Decrypt (Sub-Agent Does This)

The sub-agent runs the deterministic decrypt script that was delivered with the card file:

```
node decrypt.js <key_hex> <iv_hex> <tag_hex> Card-ChaseD-9547.md
```

This outputs the card JSON (number, CVV, expiry, name, billing address).

**Critical:** The sub-agent must **never** store, log, or persist the decrypted card data.
It exists only in memory for this single transaction. After checkout, the sub-agent is deleted.

### Step 5: Confirm (Sub-Agent Does This)

After completing (or failing) checkout at the merchant:

```bash
curl -X POST https://creditclaw.com/api/v1/bot/rail5/confirm \
  -H "Authorization: Bearer $CREDITCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "checkout_id": "r5chk_abc123", "status": "success" }'
```

Use `"status": "failed"` if checkout didn't work. On success, the transaction is recorded
in your owner's dashboard. After your first successful checkout, your card status moves
from `confirmed` to `active`.

---

## Encrypted Card File Delivery

When your owner sets up an encrypted card for you, CreditClaw delivers a single self-contained
file via the `rail5.card.delivered` event.

**Via webhook:** If you have a `callback_url`, the file is delivered automatically:
```json
{
  "event": "rail5.card.delivered",
  "bot_id": "bot_abc123",
  "data": {
    "card_id": "r5card_...",
    "card_name": "ChaseD",
    "card_last4": "9547",
    "file_content": "<self-contained markdown file with decrypt script and encrypted data>",
    "suggested_path": ".creditclaw/cards/Card-ChaseD-9547.md",
    "instructions": "Save this file to .creditclaw/cards/Card-ChaseD-9547.md — then confirm delivery via POST /bot/rail5/confirm-delivery"
  }
}
```

**Via bot messages (fallback):** If you don't have a webhook, check `GET /bot/messages` for
messages with `event_type: "rail5.card.delivered"`. The payload is identical. After saving the
file, acknowledge the message via `POST /bot/messages/ack`.

**Save the file** to `.creditclaw/cards/` (or the path in `suggested_path`). The file is
self-contained — it includes the decrypt script between `DECRYPT_SCRIPT_START/END` markers
and the encrypted data between `ENCRYPTED_CARD_START/END` markers.

Follow the `instructions` field in the message payload for next steps.

### Confirm Delivery

**After saving the file**, confirm delivery so your card status advances from `pending_delivery`
to `confirmed`:

```bash
curl -X POST https://creditclaw.com/api/v1/bot/rail5/confirm-delivery \
  -H "Authorization: Bearer $CREDITCLAW_API_KEY"
```

Response:
```json
{
  "status": "confirmed",
  "card_id": "r5card_...",
  "card_name": "ChaseD",
  "message": "Card confirmed. Complete a test purchase to verify your card works end-to-end.",
  "test_checkout_url": "https://creditclaw.com/pay/test_...",
  "test_instructions": "Navigate to the test checkout URL to complete a sandbox purchase.\nThis is a sandbox checkout — no real payment will be processed.\nUse the encrypted card file you just saved to decrypt and enter the card details.\nFill in all fields: card number, expiry, CVV, cardholder name, and billing address.\nSubmit the payment. The system will verify that the card details were decrypted correctly.\nThis proves your card file works end-to-end before any real purchase."
}
```

**Complete the test purchase** at the `test_checkout_url` to advance your card from `confirmed`
to `active`. This is a sandbox checkout — no real payment is processed. It verifies that your
card file decrypts correctly end-to-end before any real purchase.

**Pending messages for card deliveries expire after 24 hours.** If the message expires before
you retrieve it, your owner can re-stage the delivery from their dashboard.

**Recovery:** If you lose the file, your owner deletes the card and creates a new one
through the setup wizard. The file is re-delivered automatically.

---

## Card Status Progression

| Status | Meaning |
|--------|---------|
| `pending_delivery` | Key submitted, waiting for bot to confirm file delivery |
| `confirmed` | Bot confirmed file saved — ready for checkout |
| `active` | First successful checkout completed — proven working |
| `frozen` | Owner manually paused the card |

> Cards begin in `pending_setup` during owner configuration. Your bot first sees the card
> at `pending_delivery` when the encrypted file is delivered.

---

## Per-Rail Detail Check

For deeper operational info about your encrypted card — limits, approval threshold, and status:

```bash
curl https://creditclaw.com/api/v1/bot/check/rail5 \
  -H "Authorization: Bearer $CREDITCLAW_API_KEY"
```

Response:
```json
{
  "status": "active",
  "card_id": "r5_abc123",
  "card_name": "Shopping Card",
  "card_brand": "visa",
  "last4": "4532",
  "limits": {
    "per_transaction_usd": 50.00,
    "daily_usd": 100.00,
    "monthly_usd": 500.00,
    "human_approval_above_usd": 25.00
  }
}
```

Response (not connected): `{ "status": "inactive" }`

**Rate limit:** 6 requests per hour.
