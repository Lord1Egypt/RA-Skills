---
name: a-share-site-crawl
description: Crawl and validate A-share information sources with browser-first and fallback fetch workflows. Use when working with A-share content collection from 韭研公社、雪球、东方财富、财联社、巨潮资讯, especially for: (1) checking whether a site is crawlable, (2) extracting usable public content, (3) choosing between browser and plain fetch, (4) handling anti-bot / login walls, or (5) building repeatable market-news collection, normalization, and cron workflows.
---

# A Share Site Crawl

Use this skill to collect public A-share information from the five target sites and to convert raw site access into repeatable summary-ready records.

## Read Order

Always read these first:

- `references/sites.md`
- `references/workflow.md`

Read these in addition when the task involves formal collection, normalization, or recurring jobs:

- `references/entrypoints.md`
- `references/fields.md`
- `references/risks.md`

Use `references/entrypoints.md` for fixed site entry pages, verification status, cron priorities, and default crawl mode.

Use `references/fields.md` for the normalized schema, source tiering, credibility, opinion-risk handling, content typing, cron retention, time normalization, ticker normalization, and dedup rules.

Use `references/risks.md` for P0/P1/P2 risks, recognition signals, and downgrade or mitigation decisions.

## Core Rule

Prefer `browser` for page truth and `web_fetch` for cheap probing.

- Use `web_fetch` first when the site is known to have stable public text pages
- Use `browser` first when the site is dynamic, disclosure-driven, or clearly stronger in rendered form
- If both fail, report the site as restricted or missing instead of pretending it was covered
- Do not treat anti-bot code, disclaimers, shells, or login walls as usable content

## Working Workflow

### 1. Start from the correct page type

- Prefer fixed entrypoints, list pages, search pages, disclosure pages, telegraph streams, and stock-detail pages
- Do not judge 巨潮资讯 from homepage-only text
- Do not rely on noisy portal homepages when a better inner page exists

### 2. Probe and classify access

Judge each probe into one of these buckets:

- `usable`: readable and materially sufficient
- `partial`: some content is real, but clearly incomplete
- `shell-only`: mainly navigation, scripts, disclaimers, or boilerplate
- `blocked`: anti-bot, login wall, or meaningless payload

### 3. Choose extraction mode

Use one of these verdicts per site or page:

- `fetch-first`
- `browser-first`
- `restricted`
- `not-usable`

### 4. Keep site roles distinct

- 巨潮资讯: official confirmation and disclosure verification
- 东方财富: public aggregation, data-center navigation, and quasi-structured market pages
- 财联社: fast market events and telegraph flow
- 韭研公社: topic logic, timeline, and community clue discovery
- 雪球: sentiment, heat, stock-detail snapshots, and community discussion

### 5. Normalize before summarizing

When the task is more than a one-off crawl check, convert findings into normalized records using `references/fields.md`.

Minimum normalization discipline:

- assign `source_tier`, `credibility`, `content_type`, and `opinion_risk`
- normalize time to Asia/Shanghai when possible
- normalize A-share tickers conservatively
- deduplicate repeated event coverage
- separate confirmed facts from market claims and sentiment

### 6. Apply downgrade rules early

Use `references/risks.md` when deciding whether to downgrade, defer, or replace a source.

Default downgrade behavior:

- login-gated or anti-bot content -> `restricted`
- shell-only or disclaimer-heavy result -> switch entrypoint or switch tool
- 财联社 telegraph 默认先保留列表正文; only hit `detail` when the list is truncated, a canonical URL is needed, or an original-source jump matters
- 巨潮公告默认先保留列表元数据; only chase PDF when the title is high-value enough to justify body extraction, otherwise keep title-derived summary and mark that PDF body was not extracted
- community-only claim without confirmation -> keep as clue, not fact
- unavailable priority site -> disclose it and use approved fallback public sources

## Default Site Priority

Use this order for stable public collection when the task does not specify a scenario:

1. 东方财富
2. 财联社
3. 巨潮资讯
4. 韭研公社
5. 雪球

This order reflects public accessibility and extraction stability, not market importance.

## When to Ask for Stronger Access

Ask for stronger access only when the user explicitly wants better extraction from a restricted site, especially 雪球.

Examples:

- attached Chrome relay tab
- logged-in browser profile
- cookies or authenticated environment
- a dedicated crawler or site-specific script

## Scenario Call Contract

When a cron or caller specifies one of these scenario ids, treat it as a compact instruction bundle and do not ask for a longer prompt:

- `pre-open`: read `references/entrypoints.md`, `references/fields.md`, and `references/risks.md`; use the pre-open priority order; focus on overnight macro or overseas linkage, policy or industry catalysts, key announcements, expected hot sectors, and today's watchlist
- `midday`: read `references/entrypoints.md`, `references/fields.md`, and `references/risks.md`; use the intraday priority order; focus on morning index and turnover snapshot, leading or lagging themes, style or sentiment shifts, active stocks with catalysts, and deviation from the pre-open setup
- `late-session`: read `references/entrypoints.md`, `references/fields.md`, and `references/risks.md`; use the intraday priority order; focus on whether the afternoon main line strengthens or rotates, late-session anomalies, money-flow return direction, hot-stock persistence, and signals that may affect post-close review or next-day expectations
- `post-close`: read `references/entrypoints.md`, `references/fields.md`, and `references/risks.md`; use the post-close priority order; focus on index and turnover recap, main-line review, key stocks and drivers, important announcements plus exchange or regulator dynamics, and next-day clues with risks

For every scenario:

- keep the output in Chinese and lead with conclusions before detail
- keep `已确认事实`, `市场观点与情绪`, and `待核实线索` clearly separated
- keep `本轮缺失站点` and `来源层级说明` in the final output
- bind every round to the entrypoint, field-normalization, and risk-downgrade rules instead of freehand summarizing
- do not output buy or sell recommendations

## Standard Output

When producing a formal round output, always structure it with at least these sections:

- `已确认事实`
- `市场观点与情绪`
- `待核实线索`
- `本轮缺失站点`
- `来源层级说明`

Use the sections as follows:

- `已确认事实`: only T1 or well-supported T2 items, or items clearly marked as partially confirmed
- `市场观点与情绪`: T3 discussion, heat, consensus drift, and sentiment signals
- `待核实线索`: rumors, single-source community claims, partial clues, or conflicting statements
- `本轮缺失站点`: blocked, unstable, login-gated, or otherwise uncovered priority sites and what fallback was used
- `来源层级说明`: explain T1/T2/T3 usage and remind the reader that community sources are not equal to formal disclosure

## Per-Site Quick Output for Crawlability Tasks

When the task is specifically about site feasibility rather than a market summary, return:

- Site
- Status
- Recommended mode
- Best entry page
- What works
- Main limitation
- Next step

## Non-Negotiables

- Distinguish confirmed facts from community opinion
- Prefer official disclosure and high-confidence public reporting over discussion boards
- Do not output buy/sell recommendations
- Do not imply full coverage when a priority site failed or was inaccessible
