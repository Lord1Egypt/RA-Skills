# Payroll — Entries, Employer Costs, And The Returns

Payroll is the area where a bookkeeping mistake becomes a personal liability. Withheld tax is not the entity's money, and in many regimes the people who controlled it are personally on the hook when it is not remitted.

**Before any payroll work**, read `## Registrations` in `~/Clawic/data/accountant/memory.md` (which authorities, which deposit frequency, since when), `## Due` for the next deposit and return dates, and `filings/<year>.md` if `## Boxes` points there. A deposit schedule is not something to re-derive each period, and it changes only on notice.

**Contents:** [The Entry](#the-entry) · [Employer Costs](#employer-costs) · [Deposits And Returns](#deposits-and-returns) · [Leave Accrual](#leave-accrual) · [Employee Or Contractor](#employee-or-contractor) · [Owners On Payroll](#owners-on-payroll) · [Reconciling Payroll](#reconciling-payroll) · [Multi-Jurisdiction Payroll](#multi-jurisdiction-payroll)

## The Entry

A payroll run is never one line. Gross wages are the expense; net pay is only the part that leaves as cash.

```
Dr  Wages expense                          gross pay
Dr  Employer payroll tax expense           employer share
  Cr Employee tax withheld (liability)                withheld income tax
  Cr Employee social contributions (liability)        employee share
  Cr Employer contributions (liability)               employer share
  Cr Other withholdings (liability)                   pension, garnishment, benefits
  Cr Net pay / payroll clearing                       what hits the bank

On payment of the net:      Dr Payroll clearing        / Cr Bank
On remittance to authority: Dr the tax liabilities     / Cr Bank
```

- **Gross, not net.** Posting only net pay understates wage expense by the entire withholding, hides liabilities that are already owed, and guarantees the payroll return will never tie to the ledger (SKILL.md ties).
- **Withholdings are liabilities the moment they are withheld**, not when remitted. The balance-sheet account is the running total of money held on someone else's behalf.
- **Employer contributions are an expense**, employee withholdings are not — they are part of the gross the employee already earned. Booking the employee share as an employer cost double-counts.
- Use a **payroll clearing account** when a provider takes one aggregate debit covering net pay and taxes: the provider's single bank line clears the account, and the account nets to zero after every run (`reconciliation.md`).
- Cost allocation by department, project, or between COGS and operating expense happens on the **gross wage line**, and the split must be the same one used for margin (`bookkeeping.md`).

## Employer Costs

The real cost of an employee is not the salary. Build every hiring or pricing figure from the loaded cost:

```
Loaded cost = gross pay
            + employer social contributions
            + employer pension or retirement contribution
            + unemployment and disability levies
            + workers' compensation or equivalent insurance
            + benefits the employer pays
            + payroll processing per head
```

US anchors, stable enough to plan with but worth confirming for the year: employer FICA is 7.65% of wages (6.2% social security up to an annually indexed wage base, plus 1.45% Medicare with no ceiling, and an additional Medicare withholding on high earners that is **employee-only**). FUTA is 6.0% on the first 7,000 of each employee's wages, reduced to 0.6% where the state credit is available in full; state unemployment rates are experience-rated and arrive as an annual notice. Loaded cost for a typical US small employer lands roughly 10-15% above gross before benefits, and higher in most European regimes — never quote the general figure when the actual rates are on the last payroll report.

## Deposits And Returns

Missing a deposit is more expensive than missing almost any other deadline, because penalties are a percentage of the amount and escalate by days late.

- **Deposit frequency is assigned, not chosen.** In the US it is set by a lookback at prior-period tax liability, with monthly and semiweekly schedules, plus a next-business-day rule once accumulated liability crosses 100,000. The schedule is reassessed annually and notified — record it and its effective date in `## Registrations`.
- Quarterly and annual returns report **wages and taxes**, and their totals must agree to the ledger for the same span (SKILL.md ties). A difference is almost always a bonus, a benefit in kind, or a correction posted directly to the liability.
- Year-end employee statements and contractor information returns are typically due in **January**, before the entity's own return, and carry per-form penalties that scale with lateness. They are a `## Due` row from the moment the first person is paid.
- Every filing goes into `filings/<year>.md` with its period, amount, and confirmation reference — including nil returns, which are exactly the ones later disputed.

**Withheld and not deposited is an escalation, not a bookkeeping task** (SKILL.md, Escalate). Do not net it against anything, do not defer it, and say so the same day.

## Leave Accrual

- Accrue paid leave when it **vests and is payable on termination**; do not accrue leave that expires unused and is never paid out. `reporting_framework` and local labor law decide which applies, and it is a written policy, not a monthly judgement.
- Liability = accrued hours × the current pay rate + employer contributions on that pay. Rate changes revalue the whole balance, not just new accrual.
- Recompute at each close from the leave register, never by incrementing last month's number — the increment approach drifts and cannot be audited.
- Sabbaticals, long-service awards, and bonuses earned in one period and paid in another follow the same rule: expense the period the entitlement was earned.

## Employee Or Contractor

Misclassification is assessed retroactively with back taxes, interest, and penalties, and the liability usually sits with the payer. The tests differ by jurisdiction but converge on the same substance:

| Points toward employee | Points toward contractor |
|---|---|
| The payer controls how, when, and where the work is done | The worker controls method and schedule |
| Tools, equipment, and workspace provided | Own tools and premises |
| Paid for time, at regular intervals | Paid for a defined result |
| Works for this payer only, indefinitely | Multiple clients, project-bounded |
| Integrated into the organization — title, team, internal systems | Engaged for a specific deliverable |
| Cannot subcontract | Free to send a substitute |
| No financial risk of loss | Bears the risk of overrun |

A contract that says "contractor" changes nothing if the facts point the other way. Where the answer is genuinely close, it is a legal question with a jurisdiction-specific procedure for getting a determination — escalate rather than deciding it in the ledger (SKILL.md, Escalate).

Contractor payments carry their own reporting: collect the tax identification document **before the first payment**, run the year-to-date reportable total per payee from the ledger before the deadline, and record each return filed with those totals in `filings/<year>.md`. The US reporting threshold for service payments to unincorporated payees moved from its long-standing 600 figure by legislation — confirm the amount for the payment year; what does not move is that the return is due in January and penalties are per form (`tax.md`).

## Owners On Payroll

Whether an owner can or must be on payroll is determined by entity type, not preference — sole traders generally cannot employ themselves, corporate officers who work generally must be paid as employees. Structure, reasonable compensation, and the split between salary and distributions: `owner-pay.md`.

## Reconciling Payroll

At every close:

1. Net pay per the payroll report = the bank debits for the run.
2. Gross wages per the report = the wage expense in the ledger for the period, plus or minus the accrual movement.
3. Each liability account balance = the amount withheld and not yet remitted, agreeing to the provider's tax report.
4. Payroll clearing = zero after the run clears.
5. Cumulative wages year to date = the sum of the periodic returns filed so far.

A liability account with a balance that never clears is either a remittance coded to expense instead of the liability, or a genuine unpaid tax — and those two need to be told apart immediately.

## Multi-Jurisdiction Payroll

- Registration is triggered by **where the employee works**, not where the entity is. One remote hire in a new state or country creates registration, withholding, and filing obligations there, usually from the first day of work.
- Reciprocity agreements between neighboring jurisdictions change withholding but rarely the registration duty.
- Paying a foreign worker as a contractor to avoid registration is the misclassification test above, applied by an authority with a longer reach than usual.
- Every new jurisdiction is a `## Registrations` row plus new `## Due` rows before the first payroll run there, never after.

**Write when this file produced something durable**: a deposit schedule, registration, or rate notice → `## Registrations`, with the next dates in `## Due`. Each return filed → `filings/<year>.md`. A leave-accrual or classification policy → `artifacts/` with its `## Boxes` line. A payroll coding split by department or COGS → `## Coding Rules`. Anything withheld and unremitted → `## Open Items` and an immediate escalation (`memory-template.md`).
