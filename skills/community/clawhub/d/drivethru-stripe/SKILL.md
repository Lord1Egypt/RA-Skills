---
name: drivethru-stripe
description: Look up products in the Stripe catalog and create a Stripe Checkout Session that returns a hosted checkout URL. Use whenever the user needs to browse what's for sale, bill a customer, collect a one-time payment, or start a subscription via a Stripe-hosted page.
version: 0.2.0
emoji: 💳
homepage: https://stripe.com/docs/api/checkout/sessions
metadata:
  openclaw:
    requires:
      env: [STRIPE_SECRET_KEY]
      bins: [python3]
    primaryEnv: STRIPE_SECRET_KEY
    envVars:
      STRIPE_SECRET_KEY:
        required: true
        description: >
          Stripe secret API key (starts with `sk_test_` for test mode or `sk_live_` for live mode).
          Create one at https://dashboard.stripe.com/apikeys. The skill makes server-side API calls
          and will not work with a publishable key (`pk_...`).
    install:
      uv:
        - stripe>=10.0.0
---

# Stripe Checkout & Product Lookup

This skill does two things against the Stripe API:

1. **List/search products** in the Stripe product catalog — returns name, description, image, prices, and metadata.
2. **Create a [Stripe Checkout Session](https://stripe.com/docs/api/checkout/sessions/create)** and return the hosted payment URL the customer should be redirected to.

A typical flow: call `list_products.py` to find the right `price_...` id(s), then pass them to `create_checkout_session.py` as `line_items`.

## Required credentials

The agent host MUST expose **`STRIPE_SECRET_KEY`** in the environment before this skill is invoked.

- Test mode key: `sk_test_...` (use during development; charges are not real)
- Live mode key: `sk_live_...` (real money — only after explicit user confirmation)

If `STRIPE_SECRET_KEY` is missing, stop and tell the user to set it. Do not prompt the user to paste the key into chat — secrets must come from the environment.

Optional environment variables:

| Variable                  | Purpose                                                                |
| ------------------------- | ---------------------------------------------------------------------- |
| `STRIPE_API_VERSION`      | Pin a Stripe API version (defaults to the account's pinned version).   |
| `STRIPE_DEFAULT_SUCCESS_URL` | Fallback `success_url` when the user does not provide one.          |
| `STRIPE_DEFAULT_CANCEL_URL`  | Fallback `cancel_url` when the user does not provide one.           |

## When to use

- "What products do we sell?" / "List our Stripe catalog" / "Find the price of X"
- "Create a checkout link for X"
- "Bill the customer $N for Y"
- "Start a subscription to price `price_...`"
- "Generate a Stripe payment page for these items"

## When NOT to use

- The user wants to charge a saved card directly → use the PaymentIntents API instead (different skill).
- The user wants to issue a refund, manage a subscription's lifecycle, or read reports → out of scope here.
- The user wants to *create* or *edit* a product → out of scope; use the Stripe dashboard or a separate skill.

## Scripts

| Script                                | Purpose                                                       |
| ------------------------------------- | ------------------------------------------------------------- |
| `scripts/list_products.py`            | Query products (list / search / by id) + their prices         |
| `scripts/create_checkout_session.py`  | Create a Checkout Session and return the hosted checkout URL  |

---

## Listing products

Call `scripts/list_products.py` with an optional JSON filter on stdin. With no input, it returns the first 10 active products.

### Input schema (all fields optional)

```json
{
  "query": "shirt",
  "ids": ["prod_abc", "prod_def"],
  "active": true,
  "limit": 10,
  "starting_after": "prod_xyz",
  "include_inactive_prices": false
}
```

- `query` — free-text search against product name. If the string contains a `:`, it is passed through as a raw [Stripe Search](https://stripe.com/docs/search) query (e.g. `metadata['sku']:'A-100' AND active:'true'`). Search results may lag writes by up to a minute.
- `ids` — retrieve specific products by id (skips list/search). Up to ~50 is reasonable.
- `active` — defaults to `true`. Pass `false` to include archived products, or `null` for both.
- `limit` — 1–100, defaults to 10.
- `starting_after` — pagination cursor (returned as `next_starting_after`). Only applies to plain list mode.
- `include_inactive_prices` — defaults to `false`. Each returned product's `prices` array only contains active prices unless this is `true`.

### Example invocation

```bash
echo '{"query": "shirt", "limit": 5}' | python3 scripts/list_products.py
```

### Output

```json
{
  "products": [
    {
      "id": "prod_NabcXYZ",
      "name": "Cotton T-shirt",
      "description": "100% cotton, unisex",
      "image": "https://files.stripe.com/.../shirt-front.png",
      "images": ["https://files.stripe.com/.../shirt-front.png"],
      "metadata": {"sku": "TS-001", "color": "navy"},
      "active": true,
      "default_price": "price_1Nabc...",
      "prices": [
        {
          "id": "price_1Nabc...",
          "unit_amount": 1500,
          "currency": "usd",
          "recurring": null,
          "nickname": null,
          "active": true
        }
      ]
    }
  ],
  "has_more": false,
  "next_starting_after": null
}
```

- `unit_amount` is in the smallest currency unit (cents for USD).
- `image` is the first entry from `images` for convenience; use `images` if you need them all.
- `metadata` is the product's free-form key/value map set in the Stripe dashboard.
- When `has_more` is true, pass `next_starting_after` back as `starting_after` to get the next page.

When the user asks about pricing for a product, prefer the `default_price` if set; otherwise, surface all `prices` so they can pick.

---

## Creating a Checkout Session

Call `scripts/create_checkout_session.py` with a JSON payload on stdin. The script prints a JSON object with `url`, `id`, and `expires_at` on success.

### Input schema

```json
{
  "mode": "payment | subscription | setup",
  "line_items": [
    {"price": "price_123", "quantity": 1},
    {
      "price_data": {
        "currency": "usd",
        "unit_amount": 1500,
        "product_data": {"name": "Custom T-shirt", "description": "Size M"}
      },
      "quantity": 2
    }
  ],
  "success_url": "https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
  "cancel_url":  "https://example.com/cancel",
  "customer_email": "optional@example.com",
  "client_reference_id": "optional-internal-id",
  "metadata": {"order_id": "1234"},
  "allow_promotion_codes": true
}
```

- `mode` defaults to `"payment"` (one-time). Use `"subscription"` when any line item references a recurring price.
- Each `line_items[*]` entry MUST contain either `price` (existing Stripe Price ID) OR `price_data` (inline price), plus `quantity`.
- `unit_amount` is in the smallest currency unit (cents for USD).
- `success_url` is required by Stripe. Use `{CHECKOUT_SESSION_ID}` to receive the session id back as a query param.

### Example invocation

```bash
echo '{
  "mode": "payment",
  "line_items": [{"price": "price_1Nabc...", "quantity": 1}],
  "success_url": "https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
  "cancel_url": "https://example.com/cancel"
}' | python3 scripts/create_checkout_session.py
```

Successful output:

```json
{
  "url": "https://checkout.stripe.com/c/pay/cs_test_...",
  "id": "cs_test_a1B2c3D4...",
  "expires_at": 1716595200,
  "mode": "payment",
  "livemode": false
}
```

Return the `url` to the user — that is the link they (or their customer) should open to complete payment.

### Errors

The script exits non-zero and prints a JSON `{"error": {...}}` object on failure. Common cases:

- `auth_error` — `STRIPE_SECRET_KEY` is missing, malformed, or revoked.
- `invalid_request` — bad `price` id, currency mismatch, missing `success_url`.
- `validation_error` — the input JSON does not satisfy the schema.

Surface the human-readable `message` to the user and suggest the obvious fix. Do not retry on `auth_error` or `validation_error`.

## Safety

- Always confirm the **mode** (test vs live) and **total amount** with the user before creating a session in live mode.
- Never log the full `STRIPE_SECRET_KEY`. The script reads it from the environment and never echoes it.
- Treat the returned `url` as sensitive-ish: anyone with the link can pay. Share it only with the intended customer.

## References

See [`references/checkout_options.md`](references/checkout_options.md) for the less-common Checkout Session fields (shipping, tax, automatic_payment_methods, etc.).
