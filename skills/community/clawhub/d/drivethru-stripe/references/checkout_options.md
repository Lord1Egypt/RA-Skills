# Checkout Session — less-common options

All fields below pass straight through to `stripe.checkout.Session.create` and can be included in the JSON payload to `scripts/create_checkout_session.py`. Full reference: https://stripe.com/docs/api/checkout/sessions/create

## Customer

- `customer` — existing `cus_...` id. Use when the user already has a Customer.
- `customer_email` — pre-fill the email field (cannot be combined with `customer`).
- `client_reference_id` — your own internal id (max 200 chars). Returned via the `checkout.session.completed` webhook.

## Tax & shipping

- `automatic_tax: {"enabled": true}` — requires Stripe Tax to be configured on the account.
- `shipping_address_collection: {"allowed_countries": ["US", "CA"]}`
- `billing_address_collection: "required" | "auto"`

## Promotions & discounts

- `allow_promotion_codes: true` — show a "promotion code" field on the hosted page.
- `discounts: [{"coupon": "abc"}]` — apply a coupon directly (cannot combine with `allow_promotion_codes`).

## Payment methods & locale

- `payment_method_types: ["card", "us_bank_account", "link"]` — defaults to the account's enabled methods.
- `locale: "auto"` — or a specific locale like `"en"`, `"fr"`, `"es"`.

## Subscription-specific

When `mode = "subscription"`:

- `subscription_data.trial_period_days: 14`
- `subscription_data.metadata: {...}`
- Every `line_items[*].price` must reference a recurring Price.

## One-time payment specifics

When `mode = "payment"`:

- `payment_intent_data.setup_future_usage: "off_session"` — save the card for later.
- `payment_intent_data.statement_descriptor`
- `payment_intent_data.metadata`

## Setup mode

When `mode = "setup"`, do NOT pass `line_items`. The session collects a payment method without charging it; useful for saving a card before billing later.

## Expiration

- `expires_at` — Unix timestamp, must be 30 minutes to 24 hours in the future. Defaults to 24h.
