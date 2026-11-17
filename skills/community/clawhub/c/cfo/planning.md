# Financial Planning and Forecasting

## Planning Rhythm

| Cadence | Activity |
|---------|----------|
| Weekly | 13-week cash update, AR/AP review |
| Monthly | Close, variance analysis, rolling forecast refresh, hiring plan vs actual |
| Quarterly | Board prep, scenario triggers reviewed, re-forecast |
| Annually | Budget, long-range plan, comp cycle, insurance and vendor renewals |

Model depth scales with stage: pre-seed needs one sheet with cash in, cash out, and hires; the driver model earns its keep at seed; scenario machinery and a long-range plan belong at Series A and beyond. A model more sophisticated than the decisions it informs is overhead with a spreadsheet's authority.

## Rolling Forecast

- Always 12–18 months ahead; refresh monthly. A static annual budget is wrong by February — keep the budget as the board contract and the rolling forecast as the truth, and report both.
- Split by horizon: near months (1–3) bottom-up from signed contracts and pipeline; far months driver-based. Mixing methods per line item is how forecasts go stale invisibly.
- Re-forecast when reality moves, not only when the calendar says so: a missed quarter, a funding event, a pricing change, or a hiring freeze each invalidate the old one. Version every refresh and keep the prior one — the board will ask what changed and when you knew.

## Driver-Based Modeling

Three to five drivers connect operations to money; more than that and nobody can falsify the model.

| Driver | Financial impact |
|--------|------------------|
| Sales reps | Revenue = ramped reps × quota × trailing attainment |
| Customers | Revenue, support cost, churn exposure |
| Engineers | Delivery capacity, payroll |
| Usage/servers | Infrastructure cost, gross margin |

- Use *trailing actual* attainment, never 100% of quota — planning at full quota is fantasy revenue with a spreadsheet's authority.
- Count only *ramped* reps: a rep hired in March produces little before summer; headcount ≠ capacity.
- Fully loaded headcount cost ≈ 1.25–1.4× base salary. Modeling raw salaries understates people cost by 20–29% of the true figure.
- Every driver needs a named owner outside finance who agrees with the number. A driver finance invented alone is an assumption nobody defends when it misses.

## Scenario Planning

| Scenario | Assumptions | Use |
|----------|-------------|-----|
| Best case | Everything works | Stretch targets, hiring ceiling |
| Base case | Realistic, some misses | Operating plan |
| Worst case | Key risks land | Contingency with triggers |

A scenario without a pre-committed trigger is a document, not a plan. Format: "If [metric] < [threshold] by [date], then [action]" — e.g. "If Q1 net-new ARR < 60% of plan by March 15, freeze hiring and cut discretionary spend." Agree on the trigger *now*, while everyone is calm; deciding during the miss guarantees a quarter of debate you can't afford.

Build the worst case around the one variable that actually moves the answer — usually new bookings or churn, rarely opex. State its sensitivity in a single sentence ("a 20% miss on new bookings moves the zero-cash date from March to December") and put that sentence in the board pack.

## Budget Process

Calendar-year timeline: September strategy → October department inputs → November consolidation and trade-offs → December board approval. Starting in November produces a top-down decree with bottom-up resentment. Shift the whole sequence when `fiscal_year_end` is not December.

- Run top-down targets and bottom-up builds in parallel, then reconcile — either alone fails (no strategy vs no reality).
- Budget headcount is not approved headcount: every role carries a start-date assumption and a trigger.
- Zero-base every 2–3 years, not annually (exhausting) and not never (bloat compounds unnoticed).
- The budget is a contract with the board; the rolling forecast is your operating truth. Confusing them creates either sandbagging or credibility loss.

## Variance Analysis

Explain every variance beyond materiality — set the policy once (e.g. ±5% or a fixed dollar floor, whichever is greater) so "significant" isn't renegotiated monthly.

```
Revenue: $950K actual vs $1M plan (-5%)
Cause: Deal slipped to next month (timing)
Impact: Recovers in Q2
Action: None
```

Categories: timing (will reverse) · volume (more/less activity) · rate (price/cost change) · mix (different products/segments). Invisible distinction: a "timing" variance that repeats two months running is a volume variance in denial — reclassify it and cut the forecast.

Favorable variances get the same scrutiny as unfavorable ones. Underspend against plan is usually a hire that never happened or a project that stalled: good for cash, bad for the plan that assumed the output.

## Key Metrics

| Metric | Formula | Read |
|--------|---------|------|
| Gross margin | (Revenue − COGS) ÷ Revenue | SaaS 70–80%+; below 70% caps your multiple |
| Burn multiple (Sacks) | Net burn ÷ net new ARR | <1.5 efficient; 1.5–2 acceptable; >2 fix before scaling spend |
| Magic number | Net new ARR (annualized) ÷ prior-quarter S&M | >0.75 scale GTM spend; <0.5 fix GTM first |
| CAC payback | CAC ÷ (monthly ARPA × gross margin) | <12 mo SMB; <18–24 mo enterprise |
| LTV:CAC | LTV ÷ CAC | >3x — but see caveat below |
| NDR | (Start ARR + expansion − churn) ÷ start ARR | >100% floor; 110–120% best-in-class |
| Rule of 40 | Growth % + FCF margin % | ≥40 healthy; trade growth for margin as you scale |

Caveat: LTV requires churn history young companies don't have — pre-Series A, LTV is extrapolated fiction; use CAC payback, which needs only months of data. Worked example: CAC $6K, ARPA $500/mo, 75% gross margin → payback = 6,000 ÷ (500 × 0.75) = 16 months — fine for enterprise, alarming for SMB.

Metric inputs must match the definitions in the one-page revenue recognition memo exactly; a term defined in two places will be reported two ways inside a quarter.

## When The Actuals Cannot Be Trusted

Forecasting on unreconciled books compounds the error with confidence. If the last close is incomplete or the bank does not tie:

1. Say so in the artifact, in one line, naming the period affected.
2. Forecast cash from the bank balance and known commitments — cash stays verifiable when the ledger is not.
3. Fix the close before refining the model. At that moment a controller is worth more than an FP&A hire.
