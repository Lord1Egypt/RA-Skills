---
name: data-ai-daily-brief
version: "5.0.0"
description: >
  Turn any industry into a daily intelligence briefing. An AI agent searches,
  filters, writes, and delivers structured daily briefs to 9 channels — with
  machine-checked formatting and a business review gate. Ships with a Data+AI
  profile out of the box; switch to any domain via config.
read_when:
  - daily brief
  - industry report
  - industry newsletter
  - intelligence brief
  - 日报
  - 行业日报
  - 情报简报
allowed-tools:
  - read_file
  - write_to_file
  - replace_in_file
  - execute_command
  - web_search
  - web_fetch
disable: false
---

# Industry Daily Brief

An AI-driven skill that generates a high-quality industry intelligence brief: it automatically searches, filters, writes, and delivers a structured daily report. It ships with a **Data+AI profile** as the working example, and can be switched to **any industry** through the configuration file.

> **How to read this document**
> The **Workflow**, **Confidence Tiers**, **Section Definitions**, **Format Contract**, and **Hard Rules** below are **industry-agnostic** — they are the engine. Everything inside a block marked **`[Default Profile: Data+AI]`** is an **example configuration** (vendor lists, search queries, focus areas) that you replace when targeting another domain. Do not treat the Data+AI specifics as part of the framework.

## Workflow

When the user requests a daily brief, execute the following steps in order.

### Step 1: Confirm Configuration [Deterministic]

1. Read the workspace `config.json` (if present).
2. If absent, initialize defaults via `scripts/init_config.py`.
3. Confirm the target date (default: today) and the output channels.

### Step 2: Collect & Filter Information [Deterministic + LLM]

Use `web_search` to gather information, applying the following priorities and filters.

#### Core Principles

**Relevance first, filter ruthlessly.** Every item must clearly answer: *does this affect the product roadmap, architecture, cost structure, governance, operational efficiency, or real-world adoption within the target industry?* If the answer is not a clear **yes**, exclude it.

**Less is more.** Never lower the admission bar just because a section has few items. The value of the brief is precision, not item count.

#### Three-Phase Search Strategy

**Phase 1 — Targeted first-hand source search (mandatory).**
For each Tier-1 vendor in the active profile, search its official channels (site blog, release notes, GitHub releases, press wires) one by one. Also run dedicated funding / M&A / earnings queries for the tracked companies.

**Phase 2 — Expanded discovery (supplementary coverage).**
Broaden with topic keyword searches across the profile's focus areas and the date range, to catch items the targeted search missed.

**Phase 3 — Source tracing (mandatory).**
For any item discovered via secondary media, use `web_fetch` or an additional `site:` search to trace it back to a first-hand source. Items with no traceable first-hand source are flagged **⚠️ unverified** or demoted to the Watchlist.

**Coverage requirement:** every Tier-1 vendor in the active profile must receive at least one targeted search.

#### Recency Window (red line)

**Weekdays (Tue–Fri):** strictly cover only information **first published within the last 24 hours** (08:00 the previous day → 08:00 today, target timezone).

**Monday special rule:** the window expands to **72 hours** (Friday 08:00 → Monday 08:00), covering Fri–Sun. Monday item cap is raised, and the title is marked as covering the weekend.

⚠️ **Recency red line — never admit any of the following:**
- Information whose original publish date falls outside the current window
- Information that appeared in a previous brief
- Stale announcements from days or weeks ago
- Pre-announced schedules (conferences/summits) that are not a *today* first disclosure

✅ **How to verify recency:**
1. Check the original page's publish date.
2. If it falls outside the window → exclude.
3. Before writing, list each candidate's publish date and confirm item by item.

> **Stale-news guard:** a "big news" item surfacing in search results must have its *original* publish date independently confirmed before admission — search ranking is not recency.

#### `[Default Profile: Data+AI]` — Focus, Vendors, Sources

> Replace this entire block when targeting another industry.

**Focus areas:** big data, data platforms, data infrastructure, data governance, data engineering, lakehouse architecture, query engines, stream/batch processing, vector search infrastructure, open-source data ecosystem. AI items are admitted **only when they clearly affect the data platform**.

**Strictly exclude:** pure-AI news (model releases, benchmarks, consumer AI), AI items with no direct data-platform link, secondhand financial/mass-media analysis, content farms / clickbait / unsourced rewrites.

**Tier-1 vendors:** AWS, Google Cloud, Microsoft Azure, Databricks, Snowflake, Alibaba Cloud, Tencent Cloud, Huawei Cloud, Volcengine.
**Tier-2 vendors:** Confluent, MongoDB, Elastic, ClickHouse, Cloudera, Starburst/Trino, dbt Labs, Fivetran, Airbyte, Dataiku, Palantir, Baidu AI Cloud, JD Cloud.
**Chip vendors (only if directly data-platform related):** NVIDIA, Intel, AMD.

**Open-source projects:** Iceberg, Hudi, Paimon, Delta Lake, Trino, Spark, Flink, Ray, Airflow, Kafka, dbt, ClickHouse, DuckDB, Milvus, Weaviate, Lance/LanceDB, StarRocks, Doris, SeaTunnel, Amoro.

**Funding/IR sources:** SiliconANGLE Big Data, DBTA, InfoQ, PR Newswire, Business Wire, SEC EDGAR, company IR pages, Crunchbase News, CB Insights, PitchBook News, TechCrunch Venture.

**Analyst firms:** Gartner, Forrester, IDC, a16z, Sequoia, Bessemer, Futurum Group, Constellation Research, Wikibon/SiliconANGLE Research; plus regional research institutes and policy/standards bodies relevant to the market.

**Source rules:** accept only first-hand sources (official sites/blogs/release notes, GitHub repos, original posts on X/LinkedIn/blogs, earnings-call transcripts, analyst reports, PR Newswire/Business Wire). Do **not** accept secondhand financial-media analysis (analyst reports excepted).

### Step 3: Write the Brief [LLM]

Produce a professional brief for practitioners in the target industry, based only on the filtered items.

#### Confidence Tiers

- **Level A — confirmed fact:** first-hand source (official site/blog, GitHub release, earnings filing, live event). → may go into A / B / C / D.
- **Level B — high-trust secondary:** reliable media (Reuters, Bloomberg, TechCrunch) but no first-hand doc yet. → may cautiously go into A / C with a "media report / no official filing" label; prefer the Watchlist.
- **Level C — indirect signal / unverified rumor:** social leaks, community chatter, unmerged-PR speculation. → Watchlist only.

#### Deduplication

Each item belongs to exactly one primary section. Priority: A > B > C > D > E. **Mandatory self-check:** after writing all sections, list every event/source/product name and check for cross-section duplicates. If one event appears in two or more sections, keep the highest-priority section and delete or reduce the rest to a one-line reference (≤15 chars).

#### Title & Opening

Title format: `# <Brand> Daily Brief | YYYY-MM-DD` (Monday marked as covering the weekend).

**Fixed opening structure:**
```markdown
**Top 3 takeaways:**
1. [a single trend judgment — direction not full event, 15–30 chars]
2. [a single trend judgment — direction not full event, 15–30 chars]
3. [a single trend judgment — direction not full event, 15–30 chars]

**Verdict:** [the single most important industry judgment of the day, 1–2 sentences, ≤120 chars, landing on direction / investment focus / market shift]
```

**Key distinction:** the "Top 3 takeaways" are *not* a summary of Top Signals nor three event headlines. They are three cross-event "directions worth taking away today."

**Hard constraints:**
- Each takeaway 15–30 chars; no full product names, version numbers, or specific figures; no bold.
- A good takeaway lets the reader grasp *what direction changed* and *so what*.

**Verdict constraints:** ≤120 chars; a directional judgment, not a repeat of the takeaways or of Section A event details.

**Self-check:** after writing the 3 takeaways, cover Section A and read only the takeaways. If the reader can reconstruct each Section A headline and key figure from them, the takeaways read too much like a summary — rewrite.

#### Sections

The five sections use **English titles** and are mandatory (a section may be empty but its header stays).

**A. Top Signals (3 items).** The day's most important events; first-hand source required.
```markdown
### 1. Event title
**来源：** [specific source](url)
**摘要：** 2–3 sentences
**为什么对数据平台重要：** ...
> 企微摘要：one-line semantic compression
```

**B. Product & Tech (0–6 items, less-is-more).** Strictly product & tech moves in the target industry. Each item: title, source, summary (1–2 sentences), impact judgment, WeChat summary.

**C. Views & Research (0–5 items).** Two kinds of high-value content: original views from key people (founders/CEOs/CTOs in interviews, talks, blogs, X, LinkedIn) and formal research from high-credibility institutions (Gartner/Forrester/IDC/Omdia/etc., regional research bodies, top brokerages), plus officially-released policy & standards relevant to the industry. Each item: name, source, core view, mapping-to-industry judgment, WeChat summary.

**D. Capital & Corporate (0–4 items, less-is-more).** Capital/company events directly relevant to the industry, with inline type tags: **【Funding】 / 【Earnings】 / 【IPO】 / 【M&A】**.
```markdown
### 1. 【Funding】Event title
**来源：** [specific source](url)
**核心数据：** amount / valuation / revenue / growth
**摘要：** 2–3 sentences
**对数据平台的影响：** ...
> 企微摘要：one-line semantic compression
```

**E. Watchlist (1–3 items).** Three kinds: **【Preview】** upcoming events, **【Demoted】** valuable items not meeting A–D bars, **【Tracking】** follow-ups whose impact is still unverified. Each item: title, source, why it's worth watching, what signal to wait for, WeChat summary.

#### WeChat-Summary Field (all sections)

After all detailed fields, every item must carry one line: `> 企微摘要：one-sentence semantic compression`.

Rules:
- Semantic compression of the whole item, **≤120 chars**.
- A standalone, self-contained complete sentence.
- No links, no source labels.
- **Markdown only** — never rendered in the HTML output.

> The `**来源：**` and `> 企微摘要：` field markers are kept in their original Chinese form because the WeChat-push and HTML-conversion scripts (`scripts/`) parse these exact strings. When localizing the brief to another language, keep these two markers as-is or update the scripts in lockstep.

#### Output Requirements

- **Rank by importance, differentiate by channel.** Wider search means more candidates — rank strictly by real industry impact > source authority > topic heat; never lower the bar because more sources appeared.
- **WeChat concise version:** keep section caps (A≤3, B≤6, C≤5, D≤4, E≤3); pick only the most important items.
- **HTML full version:** sections may relax by 2–3 items (A still ≤3, B≤8, C≤7, D≤6, E≤5).
- Professional, concise, restrained tone. Every item must have source, summary, and impact judgment. Total 10–14 items (Monday 14–20). Never fabricate data.

### Step 4: Generate Output Files [Deterministic + LLM]

1. **Markdown** `<Brand>_Daily_Brief_{date}.md`:
   - Every item carries a `> 企微摘要：...` line.
   - Contains all items (incl. HTML-extended ones); the WeChat-summary line marks which enter the concise push.
   - **Source links must use Markdown link syntax `[text](url)`** — never bare text `（https://...）`. Bare URLs render as plain text in HTML and break clickable links.
2. **HTML** `<Brand>_Daily_Brief_{date}.html`, styled per `assets/report-template.html`:
   - Each source is a clickable hyperlink.
   - Capital section uses colored type tags (Funding/Earnings/IPO/M&A).
   - **No WeChat-summary lines.**
   - Contains all items.

### Step 4.5: Format Pre-flight (machine self-check, mandatory) [Deterministic]

⚠️ **Run immediately after generating the MD. Must print three counts + all assertions. No output = fail = return to Step 3 and regenerate.** Do the counts with actual `grep -c`, never by eye.

```
📐 Format pre-flight
- item count (^### \d+\.)            = N1
- WeChat-summary count (^> 企微摘要：) = N2
- section count (^## [A-E]\.)         = N3
- assert N1 > 0 ?                     ✅ / ❌   (at least 1; N1=0 → fail)
- assert N1 == N2 ?                   ✅ / ❌   (if N2<N1, check for fullwidth/halfwidth colon variants, then return to Step 3)
- assert N3 == 5 ?                    ✅ / ❌
- section-title language (5 English) ✅ / ❌
- numbering: each section restarts at 1, no cross-section continuation ✅ / ❌
- item separators: a standalone `---` between every two items          ✅ / ❌
- source-link format: every `**来源：**` line is `[text](url)`, no bare `（http...）` ✅ / ❌
- "Top 3" format: `**Top 3 takeaways:**` + ordered list 1./2./3.       ✅ / ❌
- "Top 3" char count: each takeaway 15–30 chars                        ✅ / ❌
- "Top 3" contains product names / versions / figures / bold ?         ❌ clean / ⚠️ hit
- verdict char count = X (≤120)                                        ✅ / ❌
- WeChat-summary char count: each ≤120                                 ✅ / ❌
- field-name compliance (per section, four required fields, no invented field names) ✅ / ❌
- field order: source line first after title, WeChat-summary line last ✅ / ❌
- conclusion: ✅ pass → Step 5 / ❌ fail → regenerate
```

**Any ❌ → return to Step 3 and regenerate the affected content.** Never patch item-count gaps or backfill summaries during the Step 5 review. This gate exists to stop "format drift causing missing WeChat-push content" at the root.

### Step 5: Review & Fix (business layer, 7 checks) [LLM]

After generation and before push, run one full review. Fail → no push. **Precondition: Step 4.5 must pass.**

1. **Recency compliance** — verify each item's publish date against the window (forced date derivation + per-item verification table).
2. **Cross-section dedup** — one event in two+ sections → merge into highest-priority section.
3. **Section-admission compliance** — each item fits its section's admission bar.
4. **Source quality** — each item has a clear first-hand source link (C may allow high-trust secondary).
5. **Content quality** — takeaways are trend judgments (15–30 chars, not event summaries); verdict ≤120 chars, no event-detail repetition; each item follows fact → impact-judgment.
6. **Search coverage** — every Tier-1 vendor was targeted; thin content means expand search, not pad.
7. **Less-is-more** — item counts within range, no padding with low-quality items.

> Format integrity is backstopped by the Step 4.5 machine pre-flight. On any format problem, return to Step 3 to regenerate rather than patching in review.

### Step 6: Deliver (per config) [Deterministic]

Per `config.json`, push to any of **9 channels** (✅ verified / 📦 community-contributed, unverified):

**Regional:** ✅ **WeChat Work** (`scripts/send_wecom.py` — concise summary first <4096 bytes, then full HTML; 3-layer priority fill; no links in summary; duplicate-push lock), 📦 **DingTalk** (`send_dingtalk.py`), 📦 **Feishu/Lark** (`send_feishu.py`).
**Global:** 📦 **Slack** (`send_slack.py`), 📦 **Discord** (`send_discord.py`), 📦 **Telegram** (`send_telegram.py`), 📦 **Microsoft Teams** (`send_teams.py`).
**Universal:** 📦 **Email** (`send_email.py`, SMTP), ✅ **GitHub Pages** (`deploy_github.py`, auto-archives history).

> **Encoding note (Windows):** under a GBK locale, running the push script directly can raise `UnicodeEncodeError` on emoji output and crash a channel mid-print. Run with `PYTHONIOENCODING=utf-8 python -X utf8 <script>` or add `sys.stdout.reconfigure(encoding='utf-8')` at the top of the entry script. If some channels fail, re-push only the failed channel with `--force` to avoid duplicate sends.

## Hard Rules

> These cannot be violated. They override all other guidance.

1. **Stability first.** The system's only goal is zero format drift, zero missed push, zero manual repair. Do not add features, change structure, or "optimize" existing rules unless explicitly requested.
2. **Recency red line.** Items whose original publish date is outside the window (weekday 24h / Monday 72h) are never admitted, no exceptions.
3. **First-hand source required.** Every item traces to a first-hand source; no pure secondhand media analysis.
4. **Never fabricate.** All figures, dates, versions come from the source text; no guessing.
5. **Dedup self-check.** After all sections, run cross-section dedup; one event in at most one section.
6. **Step 4.5 pre-flight.** After generating MD, print the counts + all assertions; any ❌ → return to Step 3. Never patch in review.
7. **Review gate.** Step 5 must pass before push; better unsent than flawed.
8. **Less is more.** No section lowers its bar for item count; an empty section beats a padded one.
9. **Push authority tiers.** In automation mode, business-layer review issues may be self-corrected then pushed; a generation-stage crash (Step 4.5 ❌) must be regenerated, never self-patched; in manual mode, issues await user confirmation.
10. **Source links are Markdown.** Source lines must use `[text](url)`; bare `（http...）` is forbidden (it breaks HTML clickable links).

## Failure Handling

| Scenario | Action |
|----------|--------|
| **Generation-stage format crash (Step 4.5 ❌)** | Return to Step 3 and regenerate the affected section or whole doc; never patch item-count gaps in review |
| Search yields nothing | Report "no qualifying information today", generate an empty template (title + date only), do not push |
| A single source is unavailable | Skip it, continue other searches, note "⚠️ {source} unreachable" |
| All candidates fail review | Output the review detail, do not push, await user decision |
| Candidates severely insufficient (A–D total < 5) | Expand search first; if still short, demote borderline items to E (tagged 【Demoted】); if still short, report and pause for user decision |
| Push fails (webhook timeout / 403) | Retry once; if it still fails, save files to workspace and notify user to push manually |
| Config missing | Generate defaults via `scripts/init_config.py`, then continue |
| HTML template missing | Generate Markdown only, skip HTML, state so in output |
| File detection with non-ASCII (e.g. Chinese) filenames | Use `find`, not `ls` — shells like Git Bash mishandle quoting of non-ASCII paths and produce false "file missing" results |

## Customization

### Switch industry
Edit `config.json` `customization`: focus areas (default Data+AI), vendor priority list, open-source project list, output language and format. Then replace the `[Default Profile: Data+AI]` block in this SKILL.md with your domain's vendors, sources, and search queries.

### Add a delivery channel
Enable it in `config.json` `adapters` and set its config:

| Channel | Key | Type | Main env vars |
|---------|-----|------|---------------|
| WeChat Work | `wechatwork` | Webhook | `WECOM_WEBHOOK_URL` |
| DingTalk | `dingtalk` | Webhook | `DINGTALK_WEBHOOK_URL`, `DINGTALK_SECRET` |
| Feishu | `feishu` | Webhook | `FEISHU_WEBHOOK_URL`, `FEISHU_SECRET` |
| Slack | `slack` | Webhook | `SLACK_WEBHOOK_URL` |
| Discord | `discord` | Webhook | `DISCORD_WEBHOOK_URL` |
| Telegram | `telegram` | Bot API | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |
| Teams | `teams` | Webhook | `TEAMS_WEBHOOK_URL` |
| Email | `email` | SMTP | `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD` |
| GitHub | `github` | API | `GITHUB_TOKEN`, `GITHUB_USER` |

### Adjust the schedule
Edit `config.json` `cron`:
```json
{ "schedule": "0 8 * * 1-5", "timezone": "Asia/Shanghai" }
```

---

*Default profile: Data+AI infrastructure. Framework is industry-agnostic — configure for any domain with public news sources.*
