# Replenishment → vendor purchasing

The full loop for buying what the Odoo replenishment report says to buy, for a
vendor whose ordering is done by a **browser-driven purchasing skill** (e.g.
`drivethru-adidas-click`) rather than an Odoo-side API integration.

```
replenish_run_report ──▶ curate ──▶ replenish_to_po ──▶ [vendor skill checkout]
        ▲                                                        │
        │                                                        ▼
   (re-run if ids                              replenish_update_po / po_post_message
    went stale)                                                  │
                                                                 ▼
                                                       replenish_confirm_po
```

Every step is one `drivethru_mcp` MCP tool, except the checkout, which is a
different skill. Two steps write live Odoo data (`replenish_to_po`,
`replenish_confirm_po`) — **confirm with the user before each**.

## 1. Run the report — `replenish_run_report`

Rebuilds the replenishment report (splitting demand by production batch / sales
order) and returns the shortage lines. Filter to the vendor you're buying for.

```json
// call
{ "vendor": "Adidas" }
// or exact: { "vendor_id": 412 }, and/or scope: { "batch": "Batch12345" }
```

Each returned line:

```json
{
  "id": 90871,                       // orderpoint id — the handle for replenish_to_po
  "product_id": 5521, "product_sku": "ADI-TEE-BLK-L",
  "style": "AD100", "color": "Black", "size": "L",
  "qty_to_order": 12, "qty_forecast": -12, "qty_on_hand": 0,
  "price": 8.50, "uom": "Units",
  "vendor_id": 412, "vendor_name": "Adidas",
  "vendor_uses_integration": false,  // false ⇒ buy via a purchasing skill, not Odoo's API
  "production_batch_id": 771, "production_batch_name": "Batch12345",
  "sale_order_id": 3310, "sale_order_name": "S03310",
  "is_out_of_stock": false, "has_alert": false
}
```

Useful args: `refresh` (default true — set false to skip the rebuild),
`only_report_lines` (default true — set false to also include standing
reordering rules), `only_to_order` (default true), `product`, `style`,
`out_of_stock_only`, `limit`. `replenish_get_orderpoint {"orderpoint_id": …}`
returns one line with full demand attribution (driving MOs / PC tickets / SOs)
and any open alerts.

## 2. Curate

Keep only the lines the user asked for — this is **your** filter, applied to the
report output:

- *"all items from Adidas"* → every line for the vendor.
- *"…for Batch12345"* → lines where `production_batch_name == "Batch12345"`.
- *"…for order S03310"* → lines where `sale_order_name == "S03310"`.

Show the kept lines back to the user (style / color / size / qty) and get a
go-ahead before replenishing.

## 3. Add to a PO — `replenish_to_po`

```json
{ "orderpoint_ids": [90871, 90872, 90873] }
```

Runs `action_replenish` and **returns the draft PO(s)** it created or grew.
Standard Odoo doesn't report which PO a replenish produced; this tool diffs the
draft PO lines around the call to recover it — so trust its `purchase_orders`,
never re-search for "the newest draft PO".

```json
{
  "replenished_orderpoint_ids": [90871, 90872, 90873],
  "purchase_order_count": 1,
  "purchase_orders": [
    {
      "id": 6120, "name": "P06120", "state": "draft",
      "partner_name": "Adidas", "vendor_order_number": null,
      "lines": [
        { "line_id": 44011, "style": "AD100", "color": "Black", "size": "L",
          "product_qty": 12, "price_unit": 8.50, "product_sku": "ADI-TEE-BLK-L" }
      ]
    }
  ],
  "warnings": []
}
```

`warnings` flags lines that produced no PO (manufacture route, held sales order,
no buy rule) and any ids that went stale — surface these to the user.

## 4. Run the vendor skill — `drivethru-adidas-click`

**Discover the skill.** The vendor's purchasing skill is named
`drivethru-<vendor>-click` — for Adidas, **`drivethru-adidas-click`**. Read its
`SKILL.md`; it is a CLI, invoked one action at a time:

```bash
echo '<json-args>' | python3 scripts/adidas.py create-purchase-order
```

If there is no matching skill for the vendor, stop and tell the user — do not
improvise a checkout.

**Input you build from the returned PO.** Map the Odoo PO `name` → `po_number`
(adidas caps it at 18 chars / a restricted charset and auto-sanitizes with a
warning), and each PO line → `{style, size, quantity}`:

```json
{
  "purchase_order": {
    "po_number": "P06120",
    "lines": [
      { "style": "JW4306", "size": "L", "quantity": 12 }
    ]
  },
  "on_insufficient_stock": "pause",
  "confirm": false
}
```

- **`color` is optional** — the adidas article number (`style`) already encodes
  the colorway, so you don't pass color. Keep the Odoo line's color/size on your
  side to map the result back.
- **Dry-run first.** `confirm: false` fills the cart + checkout and returns a
  preview without ordering. Only set `confirm: true` once the user has approved
  — it places a **real order** (no sandbox).
- There is **no `line_id`** in the adidas payload; the join key back to the Odoo
  PO line is **(style, size)** — match on those (plus color if a style has
  multiple colorways in the same PO).

**Result you get back** (`schemas.py::OrderResult`):

```json
{
  "status": "submitted",
  "po_number": "P06120",
  "confirmation_number": "0123456789",
  "order_total": "$101.40",
  "total_quantity": 12,
  "lines": [
    { "style": "JW4306", "color": "BLACK", "size": "L",
      "quantity": 12, "unit_price": "$8.45", "line_total": "$101.40" }
  ],
  "out_of_stock": [],
  "warnings": []
}
```

- `status`: `submitted` (order placed — `confirmation_number` set) · `dry_run`
  (confirm was false) · `needs_confirmation` (see step 6) · `error`.
- **Prices are strings** (`"$8.45"`) read off the priced review page — parse the
  numeric value before writing it back.

## 5. Write the result back — `replenish_update_po`

Map the adidas result → the Odoo draft PO (this is the pre-confirm sibling of
`ap_update_po_lines`, which is for confirmed POs). Match each result line to its
Odoo PO line by (style, size) to get the `line_id`; parse the `$`-prices to
numbers; `confirmation_number` → `vendor_order_number`:

```json
{
  "po_id": 6120,
  "vendor_order_number": "0123456789",
  "lines": [
    { "line_id": 44011, "price_unit": 8.45 }
  ]
}
```

`order_total` is the **net wholesale** total (freight / FedEx charges aren't
broken out by the skill); only pass `freight_cost` if you have a separate
freight figure. You can also pass these same fields directly to
`replenish_confirm_po` to price and confirm in one call.

## 6. Out-of-stock & other exceptions — `po_post_message` / `po_get_messages`

The adidas skill has its own out-of-stock gate. With `on_insufficient_stock:
"pause"` (the default), a line that can't be fully filled makes it **order
nothing** and return:

```json
{ "status": "needs_confirmation",
  "out_of_stock": [ { "style": "JW4306", "size": "L", "requested": 12, "available": 4 } ],
  "message": "..." }
```

On that result, record the issue **onto the Odoo PO** and pause it:

```json
// po_post_message
{
  "po_id": 6120,
  "issue_type": "out_of_stock",
  "body": "adidas is short on JW4306 / L — ordered 12, only 4 available. Backorder the 4, substitute, or drop?",
  "activity_user_id": 6,
  "activity_summary": "Out of stock on P06120"
}
```

This posts a chatter note and drops a To-Do activity for the responsible user.
**Do not confirm the PO while an issue is open.** Later, read the reply:

```json
// po_get_messages
{ "po_id": 6120 }
```

Returns the chatter (newest first, plain text) + open activities. Then act on the
human's path forward by **re-running `create-purchase-order`** with the matching
policy:

- **Order anyway** (accept delayed/backordered delivery) → `on_insufficient_stock: "order"`.
- **Drop** the short line(s) → `on_insufficient_stock: "skip"`, and set that Odoo
  line's `product_qty` → 0 via `replenish_update_po`.
- **Substitute** → edit the `lines` (different size/style) and re-run.

If the user's original request already pre-authorized a choice (*"order anything
out of stock"* / *"drop out-of-stock items"*), set `on_insufficient_stock`
up-front and skip the pause. Only once a clean `submitted` result comes back do
you write pricing and confirm.

## 7. Confirm — `replenish_confirm_po`

```json
{ "po_id": 6120 }
```

Confirms the PO (`state` → `purchase`, creating receipts) **with `skip_api`
always on** — the vendor skill already placed the order, so Odoo must not push
it through a vendor integration again. Returns `resubmitted_to_vendor_api:
false` to make that explicit.

## Safety notes

- **Never double-order.** Confirmation happens only through
  `replenish_confirm_po`; it is hard-wired to skip Odoo's vendor submission.
  The real purchase happens once, in the vendor skill.
- **Report lines are volatile.** The report rebuilds its orderpoint rows on
  every run, so an `orderpoint_id` can disappear between `run_report` and
  `replenish_to_po`. If ids come back under `warnings` as vanished, re-run
  `run_report` and retry with fresh ids.
- **Confirm live writes with the user.** `replenish_to_po` and
  `replenish_confirm_po` change live Odoo data — state what you're about to do
  and get a go-ahead, per the skill's write-safety rule.
- **Integrated vendors are different.** If a line's `vendor_uses_integration`
  is true, that vendor already has an Odoo-side API integration — buying it is
  the normal confirmed-PO flow, not a `drivethru-<vendor>-click` skill. This
  loop is for the click-to-buy vendors.
