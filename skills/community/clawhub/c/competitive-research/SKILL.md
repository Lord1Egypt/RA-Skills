---
name: competitive-research
description: "Use when the user asks to research a competitor, map a market, analyze a category, or produce a competitive brief. Trigger phrases: 'research competitors of X', 'who competes with Y', 'market analysis for Z', 'competitive intelligence on [brand/space]', 'analyze this market', 'who are the main players in [category]', 'build a brief before my call', 'I need to understand this space'. Also triggers when preparing a proposal, positioning exercise, content strategy, or client pitch that requires knowing the competitive landscape."
emoji: 🔍
---

# Competitive Intel

Research a competitor, market, or category. Produce a structured brief with sourced claims, evidence tiers, and explicit limitations. Distinguishes observed fact from inference throughout.

## Setup

**No API keys required.** This skill uses only `web_search` and `web_fetch`, both of which are available in standard OpenClaw sessions.

**`OPENCLAW_WORKSPACE`** — only needed for Deep Dive mode (save-report.sh). Defaults to `$HOME/.openclaw/workspace`. If the variable is unset and the default path does not exist, the script will fail with a clear error. Fix: set `OPENCLAW_WORKSPACE` or ensure `~/.openclaw/workspace` exists.

**If `web_search` is unavailable:** Ask the user to provide competitor URLs or names directly. Skip Steps 2 and 4 (identification and review mining via search) and proceed from the provided inputs. Declare this in the Limitations section.

**If `web_fetch` is blocked on a specific domain:** Note the block. Do not invent content. Use SERP snippets and metadata if available; downgrade the tier accordingly.

## Tools

- `web_search` — competitor identification, SERP analysis, review site queries
- `web_fetch` — reading competitor homepages, pricing pages, review pages
- `scripts/save-report.sh` — workspace save for Deep Dive mode (creates files, never deletes)

No other tools required. Do not invoke shell commands, file system writes, or API calls beyond the above.

## Modes

**Quick Scan** (default): 5–8 sources. 10–15 min. Short brief presented inline. No workspace save unless asked.

**Deep Dive**: 15+ sources. Full structured report. Saved to `workspace/research/competitive-intel/YYYY-MM-DD-[slug].md`. Use when the user says "thorough," "deep dive," "full report," "save this," or the scope clearly warrants it.

Confirm mode with the user if ambiguous. Do not silently upgrade Quick Scan to Deep Dive.

## Protocol

### 1 — Scope Declaration
Before researching, state:
- What you will cover (direct competitors, market structure, customer language, pricing signals)
- What you will NOT cover (private financials, internal roadmaps, anything requiring login or paid data)
- Mode selected and estimated time

Clarify "competitors" type if ambiguous:
- **Direct**: same product, same buyer, same budget
- **Adjacent**: different product, same problem or same buyer's budget
- **Aspirational**: who the target brand positions against in their own copy

Default to Direct unless specified.

### 2 — Competitor Identification
Search: `"[category] competitors"`, `"[product] alternatives"`, `"best [product type]"`, `"[product] vs"`

Check: G2, Capterra, ProductHunt, relevant subreddits, Google SERP top 10, any category-specific review sites.

Weight by frequency: competitors that surface across 3+ independent sources are the real ones. Single-source mentions are supporting cast.

### 3 — Profile Each Competitor
For each major player:
- **Positioning**: pull from their homepage headline, not inferred — quote it
- **Target customer**: from their copy, pricing page, or case studies — not inferred
- **Pricing**: only if public; note the page URL and date
- **Differentiators**: their claimed strengths (from site, ads, PR)
- **Weaknesses**: from reviews, forum complaints, missing features — cite source
- **Source**: URL + access date for each claim

Cap at 5 competitors for Quick Scan, 8–10 for Deep Dive. Do not pad with weak players.

### 4 — Customer Language Mining
Pull actual customer words from:
- G2 / Capterra / Trustpilot reviews (note: may be incentivized — label as directional)
- Reddit threads (`/r/[category]`, product-specific subreddits)
- Twitter/X search for brand mentions + complaints
- Amazon reviews for physical products
- App Store reviews for software

Record exact phrases, not paraphrases. These are raw positioning and copy material.
Organize under: pain language, desire language, objection language, switching triggers.

### 5 — Market Structure
Answer:
- Who owns which tier (enterprise / mid-market / SMB / prosumer / consumer)?
- Where is the pricing gap between tiers?
- Who is over-indexed on one segment while ignoring another?
- Is the market expanding, contracting, or consolidating?

State market size only if sourced. Label confidence tier. Do not invent TAM figures.

### 6 — Opportunity Map
This section is **inference and recommendation only** — label it as such.
- What positioning is unclaimed by current players?
- What customer pain is documented in reviews but unaddressed by incumbents?
- What distribution channel is underused?
- What buyer segment is underserved?

Never present this section as observed fact.

### 7 — Evidence Log
Every factual claim used in the report must have a row in the evidence log:
`Claim | Source Name | URL | Date Accessed | Confidence Tier`

See `references/evidence-tiers.md` for tier definitions and usage rules.

### 8 — Output and Save

Use the format in `references/report-template.md`.

Quick Scan: present inline, offer to save.
Deep Dive: present inline AND save to `workspace/research/competitive-intel/YYYY-MM-DD-[slug].md` using `scripts/save-report.sh`.

For the slug, use a short lowercase descriptor: `klaviyo`, `dtc-email-tools`, `mushroom-supplements`.

## Gotchas

**Market size claims.** Never state `"the X market is valued at $Y billion"` without a named source, publication date, and confidence tier. If no source is available, say: `"No reliable market size data found; estimate omitted."` Do not pull from memory or make plausible-sounding numbers.

**Pricing timestamp.** Always note: `"As of [date], pricing starts at $X."` Pricing pages change. A stale price claim undermines the whole report.

**Incentivized reviews.** G2 and Capterra reviews are frequently solicited by vendors. Treat them as directional signals. Note this in the Limitations section. Do not treat them as independent validation.

**Missing data is a finding.** If a company has no public pricing, no reviews, no social presence, no press — say so explicitly. Absence of data is itself a competitive signal (early stage, private, niche, or obscure).

**Scope creep.** Quick Scan must stay Quick Scan. If the user's question requires more depth, name the scope boundary and ask before expanding. Do not silently double the work.

**Do not hallucinate features.** Only report product features that are visible on the company's own site, in reviews, or in documented user reports. If a feature is implied but not confirmed, use INFERRED tier.

**"Competitors" is often wrong the first time.** Users frequently ask about adjacent or aspirational competitors while meaning direct ones, or vice versa. Confirm before investing research time in the wrong frame.

**Web fetch limitations.** Some competitor sites block scrapers or require login. Note this. Do not invent content from a blocked page.

## Verification

This is a data/analysis skill. A report is **complete** when all of the following are true:

- [ ] Scope declared upfront (what's covered, what's not, mode selected)
- [ ] At least 3 direct competitors profiled (or fewer documented as the total market)
- [ ] Every factual claim carries a tier tag (HIGH / MEDIUM / LOW / INFERRED)
- [ ] Evidence Log populated with one row per profiled competitor
- [ ] Market size either sourced-and-tiered, or explicitly omitted with reason stated
- [ ] Opportunity Map section labeled INFERRED throughout
- [ ] Limitations section present

**Edge cases — required handling:**

| Situation | Required response |
|-----------|-------------------|
| Zero web search results for a query | State: "No results found for [query]." Try alternate phrasings. If still empty, declare it in Limitations. |
| Competitor is private with no public data | State: "No public data found for [company]." Document as a finding — not an error. |
| Only 1–2 competitors exist | Complete the report with what exists. Note: "Market appears nascent or niche; fewer than 3 direct competitors identified." |
| Web fetch blocked on competitor site | Note the block per domain. Use SERP snippet metadata if available. Downgrade tier. Do not invent content. |
| User-named competitor does not appear to exist | Ask to confirm the company name before researching. Do not proceed on a mis-named target. |
| All sources are incentivized (G2-only market) | State this in Limitations. Treat all review data as directional. |

**Pass / fail signal:** If the Evidence Log has zero rows on a completed report, the report has failed verification. Minimum: one sourced claim per profiled competitor.

## Blast Radius & Hooks

**Blast radius: Low.**
- All research steps are read-only (web_search, web_fetch).
- `save-report.sh` creates files; it never modifies or deletes existing workspace content.
- Collision behavior: warns and overwrites. Acceptable — competitive intel reports are point-in-time snapshots.
- No credentials touched. No external accounts accessed.

**Hooks: None added. Decision documented.**
- No hook is needed here. The save action is explicit and user-initiated.
- Auto-save on session end would require platform hook support and risks collision on rapid re-runs.
- No trigger event identified that would materially improve safety, enforcement, verification, or auditability beyond the current explicit `save-report.sh` call.
- If a future workflow requires auto-save on Deep Dive completion, add a `post-output` hook at that time with explicit collision handling.

## References

- `references/report-template.md` — full output format to paste and fill
- `references/evidence-tiers.md` — tier definitions (HIGH / MEDIUM / LOW / INFERRED) with usage rules
- `references/example-report-dtc.md` — worked example: fictional DTC adaptogen brand "Rootwell" vs mushroom supplement competitors
- `scripts/save-report.sh` — saves completed report to workspace
