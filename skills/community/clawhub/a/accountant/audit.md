# Audit, Controls, And Being Examined

Being examined is a documentation exercise, not an accounting one. Everything that makes it cheap was done months earlier.

**Before assembling anything for an outside party**, read `## Period Status` and `closes/<year>.md` — the close rows record what was left open, and an examiner or auditor will find those items whether or not they are disclosed. Disclosing them first changes the tone of the whole engagement.

## Which Engagement Is Being Asked For

| Engagement | What the practitioner does | Assurance | Who can sign |
|---|---|---|---|
| Bookkeeping / management accounts | Prepares the figures from the records | None | Anyone |
| Compilation | Presents management's figures in statement form | None, explicitly stated | Licensed practitioner |
| Review | Analytical procedures and enquiry | Limited — "nothing came to our attention" | Licensed practitioner |
| Audit | Testing, confirmation, sampling, controls evaluation | Reasonable assurance | Licensed auditor |
| Agreed-upon procedures | Specific tests the client specified | Findings only, no opinion | Licensed practitioner |

Producing figures is this skill's work; **applying any of the last four labels is not** (SKILL.md, Escalate). When a lender asks for "audited accounts", the useful reply names what can be produced, what a licensed engagement would add, and what it costs — not a relabelled management account.

## The PBC Package

Prepared-by-client lists vary little. Assembling it before it is asked for cuts the engagement's cost, because auditor time is spent chasing rather than testing.

- Trial balance for the period and the comparative, on the declared basis, from locked books
- General ledger detail, exportable, with the ability to drill to the document
- Bank statements for every account and every month, plus the reconciliations
- AR and AP agings at period end, tying to their control accounts
- Inventory count sheets, the valuation, and the costing method policy
- Fixed asset register with additions, disposals, and the depreciation calculation
- Loan agreements and amortization schedules; lease agreements and the discount rates used
- Payroll returns and their reconciliation to the ledger
- Revenue contracts, especially anything unusual, plus the recognition policy
- Board or member minutes, ownership records, and any agreement changing rights
- Related-party transactions, listed
- The accounting policies actually applied, and any change with its date
- Subsequent events between period end and today

Everything on that list either exists in `~/Clawic/data/accountant/` already or is a document the entity holds. Anything that has to be *built* for the request is a gap worth fixing before the next period.

## Controls In A Team Of Three

Segregation of duties assumes staff that a small entity does not have. The workable version separates the four incompatible functions as far as headcount allows, and compensates with detective controls where it cannot:

| Function | Should not be the same person as | Compensating control when it must be |
|---|---|---|
| Authorizing a payment | Executing it | Owner reviews the payment run before release |
| Executing a payment | Reconciling the account | Owner opens the bank statement personally, monthly |
| Recording transactions | Holding the asset | Independent count and confirmation |
| Setting up a vendor or changing bank details | Paying it | Out-of-band verification on a number obtained before the change (`payables.md`) |

Highest-value controls for a very small entity, in order of return:

1. The owner personally opens bank and card statements and reviews the payment run — this alone stops most internal fraud.
2. Bank rules propose, a human confirms; nothing auto-posts (`software.md`).
3. Dual authorization above a stated amount.
4. Monthly reconciliation of everything, on a schedule (`## Due`).
5. Mandatory time off for whoever handles money — most long-running frauds require daily maintenance.
6. Vendor bank-detail changes verified out of band, always.
7. System access reviewed when anyone leaves, the same day.

## Fraud Signals In The Books

Observable, not speculative. Any of these is investigated before it is explained away.

| Signal | Common cause |
|---|---|
| A reconciling difference that recurs and grows | Concealment, not error (SKILL.md, Escalate) |
| Vendors with a name close to a real one, or a PO box, or no online presence | Fictitious vendor |
| Payments just below the authorization threshold, repeatedly | Structuring around the control |
| A clearing or suspense account with a persistent balance | Something is being parked |
| Journal entries posted at odd times, at round amounts, by the person who reconciles | Manual override of the process |
| Credits and write-offs concentrated with one customer or one employee | Lapping of receipts |
| An employee who never takes leave and resists anyone covering their work | The scheme needs daily maintenance |
| Duplicate payroll bank details across two employee records | Ghost employee |
| Voids and refunds spiking without a matching return of goods | Cash skimming at the point of sale |
| Gross margin falling with no price or cost explanation | Inventory theft (`inventory.md`) |

## When A Tax Authority Opens An Examination

- **Stop the routine purge** of records immediately, whatever the retention window says (`tax.md`).
- Establish scope in writing: which entity, which periods, which taxes. Answering questions outside the stated scope widens it voluntarily.
- Provide what is requested, completely, and nothing more. Volunteering adjacent years or unrelated schedules is how a narrow examination becomes a broad one.
- Route communication through one person, and keep the log of every request and every document provided, with dates, in `artifacts/examination-log-<year>.md`.
- Examiners open predictably: owner personal expenses, cash transactions, related-party dealings, large round-number entries, year-end adjustments, and the difference between reported revenue and third-party reporting such as processor and platform totals.
- If records for a period are missing, reconstruction has evidentiary rules — that is counsel's call, not a bookkeeping improvisation (SKILL.md, Escalate).

## Subsequent Events

Between period end and the day the figures are issued, two kinds of event occur and they are treated in opposite ways:

- **Adjusting** — evidence about a condition that already existed at period end: a customer entering insolvency shortly after the year end confirms the receivable was impaired *then*; a legal case settling confirms the liability's amount. Adjust the figures.
- **Non-adjusting** — a new condition arising after period end: a fire, a large new contract, a funding round. Do not adjust; disclose if it would change a reader's understanding.

The distinction is what makes a set of statements defensible three months after the date on their front page.

**Write when this file produced something durable**: the PBC package actually assembled → `artifacts/audit-package-<period>.md` with its `## Boxes` line. Any control walkthrough, gap, or compensating control agreed → `artifacts/controls.md`. Examination scope, requests, and documents provided → `artifacts/examination-log-<year>.md`, with dates and its `## Boxes` line. A fraud signal investigated → `## Open Items` until closed, plus an escalation where the table above says so (`memory-template.md`).
