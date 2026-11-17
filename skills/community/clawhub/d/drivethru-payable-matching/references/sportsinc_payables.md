# Sports Inc payables — end-to-end (SportsLink → match → bill → post-on-match)

Sports Inc is a buying group that doesn't send individual vendor invoices; the
invoices live in the SportsLink API. This is the automated payables loop for
them: pull the invoices, reconcile each to its Odoo PO, correct price variances,
create the bill, **post it when its total matches the invoice** (else leave it
in draft), and mark the SI document consumed — with a human handling anything
flagged.

Three skills cooperate (this is the ports-and-adapters split in practice):

- **Source adapter** — `sportsinc-sportslink` (`sportslink.py`): fetch invoices,
  mark consumed. Customer-agnostic.
- **Workflow** — this skill: reconcile invoice ↔ PO, correct/escalate, create the
  draft bill. Source- and ERP-agnostic.
- **ERP adapter** — `drivethru-odoo` / `drivethru_mcp` (`paymatch.py`,
  `ap_create_vendor_bill` / `ap_post_vendor_bill`): the Odoo writes.

## Configured policy (BaconCo)

- **Posting: post on match, draft on mismatch.** Create the bill, then **post it
  when the bill total matches the invoice `expected_total` within tolerance**
  (`paymatch.py post`, backed by the guarded `ap_post_vendor_bill`). A bill that
  doesn't match is **left in draft** and escalated to the reviewer — never post a
  mismatch. When a run should stay hands-off (a human reviews before posting),
  skip the `post` step and leave every bill in draft.
- **On variance: auto-fix price, escalate qty/line.** A unit-price difference is
  treated as the SI invoice being authoritative — correct the PO line (like the
  pricing review), then bill. A **quantity / missing-line / total-structure**
  variance is **not** auto-fixed — escalate it (leave the SI doc active, raise an
  activity to the reviewer, create no bill). Once the reviewer **answers** the
  escalation, you carry out their decision yourself — see
  [Acting on the reviewer's answer](#acting-on-the-reviewers-answer-quantity-escalations).
- **Reviewer:** Zach Tucker (`reviewer_user_id: 6` in BaconCo's Odoo). Keep this
  in tenant config, not hard-coded in prose.
- **Tolerance:** a small **absolute** amount (a few cents, e.g. `0.02`) for the
  `expected_total` match check on both create and post — once prices are
  reconciled the SI docTotal should equal the computed bill to within rounding.
- **Chatter: internal log notes only.** Every PO note or escalation this loop
  posts (via `po_post_message`) is an internal Odoo **log note**, never a "Send
  message" — nothing here is emailed to the vendor.

## The exactly-once loop (do not deviate)

You are creating payables — double-billing is the cardinal sin. The SportsLink
`active`/historical flag is the idempotency mechanism; the sequence is fixed:

1. **Pull the inbox.** `sportslink.py list '{"active": true, "lines": true, "ediOnly": true}'`
   → normalised invoices that are not yet imported and carry line items.
2. **Process each invoice** (below). Create the draft bill in Odoo.
3. **Mark consumed only after the draft is created.**
   `sportslink.py mark-historical '{"siDocNumbers": [<si_doc_number>]}'`.
4. **Anything that fails or is escalated stays active** — it simply reappears on
   the next run. Never `mark-historical` a doc you didn't bill.

Never use the API's `moveToHistorical=true` GET flag — it marks on read, before
billing, so a crash drops the invoice. Belt-and-suspenders on the Odoo side:
before creating, check the PO's `invoice_count` / existing bills for the same
`supplier_doc_number`, in case a prior run's mark-historical failed after the
bill was created.

## One PO can have several invoices — group by PO first

Invoices are keyed by `si_doc_number` (one row per SI document). Sports Inc
issues **one document per shipment**, so a PO that shipped in several boxes comes
back as **several rows sharing one `po_number`**. Before billing, group the
adapter's rows by `po_number`:

- **Exactly one** SI document for the PO → the single-invoice path below
  (steps 1–8).
- **Two or more** SI documents for the PO → the PO bills as several vendor
  bills, one per document. Follow **[Multiple invoices for one
  PO](#multiple-invoices-for-one-po-multi-shipment-split)** instead of steps
  5–8. Do **not** create one bill for the whole PO — its lines, freight, and
  `si_upcharge` belong to different documents.

The `drivethru-ap-sports-inc-multi-invoice` routine pre-filters to the POs most
likely to be in this case with `ap_search_purchase_orders`
`min_tracking_count: 2` (two-plus `vendor.tracking` rows ⇒ several shipments);
the single-invoice routine uses `max_tracking_count: 1`. The tracking count is
only a *net* — the SI payload's document count is what actually decides
single-vs-multi.

## Per-invoice procedure

For each normalised invoice from the adapter (single-document POs):

1. **Credit?** `is_credit: true` → do not bill. Escalate to the reviewer (vendor
   credit is a human decision). Leave active.
2. **No lines?** `has_lines: false` (scanned/OCR doc) → can't line-verify.
   Escalate to the reviewer for a header-only decision. Leave active.
3. **Find the PO.** `paymatch.py po-lines '{"po": "<po_number>"}'`. If it doesn't
   resolve (`found: false`) or the vendor doesn't line up → escalate, leave
   active.
4. **Reconcile lines** by (item/style, size, color): compare the invoice
   `net_price` to the PO line `price_unit`, and `qty_shipped` to `qty`.
   - **Price variance only** → `paymatch.py apply '{"po_id", "lines":[{"line_id",
     "price_unit": <invoice net_price>}]}'` (SI invoice is authoritative on
     price), then continue.
   - **Quantity / missing line / extra line / total-structure variance** →
     **escalate** (`paymatch.py questions '{"document_id"? , "question", ...}'`
     or a PO note + reviewer activity), leave the SI doc active, create no bill.
     (Sports Inc docs are API rows, not Documents-app files, so escalate on the
     PO chatter via `po_post_message` and/or a tracked task — there's no
     Documents folder to file.)
5. **Verify the SI charges tie out.** `docTotal` includes SI-specific charges
   (`si_upcharge`, `svc_handle`, `freight`, `sales_tax`, less `discount` /
   `freight_allowance`). Odoo's bill create() **auto-appends the Sports Inc fee
   lines** for `buying_group: "si"` POs — so pass the invoice `total` (docTotal)
   as `expected_total`; do not pre-add the SI fees yourself (you'll double them).
6. **Create the draft bill.**
   ```
   paymatch.py bill '{
     "po_id": <id>,
     "vendor_bill_number": "<supplier_doc_number or si_doc_number>",
     "invoice_date": "<invoice_date>",
     "expected_total": <invoice total>,
     "tolerance": 0.02,
     "reviewer_user_id": 6,
     "review_note": "SI SportsLink doc <si_doc_number>; matched PO <po_number>; <price fixes>."
   }'
   ```
   If the create returns `success: false` (the computed bill total missed
   `expected_total` beyond tolerance) → **do not** mark historical; escalate with
   the discrepancy and leave the doc active.
7. **Mark consumed.** On a successful draft, `sportslink.py mark-historical
   '{"siDocNumbers": [<si_doc_number>]}'`.
8. **Post it if it matches.** Post the draft (created bill `id` from step 6) so
   it hits the ledger — unless this is a draft-only run:
   ```
   paymatch.py post '{
     "bill_id": <created bill id>,
     "expected_total": <invoice total>,
     "tolerance": 0.02,
     "note": "SI SportsLink doc <si_doc_number>; matched PO <po_number>; posted on match."
   }'
   ```
   `post` re-checks the total and **refuses** (leaving the bill in draft) if it
   no longer matches within tolerance — treat a refusal as an escalation to the
   reviewer, exactly like a create mismatch. Posting an already-posted bill is a
   safe no-op (`already_posted: true`), so a re-run never double-posts.

## Multiple invoices for one PO (multi-shipment split)

When Sports Inc returns **2+ documents for one `po_number`**, the PO must bill as
**one vendor bill per SI document**. Each document (`si_doc_number`) covers a
subset of the PO's lines, with its own `freight` and its own `si_upcharge`; its
`docTotal` is the whole bill (merch + upcharge + freight). Odoo's PO→bill
`create()`, by contrast, bills **every** received line at once and computes the
SI fee on the **whole** PO — so you create that draft and then **carve it down**
to each document with the `account.move.line` tools:

- `ap_get_vendor_bill {bill_id}` — each editable line carries `purchase_line_id`,
  `product_sku`, `quantity`, `price_unit`, `tax_ids`, `account_id`, and the fee
  line's handle. These are the only ids the carve tools accept.
- `ap_update_bill_lines {bill_id, lines:[{line_id, quantity?, price_unit?,
  name?, tax_ids?}]}` — patch a line: drop a split line's `quantity` to this
  shipment's qty, restate the **Sports Inc. Fee** line's `price_unit` to this
  document's `si_upcharge`, clear `tax_ids`.
- `ap_create_bill_line {bill_id, lines:[{product_name|account_name|…,
  price_unit, tax_ids}]}` — add this shipment's freight
  (`Vendor Shipping Charge` / `Inbound Freight`, `price_unit` = `freight`) when
  the PO carried none.
- `ap_delete_bill_lines {bill_id, line_ids:[…]}` — drop the merch lines that
  belong to **later** shipments (that frees each dropped PO line to bill on the
  next pass), or a duplicate auto-added fee line.

**Precondition — line-level detail required.** Only run the split when **every**
document for the PO has line items (`has_lines: true`). If any is header-only
(scanned / OCR, `has_lines: false`), the split can't be verified line-by-line —
**skip the whole PO and escalate** (leave every one of its SI docs active).

**One bill per document; post only what the PO supports.** Create a bill for
**every** SI document (so the bill count matches the document count), but only
**post** the ones the PO's quantities cover. A document the PO can't cover — an
**over-invoice**, e.g. the vendor invoiced replacements for units it never
originally shipped, after the earlier bills already consumed the PO's whole
quantity — still becomes a bill, but a **draft with a review activity**, never a
posted one.

**Procedure** — process the documents oldest first; each pass creates one bill:

1. **Reconcile prices first, once.** Compare each SI line's `net_price` to its PO
   line `price_unit` across all the PO's documents; `ap_update_po_lines` any
   price variance (SI is authoritative on price), escalate qty/line variances —
   same rule as the single-invoice path.
2. **Create the draft.** `ap_create_vendor_bill {po_id}` bills all lines still
   billable (received, not already on a draft/posted bill). On the first pass
   that's the whole PO; on later passes only what earlier bills left behind.
   - **Over-invoice branch.** If this returns **"No billable lines"** (the PO has
     no `qty_to_invoice` left) while SI still has an unbilled document, that
     document is an over-invoice the PO can't substantiate. Create it **off-PO**
     instead: `ap_create_draft_bill {po_id, vendor_bill_number, invoice_date,
     lines: [{product_id, quantity, price_unit, tax_ids: []}], reviewer_user_id,
     review_note}` — build `lines` from the SI payload using the **PO's own
     product ids** (map by supplier item + size against `ap_get_purchase_order`),
     add the document's freight + `si_upcharge` fee lines so the draft total
     equals `docTotal`, and **do not post it** (`ap_create_draft_bill` never
     posts). Make `review_note` say we were invoiced for items not on the PO and
     a human must review. Then move to the next document (step 6).
3. **Map lines to this document.** `ap_get_vendor_bill`; pair each bill line to
   an SI line by **(supplier item, size)** via `product_sku` (e.g.
   `…(JP1477)-S`) — never by row order.
4. **Carve to exactly this document:**
   - `ap_delete_bill_lines` the merch lines that belong to **other** shipments.
   - For a PO line split across shipments, `ap_update_bill_lines` its `quantity`
     down to this document's `quantity_shipped` (the remainder bills next pass).
   - `ap_update_bill_lines` the **Sports Inc. Fee** line's `price_unit` to this
     document's `si_upcharge` (verify exactly one fee line remains; delete a
     duplicate). Do **not** re-derive the fee — use the number SI gave.
   - If this document has `freight` and no freight line exists,
     `ap_create_bill_line` a `Vendor Shipping Charge` line at that amount.
5. **Set the reference + post.** `ap_post_vendor_bill {bill_id, post: true,
   expected_total: <docTotal>, vendor_bill_number: <supplier_doc_number>,
   invoice_date: <supplier_doc_date>, tolerance: 0.02}`. The gate refuses a
   mis-carved bill (total ≠ `docTotal`); a refusal is an escalation, not a
   retry-blindly.
6. **Repeat** from step 2 for the next document until **every** document for the
   PO has a bill — posted where the PO covers it, draft-with-review-activity
   where it doesn't (the over-invoice branch). The bill count matches the SI
   document count; only the reconciling ones are posted.
7. **Mark consumed after all its bills exist.** `mark-historical` every
   `si_doc_number` for the PO (each only after its bill is created), and flip
   `is_pricing_checked = true` on the PO once all its shipments are billed. A
   partially-billed PO stays active so the next run finishes it.

Idempotency across a killed run: before creating, check the PO's existing bills
(`ap_get_purchase_order` → `existing_bills`, and each `si_doc_number` against
bill `ref`) so a re-run resumes where it stopped rather than double-billing an
already-posted document.

## Acting on the reviewer's answer (quantity escalations)

An escalation is a question, not a hand-off. When the reviewer replies (in the
PO chatter — read it with `po_get_messages` — or directly in your session) with
a decision, **you execute it**. Never turn their answer into a numbered list of
"manual steps" assigned back to them.

The common answer to an over-shipped invoice (SI invoiced qty 2, PO line says 1)
is *"update the PO to match the invoice, receive it, bill it."* Do it like this:

1. **Check the line is dropship.** `stock_dropship_pickings {po_id}` — the PO
   line's moves sit on a dropship picking (vendor → customer).
2. **Raise the PO line.** `ap_update_po_lines {po_id, lines: [{line_id,
   product_qty: <invoiced qty>, price_unit: <invoice net_price>}]}` (or
   `paymatch.py apply` with the same lines). It only increases, and refuses a
   non-dropship line. Odoo creates a **new dropship picking** for the extra
   units; the response lists it in `new_pickings`.
3. **Receive the extras.** `stock_validate_dropship {picking_id: <new picking>}`
   to preview, then again with `validate: true`. Because a dropship ships vendor
   → customer, validating it **also updates the sale order's delivered qty**, so
   the customer can be invoiced for the extra units. You don't need to touch the
   sale order separately.
4. **Fix the bill.** If a draft already exists for this SI doc, `ap_get_vendor_bill`
   and `ap_update_bill_lines` the affected lines' `quantity` up to the invoiced
   qty (or delete the draft and `ap_create_vendor_bill` again). Restate the
   Sports Inc. Fee line to the document's `si_upcharge` if it moved.
5. **Post at the SI total.** `ap_post_vendor_bill {bill_id, post: true,
   expected_total: <docTotal>, vendor_bill_number, invoice_date, tolerance: 0.02}`.
   Then `mark-historical` the SI doc, and log a note on the PO saying what you
   changed (old → new qty, picking validated, bill posted and its total).
   Mark any activity you opened for this escalation done, or say it can be
   closed.

**Non-dropship (stocked) lines.** Raising the qty creates a stock receipt
into our warehouse and does **not** touch the sale order. Treat that as a
separate decision: only pass `allow_non_dropship: true` when the reviewer's
answer explicitly covers a stocked line, and don't change the sale order
unless they asked for it.

**If a step is truly blocked** (a tool refuses, or no tool exists for it), do
every step you *can*, then escalate again naming the **exact step that's
blocked and why** (tool name + error). Don't re-list steps you could have done.

## Scheduling & resilience

- **Run after ~10:30am ET** (SI processing completes first). This is a scheduled
  batch — a good fit for a cron/Routine trigger.
- The loop is self-healing: transient API failures retry (the adapter backs off);
  anything unresolved stays active and is retried next run; a run can be killed
  and restarted safely because nothing is marked consumed until its bill exists.
- **Notify on exceptions.** Summarise per run: posted N bills and left M in
  draft (list PO / amounts, posted vs draft), corrected P prices, escalated Q
  (with reasons), and any hard failures. Draft bills + escalations are the
  human's queue.

## Why an agent, not a custom Odoo module

The deterministic mechanics (auth, paging, normalisation, mark-historical) live
in `sportslink.py`; the ERP writes are single tool calls. The **agent** adds the
judgment (which variances to auto-fix vs. escalate, credit/scanned handling, PO
resolution) and the resilience (retry, anomaly detection, human-readable failure
notices) that a deterministic module would force you to hand-code and redeploy
per edge case. Keep the mechanics in scripts (out of the model's context) and the
judgment in the agent — the same division that makes the folder pricing review
cheap.

## Not testable without live access

`sportslink.py` needs `SPORTSINC_API_KEY` and reaches `api.sportsinc.com`, and
billing writes to live Odoo. Smoke-test in stages: (1) `list` read-only against a
recent date; (2) one `bill` on a known PO with `SPORTSINC_DRY_RUN=1` so nothing
is marked consumed; (3) confirm the draft in Odoo and the reviewer activity;
then enable `mark-historical`. Confirm the `vendor_bill_number` convention
(supplier vs. SI doc number) and the bill's vendor/partner for `buying_group:si`
POs during that first pass.
