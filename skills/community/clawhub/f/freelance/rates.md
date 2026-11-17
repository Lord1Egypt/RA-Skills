# Rates — Pricing Your Own Labour

Scope: deriving the floor, choosing the basis, estimating fixed price, and raising the number. Pricing a product or a packaged offer that is not your time is `pricing`.

**Before quoting anything**, read `## Rates` and `## Win/Loss` in `~/Clawic/data/freelance/memory.md` (or the files `## Boxes` points to), plus `rate_card_file` if `config.yaml` names one. A price quoted without the last ten outcomes is a guess with a decimal point.

**Contents:** [The Floor](#the-floor) · [What the Floor Is Not](#what-the-floor-is-not) · [Choosing the Basis](#choosing-the-basis) · [Fixed-Price Estimation](#fixed-price-estimation) · [Rate Card Structure](#rate-card-structure) · [Finding the Market Number](#finding-the-market-number) · [Raising the Rate](#raising-the-rate) · [Discounts and Premiums](#discounts-and-premiums) · [Quoting Mechanics](#quoting-mechanics)

## The Floor

```
pre_tax_profit = target_income ÷ (1 − tax_setaside_pct)
billings       = pre_tax_profit + business_costs_per_year
floor_hourly   = billings ÷ billable_hours_per_year
floor_daily    = floor_hourly × billable_hours_per_day        # 6, not 8 — see below
```

Worked, in the config's `currency`: take-home 60,000 · set-aside 32% · costs 9,000 · 1,150 billable hours →
`60,000 ÷ 0.68 = 88,235` → `+ 9,000 = 97,235` → `÷ 1,150 = 84.6/hour` → `× 6 = 507/day`. Round the daily figure, never the hourly one: rounding 84.6 up to 85 first adds 2.4 to the day rate and makes the floor unreproducible next time.

- **`billable_hours_per_day` is 6, not 8.** A day sold is a day of context switching, calls and handover; charging a day rate computed on 8 productive hours silently discounts every day by 25%.
- **The tax gross-up is not optional.** Dividing take-home by hours gives a number that cannot pay its own tax bill; the error is roughly the size of the set-aside.
- **Recompute whenever a term moves**: a new subscription, an insurance renewal, a change in utilization, a change in `target_income`. A floor derived a year ago and three tools ago is under the truth.
- The floor is the refusal line, not the asking price. The asking price is the market number (→ Finding the Market Number); when the market number is below the floor, the answer is a different market, a different trade, or fewer hours sold at a higher value — never a rate under the floor "to stay busy".

## What the Floor Is Not

| Confusion | Correction |
|---|---|
| The salary hourly | Salary hours were paid whether sold or not, and carried employer tax, holiday, sick pay, pension and equipment. The freelance equivalent typically lands 2-3× the salary hourly — arithmetic, not ambition |
| The client's budget | Their budget is a constraint on scope, not on your rate. Cut deliverables, keep the number |
| What competitors charge | Their costs, utilization and tax position are not yours. Use their number as market signal (→ Finding the Market Number), never as your floor |
| A number that "feels askable" | The feeling tracks the last salary, not the market. Every practice that raised rates found the feeling lagged reality by 6-18 months |

## Choosing the Basis

`engagement_basis` sets the default; this table is when to depart from it.

| Basis | Use when | Fails when | Guard |
|---|---|---|---|
| Hourly | Scope genuinely unknowable, or ongoing support with variable load | Punishes speed and experience; caps income at hours; clients audit the timesheet | Estimate range in writing, notify at 80% of the estimate |
| Daily | Work arrives in whole-day blocks, on-site or deep work | Half-days get requested and granted for free | Minimum engagement in days; half-day priced above half the day rate |
| Fixed | Deliverable is definable and the discovery is done | Every unpriced unknown is your loss | Contingency + change-order clause (→ Fixed-Price Estimation) |
| Retainer | Recurring need, and the client is buying availability | Turns into unlimited access | Define what is included as hours *or* as scope, plus a notice period and a carry-over rule (`clients` for the relationship side) |
| Value | The outcome maps to a number the client already tracks | Client will not share the number, or attribution is arguable | Requires a measurement agreed in writing before the work |

**Retainer carry-over is the clause everyone forgets**: unused hours either expire monthly (say so) or roll for one month (say so). Silence gets read as banking, and a client will eventually claim eight months of accumulated hours.

## Fixed-Price Estimation

1. **Decompose** to tasks of ≤1 day each. Anything left at "2 weeks" is not estimated, it is hoped.
2. **Three-point per task**: `expected = (optimistic + 4 × likely + pessimistic) ÷ 6`. The pessimistic case is what happens when the client's API is undocumented and the reviewer is on holiday.
3. **Add the invisible tasks** — kickoff, reviews, revisions within the contracted count, handover, deployment, the final round of "small" comments. Typically 20-30% of build time and almost always missing from the first draft.
4. **Contingency by discovery quality**: full discovery done and requirements signed → +15%; normal → +25%; new domain, new client, or an unmet dependency → +40%. Below 15% is not an estimate, it is a bid.
5. **Price against the floor**: `price = expected_hours × (1 + contingency) × target_rate`. If that price is unsellable, the scope shrinks — the contingency never does.
6. **Cap the risk in the contract**: a change-order clause, a revision count, and a named acceptance criterion per deliverable (`contracts.md`). Fixed price without these is unlimited liability paid at a fixed number.

Milestone the payment schedule to the same decomposition so unpaid exposure stays under two weeks of billings (SKILL.md Rule 8).

## Rate Card Structure

A written card, stored at `artifacts/rate-card.md` and pointed to by `rate_card_file`, removes the on-call arithmetic that produces discounts.

- Base rate on `engagement_basis`, plus the minimum engagement (below it, sell a fixed-price audit instead of an awkward half-day).
- **Rush premium** +25-50% for work inside a week's notice. It is not a penalty; it is the cost of displacing scheduled work.
- **Out-of-hours / weekend** +50-100%, named in advance so an emergency does not become a negotiation.
- **Travel** billed at half rate plus expenses, or a flat day, but never free — travel days cannot be sold twice.
- **Retainer discount** 0-10% against the equivalent day rate, and only in exchange for something real: notice period, guaranteed minimum, or scheduling priority. A discount for nothing teaches the client the list price was fiction.
- **Expiry**: every quote carries one (14-30 days). Without it, a quote from last year gets accepted at last year's number.

## Finding the Market Number

Rate benchmarks age fast and vary by country, trade, and buyer type. The reliable sources, in order:

1. **Your own win/loss log** — win rate against price is the only data with your name on it (→ Raising the Rate).
2. **Recruiters and agencies for the same skill**: ask what they bill and what they pay a contractor. The gap is 25-50% and tells you the direct-client ceiling.
3. **Peers in the same trade and country**, asked as a specific question ("what did you charge for the last engagement like this"), not as a survey.
4. **Marketplace rates**, adjusted: they are set by global supply and the take rate, and reading them as "the market" is the single most common cause of a floor-level rate (`platforms.md`).
5. **Published salary data ÷ 1,000** is a folk rule for a daily rate from an annual salary, and it is only a sanity check — it ignores your utilization, costs and tax position entirely.

## Raising the Rate

**The diagnostic**: 8 or more of the last 10 quotes accepted means the number is below market. A healthy loss rate for a specialist is 30-50%; losing nothing means selling below what buyers would pay.

**The maths** (SKILL.md Rule 6): raising by factor `k` holds revenue while the win rate stays above `old ÷ k`.

| Rise | Win rate that keeps revenue flat | Reading |
|---|---|---|
| +10% | 60% → 55% | Almost free; do it annually by default |
| +20% | 60% → 50% | Survives losing one deal in six |
| +50% | 60% → 40% | Requires better positioning, not just a bigger number |

Sequence: **new quotes first** (immediate, no relationship cost) → **new clients only** for a quarter, to gather evidence → **existing clients at renewal**, with 30-60 days written notice and a reason that is about the market or the scope, never about your costs. The conversation with an existing client, including the grandfathering decision, is `clients`.

Never raise mid-project, never raise as a reaction to a single bad month, and never announce a raise you will withdraw when the first client pushes back — that resets the anchor lower than where it started.

## Discounts and Premiums

| Situation | Do | Not |
|---|---|---|
| Client is over budget | Cut scope, extend timeline, or reduce the revision count | Cut the rate — it is permanent and it prices the next engagement too |
| Long engagement | Volume discount only against a commitment: minimum weeks, notice, or prepayment | A standing discount for a project that could end next month |
| Charity or a cause | Full price on the invoice, discount shown as a line item | An invisible discount; nobody values what has no price on it |
| Referral from an existing client | Referral fee to the referrer if agreed, never a discount to the new client | Starting the new relationship below list |
| Prepayment | 3-5% for paying the whole engagement up front is worth it — it removes DSO and default risk | More than ~5%, which is expensive financing |
| Difficult client, unclear scope, hostile paper | A risk premium of 20-50%, or a decline | Absorbing it quietly and resenting the project |

## Quoting Mechanics

- Quote a **number and a scope together**; a number alone gets negotiated, a scope alone gets expanded.
- Present **two or three options** (reduced / recommended / extended) rather than one price to accept or reject. It moves the conversation from "yes or no" to "which".
- Put the **price after the outcome**, never first, and never itemize hours in a fixed-price quote — an hourly breakdown invites an hourly negotiation.
- **Silence after sending is not a no.** One follow-up at the quote's midpoint, one at expiry; both add information rather than asking for a decision.
- Never quote in a live call under pressure. "I will send the number today" costs nothing and prevents the discount you will honour for two years.

**After every quote**, write a row to `## Win/Loss` in `~/Clawic/data/freelance/memory.md`: date, client, number, basis, scope size. **When it resolves**, complete the row with the outcome, the reason in the client's words, and the winner's price if it is known. **When a rate changes**, add a row to `## Rates` with the inputs the floor was computed from — never overwriting the previous rate — and refresh `artifacts/rate-card.md` in the same turn.
