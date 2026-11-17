# Finance — The CEO's Version

Enough finance to allocate capital, defend a plan, and never be surprised by your own bank balance. Detailed modeling, the monthly close, forecast mechanics, and dilution math belong to `cfo`; what follows is what the CEO must be able to compute in their head and defend in a board meeting.

Contents: [Runway and the Zones](#runway-and-the-zones) · [Default Alive](#default-alive) · [Capital Allocation](#capital-allocation--the-actual-job) · [Unit Economics](#unit-economics) · [Scenarios](#scenarios) · [Valuation, Honestly](#valuation-honestly) · [Emergency Levers](#emergency-levers) · [Financial Governance](#financial-governance)

## Runway and the Zones

```
Runway (months) = Cash balance / Net monthly burn
Net burn        = Cash operating expenses − cash collected (not revenue booked)
```

Collections, not bookings. A plan built on invoiced revenue with 60-day payment terms is a plan that runs out of cash two months before the spreadsheet says so.

This table is the single canonical home for the runway bands. Bands do not overlap; nothing else in the skill re-labels them. `runway_alarm_months` (default 12) is the top of the Start The Raise band — the month count at which cash becomes priority one.

| Runway (months) | Zone | Action |
|--------|--------|--------|
| ≥18 | Comfortable | Execute the plan; opportunistic raise only if the market is hot |
| 12-17 | Start the raise (`runway_alarm_months`, default 12) | Cash becomes priority one: begin investor conversations — a round runs 3-6 months end to end, close included (SKILL.md rule 4) |
| 9-11 | Parallel paths | Raise and cut planning run at once; decide the cut trigger date now. 9 months is the hard floor to *start* a round |
| 6-8 | Urgent | Close a round, or cut to milestone + 6 months of runway (SKILL.md rule 5); below 9 you are negotiating from weakness |
| <6 | Crisis | Emergency levers, bridge, or wind-down decision while cash remains (→ SKILL.md Quick Reference: crisis, shutdown) |

Three burn numbers, all useful: **gross burn** (total cash out — the worst case if revenue stops), **net burn** (gross minus collections — the planning number), and **adjusted burn** (net burn with committed changes applied — the number to use for any decision about the future).

## Default Alive

Graham's test: at your current growth rate and burn, does revenue cross expenses before cash hits zero? Compute it with today's growth rate, not the plan's. Two consequences:

- Default dead means every plan is a fundraising plan whether or not it says so; put that in the board materials rather than presenting a plan that quietly depends on capital nobody has committed.
- Default alive is an option, not a destination: it means you can choose to raise rather than needing to, which is the only condition under which terms are good (→ SKILL.md Quick Reference: fundraising).

## Capital Allocation — The Actual Job

The CEO's finance job is deciding where the next marginal dollar goes. Compare every candidate on the same three axes: payback period in months, what it does to the strategic bet, and reversibility if it fails.

- Fund things whose payback fits inside your runway. A 24-month payback with 14 months of cash is a bet on the next round, not an investment.
- Sales and marketing spend is only scalable when CAC payback holds at scale — the first cohort's efficiency does not survive a 3x budget increase, so step it up in increments and re-measure.
- Headcount is the least reversible allocation you make: it is a multi-year commitment with a severance tail (→ SKILL.md Quick Reference: layoffs). Contractors and agencies cost more per unit and are worth it while the need is unproven.
- Say no in a way that survives: "not this quarter, and here is what would have to be true" beats an unexplained rejection that comes back monthly.

## Unit Economics

| Metric | Formula | Convention |
|--------|---------|-----------|
| CAC | Fully loaded sales + marketing spend / new customers, same period | Include salaries and tooling, not just ad spend |
| LTV | ARPA × gross margin % × average lifetime (1 / churn rate) | Break it out by segment or it means nothing |
| LTV:CAC | LTV / CAC | 3:1 is the usual health line; well above it usually means underinvestment, not excellence |
| CAC payback | CAC / (monthly ARPA × gross margin %) | Under 12 months for SMB, under 18-24 tolerated in enterprise |
| Gross margin | (Revenue − COGS) / Revenue | 70%+ for software; below that, growth costs cash |
| Burn multiple | Net burn / net new ARR (Sacks) | Under 1 is excellent, 1-2 is workable, above 2 means growth is being bought |
| Rule of 40 | Growth rate % + profit margin % | A late-stage screen; misleading below Series B |

Worked payback example: CAC 12,000; ARPA 1,000/month; gross margin 75% → 12,000 / 750 = 16 months. With 14 months of runway, that channel cannot be scaled with your own cash — it is a use of the next round, and should be presented that way.

## Scenarios

Build three, always with the same structure, and define the bear case before you need it:

| Scenario | Assumptions | Used for |
|----------|-------------|----------|
| Base | Current trajectory, closed pipeline only | The plan you commit to the board |
| Bull | Key metrics improve 20-30% | Where you would deploy upside, decided in advance |
| Bear | Revenue flat, nothing unsigned closes, one large customer leaves | Cut sizing (SKILL.md rule 5) and covenant headroom |

The bear case is not "20% worse". It is the specific set of things that plausibly go wrong together, because they correlate: a bad quarter, a churned top account, and a closed funding market arrive in the same year for the same reason.

Every scenario names its **trigger and its action**: "if Q2 bookings are under X by June 30, we execute the cut on July 15." Scenarios without triggers are documents; scenarios with triggers are decisions already made calmly (→ SKILL.md Quick Reference: decisions).

## Valuation, Honestly

Revenue multiples are convention that swings with the funding cycle — the same company was worth two to three times more at the 2021 peak than in the 2023 trough. Use these as a sanity check only, and pull live comparables before anchoring anything on them.

| Stage | Rule-of-thumb ARR multiple | What moves it |
|-------|---------------------------|---------------|
| Seed | ~10-20× | Team, market, narrative — largely not the multiple, it is priced on ownership targets |
| Series A | ~8-15× | Growth rate and retention |
| Series B | ~6-12× | Unit economics and evidence of a moat |
| Series C+ | ~5-10× | Efficiency and a path to profit |

Drivers in order of weight: growth rate, net revenue retention, gross margin, market size, and efficiency. Note the asymmetry founders miss — valuation is set by your ownership dilution target as often as by your metrics: an investor needing 20% at a 5M check produces a 25M post-money regardless of your model.

## Emergency Levers

| Lever | Cash effect visible | Cost |
|-------|---------------------|------|
| Freeze hiring and open reqs | Immediate | None; open reqs are committed cash nobody counts |
| Cut discretionary and vendor spend, renegotiate tooling | 1-30 days | Low; annual contracts are often renegotiable mid-term under threat of non-renewal |
| Collections push and payment terms | 15-45 days | Free money; a receivable is cash you already earned |
| Marketing and contractor reductions | 30 days | Pipeline in 1-2 quarters |
| Founder and exec comp deferral | 30 days | Symbolically large, financially small; use it for signal, not for runway |
| Layoffs | 30-60 days, net of severance | Highest impact, one-way door (→ SKILL.md Quick Reference: layoffs) |
| Sale-leaseback, venture debt, factoring | 30-90 days | Adds covenants and priority ahead of equity |
| Killing a product line | 90 days | Frees engineering and support; usually overdue |

Order them by cash-per-unit-of-damage, and pull the cheap ones before you touch people. But do not spend three months on small levers to avoid a cut that arithmetic already requires — that is how companies end up cutting twice.

## Financial Governance

- Weekly: cash balance and collections. Monthly: closed financials, plan variance, updated runway. Quarterly: reforecast the rest of the year, revisit hiring, refresh scenarios (→ SKILL.md Quick Reference: metrics).
- A variance over 10% on any major line gets an explanation and an owner, not a note.
- Two people on every payment above a threshold, and the CEO does not approve their own expenses. Dual control is the cheapest fraud prevention that exists (→ SKILL.md Quick Reference: governance).
- Know your bank concentration and your insured limits. Cash sitting in one uninsured account at one institution is a risk nobody thinks about until the week it matters.
