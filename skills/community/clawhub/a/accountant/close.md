# Close — Ending A Period So It Never Has To Be Reopened

A close is a dependency chain, not a checklist you can shuffle. Every step consumes the output of the one before it, which is why closes that run out of order take three passes.

**Before starting**, read `## Period Status` and `## Due` in `~/Clawic/data/accountant/memory.md`, `recurring-entries.md` (every schedule that must post this period), and `closes/<year>.md` if `## Boxes` points there — the previous close names what was left open, and that list is where this close begins.

**Contents:** [The Order](#the-order) · [Cutoff](#cutoff) · [Accruals And Deferrals](#accruals-and-deferrals) · [The Review Pass](#the-review-pass) · [Locking](#locking) · [Year-End Adds](#year-end-adds) · [Correcting A Prior Period](#correcting-a-prior-period) · [Shortening The Close](#shortening-the-close)

## The Order

| # | Step | Depends on | Done when |
|---|---|---|---|
| 1 | Import and code everything; empty the inbox | — | No uncoded transactions in the period |
| 2 | Reconcile every bank, card, loan, and processor account | 1 | Both adjusted balances equal (`reconciliation.md`) |
| 3 | Cutoff review on revenue and costs at both period edges | 2 | Every document dated within 5 days of the boundary checked |
| 4 | Post recurring schedules — prepaids, deferrals, depreciation | 3 | `recurring-entries.md` fully posted, remaining balances tie |
| 5 | Accrue what is incurred but not invoiced; reverse last period's accruals per their discipline | 3 | No known cost missing from the period |
| 6 | Tie subledgers: AR, AP, inventory, asset register | 2, 4 | Four equalities hold (`reconciliation.md`) |
| 7 | Payroll and transaction tax: liabilities agree to the returns | 2 | Liability balances explained line by line |
| 8 | Empty suspense and uncategorized | 1-5 | Balance zero |
| 9 | Review pass: variance, sign, and reasonableness | 1-8 | Every unexplained movement explained |
| 10 | Produce statements and run the ties | 9 | SKILL.md, Statement Ties That Must Hold |
| 11 | Lock the period, record the close | 10 | Closing date set in the ledger, row written |

Steps 1-2 are what fail when a close drags: no amount of adjusting fixes a period whose transactions are not all in yet.

## Cutoff

The single judgement that decides which period a number lands in. Check documents dated within five days either side of the boundary.

| Item | Belongs to the period where | Test |
|---|---|---|
| Sales of goods | Control passed — usually shipment or delivery per the terms | Read the shipping terms, not the invoice date |
| Services | The work was performed | Timesheet or milestone acceptance date |
| Purchases | Goods were received or the service consumed | Goods-received note, not the supplier's invoice date |
| Expenses paid in advance | The period consumed | Prepaid schedule, not the payment date |
| Credit notes | The original sale, if it corrects it; the current period if it is a new concession | Which one is being corrected |

Cutoff errors are the most common material misstatement in small-company accounts, and they are self-reversing: pulling a January sale into December makes December right by exactly the amount January will now be wrong.

## Accruals And Deferrals

- Accrue every cost **incurred and not invoiced**: contractor work delivered, utilities, professional fees, interest, bonuses earned. Estimate from the last invoice or the contract rate, and note the basis of the estimate in the memo.
- Follow one accrual discipline per account — reverse-and-repost, or post-against-liability — as recorded in `## Coding Rules`. Mixing them double-counts (SKILL.md, Adjusting Entries).
- Release prepaids and deferred revenue from `recurring-entries.md`, then check each schedule's remaining balance against its balance-sheet account. A mismatch means the schedule and the ledger have diverged, and the schedule is usually the one that was not updated when the contract changed.
- **Do not accrue below materiality** unless the item recurs monthly: a 40-unit accrual that must be reversed and re-posted every month costs more attention than the accuracy it buys (SKILL.md Rule 4).
- Accrue for **known bad news** at the point it is known — a lost dispute, a contract penalty, a redundancy decided before period end. Conservatism is a recognition rule, not a mood: losses when probable and estimable, gains when realized.

## The Review Pass

Run these before producing anything. Each catches a class of error the arithmetic cannot.

- **Sign check**: no negative revenue account, no negative expense account, no asset with a credit balance, no card with a debit balance. Each of these is a miscoding with a specific fix, not a display quirk.
- **Variance against the prior period, every account**: explain any line moving by more than 20% or by more than the materiality threshold, whichever is smaller. "Revenue grew" is not an explanation; "three January invoices were dated February" is.
- **Missing-recurring check**: every vendor that billed every month for the last six and did not bill this month. Silence usually means an unposted bill, not a cancelled service. Cross-check `~/Clawic/data/finances/subscriptions.md`.
- **Round-number scan**: entries at exactly 1,000 or 5,000 are often estimates that were never replaced with the real figure.
- **Duplicate scan** on the largest 20 payments of the period.
- **Balance-sheet reasonableness**: every balance-sheet account has a supporting schedule or a reconciliation. An account nobody can explain is a plug from a previous close.

## Locking

Closing without locking is not closing. Once the ties pass:

1. Set the closing date in the ledger so no entry can be posted before it without an override.
2. Write the row in `closes/<year>.md`: period, closed date, whether locked, trial balance status, adjustments posted, anything left open.
3. Update `## Period Status` and the close row in `## Due`.
4. Record headline figures in `## Results`.

An unlocked prior period is where the next reconciliation break is being created right now: software will happily post a backdated transaction into a period whose statements were already sent.

## Year-End Adds

Everything from the monthly close, plus:

- Physical stock count and its adjustment (`inventory.md`); fixed asset existence check against the register (`fixed-assets.md`).
- Allowance for doubtful accounts reassessed against the current aging (`receivables.md`).
- Depreciation and amortization for the full year agreed to the register; any asset placed in service late in the year checked against the convention rules.
- Owner transactions reviewed as a set: draws, distributions, loans to and from the owner, and reasonable compensation (`owner-pay.md`).
- Accrued but unpaid payroll taxes and unused leave agreed to the payroll system (`payroll.md`).
- Book-to-tax differences listed for the preparer, with the trial balance and asset register (`tax.md`).
- Revenue and expense accounts close to retained earnings; the opening balance of the new year is checked against the closing balance of the old (SKILL.md ties).
- Retention purge: destroy only what is past every applicable window, never during an open examination (`tax.md`).

## Correcting A Prior Period

| Situation | Treatment |
|---|---|
| Period open, error below materiality | Correct in place, in the period it belongs to |
| Period closed and locked, error below materiality, no return filed | Reversing plus correcting entry in the current open period, memo naming the original |
| Period closed, error above materiality, no return filed | Reopen deliberately, correct in the period, reclose, and note both closes in `closes/<year>.md` |
| A return has been filed on the affected figures | Not a bookkeeping decision — amendment vs current-period adjustment goes to a tax professional (SKILL.md, Escalate) |
| Statements were issued to a lender, investor, or board | The recipients decide nothing; the entity must reissue or notify. Escalate before touching the ledger |

Never fix a prior period by editing the original entry. The audit trail is the only evidence that the change was a correction rather than a manipulation (SKILL.md Rule 7).

## Shortening The Close

The target is `close_target_days` business days. If it is being missed, the cause is upstream almost every time:

- Documents arriving late → move receipt capture to the point of purchase, and accrue with an estimate instead of waiting (`invoices` handles the document side).
- Coding done only at close → bank rules that propose, reviewed weekly (`software.md`).
- Reconciling once a month → reconcile weekly; a week's worth of differences is findable, a month's is a project.
- The same questions to the client every month → they are coding rules that were never written down (`## Coding Rules`).
- Waiting on one number → close with the estimate, disclose it in the close row, and true it up next period.

**Write when this file produced something durable**: the close itself → a row in `closes/<year>.md`, plus `## Period Status`, the `## Due` close row, and `## Results`. A new recurring accrual, prepaid, or deferral → `recurring-entries.md`. An estimate used because a document was late, or anything left unresolved → `## Open Items` and the close row. A close procedure worth repeating → `artifacts/close-procedure.md` with its `## Boxes` line (`memory-template.md`).
