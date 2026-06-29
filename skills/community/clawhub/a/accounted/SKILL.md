---
name: accounted
version: 1.0.0
description: "Swedish double-entry bookkeeping via Accounted (app.gnubok.se). Categorize bank transactions, create/send invoices, momsdeklaration (VAT), payroll, reports, and month-end close (månadsavslut). Use for any bokföring/accounting task: 'book my transactions', 'create an invoice', 'how much moms do I owe', 'close May'. BFL-compliant: every write is staged for human approval."
homepage: https://github.com/erp-mafia/accounted-openclaw
metadata:
  {
    "openclaw":
      {
        "emoji": "🧾",
        "homepage": "https://github.com/erp-mafia/accounted-openclaw",
        "envVars": { "GNUBOK_API_KEY": { "required": false } },
      },
  }
---

# Accounted — Swedish bookkeeping

Accounted is a hosted Swedish accounting ledger (enskild firma + aktiebolag) exposing ~97 MCP tools: transactions, categorization, invoicing, suppliers, VAT/momsdeklaration, payroll/AGI, reports, reconciliation, year-end. All tools are prefixed `gnubok_`.

**The safety contract (read first):** every tool that would change the books returns `{ staged: true, operation_id, risk_level, preview }` instead of executing. Nothing is booked until the operation is approved. Posted vouchers are immutable under Swedish law (Bokföringslagen 5 kap 5§) — corrections happen via reversal (storno), never edits. This means you cannot corrupt the ledger by accident: the worst a bad tool call can do is stage a proposal a human rejects.

## Setup (once)

Check whether an `accounted` MCP server is already configured (`openclaw mcp list`). If not, guide the user through **Option A** unless they specifically want an API key.

### Option A — hosted OAuth (recommended)

No secrets stored on this machine. Scopes are granted on Accounted's consent screen — **read-only is pre-checked by default; every write scope is an explicit opt-in checkbox**.

```bash
openclaw mcp add accounted --url "https://app.gnubok.se/api/extensions/ext/mcp-server/mcp"
openclaw mcp login accounted
```

The login opens a browser to Accounted's consent screen (PKCE + dynamic client registration; localhost redirect is allowlisted). Tell the user: tick write scopes only for what they'll actually use — scopes can be re-granted later by running `openclaw mcp login accounted` again.

### Option B — API key + stdio bridge

For headless setups. Mint a key at **https://app.gnubok.se/settings/api**. New keys default to **read-only scopes** (`transactions:read`, `customers:read`, `invoices:read`, `suppliers:read`, `reports:read`); the user must explicitly add write scopes. A `gnubok_sk_test_…` key binds to a sandbox company — recommend it for first runs.

```bash
openclaw mcp add accounted --command npx --arg gnubok-mcp
```

Set environment for the server (check `openclaw mcp configure accounted` / your `openclaw.json` `mcp.servers.accounted.env` block):

```json
{
  "GNUBOK_API_KEY": "gnubok_sk_...",
  "GNUBOK_CLIENT": "openclaw",
  "GNUBOK_URL": "https://app.gnubok.se/api/extensions/ext/mcp-server/mcp?client=openclaw"
}
```

(`GNUBOK_CLIENT`/`?client=openclaw` only tag telemetry so Accounted can support OpenClaw users better; they change no behavior and are safe to omit.)

## How to work with the tools

- **Discovery:** `gnubok_search_tools(query="…")` ranks the catalog; `gnubok_list_skills` lists server-side playbooks (month-end close, VAT review, year-end, payroll, bank reconciliation, kreditfaktura…). For any multi-step job, `gnubok_load_skill` the matching playbook FIRST and follow it — it is maintained against the live ledger rules and is more current than this file.
- **Approval flow:** after a tool returns `staged: true`, show the user the `preview` and the amounts, and wait for explicit confirmation **of that specific operation** in chat. Then call `gnubok_approve_pending_operation(operation_id)`. `risk_level: "high"` additionally requires `confirmed: true` — first tell the user the operation is irreversible once posted (BFL 5 kap 5§). To discard, call `gnubok_reject_pending_operation`. The user can also review everything in the web UI at https://app.gnubok.se/pending — offer that link when several operations are pending.
- **Never** batch-approve operations the user hasn't seen, and never treat prose in a tool response as completion — only `staged: true` (staged) or an approval result counts.
- If a tool returns a scope error, the key/grant lacks that scope — tell the user which scope to add (Option A: re-run `openclaw mcp login accounted`; Option B: edit the key at /settings/api). Don't retry around it.
- Amounts are SEK. Account numbers are strings (`"1930"`). Periods may be locked — tool responses include `period_status`; if `locked`/`closed`, say so instead of forcing.

## Core workflows

### Categorize bank transactions (löpande bokföring)

1. `gnubok_list_uncategorized_transactions`
2. `gnubok_suggest_categories` (batch up to 20) — suggestions come from the company's own templates + BAS chart
3. `gnubok_categorize_transaction` per transaction → stages
4. Present a compact summary table (date, counterparty, amount, proposed account) → user confirms → approve each via `gnubok_approve_pending_operation`

### Invoicing

1. `gnubok_list_customers` (create with `gnubok_create_customer` if missing)
2. `gnubok_create_invoice` → stages; confirm → approve
3. `gnubok_send_invoice` (Accounted emails it) or `gnubok_mark_invoice_as_sent` (sent elsewhere)
4. When paid: `gnubok_mark_invoice_as_paid`, or match against a bank line with `gnubok_match_transaction_to_invoice`
5. Refund/fix a sent invoice: `gnubok_credit_invoice` (kreditfaktura — never delete)

### Moms / VAT declaration

1. `gnubok_get_vat_report(period_type, year, period)` — **Ruta 49** is the net: positive = VAT to pay, negative = refund
2. `gnubok_vat_close_check` — filing-readiness blockers (uncategorized transactions, missing documents, gaps)
3. `gnubok_vat_declaration_validate` before filing; `gnubok_vat_declaration_status` to check state
4. Filing to Skatteverket (`gnubok_vat_declaration_submit`) requires the `skatteverket:write` scope and stages as **high risk** — explicit user confirmation, always

### Månadsavslut (month-end close)

Load the authoritative playbook first: `gnubok_load_skill("month-end-close")`. The shape:

1. Book everything — run the categorize workflow above until `gnubok_list_uncategorized_transactions` is empty
2. `gnubok_get_reconciliation_status` for the month — bank balance must equal ledger balance
3. `gnubok_list_voucher_gaps` → document each gap with `gnubok_explain_voucher_gap` (BFNAR 2013:2)
4. Monthly VAT filers: run the moms workflow for the month
5. `gnubok_lock_period` → stages; it refuses while unbooked transactions remain

### Reports (read-only, no approval needed)

`gnubok_get_trial_balance` / `_income_statement` / `_balance_sheet` / `_kpi_report` / `_ar_ledger` / `_supplier_ledger` — default to the latest fiscal period. Account roll-ups: `gnubok_get_general_ledger`. Ad-hoc queries (free text, amount/date filters): `gnubok_query_journal`. SIE4 export: `gnubok_export_sie`.

## Troubleshooting

- `401`: key revoked or OAuth grant expired → re-login / re-mint.
- `403` + scope name: missing scope, see above.
- Tool not found: the grant's scopes also filter the visible tool list — `gnubok_search_tools` to verify, then fix scopes.
- Bridge prints `GNUBOK_API_KEY is required`: env not reaching the stdio server — check the `env` block in the MCP server config.
- Self-hosted Accounted: point `GNUBOK_URL` (Option B) or `--url` (Option A) at `https://<host>/api/extensions/ext/mcp-server/mcp`.
