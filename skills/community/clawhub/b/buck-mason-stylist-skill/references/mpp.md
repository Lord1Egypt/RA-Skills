# MPP — fully agent-driven checkout via Pima (HTTP 402 challenge)

Pima exposes the **[Merchant Payments Protocol](https://mpp.dev)** at `POST https://pima.io/mcp/buckmason/checkout`. This is the path for agents that want to handle the **entire** transaction — line items, shipping address, payment, confirmation — without bouncing the customer to a browser.

The agent-side tooling is **[stripe/link-cli](https://github.com/stripe/link-cli)** — a Node CLI / MCP server that lets an AI agent fetch a one-time **Stripe Shared Payment Token (SPT)** from the customer's Link wallet (push-approved on the customer's phone). That SPT is what the agent submits to Pima's `/checkout` endpoint to clear the HTTP 402 challenge.

## When to use MPP

Use `POST /mcp/buckmason/checkout` when the customer wants the agent to fully process the order: voice-driven concierge, BFCM speed runs, auto-replenishment, or headless surfaces. It requires an agent that can mint a Stripe SPT via `link-cli` against the customer's Link wallet.

**Don't start checkout unless the customer has explicitly opted into agent-driven payment and the total has been restated in plain English in the same turn.** The customer's Link push-approval is the consent step.

## Entry point — the `html-cart` lookbook prose handoff

The most common way the customer enters the MPP path is by pasting (or speaking) back the plain-prose handoff emitted by an `html-cart` lookbook (`references/output-formats.md` § "The handoff is plain English"). Format: a short paragraph naming the lookbook + bulleted items with sizes. Voice flows skip the paste step entirely — the customer says "from the LA Mellow Weekend lookbook, I want the camp shirt in L and the chinos in 31" — same vocabulary, same handler. On receiving the handoff (text or speech):

1. **Detect the handoff.** Heuristics: text mentions a Buck Mason lookbook context (e.g., starts with `Buck Mason — <title>` or refers to "the lookbook") and lists items with sizes. The customer might trim the paragraph or speak a fragment ("the camp shirt and the chinos") — accept either. Don't require a rigid envelope; if the message looks plausibly like a stylist handoff, proceed and confirm at the summary step.
2. **Resolve each item by name.** For each line, search `GET /mcp/buckmason/products?gender=<m|w>&q=<distinctive substring>` (`q` is exact-substring per `references/mcp-api.md`, so prefer short distinctive phrases — "Deuce Coupe Camp Shirt" beats the full product name), then `GET /products/<id>` and pick the variant matching the stated size. If the agent still has the conversation context that generated the lookbook, "the camp shirt" maps unambiguously to the rendered Look 01 piece — no MCP search needed. Resolve from `~/.buck-mason-stylist/wishlist.jsonl` if the agent was started fresh in a new session and the prose carries a `lookbook_id`-style date+title line.
3. **Disambiguate when needed.** If a name resolves to multiple products (rare on Buck Mason's catalog), ask the customer one question naming the candidates — never silently pick.
4. **Gather the rest conversationally — one round trip, defaults assumed.** Default: ship to `profile.md → shipping`, no coupon, apply all available customer credit. Restate as: *"Shipping to <street>, no coupon, applying $X in credit. Anything to change?"* Accept either "go ahead" or a one-line correction (`pickup at Abbot Kinney`, `code SPRING25`, `skip credit`). If the customer names a purchase purpose ("personal clothing", "work travel", "company wardrobe"), map it to `profile.md → preferred_link_payment_methods` before requesting Link approval.
5. **Spot price drift.** The prose carries a "Subtotal at pick" line. If the phase-1 live subtotal differs by more than ~1% (per-line, before tax), surface the diff in plain English before reading the total back. Don't surprise the customer with a price hike at the approval moment.
6. **Then proceed** with the standard phase-1 → restate-total → `link-cli spend-request create` → push-approve → phase-2 cycle from § "Lifecycle (one endpoint, two phases)" below.
7. **On success, append the order to `~/.buck-mason-stylist/wishlist.jsonl`** — one JSONL record per item with the lookbook id, item name, size, resolved SKU, qty, `order_id`, and `purchased_at`. This is the cross-session memory the agent reads next time the customer opens a lookbook ("you bought the camp shirt last week — different color this time?").

## Lifecycle (one endpoint, two phases)

```
POST /mcp/buckmason/checkout                       — phase 1 (challenge)
POST /mcp/buckmason/checkout                       — phase 2 (charge)
   with Authorization: Payment <SPT>
```

Both POSTs carry the same body. The server is **stateless** — it doesn't store a checkout between the two calls; the agent re-sends the cart the second time.

### Phase 1 — challenge

```http
POST /mcp/buckmason/checkout
Content-Type: application/json
Idempotency-Key: <uuid>          ← optional but recommended; forwarded to Stripe in phase 2
```
```json
{
  "line_items": [
    { "sku": "OLIVE-DAILY-SHIRT-L", "quantity": 1 },
    { "sku": "FORD-CHINO-32",       "quantity": 1, "pickup_location_slug": "abbot-kinney" },
    { "sku": "BREEZE-LINEN-M",      "quantity": 2, "pickup_location_name": "VEN" }
  ],
  "buyer": { "name": "Jane Doe", "email": "jane@example.com", "phone": "+15555550100" },
  "fulfillment_address": { "line1": "1320 Abbot Kinney Blvd", "city": "Venice",
                           "state": "CA", "postal_code": "90291", "country": "US" },
  "pickup_location_slug": "abbot-kinney",   // optional cart-level default; applied
                                            //  to any line item that didn't specify
                                            //  its own pickup_location_*
  "coupon": "SPRING25",                     // optional, bearer code
  "customer_credit_codes": ["GC-12345"]     // optional, bearer codes
}
```

**Per-line-item pickup location** (the only fulfillment-routing decision a customer can make). Each line item accepts any one of:
- `pickup_location_slug`: `"abbot-kinney"` — preferred; matches against the location's `short_name.parameterize` or `name.parameterize`
- `pickup_location_id`: `2` — direct numeric id
- `pickup_location_name`: `"Abbot Kinney Mens"` OR the short_name `"AKMens"` — case-insensitive. Shopify uses the short_name in its `line_item[:properties]` "Location" value; MPP accepts both so the agent can use whichever it has.

A line item with no pickup_location ships from the warehouse. A line item with a pickup_location is reserved for in-store pickup at that store. A cart can mix ship + pickup items in any combination.

> **Note: pickup vs fulfillment.** The customer-facing input is *pickup_location* (where they want to physically pick up the item). Pima also has an internal *fulfillment_location* concept on each OrderItem, but that's different — for ship items it's set later by automatic or CX/warehouse-agent routing, never by the customer. Agents should only ever speak `pickup_location_*` in MPP requests.

Server response:

```http
HTTP/1.1 402 Payment Required
WWW-Authenticate: Payment id="01HX…", realm="pima.io", method="stripe",
                  intent="charge", request="<base64url(payment-request-json)>"
Cache-Control: no-store
```
```json
{
  "payment_required": true,
  "currency": "usd",
  "line_items": [
    { "sku": "OLIVE-DAILY-SHIRT-L", "quantity": 1, "unit_price_cents": 9800,
      "pickup_location_id": null, "pickup_location_name": null, "to_pickup": false },
    { "sku": "FORD-CHINO-32", "quantity": 1, "unit_price_cents": 16800,
      "pickup_location_id": 2, "pickup_location_name": "Abbot Kinney Mens", "to_pickup": true },
    { "sku": "BREEZE-LINEN-M", "quantity": 2, "unit_price_cents": 18800,
      "pickup_location_id": 5, "pickup_location_name": "Venice Flagship", "to_pickup": true }
  ],
  "buyer": {...},
  "fulfillment_address": {...},
  "pickup_location_id": 2,
  "pickup_location_name": "Abbot Kinney Mens",
  "coupon": "SPRING25",
  "coupon_status": { "code": "SPRING25", "applied": true, "amount_cents": 1000, "type": "fixed" },
  "customer_credit_codes": ["GC-12345"],
  "credit_status": [
    { "code": "GC-12345", "applied": true, "amount_cents": 5000, "balance_remaining_cents": 0 }
  ],
  "credit_applied_cents": 5000,
  "totals": {
    "subtotal_cents": 64200, "discount_cents": 1000, "shipping_cents": 0,
    "tax_cents": 0, "credit_applied_cents": 5000,
    "total_cents": 58200,                 // gross order value
    "charge_cents": 53200,                // amount Stripe will charge after credit
    "subtotal": "$642.00", "discount": "$10.00", "shipping": "$0.00",
    "tax": "$0.00", "credit_applied": "$50.00",
    "total": "$582.00", "charge": "$532.00"
  },
  "payment_options": [
    { "type": "shared_payment_token", "provider": "stripe", "protocol": "mpp_v1",
      "protocol_homepage": "https://mpp.dev",
      "network_id": "profile_…", "amount_cents": 53200, "currency": "usd" }
  ],
  "suggested_context": "Authorize a $532.00 charge by Buck Mason: 1× Olive Daily Shirt (size L), 1× Ford Chino (size 32), 2× Breeze Linen (size M), shipping to Venice, CA, pickup at Abbot Kinney Mens via the mpp.dev Merchant Payments Protocol."
}
```

Each line item's `to_pickup` + `pickup_location_name` tell the agent how to read the cart back to the customer: "Olive Daily Shirt ships to your address; Ford Chino is reserved for pickup at Abbot Kinney Mens; 2× Breeze Linen reserved for pickup at Venice Flagship."

> **`suggested_context`** is a pre-built ≥100-char human-readable summary the agent should pass verbatim to `link-cli spend-request create --context`. As of 2026-04-29 the Link app's spend-request approval surface renders **only** the merchant name + this context blurb — it ignores `line_items`, prices, and `image_url` thumbnails on both the SPT and card credential surfaces. Until Stripe ships line-item rendering on this surface, this string is the only customer-visible cart preview at the approval moment.

### Selecting the Link payment method

`link-cli spend-request create` requires a concrete Link payment method id for `shared_payment_token` requests. Do **not** store those internal ids in `profile.md`: they are live Link wallet identifiers, not durable shopper preferences. Store only customer-readable routing hints such as card name, brand, last4, and purpose.

Recommended profile shape:

```yaml
link_payment_method: confirmed
link_payment_methods:
  - name: "Visa Credit"
    brand: "visa"
    last4: "0896"
    purpose: "personal clothing"
preferred_link_payment_methods:
  clothing: "0896"
  default: "0896"
```

Runtime selection flow:

1. Infer the purchase purpose from the user request or profile context (`clothing` for normal Buck Mason personal purchases unless the customer says otherwise).
2. Read `profile.md → preferred_link_payment_methods[purpose]`, falling back to `default` or the legacy `preferred_link_payment_method_last4`.
3. Run `link-cli payment-methods list --format json`.
4. Match the preferred last4 against the live list. If exactly one card matches, use its `id`. If no card matches or multiple cards share the same last4, ask the customer to choose by card name + last4.
5. Pass the selected id to `link-cli spend-request create --payment-method-id <id>`. Do not write the id, SPT, or any raw credential to disk.

Example:

```bash
PAYMENT_METHOD_ID="$(link-cli payment-methods list --format json \
  | jq -r '.[] | select(.card_details.last4 == "0896") | .id' \
  | head -n1)"

link-cli spend-request create \
  --credential-type shared_payment_token \
  --payment-method-id "$PAYMENT_METHOD_ID" \
  --network-id "<payment_options[0].network_id>" \
  --amount "<totals.charge_cents>" \
  --currency usd \
  --context "<suggested_context>" \
  --request-approval \
  --format json
```

### Phase 2 — read total back, mint SPT, retry with Authorization

1. Agent reads the `total` (and the breakdown — coupon, credit, shipping, tax) back to the customer **verbatim**.
2. Customer says yes.
3. Agent selects the Link payment method as above, then runs `link-cli spend-request create --credential-type shared_payment_token --payment-method-id <id> --network-id <network_id> --amount <charge_cents> --currency usd --context <suggested_context>` (or the MCP-server equivalent). Customer push-approves on their phone in the Link app. Stripe returns an SPT.
4. Agent re-POSTs the same cart with the SPT and the `acknowledged_total_cents` echo:

```http
POST /mcp/buckmason/checkout
Content-Type: application/json
Authorization: Payment <SPT>             ← canonical MPP form (Bearer also accepted)
Idempotency-Key: <uuid>                  ← reuse the same key from phase 1
X-Agent-Identity: Claude Code            ← agent self-id, persisted on Order#mpp_agent_identity
X-Agent-Model: claude-opus-4-7           ← model behind the agent, persisted on Order#mpp_agent_model
```

> **`X-Agent-Identity`** + **`X-Agent-Model`** — the wrapping agent's self-identification ("Claude Code", "Cursor", etc) and the LLM behind it ("claude-opus-4-7", "gpt-5", etc). link-cli sends `User-Agent: node` by default, which loses the actual caller, so Pima reads these two headers first and persists them in the structured columns `Order#mpp_agent_identity` + `Order#mpp_agent_model` (queryable: "how many orders did Claude Code place last week?", "which model generates the most refunds?"). Both are also formatted into the human-readable `Order#notes` ("MPP order via Claude Code (claude-opus-4-7)"). Pass via `link-cli mpp pay --header 'X-Agent-Identity: Claude Code' --header 'X-Agent-Model: claude-opus-4-7'`. Optional but recommended — without them the note falls back to a generic `link-cli (node)`.
```json
{
  "line_items": [...],            // identical to phase 1
  "buyer": {...},
  "fulfillment_address": {...},
  "pickup_location_slug": "abbot-kinney",
  "coupon": "SPRING25",
  "customer_credit_codes": ["GC-12345"],
  "acknowledged_total_cents": 8800   ← matches totals.total_cents from phase 1
}
```

Server response on success:

```http
HTTP/1.1 200 OK
Payment-Receipt: pi_3OabcXYZ...
Cache-Control: no-store
```
```json
{
  // ...same cart envelope as phase 1 plus:
  "state": "completed",                        // the MPP-checkout state, not the Pima Order status
  "order_code": "BM-9876",                     // the customer-facing order identifier
  "payment_intent_id": "pi_3OabcXYZ..."
}
```

> `order_id` is intentionally **not** in the response — it's a Pima-internal primary key. `order_code` is the customer-facing identifier (the same one printed on every order-confirmation email and used by orders.buckmason.com lookups).

**What Pima creates server-side** when phase 2 succeeds:

- A real **Customer** (guest if `buyer.email` doesn't match an existing record).
- A real **CustomerAddress** populated from `buyer.{name, email, phone}` and `fulfillment_address.{line1, line2, city, state, postal_code, country}`.
- A real **Order** with:
  - `status: "new"` — paid, awaiting fulfillment (entered into the picking/packing queue). **NOT** `"completed"` — that would mean POS-style "customer walked out with the goods," which MPP customers haven't done. Final completion happens when items are shipped or picked up.
  - `completed_at` = purchase time (per the Shopify webhook convention; not fulfillment time).
  - `source: "mpp"`.
  - `mpp_payment_intent_id` = the Stripe PaymentIntent id (reverse-link).
  - `location` = `default_shipping_location` (online-order convention; same as Shopify webhook).
  - `customer_address` linked to the address above.
- One **OrderItem** per quantity-unit per resolved line item, with:
  - `status: "new"`
  - `original_paid_price` = unit price in cents
  - For pickup items: `to_pickup: true` + `fulfillment_location` = the customer-chosen pickup store. (The schema column is named `fulfillment_location` and is dual-meaning by row — for pickup items it's the pickup store; for ship items it's later set by routing to a ship-from warehouse. That dual meaning is Pima-internal; the agent never sees it.)
  - For ship items: `fulfillment_location` left nil; Pima's order-routing flow assigns the warehouse + `to_ship` flag later.
- (Optional) **OrderGiftCertificateItems** when the cart body carries `gift_certificate_items: [...]`.

Downstream Pima processing — fulfillment routing, shipment, returns via orders.buckmason.com, exports — works on the materialized Order exactly as if it had come from a web checkout.

### Hard guarantees enforced by Pima

| Guard | Behaviour on failure |
|---|---|
| `acknowledged_total_cents` ≠ server `total_cents` | `422 total_mismatch` (with `server_total_cents` in the error payload) |
| Authorization header absent | `402 Payment Required` (challenge re-issued — agent should mint SPT and retry) |
| Card declined / Stripe error | `402` with `code: card_declined` or `stripe_error` |
| Company has no Stripe creds | `402 stripe_not_configured` |
| Bad pickup slug / pickup-disabled location | `404 pickup_location_not_found` / `422 pickup_disabled` |

`Authorization` accepts both the canonical `Payment <SPT>` form (per MPP) and `Bearer <SPT>` as a fallback for clients that only know the OAuth-style header.

### When credit covers the full order

If `customer_credit_codes` covers the entire `total_cents` (so `charge_cents == 0`), the SPT step is skipped:
- Phase 1 returns the same 402 challenge with `payment_options[].amount_cents: 0`
- Phase 2 still requires an `Authorization` header (any value) so the agent has explicitly opted into the success branch — but the SPT is unused and Stripe is not called
- Response includes `payment_intent_id: null`

### Coupons + customer credits — bearer codes (no auth)

Both follow the same model as Buck Mason POS — anyone with the code can apply (gift-card semantics).

```json
"coupon": "SPRING25",                     // single string — Pima Coupon
"customer_credit_codes": ["GC-12345"]     // array — Pima CustomerCredit (gift cards, store credit)
```

Failures are **soft-warns** (the checkout still produces a challenge):
- `coupon_not_found` / `not_applicable` / `coupon_disabled`
- `credit_not_found` / `credit_disabled` / `credit_no_balance` / `order_already_paid`

The agent should surface ("Your coupon expired — continue without it?") rather than abort.

## Discovery

`GET /mcp/buckmason/manifest` advertises the MPP surface in its `mpp` block:

```json
{
  "mpp": {
    "spec": "https://mpp.dev",
    "base_url": "/mcp/buckmason/checkout",
    "agent_tools": ["https://github.com/stripe/link-cli"]
  },
  "endpoints": [
    { "method": "POST", "path": "/mcp/<slug>/checkout", ... }
  ]
}
```

Agents that don't recognize MPP should stop and surface the missing capability instead of inventing another purchase path.

## Sandbox / staging

Two affordances let an agent run against staging or soak-test against prod without moving real money:

### `Pima-Environment` response header (and manifest field)
Every MCP/MPP response stamps `Pima-Environment: <production|sandbox>`. The same value is in `manifest.environment`. `pima.io` is production. Use this header to refuse to charge real money when the agent thinks it's hitting sandbox but the response says production (or vice versa).

```bash
curl -sI https://pima.io/mcp/buckmason/manifest | grep -i pima-environment
# Pima-Environment: production
```

### `?dry_run=true` query param on `/checkout`
Skips Stripe entirely. Returns a fake `Payment-Receipt: pi_dry_run_<random>` header, sets `state: "dry_run"` in the body, sets `Pima-Dry-Run: true` response header, and does **not** materialize a Pima Order. Lets agents validate the full envelope shape (cart resolution, totals, coupon/credit application, total-mismatch guards, Authorization parsing) without authorizing a payment.

```bash
curl -sS -i -X POST 'https://pima.io/mcp/buckmason/checkout?dry_run=true' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Payment any-string-works-in-dry-run' \
  -d '{"line_items":[{"sku":"<sku>","quantity":1}],
        "buyer":{...}, "fulfillment_address":{...},
        "acknowledged_total_cents": 9800}'
# → 200 OK
# Payment-Receipt: pi_dry_run_a1b2c3d4
# Pima-Dry-Run: true
```

Use `dry_run` for: agent regression tests against prod (without billing customers), end-to-end demos in front of stakeholders, smoke tests after a deploy, and validating a customer's chosen pickup location + size availability before requesting their actual SPT.

## Checkout safety — required prompt rules

The Stripe Shared Payment Token IS the customer's consent (Stripe-issued, scoped, time-limited; minted only after the customer push-approves in the Link app). The agent's responsibility is to make sure the customer knows what they're authorizing **before** the SPT is requested, and to never silently retry on failure.

- **Always read the total back to the customer before requesting the SPT.** Verbatim ("$88.00 — $5.00 paid by gift card GC-12345; Stripe will charge $38.00 to your card") and including currency.
- **Require an unambiguous "yes" in the same turn before kicking off `link-cli spend-request create`.** "OK" alone is not consent.
- **Always pass `--payment-method-id` for shared-payment-token requests.** Resolve it live from `link-cli payment-methods list` using the profile's purpose-to-last4 preference. If there is no unambiguous match, ask the customer to pick; never guess.
- **Never re-POST `/checkout` from a chained tool-use without a fresh user message between the read-back and the SPT mint.** Re-confirm each charge.
- **On any 4xx error, do NOT auto-retry.** Surface the error to the customer; they decide what to do.
- **On a `total_mismatch` 422, re-read the corrected total before re-attempting.** This catches hallucinated prices.
- **When announcing coupon/credit application, name the code and the saving.** "Applied SPRING25 (-$10) and gift card GC-12345 ($50 of $50 used)" — never silently apply.
- **Always disclose** the payment processor: "Your card will be charged $X.XX through Stripe via Buck Mason."
