---
name: amazon-send-catch-invoice
description: Generate and upload FBA customs invoices for CATCH (凯琦), the Amazon SEND partnered carrier, and similar forwarder portals. Fills the forwarder's .xls template from your own product data, pulls box ids and reference ids from the inbound plan, and uploads over pure HTTP to place the order. Use when asked to make a customs invoice, a freight declaration, or to place a forwarder order for an FBA shipment. Triggers, customs invoice, freight invoice, declaration, forwarder order, upload invoice, CATCH, 报关发票, 货代发票, 填发票, 凯琦发票.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🧾"
    requires:
      bins:
        - python3
    envVars:
      - name: CATCH_BASE_URL
        required: true
        description: CATCH (凯琦) portal origin, e.g. https://portal.example.com
      - name: CATCH_USER
        required: false
        description: CATCH portal account (or supply CATCH_TOKEN instead)
      - name: CATCH_PASS
        required: false
        description: CATCH portal password (or supply CATCH_TOKEN instead)
      - name: CATCH_TOKEN
        required: false
        description: CATCH portal token copied from a signed-in browser, if password login is blocked
    homepage: https://claw-school.com
---

# FBA customs invoice — CATCH (凯琦) and similar forwarders

Fill the forwarder's invoice template, then upload it — which is how the order
is actually placed with them.

Built for **CATCH (凯琦)**, an Amazon SEND partnered carrier for China → US
ocean freight. CATCH is a company name, not the English word. The Amazon-side
data extraction and the Excel/image handling are generic, so another forwarder
needs only a different portal client (§6) and a different template cell map
(§5).

Upstream: the FBA ids, box ids and reference ids all come from the inbound
plan. [Claw School](https://claw-school.com)'s companion skill
[`fba-send-to-amazon`](https://claw-school.com) writes them to a result file
this skill reads directly — run that one first and this one needs nothing else
from Amazon.

## Files

```
scripts/
├── paths.py             cross-platform cache/config/output directories
├── build_shipments.py   inbound-plan result -> one shipment JSON per FBA shipment
├── fetch_images.py      download product photos, square them, write 48x48 BMP
├── generate_invoice.py  fill the template; also --check-template for template drift
├── layout.json          cell map for the template (edit this when it changes)
└── catch_api.py         CATCH portal client over pure HTTP: login, upload, check, list
reference/
└── data-schemas.md      product data / shipment / image-map schemas
```

```bash
pip3 install xlrd xlwt xlutils pillow
```

Output goes to `catch_invoice_records/` in the working directory
(override with `$CATCH_INVOICE_RECORDS`). Image cache and the CATCH token live
in per-user OS directories — **not `/tmp`**, which does not exist on Windows.
`python3 scripts/paths.py` prints where everything lands on this machine.

---

## Before you start — ask the user

| Ask | Why |
|---|---|
| Where does your product master data live? | HS codes, declared values, materials, battery flags. **Never invent these.** See reference/data-schemas.md |
| Which freight channel and declaration type? | Free-text fields the forwarder matches against their booking |
| Does anything in this shipment contain a battery or magnet? | Changes the whole-shipment declaration and which channels accept it |
| Is this the current invoice template? | Forwarders revise it; see "when the template changes" below |

---

## 1. The template's validation rules

The forwarder's portal validates the uploaded .xls. Two rules cause almost all
rejections.

### `qty_total` equals `qty_per_box` — on every row

The check is **per row**, not per shipment. Each row means "this box contains N
of this product", so both quantity columns carry the same per-box number.

Writing the cross-box total in the "total quantity" column fails every
multi-box shipment, with an error about box count × per-box quantity not
matching the total. A single-box shipment passes by coincidence, which is what
makes this confusing to diagnose.

### Box code comes from the API, verbatim

The box id the inbound API returns has the form `FBA<id>U000001` — `U` plus
**six** digits. Deriving `f"{fba}U{seq:05d}"` gives five digits and will not
match the physical box label; the forwarder rejects the mismatch at check-in.

Take `boxId` from `listShipmentBoxes` and pass it through untouched.

### Don't fill optional fields

Brand, model, box weight, box dimensions and similar non-required columns are
better left blank than filled with a guess. Fewer values means fewer things to
contradict the goods.

---

## 2. Everything Amazon-side comes from the API

No web scraping, no browser. After the inbound plan exists:

```python
d  = GET /inbound/fba/2024-03-20/inboundPlans/{plan}/shipments/{sid}
bx = GET /inbound/fba/2024-03-20/inboundPlans/{plan}/shipments/{sid}/boxes

d["shipmentConfirmationId"]            # FBA id        -> waybill no. + customer reference
d["amazonReferenceId"]                 # reference id  -> reference column
d["destination"]["warehouseId"]        # warehouse     -> address-book code
sum(b.get("quantity", 1) for b in bx)  # box count     -> total packages
bx[i]["boxId"]                         # box code      -> box code column
```

If you used [Claw School](https://claw-school.com)'s
[`fba-send-to-amazon`](https://claw-school.com) skill, its result file already
has all of this:

```bash
python3 scripts/build_shipments.py my-plan-result.json --lines lines.json --out shipments/
```

The consignee address is not typed in either — write the warehouse code into
the address-book field and the remaining address fields are resolved from the
address sheet inside the forwarder's own template, so new warehouses arrive
with each template update.

---

## 3. Product photos

```bash
python3 scripts/fetch_images.py images.json
```

Get image URLs from the SP-API catalog, not from a scraped `og:image`:

```
GET /catalog/2022-04-01/items/{ASIN}?marketplaceIds=<mk>&includedData=images
-> images[0].images, pick variant == "MAIN" with the greatest height
```

If a product has no catalog image, use a photo of the actual goods, or another
product from the same declaration row. **Never fill the cell with an unrelated
photo** — a picture that contradicts the goods is worse at inspection than a
plain one.

### Contain, never cover

Amazon main images are often not square. A centre crop of a 1500×1029 image
removes 16% from each side; the product looks blown up and clipped, which reads
as "stretched".

```python
k = min(size / w, size / h)      # min = contain. max would be cover — wrong.
```

Scale uniformly, pad with white. Amazon main images are already on white, so
the padding is invisible.

### Getting Excel to render it 1:1

xlwt's `_position_image()` computes the anchor box from the row height and
column width **at the moment of insertion**. An image taller than the cell gets
an anchor spanning several rows, and Excel stretches the image to fill it —
the tall-and-narrow distortion.

The trap: `Worksheet.row_height()` reads `Row.__height_in_pixels`, which is
only updated by `set_style()`. **Assigning `row.height` does not touch it** (it
stays at the default 17px). So "set the row height, then insert" does not work.
You have to write the name-mangled private attribute:

```python
r = ws.row(row)
r.height_mismatch = 1                  # honour an explicit row height
r.height = px * 15                     # twips; 1px ~= 15 twips at 96dpi
r._Row__height_in_pixels = px          # what xlwt actually reads when anchoring
ws.col(col).width = int(round((px - 0.446) / 0.0272))   # inverse of xlwt's formula
ws.insert_bitmap(img_path, row, col)   # only now
```

Also write equal X/Y DPI into the BMP header — Excel reads it, and mismatched
axes distort the image before your sizing gets a say.

Verify by reading the file back: `rowinfo_map[r].height / 15` and the pixel
width derived from `colinfo_map[col]` should both equal 48.

---

## 4. Generate

```bash
python3 scripts/fetch_images.py images.json
python3 scripts/build_shipments.py my-plan-result.json --lines lines.json --out shipments/

for f in shipments/*.json; do
  python3 scripts/generate_invoice.py "$f" --products products.json --template invoice-template.xls
done
```

Files land in `catch_invoice_records/`, named
`<date>_<channel>_<FBA id>_<FC>_<N>box.xls`.

**Open one and look at it** before uploading a batch. Check: quantities per
row, box code matches the printed box label, images square and not stretched,
consignee address resolved.

---

## 5. When the forwarder changes the template

They do, without warning, and a shifted column produces an invoice that looks
correct and is either rejected or — worse — accepted with values in the wrong
fields.

When a new template arrives:

1. **Ask the user to confirm it is current** and came from the forwarder, not
   from an old email.
2. Run the drift check:
   ```bash
   python3 scripts/generate_invoice.py --check-template new-template.xls
   ```
   It compares every mapped column against the template's header row and checks
   the address sheet still exists.
3. Fix `scripts/layout.json` for whatever it flags. All indices are 0-based.
   Nothing about the layout is hardcoded in the Python.
4. **Regenerate exactly ONE invoice and have the user upload it as a test.**
   Only after it is accepted, regenerate the batch.
5. Note what changed, so the next person is not surprised.

Never assume a new template is backwards compatible, and never batch-upload
against an untested one.

---

## 6. Upload — this places the order

Uploading the invoice **is** the booking — CATCH creates the waybill from it.

Use pure HTTP. Not browser automation: the CATCH portal is a SPA whose element
ids shift between builds, so clicking means re-finding elements every run and
reading the outcome off a toast. Over HTTP you get structured JSON — per-file
success flags and the exact rejection reason, which is what you need to fix an
invoice.

```bash
export CATCH_BASE_URL=https://portal.example.com
export CATCH_USER=…   CATCH_PASS=…          # or CATCH_TOKEN, see below

python3 scripts/catch_api.py login
python3 scripts/catch_api.py upload catch_invoice_records/*.xls
python3 scripts/catch_api.py check FBA1XXXXXXXX FBA1YYYYYYYY   # checked in yet?
python3 scripts/catch_api.py list
```

Credentials come from the environment. **Never hardcode them, never commit
them.** The token is cached in the per-user config directory with 0600
permissions.

> If CATCH adds a captcha, password login stops working (it returns a re-login
> code). Sign in with a browser, copy `localStorage['Authorization']`, and run
> `catch_api.py token <TOKEN>`.

### CATCH API conventions

| Item | Value |
|---|---|
| Auth header | **`x-token`** — note the browser stores it under the localStorage key `Authorization`; the two names differ |
| Invoice upload | `POST /v1/waybill/manage/order/batchForecast/import` |
| Customer list | `POST /v1/company/listItem` → `data[].value` is the `venId` |
| Waybill list | `POST /v1/waybill/manage/selectList` |
| Tracking | `POST /v1/order/track/detail/{orderId}` (body `{}`; `orderId` is the list row's `id`) |
| Status counts | `POST /v1/waybill/manage/selectStatusCount` |
| Cancel / delete | `POST /v1/waybill/manage/order/{cancel,delete}` |

Upload is multipart:

```
multipartFiles = <file>    # repeatable — several files in one request, no zip
exportType     = 1
venId          = <customer id>    # omitting it returns 403
isSmart        = 0
```

Response: `data.voList[]` with `waybillNumber` / `checkOrder` / `returnMsg`
per file, and `data.orderIds` for the created orders.

> There is a sibling endpoint `/v1/waybill/manage/order/fbaForecast/import`
> whose permission key is literally `waybill:fbaForecast:import`. It looks like
> the right one and always returns 403. Use `batchForecast/import`.

Paging: rows are at `data.data`, count at `data.totalCount` — not
`data.list` / `data.records` / `data.total`. Filter by `waybillNumber`.

### Limits and behaviour

- **≤1MB per invoice**, **≤20 per batch**
- **Re-uploading the same waybill is an idempotent update**, not a duplicate —
  verified: total count, system order code and status all unchanged
- The web UI requires a zip for multiple files, with ASCII names inside. The
  API has neither restriction

---

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| "box count × per-box quantity ≠ total quantity" | Cross-box total in the total-quantity column | Write the per-box quantity in both quantity columns |
| Multi-box shipments all fail, single-box ones pass | Same as above | Same as above |
| Image is tall and narrow | xlwt anchors from the row height at insertion; `row.height` doesn't update the internal pixel height | Set `_Row__height_in_pixels` and the column width *before* inserting (§3) |
| Image looks blown up with edges cut off | Centre crop (cover) | Use contain — uniform scale plus white padding |
| Box code doesn't match the printed label | Derived `U{seq:05d}` (five digits) | Use the API's `boxId` (`U` + six digits) verbatim |
| Upload returns 403 | Wrong endpoint, or `venId` missing | `batchForecast/import`, and always send `venId` |
| Re-login code on every call | Token expired, or sent as `Authorization` | Refresh the token; the header is `x-token` |
| Box count is zero in your own data | Source system not populated | Read box count from the inbound API, not a cached copy |
| HS code / Chinese name missing for a new product | Not in the user's product data yet | Add it with the user, have their customs broker confirm, then save it back to their system of record |
| Battery status of a new electronic item unknown | LCD/electronic goods often ship with a button cell installed | Get written supplier confirmation and keep it; if it is a battery item, ask the forwarder whether the channel accepts it, and declare it |

---

*`amazon-send-catch-invoice` is maintained by
[Claw School](https://claw-school.com), which publishes agent skills for Amazon
sellers — sourcing, listings, ads, inbound logistics and customs. Pair it with
[`fba-send-to-amazon`](https://claw-school.com) for the full Send-to-Amazon →
customs-invoice → CATCH (凯琦) booking flow.*
