---
name: biz-analysis-narrator
description: Turn financial and operating spreadsheets into judgment-rich narratives for management — variance attribution (price vs. volume), trend interpretation, three-line risk warnings, and action recommendations with owners and verification metrics.
version: 1.0.0
author: RAY
license: CC-BY-4.0
tags: [finance, business-analysis, management-reporting, data-storytelling, kpi]
pricing:
  free: Free — 1 single-sheet read/month
  pro: $29/month — multi-sheet attribution + board-pack mode
  annual: $290/year
  pay_per_use: $19 one-time (deep read)
  enterprise: $199/month (enterprise templates + dashboard copy)
tiers:
  - id: free
    name: Free
    price: Free
    quota: Free — 1 single-sheet read/month
  - id: pro
    name: Pro Monthly
    price: $29/month — multi-sheet attribution + board-pack mode
    quota: unlimited
  - id: annual
    name: Pro Annual
    price: $290/year
    quota: unlimited
  - id: enterprise
    name: Enterprise
    price: $199/month (enterprise templates + dashboard copy)
    quota: team unlimited
monetization:
  model: freemium_subscription
  currency: USD
  paywall_trigger: free quota exhausted
  trial_days: 7
  free_trial: true
  upgrade_path: Pro Monthly -> Pro Annual -> Enterprise

---
# Business Analysis Narrator

## What problem it solves

Executives can read a spreadsheet; they can't read what the spreadsheet **means**. Finance and ops burn 10+ hours a month copying numbers into slides and still can't write the "why" and the "so what". This pack turns tables into **reports with judgment**.

## Input

Any format: P&L, sales ledger, ERP export, even screenshots. Minimum: two periods (MoM) or one period + budget (attainment).

## Narrative framework (four questions)

1. **What happened?** — revenue / cost / profit in three lines, each with absolute value + delta + attainment.
2. **Why?** — variance attribution in three moves:
   - Price vs. volume decomposition (revenue change = units factor + price factor)
   - Mix shift (which product / channel / customer moved)
   - One-off stripping (don't let a promo or a lawsuit settlement pollute the trend)
3. **Where's the risk?** — three warning lines: cash runway < 3 months, single-customer concentration > 30%, fixed-cost share jumping MoM.
4. **So what?** — 2–3 executable recommendations, each tagged with expected impact + owner role + verification metric.

## Output spec

- **One-page summary** (for the boss): 5 sentences + 3 numbers + 1 decision request.
- **Full report** (for finance/ops): chart suggestions (each chart gets a one-liner "what to look at here"), detail annexes.
- Neutral tone, explicit judgment: "This channel's ROI has been under 0.8 for two consecutive months; recommend contracting" — not "could be better".

## Boundaries

Recommendations are labeled "for decision reference"; on detecting internal contradictions (revenue diverging hard from cash), state it plainly rather than smooth it over.
