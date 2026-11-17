# Operations field reference (purchasing → shipping)

The model-by-model map of what you can query. Use it to translate a person's
words into the right field. It documents the **curated** fields (what
`ops_field_dictionary` returns) plus the Odoo-18 and BaconCo semantics behind
them. For the *exhaustive* field list of any model, call
`ops_list_model_fields {"model": "<model>"}` — any field it marks
`filterable: true` is usable in a filter by its raw name.

Conventions:
- **type** is the logical type for the filter value (`char`/`text` → string,
  `selection` → one of the listed keys, `many2one` → an id or a dotted path,
  `date`/`datetime` → `"YYYY-MM-DD"` / `"YYYY-MM-DD HH:MM:SS"`).
- **searchable=no** ⇒ the field is a non-stored compute: it appears in
  `ops_get` output but can't go in a filter. Filter on a stored proxy instead
  (noted per field).
- Dotted paths traverse a relation: on `purchase.order.line`,
  `order_id.partner_id` filters by the parent PO's vendor.

---

## purchase.order — the buy sent to a vendor

| field | type | meaning |
| --- | --- | --- |
| `name` | char | PO number, e.g. `P00042`. Search with `ilike`. |
| `partner_id` | many2one | **Vendor.** Filter a vendor's POs; `partner_id.name ilike "adidas"` matches by name. |
| `partner_ref` | char | The vendor's own order / confirmation number. |
| `state` | selection | Lifecycle: `draft` (RFQ), `sent` (RFQ sent), **`purchase`** (confirmed PO), `done` (locked), `cancel`. "Open PO" ⇒ `state = purchase`. |
| `date_order` | datetime | When the RFQ/PO was placed. |
| `date_approve` | datetime | When the PO was confirmed. |
| `date_planned` | datetime | **Expected arrival** of the goods. "Late PO" ⇒ `date_planned < now` and not fully received. |
| `amount_total` | monetary | PO total incl. tax. **Summable** — the measure for open commitment by vendor. |
| `amount_untaxed` | monetary | PO total excl. tax. Summable. |
| `invoice_status` | selection | Billing: `no` (nothing to bill), `to invoice` (waiting bills), `invoiced` (fully billed). |
| `receipt_status` | selection | Goods receipt (Odoo 17+): `pending`, `partial`, `full`. "Not received" ⇒ `!= full`. |
| `user_id` | many2one | Buyer (purchase rep). |
| `origin` | char | Source document that generated the PO (a sale order or replenishment reference). |
| `order_line` | one2many | The PO's lines. Filter POs by a line attribute via `order_line.<field>` (matches if ANY line qualifies). |
| `company_id` | many2one | Owning company. |

Notes: `receipt_status` exists in Odoo 17+; if `ops_list_model_fields` doesn't
show it on this deployment, derive receipt state from the lines
(`qty_received < product_qty`) or the receipt pickings instead.

## purchase.order.line — one product on a PO

| field | type | meaning |
| --- | --- | --- |
| `order_id` | many2one | Parent PO. Traverse header fields via `order_id.state`, `order_id.partner_id`, `order_id.date_planned`. |
| `product_id` | many2one | The variant being bought. |
| `name` | text | Line description. |
| `product_qty` | float | **Ordered** quantity. Summable. |
| `qty_received` | float | **Received** quantity. Summable. A line is still open when `qty_received < product_qty`. |
| `qty_invoiced` | float | Vendor-billed quantity. Summable. |
| `price_unit` | float | Unit cost. |
| `price_subtotal` | monetary | Untaxed line total. Summable. |
| `date_planned` | datetime | Expected arrival for the line. |
| `state` | selection | Mirrors the parent PO state. |

To find "PO lines not fully received": the cleanest path is the **header**
`purchase.order.receipt_status != full` (Odoo's own rollup — see above), which
already ignores service lines. From the lines directly, `qty_received <
product_qty` is **not** expressible as one filter (two-field comparisons aren't a
single filter — the value side is read as a literal, not the other column). So
`ops_aggregate` `purchase.order.line` grouped by `order_id` with measures
`product_qty` + `qty_received`, and keep groups where `product_qty_sum >
qty_received_sum`. Never count distinct POs in a single `ops_search` page — that
page is bounded and gives an arbitrary count; use `total_matched` or the
aggregate.

**There is no `product_type` field on the line.** The product type lives on the
related product: filter `product_id.type` (values `consu` = physical goods /
`service` / `combo`). "Physical goods only" ⇒ `product_id.type = consu`. Do not
borrow `product_type` from another schema — it silently matches nothing here.

## vendor.tracking — inbound shipment tracking (BaconCo)

Custom model that records carrier tracking for **inbound** vendor shipments
feeding production. Field names can vary by deployment — confirm with
`ops_list_model_fields {"model": "vendor.tracking"}`.

| field | type | meaning |
| --- | --- | --- |
| `tracking_number` | char | Carrier tracking number. |
| `carrier` | char | Shipping carrier for the inbound shipment. |
| `status` | char | Latest carrier status. |
| `delivery_date` | date | Actual/expected delivery date. "Arriving this week" ⇒ `delivery_date` in range. |

The production scheduler's `production_batch_supply` tool rolls these up into a
batch's `expected_ready_date` — use that tool when the question is "when can
this job start", and `vendor.tracking` when you need the raw tracking rows.

## stock.picking — a transfer (receipt / delivery / internal)

| field | type | meaning |
| --- | --- | --- |
| `name` | char | Reference, e.g. `WH/IN/00021`. |
| `partner_id` | many2one | Vendor (on receipts) or customer (on deliveries). |
| `picking_type_code` | selection | **Direction** — the primary filter: `incoming` (receipt), `outgoing` (delivery), `internal` (transfer). |
| `picking_type_id` | many2one | The specific operation type (e.g. "WH: Receipts"). |
| `state` | selection | `draft`, `waiting` (waiting another op), `confirmed` (waiting stock), **`assigned`** (ready), `done`, `cancel`. |
| `scheduled_date` | datetime | When the transfer is expected. **Late** ⇒ `scheduled_date < now` and `state != done`. |
| `date_done` | datetime | When it was validated (completed). |
| `origin` | char | Source document (SO/PO number). |
| `carrier_id` | many2one | The `delivery.carrier` (shipping method) on an outbound transfer. |
| `carrier_tracking_ref` | char | **Outbound** carrier tracking number. |
| `location_id` / `location_dest_id` | many2one | Source / destination location. |
| `backorder_id` | many2one | Set when this picking is the backorder of a partially-done one. |
| `move_ids` | one2many | The moves (product lines) on the transfer. |

"Receipts not yet done" ⇒ `picking_type_code = incoming` + `state != done`.
"Deliveries shipped today" ⇒ `picking_type_code = outgoing` + `state = done` +
`date_done` in today's range.

## stock.move — one product's movement within a transfer

| field | type | meaning |
| --- | --- | --- |
| `product_id` | many2one | The product moved. |
| `picking_id` | many2one | Parent transfer. Traverse via `picking_id.state`, `picking_id.picking_type_code`. |
| `product_uom_qty` | float | **Demand** (planned) quantity. Summable. |
| `quantity` | float | **Done** quantity (Odoo 17+; was `quantity_done` before). Summable. |
| `state` | selection | `draft`, `confirmed`, `waiting`, `assigned` (available), `partially_available`, `done`, `cancel`. Only `done` changed inventory. |
| `date` | datetime | Expected/effective move date. |
| `date_deadline` | datetime | Commitment deadline propagated from the order. |
| `reference` | char | Usually the picking name. |
| `location_id` / `location_dest_id` | many2one | Source / destination location. |
| `sale_line_id` | many2one | Originating **sale** order line (outbound). |
| `purchase_line_id` | many2one | Originating **PO** line (inbound). **Join a receipt back to its PO** here: `purchase_line_id.order_id`. |

## stock.move.line — the detailed operation line

The most granular level: the actual pick/put operation, with lot and package.

| field | type | meaning |
| --- | --- | --- |
| `move_id` | many2one | Parent move. Traverse via `move_id.*`. |
| `picking_id` | many2one | Parent transfer. |
| `product_id` | many2one | Product handled. |
| `quantity` | float | Quantity handled by this operation line (Odoo 17+). Summable. |
| `lot_id` | many2one | Lot / serial number, if tracked. |
| `result_package_id` | many2one | Destination package the goods went into. |
| `location_id` / `location_dest_id` | many2one | From / to location. |
| `state` | selection | Mirrors the parent move state. |

Use `stock.move.line` when the question is about lots, packages, or the exact
put-away/pick location; use `stock.move` for demand-vs-done quantities.

## delivery.carrier — shipping methods

| field | type | meaning |
| --- | --- | --- |
| `name` | char | The shipping method name users pick. |
| `delivery_type` | selection | Provider/integration: `fixed`, `base_on_rule`, or a carrier connector (`fedex`, `ups`, `usps`, …). |
| `product_id` | many2one | The delivery **service product** that carries the shipping cost onto orders. |
| `fixed_price` | float | Flat price (when `delivery_type = fixed`). |
| `free_over` | float | Order amount above which shipping is free. |
| `active` | boolean | Whether the method is enabled. |

## stock.warehouse.orderpoint — reordering rule (the shortage line)

The row the replenishment report is built from — what to buy and how much.

| field | type | meaning |
| --- | --- | --- |
| `product_id` | many2one | The product the rule covers. |
| `warehouse_id` | many2one | Warehouse the rule applies to. |
| `location_id` | many2one | Stock location watched. |
| `product_min_qty` | float | **Reorder point** — replenish when forecast drops below this. |
| `product_max_qty` | float | Target level to replenish up to. |
| `qty_forecast` | float | Forecast on-hand (compute, **searchable=no**). Negative ⇒ short. |
| `qty_to_order` | float | Quantity the rule wants purchased now (compute, **searchable=no**). |
| `trigger` | selection | `auto` vs `manual` replenishment. |
| `route_id` | many2one | The route the replenishment follows (Buy vs Manufacture). |

`qty_forecast` / `qty_to_order` are computed, so read them with `ops_get` (or
`ops_search` output) rather than filtering on them. To *act* on shortages —
build POs from them — use the `replenish_*` tools, which run Odoo's report and
return curated lines with vendor / style / color / size / qty. This model is
for **reading/analyzing** the shortage picture.

## product.product — the variant (SKU level)

| field | type | meaning |
| --- | --- | --- |
| `default_code` | char | **SKU** / internal reference. Search with `ilike`. |
| `name` | char | Product name. |
| `barcode` | char | Barcode. |
| `qty_available` | float | **On hand** (compute, **searchable=no**). Read via `ops_get`. |
| `virtual_available` | float | **Forecasted** = on hand + incoming − outgoing (compute, searchable=no). |
| `list_price` | float | Default sales price. |
| `standard_price` | float | Unit **cost**. |
| `categ_id` | many2one | Product category. |
| `product_tmpl_id` | many2one | Parent template. Traverse via `product_tmpl_id.*`. |
| `active` | boolean | Whether the variant is active. |

`qty_available` / `virtual_available` are computed at the warehouse the context
points to; they can't be filtered — read them per product with `ops_get`, or use
`ebay_inventory` / the mfg reader for a bulk on-hand map.

## product.template — the parent of its variants

| field | type | meaning |
| --- | --- | --- |
| `name` | char | Template name. |
| `default_code` | char | SKU (single-variant templates). |
| `list_price` | float | Default sales price. |
| `standard_price` | float | Unit cost. |
| `type` | selection | `consu` (goods — tracks inventory), `service`, (`combo`). |
| `categ_id` | many2one | Product category. |
| `sale_ok` | boolean | Can be sold. |
| `purchase_ok` | boolean | Can be purchased. |
| `seller_ids` | one2many | Vendor pricelist lines (`product.supplierinfo`) — the vendors and their costs/lead-times. |

Variant vs template: filter/aggregate stock and moves at **`product.product`**
(the variant carries SKU + on-hand); use **`product.template`** for
catalogue-level attributes (sellable/buyable, category, vendors).

---

## Manufacturing

The production side of the operations domain. (For the guided
*scheduling* workflow — rank the queue, place batches on machines, gate on
receipt readiness — use the dedicated `production_*` tools; these `ops_*` models
are for free-form querying and analysis of the same data.)

### mrp.production.batch — the scheduling unit (BaconCo)

A group of MOs sharing a machine + slot. Field names are BaconCo-custom; confirm
with `ops_list_model_fields {"model": "mrp.production.batch"}`.

| field | type | meaning |
| --- | --- | --- |
| `name` | char | Batch name/number. |
| `state` | selection | Batch lifecycle stage. |
| `sequence` | integer | **Run order** — the batch's rank in the production queue. Lower runs first. This is the primary scheduling signal. |
| `manual_sequence` | boolean | A manufacturing manager pinned this batch's run order by hand; the scheduling agent won't re-rank it. |
| `date_planned_start` / `date_planned_finished` | datetime | *Planned* start / finish on its machine. Often unset — the run order is the decision, the slot is a refinement. |
| `datetime_started` | datetime | When the batch actually started on the floor (Start Batch on the scanned worksheet, or first transition to In Progress). |
| `datetime_done` | datetime | When the batch actually finished (stamped on the transition to Done). |
| `ship_date` | date | Date the batch must ship by. Compare to `date_planned_finished` to catch slippage. |
| `event_date` | date | Customer in-hands/event date. |
| `production_center_id` | many2one | Assigned production center. |
| `primary_workcenter_id` | many2one | The machine it's scheduled on; **unset ⇒ not yet placed**. |
| `piece_count` | integer | Total pieces (compute, searchable=no). |
| `is_late` | boolean | Past its ship date (compute, searchable=no). |
| `print_decals_status` | selection | Whether this batch's DTF / Heat Press decals have printed: `na` (none to print), `no`, `partial`, `sample`, `yes`. Anything but `na`/`yes` blocks the job. |
| `art_status` | selection | Artwork rollup across the batch's decorations and digitize demands: `not_started`, `in_progress`, `digitize`, `hold_clc`, `done`. Only `done` clears it (compute, searchable=no). |
| `production_ids` | one2many | The MOs in the batch. |

### mrp.production — manufacturing order (MO)

| field | type | meaning |
| --- | --- | --- |
| `name` | char | MO number, e.g. `MO/00123`. |
| `state` | selection | `draft`, `confirmed`, `progress`, `to_close`, `done`, `cancel`. |
| `product_id` | many2one | Product being manufactured. |
| `product_qty` | float | Quantity to produce. Summable. |
| `qty_produced` | float | Produced so far. Summable. |
| `date_start` / `date_finished` | datetime | Scheduled/effective start / finish. |
| `date_deadline` | datetime | Commitment deadline from the order. |
| `origin` | char | Source document (the sale order reference). |
| `bom_id` | many2one | BOM used. Traverse via `bom_id.*`. |
| `batch_id` | many2one | Parent production batch. Traverse via `batch_id.ship_date`, etc. |

### mrp.workorder — one operation of an MO

| field | type | meaning |
| --- | --- | --- |
| `name` | char | Operation name. |
| `production_id` | many2one | Parent MO. Traverse via `production_id.*`. |
| `workcenter_id` | many2one | Machine the operation runs on. |
| `state` | selection | `pending`, `waiting`, `ready`, `progress`, `done`, `cancel`. |
| `date_start` / `date_finished` | datetime | Scheduled/effective start / finish. |
| `duration_expected` / `duration` | float | Planned / actual minutes. |
| `product_id` | many2one | Product the MO produces. |

### mrp.bom / mrp.bom.line — bill of materials

| model.field | type | meaning |
| --- | --- | --- |
| `mrp.bom.code` | char | BOM reference. |
| `mrp.bom.product_tmpl_id` | many2one | Template the BOM builds. |
| `mrp.bom.product_id` | many2one | Specific variant it builds (optional). |
| `mrp.bom.product_qty` | float | Quantity produced per run. |
| `mrp.bom.type` | selection | `normal` (manufacture) / `phantom` (kit). |
| `mrp.bom.bom_line_ids` | one2many | Component lines. Filter BOMs by a component via `bom_line_ids.product_id`. |
| `mrp.bom.line.bom_id` | many2one | Parent BOM. |
| `mrp.bom.line.product_id` | many2one | The component product. |
| `mrp.bom.line.product_qty` | float | Component quantity per BOM run. Summable. |
| `mrp.bom.line.product_uom_id` | many2one | Component UoM. |

### production.center — a group of workcenters

| field | type | meaning |
| --- | --- | --- |
| `name` | char | Center name (e.g. "Screen Print Floor"). |
| `workcenter_ids` | many2many | The machines grouped under this center. |

---

## How the models join (the make + receiving/shipping chain)

```
sale.order ──▶ stock.picking (outgoing) ──▶ stock.move ──▶ stock.move.line
     │               ▲  carrier_id → delivery.carrier
     └──▶ mrp.production (MO) ──▶ mrp.workorder ──▶ workcenter_id
                │ batch_id → mrp.production.batch → production_center_id
                └ bom_id → mrp.bom ──▶ mrp.bom.line (components)
purchase.order ──▶ purchase.order.line
      │                     ▲ purchase_line_id
      └──▶ stock.picking (incoming) ──▶ stock.move ──▶ stock.move.line
stock.warehouse.orderpoint ──▶ (replenish_* builds) ──▶ purchase.order
```

- **Receipt → PO:** `stock.move.purchase_line_id.order_id` gives the PO a
  receipt line came from.
- **Delivery → SO:** `stock.move.sale_line_id.order_id` gives the sale order a
  shipment line fulfils.
- **MO → batch / order:** `mrp.production.batch_id` groups MOs into the
  scheduling unit; `mrp.production.origin` (and `sales_order_manufacturing`) tie
  an MO back to its sale order. `mrp.workorder.production_id` is the parent MO.
- **PO/receipt on a sale order:** use `sales_order_inventory_moves {"order_id":
  ...}` to get an order's pickings already categorised into receipts /
  transfers / shipments / dropships / returns.
