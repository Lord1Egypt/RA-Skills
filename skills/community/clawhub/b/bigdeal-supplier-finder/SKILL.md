---
name: bigdeal-supplier-finder
description: Use when an agent needs to create an evidence-bound supplier discovery report for a product or sourcing brief, especially for global buyers, cross-border ecommerce, private label, OEM/ODM, manufacturer discovery, B2B platform search, trade show directory search, supplier directory research, query expansion, source map generation, or structured sourcing reports. Produces source maps, supplier candidates, evidence links, gaps, and next-search suggestions. Does not log in, bypass captcha, use paid APIs, scrape at scale, store databases, score supplier trustworthiness, recommend purchases, or perform live/external actions without explicit separate authorization.
license: MIT-0
compatibility: "Requires runtime with web search and fetch capabilities for live reports. Operates in planning-only (no-search) mode without search. Does not assume paid APIs, auth, captcha solving, or JavaScript rendering."
metadata:
  repository: https://github.com/its-How/bigdeal-supplier-finder
  version: "1.0.0"
---

# BigDeal Supplier Finder

Use this skill to help an agent discover where to search for suppliers and produce a structured, evidence-bound sourcing report. The skill is breadth-first: expand source surfaces, preserve raw signals, separate evidence from query fuel, and make uncertainty explicit.

This is a runtime-agnostic agent skill. It is not a crawler, not a supplier database, not a procurement recommendation engine, and not a trust or due-diligence score.

## Find-Stage Scope

Do:

- generate diverse search/query plans across B2B platforms, trade shows, associations, government or industry directories, company websites, supplier directories, and public media/community sources;
- record `SearchResultSignal`, `SourceAttempt`, `SourceMapEntry`, `SupplierCandidate`, `QuerySuggestion`, and `Gap` separately;
- Every Supplier Candidate must include at least one evidence link that: (a) is a valid HTTP/HTTPS URL, (b) is not a search engine results page or site-search page, (c) is not a known paywall/login-wall/captcha page, (d) points to a page that contains the supplier information claimed in the candidate fields. Evidence links that fail these criteria must be removed; if no valid evidence link remains, the candidate must not enter Supplier Candidates.
- grade evidence strength only as A/B/C/D;
- mark low-evidence and missing-evidence cases instead of hiding them.

Do not:

- log in, handle cookies, read sessions, solve captcha, bypass access controls, use paid APIs, or access credentialed sources;
- run recursive crawling, bulk scraping, database storage, contact enrichment, or background monitoring;
- label suppliers as trustworthy, safe, recommended, best, verified, compliant, or purchase-ready;
- count search pages, query-only snippets, AI answers without public URLs, failed fetches, restricted pages, paywalls, login walls, captcha pages, or D-grade raw signals as actionable leads.

## Inputs

Ask for or infer:

- product name and product category;
- sourcing intent, such as OEM, ODM, wholesale, private label, component sourcing, or market exploration;
- target markets and preferred supplier regions;
- known exclusions or risky sources;
- available runtime capability: `search+fetch`, `search-only`, or `no-search`;
- whether live web/provider/browser/credential actions are explicitly authorized.

If live or credentialed actions are not explicitly authorized, operate in planning mode only.

### Day 1 Answer

Start with a Day 1 Answer:

```text
If I did no research, I would expect the strongest suppliers to come from ______ because ______.
The actual outcome is ______.
This should be searched now because ______.
Adjacent sourcing capabilities that are out of scope are ______.
```

## Runtime Capability Assumptions

This skill assumes the agent runtime has access to:
1. **Web search** — returning result titles, snippets, and target URLs.
2. **Web fetch** — retrieving page content from public HTTP/HTTPS URLs.

If search is unavailable, operate in `no-search` mode (fail-fast with metadata only).
If fetch is unavailable, operate in `search-only` mode (C-grade candidates only).

This skill does NOT assume: paid API access, authenticated sessions, CAPTCHA solving, JavaScript rendering, or database storage.

## Live Run

When the agent runtime has search and/or fetch capability, execute the
five-round workflow below to produce an evidence-bound supplier discovery
report. The agent runs everything itself; no external script, adapter, or
registry orchestrates the run.

### Tool Discovery

Before starting, the agent must check which tools are available in its
current runtime:

1. **Search tool**: Can the agent query a search engine and receive result
   titles, snippets, and target URLs?
2. **Fetch tool**: Can the agent retrieve page content from a public
   HTTP/HTTPS URL?

Do not assume specific tool names. Each runtime exposes different interfaces.
If neither search nor fetch is available, operate in `no-search` mode (see
Runtime Capability Assumptions).

### Execution Flow

**Phase 1: Query Planning**

Generate at least 6 deduplicated query combinations across target regions,
product terms, and sourcing intents. Each query targets a specific source
category (B2B platforms, trade shows, associations, government directories,
company websites, media/community).

**Phase 2: Search**

Execute each query using the runtime's search tool. Record every result as a
`SearchResultSignal` (query fuel, not evidence). Track:
- `query_id`, `engine_or_entry`, `title`, `snippet`, `result_url`, `rank`
- `is_search_page_url` (true for SERP / site-search results)
- `admissibility` (for SERP entries: `inadmissible`)

**Phase 3: Fetch and Extract**

For each promising target URL from search results:
1. Fetch the page using the runtime's fetch tool.
2. Record a `SourceAttempt` with status and reason.
3. If the fetch fails, record the failure and add a `Gap`. Do not create
   a SourceMapEntry or SupplierCandidate.
4. If the fetch succeeds, classify the page:
   - **Discovery surface** (lists/aggregates multiple suppliers): create a
     `SourceMapEntry`.
   - **Single-supplier page**: create a `SupplierCandidate`.
5. Validate every candidate has at least one admissible evidence link
   (see Evidence Admissibility below).

**Phase 4: Expansion**

Run one base expansion pass if Supplier Candidates are fewer than 8 or
source categories are fewer than 3. Generate targeted queries for uncovered
regions or source types. Deduplicate actionable leads by canonical URL +
normalized name.

**Phase 5: Assemble Report**

Assemble all required report fields:
- `execution_metadata` (profile, runtime capabilities, started_at,
  finished_at, elapsed_seconds, rounds_completed, stage_records, stop_reason,
  limits_hit, all counters)
- `execution_limit_audit`
- `summary`
- `source_map`
- `supplier_candidates`
- `search_result_signals`
- `source_attempts`
- `queries_tried`
- `query_suggestions`
- `gaps`
- `next_steps`
- `risk_notice`

### Hard Limits

Per run:

1. **5-minute timeout**: If the run exceeds 5 minutes, stop new external
   search/fetch actions and enter ROUND_5 with existing evidence.
2. **No recursive crawl, pagination crawl, or infinite scroll**: Only fetch
   the specific target URL identified during search. Do not follow
   pagination links, "next page" buttons, or infinite-scroll loaders.
3. **No large-file downloads, form submissions, credential access, or
   anti-bot bypass**: Only fetch publicly accessible HTTP/HTTPS pages. Do
   not download PDFs, ZIPs, or media files. Do not submit forms, handle
   cookies, solve captcha, or bypass access controls.

### Evidence Admissibility

Every evidence link must satisfy ALL of these conditions:

- Valid HTTP/HTTPS URL.
- Not a search engine results page or site-search page.
- Not a known paywall, login-wall, or captcha page.
- Points to a page that contains the supplier information claimed in the
  candidate fields.

Links that fail these criteria must be removed. If no valid evidence link
remains, the candidate must not enter Supplier Candidates.

Additional rules:
- SERP / site-search pages cannot serve as evidence.
- Paywall / login-wall / captcha pages cannot serve as evidence.
- D-grade signals (AI summary, no URL, search page URL, query-only signal,
  missing minimum fields) cannot enter Supplier Candidates.
- Each candidate must have at least one evidence link.
- Deduplicate actionable leads by canonical URL + normalized supplier name.
- No fabricated "actionable" claims from failed or restricted fetches.

### Failure Handling

When a fetch attempt fails (status: failed, restricted, missing_fields,
rejected):

1. Record the attempt in `source_attempts` with the failure reason.
2. Add a `Gap` entry referencing the `source_attempt_id` and describing
   what was missing.
3. Do NOT create a SourceMapEntry or SupplierCandidate from the failed fetch.
4. If the failure is due to a hard limit, mark remaining rounds as skipped
   and continue to ROUND_5 with existing evidence.

## Workflow

### Pre-Flight

1. Classify runtime capability: `search+fetch`, `search-only`, or `no-search`.
2. If `no-search`, return fail-fast metadata and empty arrays immediately.

### ROUND_1: Seed

3. Build at least 6 deduplicated query combinations across target regions, product terms, and sourcing intents.
4. Execute initial search across at least 3 source categories.

### ROUND_2: Source Discovery

5. From ROUND_1 results, identify source surfaces (B2B platforms, directories, trade show lists, association pages).
6. Build Source Map entries from URL-backed target pages that aggregate multiple suppliers.

A Source Map entry is a **discovery surface** — a URL-backed page that lists, indexes, or aggregates multiple potential suppliers (e.g., a B2B platform category page, a trade show exhibitor list, a government supplier directory). It is NOT a specific supplier. If the page describes a single supplier with contact/location/product details, it is a Supplier Candidate, not a Source Map entry.

7. Record all search result signals as query fuel; do not treat them as evidence.

### R1b: Identity Cross-Map

Before extracting candidates, cross-map each plausible supplier candidate identity across the surfaces that expose it:

- company name and legal name;
- website URL;
- B2B platform store URL or supplier ID;
- trade show exhibitor ID;
- association member ID;
- government registry ID, when public;
- source gap when any mapping cannot be confirmed.

Mapping failures are source gaps, not market-absence claims.

### ROUND_3: Candidate Extraction

8. From Source Map entries and admissible search result target URLs, extract Supplier Candidates.

A Supplier Candidate is a **specific supplier entity** with name, region, and product match. It must come from a Source Map entry or directly from a search result target URL. If the same URL serves as both a discovery surface AND describes a specific supplier, classify it as a Supplier Candidate and do NOT duplicate it in Source Map.

9. Each candidate must have: name, region, product_match_summary, at least one evidence link, evidence grade, and provenance fields.
10. D-grade signals must not enter Supplier Candidates.

### ROUND_4: Expansion

11. From gaps and query suggestions, generate expansion queries targeting uncovered regions, source categories, or product terms.
12. Run one base expansion pass unless the profile is `no-search` or a hard limit has already stopped external actions. If Supplier Candidates are fewer than 8 or source categories are fewer than 3, run at most one targeted expansion or record why it is not possible.
13. Deduplicate actionable leads by canonical URL + normalized name.
14. If hard limit hit, stop new external search/fetch actions, continue to ROUND_5 with existing evidence, and record skipped external actions without fabricating results.

### ROUND_5: Curated Report

15. Assemble all report sections per the contract fields below.
16. Verify report against contract fields and evidence admissibility rules.
17. Record summary.

## Stopping Conditions

Stop new external search/fetch actions only under these conditions:

1. **Round budget exhausted**: All 5 rounds (ROUND_1 through ROUND_5) completed.
2. **Sufficient results after base expansion**: at least 8 Supplier Candidates and at least 3 source categories; this may skip only an additional targeted expansion.
3. **Hard limit hit**: runtime enforces a hard limit such as rate limit, token budget, fetch cap, query cap, or time cap.

Do not skip ROUND_1 through ROUND_3 because of diminishing returns or coverage saturation. When a hard limit fires before all rounds complete, record the stop reason in `execution_metadata.stop_reason`, stop new external actions, continue to ROUND_5 with existing evidence, and mark only blocked external actions as skipped in `stage_records`.

## Evidence Rules

- A: at least two independent public source types cross-confirm the same candidate.
- B: one high-structure public source such as a B2B platform, trade show, association, or government directory.
- C: low-strength but auditable public target URL evidence, such as search-only target URL snippets with minimum fields.
- D: AI summary, no public evidence URL, search page URL, query-only signal, or missing minimum fields. D-grade signals must not enter Supplier Candidates.

Search-only candidates may enter as C-grade only when they are snippet-derived, not fetched, use a non-search-page target URL, and include explicit provenance.

## Fetch Failure Handling

When a fetch attempt fails (status: failed, restricted, missing_fields, rejected):
1. Record the attempt in `source_attempts` with the failure reason.
2. Add a `gap` entry referencing the `source_attempt_id` and describing what was missing.
3. Do NOT create a SourceMapEntry or SupplierCandidate from the failed fetch.
4. If the failure is due to a hard limit (rate limit, fetch cap), mark remaining rounds as skipped.

## Product Coverage Verification

When a fetched page uses collapsible/expandable sections (accordions, "Show more", tabs), the visible content may not represent the full page. For each Supplier Candidate:

1. Note in `field_origin` whether critical fields (name, region, product_match_summary) came from visible or potentially-hidden content.
2. If product listings or supplier details appear to be truncated by UI containers, add a `gap` entry: `{ reason: "collapsible_container_coverage_gap", detail: "..." }`.
 3. Downgrade evidence grade to C if critical fields rely on content that may be hidden behind expandable UI.

Use `sources.yaml` as a source-family checklist for choosing discovery sources, not a mandatory taxonomy.

## Source & Upgrade

- **Repository**: https://github.com/its-How/bigdeal-supplier-finder
- **Upgrade**: Run `git pull` in the skill directory, or re-run `npx skills add its-how/bigdeal-supplier-finder` to get the latest version.
- **Uninstall**: Delete the `bigdeal-supplier-finder/` directory from your skills path.


## Report Contract

Report contract fields are specified in [`references/report-contract.md`](references/report-contract.md). Every report must include the fields listed there.

## Cannot Prove

Live reports prove evidence-bound supplier discovery behavior within the runtime capability assumptions stated above. They do not prove provider readiness, browser/session readiness, account state, credential safety, external site compatibility, or production readiness.

Before any live/provider phase:

- rerun review for browser/provider/credential/live boundaries.

## Live Report Validation

This skill has no deterministic test runner. Live reports are the primary
validation path. The agent must verify its own output against the contract
before declaring success.

For live reports:

1. Keep `evidence_scope: "live"` and do not mix live reports with sample
   or synthetic data.
2. Verify every report section against the contract fields before
   declaring the report complete and accurate.
3. Rerun review for provider, browser, credential, session, and
   external-write boundaries before any live smoke.
