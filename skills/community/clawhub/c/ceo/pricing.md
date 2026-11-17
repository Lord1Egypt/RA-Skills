# Pricing — The CEO's Highest-Leverage Lever

Price flows straight to gross profit: a 1% price increase held with no volume loss is a 1% revenue gain at ~100% margin, while a 1% volume gain costs whatever it costs to acquire. It is also the decision most companies make once, by intuition, and never revisit.

## What Only The CEO Can Decide

- The pricing **metric** (what a customer buys a unit of) — seats, usage, outcomes, sites, transactions.
- The **packaging** (what is in which tier and what is deliberately withheld).
- The **discount authority** matrix and who can break it.
- Whether you are the premium option or the cheap one. Both work; being accidentally in the middle does not.

Everything downstream — page layout, promo calendar, sales enablement — belongs to `cmo` and sales.

## Choosing the Metric

The pricing metric should rise with the value the customer receives and be predictable enough to budget. Test any candidate against four questions:

1. Does it grow when their success grows? (Seats do not, if your product removes headcount.)
2. Can the buyer predict next year's bill within ~20%? Unpredictable bills lose enterprise renewals regardless of value.
3. Can they game it cheaply? (Shared logins mean seat pricing is really site pricing.)
4. Can you measure it defensibly, and would you show them the meter?

Usage pricing aligns with value and terrifies procurement; seat pricing is legible and caps you; hybrid (platform fee + usage) is the common resolution — commit floor plus overage. Pick one primary metric; two independent meters make your pricing unexplainable in a sales call, which is the real cost.

## Finding the Level

- Willingness to pay is research, not a guess (Ramanujam & Tacke, *Monetizing Innovation*): ask about price before you build the packaging, not after the roadmap is locked.
- Van Westendorp's four questions ("at what price is it too expensive / expensive but worth it / a bargain / so cheap you'd doubt quality") gives a defensible range from ~20-30 interviews with real buyers. It gives a range, never a number.
- The most reliable signal is behavioral: what they pay today for the alternative, including the internal spreadsheet and the person maintaining it.
- The value-based sanity check: quantify the annual value delivered per customer, then price at 10-25% of it. Below 10% you are leaving money on the table; at 25% or above you need proof of value most buyers will not have. The bands cover the whole range: <10 under-priced, 10-25 defensible, ≥25 proof-dependent.
- If nobody ever complains about price, you are under-priced. Convention worth holding: if you win more than about 80% of deals you compete in, you are competing on price, not value.

## Raising Prices

The right cadence is annual and expected, not heroic and rare.

1. Raise on new customers first. Watch win rate and sales-cycle length for one full cycle before touching the base.
2. Grandfather existing customers for a defined period — commonly one renewal cycle — and say the period out loud so it is a decision, not a permanent exception.
3. Give 60-90 days' notice to existing customers, in a message that leads with what they get, then states the change and the date (→ SKILL.md Quick Reference: communication).
4. Expect and budget for churn among the least-engaged customers. The arithmetic: a 15% price increase with 5% churn is a net ~9% revenue gain, and you shed your worst accounts. Compute it with your own numbers before deciding: net change = (1 + increase) × (1 − churn) − 1.
5. Never raise price in the same quarter as a reliability incident or a shipped regression.
6. Handle escalations with a fixed policy decided in advance (who gets an exception and for how long), or the loudest customers set your price.

## Discount Discipline

- Discounts buy something or they are a gift: annual prepay, multi-year commit, a case study, a reference, a bigger scope. Write the exchange into the deal.
- Authority ladder, set by `discount_authority` (default rep:10, vp:20, ceo:above) — and approvals above the top rung get logged and reviewed monthly. Realized price (revenue ÷ list value) is the metric; if average realized price is falling quarter over quarter, list price is fiction.
- Never discount to close inside the quarter. Buyers learn the calendar in one cycle and every deal moves to the last week.
- End-of-life discounting on a legacy plan is a pricing decision, not a sales one — it sets the floor for renewals across the base.
- Price cuts are near-irreversible and public ones reset market expectations permanently; concede term, scope, or volume first (→ SKILL.md Quick Reference: competition).

## Packaging

- Three tiers is the default: entry that removes the objection, core where you want most customers, premium that makes core look reasonable and captures enterprise budget.
- Differentiate tiers by dimensions of value (scale, security, support, controls), never by artificially crippling the core workflow — a hobbled product reads as punishment.
- The features that belong in the enterprise tier are the ones bought by people who are not users: SSO, audit logs, permissions, data residency, an SLA, procurement paperwork.
- Free plan versus free trial: free plans work when usage creates value for other users or when your marginal cost is near zero; trials work when time-to-value is under the trial length. Running both usually means neither is designed.
- Every added tier or add-on costs sales-conversation clarity. If a rep cannot explain the lineup in 30 seconds, buyers cannot either.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Cost-plus pricing | Your costs are irrelevant to the buyer's value | Value-based, sanity-checked against alternatives |
| Copying a competitor's page | Imports their cost structure, segment, and mistakes | Price to your own value and segment |
| Pricing for the biggest logo you want | Whole book anchored to one deal that may never close | Price for the segment you actually serve |
| Never revisiting price | You give away every product improvement for free | Annual review on the calendar, with the data |
| Custom pricing for everyone | No comparability, no forecast, renewals negotiated from zero | Published tiers with a defined enterprise path |
| Announcing a rise without a value story | Reads as extraction; churn concentrates in your advocates | Ship visible value first, then raise |
