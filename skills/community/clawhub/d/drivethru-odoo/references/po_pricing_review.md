# Document-driven PO pricing review (batch)

The pattern behind *"go through every document in the Purchasing folder, check
its pricing against the purchase order, fix any line that's wrong, mark the PO
checked, and file the document."* This runs many times a day over 5–50+
documents, so the whole design is built to (a) keep the model's context window
small no matter how many documents there are, and (b) leave the Purchasing
inbox empty when it's done — every document ends up in **Matched** or
**Questions**.

Read `docs_get {"slug": "documents"}` and `docs_get {"slug": "invoices"}` for
the underlying tool semantics; this file is the operating procedure.

## The efficiency rule: extract text out-of-context, once

`documents_get` returns each file's bytes as **base64**, and reading a PDF
through a multimodal reader adds a **page image** on top. Both are enormous
next to the ~300–600 characters of text that actually matter per document. Do
that per file across a folder and the context window fills with base64 and
renders — the single biggest cost in a multi-document run.

**So do not loop `documents_get` (or a PDF reader) over the folder.** Use the
intake helper, which fetches every file, decodes and extracts the text
**locally**, and returns compact JSON — text only, no base64, no image:

```bash
python3 scripts/po_docs.py extract '{"folder": "Purchasing"}'
```

Returns `{"folder", "count", "documents": [{document_id, name, mimetype,
text, chars, needs_vision, open_activities}]}`. One call = the whole folder as
plain text. Read that; work from it.

- **`needs_vision: true`** on a document means the text pass came up empty (a
  scanned/image-only PDF or an image file). Only for those, fall back to
  `documents_get {"document_id"}` and read the bytes with a vision-capable
  reader — never for the whole folder.
- If the helper can't run (no shell, or `ODOO_MCP_URL`/`ODOO_MCP_TOKEN` unset),
  fall back to `documents_get` **one document at a time**, extract what you
  need, and don't carry the base64 forward. Never fetch the whole folder's
  bytes into context at once.

## Reading a document (per file)

Extract from the document's **text**, not its filename:

- **PO number** — the authoritative PO# is *inside* the document. Filenames can
  carry the vendor's order number instead (e.g. a file named
  `Order Acknowledgement 48482500.pdf` whose real PO is `P13183` in the body).
  Search Odoo on the PO# you read from the text.
- **Line items** — item/style, color, size, quantity, and **unit price** per
  line. Vendor size upcharges are normal (base sizes one price; 2XL/3XL/4XL
  higher) — that's correct pricing, not an error.
- **Totals are a cross-check, not the source of truth.** A shipment
  acknowledgement is often **one box of a multi-shipment order**, so its total
  is legitimately less than the PO total — the missing lines ship later. Match
  **line by line**, and treat a total gap that's fully explained by un-shipped
  lines as *not* a discrepancy.

## Matching against the PO

1. `ap_search_purchase_orders {"search": "<PO#>"}` → the PO `id`. Confirm the
   vendor and `partner_ref` line up with the document.
2. `ap_get_purchase_order {"po_id": <id>}` → the lines, each with its `line_id`
   and current `price_unit`. The PO must be **confirmed** (`state = "purchase"`)
   to edit lines.
3. Pair each document line to a PO line by **(style/item, color, size)** — not
   by row order; vendors and Odoo often sort differently. A partial shipment
   matches a subset of the PO's lines; the rest staying unmatched is expected.
4. Compare `price_unit` per line.

## Correcting pricing

Batch every mismatch on a PO into **one** `ap_update_po_lines` call:

```
ap_update_po_lines {"po_id": <id>, "lines": [{"line_id": <id>, "price_unit": <doc price>}]}
```

- `freight_cost` / `fees_cost` are PO-level fields — set them only when the
  **document itself** provides an authoritative freight/fee figure. An order
  acknowledgement usually doesn't itemize freight (e.g. shipped "UPS Ground
  Collect"); a pre-existing freight estimate or a partner-level fee on the PO
  that the document doesn't contradict is **not** a line-pricing error — note
  it for the eventual invoice match and leave it.
- The tool returns `new_amount_total` — sanity-check it against the document's
  subtotal (accounting for any partial shipment).

## Mark the PO checked

Post a note onto the PO so purchasing/sales can see the review, whether or not
anything changed:

```
po_post_message {"po_id": <id>, "body": "Pricing checked against <document> — <what you found / corrected>. ..."}
```

State the source document, list any line corrections (old → new), and call out
partial-shipment or freight/fee context so a human isn't confused by a total
that doesn't tie to the PO header.

## File the document — ALWAYS (Matched / Questions)

Every reviewed document must leave the Purchasing inbox. The folder has two
sibling subfolders — **Matched** and **Questions**. File each document by the
outcome:

- **Reconciled** (prices matched, or you corrected them with confidence) → move
  the document to **Matched**.
- **A genuine question** (can't read the PO#, prices don't reconcile,
  unexpected/missing lines, wrong vendor, anything you're not sure how to fix)
  → **don't guess.** Raise it on the *document* and assign a reviewer, then move
  the document to **Questions**:

  ```
  documents_post_message {"document_id": <id>, "body": "<the specific question>", "activity_user": "Zach Tucker"}
  ```

Move with the helper (resolves the subfolder by name under the parent):

```bash
python3 scripts/po_docs.py move '{"document_id": <id>, "to": "Matched", "under": "Purchasing"}'
python3 scripts/po_docs.py move '{"document_id": <id>, "to": "Questions", "under": "Purchasing"}'
```

Or directly: resolve the subfolders once with
`documents_list_folders {"parent_id": <Purchasing id>}`, then
`documents_update {"document_id": <id>, "fields": {"folder_id": <Matched|Questions id>}}`.
There is no delete tool by design — moving (or `active:false` to archive) is how
documents leave the inbox.

Only raise a Questions activity for a **real** ambiguity. An unambiguous
correction fully supported by the vendor document (a size priced $2 off the
vendor's own confirmation) is a Matched fix, not a question — applying it is
exactly what the task asks for.

## Per-document report

For each document, report: PO number, which lines changed (old → new) or that
none did, whether you posted the "checked" note, and whether it went to Matched
or to Questions (and why). End with a folder tally so the inbox state is
obvious.

## Worked example

Folder `Purchasing` (5 docs). Intake:
`po_docs.py extract '{"folder": "Purchasing"}'`.

- **SanMar Order Confirmation, PO# P13189** — line ST485 Black size **S** reads
  $11.94 on the confirmation but $13.94 on the PO (the other base sizes are
  $11.94; 2XL $12.94, 3XL $14.94 match). Fix:
  `ap_update_po_lines {"po_id": 13145, "lines": [{"line_id": 40941, "price_unit": 11.94}]}`
  (total $1,047.90 → $1,041.90). `po_post_message` the correction → **Matched**.
- **PO# P13193 / P13194** — every line matches. `po_post_message` "checked, no
  change" → **Matched**.
- **SanMar Shipment Acknowledgement, PO# P13137** — Box 1 of a multi-shipment
  order: 6 of the PO's 11 lines, all $1.79 and matching; document total $53.70
  vs PO $98.45 is just the 5 un-shipped lines. Not a discrepancy. Note the
  partial-shipment context in the "checked" message → **Matched**.
- **Workwear Outfitters Order Acknowledgement (PO# P13183 read from the body,
  not the "48482500" filename)** — both lines match; PO also carries freight
  $2.00 and a −$2.38 fee the acknowledgement doesn't itemize (reconcile at
  invoice). Line pricing correct → **Matched**.

None needed Questions. Had any document been unreadable or failed to reconcile,
it would have gotten a `documents_post_message` activity to Zach Tucker and
moved to **Questions**.

## Model / cost note

This workload is structured extraction + numeric comparison + a deterministic
tool sequence, with the heavy PDF work pushed into `po_docs.py` (outside the
model). That keeps per-document tokens tiny and makes a **small, low-cost model
viable**:

- **`claude-haiku-4-5`** ($1 / $5 per Mtok) — the low-cost default. Ample for
  reading extracted text, pairing lines, and driving the tools, precisely
  because the script does the extraction and the Questions/Zach path catches
  anything it's unsure about.
- **`claude-sonnet-5`** ($3 / $15; intro $2 / $10 through 2026-08-31) — the
  step-up when first-pass accuracy on messy or unfamiliar vendor layouts
  matters more than the extra cost, still far below Opus. Prefer it if you see
  Haiku mis-pairing lines or missing partial-shipment/freight nuances.

The safety net is structural: keep the Questions → Zach escalation on, and a
cheaper model that flags uncertainty stays safe on live financial data.
(Model IDs/pricing per the `claude-api` skill catalog; verify with the Models
API if in doubt.)
