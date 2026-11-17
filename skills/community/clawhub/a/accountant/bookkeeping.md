# Bookkeeping — The Chart, The Entry, The Coding Decision

The daily craft: where a transaction goes, what the entry looks like, and why the trial balance is out.

**Before coding anything**, read the chart at `chart_of_accounts` (default `~/Clawic/data/accountant/chart-of-accounts.md`) and `## Coding Rules` in `~/Clawic/data/accountant/memory.md` (or `coding-rules.md` if `## Boxes` points there). Inventing an account that already exists under another name is the most common way a chart becomes unreadable, and re-deciding a coding question the user already answered is how two months of the same vendor end up in two accounts.

**Contents:** [Designing The Chart](#designing-the-chart) · [Coding A Transaction](#coding-a-transaction) · [Entries People Get Wrong](#entries-people-get-wrong) · [Cash And Accrual, And Converting Between Them](#cash-and-accrual-and-converting-between-them) · [Opening Balances](#opening-balances) · [When The Trial Balance Is Out](#when-the-trial-balance-is-out) · [Subledgers And Control Accounts](#subledgers-and-control-accounts)

## Designing The Chart

Standard numbering, because every accountant and every piece of software expects it. A chart already declared in `chart_of_accounts` overrides these ranges: record what is actually there and use this table only for the gaps in it.

| Range | Class | Ordering inside the range |
|---|---|---|
| 1000-1999 | Assets | Most liquid first: cash, receivables, inventory, prepaid, fixed |
| 2000-2999 | Liabilities | Current before long-term |
| 3000-3999 | Equity | Capital, draws/distributions, retained earnings |
| 4000-4999 | Revenue | Operating revenue before other income |
| 5000-5999 | Cost of goods sold | Mirrors the revenue lines it belongs to |
| 6000-7999 | Operating expenses | Grouped: people, occupancy, technology, marketing, professional |
| 8000-9999 | Other income and expense, tax | Below the operating result on purpose |

- **Create an account only for a distinction that will change a decision.** "Software" and "hosting" earn separate accounts if one gets cut and the other does not; "Figma" and "Notion" do not — that is a vendor, and vendors are already a dimension of every transaction.
- **Detail belongs in a second dimension**: class, department, location, project, tracking category. A chart of 40 accounts × 6 departments answers more questions than 240 accounts, and stays codeable by a human.
- **COGS is what varies with delivery**, not what feels important to the business. Contractor time on client work is COGS; the same contractor on internal tooling is an operating expense. The split is what makes gross margin mean something (`statements.md`).
- **Match the chart to the return.** If a tax form has a line for it, having an account for it turns filing into copying. Accounts that do not map anywhere are the ones nobody can explain in an examination.
- Leave gaps of 10 between codes. Renumbering a live chart rewrites every report definition and every rule.
- Retire, never delete: closed periods still reference the account. Mark it retired with a date and stop it appearing in the picker.

## Coding A Transaction

Four questions, in order. Each one eliminates a class of error before the next is asked.

1. **Is it a P&L event at all?** Transfers between the entity's own accounts, loan drawdowns and repayments, owner contributions and draws, and tax collected on behalf of an authority are all balance-sheet movements. Coding any of them to income or expense is a misstatement, not a preference.
2. **Which period?** The event date, not the payment date, on accrual basis. Cash basis uses the money date. Never both in one set of books (SKILL.md Rule 2).
3. **Which account?** The chart, then the standing rule, then — only if neither answers — a new decision that gets written to `## Coding Rules` in the same turn.
4. **What proves it?** The document reference goes in the memo. An entry whose memo says "transfer" survives nothing.

**Splits.** A single payment covering several things is several lines, not an average. A card payment covering software, a meal, and a personal item is three lines, the last one to owner draws (`owner-pay.md`).

**Unclear transactions** go to a suspense or "ask the client" account with a note naming what is needed, and appear in `## Open Items`. They never get a plausible guess: a wrong code that looks right is never found again, while a suspense balance is found at every close.

## Entries People Get Wrong

| Transaction | Wrong entry | Correct entry |
|---|---|---|
| Loan payment of 1,000, of which 180 is interest | Dr 1,000 loan expense | Dr 820 loan liability / Dr 180 interest expense / Cr 1,000 cash |
| Asset bought on finance | Dr expense for the deposit only | Dr asset at full cost / Cr cash deposit / Cr finance liability for the balance |
| Customer prepayment | Dr cash / Cr revenue | Dr cash / Cr deferred revenue, released as delivered (`revenue.md`) |
| Refund issued to a customer | Dr expense | Dr revenue or contra-revenue / Cr cash — a refund reverses a sale, it is not a cost |
| Supplier refund or rebate received | Cr revenue | Cr the original expense account — otherwise both revenue and costs are inflated |
| Owner pays a business cost personally | Nothing, or Dr expense / Cr cash | Dr expense / Cr owner contribution (or a due-to-owner liability if it is to be repaid) |
| Business card pays a personal cost | Dr expense | Dr owner draws / Cr card (SKILL.md Rule 6) |
| Payroll paid | Dr wages for the net amount | Full gross-to-net entry (`payroll.md`) |
| Sales tax charged to a customer | Cr revenue for the gross | Cr revenue net / Cr sales tax payable (`sales-tax.md`) |
| Processor deposit | Cr revenue for the net deposit | Cr revenue gross / Dr fees / Dr refunds, deposit clears the processor account (`reconciliation.md`) |
| Deposit paid to a supplier | Dr expense | Dr prepaid or supplier advance; expense when delivered |
| Write-off of an unpaid invoice | Delete the invoice | Dr bad debt or allowance / Cr receivable (`receivables.md`) |

## Cash And Accrual, And Converting Between Them

| | Cash basis | Accrual basis |
|---|---|---|
| Revenue recognized | When money arrives | When earned — delivered or performed |
| Expense recognized | When money leaves | When incurred — goods or service received |
| Receivables and payables | Not on the balance sheet | Control accounts, with subledgers |
| Deferred and prepaid | Do not exist | Adjusting entries at each close |
| What it answers well | Can I pay next week | Did last month make money |
| What it hides | Whether the profit was earned or just collected | How near the cash actually is |

Conversion formulas, both directions — these are the only correct way to answer "what would this look like on the other basis":

- Accrual revenue = cash receipts + closing receivables − opening receivables − closing deferred revenue + opening deferred revenue
- Accrual expense = cash paid + closing payables − opening payables + closing prepaid − opening prepaid
- Cash profit = accrual profit − the movement in receivables + the movement in payables − the movement in prepaid + the movement in deferred revenue, with non-cash items (depreciation, provisions) added back

Modified cash — cash for revenue and operating costs, accrual for capital items and payroll — is legitimate and common for small entities, but it must be written down as a policy or it becomes "whichever was easier this month" (`artifacts/`).

## Opening Balances

The most damaging entries in any set of books, because everything after them inherits the error.

- Opening balances come from the **prior year's closing trial balance**, filed return, or the previous accountant's final statements — in that order of authority. Never from a bank balance alone: that gives cash and nothing else.
- Enter them dated the day **before** the first period, so the first period's reports are not distorted.
- The offset for an incomplete set of opening balances is a suspense account, never retained earnings. Retained earnings absorbs the plug invisibly; suspense screams until the missing figures arrive.
- Receivables and payables are entered as **individual open items**, not as one lump into the control account. A lump makes the subledger permanently untieable (→ Subledgers And Control Accounts).
- Record the source and date of the opening balances in `## Period Status`. The next question anyone asks about year one is where the starting numbers came from.

## When The Trial Balance Is Out

Work the arithmetic before hunting transactions. The size of the difference names the error type.

| Test on the difference | Error it indicates | Where to look |
|---|---|---|
| Divides evenly by 9 | Transposition — 540 entered as 450 | Digits of the difference: 9 → adjacent digits swapped; 90 → across a place; the magnitude tells you the column |
| Divides evenly by 2 | One amount posted on the wrong side | Search for half the difference; that amount is sitting as a debit where it should be a credit |
| Equals a round transaction amount exactly | One side of an entry missing entirely | Search the amount; the entry has one leg |
| Equals the sum of a small set | Several entries imported twice | Compare entry counts by day against the source |
| Cannot be decomposed | Not an entry error — a report boundary | Check the date range, whether draft entries are included, and whether a multi-currency account is being shown in two currencies (`currency.md`) |

Then bisect: run the trial balance for the first half of the period, then the quarter containing the break. Four passes finds a single bad entry in a year of data.

**Write when this file produced something durable**: a new or renumbered account, or a retirement → `chart-of-accounts.md`. A coding decision that will recur, with its accrual discipline → `## Coding Rules`. Opening balances and their source → `## Period Status`. A transaction nobody could resolve → `## Open Items`. A basis or modified-cash policy → `artifacts/` with its `## Boxes` line (`memory-template.md`).
