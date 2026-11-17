# Portfolio — Client Mix, Concentration, and Capacity

Scope: the questions that are about the whole book of clients rather than any one of them — who is too big, who is not worth keeping, whether there is room for one more, and what the year looks like. Individual renewals are `retention.md`.

Read `revenue/<year>.md`, `## Roster`, `## Pipeline` and `## Portfolio` in `~/Clawic/data/clients/memory.md` before answering any of these. Every number below is computed from the revenue log, never estimated from memory — recalled revenue is systematically wrong in the direction of whoever was most recently annoying.

**Contents:** [The Quarterly Review](#the-quarterly-review) · [Concentration](#concentration) · [Client Profitability](#client-profitability) · [Capacity](#capacity) · [Can I Take One More](#can-i-take-one-more) · [Forecasting Without Fiction](#forecasting-without-fiction) · [Pruning](#pruning) · [Client Mix](#client-mix)

## The Quarterly Review

Sixty minutes, on a date held in `## Due`, producing one row in `## Portfolio`.

| Step | Computed from |
|---|---|
| Revenue for the quarter, by client | `revenue/<year>.md` |
| Trailing-12-month share of the largest client | `revenue/<year>.md`, both years if the window spans them |
| Effective rate per client | Revenue ÷ all hours, including unbilled (`pricing.md`) |
| Unbilled hours per client | The `## Change Log` in each project file |
| DSO and anything past due | `## Receivables` (`getting-paid.md`) |
| Pipeline coverage for next quarter | `## Pipeline`, weighted |
| Renewals and end dates in the next 90 days | `## Due` and `## Roster` |
| Decision: keep, reprice, shrink, or replace, per client | All of the above |

The output is a decision per client, not a report. A review that ends without a changed rate, a dropped client, or a pipeline action was an hour spent admiring the data.

## Concentration

Share = **client revenue over the trailing 12 months ÷ total revenue over the same 12 months** (SKILL.md Rule 5).

| Share | What it means | Action |
|---|---|---|
| Under 20% | Losing them is a bad quarter | None |
| 20-30% | Losing them is a bad year | Watch it; keep the pipeline warm |
| Over `concentration_limit_pct` (default 30%) | A single decision by one person, who may leave, can halve your income | Standing risk item in `## Due`; pipeline effort goes here before anywhere else |
| Over 50% | Functionally an employer, without notice periods, severance, holiday or unemployment protection — and in some jurisdictions the arrangement invites an employment-status challenge for both sides | Replace revenue, not the client; do not exit before the replacement exists |

Two refinements that matter:

- **Concentration compounds with channel.** Three clients that all came from one referrer, or all from one platform, is one relationship, not three. Track source in the roster and check it at review.
- **Reducing concentration by growing is the pleasant route** — the denominator rises and nobody loses a client. It is also slower than it feels: at 45% share, replacing enough revenue to reach 30% means growing the rest of the book by roughly half.

## Client Profitability

Rank clients by effective rate, not by invoice size. The largest client is frequently not the most profitable, and the ranking is usually a surprise the first time it is computed.

For each client over the last 12 months: revenue ÷ (delivery hours + unbilled extras from the change log + meeting hours + collections time). Then look at three things:

- **The bottom quartile.** These are the reprice-or-drop candidates. Reprice first — a client who accepts a corrected rate was never the problem.
- **The gap between headline and effective rate.** A wide gap points at scope control or collections, both fixable, rather than at the price.
- **Admin load per euro.** Some clients cost four times more to invoice, chase and coordinate than others at the same fee. Enterprise clients often pay well and cost heavily in process; that is a trade, but it should be a known one.

## Capacity

- **Billable hours, not working hours.** Planning at 60-70% billable is the conventional assumption for delivery work; the remainder is sales, admin, collections and learning, all of which are real and none of which invoice. A calendar planned at 100% billable is a calendar with no business behind it.
- **Compute the ceiling explicitly**: available weeks × days per week × billable share × day rate. Four weeks off, 46 working weeks, 4 days a week, 65% billable, 800 EUR/day → 46 × 4 × 0.65 × 800 ≈ 95,700 EUR. That number is the honest ceiling of the current model, and if the income target exceeds it, the fix is rate, model or leverage — not more hours.
- **Retainers consume capacity before it is earned.** Count committed retainer hours against the ceiling first; what remains is what is actually sellable.
- **Reserve slack.** A book with zero unallocated capacity cannot absorb an emergency, cannot take the referral that arrives at the wrong time, and cannot deliver a rescue. Around 10-20% unallocated is the difference between a business and a treadmill.

## Can I Take One More

Five checks, in order, and the first no ends it:

1. **Delivery capacity** for the whole engagement, including its slow middle and its revision rounds — not just its start date.
2. **Would it push an existing client past their promised cadence?** Taking work that degrades a current client trades a known relationship for an unknown one.
3. **Effective rate** at or above the current book's median. Adding below-median work fills the calendar and lowers the average, which is how a busy year earns less than a quiet one.
4. **Concentration effect**: does it improve the mix or worsen it? A new client that is small and from a new source is worth more than its fee.
5. **Timing overlap**: do its milestones collide with an existing client's? Two deadlines in the same week is one missed deadline.

If the answer is no but the client is desirable, the honest response is a start date rather than a rushed yes — and a named date converts far better than an apologetic no.

## Forecasting Without Fiction

- **Committed** = signed work with dates. This is the only number to run the business on.
- **Probable** = verbally agreed or renewal-expected, weighted at roughly half.
- **Pipeline** = proposals out, weighted by historical close rate computed from `## Pipeline` and `## Declined Leads` — the user's own rate, not an assumed one.
- Look 90 days out at every review. The useful question is not "what will I earn" but "which month is empty", because an empty month is visible a quarter ahead and fixable then, and invisible and unfixable in its own week.
- Recurring revenue — retainers and long projects — as a share of the total is the stability number worth tracking quarter to quarter. Rising share means less selling; a very high share means concentration risk in another costume.

## Pruning

Deliberate removal of the bottom of the book, once a year, and it is the fastest available rate rise:

- Take the bottom client by effective rate and either reprice them to the current rate or end the relationship (`offboarding.md`).
- **Reprice before dropping.** A surprising share accept, and those who do were being underpriced rather than being bad clients.
- **Do not prune into an empty pipeline.** Freed capacity converts into income only if there is something to fill it with; otherwise it converts into anxiety. Prune when the pipeline is warm.
- Never prune the client who is merely quiet and profitable. Low-maintenance clients are the reason the difficult ones can be afforded.

## Client Mix

The dimensions worth balancing, checked once a year rather than every quarter:

- **Size**: a few large clients pay better per hour of overhead; several small ones survive one departure. A book of only large clients is fragile; a book of only small ones is administratively expensive.
- **Sector**: clients in one industry share a downturn. Two unrelated sectors is meaningful diversification; five is unfocused positioning and slower sales.
- **Engagement model**: retainers give predictability, projects give effective rate. A mix of both smooths income without capping it (`pricing.md`).
- **Source**: referral, past client, inbound, platform. One source producing everything is a concentration risk (`pipeline.md`).
- **Geography and currency**: cross-border clients hedge a local downturn and add payment friction, transfer costs and time-zone load. Record what was actually received in `revenue/<year>.md`, with its currency, and never sum across currencies without stating the conversion date.

**Write before you move on:** the quarterly review writes one row to `## Portfolio` in `memory.md` — quarter, revenue, active clients, largest-client share, and the decisions taken — and sets the next review date in `## Due`; any client crossing `concentration_limit_pct` becomes a standing item in `## Due` until it is back under; repricing or pruning decisions update the client's row in `## Roster` with the date and, where they change policy, `config.yaml` under `commercial`; the computed capacity ceiling and close rate are practice-level facts and belong in `## Practice Notes`, not in any client's row.
