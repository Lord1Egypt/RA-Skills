---
name: champro-api
description: CHAMPRO supplier toolkit covering everything CHAMPRO's PromoStandards services cannot reach — per-warehouse inventory (CHAMPRO publishes no INV endpoint at any version), order status and package tracking (no ODRSTAT, no OSN), ordering with a real sandbox (CHAMPRO registers no PromoStandards PO test endpoint, so the generic client refuses to send), decorated team orders with rosters and proof files, MOQ increments and lead-time catalogs, warehouse routing with split-shipment suborders, and the Custom Builder web-to-print flow (design sessions, proof/view downloads, order-from-design). JSON-in/JSON-out CLI actions over CHAMPRO's REST API and Custom Builder API, with local pre-flight that catches the documented rejections before an order is sent and a hard escalation path for partially-placed orders. Use for CHAMPRO stock or custom apparel sourcing, inventory, ordering, tracking, or Custom Builder embedding — and keep using the promostandards skill for CHAMPRO product data and pricing.
version: 0.1.0
emoji: 🏟️
homepage: https://devtools.champrosports.com/#devtools
metadata:
  openclaw:
    requires:
      bins: [python3]
    envVars:
      CHAMPRO_API_CUSTOMER_KEY:
        required: false
        description: >
          CHAMPRO API Customer Key (a GUID) for the REST API — ProductInfo,
          Inventory, PlaceOrder, OrderStatus. Generated on
          https://champrosports.com/AccountAndContactInfo. May instead be
          passed per call as `api_customer_key` in the stdin JSON, and on a
          delegated turn the runtime injects it, so it is deliberately not in
          requires.env. Treat as a secret.
      CHAMPRO_CB_CUSTOMER_KEY:
        required: false
        description: >
          CHAMPRO Custom Builder Embed Key — a DIFFERENT credential from the
          API Customer Key, generated separately on the same page. Used by the
          `cb-*` actions and as the iframe `lic` parameter. Confusing the two
          fails silently (see "Two keys, and they fail quietly"). Treat as
          account-scoped.
      CHAMPRO_API_BASE:
        required: false
        description: >
          Override for the REST API host. Defaults to
          https://api.champrosports.com. For testing against a mock only —
          sandbox vs production is chosen by URL path, not by this.
      CHAMPRO_CB_BASE:
        required: false
        description: >
          Override for the Custom Builder host. Defaults to
          https://cb.champrosports.com.
      CHAMPRO_TIMEOUT:
        required: false
        description: Per-request timeout in seconds. Defaults to 60.
    install:
      uv:
        - requests>=2.28
---

# CHAMPRO API

CHAMPRO publishes PromoStandards services, and the [`promostandards`](../promostandards)
skill already drives them. This skill is for the parts that standard cannot
reach for this supplier — which turns out to be most of the order lifecycle.

## Why this exists

CHAMPRO's registry entry lists exactly five endpoints. Run
`echo '{"config":"Champro"}' | python3 ../promostandards/scripts/ps.py capabilities`
and you get PRODUCT 2.0.0, PPC 1.0.0 and PO 1.0.0 — plus MED 1.1.0 and Company
Data, which that skill does not implement. **There is no INV service at any
version, no ODRSTAT and no OSN**, and every endpoint registers
`test_url: ""`.

That leaves four holes, and each is load-bearing:

| Need | Via PromoStandards | Via this skill |
| --- | --- | --- |
| Stock by warehouse | **nothing to call** — no INV endpoint exists | `check-inventory` — IL/CA/DR plus a restock date |
| "Where is my order" | **nothing to call** — no ODRSTAT, no OSN | `get-order-status` — status, carrier, tracking number, package contents |
| Rehearsing an order | PO 1.0.0 has **no test endpoint**, so `send-po` refuses outright | `place-order` — a real sandbox host, and it is the default |
| Decorated team orders | PO 1.0.0 cannot express a roster | `place-order` with CUSTOM — per-player name/number, proof file, team color |
| MOQ and lead times | PPC returns price breaks and charges, neither of these | `get-product-info` — MOQ, MOQCustom, lead times with surcharges |
| Design-to-order | no such concept in any spec | `cb-*` — Custom Builder sessions, proofs, order-from-design |

**Keep using `promostandards` for CHAMPRO product data and pricing.** Style,
color, size, description and price breaks all come from PRODUCT 2.0.0 and PPC
1.0.0, and this skill deliberately does not duplicate them.

## Three things that will bite you

**HTTP 200 does not mean it worked.** Verified against the live API: a bad key
returns 200 from every endpoint, with the failure buried under a different key
name each time — `Error` on ProductInfo and OrderStatus, `ResponseMessage` on
Inventory, `RequestErrors[]` on PlaceOrder, and *nothing at all* on the Custom
Builder's `GetOrderInfo`, which answers with a bare `[]`. Those captures are
checked in at `assets/fixtures/auth_failures.json` and the tests assert this
client treats every one as a failure. Never write a raw call against these
endpoints that branches on the status code.

**A rejected order is not the same as no order.** PlaceOrder answers a
partially-valid request by creating the suborders it liked *and* reporting
errors for the rest — CHAMPRO's own documented example does exactly this,
rejecting two SKUs for inventory while cutting two real suborders. There is no
cancel endpoint and no idempotency key, so resending is how you get duplicate
garments. `place-order` classifies this as `partial` and exits **3**
(`escalation_required`) with the suborder ids that now exist. Resubmit only the
failed lines, as a new order. Never the whole request.

**Sandbox is a URL, not a flag.** `/api/Order/PlaceOrder` is real;
`/api/OrderSandBox/PlaceOrder` is not. Worse, `/api/OrderSandBox/<anything>` is
a catch-all that routes every path to the sandbox place-order, while
`/api/Order/<bogus>` correctly 404s — verified live. So `client.py` never
assembles an order URL from caller input: `place_order()` takes a boolean and
picks the whole literal path. `production: true` is the only way to reach the
real host, and it is not the default.

## Two keys, and they fail quietly

| Credential | Env var | Used by |
| --- | --- | --- |
| **API Customer Key** | `CHAMPRO_API_CUSTOMER_KEY` | every REST action, and CB `place-order` |
| **Custom Builder Embed Key** | `CHAMPRO_CB_CUSTOMER_KEY` | `cb-get-design`, `cb-get-file`, `cb-embed-url` |

Both are generated on
[Account & Contact Info](https://champrosports.com/AccountAndContactInfo), and
swapping them produces no error message: `GetOrderInfo` returns `[]` and
`GetFile` returns 404 — indistinguishable from an empty design and an unknown
session. `cb-get-design` therefore reports `resolved: false` with an explicit
note rather than "0 items".

`PlaceOrder` additionally requires the **calling IP to be on the account's
allowlist** (error code 15); reads do not. On a hosted agent the egress address
is not the container's own and can change between runs. Run `check-access`
first — it prints the IP to paste into the allowlist and tells an invalid key
apart from an un-allowlisted one.

## Actions

```bash
echo '<json-args>' | python3 scripts/champro.py <action>
```

The action is `argv[1]`, arguments are a JSON object on stdin, and the result
is one JSON object on stdout — or `{"error": {...}}` with a non-zero exit.
Credentials come from the environment or inline (`api_customer_key`,
`cb_customer_key`), so they are omitted from the tables below.

**Setup**

| Action | Risk | stdin JSON |
| --- | --- | --- |
| `check-access` | read-only | `{}` — credentials, authenticated read, egress IP |

**Catalog** — the MOQ / lead-time gap in PPC

| Action | Risk | stdin JSON |
| --- | --- | --- |
| `get-product-info` | read-only | `{product_master}` or `{product_masters: [...]}` |
| `find-skus` | read-only | `{product_master, size?, configuration?, fabric?, color?}` |
| `get-lead-times` | read-only | `{product_master}` |

**Inventory** — no PromoStandards INV service exists for CHAMPRO

| Action | Risk | stdin JSON |
| --- | --- | --- |
| `check-inventory` | read-only | `{skus: [...]}` — per-warehouse stock + restock date |
| `plan-warehouses` | read-only | `{lines: [{sku, quantity}], prefer?}` — assign a warehouse that can cover each line |

**Orders** — no PromoStandards PO test endpoint exists for CHAMPRO

| Action | Risk | stdin JSON |
| --- | --- | --- |
| `validate-order` | offline (read-only with `product_masters`) | `{order \| orders, product_masters?, autowarehouse?}` |
| `preview-order` | offline | `{order \| orders}` — the exact body, no key in it |
| `split-mixed-cart` | offline | `{items, base}` — split CUSTOM out of STOCK (error 07) |
| `place-order` | **high — external write** | `{order \| orders, confirm, production?, autowarehouse?, product_masters?}` |

**Tracking** — no PromoStandards ODRSTAT or OSN service exists for CHAMPRO

| Action | Risk | stdin JSON |
| --- | --- | --- |
| `get-order-status` | read-only | `{order_numbers: [...]}` — **SubOrderIDs**, not PO numbers |
| `track-order` | read-only | `{place_order_result}` — follows every suborder at once |

**Custom Builder** — no PromoStandards equivalent in any spec

| Action | Risk | stdin JSON |
| --- | --- | --- |
| `cb-categories` | offline | `{}` |
| `cb-embed-url` | offline | `{category?}` — iframe src + ready-made tag |
| `cb-get-design` | read-only | `{session_id}` — roster, fabric, lead times |
| `cb-get-file` | read-only (writes a local file) | `{session_id, file_type, output_path?}` |
| `cb-place-order` | **high — external write** | `{session_id, ship_to, confirm, production?, po_number?, lead_time_id?}` |

**Reference**

| Action | Risk | stdin JSON |
| --- | --- | --- |
| `list-shipping-methods` | offline | `{carrier?, billing_type?}` |
| `explain-error` | offline | `{code}` or `{message}` |

Run `python3 scripts/champro.py` with no action for the full list.

## Rules that matter

**Validate before you send, because you cannot un-send.** `place-order` runs
every local rule first and refuses on a blocking finding. Pass
`product_masters` and it also checks SKUs, MOQ increments and lead-time names
against `ProductInfo`; without it those checks report as **`skipped`**, never
as passed — "not checked" and "checked and fine" must not look alike to a
caller about to place an order.

**MOQ is an increment, not a floor.** With `MOQCustom: 12`, a quantity of 18 is
rejected (error 25) even though it exceeds the minimum. The increment applies
to the **product-master total across the order's lines**, which is why a roster
of 6 + 6 is fine and 12 + 6 is not.

**Two gates on every write, guarding different mistakes.** `confirm: true`
means "send it"; `production: true` means "send it to the real host". They are
independent, and the default of both is the safe one. A sandbox order costs
nothing — CHAMPRO purges sandbox orders older than 30 days — so rehearse there
first, every time.

**One order is entirely STOCK or entirely CUSTOM** (error 07). A stock line
carries a `warehouse`; a custom line carries roster fields, and the order
carries a `lead_time` and a `proof_file_url`. `split-mixed-cart` separates a
mixed cart into two orders with suffixed PO numbers, since two orders cannot
share one PO.

**Follow suborders, not the PO.** One order can produce several suborders, one
per fulfilling warehouse, each with its own `SubOrderID` that ships and tracks
independently. `get-order-status` takes those ids; asking about only the first
reports "shipped" while the rest is still in production. `track-order` takes a
`place-order` result and follows all of them.

**Unreadable is not zero.** An inventory quantity that will not parse stays
`None` and the row is flagged `has_unreadable_quantity`, because "we could not
read the stock level" and "there is none" drive opposite decisions.

**Third-party and collect shipping need a payer account.** Twenty of the forty
published shipping methods bill someone other than your CHAMPRO account, and
those require `shipping_customer_account`. `validate-order` enforces it; a
method name outside the published list is rejected with near-matches.

**CHAMPRO fetches your proof file server-side.** A CUSTOM order's
`proof_file_url` must be a publicly reachable PDF/JPG/JPEG/PNG (errors 01 and
02). A `cb-get-file` URL carries your embed key and will not work there —
download the proof, host it, and pass that URL.

**CHAMPRO does not validate addresses; UPS does.** Ship-to must satisfy UPS
address rules or the order fails verification (errors 06 and 24). Validate
before submitting.

## Reference

- [`references/promostandards_gaps.md`](references/promostandards_gaps.md) —
  what CHAMPRO publishes, what it does not, and the evidence for each gap
- [`references/api_reference.md`](references/api_reference.md) — every endpoint,
  field and error code, with the observed-vs-documented differences
- [`references/custom_builder.md`](references/custom_builder.md) — the embed,
  the design-session lifecycle, and the order methods
- [`references/examples.md`](references/examples.md) — end-to-end flows
- `scripts/_selftest.py` — offline fixture tests, no network or credentials.
  Run it after any change: `python3 scripts/_selftest.py`
