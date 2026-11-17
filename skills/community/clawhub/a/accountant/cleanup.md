# Cleanup — Books That Are Behind, Inherited, Or Wrong

Catch-up work fails for one reason: it is attempted chronologically. Every fix in an early month moves every balance after it, so the same months get redone until someone stops.

**Before starting**, read `## Period Status`, `## Open Items`, and `closes/<year>.md` if `## Boxes` points there. If the entity has never had these files, the first deliverable of the cleanup is the diagnostic below, written down — an estimate given before the diagnostic will be wrong by a multiple.

## The Diagnostic

Answer these before quoting time, scope, or a fee. Each has a cheap test.

| Question | Test | Why it decides the plan |
|---|---|---|
| When was the last reconciled month? | Compare each bank statement's closing balance to the ledger | This is the restart point, and everything before it may be out of scope |
| Do the last filed return's figures agree to the books? | Trial balance at that year end vs the return | A disagreement makes every later balance suspect |
| Are opening balances documented? | Is there a source for them | Undocumented opening balances are the largest single risk |
| Do subledgers tie? | AR and AP aging totals vs control accounts | A break means journals were posted to control accounts |
| Is there a suspense, uncategorized, or opening-balance-equity balance? | Read the trial balance | Its size estimates the volume of unfinished work |
| How many transactions are uncoded? | Count them | The only honest input to a time estimate |
| Which periods are filed and therefore frozen? | Filings list | Determines what may be corrected in place |
| Who has been posting, and with what access? | User list and journal entry log | Distinguishes disorder from something worse (`audit.md`) |
| Are personal and business transactions mixed? | Scan the largest 50 payments | Predicts most of the remaining work |

Write the diagnostic as an artifact with its date and figures. It is the baseline the whole engagement is measured against, and it is what makes a scope change a conversation rather than an argument.

## Sequencing

1. **Find the last known-good balance** — the most recent point where the ledger agreed to a bank statement, a filed return, or a prior accountant's final trial balance. Everything before it is history unless something specific requires reopening it.
2. **Freeze the past.** Set the closing date lock at that point. Nothing gets fixed behind it without a deliberate decision (`close.md`).
3. **Reconcile forward, one period at a time**, and do not move to the next until the current one ties. This is the whole method: each closed period becomes the next one's foundation, so no work is ever redone.
4. **Code as you go**, using the standing rules and adding to `## Coding Rules` when a new one is decided. Do not batch-code the whole backlog first: coding without reconciling means coding transactions that will turn out to be duplicates.
5. **Park what cannot be resolved** in suspense with a specific question, and keep one running list for the client in `## Open Items` rather than asking daily.
6. **Rebuild the subledgers** — open invoices and open bills as individual items, never as one lump into the control account.
7. **Then adjust**: accruals, prepaids, depreciation, inventory, payroll ties.
8. **Close and lock each period as it finishes**, writing its row in `closes/<year>.md` with anything left open named.

Time estimate: transactions per month × months, plus a fixed block per period for reconciliation and adjustment, plus the diagnostic's open-question count. Estimating from months alone is what makes catch-up quotes wrong.

## What To Fix And What To Leave

| Situation | Decision |
|---|---|
| Error inside an open, unfiled period | Fix in place |
| Error in a closed period, below materiality, no return filed | Correct in the current period with a reversing entry and a memo |
| Error above materiality in a period whose return was filed | Not a bookkeeping call — a tax professional decides amendment vs adjustment (SKILL.md, Escalate) |
| Missing detail behind a correct total | Leave it, and note the limitation |
| A total that is wrong and material | Fix it, whatever the effort |
| Years before the last filed return, in agreement with it | Leave alone; reopening invites a mismatch with what was filed |
| Personal transactions mixed in throughout | Reclassify to draws or contributions; this is usually the largest single block of work (`owner-pay.md`) |

The governing principle: **the cost of a fix must be lower than the cost of the wrong number**. A cleanup that reconstructs immaterial detail from four years ago is burning the budget that should have gone into making next year clean.

## The Usual Findings

In roughly the order they appear:

- Transfers between the entity's own accounts recorded as income and expense, inflating both.
- Processor payouts booked as revenue, so revenue, fees, and refunds are all wrong (`reconciliation.md`).
- Personal spending on business accounts, uncategorized or coded to a generic expense.
- Loan payments coded entirely to expense, so the liability never reduces.
- Sales tax collected sitting in revenue (`sales-tax.md`).
- Payroll recorded as one net figure, with the liabilities missing entirely (`payroll.md`).
- Duplicate transactions from a feed re-import, usually across one specific date range.
- Inventory purchases expensed, with the inventory account frozen at a figure from years ago.
- An asset register that exists on paper and never matched the ledger, with disposals never recorded.
- Undeposited funds or a clearing account growing every month since inception.
- Opening balance equity with a large balance nobody can explain.
- Accrued liabilities from three years ago that were never reversed.

Each of these has a known fix in its own file; the value of the list is that finding one predicts the others.

## Prior-Period Errors And Restatement

- A correction of a prior-period error, where the framework requires it and the amount is material, is applied **retrospectively**: restate the comparatives and adjust opening retained earnings, rather than running the fix through the current period's profit.
- Below materiality, correcting in the current period is normal and acceptable — this is the practical reason materiality gets set before it is needed (SKILL.md Rule 4).
- A **change in estimate** — useful life, allowance rate, provision — is never restated; it applies from now forward.
- A **change in accounting policy** is usually retrospective and disclosed, and it needs a reason better than a preference.
- Anything touching filed returns or issued statements goes to a professional before it is posted (SKILL.md, Escalate).

## Preventing The Next One

A cleanup that ends without changing the process is a subscription. Before closing the engagement, put in place:

- A weekly coding pass and a monthly reconciliation, as `## Due` rows.
- Standing coding rules for everything that was asked twice → `## Coding Rules`.
- A separate business account and card, with personal spending stopped rather than reclassified monthly.
- Receipt capture at the point of purchase, so close does not wait on documents (`invoices`).
- The closing date lock enforced, and access reviewed (`software.md`).
- A close procedure written down → `artifacts/close-procedure.md`.

## Taking Over From Another Bookkeeper

- Ask for the trial balance, the general ledger export, the reconciliations, the asset register, and the document archive — in writing, with a date.
- Verify the handover against the last filed return before accepting the balances as a starting point.
- Do not correct the predecessor's judgement calls without understanding the reason; several will be deliberate and defensible.
- Record the handover date, what was received, and what was not, in `artifacts/handover-<date>.md`. When something is missing two years later, that record is the only thing that establishes it was never there.

**Write when this file produced something durable**: the diagnostic and the plan → `artifacts/cleanup-plan-<date>.md` with its `## Boxes` line, and the engagement in `~/Clawic/data/projects/<project>.md` when it spans months. The restart point and its source → `## Period Status`. A handover taken over from a predecessor, with what was and was not received → `artifacts/handover-<date>.md` with its `## Boxes` line. Each period as it closes → `closes/<year>.md`. Every rule decided while coding the backlog → `## Coding Rules`. Open questions for the client → `## Open Items` (`memory-template.md`).
