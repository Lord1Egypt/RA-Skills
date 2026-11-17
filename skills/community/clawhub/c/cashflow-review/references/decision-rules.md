# Cashflow decision rules

Choose exactly one decision after reconciling evidence, cash, direct cost,
human time, and delivery acceptance. Do not substitute a forecast, benchmark,
invoice, contract, or pipeline metric for the underlying records.

Run Authorization permits this private reconciliation and decision work
without another approval; it never authorizes an external next step. Return the
decision and its receipts to `moneyprinter` for Money Machine Run update and
route reranking.

## Calculations and labels

- **Cash collected:** total settled payments received during the review period
  and supported by inspected, privacy-safe settlement artifacts.
- **Revenue contracted:** total signed obligations supported by inspected,
  privacy-safe signed-obligation artifacts and not yet collected; report
  separately from cash.
- **Revenue booked:** total unpaid invoices or orders; report separately from
  cash and contracted revenue.
- **Direct cost:** known test-attributable cash costs, including refunds,
  processor fees, contractors, delivery materials, and paid tools.
- **Human hours:** actual human time by role. Do not infer missing time or
  convert it to a cost without an approved, evidence-backed rate.
- **Gross profit:** `cash collected - direct cost`. This is cash gross profit
  before any human labor cost not already included in direct cost. It uses no
  speculative future cash, estimated labor savings, or assumed renewals.
- **Approved labor cost:** the user-approved total supported by recorded human
  hours and evidence-backed role-specific or blended labor rates, excluding
  labor already counted in direct cost.
- **Labor-adjusted profit:** `cash collected - direct cost - approved labor
  cost`.
- **Realized hourly value:** `(cash collected - direct cost) / recorded total
  human hours`. Calculate it only when total human hours are known and greater
  than zero. Compare it only with an explicit minimum hourly value approved for
  this test; do not invent the floor.

Labor economics are acceptable through either of two paths:

1. Recorded human hours, an approved labor cost, and positive labor-adjusted
   profit; or
2. Recorded human hours, a calculable realized hourly value, and a result at or
   above the explicit approved minimum hourly value.

If human hours are missing, both paths are unavailable, or the selected path
fails its threshold, labor economics are unknown or unacceptable. Positive
cash gross profit alone does not resolve that gap.

For reply, meeting, proposal, close, delivery-acceptance, and repeat rates,
show the recorded numerator and denominator. If the denominator does not
exist, report `N/A — denominator unavailable` and describe the evidence gap.

## Select one decision

Use one, and only one, of these labels verbatim:

- `STOP — no credible signal or unacceptable economics`
- `REVISE — signal exists but offer, channel, or delivery failed`
- `REPEAT — one more bounded test is justified`
- `SCALE — cash and delivery proof support increased volume`

### STOP — no credible signal or unacceptable economics

Choose `STOP` when there is no credible signal after a fair bounded test, the
economics are unacceptable, a legal/policy/safety issue blocks the route, or
missing authority/proof prevents an honest conclusion. Name the failed
assumption and do not continue merely because effort has already been spent.

### REVISE — signal exists but offer, channel, or delivery failed

Choose `REVISE` when a credible signal exists but a specific fixable element
failed: buyer/offer fit, price, channel, delivery quality, acceptance criterion,
or cost structure. State the one change, the next bounded hypothesis, and the
new stop condition. Do not conceal refunds, rework, or rejection.

### REPEAT — one more bounded test is justified

Choose `REPEAT` when the result has credible but insufficient evidence for
scale, the delivery outcome is acceptable or the remaining uncertainty is
narrow and safely testable, and one more bounded test can resolve it within a
defined cost and human-work ceiling. State the exact evidence gap and threshold
for the next review.

### SCALE — cash and delivery proof support increased volume

Choose `SCALE` only when all of the following are true:

1. At least one settled payment with the required inspected settlement artifact
   supports the `Cash collected` result.
2. Delivery acceptance is documented against pre-defined criteria.
3. Cash gross profit is positive using settled cash minus known direct cost,
   with material unknown cash costs disclosed.
4. Human hours are recorded by role.
5. Labor economics pass at least one approved path: labor-adjusted profit is
   positive after an approved labor cost, or realized hourly value meets or
   exceeds an explicit approved minimum.
6. Delivery capacity, correction/refund handling, authority, and compliance
   remain credible at the proposed increased volume.

Never choose `SCALE` on a simulation, estimated economic value, pipeline
signal, invoice, contract, booked revenue, or any combination of those alone.
Unknown human hours, an unavailable labor-economics path, non-positive
labor-adjusted profit, or realized hourly value below its approved threshold
must result in `STOP`, `REVISE`, or `REPEAT`, never `SCALE`. Choose among those
three from the actual evidence: use `REPEAT` for a narrow measurement gap,
`REVISE` for a fixable pricing, scope, cost, or delivery problem, and `STOP`
for unacceptable economics or an unsafe or non-credible route.

## External next steps

A decision authorizes no external action. If a next step would contact, send,
post, publish, purchase, charge, sign, submit, or change an account, stage the
canonical checkpoint from payable-test:

```markdown
Action: [send/post/publish/purchase/charge/sign/submit/account change]
Exact payload: [the final text, asset, order, charge amount, agreement, or setting]
Destination: [named recipient, audience, platform, vendor, or system]
Channel: [email/DM/post/listing/payment rail/contract flow/account surface]
Account: [named sending, publishing, purchasing, payment, or system account]
Timing: [execution date/time or bounded window]
Scope: [one exact action and its included payload, audience, or commitment]
Volume: [one recipient/item or exact bounded count]
Tool: [host tool, connector, browser, CLI, or service used for execution]
Expected cost: [cash amount/currency, staff time, fee, or "none known"]
Evidence label: [label that the action could support]
Rollback or correction path: [how it can be withdrawn, corrected, refunded, reversed, or remediated]
Approver authority status: [Pass + basis / Unknown / Fail]
Third-party data status: [None used / Pass + consent or lawful-use basis and minimum data / Unknown / Fail]
Regulated-review status: [Not applicable / Pass + qualified reviewer, jurisdiction, and approved scope / Unknown / Fail]
Approval requested: Approve this exact action now? [yes/no]
```

Any `Unknown` or `Fail` prerequisite blocks the request. Any material change to
the action, payload, destination, channel, account, timing, scope, volume, tool,
cost, evidence label, rollback/correction path, authority, data basis, or
regulated-review status requires a fresh immediate approval.
After an immediately preceding exact approval, the current host may perform
only that approved action, record an `Action receipt`, and return it to
`moneyprinter`. Broad, batch, stale, or materially changed permission is
invalid. Regardless of whether an external step is staged, return exactly one
`STOP`, `REVISE`, `REPEAT`, or `SCALE` decision for portfolio reranking.
