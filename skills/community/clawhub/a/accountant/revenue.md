# Revenue — When Income Counts

Revenue is the number everyone reads first and the one most often recognized too early. The rule is not "when invoiced" and not "when paid": it is when the promise was kept.

**Before booking anything other than a plain delivered sale**, read `artifacts/` for an existing revenue recognition policy and `recurring-entries.md` for deferred revenue schedules already running. Two contracts of the same shape must be treated the same way, and the policy is where that consistency lives.

## The Five Steps

ASC 606 and IFRS 15 converge on the same model. Applied to a real contract it takes minutes and settles most arguments.

1. **Identify the contract** — enforceable rights and obligations, collection probable. If collection is not probable, there is no contract for accounting purposes yet; cash received sits as a liability.
2. **Identify the performance obligations** — each distinct good or service the customer can benefit from on its own. Setup that only exists to deliver the subscription is usually not distinct; training that could be bought separately usually is.
3. **Determine the transaction price** — including variable consideration (discounts, rebates, bonuses, penalties, refunds), constrained to the amount that will not later reverse significantly.
4. **Allocate the price** to the obligations by relative standalone selling price — the observable price when sold alone, otherwise an estimate. A discount is allocated across all obligations unless it demonstrably relates to one.
5. **Recognize as each obligation is satisfied** — at a point in time, or over time when the customer receives the benefit as you perform, you build an asset the customer controls, or the work has no alternative use and you have an enforceable right to payment for work done.

## Common Shapes

| Situation | Recognition | Entry pattern |
|---|---|---|
| Goods delivered | On transfer of control — usually shipment or delivery per terms | Dr AR / Cr revenue |
| Time and materials services | As performed, monthly | Dr AR or unbilled receivable / Cr revenue |
| Fixed-fee project with milestones | On acceptance of each milestone, or over time if the criteria are met | Billing ahead sits in deferred revenue |
| Annual subscription paid upfront | Ratably over the term | Dr cash / Cr deferred revenue; monthly release |
| Setup fee that is not distinct | Over the expected customer life, not on day one | The most common early-recognition error |
| Usage-based billing | As usage occurs, including unbilled usage at period end | Accrue the unbilled portion at close |
| Deposit or retainer | Liability until the work is done | Never revenue on receipt |
| Sale with a right of return | Revenue net of expected returns, with a refund liability and a return asset | Estimate from the entity's own history |
| Gift cards and credits | Liability on sale; revenue on redemption, plus expected breakage recognized in proportion to redemptions where permitted | Unredeemed balances may be subject to unclaimed-property rules |
| Reseller or marketplace | Gross if principal, net if agent (→ Gross Or Net) | Changes revenue dramatically, profit not at all |
| Licence with ongoing updates | Split: the licence at a point in time, the support over the term | Requires standalone prices |
| Long-term construction | Over time, measured by inputs (cost-to-cost) or outputs | Loss on a contract is recognized in full as soon as it is expected |

## Deferred Revenue

- The liability is the obligation, not the cash. Money not yet received but already earned is the mirror: an **unbilled receivable** (contract asset), which is a different account and behaves differently in the aging.
- Keep the schedule in `recurring-entries.md`, and check the remaining balance against the deferred revenue account at every close. A schedule that has drifted from the ledger is almost always the schedule, not the ledger — someone changed a contract and never updated it.
- Straight-line release is the default; use a usage or milestone pattern only when delivery genuinely is not even. Prorate the first and last month by days.
- **A cancelled contract with a refund** reverses the remaining deferred balance against cash or a payable; **cancelled with no refund** releases the remaining balance to revenue only when the obligation is genuinely extinguished, which is a contract question.
- Deferred revenue is a working-capital source: it consumes no cash and funds the business, which is why it should be visible in the cash flow discussion rather than buried in "other liabilities" (`statements.md`).

## Gross Or Net

The single most consequential presentation decision in a marketplace, agency, or reseller model. Ask who controls the good or service **before** it transfers to the customer:

| Indicator | Principal (gross) | Agent (net) |
|---|---|---|
| Primary responsibility for fulfilment | You | The other party |
| Inventory or fulfilment risk before transfer | You carry it | You never hold it |
| Pricing discretion | You set the price | The supplier sets it |
| Credit risk on the customer | Yours | Not yours |

Booking gross when you are an agent inflates revenue with no effect on profit — and revenue is what registration thresholds, covenants, valuation multiples, and investors read. It is also one of the first things diligence tests. Document the conclusion per revenue stream in a policy artifact.

## Variable Consideration And Contract Costs

- Estimate variable amounts with either the expected value (many similar contracts) or the most likely amount (a binary outcome), then **constrain** to the portion that will not significantly reverse. Recognizing an unconstrained performance bonus and reversing it two quarters later is exactly what the constraint exists to prevent.
- Volume rebates payable to customers reduce revenue, they are not a marketing expense.
- **Incremental costs of obtaining a contract** — a sales commission that would not exist without the contract — are capitalized and amortized over the period of benefit, including expected renewals, unless the amortization period would be a year or less and the practical expedient is elected. Expensing all commissions immediately while deferring the related revenue misstates both periods.
- Costs to **fulfil** a contract that are not covered by another standard are capitalized when they relate directly, generate resources, and are expected to be recovered.

## Related Practicalities

- **Barter and in-kind exchanges** are revenue at the fair value of what was received, and simultaneously an expense. Recording nothing because no cash moved understates both sides.
- **Related-party revenue** is disclosed separately and never assumed to be at market price.
- **Revenue cutoff at period end** is the most common material misstatement: check every invoice within five days of the boundary against its delivery evidence (`close.md`).
- **The tax definition of income may differ** from the accounting one — cash-basis tax reporting, advance-payment deferral rules, and long-term contract methods all create book-tax differences (`tax.md`).
- What "ARR" or "bookings" mean is a management metric, not revenue, and mixing the two in one report is how a board ends up with two different growth rates. Metric definitions belong to `cfo`; this file owns what hits the ledger.

**Write when this file produced something durable**: the recognition policy for each revenue stream, the gross-versus-net conclusion, and the standalone prices used → `artifacts/policy-revenue-recognition.md` with its `## Boxes` line. Every deferral schedule → `recurring-entries.md`. A contract shape treated for the first time → `## Coding Rules` so the next one matches. A contract dispute affecting recognition → `## Open Items` (`memory-template.md`).
