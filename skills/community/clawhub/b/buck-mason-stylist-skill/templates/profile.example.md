# Buck Mason shopper profile

Copy this file into your agent's persistent workspace as `profile.md` and fill in the fields you know. Skip anything optional — the agent will ask once if it needs something missing.

## Identity (optional, only needed for account linking + checkout)

- name: Jane Doe
- email: jane@example.com
- gender: m                         # m / w / u — used for catalog filters and recommend
- pima_api_key: pkLOMQfU1qM        # Buck Mason public Pima API key — required on every /api/* call (order tracking, returns). Not needed for /mcp/* (which is path-tenanted).
- pima_account_linked: false       # set true if you've logged in via /api/login_via_token (only needed for account/checkout/return flows)
- jwt: null                         # don't fill manually; agent stores after login_via_token returns
- link_payment_method: unconfirmed # unconfirmed / confirmed / none. Confirms a Stripe Link wallet with a linked payment method exists on the customer's phone. Required for MPP fully-agent-driven checkout (workflow #4 path B). When `confirmed`, the lookbook workflow defaults to the interactive `html-cart` format and the cart handoff routes through MPP. Set up Link at https://link.com or in any Stripe checkout flow.

## Link payment preferences (optional, MPP checkout only)

Store only card labels / last4 / purpose hints here. The agent resolves the live
Link payment-method id at checkout time with `link-cli payment-methods list` and
passes that id to `link-cli spend-request create --payment-method-id`. Do not
store Link internal payment-method ids, Stripe SPTs, raw card numbers, or CVVs.

```yaml
link_payment_methods:
  - name: "Personal Visa"
    brand: "visa"
    last4: "1234"
    purpose: "personal clothing"
  - name: "Company Amex"
    brand: "amex"
    last4: "9876"
    purpose: "business wardrobe"

preferred_link_payment_methods:
  clothing: "1234"   # normal personal Buck Mason purchases
  business: "9876"   # use only when the customer says this is for work
  default: "1234"
```

## Build (required for image-gen fidelity)

The image-gen pipeline uses these to render the garments **on a body that matches yours**, not on a generic model.

- height: 6'1"                        # imperial or metric (e.g., 185 cm)
- weight: 175 lb                       # imperial or metric (e.g., 79 kg)
- build: athletic-lean                 # athletic-lean / athletic / lean / average / muscular / stocky / heavy
- shoulder_width: average              # narrow / average / broad
- torso_length: average                # short / average / long
- leg_length: long                     # short / average / long
- posture: upright                     # upright / relaxed / forward
- age_range: late-30s                  # early-20s / mid-20s / late-20s / early-30s / mid-30s / late-30s / 40s / 50s / 60s+

## Face (required for image-gen fidelity)

- hair_color: salt-and-pepper          # natural-language description
- hair_style: short tousled, slightly graying at temples, darker on top
- beard: neatly trimmed greying stubble    # clean-shaven / stubble / short beard / full beard / mustache
- eye_color: hazel
- skin_tone: fair with light tan
- distinguishing_features: ""          # scars, piercings, tattoos visible above the neck, glasses always worn, etc.
- glasses: brown tortoiseshell aviator (worn outdoors / for driving) | none

## Sizes (required)

Use Buck Mason's size names — letter sizes for tops, waist x inseam for pants.

- shirt: L              # XS / S / M / L / XL / XXL
- tee: L
- short: M
- pant: 32x32           # waist x inseam
- jean: 32x32
- jacket: L             # for outerwear (peacoat, waxed jacket)
- sport_coat: 40R       # 36-46, S/R/L
- shoe: 10.5            # US men's
- belt: 34              # waist size

If you wear a different size in a specific Buck Mason cut (e.g. you size up in the boxy tee), note it under `cut_overrides`:

```yaml
cut_overrides:
  boxy_tee: XL
  field_pant: 33x32
```

## Fit prefs (optional)

- preferred_fit: standard          # slim / standard / relaxed
- shirt_length: tucked             # tucked / untucked
- pant_break: full                 # no / slight / full
- avoid: ["cropped", "drop-shoulder"]

## Color prefs (optional)

- favorites: [olive, indigo, navy, oat, tobacco, charcoal]
- avoid: [pastel pink, mustard yellow]
- neutrals: [white, oat, stone]

## Fabric prefs (optional)

- love: [oxford cotton, linen, melton wool, suede]
- avoid: [synthetics, polyester blends]

## Style ethos (optional but high-leverage)

A short tag the agent uses to bias **classic vs trend** and to phrase the "why" sentence on every lookbook pick. Pick one or two from the list, or write your own in the same form (8–14 words). See `references/style-reasoning.md`.

- style_ethos: "lived-in west-coast heritage basics, no logos, classics over trends"

Other examples:
- "modern Japanese minimalism, monochrome, clean line, no embellishments"
- "preppy New England, navy/white/khaki, classic cuts, low color saturation"
- "California workwear, raw denim, heavy boots, lived-in selvedge"
- "European editorial, mid-tones, tailored linen, leather over rubber"
- "low-key athletic minimalism, technical fabrics that don't look athletic"

The agent uses this to:
- weight `recently_live` results lower if the customer is anti-trend
- prefer cuts/colors that match the ethos when there's a tie
- write rationale sentences that reference the ethos by name

## Shipping address (required for checkout)

- address_line1: 123 Main St
- address_line2: Apt 4
- address_city: San Francisco
- address_state: CA
- address_zip: 94110
- address_country: US
- address_phone: 415-555-0101

## Home zip (required for "stores near me")

- home_zip: 94110

## Lookbook deploy voting (required for default Cloudflare voting)

- lookbook_votes_kv_id: ""           # Cloudflare KV namespace id for partner/stakeholder lookbook voting. Create once with:
                                    # CLOUDFLARE_ACCOUNT_ID=<acct> wrangler kv namespace create LOOKBOOK_VOTES

## Reference photos for try-on (recommended)

The agent uses these as identity anchors for image-gen. Provide **2–3 photos** if possible — one clean front-facing portrait, one full-body, optionally one in different lighting. They give the model multiple data points so it doesn't smooth your features into a generic model face.

- reference_photos:
    - path: ~/photos/me-portrait.jpg     # clean front-facing head-and-shoulders, neutral expression, no sunglasses
    - path: ~/photos/me-full-body.jpg    # standing, three-quarter or front, neutral pose
    - path: ~/photos/me-day.jpg          # optional: outdoor daytime for lighting reference

## Past orders (optional, agent can populate from /api/order_history if you log in)

```yaml
past_orders: []
```

## Budget defaults (optional)

- typical_outfit_budget: 400        # default total dollars per outfit when not specified
- max_per_item: 250                 # never recommend a single piece over this without confirming

These map to `?budget=` and `?max_price_per_item=` on `/mcp/recommend`.

## Notes (free text the agent should remember)

- I always size up in linen.
- I prefer pickup over shipping when a store is within 10 miles.
- I have a Buck Mason store credit balance — apply it before any coupon.
