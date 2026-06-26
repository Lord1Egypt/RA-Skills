# Audience Architecture Output Template

## Section 1: Current State Audit

### Active Audiences Inventory

| Platform | Campaign | Audience Type | Size | 30d Spend | ROAS | CPM | Frequency | Created | Status |
|----------|----------|--------------|------|-----------|------|-----|-----------|---------|--------|
| Meta | [name] | [interest/LAL/retargeting] | [n] | $[x] | [x]x | $[x] | [x]/wk | [date] | [active/decay/paused] |
| TikTok | [name] | [interest/LAL/retargeting] | [n] | $[x] | [x]x | $[x] | [x]/wk | [date] | [active/decay/paused] |
| Google | [name] | [search/shopping/display/PMax] | [n] | $[x] | [x]x | $[x] | [x]/wk | [date] | [active/decay/paused] |

### Decay Flags
- [ ] Audiences with frequency >8/week: [list]
- [ ] Audiences with ROAS below break-even ([x]x): [list]
- [ ] Audiences unchanged for 90+ days: [list]
- [ ] Customer match lists last refreshed: [date per platform]

---

## Section 2: Customer Segmentation

### Tier Summary

| Tier | Definition | Count | Avg AOV | Repeat Rate | Top Categories | Seed Quality |
|------|-----------|-------|---------|-------------|----------------|-------------|
| T1 — High-LTV Repeaters | 3+ orders OR top 20% revenue, <20% returns | [n] | $[x] | [x]% | [cats] | Premium |
| T2 — Recent Single | 1 order in 90d, AOV > median | [n] | $[x] | N/A | [cats] | Good |
| T3 — Lapsed | Last order 180+ days | [n] | $[x] | [x]% | [cats] | Retarget only |
| T4 — Discount-Only | Sale purchases only, sub-median AOV | [n] | $[x] | [x]% | [cats] | Exclude |

### Seed Readiness
- Tier 1 count vs. recommended 1,000–5,000: [assessment]
- Data fields available: [email / phone / MAID / all three]
- Match rate expectations: Meta [x]%, Google [x]%, TikTok [x]%

---

## Section 3: Prospecting Audiences

### Meta Prospecting

| Audience | Type | Seed/Source | Expected Reach | Daily Budget | Expected CPM |
|----------|------|------------|----------------|-------------|-------------|
| [name] | LAL 1% | Tier 1 | [n]M | $[x] | $[x] |
| [name] | LAL 3% | Tier 1 | [n]M | $[x] | $[x] |
| [name] | Interest Stack | [interests with AND] | [n]M | $[x] | $[x] |
| [name] | Broad / Advantage+ | None | [n]M | $[x] | $[x] |

### TikTok Prospecting

| Audience | Type | Source | Expected Reach | Daily Budget | Expected CPM |
|----------|------|--------|----------------|-------------|-------------|
| [name] | LAL | Tier 1 upload | [n]M | $[x] | $[x] |
| [name] | Interest | [content vertical] | [n]M | $[x] | $[x] |
| [name] | Smart+ | Automated | [n]M | $[x] | $[x] |

### Google Prospecting

| Audience | Type | Source | Expected Reach | Daily Budget | Expected CPM |
|----------|------|--------|----------------|-------------|-------------|
| [name] | Customer Match Signal | Tier 1+2 | [n]M | $[x] | $[x] |
| [name] | In-Market | [segments] | [n]M | $[x] | $[x] |
| [name] | PMax w/ Signals | Combined | [n]M | $[x] | $[x] |
| [name] | YouTube Remarketing | Channel engagement | [n]K | $[x] | $[x] |

---

## Section 4: Retargeting Funnel

| Segment | Window | Signal | Platform(s) | Daily Budget | Creative Type | Offer |
|---------|--------|--------|------------|-------------|--------------|-------|
| Hot | 0–7d | ATC / Checkout | Meta, Google, TikTok | $[x] | Dynamic product | [none/free ship/discount] |
| Warm | 7–30d | Product view 2x+, Ad engage | Meta, Google | $[x] | Collection showcase | [none/free ship] |
| Cool | 30–90d | Site visit, Email sub | Google, Meta | $[x] | Brand story | None |
| Lapsed | 90–180d | Past purchaser (non-T1) | Email + Meta | $[x] | Win-back | [discount] |

---

## Section 5: Exclusion Matrix

| Campaign Type | Excludes |
|--------------|----------|
| Prospecting (all platforms) | All purchasers (lifetime) + ATC 30d + all retargeting audiences |
| Warm retargeting | Purchasers 30d + hot retargeting audiences |
| Hot retargeting | Purchasers 7d |
| Cross-platform suppression | [CDP/manual sync method and frequency] |

---

## Section 6: Budget Allocation

### Funnel Stage Budget

| Stage | % of Total | Monthly Budget | Primary Platform |
|-------|-----------|---------------|-----------------|
| Cold Prospecting | [x]% | $[x] | [platform] |
| Warm Retargeting | [x]% | $[x] | [platform] |
| Hot Retargeting | [x]% | $[x] | [platform] |
| Reactivation | [x]% | $[x] | [platform] |
| Incrementality Holdout | [x]% | $[x] | — |

### Frequency Caps

| Stage | Cap | Measurement |
|-------|-----|-------------|
| Prospecting | [x] impressions/user/week | Per platform |
| Warm Retargeting | [x] impressions/user/week | Per platform |
| Hot Retargeting | [x] impressions/user/week | Per platform |
| Cross-Platform Total | [x] impressions/user/week | CDP-level |

### Refresh Schedule
- Retargeting seeds: [weekly/biweekly]
- Lookalike seeds: [monthly]
- Full architecture review: [quarterly]

---

## Section 7: Measurement Framework

### KPIs by Stage

| Stage | Primary KPI | Target | Secondary KPI |
|-------|-----------|--------|--------------|
| Prospecting | Cost per new customer | $[x] | Blended ROAS |
| Warm Retargeting | ROAS | [x]x | Frequency |
| Hot Retargeting | Conversion rate | [x]% | Revenue per impression |
| Reactivation | Reactivation rate | [x]% | Reactivated LTV |

### Fatigue Signals (2 of 3 triggers pause + rebuild)
- [ ] Frequency >8/week
- [ ] CTR decline >30% from baseline
- [ ] CPM increase >25% from baseline

### Incrementality Test Design
- Holdout: [x]% of retargeting budget
- Duration: [x] weeks
- Measurement: conversion lift vs. holdout group

---

## Section 8: Implementation Timeline

| Week | Action | Platform | Owner |
|------|--------|----------|-------|
| 1 | Customer file segmentation + upload | All | [name] |
| 1 | Exclusion lists configured | All | [name] |
| 2 | Prospecting audiences launched | Meta, TikTok | [name] |
| 2 | Retargeting funnels launched | Meta, Google | [name] |
| 3 | Google PMax + YouTube launched | Google | [name] |
| 3 | Incrementality holdout started | Meta | [name] |
| 4 | First performance review | All | [name] |
| 8 | Full architecture review + seed refresh | All | [name] |
