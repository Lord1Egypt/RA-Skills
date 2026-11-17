# Operations query patterns

Worked `ops_search` / `ops_aggregate` recipes for the questions this agent gets
most. Each shows the tool call arguments (the JSON you pass to
`python3 scripts/odoo_mcp.py call <tool> '<json>'`). Field names come from
`ops_field_dictionary`; confirm any you're unsure of before calling.

## Purchasing

**Open purchase orders for a vendor**
```json
// ops_search
{ "model": "purchase.order",
  "filters": [
    { "field": "state", "op": "=", "value": "purchase" },
    { "field": "partner_id.name", "op": "ilike", "value": "adidas" }
  ],
  "order_by": "date_planned asc" }
```

**POs past their expected arrival and not fully received** (the classic "late
PO" sweep)
```json
{ "model": "purchase.order",
  "filters": [
    { "field": "state", "op": "=", "value": "purchase" },
    { "field": "date_planned", "op": "<", "value": "2026-07-14" },
    { "field": "receipt_status", "op": "!=", "value": "full" }
  ],
  "order_by": "date_planned asc" }
```
If `receipt_status` isn't present on the deployment, drop that filter and use the
line-aggregate fallback below.

**Not fully received AND confirmed more than a week ago** (the receipt-status
sweep — answer it at the PO header, in one call, no per-line looping)
```json
{ "model": "purchase.order",
  "filters": [
    { "field": "state",          "op": "=",  "value": "purchase" },
    { "field": "receipt_status", "op": "!=", "value": "full" },
    { "field": "date_approve",   "op": "<",  "value": "2026-07-08 00:00:00" }
  ],
  "fields": ["name", "partner_id", "receipt_status", "date_approve"],
  "order_by": "date_approve asc" }
```
- The **count is `total_matched`** from the response — *not* the number of rows on
  the page. To list every PO, page (`offset`/`limit`) until collected ==
  `total_matched`.
- `date_approve` = when the PO was confirmed; "more than a week ago" from
  2026-07-15 ⇒ `< 2026-07-08 00:00:00`.
- `receipt_status` (Odoo 17+) is Odoo's own rollup of "some physical line still
  short," and it already ignores service lines — so it needs no product-type
  filter. Confirm it exists first with
  `ops_list_model_fields {"model":"purchase.order"}`; if absent, use the fallback.

**Same question from the lines, when `receipt_status` is absent** (aggregate —
never page-count, never a two-field filter)
```json
{ "model": "purchase.order.line",
  "filters": [
    { "field": "order_id.state",        "op": "=", "value": "purchase" },
    { "field": "order_id.date_approve", "op": "<", "value": "2026-07-08 00:00:00" },
    { "field": "product_id.type",       "op": "=", "value": "consu" }
  ],
  "group_by": ["order_id"],
  "measures": ["product_qty", "qty_received"] }
```
Keep each `order_id` group where `product_qty_sum > qty_received_sum` — that set is
the not-fully-received POs. Physical goods only via `product_id.type = consu`
(the type lives on `product_id`; there is **no** `product_type` field on the
line). The subtraction happens on aggregated sums, one row per PO, so it dodges
both the page-count trap and the impossible `qty_received < product_qty` filter.

**Inbound tracking on a set of POs — delivered but not yet received**
```json
// 1) confirm the real field names first — they vary by deployment
// ops_list_model_fields {"model": "vendor.tracking"}
// 2) pull tracking for the base-set PO ids (the PO link field name is deployment-specific)
{ "model": "vendor.tracking",
  "filters": [ { "field": "<po_link_field>", "op": "in", "value": [/* PO ids */] } ],
  "fields": ["<po_link_field>", "tracking_number", "carrier", "status", "delivery_date"] }
```
The "delivered > 1 day ago" group = `status` is the delivered value **and**
`delivery_date < <yesterday>`. Read the exact `status` selection/text value from
the field dictionary — don't assume the literal `"delivered"`. A tracking sweep
that returns nothing is only trustworthy if you've confirmed the link + status
field names actually exist; otherwise "none found" may just be a bad field name.

**Open PO value by vendor** (analysis)
```json
// ops_aggregate
{ "model": "purchase.order",
  "filters": [ { "field": "state", "op": "=", "value": "purchase" } ],
  "group_by": ["partner_id"],
  "measures": ["amount_total"],
  "order_by": "amount_total_sum desc" }
```

**PO lines still awaiting receipt, by product**
```json
{ "model": "purchase.order.line",
  "filters": [ { "field": "state", "op": "=", "value": "purchase" } ],
  "group_by": ["product_id"],
  "measures": ["product_qty", "qty_received"] }
```
Then per group, `product_qty_sum − qty_received_sum` is the outstanding qty.

## Receiving & inbound

**Receipts not yet done** (open incoming transfers)
```json
{ "model": "stock.picking",
  "filters": [
    { "field": "picking_type_code", "op": "=", "value": "incoming" },
    { "field": "state", "op": "not in", "value": ["done", "cancel"] }
  ],
  "order_by": "scheduled_date asc" }
```

**Late receipts** (scheduled in the past, still open)
```json
{ "model": "stock.picking",
  "filters": [
    { "field": "picking_type_code", "op": "=", "value": "incoming" },
    { "field": "state", "op": "not in", "value": ["done", "cancel"] },
    { "field": "scheduled_date", "op": "<", "value": "2026-07-14 00:00:00" }
  ] }
```

**A receipt's moves back to their PO**
```json
{ "model": "stock.move",
  "filters": [ { "field": "picking_id", "op": "=", "value": 12345 } ],
  "fields": ["product_id", "product_uom_qty", "quantity", "state", "purchase_line_id"] }
```
Then `ops_get {"model": "purchase.order.line", "id": <purchase_line_id>}` →
`order_id` for the PO.

## Shipping & outbound

**Deliveries shipped today**
```json
{ "model": "stock.picking",
  "filters": [
    { "field": "picking_type_code", "op": "=", "value": "outgoing" },
    { "field": "state", "op": "=", "value": "done" },
    { "field": "date_done", "op": ">=", "value": "2026-07-14 00:00:00" }
  ] }
```

**Ready-to-ship deliveries with no tracking number yet**
```json
{ "model": "stock.picking",
  "filters": [
    { "field": "picking_type_code", "op": "=", "value": "outgoing" },
    { "field": "state", "op": "=", "value": "assigned" },
    { "field": "carrier_tracking_ref", "op": "unset" }
  ] }
```

**Deliveries by carrier** (analysis)
```json
{ "model": "stock.picking",
  "filters": [ { "field": "picking_type_code", "op": "=", "value": "outgoing" } ],
  "group_by": ["carrier_id"],
  "measures": [] }
```

## Inventory & replenishment

**Shortage lines (reordering rules) in a warehouse**
```json
{ "model": "stock.warehouse.orderpoint",
  "filters": [ { "field": "warehouse_id", "op": "=", "value": 1 } ],
  "order_by": "product_min_qty desc" }
```
`qty_to_order` / `qty_forecast` are computed — read them from the returned
records; to actually build POs from shortages use `replenish_run_report` /
`replenish_to_po`, not this model.

**A product's stock position**
```json
// ops_get — qty_available / virtual_available are computes, so use get, not a filter
{ "model": "product.product", "id": 5521,
  "fields": ["default_code", "name", "qty_available", "virtual_available",
             "standard_price"] }
```

**Find a product by SKU**
```json
{ "model": "product.product",
  "filters": [ { "field": "default_code", "op": "ilike", "value": "ADI-TEE" } ],
  "fields": ["default_code", "name", "product_tmpl_id"] }
```

## Counting correctly

The single biggest source of wrong answers here is reporting a count that came
from the wrong place. Get counts from one of exactly two primitives:

- **`total_matched`** on an `ops_search` response — the true size of the match.
  The returned `rows` are one bounded page; `len(rows)` is the page size, not the
  count. Never report "N records" by eyeballing a returned list unless you've
  paged the entire set and it equals `total_matched`.
- **`ops_aggregate`** — for any sum, average, or grouped breakdown, and for a
  count under a condition the filters can express. It runs over the whole match
  server-side, so there's no page to miscount.

Reruns are deterministic: identical filters ⇒ identical `total_matched`. If two
runs disagree, the query changed or a page was miscounted — reconcile the exact
filters, don't invent a reason the data "moved."

## Tips

- **Dates**: pass `"YYYY-MM-DD"` for date fields, `"YYYY-MM-DD HH:MM:SS"` for
  datetimes. A "today" bound is the start of the day; a range needs two filters
  (`>=` start and `<` next-day-start).
- **Two-field comparisons** (e.g. `qty_received < product_qty`) aren't a single
  filter — the value side is read as a literal, not the other column. Either
  aggregate both and subtract (one row per group), or pull the candidate set with
  a coarse filter and check the pair per record in `ops_get` output.
- **Totals**: `ops_search` returns `total_matched` (the full match count, not
  just the page). `ops_aggregate` is the tool when the user wants sums/averages
  or a breakdown.
- **Unknown field?** The error names the bad field and points at
  `ops_list_model_fields`. Call it for the model, pick the right field, retry.
  Verify a field exists *before* filtering on it — a wrong name can silently
  match nothing (a count that quietly collapses) rather than erroring.

## Anti-patterns — what silently produces a wrong number

Each of these has shipped a confidently-wrong count. Recognise and avoid them:

- **Faking a shell/SQL run.** There is no `env[...]`, no SQL — only the `ops_*`
  tools. Never claim to have run one; translate any shared shell code into
  `ops_*` calls and run *those*.
- **Counting a page.** Reporting `len(rows)` from an `ops_search` page instead of
  `total_matched`. A line search can match tens of thousands of rows and hand
  back only the first page — counting distinct parents in that page gives an
  arbitrary number that changes with the filter.
- **A two-field filter.** `{"field":"qty_received","op":"<","value":"product_qty"}`
  compares `qty_received` to the *string* `"product_qty"`, not the column. Use
  `receipt_status` or an aggregate-and-subtract.
- **A guessed field name.** `product_type` (doesn't exist — use `product_id.type`);
  an assumed `purchase_order_id` / `status` on `vendor.tracking` without checking.
  Confirm with `ops_list_model_fields` first.
- **A number from memory.** Restating a prior count, or "it should be the same,"
  without re-running the query and reading the fresh `total_matched`.
- **Rationalising a swing.** If two runs disagree, your method is wrong, not the
  data — reconcile the exact filters instead of narrating why it "changed."
