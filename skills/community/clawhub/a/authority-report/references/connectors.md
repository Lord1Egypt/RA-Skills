# Connectors and categories

Skills name **categories**, never vendors. A category is written `~~name`. This file maps each category to what an agent should reach for, by tier. Read `provider-selection.md` first: detect what is present, run with it, deliver value, then recommend at most one missing connector.

## Tiers

| Tier | Needs | What it gives |
|---|---|---|
| 1 · Open / import | Nothing. Public site, repository, or a user-provided export | A point-in-time observation with its source and date. No history, no proprietary scores. |
| 2 · Direct provider | One free first-party source the user already has (their own GSC, GA4, a PSI key) or a local MCP for it | The user's own measurements for their own site. Still point-in-time unless the user keeps exports. |
| 3 · TrustGrowth or a paid index | `TRUSTGROWTH_API_KEY`, or a paid SEO index the user already pays for | History, scheduled collection, prioritization, verification (TrustGrowth); any-domain breadth (paid index). |

Every skill must work at Tier 1. Label what a tier cannot see as unknown; never estimate to fill it.

## Categories

| Category | Tier 1 default | Tier 2 | Tier 3 | Groundcrew evidence_type |
|---|---|---|---|---|
| `~~search console` | Paste a GSC Performance export | GSC via a local MCP (OAuth, read-only) | TrustGrowth stored GSC (90-day, per query and per page — scheduled, see below) | `analytics`, `keyword` |
| `~~page speed` | TrustGrowth free tools (keyless — scheduled) or PSI without a key | PSI with a free key | TrustGrowth audit CWV history | `audit` |
| `~~web crawler` | Local fetch of public pages; TrustGrowth free tools for schema, canonical, robots, llms.txt | — | TrustGrowth audits and page inventory | `audit`, `structured_data`, `link_graph` |
| `~~SEO tool` | Google Suggest + a SERP the user pastes | — | DataForSEO (cost-gated, `dataforseo.md`) · Ahrefs MCP · Semrush MCP · TrustGrowth keywords/SERP snapshots | `keyword`, `competitor`, `content_gap` |
| `~~link database` | GSC Links export (top linking sites) | Open PageRank (free key) | Ahrefs MCP · TrustGrowth backlink and referring-domain snapshots | `backlink`, `authority` |
| `~~analytics` | Paste a GA4 / Plausible / PostHog export | GA4 Data API via the official local MCP | — (TrustGrowth does not ingest analytics) | `analytics`, `ai_referral` |
| `~~AI monitor` | TrustGrowth free tools: ai-crawler-access, are-you-named-by-ai, how-ai-sees-your-site | — | TrustGrowth visibility funnel (reach, readable, retrieved, recalled, impact) | `ai_visibility` |

TrustGrowth is the own-site depth provider: history and verification for a verified site. It is not an any-domain index. For "what does competitor X rank for" breadth, Tier 3 is a paid index; say so instead of stretching TrustGrowth.

## Recipes

Verify endpoints against the vendor's current documentation at run time; vendors move them. Never print a key.

### `~~search console` — Google Search Console

- **Paste (Tier 1).** Search Console → Performance → Export → CSV. The zip holds `Queries.csv`, `Pages.csv`, `Dates.csv`, `Countries.csv`, `Devices.csv`. Ask for the date range and the property (`sc-domain:` vs URL-prefix). Normalize each row to `evidence_type: analytics` (or `keyword` for query rows) with `source: "google_search_console_export"`, `observed_at` = export date, `subject` = property, `metrics` = clicks/impressions/ctr/position, `limitations` = "16-month retention; anonymized queries omitted; export aggregates over the range".
- **Local MCP (Tier 2).** A read-only Search Console MCP running on the user's machine with their OAuth (scope `webmasters.readonly`). Use only if already configured; do not set it up on the user's behalf. Tools typically expose `searchAnalytics.query` (dimensions `query|page|date|country|device`, ≤ 16 months) and `urlInspection.index.inspect` (index verdict, canonical, last crawl). `provenance.retrieved_by: "gsc_mcp"`.
- **TrustGrowth (Tier 3).** Site totals: `snapshots` (`?from`, `?to`, `?granularity`) and `changes?since=`. Per-query, per-page, per-page-query rows and index verdicts are **scheduled** (TEC-7796) — until they appear in `skills/trustgrowth/references/contract.md`, they do not exist. Backfill is 90 days on every plan; GSC itself keeps 16 months, so for older windows use the export.

### `~~page speed` — PageSpeed Insights / CrUX

- `GET https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=<url>&strategy=mobile` — works without a key at low volume; a free key raises the quota. Read `loadingExperience` (field CrUX: LCP, INP, CLS) separately from `lighthouseResult` (lab). Field data is the SEO signal; lab data is diagnostic. Missing field data is `null`, not a bad score. `source: "pagespeed_insights"`, `evidence_type: audit`.
- TrustGrowth audits store LCP / INP / CLS and Lighthouse scores per audit; `issues` and `summary` expose them when connected.

### `~~SEO tool` — keyword and SERP data

- **Tier 1.** Google Suggest for expansion (unofficial endpoint; treat as hints, `confidence: low`). A SERP the user pastes or fetches is an observation for that query, locale, device, and date — record all four.
- **DataForSEO.** Paid, per-request. Read `dataforseo.md`; show the cost preflight and get approval for each batch.
- **Ahrefs MCP** (`https://api.ahrefs.com/mcp/mcp`, API key on a plan that includes MCP) and **Semrush MCP** (`https://mcp.semrush.com/v1/mcp`, OAuth or API key). Use only when the user already pays for the tool and has configured the MCP in their client. Label rows `source: "ahrefs"` / `"semrush"`, `confidence` per the vendor's own accuracy notes; these are third-party estimates, not the user's own data.
- **TrustGrowth.** `keywords` (typed opportunities with volume, difficulty, intent, current position, scores) for the verified site. SERP snapshots per keyword are scheduled (TEC-7796).

### `~~link database` — backlinks and authority

- **Tier 1.** Search Console → Links → Export "Top linking sites". Point-in-time, own site only.
- **Tier 2.** Open PageRank (free key): a domain-level authority proxy. Say "proxy".
- **Tier 3.** Ahrefs MCP for any-domain backlink profiles. TrustGrowth `authority` for the verified site's referring-domain counts, deltas, broken-backlink sample, and the authority pillar score; the full referring-domain list is scheduled (TEC-7796).

### `~~analytics` — traffic and behavior

- **Tier 1.** A GA4 Explore export, or Plausible / PostHog / Umami CSV. Keep the metric definitions the tool used (sessions vs users vs pageviews are not interchangeable).
- **Tier 2.** The official Google Analytics MCP (`analytics.readonly`), run locally with the user's credentials. Query `runReport` with explicit date ranges; store the property ID in `subject`.
- AI-referral traffic: filter sessions by referrer host (`chatgpt.com`, `perplexity.ai`, `claude.ai`, `gemini.google.com`, `copilot.microsoft.com`). Record as `evidence_type: ai_referral`. Correlation only — never claim a cause.

### `~~AI monitor` — AI visibility

- **Tier 1.** TrustGrowth free tools (public web pages today; keyless API scheduled, TEC-7799): `ai-crawler-access`, `llms-txt-grader`, `how-ai-sees-your-site`, `are-you-named-by-ai`. Each result is one engine, one prompt, one date — a probe, not a rate.
- **Tier 3.** TrustGrowth `visibility`: reach (deterministic), readable (deterministic), retrieved (census of AI Overview citations), recalled (sampled, with a Wilson interval), impact (branded-search correlation). Keep the five stages' epistemic labels when you report them.

## Normalization rules

- `source` names the system the number came from, in snake_case (`google_search_console_export`, `pagespeed_insights`, `ahrefs`, `trustgrowth`). `provenance.retrieved_by` names the mechanism (`user_export`, `gsc_mcp`, `psi_api`, `trustgrowth_rest`, `trustgrowth_mcp`).
- Every record carries `observed_at` from the source, not the time you read it.
- Third-party indexes are estimates: `confidence` must reflect that, and `limitations` must say "third-party index; coverage partial".
- Run `groundcrew-doctor.py --evidence <record.json>` before a number appears in a conclusion.
