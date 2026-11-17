# The order-entry grid — build & apply

The grid is the fast, rep-friendly entry surface. It writes standard
`sale.order.line` records (the Order Lines tab stays the source of truth) and,
behind the scenes, constructs the manufactured products, BOMs and routes for
decorated columns. These MCP tools call the exact same `sale.order.grid_*` RPCs
the in-browser widget calls — no browser required.

## Mental model

- A **column** = one **style + color + decoration package**. (In the widget
  these render as rows, but the code calls them columns.)
- A column's **cells** = **size → quantity**. Each non-empty cell becomes one
  `sale.order.line`, tagged with the column's `grid_column_key`.
- Empty cells (qty 0 / omitted) create no line. Deleting a cell = omit it.

## The easy path: `sales_grid_add_column`

Add one style+color with a size run and decorations, without hand-building the
payload. It resolves the template's variants, builds the column and cells,
**preserves the other columns**, and applies.

```bash
# 1. find the blank template (a vendor_item)
python3 scripts/odoo_mcp.py call sales_grid_search_templates \
  '{"order_id": 42, "query": "K500"}'
#    → [{"id": 512, "display_name": "Port Authority K500", "style_number": "K500", ...}]

# 2. see its colors & sizes (the value ids you need)
python3 scripts/odoo_mcp.py call sales_grid_load_variants \
  '{"order_id": 42, "template_id": 512}'
#    → {"colors":[{"value_id":88,"name":"Red"},...],
#       "sizes":[{"value_id":301,"name":"S","sequence":1},{"value_id":302,"name":"M",...}], ...}

# 3. (optional) find decorations to attach
python3 scripts/odoo_mcp.py call sales_search_decorations '{"query":"left chest"}'

# 4. add the column
python3 scripts/odoo_mcp.py call sales_grid_add_column '{
  "order_id": 42,
  "template_id": 512,
  "color_value_id": 88,
  "size_qtys": {"301": 5, "302": 12, "303": 15, "304": 10},
  "decoration_ids": [900, 901],
  "price": 18.50
}'
```

`size_qtys` keys are **size value_ids** from `sales_grid_load_variants` (not
names). `color_value_id` is omitted only for attribute-less products. `price` is
optional (applied to every cell); `route_id` / `vendor_id` are optional per-row
overrides. Repeat step 4 per style/color.

The response is the full grid state plus `added_column_key`.

## The raw path: `sales_grid_apply`

For multi-column edits or full control, send the whole payload. **Every cell you
want to keep must be in the payload — a cell that's absent is deleted.**

```jsonc
{
  "order_id": 42,
  "payload": {
    "columns": [ /* full column config to persist — overwrites order_grid_config */
      {
        "key": "col_512_88_1",
        "tmpl_id": 512, "tmpl_name": "Port Authority K500", "product_name": "Port Authority K500",
        "style": "K500", "product_type": "vendor_item",
        "color_vid": 88, "color_name": "Red", "is_no_attr": false,
        "variant_map": {"88::301": 9001, "88::302": 9002, "88::303": 9003},
        "decoration_ids": [900, 901], "decoration_summary": "Left Chest, Back",
        "_size_names": {"301":"S","302":"M","303":"L"}, "_size_seqs": {"301":1,"302":2,"303":3}
      }
    ],
    "cells": [ /* one per non-empty cell */
      {"column_key":"col_512_88_1","product_id":9001,"size_vid":301,"qty":5,"price":18.50},
      {"column_key":"col_512_88_1","product_id":9002,"size_vid":302,"qty":12,"price":18.50}
    ],
    "row_routes": {},   // optional {col_key: route_id}
    "row_vendors": {}   // optional {col_key: vendor_id}
  }
}
```

- `variant_map` key = `"<color_vid>::<size_vid>"` → blank `product.product` id
  (`"0::0"` for attribute-less products).
- In `cells`, `product_id` is the **blank** variant id; for decorated columns
  the server swaps in the manufactured `bacon_item` variant automatically.
- **Prefer `sales_grid_add_column`** — it assembles this for you and preserves
  existing cells. Use `sales_grid_read` first if you build a raw payload, so you
  can carry the existing columns/cells forward.

Read the full state anytime with `sales_grid_read {"order_id": 42}`. Validate a
payload without saving with `sales_grid_validate`.

## Costs & prices

- `sales_grid_read_costs` / `sales_grid_apply_costs` — per-line blank &
  decoration cost. `per_unit_blank_cost` is the canonical cost field; setting a
  blank cost marks it manual. `cost_cells`: `[{sol_id, blank_cost?, decoration_cost?}]`.
- `sales_grid_calculate_prices {"order_id", "margins": {"<col_key>": 45}}` —
  set selling price from a target margin % (rounds up to $0.25). Omit `margins`
  to use the team's default markup.

## Gotchas

- **Grid becomes read-only** once the order is `sale`/`done`/`cancel` —
  `sales_grid_apply` refuses.
- **`sales_grid_apply` writes a positive selling price to the variant's global
  `product.product.lst_price`.** An explicit `$0.00` is honored on the line but
  never overwrites the catalog price.
- **Absent cell = deleted line.** `sales_grid_add_column` handles preservation;
  a hand-built `sales_grid_apply` must include every cell to keep.
- **`sales_grid_read` mutates** (it reconciles orphan lines and scrubs stale
  variant maps). Treat it as a deliberate read.
- **No concurrent-edit locking** — last apply wins. Don't interleave with a
  human editing the same order.
- **Preview after grid entry.** Decorated columns build products during
  `grid_apply`, but always run `sales_preview_order` before submit to catch any
  line entered outside the grid.
