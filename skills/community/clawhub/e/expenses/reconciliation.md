# Reconciliation — Making the Log Agree With the Bank

**Before a reconciliation pass**, read the month's `~/Clawic/data/expenses/ledger/<YYYY-MM>.md`, the `## Monthly Totals` row in `memory.md` for its `Reconciled` state, and `~/Clawic/data/finances/accounts.md` so every account is reconciled separately and none is forgotten.

**Contents:** [Two Sources, Two Truths](#two-sources-two-truths) · [Matching](#matching) · [Classify Every Gap Before Fixing Any](#classify-every-gap-before-fixing-any) · [Importing a CSV](#importing-a-csv) · [Cash Cannot Be Reconciled](#cash-cannot-be-reconciled) · [The Residual](#the-residual) · [Fraud and Disputes](#fraud-and-disputes) · [What Reconciled Means](#what-reconciled-means)

## Two Sources, Two Truths

The statement is authoritative for **amount, date and the fact that money moved**. The ledger is authoritative for **purpose, category, beneficiaries and tags**. Neither replaces the other, and the direction of correction follows that split:

- Amount differs → the statement wins, correct the ledger row.
- Category or purpose is missing on the statement → nothing to correct; the statement was never going to have it.
- The entry is absent from the statement → it is pending, it is cash, it is on another account, or it did not happen.

An agent that "reconciles" by overwriting the ledger with the import destroys the half of the data that only the ledger has. Import fills gaps; it never replaces rows that already carry purpose.

## Matching

Match on **amount exact + date within a three-day window**. Card transactions post one to three days after purchase (SKILL.md Rule 2), and a fixed same-day match fails on roughly every weekend purchase.

Widen the window only for known slow posters — hotels settling at checkout, fuel pumps, tolls, small foreign merchants — and never widen it beyond about seven days, because past that the false-match rate exceeds the value.

Foreign entries match on the **home amount as posted**, which will differ from the estimated conversion. That difference is the point of the pass: replace the estimated rate with the settled one and drop the `#rate-estimated` tag (`currency.md`).

Amount mismatches with a plausible cause, in order of frequency: a tip added after authorization, an FX settlement difference, a partial refund already applied, a fuel pump pre-authorization replaced by the real amount, a hotel incidental. Each is a correction to the ledger row, not a new row.

## Classify Every Gap Before Fixing Any

The discipline that makes a pass converge: read all the gaps, label each, then act. Fixing them one at a time as they appear creates duplicates, because the entry you are about to add is often the one you will find three lines later.

| Gap | Almost always | Action |
|---|---|---|
| On the statement, not in the ledger | A missed entry | Add it, tag `#reconstructed`, category from the vendor rule |
| In the ledger, not on the statement, recent | Pending | Tag `#pending`, resolve next pass |
| In the ledger, not on the statement, old | Cash, another account, or an entry that never happened | Check the other accounts first; delete only after that |
| Amount differs | Tip, FX, partial refund, pre-authorization | Correct the ledger row to the posted amount |
| Same amount, same vendor, twice | Either a real repeat or a double charge | Ask nothing — check whether both posted; two postings is real money (`capture.md`) |
| A charge from a vendor the user does not recognize | Possibly fraud, possibly a parent-company billing name | Search the descriptor before alarming anyone; then Fraud and Disputes below |
| Anything else | An account not yet in `finances/accounts.md` | Add the account, then re-run the pass for it |

## Importing a CSV

- **Map the columns once per bank** and store the mapping — banks change nothing about their export for years, and re-deriving the mapping every month is where import time actually goes.
- **Sign convention** varies: some exports use negative for debits, some use separate debit and credit columns, some use positive for everything and a type column. Getting it backwards turns a month of spending into a month of income and the total still looks like a number.
- **Dedupe key: date + amount + last four of the account.** Without it, overlapping export ranges triple the same coffee. With it, genuine repeats on the same day survive only if the key includes a sequence — so treat a key collision as a *candidate*, verify against the statement, and never auto-delete.
- **Never import a range that overlaps an already-imported range** without running the dedupe. Record the imported range per account so the next import starts where the last one ended.
- **Pending rows in an export change.** Import posted rows only, or re-import the pending window next time and let the dedupe reconcile it.
- The vendor string in the export is the canonical one for vendor rules (`categories.md`) — it is what the next import will present, not what the user calls the shop.
- **One account at a time.** A merged multi-account file makes the residual unattributable, and an unattributable residual is one nobody ever chases.

## Cash Cannot Be Reconciled

There is no external record. The wallet count is its reconciliation (`capture.md`):

```
unlogged cash = (previous count + withdrawals) − logged cash spend − current count
```

Withdrawals appear on the statement, so the cash *entering* the wallet is verifiable; only its destination is not. A month whose cash portion is large is reconcilable in its card half and estimated in its cash half — say so rather than reporting the month as clean.

## The Residual

A small, stable difference that will not resolve is not a reason to abandon reconciliation, and chasing it forever is why most people abandon reconciliation.

- If the residual is below roughly a tenth of `receipt_threshold` and does not grow, book **one** adjustment entry — vendor `adjustment`, category `other`, tagged `#reconciliation-adjustment` — and note the date and the amount. One line, closed.
- If it grows month over month, it is not a residual: something systematic is wrong. The usual causes are a sign convention flipped on one import, a duplicated recurring charge, or an account nobody is reconciling.
- Never adjust in the direction that makes a total look better. Record the difference as it is; an adjustment that always goes one way is the same thing as not reconciling.

## Fraud and Disputes

A charge with no matching entry, from an unrecognized descriptor, is handled today, not at month close — dispute windows are finite and they run from the statement date, not from discovery.

1. Search the descriptor: a large share of "unknown" charges are the parent company, the payment processor, or a subscription's billing name rather than the brand.
2. If it is genuinely unrecognized, the user contacts the card issuer. Timing matters: US billing-error rights under the Fair Credit Billing Act require notice within 60 days of the statement, and card-network chargeback windows are commonly around 120 days from the transaction. Confirm the applicable window before relying on either number.
3. In the ledger: keep the row, tag `#disputed`, and set a `## Due` line for the decision date. A disputed charge that is deleted has nothing chasing it.
4. On resolution: a reversal is a negative row referencing the original (`capture.md`); a denied dispute keeps the charge and the reason.
5. If a card is reissued, its last four changes — update `~/Clawic/data/finances/accounts.md` in place, never as a second row, and never store the number itself.

## What Reconciled Means

`Reconciled: yes` on a `## Monthly Totals` row means: every account's statement for that month was matched, every gap was classified and resolved, and any residual was booked. Anything less is `partial`, and a partial month is an estimate that must not be compared against a clean one as though it were data (SKILL.md Rule 6).

Cadence: on `close_day`, per account, for the month just ended (`reports.md`). A month left unreconciled for more than about two statement cycles usually stays unreconciled, because the disputes have expired and nobody remembers the cash — surface that as a fact when it happens.

**Write on the way out.** Every corrected, added or resolved row goes back into `ledger/<YYYY-MM>.md` in the same pass; the `Reconciled` column of the month's row in `## Monthly Totals` is set to `yes` or `partial`; a booked residual is its own tagged row; a dispute writes its `#disputed` tag and its `## Due` decision date; a new account or a reissued card updates its row in `~/Clawic/data/finances/accounts.md` in place; a bank's column mapping and imported range are worth keeping — mapping to `config.yaml` under `tooling`, imported range in the ledger file's header line. Formats in `memory-template.md`.
