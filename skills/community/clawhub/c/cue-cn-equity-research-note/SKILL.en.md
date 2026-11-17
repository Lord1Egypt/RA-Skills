---
name: cn-equity-research-note
slug: cue-cn-equity-research-note
displayName: "Equity Deep-Dive Note · Every Claim Sourced · Citation (个股深度研究)"
summary: "Pre-earnings single-name study: business, competition, drivers, risks, figures."
description: "Pre-earnings study: business, competition, drivers, risks, key figures. Every claim carries quote, anchor and [S#]; sources carry URL and date. Ratios only from quotes. No ratings, targets or forecasts. Triggers: equity research / business breakdown / competitive position / drivers / risk list"
version: "0.2.2"
license: MIT
tags: [equity-research, deep-dive, sourced-claims, business-breakdown, key-figures]
---

# Equity Deep-Dive Note · Every Claim Sourced

**What it produces**: a research draft on a company during the period when **no financial report has been released yet** — every claim and every figure traceable back to one quoted sentence.
**It is not** an investment decision, not a recommendation, not a rehash of broker reports, and it never publishes on its own.

## 0. When to use / when not to

| You want | Use |
|---|---|
| Single-name research while results are not out: how the business splits, where it competes, what drives it, what could go wrong, what the key numbers are | **this skill** |
| Post-results commentary: period-over-period differences, account-level reconciliation | `cn-earnings-note` |
| A set of questions answered across many sources ("how much of revenue is overseas?") | `cn-research-brief` |
| Scraping broker reports and repeating their conclusions | not this skill — claims must go back to a sentence |
| Ratings, target prices, timing, share-price direction | never — see §4 check three |

**Three-way boundary (the line users need):**

- `cn-earnings-note` = commentary on **released** financials; its input must include the report. This skill **does not require a report**; it works the **expectation period**.
- `cn-research-brief` = **question-driven** (it answers what you ask). This skill is **subject-keyed**: give a ticker or name, get one structured company study.
- Broker-report scrapers = **fetching report text**. This skill treats reports as one source among many but **reproduces the quoted sentence**, never the conclusion.

## 1. Input contract

Ask before starting (ask only what is missing, ≤5 questions, each with a default):

- **Subject**: ticker or full company name (default: the name from the previous turn; ask if none)
- **As-of date**: the cut-off for the study, default today; retrieval dates on source lines are the actual search dates, never back-filled from the cut-off
- **Focus** (optional): e.g. "capacity and customer mix"
- **Material** (optional): announcement PDFs, research notes, pages, minutes — via `+parse`; absence does not block
- **Market** (optional): A-share / HK / US, default inferred from the ticker and stated at the top

## 2. Five sections (missing one is a failure)

| # | Section | Minimum |
|---|---|---|
| 1 | Business breakdown | where revenue and profit come from, split by product line or segment; the sources decide how many lines, no padding |
| 2 | Competitive position | share, rivals, barriers, pricing power, each with a quote; **no quote for share means no share claim** |
| 3 | Drivers | variables that move results over the next 6–24 months, each as "variable → transmission → observable metric" |
| 4 | Risk list | each as "risk → trigger → disclosed mitigation"; if no mitigation is disclosed, say it was not obtained |
| 5 | Key-figure table | one table, one figure per row: metric / value / basis and period / quote / anchor / [S#] |

Findings are written as `-` list lines ending in the triple (§3). **Judgments need sourcing too** — that is what separates this from a quick brief.

## 3. Quote and anchor (the shape check two enforces)

```
- finding …… 「a contiguous span of the source text」〔锚:page/section/table〕[S3]
```

- **Quote**: wrapped in 「」, taken **contiguously** from the source; no rewriting, no stitching, no ellipsis-then-continue.
- **Anchor**: `〔锚:…〕` naming the location (page, section number, table name or paragraph index).
- **Reference**: `[S#]` matching one source line in §5.
- A finding supported by several sentences carries several triples; never weld them into one fake quote.

## 4. Five checks (offline, zero network)

Authoritative behaviour is `scripts/check_note.py`; this section explains the intent:

1. **ER-FORM form**: five sections present and ordered, each non-empty; key-figure table has a header row with quote/anchor/source columns; subject and as-of date present; no stray prose in the content sections.
2. **ER-ANCHOR quote and anchor**: every `-` finding ends with the quote + anchor + [S#] triple; every referenced [S#] has a registered source line; source lines carry a clickable http(s) URL **and** a retrieval date.
3. **ER-REDLINE red lines**: ratings (buy/add/recommend/outperform), target prices, price forecasts, bullish/bearish calls — zero tolerance. A `[待人工]` clause exempts only that clause.
4. **ER-NOSELF no self-computed ratios**: any percentage must appear verbatim inside that line's quote. Otherwise it must be marked `〔自算〕` with both a numerator source and a denominator source on the same line.
5. **ER-SCOPE scope**: language belonging to released-results commentary points to `cn-earnings-note`; question-driven language points to `cn-research-brief`; report-conclusion language is rejected.

## 5. Sources section

```
## Sources

- [S1] Title | https://… | retrieved 2026-11-09 | type: announcement/research/news/website
```

- The URL must be a clickable original. If you cannot get one, name it under the risk section as not obtained — do not list it here.
- The retrieval date is **the day you actually searched**, not the source's publication date; both may appear side by side.

## 5b. Confirming the channel is present (optional)

Only needed once a `CUE_API_KEY` is configured. List the catalog first, then confirm the tools are present at the routing address it gives:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000
# take the group's routing address from the catalog, then confirm the tools are present
curl -s -X POST "$ROUTING_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Without a credential the skill still works: put the material in the working directory and use the user-supplied path.

## 6. No-channel / missing material

- With no material at all, produce a **shaped skeleton**: five sections present, one placeholder each, empty sources. A skeleton **failing the checks is by design**, not an omission to fix.
- A single section missing material says what was not obtained and is summarised at the end; never paper over the gap with "about" or "roughly".

## 7. Files

`SKILL.md` / `SKILL.en.md` / `README.md` / `README.en.md` / `CHANGELOG.md` / `scripts/check_note.py` / `scripts/fixtures/` (1 good + several bad) / `scripts/fixtures/run_fixtures.sh`.

> Note: the declaration layer (`consumes` / `inputs` / `produces`) lives only in `SKILL.md`; this English face carries no such keys.
