# Order-entry fields & model background

## The two product kinds (this drives everything)

- **`vendor_item`** — a raw **blank**: a purchasable garment variant with a
  style number, color, size, SKU, and a vendor (SanMar, S&S, Alpha Broder).
- **`bacon_item`** — a **manufactured end item** = blank + decoration(s). It has
  a 1-line bill of materials whose component is the blank, and Make-to-Order +
  Manufacture routes so confirming the order launches a purchase order for the
  blank and a manufacturing order for the decoration.

A rep thinks "50 red K500 polos, embroidered left chest." The system needs, for
each size, a `bacon_item` variant with a BOM pointing at the right blank
variant, correct routes, a vendor on the blank, and the decoration linked. The
**grid + Preview** build all of that (see `grid_build_and_apply.md`). You never
touch a BOM or a route by hand.

### End-item construction (Preview)

`sales_preview_order` runs `create_ad_hoc_end_items()`, which for every line
that is a raw blank carrying decoration tags (or a bacon_item whose tags drifted
from its template) finds-or-creates the `bacon_item` template + size variants +
BOM + routes and swaps the line onto the manufactured variant. **It runs on
Preview, not on confirm** — so always Preview before you submit. It's
idempotent and safe to re-run. (Template matching is by name, so avoid renaming
constructed products mid-order.)

## Discover every field

`sales_list_model_fields` (from `drivethru-odoo`) enumerates **every** field on
a model with its type, whether it's stored/filterable, selection values, and
relation. It now covers `sale.order`, `sale.order.line`, `decoration`,
`decoration.request`, `decoration.request.requirement`,
`decoration.customization.line`, `decoration_method`, `decoration_location`,
`sale.order.department`, plus the product/mrp/stock graph.

```bash
python3 scripts/odoo_mcp.py call sales_list_model_fields '{"model":"decoration.request"}'
python3 scripts/odoo_mcp.py call sales_list_model_fields '{"model":"sale.order","filter":"date"}'
```

The curated highlights below are what matters for **entry** (the read-side
`sales_field_dictionary` covers querying).

## `sale.order` — entry-relevant fields

Writable via `sales_create_order` / `sales_update_order` unless noted.

| Field | Meaning / note |
| --- | --- |
| `partner_id` | Customer. Required. (Set at create; drives auto-population.) |
| `order_contact` | Order contact (a child of the customer); used for proof approvals & emails. |
| `customer_po` | Customer PO #. **Required when the customer has `requires_po`.** Chipply: no duplicates. |
| `commitment_date` | **Requested Ship Date. Required to confirm** (except website / chipply). This is "the ship date" in most requests. |
| `event_date` | Customer's event / in-hands date. Drives digitize due dates. |
| `expected_date` | Internal expected ship date. |
| `sale_order_department` | Department. **Required when the customer has `required_department`.** |
| `user_id` / `team_id` | Salesperson / sales team (auto-set from customer). |
| `shipping_policy` | `by_order` (default) or `by_batch` (auto-splits the pick per production batch). |
| `require_proof_approvals` | Default **true** — order wants decoration proofs approved before confirm (advisory gate). |
| `shipping_label_notes` | **Required when the customer has `requires_shipping_label_notes`.** |
| `shipping_attn` | Order-specific ship-to attention (intentionally NOT copied from the partner). |
| `carrier_id` | Delivery method. Name "Dropship" forces the Dropship route on all lines. |
| `customer_shipping_account` | Required if the carrier `carrier_requires_customer_account`. |
| `priority` | `0` Normal / `1` Urgent (propagates to receipts/MOs). |
| `is_on_hold` (read-only) | Hold flag — set via `sales_set_hold`, not a direct write. |
| `sale_order_linked_decorations` (computed) | The aggregate of all decorations on the order — what the checklist inspects. |
| `state` (computed) | `draft → sent → submitted → sale → done / cancel`. Note the custom **`submitted`** stage. |

## `sale.order.line` — entry-relevant fields

| Field | Meaning / note |
| --- | --- |
| `product_id` | The variant. For a decorated line this becomes the `bacon_item` after Preview. |
| `product_uom_qty` | Quantity. |
| `price_unit` | Selling price. `None`/omitted = let Odoo price; explicit `0` is honored. |
| `decoration_tags` | **The key entry field.** The decorations on this line — auto-populates from the product's linked decorations, and the Preview pipeline keys off it. |
| `per_unit_blank_cost` | Blank unit cost (canonical cost field). Enter via the cost grid; blocks quote-send if 0. |
| `vendor_id` | Force a specific vendor for this line's blank at procurement. |
| `customization_lines` | Per-unit names/numbers for custom-text decorations. |
| `grid_column_key` | Tags a line as belonging to a grid column. Lines without it are "manual" and invisible to the grid. |
| `product_style` / `product_color` / `product_size` / `product_sku` | Blank attributes (read-only, related). |
| `display_type` | Set for section/note lines (not real product lines). |

## `decoration.request` — the essentials for entry

Full field list via `sales_list_model_fields {"model":"decoration.request"}`.
The ones you'll touch:

| Field | Meaning |
| --- | --- |
| `state` | `created → progress → ready → sent → (revision) → approved → done`, or `cancelled`. |
| `sale_order_id` | The order this RFD belongs to. |
| `decoration_ids` (computed) | Decorations aggregated from the request's requirement lines. |
| `manual_decoration_ids` | Decorations added directly (the "Art tab"). |
| `approval_line_ids` | One approval line per decoration; customer signs each. |
| `user_id` | Assignee (artist). |
| `due_date` | Defaults to today+2. |
| `is_approved` / `has_unapproved_decorations` | Approval rollups. |

See `decoration_flow.md` for how requests are created and advanced.

## Where the model lives (for deeper digging)

- `sales_module_addon/models/sale_order.py`, `sale_order_line.py` — the SO and
  line, the confirm pipeline, end-item construction.
- `sales_order_grid_entry/models/sale_order.py` — the grid RPCs.
- `artwork_module_custom/models/decoration.py`, `decoration_request.py` — the
  decoration models.
- `res_partner_addon/models/res_partner.py`, `sale_order.py` — customer flags
  and the partner confirm gates.
