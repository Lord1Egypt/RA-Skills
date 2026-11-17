---
name: drivethru-odoo-sales-assistant
description: Enter and manipulate BaconCo sales orders in Odoo the way a rep does — through the `drivethru_mcp` MCP server's sales-entry tools. BaconCo is a custom-apparel manufacturer where the product is constructed at order time (blank garment + decoration → finished good), so a sale order is really a manufacturing order. This skill creates a draft order, reads the customer's internal notes for special handling, drives the order-entry grid (style + color + size→qty + decorations, building the manufactured products/BOMs/routes behind the scenes), attaches decorations and decoration requests, enters per-unit customizations, runs a pre-submission checklist, and submits/confirms. Builds on `drivethru-odoo`. Use whenever the user wants to create, build up, edit, price, or confirm a sales order / quote, work the sales-order grid, add decorations or a decoration request, or enter an order from scratch.
version: 0.1.0
emoji: 🧾
homepage: https://www.odoo.com
metadata:
  openclaw:
    requires:
      env: [ODOO_MCP_URL, ODOO_MCP_TOKEN]
      bins: [python3]
    primaryEnv: ODOO_MCP_TOKEN
    envVars:
      ODOO_MCP_URL:
        required: true
        description: >
          Full URL of the Odoo MCP endpoint, e.g.
          `https://odoo.example.com/drivethru_mcp/v1` (the MCP server exposed by
          the `drivethru_mcp` Odoo module, not the Odoo base URL).
      ODOO_MCP_TOKEN:
        required: true
        description: >
          The `drivethru.mcp_key` value from the Odoo `drivethru_mcp` module,
          sent as `Authorization: Bearer`. Treat as a secret; never paste into
          chat.
    install:
      uv:
        - mcp>=1.9.0
---

# BaconCo Sales Order Assistant

This skill lets you **build and manipulate sales orders** in BaconCo's Odoo —
create an order, work the order-entry grid, attach decorations, run the
pre-submission checklist, and submit/confirm — by calling the `drivethru_mcp`
MCP server's `sales_*` entry tools. It is the **write** companion to
[`drivethru-odoo`](../drivethru-odoo/SKILL.md) (which reads the sales book) and
uses the same MCP client and credentials.

```bash
# Discover the tools (names/schemas evolve — trust this over any list here)
python3 scripts/odoo_mcp.py tools
# Call one
python3 scripts/odoo_mcp.py call <tool_name> '{"...": "..."}'
echo '{"...": "..."}' | python3 scripts/odoo_mcp.py call <tool_name>
```

Credentials (`ODOO_MCP_URL`, `ODOO_MCP_TOKEN`) come from the environment; if
either is missing the script exits with `config_error` — stop and tell the
user. Never ask them to paste the key into chat.

## The one thing to understand first

**At BaconCo the product usually does not exist until the order is entered.**
A t-shirt line isn't "pick a product" — it's "construct a manufactured
`bacon_item` = a blank garment + decoration(s), with a bill of materials
(component = the blank), Make-to-Order + Manufacture routes, a vendor on the
blank, and linked decorations." All of that has to be **correct before
confirm**, or purchasing buys the wrong blank, workorders come out empty, and
the order ships wrong — silently, days later. The sale order is where
manufacturing truth is set.

You do **not** build any of that by hand. The Odoo model does it. Your job is
to feed it correct inputs (style, color, size, decoration) through the grid and
then **run the checklist before you submit**. See
[`references/order_entry_fields.md`](references/order_entry_fields.md) for the
full model background.

## The golden path

1. **Read the customer first.** `sales_get_customer {"partner_id": <id>}` —
   read `internal_notes` (and `commercial_internal_notes`) for *special actions
   for this customer*, and note the hard flags (`requires_po`,
   `required_department`, `requires_shipping_label_notes`, `approval_state`).
   Set those on the order up front. (Find the id with `sales_search_customers`.)
   → [`references/customer_prep.md`](references/customer_prep.md)
2. **Create the draft.** `sales_create_order {"partner_id", ...}` — customer
   settings (salesperson, term, team) auto-populate. It returns the order, the
   customer prep bundle, and an initial checklist.
3. **Add product + decorations via the grid.**
   `sales_grid_search_templates` → `sales_grid_load_variants` →
   `sales_grid_add_column` (one style + color + size→qty + decorations), repeat
   per style/color. → [`references/grid_build_and_apply.md`](references/grid_build_and_apply.md)
4. **Handle decorations.** Create/attach decorations, spin up a decoration
   request (RFD), and enter per-unit customizations for name/number decorations.
   → [`references/decoration_flow.md`](references/decoration_flow.md)
5. **Build the products (Preview).** `sales_preview_order` — turns decorated raw
   blanks into manufactured products with BOMs and routes. **Required before
   submit/confirm.** Confirm does NOT do this.
6. **Run the checklist.** `sales_run_preflight` — fix every blocking item.
   → [`references/pre_submission_checklist.md`](references/pre_submission_checklist.md)
7. **Submit or confirm.** `sales_submit_order` (internal review) or
   `sales_confirm_order` with `confirm=true` (goes live, launches procurement).

## Tool map

Run `python3 scripts/odoo_mcp.py tools` for the authoritative list. The entry
surface (names may evolve):

| Area | Tools |
| --- | --- |
| Customer prep & notes | `sales_search_customers`, `sales_get_customer`, `sales_add_customer_note` |
| Order lifecycle | `sales_create_order`, `sales_update_order`, `sales_add_lines`, `sales_remove_lines`, `sales_preview_order`, `sales_run_preflight`, `sales_submit_order`, `sales_confirm_order`, `sales_set_hold` |
| Grid | `sales_grid_read`, `sales_grid_add_column`, `sales_grid_apply`, `sales_grid_search_templates`, `sales_grid_load_variants`, `sales_grid_validate`, `sales_grid_read_costs`, `sales_grid_apply_costs`, `sales_grid_calculate_prices` |
| Decorations & requests | `sales_list_decoration_options`, `sales_search_decorations`, `sales_create_decoration`, `sales_link_decorations`, `sales_create_decoration_request`, `sales_get_decoration_request`, `sales_advance_decoration_request`, `sales_upload_customizations` |
| Field discovery | `sales_list_model_fields` (from `drivethru-odoo`) — lists **every** field on `sale.order`, `sale.order.line`, `decoration`, `decoration.request`, … |
| Reading the book | all the read-only `sales_*` query tools in `drivethru-odoo` (`sales_get_order`, `sales_search_orders`, `sales_order_manufacturing`, …) |
| Operator docs | `docs_get {"slug": "sales_order_entry"}` — the operator reference for this surface |

## Non-negotiables

- **Read the customer's internal notes before you enter an order.** They hold
  the "special actions for this customer" and there is no pop-up warning system
  on this Odoo — the notes are it. Honor the hard flags so confirm doesn't hard-
  refuse.
- **Preview before submit.** Any decorated line entered as a raw blank must go
  through `sales_preview_order` so its manufactured product, BOM and routes get
  built. Skipping it is the classic silent failure.
- **Run the checklist before you submit, every time.** It predicts every gate
  Odoo will enforce plus the softer things (notes reviewed, costs entered,
  proofs approved). This is the most important habit — and the checklist itself
  is the thing we tune as we test (see the reference; edit it there and in the
  MCP `sales_entry` service's `_evaluate_checklist`).
- **Confirm is live and hard to reverse.** `sales_confirm_order` is a dry run
  unless you pass `confirm=true`, and it refuses on blocking checklist failures
  unless `force_confirm=true`. State exactly what you're about to do and get the
  user's go-ahead before confirming. Prefer `sales_submit_order` when a human
  will do the final confirm.
- **Leave timestamped notes.** When you learn something about handling a
  customer (color preferences, PO rules, ship quirks), record it with
  `sales_add_customer_note` — it **appends a timestamped entry to the
  customer's Internal Notes** (`res.partner.comment`), the same field you read
  in step 1, so it lands where the next rep and your future self will see it.
  For general lessons about the order-entry process itself, append to
  [`references/lessons_learned.md`](references/lessons_learned.md).

## Working inside an Odoo Discuss conversation

You are often answering a person in an Odoo Discuss DM (see `drivethru-odoo` for
the `[Conversation context]` block and the person's `user_id`). Be concise and
conversational — summarize what the tools returned, don't dump JSON.
**Confirm before writes:** creating/editing orders, applying the grid, and
especially submitting/confirming change live Odoo data. Say what you're about to
do and get a go-ahead. When you need an SOP ("what's our policy on rush
orders?"), use the permission-scoped `knowledge_*` tools from `drivethru-odoo`.

## References

- [`references/customer_prep.md`](references/customer_prep.md) — reading the
  customer's internal notes & hard flags; leaving timestamped notes.
- [`references/order_entry_fields.md`](references/order_entry_fields.md) — the
  important `sale.order` / `sale.order.line` / `decoration.request` fields, and
  the model background (bacon_item vs vendor_item, end-item construction).
- [`references/grid_build_and_apply.md`](references/grid_build_and_apply.md) —
  how the grid works and how to build & apply changes (add_column and the raw
  payload), with the gotchas.
- [`references/decoration_flow.md`](references/decoration_flow.md) — decorations,
  requests, production-readiness, custom text.
- [`references/pre_submission_checklist.md`](references/pre_submission_checklist.md)
  — **the pre-submission checklist** (the part we tune together as we test).
- [`references/lessons_learned.md`](references/lessons_learned.md) — a
  timestamped log for things learned about the order-entry process.

## Errors

Same envelope as `drivethru-odoo`: `config_error` (exit 2, creds missing),
`invalid_arguments` (exit 2), `connection_error` (Odoo unreachable / key
rejected). A tool that ran but failed returns a normal result with
`isError: true` and a human-readable message — surface that. When Odoo refuses a
write (a `UserError`), the tool returns the Odoo message verbatim in its
`details.odoo_error`; relay it and fix the underlying issue.
