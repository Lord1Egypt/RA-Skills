---
name: creditclaw-openclaw-checkout
version: 3.0.0
updated: 2026-03-24
description: "OpenClaw plugin checkout flow — main agent fills the form, CreditClaw plugin handles card fields."
companion_of: SKILL.md
api_base: https://creditclaw.com/api/v1
credentials: [CREDITCLAW_API_KEY]
requires_plugin: creditclaw-openclaw
---

# OpenClaw — Plugin Checkout Flow

> **Companion to `SKILL.md`.**
> For registration, card setup, spending permissions, and the full API reference, see the main skill file.

On OpenClaw, the **main agent** handles the entire checkout — browsing, cart, shipping, billing,
expiry date — everything except the card number and CVV. Those two fields are filled by the
**CreditClaw plugin** (`creditclaw_fill_card`), which decrypts the card internally and types
the values into the browser. The main agent never sees decrypted card details.

**Security:** The plugin pattern ensures:
- Your main agent **never sees** decrypted card details — they exist only inside the plugin
- Card data never appears in any agent's reasoning trace or context window
- The plugin zeros card data from memory immediately after filling
- Decryption keys are single-use and server-issued — consumed on first retrieval
- Server-side guardrails still enforce all spending limits regardless of what happens client-side

> **No plugin?** If the CreditClaw plugin is not installed, use the legacy sub-agent flow
> documented in `agents/OPENCLAW_legacy.md`.

---

## Purchase Flow

```
Main Agent:
  1. Browse, shop, add to cart (SHOPPING-GUIDE.md)
  2. Fill shipping, billing, contact info, expiry date — everything except card number and CVV
  3. Confirm all fields, identify if card inputs are in an iframe
  4. Call POST /bot/rail5/checkout for approval; wait if pending
  5. Call creditclaw_fill_card (plugin fills card number and CVV)
  6. Click submit, detect success or failure
  7. Handle result: inform owner, confirm with CreditClaw, announce
```

---

## Step 1: Browse and Shop

Follow `SHOPPING-GUIDE.md` to find the product, detect the platform, navigate the store,
and add items to cart. Proceed to the checkout page.

## Step 2: Fill the Checkout Form

Fill **every field** on the checkout form except the card number and CVV:

- Name, email, phone
- Shipping address (street, city, state, zip, country)
- Billing address (if separate from shipping)
- Cardholder name
- **Expiry date** (month and year) — fill this yourself using the card details from `GET /bot/status` (last4 and brand are visible, and the expiry date is not sensitive)

On multi-step checkouts, click through each section until you reach the payment step.

## Step 3: Confirm Fields and Identify Card Inputs

Take a snapshot, verify all non-card fields are filled, and note whether the card
fields are in an iframe:

```bash
openclaw browser snapshot --efficient --selector "form"
```

Check that shipping, billing, contact info, and expiry are all populated. Fix anything
that's missing or incorrect. **Do not fill the card number or CVV fields.**

From the same snapshot, identify where the card number and CVV fields are — regular
`<input>` elements on the page, or inside an iframe. If they're in an iframe, note the
iframe selector (e.g. `iframe[src*='stripe.com']`). You will pass this as `frame_hint`
to the plugin.

## Step 4: Request Checkout Approval

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

| Field | Required | Description |
|-------|----------|-------------|
| `merchant_name` | Yes | Merchant name (1-200 chars) |
| `merchant_url` | Yes | Merchant website URL |
| `item_name` | Yes | What you're buying |
| `amount_cents` | Yes | Amount in cents (integer) |
| `category` | No | Spending category |

**Approved response:**
```json
{
  "approved": true,
  "checkout_id": "r5chk_abc123",
  "checkout_steps": ["..."]
}
```

**Pending response (requires owner approval):**
```json
{
  "approved": false,
  "status": "pending_approval",
  "checkout_id": "r5chk_abc123",
  "message": "Amount exceeds auto-approve threshold. Your owner has been notified.",
  "expires_in_minutes": 15
}
```

If `pending_approval`, poll for the result:

```bash
curl "https://creditclaw.com/api/v1/bot/rail5/checkout/status?checkout_id=r5chk_abc123" \
  -H "Authorization: Bearer $CREDITCLAW_API_KEY"
```

Poll every 30 seconds. Do not call the plugin until the status is `approved`.

| Status | Meaning |
|--------|---------|
| `pending_approval` | Owner hasn't responded — poll again in 30s |
| `approved` | Proceed |
| `rejected` | Do not proceed |
| `expired` | 15-min window passed — re-initiate if needed |

## Step 5: Fill Card Fields with Plugin

Once the checkout is approved, call the CreditClaw plugin:

```
creditclaw_fill_card({
  checkout_id: "r5chk_abc123",
  card_file_path: ".creditclaw/cards/Card-ChaseD-9547.md",
  frame_hint: "iframe[src*='stripe.com']"
})
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `checkout_id` | Yes | The approved checkout ID |
| `card_file_path` | Yes | Path to encrypted card file (saved during card delivery) |
| `frame_hint` | No | CSS selector for payment iframe. Omit if card fields are on the main page. |

You know where the card file is because you saved it during card delivery. The default
path is `.creditclaw/cards/Card-{name}-{last4}.md`, but use the actual path if you
saved it elsewhere.

**Plugin returns one of:**

```json
{ "status": "filled", "fields_filled": ["card_number", "cvv"], "message": "Card number and CVV filled." }
```

```json
{ "status": "fill_failed", "reason": "card_number_not_found", "message": "Could not locate the card number input." }
```

```json
{ "status": "error", "reason": "key_retrieval_failed", "message": "Could not retrieve decryption key." }
```

**If `filled`** — proceed to Step 6.

**If `fill_failed`** — the card fields couldn't be located or filled. Take a snapshot to
understand the page layout. If you can provide a better `frame_hint` or if the page has
changed, call the plugin again. Start a new checkout if the key was already consumed.
Max 2 retry attempts with new checkouts.

**If `error`** — check the reason. Common errors:
- `missing_api_key`: `CREDITCLAW_API_KEY` is not set
- `card_file_error`: Encrypted card file not found or unreadable
- `key_retrieval_failed`: API rejected the key request (check checkout status)
- `decryption_failed`: Key material doesn't match the card file

## Step 6: Submit and Detect Result

After the plugin fills the card fields, click the submit/pay button:

```bash
openclaw browser click <submit_button_ref>
openclaw browser wait --load networkidle --timeout-ms 15000
openclaw browser snapshot --efficient
```

| Signal | Meaning |
|--------|---------|
| "Thank you" / "Order confirmed" / "Order #..." | **Success** — capture order number |
| "Payment successful" / "Receipt" | **Success** |
| "Payment declined" / "Card declined" | **Failed** |
| "Error" / "try again" | **Failed** |
| Page unchanged after 15 seconds | **Failed** |
| CAPTCHA / 3DS / OTP | **Cannot proceed** — report to owner |

## Step 7: Handle Result

### On Success

1. **Inform your owner immediately** with a screenshot:
   > "Purchased {item} at {merchant} for ${amount}. Order ID: {order_id}. [screenshot attached]"

2. **Wait up to 2 minutes** for your owner to respond.

3. **If owner confirms or no response within 2 minutes:**
   - Call `POST /bot/rail5/confirm` with `"status": "success"`

4. **If owner contests or reports a problem:**
   - Analyze the issue. If corrections are needed and the page allows it, fix what you can.
   - If the card fields need re-entry, start a new checkout from Step 4.

### On Failure

Take a snapshot and analyze the cause:

| What you see | Likely cause | Action |
|---|---|---|
| "Please fill in [field]" or a required field highlighted empty | Main agent missed a field | Fix the field, start new checkout from Step 4 |
| "Invalid card number" or "Check your card details" | Plugin typed in wrong field or input wasn't accepted | Provide better `frame_hint`, start new checkout from Step 4 |
| "Card declined" / "Insufficient funds" / "Do not honor" with all fields correct | Genuine payment decline | This is a real failure |
| CAPTCHA / 3DS / OTP appeared | Security challenge | Cannot proceed — report to owner |

If the form is correctly filled and the payment was genuinely declined, call
`POST /bot/rail5/confirm` with `"status": "failed"`.

**Max 2 retry attempts** with new checkouts. If still failing after 2 retries with
the form correct, treat it as a genuine decline.

### Confirm with CreditClaw

```bash
curl -X POST https://creditclaw.com/api/v1/bot/rail5/confirm \
  -H "Authorization: Bearer $CREDITCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "checkout_id": "r5chk_abc123", "status": "success" }'
```

Use `"status": "failed"` if the payment was genuinely declined.

**On success:**
> "Purchased {item} at {merchant} for ${amount}. Order ID: {order_id}."

**On genuine decline:**
> "Purchase of {item} at {merchant} failed — {reason}. No charge was made."

---

## Recovery

### Plugin Error Recovery

If the plugin returns `error` with `key_retrieval_failed`, check what happened:

```bash
curl "https://creditclaw.com/api/v1/bot/rail5/checkout/status?checkout_id=r5chk_abc123" \
  -H "Authorization: Bearer $CREDITCLAW_API_KEY"
```

| Checkout status | `key_delivered` | Meaning | Action |
|---|---|---|---|
| `approved` | `false` | Key was never retrieved | Safe to start new checkout from Step 4 |
| `approved` | `true` | Key was retrieved but plugin failed after | Start new checkout — key is consumed |

### Re-initiating After Failure

Start a new attempt from Step 4. Each checkout gets a fresh `checkout_id` and a
fresh single-use decryption key. There is no limit on retry attempts, but each
attempt goes through the full guardrail and approval flow.

---

## Complete Example

```
# Main agent browses DigitalOcean, adds Droplet hosting to cart, fills checkout form
# Main agent fills: email, name, address, billing, cardholder name, expiry (03/28)
# Main agent identifies: card number and CVV are in a Stripe iframe

# Step 4: Request approval
POST /api/v1/bot/rail5/checkout
{ "merchant_name": "DigitalOcean", "merchant_url": "https://cloud.digitalocean.com/billing",
  "item_name": "Droplet hosting - 1 month", "amount_cents": 1200, "category": "cloud_compute" }
# → { "approved": true, "checkout_id": "r5chk_abc123" }

# Step 5: Fill card fields with plugin
creditclaw_fill_card({
  checkout_id: "r5chk_abc123",
  card_file_path: ".creditclaw/cards/Card-ChaseD-9547.md",
  frame_hint: "iframe[src*='js.stripe.com']"
})
# → { "status": "filled", "fields_filled": ["card_number", "cvv"] }

# Step 6: Submit and detect result
openclaw browser click <pay_button_ref>
openclaw browser wait --load networkidle --timeout-ms 15000
openclaw browser snapshot --efficient
# → "Thank you for your purchase. Order ID: ORD-12345"

# Step 7: Inform owner
# → "Purchased Droplet hosting at DigitalOcean for $12.00. Order ID: ORD-12345. [screenshot]"
# → Wait up to 2 minutes for owner response
# → Owner confirms (or no response) → proceed

# Confirm with CreditClaw
POST /api/v1/bot/rail5/confirm
{ "checkout_id": "r5chk_abc123", "status": "success" }

# Done.
"Purchased Droplet hosting - 1 month at DigitalOcean for $12.00. Order ID: ORD-12345."
```
