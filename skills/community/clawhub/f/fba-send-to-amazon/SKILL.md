---
name: fba-send-to-amazon
description: Create FBA inbound plans (Send to Amazon) via SP-API v2024-03-20 — identical-box packing for an even multi-warehouse split and $0 placement fee, carrier booking (Amazon SEND, partnered or your own), box-label download and square-sticker formatting. Use when asked to send inventory to FBA, create an inbound plan/shipment, book a freight carrier for an inbound, or print box labels. Triggers, send to amazon, STA, inbound plan, FBA shipment, box label, placement fee, Amazon SEND, partnered carrier, FBA发货, 创建入库计划, 箱唛.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📦"
    requires:
      bins:
        - python3
      config:
        - ~/.config/sp-api/credentials.json
    envVars:
      - name: LWA_CLIENT_ID
        required: false
        description: LWA client id (or put it in the credentials file)
      - name: LWA_CLIENT_SECRET
        required: false
        description: LWA client secret (or put it in the credentials file)
      - name: SPAPI_REFRESH_TOKEN
        required: false
        description: SP-API refresh token (or put it in the credentials file)
    homepage: https://claw-school.com
---

# FBA inbound plans (SP-API v2024-03-20)

End-to-end: create the plan, pack it so Amazon splits it evenly across
warehouses at $0 placement fee, book the carrier, print box labels.

Read §1 before the first run with new SKUs — it is a browser step the API
cannot do. If a call fails, go to §7 before acting on what the error says.

Part of the Amazon operations skill set from **[Claw School](https://claw-school.com)**.
Its companion, [`amazon-send-catch-invoice`](https://claw-school.com), picks up
where §10 leaves off and produces the customs paperwork.

Amazon's own reference for this API is the
[Fulfillment Inbound v2024-03-20 use-case guide](https://developer-docs.amazon.com/sp-api/docs/fulfillment-inbound-api-v2024-03-20-use-case-guide).

## Before you start — ask the user

Do not guess these. Confirm with the user, once, up front:

| Question | Why it matters |
|---|---|
| Which MSKUs and total quantities? | Drives the whole plan |
| **Split across several warehouses, or keep it to fewer boxes?** | The even split is a *choice*, not the default best answer — see below |
| How many boxes, and are all boxes identical? | Identical boxes are what makes an even split possible (§3) |
| Box dimensions and gross weight? | Required by `setPackingInformation` |
| Ship-from address and pickup contact? | Required; a wrong contact fails confirmation misleadingly |
| Which carrier and service level? | Run `list_carriers.py` and have the user pick the exact string |
| Any new SKUs in this batch? | New SKUs need a prep category set in a browser first (§1) |

### The multi-warehouse split is optional — decide it with the user, early

Raise this **the moment you have the SKU × quantity list**, before building
anything. Splitting into N identical boxes across N fulfillment centres avoids
the placement fee, but it is not automatically the right call:

| Situation | Better choice |
|---|---|
| Enough volume to fill several boxes, freight priced per shipment | Split — the placement fee saved usually beats the extra per-shipment freight |
| Total weight or volume too low to justify several boxes | **Fewer boxes**, accept the placement fee. Sea freight often has a per-shipment minimum, and several under-filled boxes can cost more than the fee |
| User just wants the smallest number of boxes to handle | Fewer boxes. Their time and the warehouse's handling cost are real |

Ask plainly: *"This can go out as N identical boxes to N warehouses with no
placement fee, or as fewer boxes to fewer warehouses with a placement fee of
roughly $X. Which do you want?"* You will know the real fee after
`generatePlacementOptions` (§3.3) — if the user is undecided, run that far and
show them the actual numbers before confirming.

If they choose fewer boxes, nothing else in this skill changes: set
`num_boxes` accordingly and let `confirmPlacementOption` pick the cheapest
option, which may well be a paid single-warehouse one.

## Files

```
scripts/
├── spapi.py                 minimal SP-API client (LWA token + retrying requests)
├── create_inbound_plan.py   the full flow, driven by a JSON config
├── plan.example.json        config template — copy and fill in
├── list_carriers.py         discover the exact carrier strings your account is offered
├── get_labels.py            download labels, split FBA/carrier, square them up
└── void_plan.py             cancel a plan, guarded by an exact shipment fingerprint
```

Credentials: `~/.config/sp-api/credentials.json`, or the `LWA_*` /
`SPAPI_REFRESH_TOKEN` environment variables. Never hardcode them, never commit
them. `python3 scripts/spapi.py` prints a smoke test.

Dependencies: stdlib only, except `get_labels.py`, which needs
`pip3 install pymupdf numpy` for the split and square steps.

---

## 1. Prerequisite: new SKUs need a prep category

A new MSKU's first inbound fails with `FBA_INB_0182` until its prep category is
set, and **there is no SP-API call that sets it**. It can only be done in
Seller Central, in a browser.

### Ask the user first — do not just open a browser

This needs a browser already **signed in to Seller Central**, which is the
user's own session. Don't launch one unannounced. Tell them what is needed and
let them choose:

> These SKUs have no prep category yet, and the API can't set one — it has to
> be clicked in Seller Central. Two options:
>
> **A. You do it** — it's about a minute. Send to Amazon → start a draft with
> these SKUs → for each one click *Prep and labeling details needed* →
> *Choose prep category* → usually **No prep needed** → Save → then void the
> draft. Tell me when it's done.
>
> **B. I do it** — I'll need to drive a browser that's already logged into your
> Seller Central. Want me to go ahead?
>
> Either way, please confirm the right category per SKU. *No prep needed* is
> the common answer but it is not always correct, and it is your declaration.

**Default to A.** It is faster than explaining, it keeps the user's session
under their control, and they are the one who can actually judge the category.
Only take B if they ask for it and browser tooling is available.

### If the user picks B

1. Open **Send to Amazon**, start a throwaway workflow containing the new SKUs.
2. Per SKU: **Prep and labeling details needed** → **Choose prep category** →
   the category the user confirmed → Save.
3. **Void the throwaway workflow** when every SKU is set.
4. Then run the API flow below.

Two things break naive automation of this page:

- The STA page is a React micro-frontend and its modals (`kat-modal`) live in
  **shadow DOM**. Ordinary selectors don't reach them; pierce the shadow root,
  e.g. via `evaluate_script`.
- The void button's **DOM text is "Confirm"** even though it renders as
  "Void workflow". Matching the visible label finds nothing.

Prefer a DOM snapshot over screenshots here — it's text, far cheaper, and the
state you need (which SKUs still lack a category) is all in the DOM.

---

## 2. The call order

Order errors fail silently or with misleading messages.
**`setPackingInformation` must run after `confirmPackingOption` and before
`confirmPlacementOption`.**

```
createInboundPlan
  → generatePackingOptions → listPackingOptions      (gives packingOptionId + packingGroups)
  → confirmPackingOption
  → setPackingInformation                            (uses packingGroupId, NOT packingOptionId)
  → generatePlacementOptions → confirmPlacementOption (pick the $0 option)
  → generateTransportationOptions
  → [book a delivery window ONLY if preconditions demand it]
  → confirmTransportationOptions                     (contactInformation goes here)
```

Every POST/PUT returns an `operationId`. Poll `GET /operations/{id}` until
`operationStatus == "SUCCESS"` — **not `"SUCCEEDED"`**, which never appears.

---

## 3. Even multi-warehouse split at $0 placement fee

**Only if the user chose it** (see "Before you start"). If they want fewer
boxes instead, skip to §3.3 — the packing mechanics below still apply, you just
declare fewer boxes and accept whatever placement option is cheapest.

Two things make the even split work.

### 3.1 Express N identical boxes as `quantity: N`

`BoxInput.quantity` means "number of containers identical in weight,
dimensions and contents". **Five identical boxes = one box object with
`quantity: 5`**, not five box objects.

That tells Amazon the box is an indivisible atom, so placement can only hand
out whole boxes — the split comes out even by construction.

> Skip packing info and Amazon re-splits freely by SKU. A 445-unit plan came
> back as 90 / 106 / 85 / 60 / 104 units per shipment: five different box
> contents, five different pick lists, and placement fees.

### 3.2 The `setPackingInformation` body — every field here is a trap

```python
box = {
    "contentInformationSource": "BOX_CONTENT_PROVIDED",   # required; omitting it returns 403
    "dimensions": {"length": 40, "width": 30, "height": 30, "unitOfMeasurement": "CM"},
    "weight":     {"unit": "KG", "value": 7.5},
    "quantity":   5,                                      # 5 identical boxes
    "items": [{"msku": ..., "quantity": <per box>,
               "labelOwner": "SELLER", "prepOwner": "SELLER"}],   # both required
}
body = {"packageGroupings": [{"packingGroupId": group_id, "boxes": [box]}]}
```

| Don't send | Do send |
|---|---|
| `packingOptionId` | `packingGroupId` — there is no packingOptionId field in this schema |
| `boxId` | nothing; it is output-only |
| items with only msku + quantity | add `labelOwner` and `prepOwner` |
| (omitted) `contentInformationSource` | required |

If `listPackingOptions` returns **more than one packing group**, these SKUs
cannot share a box type. Amazon will demand separate boxes per group and an
identical-box split is impossible as configured — tell the user and either
split the plan or change the SKU set.

### 3.3 Pick the $0 placement option

A typical response offers a multi-warehouse split at $0 alongside several
single-warehouse consolidations at a fee. The $0 option means you ship to
several fulfillment centres yourself and Amazon charges nothing to
redistribute. `create_inbound_plan.py` always picks the cheapest and prints the
full list so you can see what was rejected.

---

## 4. Booking the carrier

Never guess the carrier string. It is account- and lane-specific:

```bash
python3 scripts/list_carriers.py <planId>
```

That prints every offered option with its exact `carrier.name`,
`shippingMode`, `shippingSolution`, price, and preconditions. Paste the one the
user picks into the config:

```json
"carrier": {
  "shipping_mode": "OCEAN_LCL",
  "shipping_solution": "AMAZON_PARTNERED_CARRIER",
  "name": "<exact string from list_carriers.py>"
}
```

> Forwarder service names rarely match Amazon's strings. A service the
> forwarder sells as "expedited shipping / courier delivery" may appear in the
> API as `<Carrier> Ocean LCL Expedited Courier`. Match on the API string, and
> have the user confirm it is the service they actually bought.

### Delivery window: SEND doesn't need one, most other carriers do

**Amazon SEND is the exception, not the rule.** A SEND carrier's options come
back with no preconditions and no window is booked. Almost everything else —
your own carrier's SPD/LTL, FIST carriers, and so on — requires a confirmed
delivery window before transportation can be confirmed.

| Carrier | Delivery window |
|---|---|
| **Amazon SEND** | **Not required** — `preconditions` comes back `[]` |
| Your own carrier, SPD / LTL | Required — `['CONFIRMED_DELIVERY_WINDOW']` |
| FIST carriers | Required |
| Anything else | Assume required until the option says otherwise |

**Read `preconditions` per option; never hardcode either answer.** The field is
the authority — it accounts for carrier, lane and account in a way no lookup
table can, and it is what breaks first when Amazon changes a program.

```python
if "CONFIRMED_DELIVERY_WINDOW" in (option.get("preconditions") or []):
    confirm_delivery_window(plan_id, shipment_id)
```

`list_carriers.py` prints `preconditions` for every offered option, so you can
see which way a given carrier goes before committing to it.

### contactInformation goes in the confirm request

The carrier collects from you, so it needs a pickup contact — and that contact
belongs inside `transportationSelections`, per the official
`ConfirmTransportationOptionsRequest` example. Not in the generate request.

Omit it and you get `FBA_INB_0117 "partnered carrier is unavailable at the
moment"`, which reads like an Amazon outage. It is not. Believing the message
cost roughly a dozen pointless retries.

```python
selections = [{"shipmentId": sid,
               "transportationOptionId": option_id,
               "contactInformation": {"name": ..., "phoneNumber": ..., "email": ...}}]
```

### Other traps

- `readyToShipWindow` is a `WindowInput`: it has **only `start`**, no `end`.
- Only `shipmentId` + `readyToShipWindow` are required per shipment.
  `freightInformation` (including `declaredValue`) and `pallets` are optional —
  **don't send optional fields you don't need**; the carrier still quotes.
- **Transportation option ids are single-use.** A failed confirm consumes them;
  reusing one returns `FBA_INB_0348 "not AVAILABLE"`. Every retry must
  regenerate and reselect, not re-post the same payload.

---

## 5. Box labels

**2024-03-20 has no box-label endpoint.** Its `createMarketplaceItemLabels` is
for FNSKU item labels, something else. Box labels come from v0, whose read
operations still work:

```
GET /fba/inbound/v0/shipments/{FBA_ID}/labels
    ?MarketplaceId=…&PageType=…&LabelType=UNIQUE
    &PackageLabelsToPrint=<boxId>      # repeatable, one per box
```

Box ids come from 2024-03-20's `listShipmentBoxes` → `boxId`
(e.g. `FBA1XXXXXXXXU000001`) and **only exist after `setPackingInformation`**.

### PageType controls page size *and* whether the carrier label exists

| PageType | Size | Pages | Note |
|---|---|---|---|
| `PackageLabel_Letter_2` / `A4_2` | 8.5×11" | 2 | FBA page sideways |
| `PackageLabel_Thermal` | 4.2×6" | 2 | carrier page sideways |
| **`PackageLabel_Thermal_No_Carrier_Rotation`** | **4.2×6"** | **2** | **both upright** ← default |
| `Letter_6` / `A4_4` / `Plain_Paper` / `Thermal_NonPCP` | — | 1 | ⚠️ **no carrier label** |
| `Letter_4` | — | — | rejected in some marketplaces |

The `*_NonPCP` and single-page types **silently drop the partnered-carrier
label**. Never use them while shipping PCP — you'd print box labels with no
carrier label and the pickup would be refused.

### Splitting and squaring

Page 1 is the Amazon box label (has extractable text); page 2 is the carrier
label (raster only). **Classify by content, not page index** — order is not
guaranteed and multi-box shipments misfile otherwise.

`--square [mm]` re-lays each label onto a square canvas: measure true ink
bounds by rendering (so barcodes count), scale uniformly, centre. Uniform
scaling matters — a stretched barcode has out-of-spec bar widths and strict
scanners reject it. Content is embedded as vector, never rasterised.

```bash
python3 scripts/get_labels.py <planId> --square        # 100×100mm stickers
python3 scripts/get_labels.py <planId> --square 80     # 80×80mm
python3 scripts/get_labels.py <planId>                 # raw 4×6 thermal
python3 scripts/get_labels.py <planId> --page-type PackageLabel_Letter_2
```

Output: `labels/fba_<FBA>_<FC>.pdf`, `labels/carrier_<FBA>_<FC>.pdf`.
Use `--carrier-prefix <name>` to name the forwarder label after your forwarder.

---

## 6. Cancelling a plan

```
PUT /inboundPlans/{id}/cancellation      # not DELETE, not POST /void
```

```bash
python3 scripts/void_plan.py <planId> --expect FBA1... FBA2... FBA3...        # dry run
python3 scripts/void_plan.py <planId> --expect FBA1... FBA2... FBA3... --yes  # do it
```

The `--expect` set must match the plan's shipments **exactly** — a subset match
is refused, because a superset means you're about to cancel shipments you never
listed. Dry run is the default.

> ⚠️ Never leave an unattended background loop cancelling shipments. However
> tight the predicate looks, a human should confirm each destructive run.

### listInboundPlans lags badly

A newly created ACTIVE plan can be missing from `listInboundPlans` for **many
hours** (voided ones appear sooner). Consequences:

- **Always capture the plan id when you create it.** `python3 -u … | tee run.log`.
  Losing it is genuinely hard to recover from.
- **Most reliable lookup — Seller Central's internal endpoint**, from a browser
  already signed in to Seller Central. It resolves instantly when SP-API can't:
  ```js
  const r = await fetch(`/fba/shippingqueue/api/v1/shipment/queryShipment?shipmentId=FBA1XXXXXXXX`,
                        {headers: {accept: 'application/json'}, credentials: 'include'});
  const j = await r.json();   // j.workflowId IS the inboundPlanId
  ```
  Shipments from the same batch return the same `workflowId`, which is how you
  prove which shipments belong to which plan.
- Or list shipments by date range through v0:
  ```
  GET /fba/inbound/v0/shipments?MarketplaceId=…&QueryType=DATE_RANGE
      &LastUpdatedAfter=…&LastUpdatedBefore=…&ShipmentStatusList=WORKING
  ```
  Shipment names carry a timestamp, which distinguishes batches. With
  `QueryType=SHIPMENT`, pass only `ShipmentIdList` and no status list; several
  ids at once get truncated by pagination, so query them one at a time.

---

## 7. Troubleshooting: Amazon's error codes lie

When something fails, this is the section to read first — because the error
text will usually point you somewhere else.

**Parameter errors routinely masquerade as permission errors or service
outages.** This flow hit that four separate times:

| Error | Looks like | Actually |
|---|---|---|
| `403 Unauthorized` on setPackingInformation | Missing API role | Wrong field names / missing required fields in the body |
| `403 Unauthorized` on label download | Missing API role | **The path does not exist** — 2024-03-20 has no label endpoint |
| `FBA_INB_0117 partnered carrier is unavailable at the moment` | Amazon outage | `contactInformation` sent at the wrong nesting level |
| `FBA_INB_0348 not AVAILABLE` | The option expired | Option ids are single-use; a failed confirm consumed it |
| `FBA_INB_0182` on createInboundPlan | A plan problem | A SKU has no prep category — fix it in the browser (§1) |
| `Value null at 'cartonIdList'` | Parameter is named cartonIdList | It is `PackageLabelsToPrint`; cartonIdList is an internal name |
| `operationStatus` never reaches SUCCEEDED | Timeout | The success value is `SUCCESS`; `SUCCEEDED` never appears |

**Before believing an error, diff your request against the official model spec
field by field.** And always print the HTTP response body — the status line
alone tells you nothing, and an unexplained `HTTP Error 403:` is how a
one-line parameter fix turns into half a day of debugging API permissions.

```bash
curl -sL https://raw.githubusercontent.com/amzn/selling-partner-api-models/main/models/\
fulfillment-inbound-api-model/fulfillmentInbound_2024-03-20.json -o /tmp/fbainb.json
# v0 model (for box labels): .../fulfillmentInboundV0.json
```

---

## 8. Network robustness

SP-API drops SSL connections occasionally (`SSLEOFError`). Every request needs
a retry, or a mid-flow crash leaves an **orphan plan**: placement confirmed,
shipments created, plan id lost and unsearchable for hours.

```python
except (urllib.error.URLError, OSError):            # SSL / socket drop
    time.sleep(2 ** attempt); continue
except urllib.error.HTTPError as e:
    if e.code in (429, 500, 502, 503, 504):
        time.sleep(2 ** attempt); continue
    raise RuntimeError(f"HTTP {e.code}: {e.read().decode()}")   # ALWAYS print the body
```

Not printing the body is how a parameter error becomes an unexplained
`HTTP Error 403:` and half a day of debugging the wrong thing. `spapi.py`
does this for you.

---

## 9. Full run

```bash
cp scripts/plan.example.json my-plan.json
# fill in SKUs, box spec, addresses, contact — then discover the carrier:

python3 -u scripts/create_inbound_plan.py my-plan.json | tee run.log   # tee: keep the plan id
python3 scripts/list_carriers.py <planId>          # if the carrier string was wrong
python3 scripts/get_labels.py <planId> --square
```

Results land in `my-plan-result.json`: plan id, and per shipment the FBA id,
Amazon reference id, warehouse code, real box ids, box count, unit count and
item detail.

---

## 10. After shipping: customs paperwork

Forwarders usually want a customs invoice (HS codes, product names, declared
unit values, materials, product photos). Everything Amazon-side that the
invoice needs is already in the API:

```python
d  = GET /inbound/fba/2024-03-20/inboundPlans/{plan}/shipments/{sid}
bx = GET /inbound/fba/2024-03-20/inboundPlans/{plan}/shipments/{sid}/boxes

d["shipmentConfirmationId"]            # FBA id
d["amazonReferenceId"]                 # Amazon reference id
d["destination"]["warehouseId"]        # warehouse code
sum(b.get("quantity", 1) for b in bx)  # box count
bx[0]["boxId"]                         # box code — take it, don't derive it
```

**Use the API's `boxId` verbatim.** Its format is `FBA<id>U000001` — U plus
**six** digits. Deriving `f"{fba}U{seq:05d}"` gives five digits and won't match
the physical box label, which the forwarder will reject at check-in.

### Generating the invoice itself

If the SEND carrier you booked in §4 is **CATCH (凯琦)**,
[Claw School](https://claw-school.com) publishes a companion skill that finishes
the job:

> **[`amazon-send-catch-invoice`](https://claw-school.com)** — fills CATCH's
> invoice template from your own product data, takes the FBA ids / reference
> ids / box codes straight out of this skill's result file, and uploads over
> pure HTTP, which is how the order is actually placed with CATCH.

Hand it `<config>-result.json` from §9 and it needs nothing else from Amazon.

For a different forwarder, the same skill is still a reasonable starting point —
the Amazon-side data extraction and the Excel/image handling are generic; the
portal client and the template cell map are the parts you would swap.

---

*`fba-send-to-amazon` is maintained by [Claw School](https://claw-school.com),
which publishes agent skills for Amazon sellers — sourcing, listings, ads,
inbound logistics and customs.*
