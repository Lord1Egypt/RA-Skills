---
name: exa-neural-query-planner
displayName: "Exa Neural Query Planner"
version: "1.0.0"
description: "Plan Exa neural web searches before calling any Exa wrapper — craft queries, pick categories, set domain/date filters, define fallbacks, and decide when Exa beats keyword search."
triggerKeywords:
  - exa search plan
  - exa neural query
  - plan exa search
  - exa domain filter
  - exa category research
  - exa vs tavily
  - exa search strategy
  - neural web search query
  - exa query planner
  - optimize exa search
tags:
  - exa
  - web-search
  - documentation
  - research
  - query-planning
license: "MIT"
language: "en"
hasExecutableCode: false
promptOnly: true
execution: "noExec"
---

# Exa Neural Query Planner

## Purpose

Produce an **Exa search plan** before any Exa API call (via `exa`, `exa-plus`, `web-search-plus`, MCP, or custom scripts). Exa’s neural search rewards well-phrased natural-language queries and the right `category` / domain / date filters — most wrappers execute requests but don’t help you **plan** them.

This skill does **not** call Exa, store API keys, or wrap the API. It outputs a ready-to-run plan another skill or script can execute.

## When to use

Use when the user mentions:

- Searching with Exa or exa.ai
- Neural / semantic web search for docs, papers, companies, news, or GitHub repos
- Choosing Exa filters (domains, dates, categories)
- Poor Exa results and needing better query phrasing
- Whether to use Exa vs keyword search (Google/Serper/Tavily)

## Safety and boundaries

**Do not** ask for or echo `EXA_API_KEY` or other secrets.

**Do not** claim live web results — this skill only plans queries; execution happens elsewhere.

**Do not** instruct bypassing paywalls, scraping behind logins, or violating site terms.

**Rate/cost awareness:** Note that `type: deep` and high `numResults` cost more; recommend conservative defaults unless the user needs exhaustive coverage.

## Required inputs

Ask only what’s missing:

1. **Research goal** — one sentence (what decision or answer depends on this search).
2. **Entity type** — company, person, product, paper, news event, code/library, policy, or mixed.
3. **Freshness** — breaking (24h), recent (30d), evergreen, or historical range.
4. **Trusted sources** (optional) — domains to prefer or block (e.g. `arxiv.org`, `github.com`, exclude `pinterest.com`).
5. **Depth** — quick scan (3–5 results) vs thorough (10–20).
6. **Downstream** — human summary, agent context, or citation list.

## Workflow

1. Restate the goal and recommend **Exa vs keyword search** (see decision rubric).
2. If Exa: draft the plan using **Output format**.
3. Include **2–3 fallback queries** (broader/narrower/different category).
4. Flag **stop conditions** — when results are likely sufficient or when to switch provider.

## Exa vs keyword — decision rubric

| Prefer **Exa neural** | Prefer **keyword / Serper** |
|----------------------|----------------------------|
| Fuzzy concept discovery (“alternatives to X for Y”) | Exact error string or CVE ID |
| Finding similar pages to a URL | Known official docs URL |
| Research synthesis across sources | Site: operator style lookup |
| Company/person landscape | Single definitive fact (price, date) |

When unsure, plan **one Exa neural query + one keyword fallback**.

## Output format

Return markdown:

### Exa search plan — {short goal}

| Field | Value |
|-------|-------|
| Recommended | Exa neural / keyword / both |
| Category | `company` \| `research paper` \| `news` \| `github` \| `pdf` \| `tweet` \| auto |
| numResults | 5–20 |
| Freshness | date filter or “none” |

#### Primary query

Natural-language query optimized for Exa neural search (complete sentence, include context nouns, avoid boolean operators).

#### API hints (for executor skill)

```yaml
type: neural          # or auto / keyword if noted
useAutoprompt: true   # default true for vague goals
category: <category>  # if applicable
includeDomains: []    # optional
excludeDomains: []    # optional
startPublishedDate:   # ISO or null
endPublishedDate:     # ISO or null
```

#### Fallback queries

1. Broader variant
2. Narrower variant (domain- or category-locked)
3. Keyword-style variant (if neural underperforms)

#### Quality checks after execution

- [ ] Top 3 results match entity type
- [ ] Publication dates fit freshness requirement
- [ ] No duplicate domains dominating results
- [ ] Snippets contain answer-bearing text (not nav pages)

#### Stop / escalate

When to stop searching vs try fallback vs switch to Tavily/Serper.

## Quality bar

- **Queries are sentences**, not keyword bags — e.g. “Startup companies building on-chain identity verification for EU enterprises” not `on-chain identity EU`.
- **Category matches entity** — don’t use `github` for legal news.
- **Filters are justified** — every `includeDomains` entry ties to the goal.
- **Executor-ready** — another skill can copy the YAML block without reinterpretation.

## Examples

**Good primary query:** “Peer-reviewed research on retrieval-augmented generation evaluation metrics published after 2024.”

**Bad primary query:** “RAG eval metrics 2024.”

**Good excludeDomains:** `pinterest.com, quora.com` when researching B2B SaaS pricing.

**Bad excludeDomains:** Blocking all blogs when the goal is practitioner guides.
