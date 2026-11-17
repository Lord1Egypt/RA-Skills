# Payable matching — full procedure, tool shapes, example, economics

Reference behind `SKILL.md`. Read it when you need the detail behind a step,
the exact field names a payload carries, or the cost model for running this at
volume.

---

## 1. Why the design is shaped this way

Two forces drive every choice:

- **Context economy.** Documents are PDFs. `documents_get` returns their bytes
  as base64; a multimodal PDF reader adds a page image. Both are enormous next
  to the ~300–600 characters of text that actually matter, and this runs over
  many documents many times a day. So text extraction is pushed into
  `scripts/paymatch.py` (`extract`), which decodes and reads the text **locally**
  and returns text only. The model never sees base64 or a render. `po-lines`
  likewise trims the verbose PO payload to the matchable fields. The result: a
  document "match" costs the model a few thousand tokens, not tens of thousands.

  Extraction runs **PyMuPDF → poppler `pdftotext -layout` → pypdf** and
  quality-gates the output. PyMuPDF is first because it honours ToUnicode CMaps
  and reads **Type3 / custom-encoded fonts** that pypdf returns as empty or
  garbage (the failure that stranded Charles River Apparel confirmations). A
  result that is empty or fails the reliability gate flags the document
  `needs_vision: true`; the model then calls `render` to rasterise the page(s)
  with PyMuPDF (no system poppler) and reads them with vision (plus tesseract OCR
  if present) — keeping even the unreadable-text case out of a dead-end
  escalation, while still never pulling raw base64 into context.

- **Judgment stays with the model.** The script does deterministic I/O (fetch,
  decode, extract, apply a price, move a file). The *matching decision* — which
  document line pairs to which PO line, whether a total gap is a partial
  shipment, whether a freight figure is authoritative, whether something is a
  genuine question — needs the model, because vendor documents vary too much for
  a rigid parser. Get this division wrong in either direction and you either
  bloat context (model reading raw bytes) or get brittle matches (script
  guessing intent).

---

## 2. The tool surface (MCP), and the payload shapes you'll see

The skill drives the Odoo `drivethru_mcp` MCP tools. `paymatch.py` wraps the
ones below; the field names are what the tools actually return (know them so you
don't waste calls discovering them).

### Documents app

- `documents_list_folders {name?, parent_id?}` → `{folders: [{id, name, parent,
  document_count}]}`. Resolve `Purchasing` → its id; list its children with
  `{parent_id}` to get the `Matched` / `Questions` folder ids.
- `documents_search {folder_id, limit, offset, include_subfolders?}` →
  `{documents: [{id, name, type, mimetype, file_size, folder:{id,name}, tags,
  res_model, res_id, ...}], total_matched}`. Metadata only — **no bytes**.
  Paginate on `total_matched`.
- `documents_get {document_id}` → the metadata **plus** `data_base64` (the file
  bytes) and `open_activities`. Files over the 20 MB guard return a
  `download_url` instead of bytes. (`paymatch.py extract` calls this per file
  and throws the base64 away after extracting text.)
- `documents_update {document_id, fields:{folder_id}}` → moves the document
  (this is how a document leaves the inbox — there is no delete tool).
- `documents_post_message {document_id, body, activity_user?, activity_summary?,
  activity_date_deadline?}` → posts a chatter note and, with `activity_user`,
  schedules a To-Do for that reviewer. `activity_user` matches login/email
  first, then name.

### Accounts payable

- `ap_search_purchase_orders {search?, vendor?, state?, limit?}` →
  `{count, purchase_orders: [{id, name, partner_id, partner_name, partner_ref,
  amount_untaxed, amount_total, freight_cost, fees_cost, state,
  receipt_status, invoice_count, buying_group, ...}]}`. `search` matches PO name
  / partner_ref / vendor order number.
- `ap_get_purchase_order {po_id}` → the header fields above **plus**
  `lines: [{id, product_id, product_name, product_sku, description,
  product_qty, qty_received, qty_invoiced, price_unit, price_subtotal,
  style_number, intelligent_id, ...}]` and `existing_bills`. `id` on a line is
  the `line_id` you pass to update. (`paymatch.py po-lines` trims this to
  `{line_id, sku, style, description, qty, qty_received, qty_invoiced,
  price_unit, price_subtotal}` — `qty_received` vs `qty` is the per-line signal
  for whether a partial shipment has now completed the PO.)
- `ap_update_po_lines {po_id, lines:[{line_id, price_unit?, product_qty?}],
  freight_cost?, fees_cost?, allow_non_dropship?}` → `{po_name,
  lines_updated:[{line_id, old_price, new_price, old_qty?, new_qty?,
  is_dropship?}], new_pickings, new_amount_total}`. The PO must be
  `state: "purchase"` (confirmed). `product_qty` is **only** for carrying out a
  reviewer-approved qty raise (increase-only, dropship lines unless
  `allow_non_dropship`). Never use it to "fix" a variance on your own; see
  `sportsinc_payables.md` → *Acting on the reviewer's answer*.
- `ap_create_vendor_bill {po_id, vendor_bill_number?, invoice_date?, line_ids?,
  expected_total?, tolerance?, reviewer_user_id?, review_note?}` → **draft**
  `account.move`. The payables tail (`paymatch.py bill`). Bills the PO's
  remaining `qty_to_invoice`; errors "No billable lines" when the PO has none
  left.
- `ap_create_draft_bill {po_id|vendor_id, vendor_bill_number?, invoice_date?,
  lines?:[{product_id|product_name, quantity, price_unit, tax_ids?, …}],
  reviewer_user_id?, review_note?}` → an **off-PO draft** bill, independent of
  `qty_to_invoice`, that **never posts**. For the over-invoice case (SI billed
  items the PO can't cover — e.g. replacements for units never received): seed
  the lines from the payload with the PO's own product ids, and pass
  `reviewer_user_id` + `review_note` to land it with a review activity. `po_id`
  links `invoice_origin` (traceability + re-run idempotency).
- `ap_post_vendor_bill {bill_id, post?, expected_total, tolerance?,
  vendor_bill_number?, invoice_date?, note?}` → **posts** a draft vendor bill,
  the **match & post** step (`paymatch.py post`). Guarded: `in_invoice` + draft
  only, previews unless `post:true`, and **refuses to post** when the bill total
  misses `expected_total` beyond `tolerance` (an absolute currency amount) —
  returns `{posted, total_check{expected,actual,difference,within_tolerance},
  already_posted?}`. A refused/mismatched bill stays in draft → escalate to
  Questions, never post it.

### Vendor-bill line CRUD (multi-shipment split — one PO, several SI invoices)

Only for the multi-invoice case (see `sportsinc_payables.md` →
*Multiple invoices for one PO*). All three edit **draft `in_invoice`** moves only
and never touch the auto-computed tax/payable journal items. `ap_get_vendor_bill`
returns each editable line with `purchase_line_id`, `product_sku`, `quantity`,
`price_unit`, `tax_ids`, `account_id`, and `cost_center_id` — the handles below.

- `ap_create_bill_line {bill_id, lines:[{product_id|product_name,
  account_id|account_name, name?, quantity?, price_unit?, tax_ids?,
  cost_center_id|cost_center_name?, display_type?}]}` → adds line(s); resolves
  product/account by id **or** name. Use for a shipment's freight
  (`Vendor Shipping Charge` / `Inbound Freight`, `tax_ids: []`).
- `ap_update_bill_lines {bill_id, lines:[{line_id, quantity?, price_unit?,
  name?, tax_ids?, …}]}` → patches line(s); absent keys unchanged, `tax_ids`
  REPLACES (`[]` clears). Restate a split line's `quantity`, or the Sports Inc.
  Fee line's `price_unit` to the document's `si_upcharge`.
- `ap_delete_bill_lines {bill_id, line_ids:[…]}` → removes line(s); dropping a
  merch line frees its PO line to bill on the next shipment's bill.

Also on `ap_search_purchase_orders`: `min_tracking_count` / `max_tracking_count`
filter on the count of `vendor.tracking` rows — `min:2` is the likely
multi-invoice slice, `max:1` the single-shipment slice.

### PO chatter

- `po_post_message {po_id, body, issue_type?, activity_user_id?}` → posts the
  "checked" note (or an exception) onto the PO as an internal **log note** (never
  a customer/vendor-facing "Send message"). `{message_id}`.
- `po_get_messages {po_id, limit?}` → the PO's chatter, newest first as plain
  text, plus open activities. Read it before posting a partial-shipment note to
  see which lines earlier shipments already checked (`paymatch.py notes` wraps
  this and also resolves a PO number → id).

### Document render (vision / OCR fallback)

- `paymatch.py render {document_id, pages?, dpi?}` pulls the file via
  `documents_get` and rasterises its page(s) to PNG with **PyMuPDF** — no system
  poppler needed — returning `{images:[paths], ocr_text, ocr_engine}` (OCR text
  only when `tesseract` is installed). This is the escape hatch for a
  `needs_vision` document: a scan, or a Type3 / custom-encoded PDF whose text
  layer won't decode. Read the returned image(s) with vision to pull the PO
  number and line items, then match as normal — never escalate it unread.

Operator docs for deeper semantics (fetch via the MCP `docs_get` tool):
`documents` and `invoices`.

---

## 3. Matching rules

- **PO number comes from the document body, not the filename.** Filenames often
  carry the vendor's order number; read the "PO Number / PO #" field in the
  text.
- **Pair lines by (style/item, color, size), never by row order.** Odoo and the
  vendor sort differently, and a partial shipment matches only a subset of the
  PO's lines.
- **Size upcharges are legitimate pricing.** Base sizes (S–XL) at one price with
  2XL/3XL/4XL higher is normal — not an error. A single base size priced off
  the others (e.g. S at $13.94 when M/L/XL are $11.94 and the vendor confirms
  $11.94) is the error.
- **Totals cross-check, they don't decide.** A shipment acknowledgement is often
  one box of a multi-shipment order; its total is legitimately below the PO
  total by the value of the un-shipped lines. Reconcile lines; explain the gap
  in the checked note.
- **Partial shipments accumulate — name the lines and call the last one.** When a
  shipment covers only some of the PO's lines, list the checked lines/SKUs in the
  log note, then read the PO's prior notes (`po_get_messages` / `paymatch.py
  notes`) and per-line `qty_received`. When this shipment's lines **unioned with
  the previously-checked lines cover every line on the PO** (nothing on
  back-order), annotate that the PO is **now fully checked across all shipments**;
  otherwise state which lines are still outstanding. The log notes are the ledger
  this relies on — never claim completion without them.
- **Log notes only — never "Send message".** Every annotation on a PO or document
  (checked note, partial-shipment note, question) is an internal Odoo log note; it
  must never notify followers or email the vendor/customer. `po_post_message` /
  `documents_post_message` (and the helper's `matched` / `questions`) post log
  notes — use nothing that sends externally.
- **Freight / fees are PO-level and invoice-time.** Correct them only when the
  document gives an authoritative figure. A pre-existing freight estimate or a
  partner-level fee the document doesn't itemize (e.g. an order acknowledgement
  shipped "UPS Ground Collect") is not a line-pricing error — note it for the
  eventual invoice match and leave it.
- **Confirmed POs only.** `ap_update_po_lines` requires `state: "purchase"`. A
  draft/other-state PO that needs a change is a Questions case.

---

## 4. Filing rule (non-negotiable)

Every reviewed document leaves the Purchasing inbox into a sibling subfolder:

- **Matched** — prices reconciled, or corrected with confidence.
  `paymatch.py matched '{"po_id", "document_id", "body"}'` posts the checked
  note and moves the document in one call.
- **Questions** — a genuine ambiguity (unreadable/unresolvable PO#, prices that
  don't reconcile, unexpected/missing lines, wrong vendor).
  `paymatch.py questions '{"document_id", "question", "reviewer": "Zach Tucker"}'`
  raises the reviewer activity and moves the document in one call. Add
  `po_id` + `po_note` to also annotate the PO.

Only escalate a **real** question. An unambiguous fix the vendor document
supports is a Matched correction — that is the job, not a question.

---

## 5. Worked example (the five-document run this skill was built from)

`paymatch.py extract '{"folder": "Purchasing"}'` returned five documents as
text. Per document:

| Document (text) | PO# (from body) | Finding | Action |
|---|---|---|---|
| SanMar Order Confirmation, SO-163291890 | **P13189** | Size **S** line reads $11.94 on the confirmation but $13.94 on the PO (M/L/XL $11.94, 2XL $12.94, 3XL $14.94 all match) | `apply {po_id:13145, lines:[{line_id:40941, price_unit:11.94}]}` (total $1,047.90→$1,041.90) → `matched` |
| SanMar Order Confirmation, SO-163292190 | **P13193** | Both lines $1.87, match | `matched` (checked, no change) |
| SanMar Order Confirmation, SO-163289633 | **P13194** | 3 lines $3.99, match | `matched` (checked, no change) |
| SanMar **Shipment** Acknowledgement, SO-163260908 | **P13137** | Box 1 of a multi-shipment order: 6 of the PO's 11 lines, all $1.79 and matching; doc total $53.70 vs PO $98.45 is just the 5 un-shipped lines | `matched`, checked note explaining the partial shipment |
| Workwear Outfitters Order Acknowledgement (filename `48482500`) | **P13183** (read from body) | Both lines match ($14.30, $40.32); PO also carries freight $2.00 and a −$2.38 fee the ack doesn't itemize (invoice-time) | `matched`, note the freight/fee for the invoice match |

None needed Questions. A document whose text won't extract (scanned, or
Type3/custom-encoded like the Charles River Apparel confirmations) is **not** a
Questions case — it flags `needs_vision`, and you `render` it and read the
page image(s) with vision/OCR, then match normally. Only a genuine
reconciliation failure (unresolvable PO#, prices that don't reconcile, wrong
vendor) is `questions`-filed to Zach Tucker instead.

The pattern per document is 2–3 helper calls after the single `extract`:
`po-lines` → (`apply` if a fix) → `matched`/`questions`.

---

## 6. Low-cost model recommendation + per-match economics

Because the heavy PDF work lives in `paymatch.py` and the PO payload is trimmed,
the model reads a few hundred characters of text plus a lean line list per
document and drives a short deterministic tool sequence — light work a small
model handles well, with the Questions→reviewer path as the safety net on live
financial data.

**Recommended: `claude-haiku-4-5` as the default; `claude-sonnet-5` as an
accuracy step-up.** (IDs/pricing per the `claude-api` skill catalog; verify with
the Models API if unsure.)

| Model | Price in/out (per 1M) | Est. cost / match | Use as |
|---|---|---|---|
| `claude-haiku-4-5` | $1 / $5 | **~$0.02–0.05** (~$0.03 typical) | Default — cheapest; ample here |
| `claude-sonnet-5` | $3 / $15 (intro $2/$10 to 2026-08-31) | **~$0.04–0.14** (~$0.07 typical) | Step-up for messy/unfamiliar vendor layouts |

**Per-match token shape** (one document reconciled): ~3–4K *new* input
(extracted text + lean PO lines + tool results) + ~1K output, plus cached
re-reads of the system/tools prefix at 0.1×. The `extract` step is a script
call — near-zero model tokens, shared across the whole folder. At **50
docs/day (~1,300/mo)** that's roughly **$40/mo on Haiku**, **~$90/mo on
Sonnet**. These are modeled from observed document/PO shapes, not billed
counts — **run one real batch on Haiku with usage logging to confirm COGS.**

**Suggested pricing** (price off value/labor replaced, not inference cost — a
clerk eyeballing a confirmation against a PO is ~3–8 min ≈ $1.25–3.30 loaded,
and the tool also catches real overcharges — e.g. the $6.00 error above):

| Package | Price | Gross margin on Haiku | Notes |
|---|---|---|---|
| Per-match (standard) | **$0.50** | ~94% | Haiku-backed default; obvious ROI vs. clerk time |
| Per-match (high-accuracy) | **$1.00** | strong even on Sonnet | Sonnet 5 for accuracy-sensitive vendors |
| Monthly plan | **~$499/mo, up to 1,500 matches** (~$0.33 effective) | ~90%+ | Predictable for the customer; overage ~$0.40 |

Lead with **$0.50/match on Haiku 4.5**; offer the **$1.00 Sonnet tier** as an
accuracy upsell. Keep the cache warm and the loop tight (one `extract` per
folder, cache the prefix) — a bloated system prompt or extra turns is the main
cost risk, and the skill already keeps the expensive PDF work out of the model.
