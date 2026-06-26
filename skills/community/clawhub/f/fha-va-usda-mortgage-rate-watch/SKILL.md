---
name: fha-va-usda-mortgage-rate-watch
description: Daily FHA, VA, and USDA government-backed mortgage rate monitoring, comparison, and newsletter-style summaries. Use when the user asks about current FHA mortgage rates, VA loan rates, USDA home loan rates, government-backed mortgage rate trends, first-time homebuyer rate options, daily rate updates, refinance rates for FHA/VA/USDA, or wants a rate watch summary or newsletter. Also triggers on questions about FHA vs VA vs USDA loan differences, rate eligibility, or mortgage rate history for these programs.
---

# FHA, VA & USDA Mortgage Rate Watch

Monitor and summarize daily government-backed mortgage rates across FHA, VA, and USDA loan programs.

## Safety & Disclaimers

- ✅ Fetch and summarize publicly available rate data
- ✅ Compare FHA, VA, and USDA rate trends
- ✅ Explain loan program differences and eligibility basics
- ✅ Generate rate watch summaries and newsletter-style reports
- ❌ **NEVER guarantee** specific rates or approval
- ❌ **NEVER recommend** a specific lender or loan product
- ❌ **NEVER provide** personalized mortgage advice
- ❌ **NEVER replace** a licensed loan officer or mortgage broker

> Mortgage rates depend on individual credit profiles, lender policies, and market conditions. Always verify rates with a licensed lender. Data sourced from public aggregators and may lag real-time pricing.

## Rate Data Sources

Fetch current rates via web search or these public sources:

| Source | URL | Notes |
|--------|-----|-------|
| Freddie Mac PMMS | freddiemac.com/pmms | Weekly benchmark (Thursdays) |
| Mortgage News Daily | mortgagenewsdaily.com | Near-real-time daily rates |
| Bankrate | bankrate.com/mortgages | Daily averages by loan type |
| NerdWallet | nerdwallet.com/mortgages/mortgage-rates | Daily comparison |
| HUD/FHA | hud.gov | FHA program details |
| VA.gov | va.gov/housing-assistance/home-loans | VA loan eligibility |
| USDA RD | rd.usda.gov | USDA loan areas and eligibility |

When fetching rates, search for today's date + loan type (e.g., "FHA 30 year fixed rate today April 2026").

## Loan Program Quick Reference

For detailed eligibility rules, MIP/funding fee structures, and program comparisons, see [references/loan-programs.md](references/loan-programs.md).

| Program | Min Down | Credit Floor | Key Feature |
|---------|----------|-------------|-------------|
| **FHA** | 3.5% | 580 (3.5% down) | MIP required; first-time buyer friendly |
| **VA** | 0% | No VA minimum | Funding fee; military/veteran only |
| **USDA** | 0% | 640 typical | Guarantee fee; rural/suburban areas |

## Core Workflows

### 1. Daily Rate Summary

Fetch today's rates and format:

```
📊 Rate Watch — [DATE]

FHA 30-Year Fixed: X.XX% (▲/▼ X.XXpp from last week)
VA 30-Year Fixed:  X.XX% (▲/▼ X.XXpp)
USDA 30-Year Fixed: X.XX% (▲/▼ X.XXpp)

Conventional 30-Yr (for comparison): X.XX%

🔍 Commentary:
[1-2 sentences on trend direction and what's driving it]

Sources: [list sources checked]
⚠️ Rates are national averages. Your rate depends on credit, lender, and loan details.
```

### 2. Rate Comparison Table

When comparing across programs or timeframes:

```
| Loan Type | Rate | APR | Monthly P&I ($250K) |
|-----------|------|-----|---------------------|
| FHA 30-yr | X.XX% | X.XX% | $X,XXX |
| VA 30-yr  | X.XX% | X.XX% | $X,XXX |
| USDA 30-yr | X.XX% | X.XX% | $X,XXX |
| Conv 30-yr | X.XX% | X.XX% | $X,XXX |
```

Include MIP/funding fee impact in APR when available.

### 3. Payment Impact Calculator

Use the standard amortization formula:

```
M = P × [r(1+r)^n] / [(1+r)^n – 1]

P = loan amount, r = monthly rate, n = total months
```

Show how rate changes affect monthly payment:

```
Per 0.25% rate change on $300,000 loan:
  → ~$45/month difference
  → ~$16,200 over 30 years
```

### 4. Newsletter-Style Summary

For weekly or subscriber-style output, see the template in [references/newsletter-template.md](references/newsletter-template.md).

### 5. Rate Alerts via Cron

Set up recurring rate checks:

```
"Check FHA/VA/USDA rates every weekday morning and send a summary"
"Alert me if FHA 30-year drops below 6%"
```

Use cron jobs for scheduled delivery. Store last-known rates in `memory/rate-watch-state.json` to calculate deltas.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/payment_calc.py` | Calculate monthly P&I for given rate, amount, and term |

## References

| File | Contents |
|------|----------|
| [references/loan-programs.md](references/loan-programs.md) | FHA, VA, USDA eligibility, fees, and program details |
| [references/newsletter-template.md](references/newsletter-template.md) | Weekly newsletter template with formatting guidance |
