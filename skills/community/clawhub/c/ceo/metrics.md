# Metrics — What the CEO Actually Watches

A CEO needs five numbers they can recite cold and defend under hostile questioning, plus the discipline to keep everyone using the same definitions. Everything else is a dashboard someone else owns.

## Pick The Model First

`business_model` (default b2b-saas) selects the row. Getting it wrong produces a dashboard that measures someone else's company.

| Business model | Primary health metric | The one that predicts it | Common vanity substitute |
|---|---|---|---|
| B2B SaaS | Net revenue retention | Logo retention by cohort, expansion rate | ARR growth with churn hidden inside |
| PLG / self-serve | Paid conversion of activated users | Activation rate (first value reached) | Signups |
| Marketplace | Liquidity: share of listings that transact in a window | Repeat rate on both sides | GMV |
| Consumer subscription | Retention at day 30/90/365 | Week-1 engagement depth | Downloads, MAU |
| Ecommerce / DTC | Contribution margin per order | Repeat purchase rate at 90 days | Revenue, ROAS alone |
| Services / agency | Utilization and realized rate | Pipeline coverage against booked capacity | Bookings |
| Hardware | Gross margin after warranty and returns | Sell-through, not sell-in | Units shipped |
| Anything pre-PMF | Retention curve shape (does any cohort flatten?) | Weekly customer conversations | Total users |

Default when unclear: the metric that, if it stalled for two quarters, would end the company. That is the one.

## The Five

Keep exactly five on the CEO page, unchanged for at least a year unless the model changes:

1. **Growth** — the revenue number for your model, monthly, with the rate not just the level.
2. **Retention** — cohort-based, at the interval that matters for your model.
3. **Cash** — balance, net burn, runway in months (canonical zones and math → SKILL.md Quick Reference: finance).
4. **Efficiency** — one ratio: burn multiple (net burn / net new ARR, Sacks), CAC payback in months, or contribution margin.
5. **The bet** — the single leading indicator of this year's strategic bet. It is the only one that changes with the plan.

Changing a metric mid-year requires the same ceremony as changing a priority: announce it, say why, and show both definitions side by side for a quarter.

## Definitions Discipline

Most metric arguments are definition arguments wearing a costume.

- Every metric has one written definition, one owner, and one query. Store them where the whole company can read them; contradictions found in a board meeting are the expensive version.
- The recurring disputes worth settling in writing: what counts in ARR (annualized monthly? contracted? does usage overage count? do month-to-month contracts?), whether churn is logo or revenue and gross or net, what makes a user "active", whether pipeline is created-date or close-date weighted, when revenue is recognized versus collected.
- Board metrics and internal metrics use the same definitions. Two sets of books, even innocent ones, is how a CEO ends up defending a number they did not know was different.
- Averages hide the business. Any metric that matters gets a distribution or a cohort split at least quarterly — an average sales cycle of 60 days can be two segments at 20 and 140.
- Instrument before you launch. Reconstructing a cohort from logs six months later costs a week and produces a number nobody trusts.

## Leading Versus Lagging

Revenue is lagging by the length of your sales cycle. If your cycle is 90 days, this quarter's revenue was decided last quarter, and managing it now is theater. Pair every lagging metric with the leading one you can still act on:

| Lagging | Leading, actionable now |
|---|---|
| Quarterly revenue | Qualified pipeline created this month, coverage ratio |
| Annual churn | Product usage decline in accounts, support ticket sentiment, exec-sponsor contact |
| Headcount plan attainment | Offer acceptance rate, time-to-first-onsite |
| NPS | Time-to-first-value for new customers |
| Burn | Committed spend and open reqs — both are cash already promised |

## Operating Cadence

| Rhythm | Who | Content |
|---|---|---|
| Weekly | Exec team, 30 min | The five, versus plan, exceptions only; anything off-plan gets an owner and a date |
| Monthly | Company | Same five at the all-hands (→ SKILL.md Quick Reference: communication); financials closed and reviewed with the finance owner |
| Quarterly | Board | The five plus the bet's progress, plan reforecast, one strategic question (→ SKILL.md Quick Reference: board) |
| Annually | Company | Reset the bet and the plan (→ SKILL.md Quick Reference: strategy) |

The weekly meeting reviews variance, not status. If the number is on plan, it takes ten seconds. A metric review where every number is explained at equal length teaches the team that reporting matters more than moving.

## Reading Numbers Like a CEO

- A number that moved and nobody can explain is a broken pipeline until proven otherwise. Verify the instrumentation before you build a story on it.
- Two consecutive months is noise; three is a trend; one month is an anecdote with a decimal point.
- When a metric improves right after you started watching it, check what stopped being counted.
- Ask for the denominator every time. Conversion "up 40%" on a traffic drop is not a win.
- Segment before you conclude. Total churn flat can mean your best segment is growing while your largest is collapsing.
- Benchmarks are for calibration, never targets. Copying a public company's target rate at your stage imports the wrong constraint; your own trajectory is the comparison that matters.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Adding metrics after every bad quarter | The page becomes 30 numbers and the org loses focus | Five on the CEO page; the rest live with their owners |
| Board metrics ≠ internal metrics | You get surprised by your own reporting | One definition set, one source |
| Chasing a metric you cannot act on | Motion without leverage | Every metric on the page has a lever and an owner |
| Rewarding on a single metric | It gets gamed within a quarter, reliably | Pair every incentive metric with a quality guardrail |
| Reporting bookings as revenue | Cash arrives later or not at all; the plan is fiction | Say which is which every time (→ SKILL.md Quick Reference: finance) |
