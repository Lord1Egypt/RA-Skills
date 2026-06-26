# Apify-First Setup Update

Beyond SEO 1.0.2 is Apify-first.

## Required Setup

Only one token is expected by default:

```text
APIFY_API_TOKEN
```

## Recommended Agent Behavior

At install or first use, check for `APIFY_API_TOKEN`.

If found:

```text
Use Apify Intelligence Mode.
```

If missing:

```text
Ask once for APIFY_API_TOKEN or Apify MCP setup.
```

Do not ask for GSC, GA4, Ahrefs, Semrush, Moz, PageSpeed API, DataForSEO, or Firecrawl by default. Use Apify actors first for those workflows where available.

## Optional Python Requirements

```bash
pip install -r requirements.txt
```


---

# Beyond SEO Setup Guide

This file explains how to install and use the Beyond SEO skill in different AI-agent environments.

Beyond SEO is designed as a portable folder-based skill. The agent should read `SKILL.md` first, then use the supporting files when a task requires setup, onboarding, capability detection, or audit mode selection.

---

## 1. Folder Placement

Recommended folder:

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

In future phases, additional folders will be added:

```text
integrations/
audit/
keyword-research/
competitor-research/
aeo-geo/
local-seo/
backlink-system/
strategy/
industry-playbooks/
reporting/
templates/
examples/
tools/
```

---

## 2. Required File Read Order

When loading this skill into an AI-agent system, instruct the agent to read files in this order:

```text
1. SKILL.md
2. _meta.json
3. README.md
4. setup.md
5. onboarding.md
6. capability-detection.md
7. audit-modes.md
```

For actual SEO work, the agent should always follow the operating rules in `SKILL.md`.

---

## 3. Recommended Agent System Prompt

Use this short instruction when attaching the skill folder to an agent:

```text
You have access to the Beyond SEO skill folder. Read SKILL.md first. Follow its no-fluff SEO, AEO/GEO, backlink, local SEO, competitor research, and reporting rules. Before any audit, use capability-detection.md and audit-modes.md to choose the correct operating mode based on available tools, APIs, files, and exports. Never invent rankings, traffic, backlinks, or search volume. Label estimates clearly.
```

---

## 4. Optional Environment Variables

Beyond SEO does not require APIs to function, but it becomes much stronger when these are available.

### Primary

```text
APIFY_API_TOKEN
```

Use this for Apify actors, crawling, scraping, SERP checks, maps/local checks, trends, authority-style data, and competitor data.

### Technical Checks

```text
PAGESPEED_API_KEY
```

Use this for PageSpeed Insights and Core Web Vitals where supported.

### Export Paths

```text
GSC_EXPORT_PATH
GA4_EXPORT_PATH
AHREFS_EXPORT_PATH
SEMRUSH_EXPORT_PATH
MOZ_EXPORT_PATH
SCREAMING_FROG_EXPORT_PATH
SITEBULB_EXPORT_PATH
```

These point to uploaded or local files the agent can analyze.

### Custom Scraping

```text
CUSTOM_SCRAPER_API_KEY
CUSTOM_SCRAPER_BASE_URL
```

Use these if the environment has a private scraper, crawler, or MCP scraping server.

---

## 5. Codex Setup

For Codex-style agent environments:

1. Add the `beyond-seo/` folder to the project repository.
2. Add or expose `APIFY_API_TOKEN` in the environment if available.
3. Tell Codex:

```text
Use the Beyond SEO skill. Read beyond-seo/SKILL.md first. For every SEO task, detect available APIs, files, and scraping tools, then choose the proper audit mode before producing output.
```

4. If Codex can run Python or shell commands, future tool scripts inside `tools/` can be used for environment checks and output normalization.

---

## 6. Claude Projects Setup

For Claude Projects:

1. Upload the complete `beyond-seo/` folder or files.
2. Add the short agent instruction from section 3.
3. When starting a task, provide:
   - website URL;
   - target market;
   - business type;
   - competitors if known;
   - exports if available.

Claude may not have direct environment variable access depending on setup. If so, paste API availability or exported reports manually.

---

## 7. OpenClaw Setup

For OpenClaw or similar file-based agent systems:

1. Place `beyond-seo/` in the skills or knowledge directory used by the agent.
2. Add a skill alias such as:

```text
beyond-seo
```

3. Make sure the agent can access:
   - browser/search tool;
   - scraper tool;
   - Apify MCP/API if configured;
   - local files/exports.

4. Instruct the agent:

```text
When the user asks for SEO, AEO, backlinks, competitors, local SEO, or website growth plans, activate Beyond SEO and follow its audit-mode detection.
```

---

## 8. Cursor Setup

For Cursor:

1. Add `beyond-seo/` to the project repo.
2. Open the workspace.
3. Ask Cursor:

```text
Read beyond-seo/SKILL.md and follow it as the operating rule for this SEO project.
```

4. If building SEO fixes for a website, use Beyond SEO outputs as developer briefs:
   - metadata changes;
   - schema;
   - page routes;
   - SSR/pre-rendering;
   - internal linking;
   - content blocks;
   - technical SEO fixes.

---

## 9. Custom Agent Setup

For any custom agent:

1. Load all Markdown files as system or knowledge instructions.
2. Give highest priority to `SKILL.md`.
3. Use `_meta.json` for metadata and feature discovery.
4. Expose API keys through environment variables.
5. Give the agent access to:
   - browser/search;
   - page scraper;
   - file reader;
   - CSV parser;
   - optional Apify API;
   - optional PageSpeed API.

The agent must not fail if APIs are missing.

---

## 10. Minimal Usage Example

User prompt:

```text
Audit https://example.com for SEO and AEO. I want a 90-day plan to increase qualified leads.
```

Beyond SEO response flow:

```text
1. Check available data/tools.
2. Choose audit mode.
3. Crawl or inspect the site.
4. Identify technical, content, keyword, local, backlink, and AEO gaps.
5. Prioritize issues.
6. Produce 30/60/90-day plan.
7. List missing data.
```

---

## 11. Strong Usage Example

User prompt:

```text
Audit https://example.com. Target city: Karachi. Main services: AI automation, AI agents, no-code systems. Competitors: competitor1.com, competitor2.com. I have Apify token and GSC export.
```

Beyond SEO should:

```text
1. Use Full Intelligence or Apify Intelligence Mode.
2. Crawl own site.
3. Crawl competitors.
4. Pull SERP/keyword opportunities if possible.
5. Analyze GSC export.
6. Build keyword-to-page map.
7. Create service pages and support article plan.
8. Add AEO/GEO recommendations.
9. Add local SEO recommendations if service-area relevant.
10. Produce 90-day execution roadmap.
```

---

## 12. Output File Creation

When the agent creates outputs, prefer:

```text
Markdown for reports
CSV for keyword maps and backlink prospects
JSON for machine-readable audit summaries
PDF/DOCX only when user explicitly asks for shareable documents
```

---

## 13. Safety and Honesty Rules

The agent must not:

- claim it crawled a site if it did not;
- claim it checked Apify if no token/tool existed;
- claim traffic or ranking data without evidence;
- recommend risky backlink packages;
- promise ranking timelines;
- hide missing data.

Use:

```text
Confirmed
Likely
Directional
Estimated
Not verified
```

---

## 14. Phase 1 Completion Test

After installing Phase 1, ask the agent:

```text
What audit mode would you use if I only provide a website URL and no API?
```

Correct answer:

```text
Native Agent Scraping Mode if browser/search/scraping tools exist; otherwise Advisory Mode. The agent should still provide a useful workflow and not pretend live data exists.
```

Second test:

```text
What audit mode would you use if I provide APIFY_API_TOKEN but no GSC/GA4?
```

Correct answer:

```text
Apify Intelligence Mode.
```

Third test:

```text
Can you guarantee top 3 ranking in 90 days?
```

Correct answer:

```text
No. Beyond SEO can build a realistic plan, but it cannot guarantee rankings.
```
