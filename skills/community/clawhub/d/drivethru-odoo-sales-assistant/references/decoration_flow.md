# Decorations, requests & customization

A **decoration** is one piece of art applied at one location by one method
(embroidery, DTF, heat press, screen print, promotional). It carries the method,
location, color spec, size, production files, and approval state — and drives
the manufacturing workorders. Decorations get onto an order via a line's
`decoration_tags` (auto-populated from the product's linked decorations) and are
aggregated on the order as `sale_order_linked_decorations`.

## Find or create decorations

```bash
# method + location ids (both are REQUIRED to create a decoration)
python3 scripts/odoo_mcp.py call sales_list_decoration_options '{}'

# search the catalogue
python3 scripts/odoo_mcp.py call sales_search_decorations \
  '{"query":"ABC logo","method_id":3,"production_ready":true}'

# create a draft decoration
python3 scripts/odoo_mcp.py call sales_create_decoration '{
  "name":"ABC Corp Logo - Left Chest",
  "decoration_method_id":3, "decoration_location_id":7,
  "num_colors":2, "size_width":3.5, "size_height":2.0
}'
```

Odoo **refuses exact duplicates** (same design + method + location + size).
Method and location are mandatory. Attach decorations to a column with the grid
(`decoration_ids` on `sales_grid_add_column`), or order-wide with
`sales_link_decorations {"order_id","decoration_ids":[...]}`.

## Production readiness (a confirm gate)

A decoration is **production-ready** only when its production file exists:

| Method | Needs |
| --- | --- |
| Embroidery | a **DST** file (`embroidery_production_dst`) |
| DTF / Heat Press | a **PNG** file (`dtf_production_png`) |
| Screen Print / Promotional | never auto-ready via this compute |

At confirm, **all linked decorations must be production-ready** — except
**Embroidery is exempt** from this gate (an embroidery decoration confirms even
without its DST). Not-ready decorations are a **blocking-overridable** checklist
item: only a manager (`can_confirm_so_without_production_art`) or
`force_confirm=true` gets past it. `sales_search_decorations` reports
`production_ready`, `has_dst`, `has_dtf_png` per decoration.

## Decoration requests (RFD) & approvals

A **decoration request** (RFD) is the art/proof workflow for an order.

```bash
# create/generate an RFD from the grid's decorated columns
python3 scripts/odoo_mcp.py call sales_create_decoration_request \
  '{"order_id": 42, "generate": true}'
#   → builds one process per shared art set, one requirement per decoration

# read it
python3 scripts/odoo_mcp.py call sales_get_decoration_request '{"request_id": 88}'

# advance it through the workflow (whitelisted actions)
python3 scripts/odoo_mcp.py call sales_advance_decoration_request \
  '{"request_id": 88, "action": "mark_ready"}'
```

State machine: `created → progress → ready → sent → (revision) → approved →
done` (or `cancelled`). Whitelisted `action` values for
`sales_advance_decoration_request`: `set_in_progress`, `mark_ready`,
`self_approve`, `mark_done`, `cancel`, `convert_requirements`,
`create_decoration`.

Notes:
- `mark_ready` validates the decorations (size, colors, thumbnail) and syncs
  one approval line per decoration.
- `mark_done` requires all linked/manual decorations to be in a done-ish state.
- `self_approve` needs the self-approve permission group.
- Two link paths exist: decorations attached via **requirement lines** land in
  `decoration_ids` (validated/approved/gating); decorations created via
  `create_decoration`/`convert_requirements` may only be linked by reverse
  pointer — prefer requirement lines or `manual_decoration_ids` so they count.

## Custom text (names / numbers) — a hard confirm gate

Decorations with `includes_custom_text` (personalized names/numbers) need **one
`decoration.customization.line` per unit** on the line. If a line has qty 20 and
a custom-text decoration, it needs 20 customization values, or confirm blocks:

```bash
python3 scripts/odoo_mcp.py call sales_upload_customizations '{
  "order_line_id": 55123,
  "decoration_id": 902,
  "values": [
    {"value":"SMITH","type":"name"},
    {"value":"12","type":"number"},
    {"value":"JONES","type":"name"}
  ]
}'
```

`type` is `name` | `number` | `other`. The `value` is case-sensitive — it feeds
the production file exactly as typed. The checklist's `customization_lines`
check reports any line short of one-per-unit.
