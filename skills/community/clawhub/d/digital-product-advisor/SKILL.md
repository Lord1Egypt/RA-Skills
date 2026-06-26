---
name: digital-product-advisor
description: "Use when helping a user choose consumer electronics products through source-aware market research, comparison, and recommendation. MVP focuses on Bluetooth earbuds."
version: 0.1.0
author: Jack + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [product-research, buying-guide, consumer-electronics, bluetooth-earbuds, shopping]
    related_skills: []
---

# Digital Product Advisor

## Overview

This skill helps an agent produce practical, source-aware buying recommendations for consumer electronics. The MVP focuses on Bluetooth earbuds / true wireless earbuds.

The core workflow is documentation-first: clarify the buying context, collect current market options, compare candidates using user-specific weights, and produce a clear recommendation report. Optional scripts can normalize inputs, validate candidate JSON, and calculate weighted scores, but the skill must remain useful without scripts.

## When to Use

Use this skill when the user asks for help choosing, comparing, shortlisting, or buying Bluetooth earbuds, especially when they mention:

- budget, currency, or price range
- country, region, marketplaces, or purchase channels
- specific brands to include or exclude
- use cases such as commuting, calls, music, gym, gaming, studying, or travel
- features such as ANC, transparency mode, mic quality, multipoint, low latency, codecs, or water resistance

Do not use this skill for:

- automatic checkout or purchasing
- medical/hearing-health claims
- investment-style price prediction
- non-earbud product categories unless clearly marked as out-of-MVP / lower-confidence

## MVP Scope

Supported category:

- Bluetooth earbuds / true wireless earbuds

Supported recommendation modes:

- open-market search
- brand-only comparison, e.g. "only Sony"
- brand-vs-brand comparison, e.g. "Bose vs Sony"
- budget-limited shortlist
- region/currency-specific recommendation

## Required Mindset

Do not produce a stale generic list. Product availability, discounts, and value change by region and date.

Always adapt recommendations to:

- user location / region
- currency
- budget
- brand scope
- phone ecosystem
- use case
- purchase channel
- must-have features
- deal breakers

## Clarification Workflow

Infer obvious parameters from the user's message. Ask at most 3 high-impact clarification questions if needed.

High-impact missing fields:

1. Budget and currency
2. Region / market / where they can buy
3. Main use case
4. Phone ecosystem
5. Brand scope if they imply brand preference

Examples of inference:

- "1000 RMB" implies currency CNY and likely China market.
- "JD" or "Tmall" implies China market and CNY.
- "Only Sony" means brand_scope.mode = include_only, include = ["Sony"].
- "Avoid Apple" means brand_scope.mode = exclude, exclude = ["Apple"].
- "iPhone" means Apple ecosystem; AirPods compatibility may matter.

If budget, region, and use case are all present, proceed without more questions.

## Parameter Model

See `references/parameters.md` for the canonical schema.

Minimum normalized request:

```json
{
  "product_category": "bluetooth_earbuds",
  "region": "China",
  "currency": "CNY",
  "budget": {"min": null, "max": 1000, "currency": "CNY"},
  "brand_scope": {"mode": "open_market", "include": [], "exclude": []},
  "marketplaces": ["JD", "Tmall", "official_store"],
  "use_case": ["commuting", "calls"],
  "phone_ecosystem": "Android",
  "must_have": ["ANC", "good_microphone"],
  "nice_to_have": [],
  "deal_breakers": [],
  "purchase_timeline": "this_week"
}
```

## Research Workflow

1. Normalize the user request.
2. Choose recommendation mode: open-market, include-only brand, exclude-brand, or brand-vs-brand.
3. Gather current candidates from the user's region and marketplace context.
4. For each candidate, collect price, availability, key specs, review signals, known issues, and product links.
5. Use at least three source categories when possible:
   - official/spec source
   - review/testing source
   - price/availability source
6. Remove candidates that violate hard constraints.
7. Score remaining candidates using user-specific weights.
8. Produce a scenario-based report with tradeoffs and confidence level.

## Bluetooth Earbuds Domain Guidance

Use `references/bluetooth-earbuds.md` for category-specific criteria.

Important dimensions:

- sound quality
- ANC / transparency
- call microphone quality
- comfort and fit
- battery life
- codec support
- latency
- multipoint
- app quality / EQ
- water resistance
- ecosystem fit
- reliability / known defects
- price-to-performance
- local warranty and availability

## Scoring

Use `references/scoring-framework.md`.

Scoring should be weighted by user intent. Do not present the weighted score as objective truth; it is a decision aid.

For commuting + calls, emphasize:

- ANC
- mic quality
- comfort
- battery
- value

For music-first, emphasize:

- sound quality
- comfort
- codec/EQ support
- reliability
- value

For gym use, emphasize:

- fit stability
- water resistance
- comfort
- battery
- replacement cost

## Report Format

Use `templates/report-template.md`.

Every final report should include:

1. one-line recommendation
2. user requirement summary
3. shortlist table
4. top picks by scenario
5. detailed tradeoffs
6. avoid / caution section if relevant
7. final recommendation
8. product links / where to buy
9. sources checked
10. confidence level

Product links should be included when available:

- Add marketplace product links in the shortlist table when the product can be bought online.
- Prefer official store, flagship store, or trusted marketplace listings over affiliate, ad, or random reseller links.
- If exact product-page links are blocked by anti-bot pages or unavailable, include a marketplace search link and label it clearly as a search link rather than a verified product page.
- Do not invent URLs. If no reliable link is available, write `Link unavailable` and explain why in sources or confidence notes.

## Markdown Export

The canonical export format is Markdown. When the user asks to export/save a report, save it as a `.md` file under one grouped folder for the category:

```text
reports/earbuds/
```

Use `references/export-policy.md` for title, metadata, filename, and path rules.

Default behavior:

1. Generate the report normally.
2. Create a meaningful H1 title using product category, region, budget/brand scope, and primary use case.
3. Save the file under `reports/earbuds/` unless the user gives another folder.
4. Use a readable lowercase hyphenated filename such as `YYYY-MM-DD-earbuds-china-under-1000-cny-commuting-calls.md`.
5. If the target file already exists, append `-v2`, `-v3`, etc. Do not overwrite unless requested.
6. Tell the user the exact saved path.

Example title:

```markdown
# Bluetooth Earbuds Buying Report: China, Under 1000 CNY, Commuting + Calls
```

Example path:

```text
reports/earbuds/2026-05-08-earbuds-china-under-1000-cny-commuting-calls.md
```

## Optional Scripts

Scripts live in `scripts/` and are optional.

Use scripts when available for:

- request normalization
- candidate data validation
- deterministic weighted scoring
- Markdown report path generation

Do not fail the task if scripts are unavailable. Continue manually using the Markdown workflow.

## Common Pitfalls

1. Treating global MSRP as local value. Always check region and currency.
2. Recommending products unavailable in the user's market.
3. Overweighting codec specs. Codec support matters only if the user's device supports it too.
4. Ignoring fit. Earbuds can be technically excellent and still bad for a user with fit constraints.
5. Trusting a single review source. Use multiple source categories.
6. Pretending scores are objective. Explain assumptions and tradeoffs.
7. Hardcoding stale rankings into the skill.
8. Comparing across brands when the user asked for a brand-only shortlist.

## Verification Checklist

Before final answer, verify:

- [ ] Budget, region, currency, and use case are known or explicitly assumed.
- [ ] Brand scope is respected.
- [ ] Candidate list matches availability region.
- [ ] Prices use the requested currency or clearly note conversion.
- [ ] Product links are included where available, or missing links are explicitly labeled.
- [ ] At least three source categories were considered when possible.
- [ ] Recommendation includes tradeoffs, not just a winner.
- [ ] Final report includes confidence level.
- [ ] Claims about subjective sound/fit are framed cautiously.
