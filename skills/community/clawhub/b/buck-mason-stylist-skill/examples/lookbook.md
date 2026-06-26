# Worked example: lookbook + MPP checkout

**Customer says:** "Build me a 3-look lookbook for the Sonoma wedding, then check out look 2."

## 1. Load context

- `profile.md` → `gender: m`, sizes, fits, reference photo URL, `home_zip`
- `wardrobe.md` → owned items
- `events.md` → match "Sonoma wedding"

```yaml
- name: Sarah & James wedding
  date: 2026-05-30
  location: Sonoma County, CA
  setting: outdoor vineyard ceremony, dinner under string lights
  dress_code: smart casual / cocktail
```

Apply `references/seasons.md`: late spring + NorCal coast/inland → mild + foggy evenings; smart casual → sport coat + dress shirt + trouser + suede chukka or dress shoe; palette → olive/stone/tobacco/indigo.

Get a season-aware capsule recommendation (one call):

```
GET /mcp/buckmason/recommend?gender=m&occasion=wedding&dress_code=smart_casual&season=spring&near_zip=94110&radius_mi=25&sizes[shirt]=L&sizes[pant]=32x32&sizes[shoe]=10.5&sizes[jacket]=L
```

Response gives `capsule: [{slot: 'sport_coat', products: [...]}, {slot: 'shirt', ...}, {slot: 'pant', ...}, {slot: 'shoe', ...}]` — each product summary already includes `nearby_in_stock`, image, price.

## 2. Compose 3 outfits

Cross-reference wardrobe (`wardrobe.example.md`):
- Has: navy sport coat ✓, suede chukka ✓, indigo jean
- Gap: dress shirt finer than oxford; wool/wool-blend trouser; possibly a tie/pocket square

Three looks:

| Look | Sport coat | Shirt | Pant | Shoe | Accessory |
|---|---|---|---|---|---|
| 1 — ceremony classic | navy (owned) | white poplin | stone wool trouser | brown suede dress shoe | navy knit tie |
| 2 — daytime relaxed | none | pale-blue poplin | tobacco chino | suede chukka (owned) | none |
| 3 — dinner-only | navy (owned) | white poplin | indigo jean (owned, dark) | brown suede dress shoe | pocket square |

For each item not in the wardrobe, the `/mcp/buckmason/recommend` response already has `image_url`, `price`, `nearby_in_stock`. If you need finer detail (full image gallery, per-store counts), call `GET /mcp/buckmason/products/<slug>?near_zip=…&radius_mi=25`.

## 3. Generate try-on images

For each look, follow `references/image-generation.md`:

```python
from openai import OpenAI
client = OpenAI()

reference = open(profile["reference_photo_local"], "rb")

for look_num, look in enumerate(LOOKS, start=1):
    product_images = [open(p["flatlay_path"], "rb") for p in look["items"]]
    prompt = build_prompt(
        outfit=look["description"],
        setting=SETTINGS[look_num - 1],
        composition=COMPOSITIONS[look_num - 1],
    )
    result = client.images.edit(
        model="gpt-image-2",
        image=[reference] + product_images,
        prompt=prompt, size="1024x1536", quality="high", n=1,
    )
    save(f"lookbook/2026-05-30-sonoma-wedding/looks/look-{look_num}.png",
         b64decode(result.data[0].b64_json))
```

Settings + compositions for a Sonoma vineyard wedding:

```python
SETTINGS = [
    "outdoor vineyard ceremony aisle, late afternoon, soft warm side-light, white folding chairs visible in soft focus",
    "vineyard exterior between rows of vines, midday, dappled sunlight, walking",
    "long dinner table under string lights at dusk, warm bulb glow, soft fog, candid",
]
COMPOSITIONS = [
    "full-body, three-quarter turn, hands relaxed, eye-level 35mm",
    "medium-wide, walking toward camera, hand in pocket, slight smile, 50mm",
    "seated at table edge, leaning slightly forward in conversation, 50mm shallow depth",
]
```

## 4. Assemble the lookbook markdown

```
lookbook/2026-05-30-sonoma-wedding/
  profile.jpg                         (cached)
  products/
    poplin-white.jpg
    wool-trouser-stone.jpg
    dress-shoe-brown.jpg
    knit-tie-navy.jpg
    poplin-pale-blue.jpg
    chino-tobacco.jpg
    pocket-square-tonal.jpg
  looks/
    look-1.png
    look-2.png
    look-3.png
  lookbook.md
  checkout-look-2.txt
```

`lookbook.md` body (rendered to the customer):

```markdown
# Sarah & James, Sonoma — May 30

> AI-generated previews; fit and fabric may vary slightly. Free returns within 30 days.

## Look 1 — Ceremony classic
![](looks/look-1.png)
- Navy sport coat (you own it)
- White poplin dress shirt — $98 — [shop](https://www.buckmason.com/products/poplin-white)
- Stone wool trouser — $148 — [shop](...)
- Brown suede dress shoe — $228 — [shop](...)
- Navy knit tie — $58 — [shop](...)
**Total new: $532** — [Select Look 1 for checkout](#)

## Look 2 — Daytime relaxed
![](looks/look-2.png)
- Pale-blue poplin dress shirt — $98 — [shop](...)
- Tobacco chino — $128 — [shop](...)
- Suede chukka (you own it)
**Total new: $226** — [Select Look 2 for checkout](#)

## Look 3 — Dinner-only
![](looks/look-3.png)
- Navy sport coat (you own it)
- White poplin dress shirt (Look 1)
- Indigo jean (you own it)
- Brown suede dress shoe (Look 1)
- Tonal pocket square — $32 — [shop](...)
**Total new: $32** — [Select for MPP checkout](#)
```

## 5. Prepare MPP checkout for Look 2

Look 2 needs 2 new items: pale-blue poplin (size L) + tobacco chino (size 32x32). First resolve each item to a live SKU through the MCP product detail endpoint, then preflight checkout:

```
POST https://pima.io/mcp/buckmason/checkout
Content-Type: application/json

{
  "line_items": [
    { "sku": "POPLIN-PALE-BLUE-L", "quantity": 1 },
    { "sku": "CHINO-TOBACCO-32x32", "quantity": 1 }
  ],
  "buyer": { "name": "...", "email": "...", "phone": "..." },
  "fulfillment_address": { "line1": "...", "city": "...", "state": "...", "postal_code": "...", "country": "US" }
}
```

Response:
```json
{
  "payment_required": true,
  "totals": { "subtotal_cents": 22600, "charge_cents": 22600, "charge": "$226.00" },
  "payment_options": [{ "type": "shared_payment_token", "provider": "stripe", "network_id": "..." }],
  "suggested_context": "Authorize a $226.00 charge by Buck Mason: ..."
}
```

Render to the customer:

```
Checkout for Look 2:
  Pale-blue Poplin Dress Shirt — L — $98.00
  Tobacco Chino — 32x32 — $128.00
  Total to charge: $226.00
```

## 6. Customer says "just buy it for me, no browser"

Use the **MPP** flow (Merchant Payments Protocol) at `POST /mcp/buckmason/checkout`. The agent fetches a one-time **Stripe Shared Payment Token (SPT)** from the customer's Link wallet via [`stripe/link-cli`](https://www.npmjs.com/package/@stripe/link-cli) — the customer push-approves the spend on their phone, and that approval IS the consent. Full lifecycle in `references/mpp.md`.

**Before `link-cli spend-request create --request-approval`, the agent MUST read aloud, in plain English, in the same turn:**
1. Every line item with size + quantity + unit price.
2. Subtotal, taxes/shipping if available, **and the final total in dollars**.
3. The shipping destination (city + zip is enough; full address optional).
4. Buck Mason's return window (30 days, free returns).
5. That this charge is **non-reversible by the agent** — refunds go through orders.buckmason.com after the fact.

Wait for an unambiguous "yes, go ahead" before invoking `link-cli`. Do not fast-path it.

Quick shape (read `references/mpp.md` for the complete contract):

```
# Phase 1 — challenge
POST https://pima.io/mcp/buckmason/checkout
Idempotency-Key: <uuid>
{ "line_items": [...], "buyer": {...}, "fulfillment_address": {...} }

→ HTTP 402 Payment Required
  WWW-Authenticate: Payment id="…", method="stripe", request="<base64url>"

# Agent reads the total back to the customer in plain English.
# Customer says "yes, buy it." Agent runs:
link-cli spend-request create --request-approval --amount <total_cents> ...

# Customer push-approves in Link app. link-cli returns the SPT.

# Phase 2 — charge (same body, same Idempotency-Key)
POST https://pima.io/mcp/buckmason/checkout
Authorization: Payment <SPT>
Idempotency-Key: <uuid>
{ ...same body..., "acknowledged_total_cents": <total_cents> }

→ 200 OK { "order_code": "ORD-AB12CD", "status": "processing", ... }
```

Confirm to the customer: order code, total charged, expected delivery from the order-tracking response (later visible via `GET /api/order_history?order_code=...`).

If the agent doesn't have `link-cli` set up or the customer hasn't opted into agent-driven payment, **do not** ask for card details or invent another purchase path. Stop and explain that fully agent-driven checkout requires Link approval through `link-cli`.
