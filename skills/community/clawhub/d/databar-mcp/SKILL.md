---
name: databar
description: "Drive Databar MCP: leads, marketing intel, tables, flows."
version: 0.2.2
author: Dennis Rongo (dennisrongo), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Databar, MCP, Lead-Gen, Enrichment, Scraping]
---

# Databar (MCP) Skill

Run Databar data workflows through the `mcp__databar__*` MCP tools: discover and run enrichments and waterfalls, manage workspace tables, build reusable flows, and export results to CRMs. All paid operations bill in Databar credits (not dollars) — this skill prices before it spends.

## When to Use

- Contact enrichment and lead generation: find/verify emails, phone numbers, LinkedIn profiles, decision-makers at companies.
- Web data pulls: Google Maps, SERP, reviews, job postings, Amazon, YouTube search/comments.
- Company intelligence: tech stack, firmographics, hiring signals, funding/partnership news by domain.
- Marketing & SEO: competitor keywords (organic + PPC), transactional keywords by topic, LinkedIn ad library, brand social stats.
- Social & community intelligence: X/Twitter, TikTok, LinkedIn posts, Reddit, Telegram, Hacker News.
- Job search & recruiting: people search by title/company, hiring-company discovery, Sales Navigator exports.
- E-commerce & reputation: product details/pricing from any store, Google Shopping, Trustpilot/Capterra/app-store reviews.
- Investor & market intelligence: funding rounds and investors, public-company financials, earnings transcripts, real-time stock data.
- App-market intelligence: App Store/Google Play data, revenue estimates, review mining.
- Web traffic & domain intel: traffic estimates, SEO statistics, global rank, redirects, cheap firmographics by domain.
- Repeatable pipelines: tables with attached enrichment columns, scheduled sources, flows.
- Pushing results to HubSpot, Salesforce, Google Sheets, webhooks.

Don't use for: one-off page reads that `web_extract` already covers, or any bulk run where you haven't checked `price_credits` yet.

## Prerequisites

- Databar MCP server connected. Verify: `terminal(command="hermes mcp list")` shows `databar ... enabled`.
- Hosted endpoint: `https://mcp.databar.ai/mcp` (preferred — always current). API key from your Databar workspace → Integrations, sent as `Authorization: Bearer <key>`.
- Credits in the account. Check before spending: `mcp__databar__get_user_balance`.

## How to Run

Databar tools are loaded on demand. In Hermes: `tool_search(query="databar <topic>")` → `tool_describe(name="mcp__databar__<tool>")` → `tool_call`. Tool names are always `mcp__databar__<tool>`.

## The Databar Model (read once)

1. **Discover** → **run** → **poll** → **persist** (optional) → **export** (optional).
2. An **enrichment** is one provider. A **waterfall** tries multiple providers in sequence until one returns data — use waterfalls for email/person lookups where hit rate matters.
3. Every paid call has a `price_credits` cost (visible in `get_enrichment_details`), billed per record. Paginated enrichments bill per page.
4. Runs are async: `run_*` returns a task id, not data. `get_task_status` returns results once complete.
5. Tables: create → add rows → attach enrichment/waterfall/flow as result columns → run on all or empty rows.

## Quick Reference

| Stage | Tools |
|---|---|
| Account | `get_user_balance` |
| Discover enrichments | `search_enrichments`, `get_enrichment_details`, `get_param_choices` |
| Discover waterfalls | `search_waterfalls` |
| Run now | `run_enrichment`, `run_bulk_enrichment`, `run_waterfall`, `run_bulk_waterfall` |
| Poll results | `get_task_status` |
| Tables | `create_table`, `rename_table`, `delete_table`, `get_table_columns`, `rename_column`, `delete_column` |
| Rows | `create_rows`, `upsert_rows`, `patch_rows`, `delete_rows`, `get_table_rows` |
| Table enrichments | `add_table_enrichment`, `add_table_waterfall`, `get_table_enrichments`, `get_table_waterfalls`, `run_table_enrichment` |
| Flows | `list_flows`, `create_flow`, `get_flow`, `update_flow`, `run_flow`, `delete_flow`, `get_table_flows`, `add_table_flow` |
| Sources & export | `add_table_source`, `get_table_sources`, `sync_table_source`, `update_table_source_schedule`, `pause/resume_table_source`, `delete_table_source`, `search_exporters`, `get_exporter_details`, `add_table_exporter`, `get_table_exporters`, `run_table_exporter` |
| Folders | `list_folders`, `create_folder`, `rename_folder`, `delete_folder`, `move_table_to_folder` |

## Procedure — one-off enrichment

1. `get_user_balance` — record starting credits. ✓ balance noted.
2. `search_enrichments(query="...")` — shortlist by rank; note `id`, `price_credits`, `auth_method` per option.
3. `get_enrichment_details(enrichment_id=...)` — exact param slugs and response fields. If a param shows `choices.mode: "remote"`, resolve options with `get_param_choices`. ✓ params known before spending.
4. `run_enrichment(enrichment_id, params)` or `run_bulk_enrichment(enrichment_id, params_list)` for batches.
5. `get_task_status(task_id)` — wait ~3–5 s for singles, then poll every few seconds; waterfalls take longer.
6. Bulk results are position-aligned: `data[i]` answers `params_list[i]`, `null` means no data. ✓ `len(data) == len(params_list)`.

## Procedure — email/contact waterfall

1. `search_waterfalls(query="email finder")` — note `identifier`, `available_enrichments`, `input_params`.
2. `run_waterfall(waterfall_identifier="email_getter", params={...})` — optionally pass `email_verifier` (an enrichment id) to verify hits, or `provider_ids` to restrict providers.
3. Poll `get_task_status`; report hit rate. For batches use `run_bulk_waterfall` (same position-alignment rule).

## Procedure — table pipeline (repeatable)

1. `create_table(name, columns)` then `create_rows` (max 100/call; `options.allow_new_columns: true` auto-creates unknown columns).
2. `add_table_enrichment(table_uuid, enrichment_id, params)` — each param maps to `{"type": "mapping", "value": "<column name>"}` (read per-row) or `{"type": "simple", "value": "<static>"}`.
3. `run_table_enrichment(table_uuid, enrichment_id, run_strategy="run_empty")` — skips rows that already have results; `"run_all"` re-processes everything (billed again).
4. Read back with `get_table_rows` (filters: equals, contains, not_equals, is_empty, is_not_empty — AND-ed; max 500/page).
5. Export: `search_exporters` → `get_exporter_details` → `add_table_exporter` → `run_table_exporter`.

Recipes for common goals are in `references/` — `recipes.md` (sales/lead-gen core: lead lists, Maps, hiring signals, tech stacks, scheduled sources), `recipes-marketing-social.md` (SEO/PPC, ads, social listening, review mining, price watch, news), `recipes-people-research.md` (decision-makers, warm intros, job search, dossiers, research sourcing), and `recipes-finance-app.md` (funding intel, public-company teardowns, app-market intelligence, domain/traffic teardowns).

## Cost discipline

- Call `get_enrichment_details` before the first run of any enrichment — the same data can cost 1–15+ credits depending on provider. Price the whole chain, not one hop.
- Paginated enrichments bill per page — request only the pages you need.
- `run_strategy="run_empty"` instead of `"run_all"` on re-runs of table enrichments.
- Report the credit delta (`get_user_balance` before/after) with the delivered result.

## Pitfalls

- **Async ≠ done.** A task id from `run_*` is not a result. Always confirm via `get_task_status` before reporting data.
- **Positional joins.** Bulk results carry no keys — preserve your input order or join by index.
- **Destructive tools are permanent.** `delete_table`, `delete_rows`, `delete_column`, `delete_flow`, `delete_folder` have no undo. Never delete without explicit user instruction.
- `delete_flow` is refused while the flow is attached to a table column — remove the column first.
- `upsert_rows` key must be exactly one column; `create_rows`/`upsert_rows`/`patch_rows` cap at 100 rows per call.
- BYOK enrichments (`auth_method: "user_or_databar"`) may require your own provider API key if Databar-side auth fails.
- Results may come from cache; pass `skip_cache: true` when freshness matters (full price).
- The npm `databar-mcp-server` stdio package lags the hosted server — prefer the hosted URL unless your client requires stdio.

## Verification

- `get_user_balance` before/after shows the expected credit delta.
- `get_task_status` reports completed with data; for tables, `get_table_rows` shows result columns filled on the intended rows.
