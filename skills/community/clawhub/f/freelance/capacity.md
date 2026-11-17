# Capacity — Utilization, Overbooking, and Time Off

Scope: how much can actually be sold, how a week is shaped, and how to take holiday and sick leave in a business with no HR. General scheduling technique is `time-management`; the growth decision behind a capacity ceiling is `scaling.md`.

**Before advising**, read `## Capacity` and `## Engagements` (committed hours per engagement) in `~/Clawic/data/freelance/memory.md`, plus `billable_hours_per_year` in `config.yaml` and the last three months of `income/<year>.md`. Capacity advice given without the trailing utilization is a guess.

**Contents:** [The Real Year](#the-real-year) · [Utilization](#utilization) · [The Week Shape](#the-week-shape) · [Committing Capacity](#committing-capacity) · [Overbooking](#overbooking) · [Saying No](#saying-no) · [Funded Time Off](#funded-time-off) · [Sickness and Emergencies](#sickness-and-emergencies) · [Parental Leave](#parental-leave) · [Burnout Signals](#burnout-signals) · [Part-Time and Reduced Capacity](#part-time-and-reduced-capacity)

## The Real Year

```
weeks available   = 52 − holiday weeks − public holidays − sick allowance − training
hours worked      = weeks available × hours per week
billable hours    = hours worked × utilization
```

Worked: 52 − 5 holiday − 2 in public holidays − 1 sick − 1 training = **43 weeks** × 40 h = 1,720 worked hours × 60% = **1,032 billable**. That is the honest number behind the 1,100-1,400 band, and it is why the rate floor divides by roughly 1,200 rather than 2,080 (SKILL.md Rules 1 and 2).

The unbillable 40% is not waste — it is selling, proposals, invoicing, admin, tax, learning, and the gaps between engagements. It is the business, and the rate is what funds it.

## Utilization

`utilization = billable hours ÷ hours worked`, computed monthly from `income/<year>.md`.

| Band | Reading | Action |
|---|---|---|
| <40% | Not enough work, or too much unbilled overhead | Separate the two before acting: a selling problem is `pipeline.md`, an admin problem is automation or an accountant |
| 50-65% | Healthy for a solo practice | Hold; this is the band the rate assumes |
| 65-75% | Running hot | Selling is being squeezed; check pipeline coverage this week |
| >75% sustained | No selling is happening at all | The cliff is one engagement away; raise the rate rather than the hours (`rates.md`) |

Agencies target 70-80% for billable staff because someone else does the selling, the invoicing and the admin. A solo practice copying that number is copying a structure it does not have.

**Effective rate is the honest companion metric**: `collected ÷ all hours worked`. A high day rate with 35% utilization pays less than a moderate one at 60%, and only this number shows it.

## The Week Shape

- **Batch the unbillable.** One fixed half-day for selling, invoicing and admin beats an hour scattered daily; scattered admin consumes the deep-work blocks that are the actual product.
- **Protect two multi-hour blocks a day** for the work being paid for. Client calls fragment the day worse than their duration suggests.
- **Keep one day unsold** at 3-4 sold days per week. It absorbs overruns, urgent client requests and the selling hour, and it is the difference between a normal week and a weekend of catch-up.
- **Publish your hours** and answer inside them. Availability that expands to fill the client's anxiety cannot be reclaimed later without a conversation.
- **One context per day where possible.** Two clients in a day costs a switching tax that nobody bills for.

## Committing Capacity

- Express commitments in the same unit as the engagement: days per week, hours per month, or milestone dates. Record it in the `Committed` column of `## Engagements` — it is what makes the next "can you take this" answerable in seconds.
- **Never commit above 80% of sellable capacity.** The remaining 20% covers overruns and the urgent request from the best client, which always arrives.
- **Retainers reserve capacity, and reserving is the service.** A retainer client who used none of their hours still bought the reservation — which is exactly what the contract should say (`rates.md`).
- **Sequence, do not parallelize**, where the client allows it. Two half-speed projects finish later than two sequential ones and double the coordination.
- **Lead time is a real quote input**: "the next start is in three weeks" is information the client needs and a signal of demand. Never invent availability that requires a weekend.

## Overbooking

The failure mode of a good quarter. When it happens, in order:

1. **Tell the affected client immediately**, with a new date. A revised date given early costs goodwill; a missed date given late costs the client.
2. **Renegotiate scope before renegotiating time** — cutting the third deliverable often saves the date.
3. **Subcontract only work you can specify and review**, and only with margin (`scaling.md`). Subcontracting a rescue with no margin buys a second problem.
4. **Buy time with a partial delivery** where the client's real deadline is one piece of the whole.
5. **Refund or reschedule rather than deliver badly.** One late delivery is recoverable; one bad delivery ends the referral chain.
6. **Never absorb it in unpaid weekends** as a standing solution. It hides the pricing signal — sustained overbooking means the rate is too low (`rates.md`, Rule 6).

## Saying No

Declining is a capacity instrument, and it needs a script so it happens fast.

- **Decline in one message**: no availability (or no fit), a date when that changes, and a referral to someone who can do it. Three lines, no apology paragraph.
- **Refer generously**. Referrals out are the most reliable source of referrals in, and they cost nothing when the calendar is full.
- **The waitlist**: for good clients, offer a start date instead of a no. A dated queue converts refusals into pipeline.
- **Price instead of declining** when the answer is "only if it were worth disrupting the schedule": quote the rush or displacement premium and let the number decide. It is not rudeness — it is the correct price for displacing booked work.
- **Never say yes conditionally to a bad fit.** "Maybe next month" for work you do not want returns next month, and by then you are the person who said maybe.

## Funded Time Off

Freelancers take dramatically less holiday than employees, and the cause is always the same: it was never priced or funded.

- **Price it into the rate.** The floor already assumes only ~43 working weeks; a rate derived from 52 has silently priced the holiday at zero (→ The Real Year).
- **Fund it**: holiday days × day rate into the holiday sinking fund monthly (`cashflow.md`).
- **Book it in the calendar first**, then sell around it. Holiday that waits for a quiet period never happens — the quiet period arrives unannounced and gets spent worrying about the pipeline.
- **Tell clients weeks ahead** and put the dates in the contract for retainers. A retainer client discovering your absence on the Monday is a relationship problem; one told in advance simply plans around it.
- **Cover, not availability.** Either agree that nothing runs while you are away, or arrange a named substitute and say what they will and will not do. "Reachable for emergencies" means a working holiday for the price of a real one.
- Put planned time off in `## Due` and in `## Capacity`, so quoting does not accidentally sell those weeks.

## Sickness and Emergencies

- **A sick-day fund is the minimum**: 5-10 days a year at the day rate, held separately (`cashflow.md`).
- **Income protection insurance** covers the longer case — a monthly benefit after a waiting period. Worth pricing once you have dependents, a mortgage, or a practice that cannot survive a quiet quarter (`insurance.md`).
- **Have a two-line contingency written before you need it**: who tells the clients, what the substitute can access, and which deadlines can move. Nobody writes this with a fever.
- **Force majeure and illness in the contract**: a clause allowing dates to move for illness, with notice, converts a crisis into an administrative message (`contracts.md`).
- **Do not deliver while ill and then apologize for the quality.** Move the date; a moved date is normal, and a bad deliverable is remembered.

## Parental Leave

- **Statutory support for the self-employed varies enormously** — from a genuine paid allowance in some countries to nothing at all in others, and eligibility often depends on contributions made months or years earlier. Check the rules for `tax_jurisdiction` well before it is relevant, because the contribution history is the part that cannot be fixed retroactively.
- **Plan the runway as a project**: months of no income plus continuing business costs, funded from the buffer plus a dedicated sinking fund.
- **Retainer clients are the best structure to enter it with** — predictable, pausable, and easier to resume than a project pipeline started from zero.
- **Tell clients early and give a return date**, even an approximate one. The alternative is that they replace you permanently rather than temporarily.

## Burnout Signals

Observable, not emotional. Two or more together means capacity is the problem, not motivation.

| Signal | What it indicates |
|---|---|
| Utilization above 75% for two consecutive months | No slack, no selling, no recovery |
| Working weekends in three of the last four weeks | The commitment level exceeds the sellable week |
| Zero holiday days taken in the last 6 months | Unfunded or unbooked time off |
| Dreading a specific client's messages | A relationship or scope problem masquerading as workload (`clients`) |
| Quality complaints appearing where there were none | The capacity ceiling reached the deliverable |
| Deferring invoicing, tax or admin repeatedly | The unbillable half is not batched, and it is compounding |

The response is capacity or price, never willpower: raise the rate and sell fewer hours (`rates.md`), or change what is sold (`scaling.md`).

**After any capacity work**, update `## Capacity` in `~/Clawic/data/freelance/memory.md` (days sold per week, trailing utilization, holiday taken and planned) and the `Committed` column of the engagement rows. **Planned time off, a holiday period, or a return-to-work date** becomes a dated row in `## Due` so no quote sells those weeks. **Hours worked and billable hours** go into the month row in `income/<year>.md` — without both columns, utilization and effective rate cannot be computed at all.
