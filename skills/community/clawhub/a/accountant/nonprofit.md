# Nonprofit And Fund Accounting

A nonprofit's books answer a question a commercial ledger never asks: not "did we make money" but "did we spend each donor's money on what they gave it for". Everything structural follows from that.

**Before any nonprofit work**, read `## Books` in `~/Clawic/data/accountant/memory.md` for the entity form and exemption status, and `artifacts/` for the functional expense allocation methodology — an allocation basis that changes between periods makes every comparative meaningless.

## What Changes Versus A Company

| Commercial | Nonprofit |
|---|---|
| Equity | Net assets, split by donor restriction |
| Income statement | Statement of activities, by restriction class |
| Retained earnings | Accumulated net assets, not distributable |
| Profit | Change in net assets |
| Expenses by nature | Expenses by **function** as well: program, management and general, fundraising |
| Owners | No owners; no distributions exist at all (`owner-pay.md`) |
| Tax on profit | Generally exempt, but taxed on unrelated business income |

Board-designated reserves are **not** restricted: the board can undesignate what it designated. Only a **donor** can restrict, and only in writing at or before the gift. Presenting board designations as restricted overstates how constrained the organization is, which is exactly backwards from the risk everyone assumes.

## Net Asset Classes

Two classes under current US standards, and the same distinction in substance elsewhere:

- **Without donor restrictions** — general operating funds, including board-designated amounts (disclosed separately).
- **With donor restrictions** — purpose restrictions (a program, a project), time restrictions (a future period), and perpetual restrictions (an endowment corpus).

```
Restricted gift received:      Dr Cash / Cr Contribution revenue — with donor restrictions
Restriction satisfied:         Dr Net assets released from restriction (with)
                               Cr Net assets released from restriction (without)
                               — the expense itself is recorded normally, in the period incurred
```

- The release entry is what proves the money was used as promised. Spending restricted funds without releasing them leaves the restricted balance permanently overstated and makes the next grant report impossible to produce.
- **Restricted cash is not available cash.** A liquidity presentation showing total cash without separating restricted balances is the single most misleading figure in nonprofit reporting, and it is why a disclosure of resources available within a year is required under US standards.
- Track each restriction with its purpose, amount, and expiry in `## Open Items` until it is released — that register is what the release entries are computed from.

## Contributions Versus Exchange Transactions

The classification decides the timing, and it is the most consequential judgement in the ledger.

| | Contribution | Exchange transaction |
|---|---|---|
| Nature | Voluntary, non-reciprocal | Commensurate value received by the payer |
| Timing | Recognized when the promise is **unconditional**, not when the cash arrives | Recognized as the obligation is satisfied (`revenue.md`) |
| Example | An unrestricted donation; most foundation grants | A ticketed training course; a service contract |

- **Conditional promises** — those with a barrier the organization must overcome and a right of return or release — are recognized only when the condition is met. A cost-reimbursement grant is usually conditional: revenue is recognized as qualifying costs are incurred, not on signature.
- A **restriction** is not a condition. Restricted-and-unconditional is recognized immediately, in the restricted class; conditional is not recognized at all yet.
- Multi-year unconditional pledges are recognized at present value, with the discount unwinding as contribution revenue in later periods, and an allowance for uncollectible pledges assessed like any receivable (`receivables.md`).
- Special events are usually **split**: the fair value of what the attendee received is exchange revenue, the excess is a contribution. Reporting the whole ticket as a donation overstates giving and misstates the donor's own deduction.

## Gifts In Kind And Volunteers

- **Donated goods** are revenue and an expense or asset at fair value on receipt, with the valuation basis documented. Under current US standards they are presented separately by category with the valuation techniques disclosed.
- **Donated services** are recognized only when they create or enhance a non-financial asset, or require specialized skills that would otherwise have been purchased — a donated audit or legal work qualifies; volunteer hours stuffing envelopes do not.
- Volunteer hours that fail the test are still worth tracking outside the ledger: many grant applications and match requirements need the number, and it is not reconstructible later.

## Functional Expense Allocation

Every expense is reported by function as well as by nature. The allocation basis is a methodology, not a monthly guess.

| Cost | Common basis |
|---|---|
| Salaries | Time records or a documented time study, by program |
| Occupancy | Square footage used by each function |
| Technology | Headcount, or usage where measurable |
| Depreciation | Follows the function of the asset's use |
| Direct program costs | Not allocated — charged directly |

- Management and general covers governance, finance, and administration; fundraising covers all solicitation, including the fundraising portion of a mixed-purpose mailing.
- **Joint costs** of activities that combine program and fundraising can be allocated only when purpose, audience, and content criteria are met; otherwise the whole cost is fundraising. Funders read this closely.
- Overhead ratios are scrutinized and frequently misused — but the answer is a documented, consistently applied methodology, not an allocation tuned to produce a better ratio. Write it down as an artifact, with the date and the basis for each pool.

## Grants

- Read the agreement before the first entry: is it a contribution or an exchange, is it conditional, what costs are allowable, what is the reporting cadence, and is there an indirect cost rate.
- **Track each grant separately** from day one, coded so its report can be produced from the ledger rather than assembled by hand. A tracking category or class per grant is the standard mechanism (`software.md`).
- Unspent restricted funds at the end of a grant period are either returnable or extendable, and which one it is determines whether the balance is a liability or restricted net assets. This is a contract question with a balance-sheet answer.
- Government grants often carry audit requirements triggered by expenditure thresholds, with their own procedures and deadlines — an obligation to know about **before** accepting the money.
- Every grant report submitted goes into `filings/<year>.md` alongside tax filings: to the organization, a missed grant report has the same consequences as a missed return.

## Exemption And Filings

- Exemption is **conditional and revocable**. It is lost by operating outside the exempt purpose, by private benefit or inurement to insiders, by prohibited political activity, and — most commonly — by simply failing to file for consecutive years.
- **Unrelated business income** is taxable even for an exempt organization: activity that is a trade or business, regularly carried on, and not substantially related to the exempt purpose. Advertising revenue, unrelated merchandise, and some rental income are the usual candidates, and they need a separate return.
- The annual information return is a **public document**. It is read by funders, journalists, and charity raters, so the figures in it are effectively published — which raises the cost of an inconsistency between it and the financial statements.
- Charitable solicitation registration is a **separate obligation from tax exemption**, is per state or region, must be renewed, and is triggered by soliciting there — including online in several jurisdictions.
- Transactions with insiders carry sanctions in many regimes; they need board approval, comparability data, and contemporaneous documentation. This is a `## Due` governance item, not a bookkeeping one.

**Write when this file produced something durable**: the functional expense allocation methodology and its bases → `artifacts/policy-functional-allocation.md` with its `## Boxes` line. Each restriction with purpose, amount, and expiry → `## Open Items` until released, or its own box once there are more than a handful. Grant terms and reporting cadence → `## Due`, with each report filed in `filings/<year>.md`. Exemption status, registrations, and renewal dates → `## Registrations` (`memory-template.md`).
