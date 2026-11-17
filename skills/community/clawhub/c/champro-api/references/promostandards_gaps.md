# What CHAMPRO publishes over PromoStandards, and what it does not

This skill exists because of a specific, checkable set of gaps. This file
records them and how to re-verify each one, so a future reader can tell whether
CHAMPRO has since closed any of them.

## What the registry says

From the endpoint capture bundled with the `promostandards` skill
(`assets/promostandards_endpoints.json`, company code `CHAMPRO`):

| Service | Version | Status | Test endpoint |
| --- | --- | --- | --- |
| Company Data | 1.0.0 | Production | none |
| PPC (Product Pricing & Configuration) | 1.0.0 | Production | none |
| PO (Purchase Order) | 1.0.0 | Production | none |
| MED (Media Content) | 1.1.0 | Production | none |
| PRODUCT (Product Data) | 1.0.0 and 2.0.0 | Production | none |

All five live under `https://api.dc-onesource.com/xml/CHAMPRO/<SERVICE>/<VERSION>/soap`.

Re-check with:

```bash
echo '{"config":"Champro"}' | python3 ../promostandards/scripts/ps.py capabilities
```

which today reports PO 1.0.0, PPC 1.0.0 and PRODUCT 2.0.0, each with
`hasTestEndpoint: false`. MED and Company Data are absent because that skill
implements no adapter for them, not because CHAMPRO omits them.

## The gaps

### 1. No inventory service at all

`INV` does not appear at any version. This is not a version-coverage problem
the `promostandards` skill could fix with another adapter — CHAMPRO publishes
no inventory endpoint to call. Roughly two thirds of PromoStandards suppliers
are in the same position; CHAMPRO's answer is the REST `Inventory` endpoint,
which is *better* than INV 1.2.1 would have been (that version has no warehouse
breakdown anywhere in its schema) and comparable to 2.0.0, plus a
`MORE_EXPECTED_ON` restock date that neither version carries.

→ `check-inventory`, `plan-warehouses`

### 2. No order status and no shipment notification

Neither `ODRSTAT` nor `OSN` is published, so there is no standards path to an
order's status or its tracking numbers. The REST `OrderStatus` endpoint answers
both at once, keyed on the **SubOrderID** that PlaceOrder returns.

→ `get-order-status`, `track-order`

### 3. PO 1.0.0 exists, but there is no way to rehearse against it

Every CHAMPRO endpoint registers `test_url: ""`. The `promostandards` skill
refuses `send-po` outright when no test endpoint exists rather than falling
back to production — the right call, and it means the standards path offers no
rehearsal for CHAMPRO at all, only `preview-po`.

The REST API has a real sandbox host, `/api/OrderSandBox/PlaceOrder`, whose
orders CHAMPRO purges after 30 days. This skill defaults to it.

→ `place-order` (sandbox by default), `preview-order`, `validate-order`

### 4. PO 1.0.0 cannot express a decorated team order

CHAMPRO's custom business is rostered uniforms: a proof file, a team color, a
lead-time selection, and per-garment player name, number and size. PO 1.0.0 has
nowhere to put any of it. The REST CUSTOM order type carries all of it as
first-class fields.

→ `place-order` with `order_type: "CUSTOM"`

### 5. PPC carries no MOQ and no lead-time catalog

`getConfigurationAndPricing` returns quantity price breaks, FOB points,
decoration locations and charges. It does not return a minimum order quantity,
and it has no concept of a named lead time with a surcharge. Both are hard
requirements for a CHAMPRO order — a quantity that is not a multiple of the MOQ
is error 25, and an unrecognised lead-time name is error 22.

→ `get-product-info`, `get-lead-times`

### 6. Warehouse routing, split shipments, and shipping-method selection

A STOCK order line names its own warehouse (or delegates to
`Autowarehouse: "YES"`), and CHAMPRO answers with one **suborder per fulfilling
warehouse**. It also takes a `ShippingMethod` from a published list of forty,
twenty of which bill a third party or the recipient and therefore require a
carrier account. None of this is modelled in PO 1.0.0.

→ `plan-warehouses`, `list-shipping-methods`, `place-order`

### 7. The Custom Builder has no analogue in any spec

A web-to-print configurator embedded by iframe, producing a Design Session ID
that is then the handle for the roster, the proof PDF, four view renders, and
placing the order. No PromoStandards service describes anything like it.

→ `cb-embed-url`, `cb-get-design`, `cb-get-file`, `cb-place-order`

## What stays with `promostandards`

**Product data and pricing.** PRODUCT 2.0.0 and PPC 1.0.0 are published, in
production, and the generic client drives them correctly. Styles, colors,
sizes, descriptions, price breaks, FOB points, decoration locations and charges
all belong there, and this skill deliberately does not duplicate them.

The REST `ProductInfo` endpoint overlaps slightly — it returns the sellable SKU
grid — but it exists here for what PPC lacks: MOQ, MOQCustom and the lead-time
catalog. Use it for those, and for resolving a size/fabric description to an
orderable SKU.

**Media.** CHAMPRO publishes MED 1.1.0. The `promostandards` skill has no
adapter for it yet, so product imagery is reachable today only by calling that
endpoint directly. Adding a MED adapter there is the right fix — not another
endpoint here.

## Re-verifying

Auth-failure shapes were captured live on 2026-08-21 with an all-zeros key and
are checked in at `assets/fixtures/auth_failures.json`. To re-capture:

```bash
K=00000000-0000-0000-0000-000000000000
curl -sS "https://api.champrosports.com/api/Order/ProductInfo?ProductMaster=JSBJ8&APICustomerKey=$K"
curl -sS -X POST https://api.champrosports.com/api/Order/Inventory \
  -H 'Content-Type: application/json' \
  -d "{\"APICustomerKey\":\"$K\",\"Orders\":[{\"OrderItems\":[{\"SKU\":\"BBS44ABS\"}]}]}"
```

Both return HTTP 200. If CHAMPRO ever starts returning real status codes, the
tests in `scripts/_selftest.py` will still pass — they assert the body is
treated as authoritative, which stays correct either way.
