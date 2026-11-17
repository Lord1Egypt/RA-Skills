# Financial Operations

## Monthly Close

Target 5–10 business days; every day past 10 means the whole company decides on stale data. Below audit stage, close *speed* beats close *perfection*: get cash, revenue, and payroll exactly right first; refine expense allocations later.

| Day | Activity |
|-----|----------|
| 1–3 | Transaction cutoff, preliminary data |
| 4–6 | Reconciliations, accruals |
| 7–8 | Review, adjustments |
| 9–10 | Final close, variance analysis, reporting |

Checklist: bank reconciliations · revenue recognized per policy · expenses accrued · payroll posted · intercompany balances eliminated · balance sheet reconciled · variance analysis drafted.

The close calendar owns every external deadline too: lender reporting dates, investor information rights, and recurring tax filings. A deadline that lives only in someone's memory is the one that becomes a technical default.

## Internal Controls

Segregation of duties — one person must never both initiate and approve money movement:

| Process | Separation |
|---------|------------|
| Payments | Approver ≠ payer |
| Deposits | Receiver ≠ recorder |
| Payroll | Processor ≠ approver |
| Journal entries | Preparer ≠ approver |

Approval thresholds (canonical template; SKILL.md Rule 9 keys off this). Tiers scale from `approval_threshold`: below it a manager approves, to 10× a director, to 50× a VP, above 50× the CFO with the CEO. At the default of $1,000 that reads <$1K manager · $1K–$9,999 director · $10K–$49,999 VP · $50K+ CFO/CEO. Thresholds exist so finance says yes fast below the line, not to slow everything down. Publish the matrix and the turnaround time; an unpublished threshold is a bottleneck people route around.

Below ten people, perfect segregation is impossible. Compensating controls that actually work at that size: the founder reviews the full bank statement monthly, no exceptions; a second person approves any payment above a low threshold; and no single person holds both the banking credentials and the accounting login.

**Fraud reality**: the top startup loss vector is business email compromise — a "vendor" emails new bank details before a large payment. Control: verify every bank-detail change by phone at a number you already had on file, never one from the requesting email. This single rule blocks the most expensive fraud class a small company faces.

Related controls worth the ten minutes each: dual approval on new payees, a hard rule that no payment is ever released on an urgency claim from an executive (that *is* the attack), corporate cards with per-card limits instead of a shared card, and quarterly review of who still holds banking and payroll access — offboarding routinely misses financial systems.

## Spend and Procurement

- Every recurring vendor has an owner, a renewal date, and a cancellation notice period recorded in one place. Auto-renewals with 60- or 90-day notice windows are the most common avoidable cost in a startup.
- Route new spend above the manager threshold through a one-line business case: what it replaces, what it costs annually, who owns it. It takes a minute and kills half the requests before they are submitted.
- Expense policy: one page, receipts above a stated amount, categories that map to the chart of accounts, and reimbursement inside one payroll cycle. Slow reimbursement is a trust cost paid in the wrong currency.
- Annual vs monthly contracts is a cash decision, not a procurement one: annual prepay for a discount is fine at 18+ months of runway and wrong at 9.

## Financial Systems

| Function | Options |
|----------|---------|
| Accounting | QuickBooks, Xero → NetSuite at scale |
| Expense management | Brex, Ramp, Expensify |
| Billing | Stripe Billing, Chargebee |
| Payroll | Gusto, Rippling, ADP |
| FP&A | Spreadsheets first; Mosaic, Pigment when >2 people consume the model |
| Cap table | Carta, Pulley |

Selection rule: buy for the next 18–24 months, not the 5-year vision. NetSuite at seed is the classic overbuy — a year of implementation for scale you don't have. The reverse trap exists too: spreadsheet accounting past ~$1M in revenue guarantees a cleanup bill before your first raise or audit.

Migration timing: move systems immediately after a close, never mid-quarter, and never during a raise or an audit. Budget for parallel running and for the historical data that will not migrate cleanly. Record which systems the user actually runs in memory so recommendations stop being generic.

## Insurance and Obligations

- **D&O** becomes necessary when the first outside director joins — no serious director serves without it. **E&O / tech errors** is increasingly a customer contract requirement. **Cyber** is required by many enterprise buyers and by some insurers as a condition of other coverage. Employment practices liability matters most around a layoff.
- Renewals are annual and priced on headcount, revenue, and claims history; start 60 days out, and expect coverage questions to appear in customer security reviews.
- Record retention: financial records, contracts, board consents, and tax filings are kept for the statutory period in each jurisdiction — and everything relevant is preserved the moment litigation or an audit is foreseeable, which is a legal obligation, not a policy choice.

## Building the Finance Team

| Stage | Hire |
|-------|------|
| Pre-seed | Outsourced bookkeeper |
| Seed | Fractional CFO or part-time controller |
| Series A | Full-time controller |
| Series B | CFO, first FP&A analyst |
| Series C+ | Treasury, tax, accounting manager |

Ordering principle: controller before FP&A — get the actuals right before you forecast them. A forecast built on unreconciled books compounds the error with confidence.

The trigger to bring accounting in-house is scrutiny, not revenue: a lender, an audit, or a board that asks about a specific line and needs the answer within a day. Outsourced providers are excellent until the question is urgent and specific.

## Audit Readiness

- Triggers: investor requirement (usually Series B+), enterprise customer demand, acquisition prep, regulation.
- Budget 3–6 months for the first audit; pick an auditor with a startup practice — Big 4 at Series B is paying enterprise rates for a junior team.
- Audit the prior year *before* a deal forces you to: acquirers require audited financials, and a retroactive audit under deal pressure surfaces every historical shortcut at the worst possible negotiating moment.
- Clean historical books and written accounting policies first; auditing a mess costs more than fixing then auditing. The one-page revenue recognition memo is the first policy the auditor asks for.
- Expect a management letter listing control deficiencies. Fix them the same year — the second appearance of the same item is what a lender or acquirer reads as a governance signal.

