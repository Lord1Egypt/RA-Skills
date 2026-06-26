---
name: drivethru-odoo
description: Talk to an Odoo ERP through its `drivethru_mcp` MCP server — discover the available Odoo tools at runtime and call them to look up eBay products/inventory, push eBay orders and read tracking, run the Accounts Payable PO→vendor-bill flow, and schedule MRP production batches. Use whenever the user needs to read from or write to Odoo, especially when you are answering a person inside an Odoo Discuss conversation.
version: 0.2.0
emoji: 🏭
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
          `https://odoo.example.com/drivethru_mcp/v1` (note the path — this is
          the MCP server exposed by the `drivethru_mcp` Odoo module, not the
          Odoo base URL).
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

# Odoo Drive Thru MCP integration

This skill connects to the Odoo **`drivethru_mcp`** module's **MCP server**
(`POST $ODOO_MCP_URL`, a Streamable-HTTP MCP endpoint) and lets you use its
tools on the user's behalf. Unlike a static API wrapper, the tool surface is
**discovered at runtime** — call `tools` to see exactly what this Odoo exposes.

The single helper script is `scripts/odoo_mcp.py`:

```bash
# Discover the available tools (name + description + JSON input schema)
python3 scripts/odoo_mcp.py tools

# Call a tool — arguments are a JSON object as the 2nd arg or on stdin
python3 scripts/odoo_mcp.py call <tool_name> '{"...": "..."}'
echo '{"...": "..."}' | python3 scripts/odoo_mcp.py call <tool_name>
```

Every invocation prints one JSON object on stdout, or
`{"error": {"type": ..., "message": ...}}` with a non-zero exit on failure.

## Required credentials

`ODOO_MCP_URL` and `ODOO_MCP_TOKEN` must be in the environment. If either is
missing the script exits with `{"error": {"type": "config_error", ...}}` (exit
2) — stop and tell the user to configure them. Secrets come from the
environment; never ask the user to paste the key into chat.

## Always start with `tools`

The MCP server's `tools/list` is the source of truth for tool names and their
exact input schemas — **run `python3 scripts/odoo_mcp.py tools` first** and read
the `inputSchema` for any tool before calling it. The current Odoo exposes these
tool groups (names may evolve — trust `tools` over this list):

| Domain      | Representative tools                                                      |
| ----------- | ------------------------------------------------------------------------ |
| eBay        | `ebay_list_products`, `ebay_inventory`, `ebay_create_order`, `ebay_order_tracking` |
| Accounts Pay| `ap_search_purchase_orders`, `ap_get_purchase_order`, `ap_update_po_lines`, `ap_create_vendor_bill`, `ap_get_vendor_bill`, `ap_search_vendors` |
| Production  | `production_overview`, `production_list_batches`, `production_get_batch`, `production_schedule_batch`, `production_plan_batch`, `production_bulk_schedule`, `production_list_workcenters`, `production_get_workcenter`, `production_list_production_centers`, `production_list_decoration_methods` |
| Operator docs | `docs_list`, `docs_get` — fetch the operator reference for deeper context |

## Working inside an Odoo Discuss conversation

You are often answering a **person in an Odoo Discuss DM** (your messages are
posted straight back into their thread). So:

- **Be concise and conversational.** Reply in plain prose, not raw JSON dumps —
  summarize what the tools returned. Surface a tool error's human-readable
  message rather than the raw envelope.
- **Ask for missing information** instead of guessing identifiers. If you need a
  PO, batch, or order id, look it up with a search/list tool first.
- **Confirm before writes.** Creating orders/bills, updating prices, and
  scheduling/planning batches change live Odoo data. State exactly what you're
  about to do and get the user's go-ahead before calling a write tool.
- Use `docs_list` / `docs_get` when you need the operator-level rules behind a
  workflow (e.g. how vendor-bill matching or batch scheduling is meant to work).

## Typical flows

- "What eBay inventory do we have for A-1, B-2?" → `ebay_inventory`
  `{"skus": ["A-1", "B-2"]}`.
- "Find the PO for vendor X and bill it." → `ap_search_purchase_orders` →
  `ap_get_purchase_order` → (confirm) → `ap_create_vendor_bill`.
- "Show the production plan and schedule batch 142 onto workcenter 3." →
  `production_overview` → `production_get_batch` `{"batch_id": 142}` → (confirm)
  → `production_schedule_batch`
  `{"batch_id": 142, "primary_workcenter_id": 3, "date_planned_start": "..."}`.

## Errors

- `config_error` (exit 2) — `ODOO_MCP_URL` / `ODOO_MCP_TOKEN` missing.
- `invalid_arguments` (exit 2) — bad CLI usage or non-JSON arguments.
- `connection_error` — Odoo unreachable, transport error, or the key was
  rejected (the MCP server requires a valid key even to list tools).
- A tool that ran but failed returns a normal MCP result with `isError: true`
  and a human-readable message in its content — surface that to the user.

## References

- [`references/agent_api_endpoints.md`](references/agent_api_endpoints.md) — the
  underlying Odoo operations (now exposed as MCP tools); `tools/list` is
  authoritative for the live schema.
- [`references/production_scheduling.md`](references/production_scheduling.md) —
  the MRP data model behind the production tools.

## Legacy REST scripts (deprecated)

`scripts/sales.py`, `scripts/ap.py`, `scripts/production.py`, and
`scripts/odoo_client.py` are the previous REST wrappers for the old `agent_api`
module. They still work against the `drivethru_mcp` module's REST back-compat
routes (`/agent_api/v1/*`) but are deprecated — prefer `scripts/odoo_mcp.py`.
They will be removed once all deployments are on the MCP surface.
