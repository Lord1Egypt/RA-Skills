# Databar Recipes

Concrete recipes for common goals. Enrichment/waterfall IDs are **examples verified August 2026** — always re-verify with `search_enrichments` before running; the catalog changes and prices shift. Waterfall identifiers (`email_getter`, etc.) are stable.

## Recipe 1 — Lead list from a domain list

Goal: companies in, verified decision-maker emails out.

1. `create_table(name="...", columns=["domain", "company", "email", "first_name", "last_name", "title", "verified"])` → `create_rows` with domains (100/call).
2. `add_table_enrichment` — company data enrichment mapped `{"domain": {"type": "mapping", "value": "domain"}}`.
3. `search_waterfalls(query="email finder")` → `add_table_waterfall` (`email_getter`) mapped to name/company/domain columns.
4. `run_table_enrichment(..., run_strategy="run_empty")` → `get_table_rows` → export.

Cost shape: ~4–15 credits per fully enriched row depending on provider pricing and waterfall depth.

## Recipe 2 — Local business leads (Google Maps)

1. `search_enrichments(query="google maps businesses")` → pick by price/rank → `get_enrichment_details` for the exact `query`/`location` param slugs.
2. `run_enrichment` with location + keyword. Paginated: bill per page.
3. Feed business names + websites into the Recipe 1 email waterfall.

## Recipe 3 — Hiring-signal leads (companies hiring for a role)

1. `search_enrichments(query="search job postings")` → e.g. TheirStack job search or Pubrio postings-with-filters.
2. Run with role keywords (e.g. "data entry", "operations coordinator", "prompt engineer") — each posting is a company with budget attached to a workflow problem.
3. Extract company domains → Recipe 1 waterfall for contacts.

## Recipe 4 — Competitor / prospect tech stack

Goal: know who already runs Zapier/Make/n8n/Airtable/HubSpot.

1. `search_enrichments(query="tech stack")` → Bloomberry tech-vendors-by-domain (cheap) or BuiltWith categorized (deeper).
2. `run_bulk_enrichment` on a domain list, or attach to a table column.
3. Filter rows for the tools that qualify them for your pitch (e.g. automation consultancies target Zapier/n8n users).

## Recipe 5 — Scheduled table with webhook/CRM source

1. `add_table_source(table_uuid, source_type="webhook")` → capture the endpoint URL for your sender.
2. Or `source_type="crm"` with `dataset_id` + `schedule` (`{"cron_string": "0 12 * * *", "rows": 200, "overwrite": true}`) via `update_table_source_schedule`.
3. Attach result columns (Recipe 1 step 3) with `run_strategy="run_empty"`; rows sync in, enrichments fill, exporter pushes out.

## Recipe 6 — YouTube / SERP research pull

1. `search_enrichments(query="youtube search")` / `query="google serp"` → run with keyword.
2. Comments scrapers feed content-mining: audience questions, title patterns, video ideas with proven demand.

## Cross-cutting rules

- Price the full chain before running (see Cost discipline in SKILL.md).
- Bulk results are position-aligned — keep input order.
- Nothing is deleted without explicit instruction; `delete_*` tools are permanent.
