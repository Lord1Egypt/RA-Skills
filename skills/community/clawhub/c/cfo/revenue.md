# Revenue Recognition and Metric Definitions

Most startup finance arguments are one confusion: four different numbers all called "revenue". Fix the definitions once, write them down, and every later dispute becomes a lookup.

## The Four Numbers

A $120K 12-month contract signed January 1, billed quarterly in advance, delivered continuously:

| Number | What it measures | This contract | Where it belongs |
|---|---|---|---|
| Bookings | Contract value signed | $120K in January | Sales performance, pipeline conversion |
| Billings | Invoices issued | $30K per quarter | Cash forecasting input |
| Revenue | Delivery earned | $10K per month | P&L, gross margin, Rule of 40 |
| Cash | Money received | Whenever they actually pay | The only number that makes payroll |

Deferred revenue is the gap between billings and revenue: bill $30K on day one, recognize $10K, and $20K sits as a liability. That liability is an obligation to deliver, not a war chest — a company can be cash-rich and deeply committed at the same time.

## ASC 606 in Five Steps, and Where Startups Break Each

1. **Identify the contract** — a signed order form, not a verbal yes. Break: revenue booked from a handshake ahead of the quarter close.
2. **Identify performance obligations** — software, implementation, support, and training may be separate. Break: bundling implementation into the subscription and recognizing it ratably when it is delivered up front.
3. **Determine the transaction price** — including variable consideration, credits, and refunds. Break: ignoring an SLA credit likely to be claimed.
4. **Allocate to obligations** — by standalone selling price. Break: allocating by whatever line the customer negotiated hardest on.
5. **Recognize as obligations are satisfied** — over time for continuous delivery, at a point in time for a one-off. Break: recognizing an annual contract on signature.

Write the policy down once, in a one-page revenue recognition memo, and hand it to the auditor and to sales leadership. Two pages of policy prevents twenty pages of restatement.

## ARR: What Counts

- Recurring, contracted, and expected to renew. **Excluded**: professional services, implementation and training fees, one-time hardware, overages billed ad hoc, and anything with a termination-for-convenience clause that has already been invoked.
- Month-to-month contracts count at 12× only if you disclose it; a diligence team will recompute without them.
- Usage-based revenue: annualize a **trailing 3-month average**, never a peak month. A spike annualized is the single most common overstated ARR in diligence.
- Ramped contracts (year 1 at $60K stepping to $120K) enter ARR at the current contractual rate, with the steady-state noted separately. Booking the end-state rate on day one inflates ARR by the ramp.
- Publish the bridge from GAAP revenue to ARR. If nobody can walk from one to the other, the ARR number is an assertion.

## The ARR Bridge

```
Beginning ARR + new + expansion − contraction − churn = Ending ARR
```

- Every component reported separately and every quarter. A single net number hides the case where churn and new bookings both doubled.
- Net dollar retention = (beginning ARR + expansion − contraction − churn) ÷ beginning ARR, measured on the **cohort that existed at the start**, excluding new logos. Including new customers is the classic way an NDR above 100% appears in a company that is shrinking its base.
- Definitions of "churn" (logo vs dollar, and when a downgrade becomes contraction) go in the same memo as the recognition policy.

## Resellers, Marketplaces, and Gross vs Net

- Principal (you control the good before transfer, set the price, carry the risk) → report **gross**, with the partner's cut as cost. Agent → report **net**, only your fee.
- Getting this wrong changes reported revenue by multiples and is a favorite diligence finding. Marketplaces reporting GMV as revenue is the loud version; a reseller arrangement booked gross is the quiet one.
- Take rate, GMV, and revenue are three separate lines in the metrics pack — never a single "revenue" figure.

## Commissions and Contract Costs

- Incremental costs of obtaining a contract (sales commissions, and the payroll taxes on them) are capitalized and amortized under ASC 340-40 over the period of benefit — the expected customer relationship, not the initial term, when renewals earn a lower commission.
- A practical expedient allows expensing when the amortization period would be a year or less; startups commonly take it, disclose it, and stop there.
- Cash impact is unaffected: the commission is paid on the payroll cycle regardless of how it is amortized. Model both.

## Restatement Risk Checklist

Run before any figure goes to a board, a lender, an investor, or a buyer:

- Any revenue recognized before the obligation was delivered?
- Any contract counted in ARR that a customer has disputed, paused, or served notice on?
- Any metric whose definition changed this period without the history restated?
- Any related-party or reseller revenue booked gross that should be net?
- Does revenue in the deck tie to revenue in the ledger to revenue in the model?

Anything unresolved on this list is a Red Flag: freeze external use of the figure and route it to the accountant or auditor.
