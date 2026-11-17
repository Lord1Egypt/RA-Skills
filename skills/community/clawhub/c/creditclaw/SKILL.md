---
name: creditclaw
description: "Pay with Virtual Cards. Spending power for AI Agents, controlled by your human."
version: 3.0.0
metadata:
  version: "3.0.0"
  openclaw:
    requires:
      env:
        - CREDITCLAW_API_KEY
    invocation: user_confirmed
---

# CreditClaw — Virtual Cards for AI Agents

CreditClaw.com gives you spending power your owner controls. Your owner creates a **Virtual Card** from their own Visa/Mastercard, sets its spending limit, and links it to you. When you need to pay, you mint fresh card numbers off that card and fill the merchant's payment form.

Base URL: `https://creditclaw.com/api/v1`

> `rail3` in the endpoint paths below is a literal, fixed segment (the Virtual Cards rail) — never substitute your bot ID into it.

## Security

- All requests: `Authorization: Bearer <CREDITCLAW_API_KEY>` (except registration, which returns your key).
- **Never send your API key to any domain other than `creditclaw.com`, and never share it** — it's your identity and can spend your owner's money.
- **Mint fresh card numbers immediately before each purchase.** Never reuse or cache numbers across purchases — discard them after submitting the payment form.
- Spending limits are baked into each Virtual Card and enforced at the card network. Your owner can freeze or revoke a card at any time.

## 1. Register (once)

Already have a `CREDITCLAW_API_KEY` from a previous session? You're registered — skip to step 3. Never re-register; that creates a new bot that must be re-linked.

```bash
curl -X POST https://creditclaw.com/api/v1/bots/register \
  -H "Content-Type: application/json" \
  -d '{
    "bot_name": "my-research-bot",
    "owner_email": "jonathan@example.com",
    "pairing_code": "483-921"
  }'
```

- `bot_name` and `owner_email` required. `pairing_code` (from your human's onboarding screen) links you to their account automatically — include it whenever you have one.
- No pairing code? Register without it and give your human the `owner_verification_url` from the response so they can claim you.
- **Save the `api_key` from the response immediately** — it cannot be retrieved again. Store it where your platform stores credentials (default: env var `CREDITCLAW_API_KEY`; OpenClaw: `~/.openclaw/.env`). Load it next session.
- Rate limit: 3 registrations per hour per IP.

## 2. Your Owner Creates a Virtual Card

Only your owner can create Virtual Cards, at `https://creditclaw.com/virtual-cards`. Each card has its own spending limit, expiry date, and bot link. The card must be **linked to you** and `active` before you can use it. If you have no usable card, ask your human — don't poll.

## 3. See Your Cards

```bash
curl https://creditclaw.com/api/v1/bot/rail3/cards \
  -H "Authorization: Bearer $CREDITCLAW_API_KEY"
```

Returns your linked cards with `card_id`, `card_name`, `status`, `is_frozen`, and spending limits (`limit_amount_cents` per `limit_period`; `intent_mode: "open"` means no cap). Pick the `card_id` you'll pay with — it must have `status: "active"` and `is_frozen: false`. Limits are enforced at the card network, so an over-limit purchase declines on its own.

## 4. Pay: Mint Fresh Card Numbers

When you're on the merchant's checkout page and ready to pay:

```bash
curl -X POST https://creditclaw.com/api/v1/bot/rail3/cards/vc_9d2f.../credentials \
  -H "Authorization: Bearer $CREDITCLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "merchant": {
      "name": "Acme Books",
      "url": "https://acmebooks.com",
      "country_code": "US"
    }
  }'
```

The `merchant` body is optional but recommended — numbers minted with the real merchant's name and site have the best acceptance odds. An empty body (`{}`) works too.

**Response:**
```json
{
  "card_id": "vc_9d2f...",
  "card_number": "4111111111111111",
  "exp_month": "12",
  "exp_year": "2027",
  "cvc": "123",
  "cardholder_name": "Jonathan Miller",
  "credential_expires_at": "2026-08-13T15:20:00.000Z"
}
```

The response may include extra helper fields (`credential_merchant`, `usage_notes`) — safe to ignore.

Fill the merchant's payment form:

| Form field | Use |
|------------|-----|
| Card number | `card_number` |
| Expiry (MM/YY) | `exp_month` / last 2 digits of `exp_year` |
| CVC / CVV / security code | `cvc` |
| Name on card | `cardholder_name` (if null, ask your human) |

- Shipping address needed? `GET /bot/shipping-addresses` returns your owner's saved addresses as markdown (`address_count: 0` = none saved — ask your human).
- Card fields are often inside iframes (Stripe, Shopify, etc.) — interact with the frame; the submit button is usually on the main page.
- **Hard stops: CAPTCHA, 3-D Secure, or OTP challenges — stop and tell your human.** Never attempt to bypass them.
- **Discard the numbers immediately after submitting.** Next purchase = new mint call.

**After you submit:** success → done, tell your human what you bought. Declined → stop and tell your human; never retry a declined payment. Page hangs or errors *after* submit → the charge may still have gone through; don't mint again, tell your human so they can check their card statement.

## Errors

| Status | `error` | What to do |
|--------|---------|------------|
| 401 | `unauthorized` | API key wrong or missing. Load the saved one — don't re-register. |
| 400 | `validation_error` / `invalid_json` | Fix the request body (`merchant` fields: `name`, `url`, `country_code` 2 letters) and retry. |
| 409 | `duplicate_registration` | Already registered with this name + email. Load your saved key. |
| 404 | `card_not_found` | Check the `card_id` against `GET /bot/rail3/cards`. |
| 403 | `card_not_linked` | Card isn't linked to you. Ask your human to link it. |
| 403 | `card_frozen` | Owner froze the card. Ask them to unfreeze it. |
| 403 | `card_not_active` | Card isn't authorized yet, or is expired/revoked. Your human must fix it. |
| 403 | `master_guardrail` | Owner's account-wide guardrail is blocking purchases. Tell them; don't retry. |
| 409 | `card_expired` | The card's permission expired — your human must create a new Virtual Card. |
| 412 | `reauth_required` | Owner must sign in at creditclaw.com to re-enable autonomous purchases. Tell them. |
| 503 | `auth_transient` | Temporary issue — retry shortly. |
| 429 | `rate_limited` | Slow down; retry after `retry_after_seconds`. |
| 4xx/5xx | `credential_mint_failed` | Provider issue minting numbers. Retry once with a fresh call. |
