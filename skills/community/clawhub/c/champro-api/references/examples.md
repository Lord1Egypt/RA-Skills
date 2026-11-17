# End-to-end flows

Every example is copy-pasteable from the skill directory. Credentials come from
`CHAMPRO_API_CUSTOMER_KEY` / `CHAMPRO_CB_CUSTOMER_KEY`, or add
`"api_customer_key": "…"` to any payload.

## 0. Before anything else

```bash
echo '{}' | python3 scripts/champro.py check-access
```

Confirms the key authenticates and prints the egress IP. Reads work without the
IP allowlist; `PlaceOrder` does not, so add that address under **API Allowed IP
Addresses** on the Account & Contact Info page before ordering. On a hosted
agent the address can change between runs — re-run this if a previously working
order starts failing with code 15.

## 1. Stock order: from a size list to tracking numbers

**Find the SKUs.** Sizes and fabrics are described in prose; SKUs are not.

```bash
echo '{"product_master":"JSBJ8","configuration":"YOUTH","fabric":"ACTIVE CLOTH"}' \
  | python3 scripts/champro.py find-skus
```

`ambiguous: true` means the filters matched more than one SKU — narrow them
rather than picking the first.

**Check stock and let the warehouses be chosen.**

```bash
echo '{"lines":[{"sku":"BBS44ABS","quantity":3},{"sku":"HJ2ABM","quantity":3}],
       "prefer":["IL","CA","DR"]}' \
  | python3 scripts/champro.py plan-warehouses
```

`order_items` comes back ready to paste into an order. A line marked `split`
needs more than one warehouse — CHAMPRO takes one warehouse per line, so that
means emitting two lines, which is your decision, not something to do silently.
A line marked `short` has a `more_expected_on` date if CHAMPRO has one.

**Validate, then rehearse, then commit.**

```bash
cat > /tmp/order.json <<'JSON'
{
  "order": {
    "po": "PO-2026-0412",
    "order_type": "STOCK",
    "ship_to_first_name": "DANA", "ship_to_last_name": "FRANK",
    "address": "220 STREET AVE", "city": "ROANOKE",
    "state_code": "VA", "zip_code": "24153",
    "phone": "5405551234", "is_residential": true,
    "shipping_method": "UPS GROUND",
    "items": [
      {"sku": "BBS44ABS", "warehouse": "CA", "quantity": 3},
      {"sku": "HJ2ABM",   "warehouse": "IL", "quantity": 3}
    ]
  },
  "product_masters": ["BBS44", "HJ2"]
}
JSON

python3 scripts/champro.py validate-order   < /tmp/order.json
python3 scripts/champro.py preview-order    < /tmp/order.json
```

`validate-order` with `product_masters` checks SKUs, MOQ increments and lead
times against the live catalog. Without it those report as `skipped`, not as
passed. `preview-order` shows the exact body — with no API key in it, so it is
safe to paste into a ticket.

```bash
# sandbox (the default) — costs nothing, purged after 30 days
jq '. + {confirm: true}' /tmp/order.json | python3 scripts/champro.py place-order

# production — only after the sandbox run looked right
jq '. + {confirm: true, production: true}' /tmp/order.json \
  | python3 scripts/champro.py place-order
```

**Track every suborder.** One order becomes one suborder per fulfilling
warehouse, each shipping independently.

```bash
jq '. + {confirm: true, production: true}' /tmp/order.json \
  | python3 scripts/champro.py place-order > /tmp/placed.json

jq '{place_order_result: .}' /tmp/placed.json \
  | python3 scripts/champro.py track-order
```

## 2. Custom order: a rostered team uniform

Custom orders need a lead time by name and a proof file CHAMPRO can fetch.

```bash
echo '{"product_master":"JSBJ8"}' | python3 scripts/champro.py get-lead-times
```

```bash
cat > /tmp/custom.json <<'JSON'
{
  "order": {
    "po": "PO-VALLEY-001",
    "order_type": "CUSTOM",
    "ship_to_first_name": "SAM", "ship_to_last_name": "REYES",
    "address": "12 SCHOOL RD", "city": "VALLEY",
    "state_code": "IL", "zip_code": "60007",
    "phone": "3125551234", "is_residential": false,
    "lead_time": "JUICE Standard",
    "proof_file_url": "https://cdn.example.com/proofs/valley-2026.pdf",
    "team_color": "RED",
    "items": [
      {"sku": "JSBJ8YACS", "quantity": 6, "team_name": "VALLEY", "player_name": "SCUBY", "player_number": "34"},
      {"sku": "JSBJ8YACL", "quantity": 6, "team_name": "VALLEY", "player_name": "EDNA",  "player_number": "30"}
    ]
  },
  "product_masters": ["JSBJ8"]
}
JSON

python3 scripts/champro.py validate-order < /tmp/custom.json
```

`JSBJ8` has `MOQCustom: 12`, and that is an **increment**: 6 + 6 passes, 12 + 6
does not. The rule applies to the product-master total across the order's
lines, not per line.

## 3. A mixed cart

One order is entirely STOCK or entirely CUSTOM (error 07).

```bash
echo '{
  "items": [
    {"sku": "BBS44ABS", "quantity": 3, "warehouse": "CA"},
    {"sku": "JSBJ8YACS", "quantity": 12, "team_name": "VALLEY", "player_name": "AL", "player_number": "7"}
  ],
  "base": {"po": "PO-9001", "ship_to_first_name": "SAM", "ship_to_last_name": "REYES",
           "address": "12 SCHOOL RD", "city": "VALLEY", "state_code": "IL",
           "zip_code": "60007", "phone": "3125551234"}
}' | python3 scripts/champro.py split-mixed-cart
```

Produces `PO-9001-S` and `PO-9001-C`, since two orders cannot share one PO.
Fill in each order's type-specific fields (shipping method / lead time and
proof), then submit them together as `orders: [...]`.

## 4. Third-party and collect freight

```bash
echo '{"billing_type":"BillThirdParty"}' \
  | python3 scripts/champro.py list-shipping-methods
```

Any method whose `billing_type` is set bills someone other than your CHAMPRO
account and requires the payer's carrier account:

```json
{"shipping_method": "UPS GROUND THIRD PARTY", "shipping_customer_account": "9999999"}
```

`validate-order` refuses the order without it.

## 5. Custom Builder: design → proof → order

```bash
echo '{"category":"FASTPITCH"}'      | python3 scripts/champro.py cb-embed-url
echo '{"session_id":"<id>"}'          | python3 scripts/champro.py cb-get-design
echo '{"session_id":"<id>","file_type":"ProofPdf","output_path":"/tmp/proof.pdf"}' \
  | python3 scripts/champro.py cb-get-file
```

If `cb-get-design` returns `resolved: false`, do **not** read that as an empty
design — CHAMPRO answers a wrong embed key and an unknown session id the same
way. Check `CHAMPRO_CB_CUSTOMER_KEY` is the *embed* key, not the API key.

Then either order the design directly:

```bash
echo '{"session_id":"<id>","po_number":"PO-7","lead_time_id":"EX",
       "ship_to":{"first_name":"SAM","last_name":"REYES","address1":"12 SCHOOL RD",
                  "city":"VALLEY","state":"IL","zip":"60007","phone":"3125551234"},
       "confirm":true}' \
  | python3 scripts/champro.py cb-place-order
```

…or host `/tmp/proof.pdf` somewhere public and place a REST CUSTOM order with
that URL and the roster from `cb-get-design`, which buys you `validate-order`'s
pre-flight and the sandbox host.

## 6. When an order comes back partial

```json
{"error": {"type": "escalation_required", "message": "PlaceOrder returned suborders AND errors: 2 suborder(s) were created (1212121, 1212133) alongside 2 error(s)…"}}
```

Exit code **3**. Those suborders are real garments in production and there is
no cancel endpoint.

1. `get-order-status` on each id in the message to confirm what exists.
2. Read the errors — `E2.8.3: <SKU> - Not enough Inventory.` names the failed
   lines.
3. Re-run `plan-warehouses` for those SKUs and submit them as a **new order
   with a new PO**.

Never resend the original request. It is not idempotent, and the half that
succeeded will succeed again.

## 7. Decoding an error

```bash
echo '{"code":"25"}' | python3 scripts/champro.py explain-error
echo '{"message":"E2.8.3: BP62YGHBPS - Not enough Inventory."}' \
  | python3 scripts/champro.py explain-error
```

`account_level: true` means no change to the order payload will help — the fix
is on the Account & Contact Info page or a call to CHAMPRO support.
