## Apify-First Release Note

Beyond SEO 1.0.2 uses Apify as the primary data layer. The skill should ask for only `APIFY_API_TOKEN` by default, then use Apify actors for crawling, SERP, competitors, Maps/local, reviews, Trends, PageSpeed/Lighthouse, GSC/GA4-style connector or export workflows, and backlink/authority checks where available.

Other APIs should not be requested up front. They are only optional later if Apify cannot fetch the needed data or if a private authenticated account/export is required.


---

# Beyond SEO

## Universal Agent Compatibility

This release is designed to be portable across Codex, Claude Projects, OpenClaw, Cursor, MCP-enabled agents, and custom file-based AI agents.

For Codex-style skill loading, `SKILL.md` now includes YAML frontmatter at the top. For Claude/OpenClaw/custom agents, load the full folder and instruct the agent to read `SKILL.md` first, then use the supporting modules as needed.

## Release Maturity Note

This is a complete structure release with deep core modules and several concise specialist modules. Shorter modules are intentional lightweight playbooks that define the workflow and should be expanded later only when a project needs deeper industry-specific SOPs.


**Beyond SEO** is a portable AI-agent skill for serious SEO, AEO/GEO, local SEO, competitor research, backlink evaluation, and client-ready SEO growth planning.

This skill is designed to work across different AI-agent environments, including Codex, Claude Projects, OpenClaw, Cursor, MCP-style agents, and custom local agents.

It is intentionally built as a file-based operating system rather than a single prompt. Each file teaches the agent how to think, what to check, how to use available tools, how to fall back when tools are missing, and how to produce practical, evidence-based outputs.

---

## What Beyond SEO Is

Beyond SEO is a senior SEO strategist inside an agent.

It should be able to:

- audit a website technically;
- inspect page architecture and crawlability;
- identify thin pages, missing headings, duplicate metadata, schema gaps, and JavaScript-rendering issues;
- check current keyword opportunities when data is available;
- compare competitors;
- map keywords to service pages, course pages, product pages, or supporting articles;
- create 30/60/90-day SEO plans;
- evaluate backlinks and authority gaps;
- suggest safe free and paid backlink strategies;
- audit local SEO and Google Business Profile opportunities;
- evaluate AEO/GEO readiness for answer engines and AI search;
- create client-ready reports and developer briefs.

---

## What Beyond SEO Is Not

Beyond SEO is not:

- a generic SEO checklist;
- a keyword stuffing prompt;
- a backlink spam system;
- a fake guarantee machine;
- a “write more blogs” assistant;
- a high-DA worshipper;
- a tool that invents rankings or search volume.

If data is missing, Beyond SEO must say the data is missing.

---

## Phase 1 Files

Phase 1 creates the core brain and operating rules.

```text
beyond-seo/
├── SKILL.md
├── _meta.json
├── README.md
├── setup.md
├── onboarding.md
├── capability-detection.md
└── audit-modes.md
```

### `SKILL.md`

The master instruction file. Defines the role, rules, audit workflow, no-fluff behavior, data quality standards, SEO/AEO/backlink/local logic, and required reporting structure.

### `_meta.json`

Machine-readable metadata for agent systems. Includes skill name, version, supported environments, optional environment variables, and quality rules.

### `README.md`

Human-facing overview. Explains what the skill does and how the file structure works.

### `setup.md`

Installation and configuration instructions for Codex, Claude Projects, OpenClaw, Cursor, and custom agent systems.

### `onboarding.md`

The standard opening process the agent uses when a user requests an SEO task. It explains what information to request, what not to over-ask, and how to proceed with limited data.

### `capability-detection.md`

The logic for detecting available tools, APIs, exports, and files before choosing an audit mode.

### `audit-modes.md`

Defines the five audit modes:
1. Full Intelligence Mode
2. Apify Intelligence Mode
3. Native Agent Scraping Mode
4. File Analysis Mode
5. Advisory Mode

---

## Recommended Optional Inputs

For the strongest audit, provide:

```text
Website URL
Target country/city
Business type
Main services/products/courses
Competitor URLs
Google Search Console export
Google Analytics export
Google Business Profile export/access
Ahrefs/Semrush/Moz exports or screenshots
Screaming Frog/Sitebulb crawl export
Apify API token
```

But the skill must still work without these, using the best available mode.

---

## Primary Environment Variable

```text
APIFY_API_TOKEN
```

Beyond SEO is Apify-first because Apify can act as a flexible SEO data layer for crawling, SERP scraping, maps/local checks, trends, authority-style scrapers, and competitor research.

If Apify is not available, Beyond SEO falls back to native browsing/scraping/search tools, uploaded files, or advisory workflows.

---

## Standard Output Philosophy

Every useful Beyond SEO output must tell the user:

```text
What was checked
What was found
Why it matters
What to do next
What priority it has
What data is missing
```

Every recommendation must connect to at least one of:

```text
Ranking
Qualified traffic
Crawlability
Indexability
Topical authority
Local visibility
Backlink authority
AEO/GEO visibility
Conversion
Measurement
Risk reduction
```

---

## Build Roadmap

### Phase 1: Core Brain

Complete.

### Phase 2: Apify + Scraping Engine

Included files:

```text
integrations/apify.md
integrations/apify-actor-registry.md
integrations/apify-workflows.md
integrations/native-agent-scraping.md
integrations/fallback-without-apis.md
```

### Phase 3: Audit Engine

Included files:

```text
audit/full-site-audit.md
audit/technical-seo-audit.md
audit/on-page-seo-audit.md
audit/content-quality-audit.md
audit/schema-audit.md
audit/conversion-seo-audit.md
```

### Phase 4: Keyword + Competitor Engine

Complete files:

```text
keyword-research/keyword-discovery.md
keyword-research/keyword-clustering.md
keyword-research/keyword-to-page-map.md
competitor-research/competitor-discovery.md
competitor-research/serp-gap-analysis.md
competitor-research/content-gap-analysis.md
```

### Phase 5: AEO/GEO Engine

Complete files:

```text
aeo-geo/ai-search-readiness.md
aeo-geo/answer-engine-optimization.md
aeo-geo/entity-seo.md
aeo-geo/topical-authority.md
```

### Phase 6: Local + Backlink Engine

Complete files:

```text
local-seo/google-business-profile.md
local-seo/map-pack-audit.md
backlink-system/backlink-audit.md
backlink-system/free-backlink-posting.md
backlink-system/paid-backlink-evaluation.md
backlink-system/backlink-quality-scoring.md
backlink-system/backlink-outreach-prompts.md
```

### Phase 7: Reporting + Templates

Included files:

```text
strategy/30-day-plan.md
strategy/60-day-plan.md
strategy/90-day-plan.md
strategy/500-query-growth-model.md
reporting/client-audit-report.md
reporting/proposal-style-report.md
templates/seo-audit-report-template.md
templates/keyword-map-template.csv
templates/backlink-prospect-template.csv
examples/sample-final-audit-output.md
```

---

## Non-Negotiables

Beyond SEO must never:

- guarantee rankings;
- invent keyword/search/backlink data;
- recommend spam links;
- treat DA/DR as the only backlink quality signal;
- ignore conversion when lead goals are mentioned;
- ignore local SEO for local businesses;
- ignore E-E-A-T for YMYL niches;
- call AEO/GEO a strategy without explaining exact actions;
- give 100 tasks with no priority.

Good SEO is not activity. Good SEO is a system that increases qualified visibility and turns that visibility into business outcomes.


### Backlink Source Library Seed

A Phase 6 seed file has been added early at `backlink-system/free-paid-backlink-source-library.md` so the skill remembers the user's backlink document categories and free/paid backlink evaluation rules.



## AI-Friendly SEO Expansion — 1.0.3

Beyond SEO now includes a dedicated AI-friendly SEO workflow.

When a user asks for AI-friendly SEO, the skill audits:

```text
Traditional SEO
AEO: answer readiness
GEO: AI citation/source-worthiness
Entity SEO: knowledge graph clarity
Reputation SEO: proof stack
Conversation SEO: full human question coverage
```

Use Apify first for crawling, SERP/PAA, competitors, Maps/local, reviews, Trends, PageSpeed/Lighthouse, third-party mentions, and authority/backlink checks.
