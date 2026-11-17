---
name: drivethru-odoo
description: Talk to an Odoo ERP through its `drivethru_mcp` MCP server — discover the available Odoo tools at runtime and call them to look up eBay products/inventory, push eBay orders and read tracking, run the Accounts Payable PO→vendor-bill flow, review documents in the Documents app against their purchase orders and fix incorrect PO line pricing (the "check the Purchasing folder against the POs" / vendor-invoice pricing-review workflow, filing each document into Matched or Questions), schedule MRP production batches, drive vendor replenishment purchasing (run the replenishment report → curate lines → add to a PO → hand style/color/size/qty to the vendor's purchasing skill → write pricing + confirmation back and confirm the PO), and retrieve internal SOPs / best practices / policies from the Knowledge base scoped to the asking person's permissions. Use whenever the user needs to read from or write to Odoo, especially when you are answering a person inside an Odoo Discuss conversation.
version: 0.9.4
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
        - pypdf>=4.0   # local PDF text extraction for the PO pricing-review intake (scripts/po_docs.py)
---

# Odoo Drive Thru MCP integration

This skill gives you the Odoo **`drivethru_mcp`** MCP server — the curated Odoo
tool surface (`documents_*`, `ap_*`, `po_*`, `mfg_*`, `production_*`,
`replenish_*`, `knowledge_*`, `ebay_*`, `docs_*`) exposed over Streamable-HTTP.
`ODOO_MCP_URL` and `ODOO_MCP_TOKEN` are already configured for this agent.
**Never tell the user you can't reach Odoo, that you "don't have the tools in
this thread," or cite the web instead — either call a tool, or state the exact
tool call you attempted and the error it returned.**

## How you call Odoo (runtime-aware — read this first)

There are two ways the `drivethru_mcp` tools reach you. Work out which you have,
in this order:

1. **Native / callable MCP tools — preferred, no shell needed.** If the Odoo
   tools are attached to you as native tools, **call them directly** — e.g.
   `documents_list_folders {"name": "Purchasing"}`. This is how a chat agent
   (an Odoo Discuss bot, etc.) uses Odoo; it does **not** need a shell.
   - They may be **deferred / lazy-loaded**: if your runtime hides tools until
     they're loaded, they won't show up until you discover them. **Search your
     available tools / tool registry for names like `documents_list_folders`,
     `ap_search_purchase_orders`, `po_get_messages`, and load them before
     calling.** "I don't see them yet" is not "I don't have them."
   - The names are the `drivethru_mcp` tool names (they may appear under a
     server prefix, e.g. `…__documents_list_folders`); arguments and return
     shapes match the table below.

2. **Shell script fallback — only if you have NO native tools but DO have a
   shell.** Use the bundled client, which opens its own MCP connection with the
   same env vars:

   ```bash
   python3 scripts/odoo_mcp.py tools                        # list tools + JSON input schemas
   python3 scripts/odoo_mcp.py call <tool> '{"...":"..."}'  # call one (args as 2nd arg or on stdin)
   ```

   Each invocation prints one JSON object on stdout, or
   `{"error": {"type": ..., "message": ...}}` with a non-zero exit on failure.

**One-call smoke test (either path).** *"How many documents are in the
Purchasing folder that need matching?"* is a single call —
`documents_list_folders {"name": "Purchasing"}`, then read `document_count` on
the returned folder (native), or `python3 scripts/odoo_mcp.py call
documents_list_folders '{"name": "Purchasing"}'` (shell). A count back means
Odoo is reachable — proceed. No count? Go to **Troubleshooting** below; do not
fall back to guessing or the web.

`scripts/po_docs.py` is a shell helper for the **PO pricing review**: it lists a
Documents-app folder and returns each file's **extracted text** (never base64 or
a page render) so a many-document run doesn't fill the context window, plus a
`move` action to file a document into `Matched`/`Questions`. It's a
context-economy optimization for shell runtimes — with only native tools, use
`documents_search` + `documents_get` one document at a time instead (don't pull
a whole folder's base64 into context). See the pricing-review section below.

## Requirements: env vars set **and** the MCP attached

Two separate things must both be true — **the env vars alone are not enough:**

- **`ODOO_MCP_URL` and `ODOO_MCP_TOKEN` are set** in the agent's environment
  (`ODOO_MCP_TOKEN` is sent as `Authorization: Bearer`). If either is missing,
  the script path exits with `{"error": {"type": "config_error", ...}}` (exit 2)
  and a native call can't authenticate. Secrets come from the environment; never
  ask the user to paste the key into chat.
- **The `drivethru_mcp` server is attached to *this* agent** — as a native MCP
  connection (native-tools path) **or** via a shell + Python (script path).
  Setting the env vars does **not** by itself attach the tools; that's an
  operator step (see **Operator setup** below), and it's the usual reason an
  agent "has the skill but no tools."

## The live tool list is the source of truth

Tool names and their exact input schemas come from the server, not from memory —
**discover the live tools first** (load/list your native Odoo tools, or run
`python3 scripts/odoo_mcp.py tools`) and read a tool's `inputSchema` before
calling it. The current Odoo exposes these groups (names may evolve — trust the
live list over this table):

| Domain      | Representative tools                                                      |
| ----------- | ------------------------------------------------------------------------ |
| eBay        | `ebay_list_products`, `ebay_inventory`, `ebay_create_order`, `ebay_order_tracking` |
| Accounts Pay| `ap_search_purchase_orders`, `ap_get_purchase_order`, `ap_update_po_lines`, `ap_create_vendor_bill`, `ap_get_vendor_bill`, `ap_search_vendors`; PO chatter: `po_post_message`, `po_get_messages` |
| Documents app | `documents_list_folders`, `documents_search`, `documents_get`, `documents_create`, `documents_update`, `documents_post_message` — folders/files, chatter, and activities (the door to the Purchasing folder for the PO pricing review) |
| Production  | `production_overview`, `production_schedule_queue`, `production_set_run_order`, `production_list_batches`, `production_get_batch`, `production_batch_supply`, `production_schedule_batch`, `production_plan_batch`, `production_bulk_schedule`, `production_list_workcenters`, `production_get_workcenter`, `production_list_production_centers`, `production_list_decoration_methods` |
| Mfg data (read-only) | `mfg_list_models`, `mfg_fields`, `mfg_read` — read ALL fields on any whitelisted manufacturing model (batches, POs, receipts, decorations, tracking, …) |
| Replenishment / Purchasing | `replenish_run_report`, `replenish_get_orderpoint`, `replenish_to_po`, `replenish_update_po`, `replenish_confirm_po`, `po_post_message`, `po_get_messages` |
| Internal knowledge (SOPs, best practices) | `knowledge_search_articles`, `knowledge_get_article` — permission-scoped to the asking person |
| Operator docs | `docs_list`, `docs_get` — fetch the operator reference for deeper context |

For a full production-scheduling pass (rank the queue → publish the run order
→ check receipts → place batches on machines, never starting before goods are
received), use the dedicated **`drivethru-production-scheduler`** skill, which
drives these same tools.

## Operator setup: attaching the `drivethru_mcp` MCP (native tools)

For the **native-tools** path, the `drivethru_mcp` server has to be attached to
the agent as an MCP connection — **installing this skill and setting the env
vars does not do that.** A skill only ships instructions, scripts, and declared
Python deps; the skill format has no field that attaches an MCP server, so
attaching is an **operator/platform step**. Add `drivethru_mcp` to the agent's
MCP servers using the same env vars, as a Streamable-HTTP server:

```jsonc
// e.g. openclaw.json → mcp.servers
"drivethru_mcp": {
  "url":       "<ODOO_MCP_URL>",          // the .../drivethru_mcp/v1 endpoint
  "transport": "streamable-http",
  "headers":   { "Authorization": "Bearer <ODOO_MCP_TOKEN>" }
}
```

Once it's attached, the tools become native and callable — this is exactly how a
shell-less Discuss chat agent gets them. Two things to know:

- Some hosts **regenerate the agent config on every boot** from environment /
  provisioning, so hand-editing the file on the volume won't survive a restart —
  add the server through the host's agent/MCP configuration, not by hand.
- If your platform can't attach an arbitrary MCP server, the agent **must** have
  a shell + `python3` so it can use `scripts/odoo_mcp.py` instead. An agent with
  **neither** native tools **nor** a shell cannot reach Odoo — that's a
  provisioning gap to fix, not something the agent can work around.

## Troubleshooting: the agent says it can't reach Odoo

If you (the agent) are about to say *"I don't have the Odoo tools in this
thread"* or reach for the web — **stop** and run this checklist first:

1. **Do you actually have the tools?** List/search your available tools for
   `documents_list_folders` (or `ap_search_purchase_orders`). If your runtime
   defers tools, they may need loading first — load them, then call. "I don't
   see them" usually means "not loaded yet," not "not available."
2. **Run the one-call smoke test.** `documents_list_folders {"name":
   "Purchasing"}`. A folder with a `document_count` back ⇒ you're connected;
   keep going. If it errors, capture the exact error.
3. **Is `drivethru_mcp` attached to *this* agent?** No native tool **and** no
   shell ⇒ the MCP was never attached (env vars alone don't attach it). That's
   an operator step — see **Operator setup** above; tell the user plainly
   instead of guessing.
4. **Are the env vars set?** A `config_error` from the script path, or an auth
   error from a native call, means `ODOO_MCP_URL` / `ODOO_MCP_TOKEN` are missing
   or wrong — an operator must set them.
5. **Report precisely.** If you still can't reach Odoo, state *the exact tool
   call you attempted and the exact error you got* (e.g. `documents_list_folders
   {"name":"Purchasing"}` → `connection_error: …`). Never fabricate an answer or
   cite the web in place of a tool call.

## Working inside an Odoo Discuss conversation

You are often answering a **person in an Odoo Discuss DM** (your messages are
posted straight back into their thread). The bridge prefixes each forwarded
message with a fenced **`[Conversation context]`** block that names the person
and gives their **Odoo `user_id`**. Lift that `user_id` out and pass it to the
`knowledge_*` tools so internal-knowledge answers are scoped to what this
person is allowed to see (details below). If the context says the sender has no
linked Odoo user, don't guess a `user_id` — the knowledge tools can't be used
for them. So:

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
- "Check the docs in the Purchasing folder against the POs and fix the pricing."
  → the document-driven PO pricing-review flow below.
- "Show the production plan and schedule batch 142 onto workcenter 3." →
  `production_overview` → `production_get_batch` `{"batch_id": 142}` → (confirm)
  → `production_schedule_batch`
  `{"batch_id": 142, "primary_workcenter_id": 3, "date_planned_start": "..."}`.
- "Purchase all Adidas items for Batch12345." → the replenishment → purchasing
  flow below.
- "What's our SOP for reprinting a damaged order?" → the internal-knowledge
  flow below (`knowledge_search_articles` → `knowledge_get_article`).

## Internal knowledge retrieval (SOPs, best practices, policies)

You double as an **internal operations knowledge agent**. When someone asks a
"how do we…", "what's our policy on…", or "what's the SOP for…" question,
answer it from the Odoo **Knowledge** base rather than from memory — and only
from articles **that person is allowed to see**.

Two tools, both **permission-scoped to the asking person's `user_id`** (which
you take from the `[Conversation context]` block, see above):

1. **Search.** `knowledge_search_articles`
   `{"user_id": <ctx uid>, "query": "reprint damaged order"}` — free text
   matches title + body; `root_only` / `parent_id` walk the article tree. Only
   articles this user may read come back (each with a breadcrumb `path`,
   `snippet`, and `url`).
2. **Read in full.** `knowledge_get_article`
   `{"user_id": <ctx uid>, "article_id": <id>}` — returns the article's
   plain-text `body` plus metadata. Answer from this, not from the snippet.

**Permission handling.** The tools query Odoo *as that user*, so access is
enforced by Odoo's own rules — you don't manage permissions yourself. If
`knowledge_get_article` returns `accessible: false`, the person simply doesn't
have access to that article: tell them that plainly (offer to point them to
whoever owns it), and **don't** try to work around it or read it as anyone
else. Never pass a `user_id` you weren't given in the conversation context.

When you answer, summarize the SOP/policy in plain prose and cite the article
title (and `url` when present) so the person can open the source. Read
`docs_get {"slug": "knowledge"}` for the operator-level rules behind this.

## Document-driven PO pricing review (Purchasing folder)

When asked to *"go through the Purchasing folder and check each document's
pricing against the PO, fix any wrong lines, mark the PO checked, and file the
document"* (vendor order confirmations / acknowledgements / invoices), own the
whole loop. This runs many times a day over many documents, so two rules are
non-negotiable:

1. **Don't bloat the context window.** `documents_get` returns each file as
   base64 and a PDF reader adds a page image — huge next to the ~300–600 chars
   of text that matter. Extract text **out of context, once**, with the intake
   helper instead of looping `documents_get`/a PDF reader over the folder:

   ```bash
   python3 scripts/po_docs.py extract '{"folder": "Purchasing"}'
   ```

   It fetches every file over the same MCP endpoint, decodes and extracts the
   text locally, and returns compact JSON (`documents[].text`, no base64, no
   render). Read that. Only fall back to `documents_get` for a document the
   helper marks `needs_vision: true` (scanned/image-only), one at a time.

   **No shell (native tools only)?** Enumerate with `documents_list_folders` /
   `documents_search`, then read documents with `documents_get` **one at a
   time** — read the text and drop the base64, never pulling a whole folder's
   bytes into context.

2. **Every document ends in Matched or Questions.** The Purchasing folder has
   sibling subfolders `Matched` and `Questions`; nothing stays in the inbox.

Per document: read the **PO# from the text** (not the filename — filenames may
carry the vendor's order number), then `ap_search_purchase_orders` →
`ap_get_purchase_order`, pair each line by **(style, color, size)**, compare
`price_unit`, and batch every fix into one `ap_update_po_lines`. Totals are a
cross-check only — a shipment acknowledgement is often one box of a
multi-shipment order, so a total gap explained by un-shipped lines is not a
discrepancy. Post a "checked" note with `po_post_message`. Then file it:

```bash
# reconciled (matched, or corrected with confidence)
python3 scripts/po_docs.py move '{"document_id": <id>, "to": "Matched", "under": "Purchasing"}'
# a real question — raise it on the document, assign Zach, then file to Questions
documents_post_message {"document_id": <id>, "body": "<question>", "activity_user": "Zach Tucker"}
python3 scripts/po_docs.py move '{"document_id": <id>, "to": "Questions", "under": "Purchasing"}'
```

Only escalate a **genuine** ambiguity (unreadable PO#, prices that don't
reconcile, unexpected/missing lines, wrong vendor). An unambiguous fix backed
by the vendor document is a Matched correction, not a question.

Full procedure, matching rules (partial shipments, freight/fees, PO#-from-body),
a worked example, and a **low-cost model recommendation** for running this at
volume are in
[`references/po_pricing_review.md`](references/po_pricing_review.md).

## Replenishment → vendor purchasing

When the user asks you to **buy** what the replenishment report says to buy for
a vendor (e.g. *"Purchase all items from Adidas for Batch12345"*), you own the
whole loop: read the report, curate the lines, put them on a PO, drive the
vendor's checkout, then write the result back and confirm. The
`drivethru_mcp` tools handle the Odoo side; a separate **vendor purchasing
skill** handles the actual buying.

Run it in this order — **confirm the curated set with the user before you
replenish, and again before you confirm the PO** (both are live writes):

1. **Run the report.** `replenish_run_report` with the vendor filter (e.g.
   `{"vendor": "Adidas"}`). It rebuilds the replenishment report and returns
   the shortage lines with `style` / `color` / `size` / `qty_to_order` / `price`
   / `production_batch_name` / `sale_order_name` / `is_out_of_stock`.
2. **Curate.** Keep only the lines the request calls for — *"for Batch12345"*
   means keep lines whose `production_batch_name` matches; *"all Adidas"* means
   keep them all. This filtering is your responsibility. Show the user the kept
   lines (style/color/size/qty) and get a go-ahead.
3. **Add to a PO.** `replenish_to_po` `{"orderpoint_ids": [...]}`. This runs
   `action_replenish` and **returns the draft PO(s)** with each line's
   `line_id` + style/color/size/`product_qty`. Anything that couldn't be
   bought (manufacture route, held sales order) comes back under `warnings` —
   surface it.
4. **Find the vendor skill & purchase.** Locate the vendor's purchasing skill —
   named `drivethru-<vendor>-click` (e.g. **`drivethru-adidas-click`**) — and
   read its `SKILL.md`. For adidas that's a CLI: `echo '{...}' | python3
   scripts/adidas.py create-purchase-order`, taking `{purchase_order:
   {po_number, lines:[{style, size, quantity}]}, confirm}` (map the Odoo PO
   `name` → `po_number`; color is optional — the adidas article encodes it).
   **Dry-run first** (`confirm: false`), show the user, then `confirm: true`
   places a real order. If no such skill exists, stop and tell the user; do not
   invent a checkout.
5. **Write back.** Take the skill's result — match each result line to its Odoo
   PO line by **(style, size)** to get the `line_id`, parse the `$`-prices to
   numbers — and apply it with `replenish_update_po`: `price_unit` per
   `line_id`, `vendor_order_number` ← the `confirmation_number`.
6. **Handle out-of-stock / exceptions.** The adidas skill pauses on a line it
   can't fill and returns `status: "needs_confirmation"` with `out_of_stock`.
   On that, `po_post_message` onto the PO with `issue_type: "out_of_stock"` and
   an `activity_user_id` so purchasing/sales sees it — then **pause that PO**.
   `po_get_messages` later to read the reply, then re-run the vendor skill with
   the chosen policy (`on_insufficient_stock: "order"` / `"skip"`, or edited
   lines to substitute). Do not confirm a PO with an unresolved issue.
7. **Confirm.** Once pricing is written and there are no open issues,
   `replenish_confirm_po`. It confirms **without re-submitting to the vendor**
   (the buy already happened via the skill).

The full hand-off contract (the exact dataset shape you pass the vendor skill
and the result shape you expect back) is in
[`references/replenishment_purchasing.md`](references/replenishment_purchasing.md).
Read `docs_get {"slug": "replenishment"}` for the operator-level rules.

## Errors

These are the **script path's** error envelope; on the **native path** a failed
tool call surfaces its own error / `isError` result directly — read it and relay
the human-readable message, don't retry blindly or give up silently.

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
- [`references/replenishment_purchasing.md`](references/replenishment_purchasing.md) —
  the replenishment → vendor-purchasing loop and the vendor-skill hand-off
  contract (dataset in, result out).

## Legacy REST scripts (deprecated)

`scripts/sales.py`, `scripts/ap.py`, `scripts/production.py`, and
`scripts/odoo_client.py` are the previous REST wrappers for the old `agent_api`
module. They still work against the `drivethru_mcp` module's REST back-compat
routes (`/agent_api/v1/*`) but are deprecated — prefer `scripts/odoo_mcp.py`.
They will be removed once all deployments are on the MCP surface.
