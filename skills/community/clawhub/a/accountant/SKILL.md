---
name: Accountant
slug: accountant
version: 1.0.2
description: 'Keeps books that close: double-entry entries, reconciliation, month-end close, financial statements, and the tax filings that follow. Use when transactions need coding to a chart of accounts, when the books do not balance or a reconciliation is off by an amount nobody can find, when a period has to be closed, locked, or corrected, when accrual versus cash, deferred revenue, prepaid expenses, depreciation, or inventory costing is the question, when payroll entries, contractor 1099s, sales tax or VAT returns, or quarterly estimated taxes come due, when receivables age and a bad debt has to be written off, when owner draws, salary, or distributions need treating, when abandoned or messy books have to be caught up, or when an audit, a lender, or a tax examination is coming. Not for company forecasting and fundraising (`cfo`), personal money decisions (`money`), issuing invoices (`invoice`), archiving received ones (`invoices`), or bank payment operations (`banking`).'
homepage: https://clawic.com/skills/accountant
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 📊
    os:
    - linux
    - darwin
    - win32
    displayName: Accountant
    configPaths:
    - ~/Clawic/data/accountant/
    - ~/Clawic/data/finances/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/accountant/
      - ~/Clawic/data/finances/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/accountant/config.yaml` (what the user declared) and `~/Clawic/data/accountant/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — that index *is* the list of files; never work from a list of names memorized here, because most boxes get created after this skill was written. Read `~/Clawic/data/finances/accounts.md` before any reconciliation, balance, or "which account paid this" question. If none of it exists, work from defaults and say nothing about it. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens.

**Write before the session ends** whenever it produced something durable: a chart of accounts or a coding decision that will repeat; a period closed or reopened; a reconciliation finished, or a difference found and explained; an asset capitalized, depreciated, or disposed; a filing submitted with its totals; a recurring accrual or amortization schedule; a registration or a deadline; a balance the next session must not re-derive — or something the user will read again: an accounting policy, a position taken and why, a close procedure, an audit package, a cleanup plan. `memory-template.md` has every destination, format, and threshold, and is the only file you open in order to write.

**Bank, card, loan, and processor accounts go to the shared box `~/Clawic/data/finances/accounts.md`**, not here: one file holds every account whatever discovered it, so "which accounts exist and when was each last reconciled" answers itself. Standing vendor commitments go to `~/Clawic/data/finances/subscriptions.md`, the budget the actuals are compared against to `~/Clawic/data/finances/budget.md`, a named human — a client, their tax preparer, a vendor's billing contact — to `~/Clawic/data/contacts/contacts.md`, and a cleanup or migration engagement that spans months to `~/Clawic/data/projects/<project>.md`. In every case the entity lives in the shared box and this skill's rows keep only its name.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. Store the pointer and strip the value: `keychain:bank-main`, `1password:Work/Xero`, `env:PAYROLL_API_KEY`, `file:~/Documents/efile.p12`. A full bank account number, a national ID, or an e-file PIN is a credential; the last four and the tax registration number are working data.

Bookkeeping is not data entry — it is the discipline that makes a number defensible six months later, in front of a lender, an auditor, or a tax authority. Produce the journal entry, name the accounts on both sides, and say what tie-out proves it right. Work from defaults immediately: never open with questions about their entity, their software, or how proactive to be. The one exception to silence is `jurisdiction` — while it is unset, name the tax regime, deadlines, and retention rules you are assuming before acting on them. That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale, country) → the Configuration table default.

## When To Use

- **Act-as** — keeping the books: coding transactions, writing journal entries, reconciling accounts, running the close, producing statements, preparing filing figures
- **Advise** — deciding treatment: basis, revenue recognition, capitalization, costing method, entity and owner-pay structure, what an auditor or examiner will ask for
- Something does not tie: the trial balance is out, a reconciliation has a difference, a subledger disagrees with the general ledger, last year's closing balance is not this year's opening balance
- Deadlines and filings: payroll returns, contractor information returns, sales tax or VAT, estimated income tax, annual accounts
- Books that were abandoned, inherited, or migrated between systems and now need catching up or converting
- Not for forecasting, runway, board reporting, or fundraising (`cfo`), personal budgeting and debt decisions (`money`), issuing invoices to clients (`invoice`), or filing supplier invoices as documents (`invoices`) — this owns the ledger those all feed

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "Which account does this go to?" | Chart of accounts first, then the standing coding rule; create an account only for a distinction you will act on | `bookkeeping.md` |
| Trial balance is out of balance | Difference ÷ 9 with no remainder → transposition; difference ÷ 2 → one side posted twice or reversed | `bookkeeping.md` |
| Bank or card does not match the ledger | Build both adjusted balances before hunting a single transaction (Rule 3) | `reconciliation.md` |
| Stripe/PayPal/Shopify deposit does not match sales | The deposit is net of fees, refunds, and chargebacks — book gross, then each deduction | `reconciliation.md` |
| Month-end or year-end close | Dependency-ordered checklist, cutoff, accruals, lock | `close.md` |
| "Are these numbers right?" | Run the tie-outs (→ Statement Ties That Must Hold), then explain the variance | `statements.md` |
| Building or reading a balance sheet, P&L, or cash flow | Indirect-method walk, comparatives, common-size, the ratios that change a decision | `statements.md` |
| Customer has not paid; write-off or chase | Aging buckets, allowance method, write-off entry, DSO | `receivables.md` |
| Vendor bill, unbilled cost, early-pay discount, duplicate payment | Three-way match, accrual for goods received, discount APR formula | `payables.md` |
| Payroll to record, or payroll taxes due | Gross-to-net entry, employer taxes, deposit schedule, PTO accrual | `payroll.md` |
| Employee or contractor? | Control test, the information return, the cost of getting it wrong | `payroll.md` |
| Stock on hand, COGS, margin swinging with buying | FIFO / weighted average / LIFO, perpetual vs periodic, NRV, shrinkage | `inventory.md` |
| Equipment, vehicle, software, or a lease | Capitalization test, depreciation method, book vs tax, disposal, ASC 842 | `fixed-assets.md` |
| Money received before delivery, subscriptions, milestones | Five-step recognition, deferred revenue schedule, gross vs net | `revenue.md` |
| Income tax: entity, deadlines, estimates, deductions, retention | Deadline calendar, safe harbor, book-tax differences, records to keep | `tax.md` |
| Sales tax, VAT, or GST: nexus, registration, returns | Where you owe, what rate, exemption certificates, reverse charge | `sales-tax.md` |
| Owner wants to take money out | Draw vs salary vs distribution by entity type; reasonable compensation | `owner-pay.md` |
| Audit, review, lender request, or a tax examination | PBC package, controls in a small team, what examiners open first | `audit.md` |
| Software: setup, bank feeds, migration, or a feature behaving oddly | Account structure, rules that propose vs auto-post, conversion balances | `software.md` |
| Books are months behind, or inherited in a mess | Diagnose, pick the restart point, reconcile forward — never oldest-first | `cleanup.md` |
| Transaction in another currency, or foreign entity | Functional currency, remeasurement vs translation, realized vs unrealized | `currency.md` |
| Nonprofit, grants, restricted funds | Net asset classes, release from restriction, functional expense allocation | `nonprofit.md` |
| Anything else accounting | Name the two accounts the entry touches and the period it lands in; if you cannot, the transaction is not understood yet — ask one question | — |

Coverage map: `bookkeeping.md` entries and the chart of accounts · `reconciliation.md` making it match · `close.md` the period end · `statements.md` the three statements and ratios · `receivables.md` money owed to you · `payables.md` money you owe · `payroll.md` people costs and returns · `inventory.md` stock and COGS · `fixed-assets.md` capital items and leases · `revenue.md` when income counts · `tax.md` income tax and records · `sales-tax.md` transaction taxes · `owner-pay.md` taking money out · `audit.md` being examined · `software.md` the ledger system · `cleanup.md` catch-up work · `currency.md` foreign currency · `nonprofit.md` fund accounting.

## Core Rules

1. **Every entry balances, and its date decides the period.** Debits = credits on every entry, without exception; the date is the date of the event, not the day it was typed. Cutoff test at close: a cost incurred on the 30th belongs to that month even if the invoice arrives on the 12th of the next one — accrue it (`close.md`).
2. **Basis is declared once and applied to everything.** `accounting_basis` accrual recognizes when earned or incurred, cash when money moves; choosing per transaction produces books that convert to neither. Conversion runs both ways with a formula: accrual revenue = cash receipts + closing AR − opening AR; accrual expense = cash paid + closing AP − opening AP (`bookkeeping.md`).
3. **Reconcile before you report.** No statement, no filing, and no answer to "how did we do" from a period whose bank, card, and processor accounts are unreconciled. Reconciled means the two adjusted balances are equal to the cent: bank statement + deposits in transit − outstanding payments ± bank errors = ledger balance + collections and interest − fees and returned items ± ledger errors. A leftover difference is a finding, never a rounding (`reconciliation.md`).
4. **Materiality is a number set before it is needed.** Threshold = the smaller of `materiality_pct` × annual revenue (default 0.5%) and 5% of pretax income. Below it, correct in the current period; above it, correct the period the error belongs to and say so. Qualitative override, which outranks the arithmetic: anything that flips a profit into a loss, breaches a covenant, changes a filed return, or involves suspected fraud is material at any size.
5. **Capitalize by threshold and life, never by how the result looks.** Capitalize when unit cost ≥ `capitalization_threshold` (default 2,500 — the US de minimis safe harbor for a taxpayer without an applicable financial statement) AND useful life > 1 year. Fail either test and it is an expense. The policy is written once and applied in both directions, including the year profit is embarrassing (`fixed-assets.md`).
6. **The entity is separate; owner money moves through equity.** Personal spend on the business card is a draw, not an expense. A business cost paid personally is a contribution or a reimbursement, never invisible. Coding either through the P&L misstates profit, the tax return, and — for a limited-liability entity — the argument that the entity is separate at all (`owner-pay.md`).
7. **Never delete a posted transaction; reverse it.** A correction is a reversing entry plus the correct entry, both dated in the open period, both carrying a memo naming what they fix. Editing or deleting inside a period already filed silently changes a return somebody signed (→ Escalate To A Licensed Professional).
8. **Close the period, then lock it.** A period is closed when subledgers tie to the general ledger, every account is reconciled, uncategorized and suspense accounts are empty, and the trial balance agrees — then the closing date is locked in the ledger and the totals recorded. A prior period left open is where the next surprise is being written right now (`close.md`).
9. **Every figure in a filing traces to a document, and both outlive the assessment window.** Default retention is the longest window that applies: in the US, 3 years from filing, 6 years if income could be understated by more than 25%, indefinitely where no return was filed, and 4 years for employment tax records. Non-US windows are longer more often than shorter — set `jurisdiction` and check (`tax.md`).

## Debits And Credits

The mechanical core. Get the normal balance right and the entry writes itself.

| Account type | Normal balance | Increases with | Appears on | Closed at year end |
|---|---|---|---|---|
| Asset | Debit | Debit | Balance sheet | No |
| Contra-asset — accumulated depreciation, allowance for doubtful accounts | Credit | Credit | Balance sheet, netted against its asset | No |
| Liability | Credit | Credit | Balance sheet | No |
| Equity — capital, retained earnings | Credit | Credit | Balance sheet | No |
| Contra-equity — owner draws, dividends, treasury stock | Debit | Debit | Balance sheet, netted against equity | Yes, into retained earnings |
| Revenue | Credit | Credit | Income statement | Yes, into retained earnings |
| Contra-revenue — returns, allowances, sales discounts | Debit | Debit | Income statement, netted against revenue | Yes |
| Expense and COGS | Debit | Debit | Income statement | Yes, into retained earnings |

- **Cash test**: if money moved, one side of the entry is a cash, card, or clearing account. If neither side is a balance-sheet account, no money moved and the entry is a reclassification — date it in the open period and memo what it fixes (Rule 7).
- **Contra accounts are never debited away.** Reducing accumulated depreciation to make a balance sheet look better destroys the asset register tie (→ Statement Ties That Must Hold).
- **Suspense and "uncategorized" are transit accounts, not destinations.** Any balance in one at close is an unfinished entry, and it is wrong by exactly that amount (`close.md`).

## Adjusting Entries

Six shapes cover almost every adjustment. Each one exists because cash timing and economic timing differ.

| Adjustment | Situation | Entry |
|---|---|---|
| Accrued expense | Cost incurred, invoice not yet received | Dr expense / Cr accrued liabilities |
| Accrued revenue | Delivered, not yet billed | Dr unbilled receivable / Cr revenue |
| Deferred revenue | Billed or collected before delivery | On receipt Dr cash / Cr deferred revenue; on delivery Dr deferred revenue / Cr revenue |
| Prepaid expense | Paid before consumption | On payment Dr prepaid asset / Cr cash; each period Dr expense / Cr prepaid |
| Depreciation and amortization | Capital item in service | Dr depreciation expense / Cr accumulated depreciation |
| Valuation allowance | Estimated uncollectible, obsolete, or impaired | Dr the matching expense / Cr the allowance account |

**The double-count rule.** An accrual and the real invoice both hitting expense is the single most common close error. Pick one discipline per account and never mix them: (a) reverse the accrual on the first day of the next period and let the invoice post normally, or (b) leave the accrual standing and post the invoice against the liability, not the expense. Record which discipline each account uses in `## Coding Rules` (`memory-template.md`) — the next person will otherwise pick the other one.

**Straight-line amortization formula** for a prepaid or a deferral: monthly amount = total ÷ number of periods covered, with the first and last month prorated by days if the term does not start on the 1st. A twelve-month insurance policy starting the 17th is 12 full months of coverage and 13 lines in the schedule.

## Statement Ties That Must Hold

Run these before any number leaves the session. Each is an equality; a break names its own cause.

| Tie | Both sides | What a break usually means |
|---|---|---|
| The balance sheet balances | Assets = Liabilities + Equity | An unbalanced import, or an opening balance never entered |
| Profit reaches equity | Net income for the period = change in retained earnings + distributions − contributions | Someone posted directly to retained earnings, or a closed period moved |
| Cash foots to the bank | Closing cash on the cash flow statement = balance sheet cash = sum of reconciled account balances | An unreconciled account, or a term deposit misclassified as a cash equivalent |
| Subledgers tie to the ledger | AR aging total = AR control account; AP aging total = AP control account | A journal entry posted straight to the control account, bypassing the subledger |
| Payroll ties | Gross wages on the period's payroll returns = wage expense in the ledger ± the accrual movement | Net-pay-only postings (→ Traps) |
| Transaction tax ties | Sales tax / VAT liability balance = returns filed and unpaid + tax collected since the last return | Tax collected booked as revenue (`sales-tax.md`) |
| Inventory ties | Count × the costing method = the inventory account | Purchases expensed on payment, or shrinkage never booked (`inventory.md`) |
| Fixed assets tie | Asset register totals for cost and accumulated depreciation = their ledger accounts | An asset disposed of in the world and not in the books (`fixed-assets.md`) |
| Year over year | Closing balance of every balance-sheet account = the next year's opening balance | A prior period edited after it was closed (Rule 8) |

## Escalate To A Licensed Professional

Observable signals that outrank every protocol in this skill. Judgement here is not conservatism — each of these carries personal liability, a penalty regime, or a licence requirement.

| Signal (observable) | Suspicion | Action |
|---|---|---|
| Payroll taxes were withheld from staff and not deposited | Trust-fund money spent; personal liability attaches to whoever controlled the funds | Escalate the same day, before any other bookkeeping work |
| A period already filed with a tax authority needs its numbers changed | This is an amended return, not an edit | Stop; a tax professional decides amendment vs adjustment in the current period |
| Statements are requested as "audited", "reviewed", or "compiled" | Those are attestation engagements reserved to licensed practitioners | Produce the figures, refuse the label, name what a licensed engagement would add |
| A transaction is described as needing to "not show", or cash revenue is being excluded | Evasion, not planning | Stop, decline, and record the request in one line in `## Open Items` |
| Ownership changes, a partner joins or leaves, or an entity is converted | Tax consequences depend on facts a ledger does not hold | Tax counsel before any entry is posted |
| Sales into a new state or country crossed a threshold | Registration obligations run from the crossing date, with penalties and interest | Specialist before the next return (`sales-tax.md`) |
| The entity cannot pay its taxes, or insolvency is on the table | Priority of claims and director duties change the rulebook | Licensed advisor plus counsel |
| Records are missing for a period under examination | Reconstruction has evidentiary rules | Tax counsel decides what is reconstructed and how |
| A difference survives reconciliation and grows across periods | Undetected fraud or a broken conversion | Stop reporting from those books until it is explained (`audit.md`) |

Anything in this table suspends the protocols above: route to a licensed accountant, tax adviser, or counsel, and say in one line why.

## Output Gates

Before delivering an entry, a statement, a filing figure, or a "here is where you stand":

- Does every entry balance, name both accounts explicitly, and carry a date inside an open period?
- Is the period reconciled, or have I said out loud which accounts are not and what that leaves uncertain (Rule 3)?
- Did I run the ties that apply to this number (→ Statement Ties That Must Hold), rather than trusting the software's total?
- Is every figure stated on the declared basis and in `base_currency`, with the period labelled and comparatives on the same basis?
- Does anything here depend on a jurisdiction rule, rate, or limit that is indexed or was recently legislated? Then it is looked up for the filing year, not carried over from last year.
- Is anything in the Escalate table present? Then that is the answer, before the accounting.
- Did anything durable come out of this — a closed period, a reconciliation, a filing, an asset, a coding decision, a policy, an account? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/accountant/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| jurisdiction | text (country, plus state/province) | none | Selects deadlines, thresholds, forms, and retention windows in `tax.md`, `payroll.md`, `sales-tax.md`; while unset, name the regime being assumed before acting on it |
| accounting_basis | cash \| accrual \| modified-cash | accrual | Which recognition rule every entry follows, and whether close includes accruals and deferrals (Rule 2) |
| reporting_framework | us-gaap \| ifrs \| local-gaap \| tax-basis | us-gaap | Statement presentation and the treatment of leases, inventory, and revenue in `statements.md`, `inventory.md`, `fixed-assets.md` |
| entity_type | sole-trader \| partnership \| llc \| s-corp \| c-corp \| nonprofit | sole-trader | Equity account structure, how owners get paid (`owner-pay.md`), which return and deadline apply |
| fiscal_year_end | text (MM-DD) | 12-31 | Period boundaries for close, annual deadlines, depreciation conventions |
| base_currency | text (ISO code) | from `profile.yaml`, else USD | Currency every figure is stated in; a transaction in another currency routes to `currency.md` |
| ledger_software | quickbooks \| xero \| wave \| sage \| freeagent \| spreadsheet \| other | spreadsheet | Which mechanics, feature names, and traps in `software.md` apply |
| materiality_pct | number (% of revenue, 0.1-5) | 0.5 | One input to the materiality threshold in Rule 4 |
| capitalization_threshold | number, in `base_currency` | 2500 | Unit cost at or above which a >1-year item is capitalized (Rule 5) |
| close_target_days | number (business days after period end, 1-20) | 10 | The `## Due` close row, and how far estimates are used instead of waiting for documents |
| chart_of_accounts | path | none | The declared chart of accounts, normally `~/Clawic/data/accountant/chart-of-accounts.md`; overrides the default structure in `bookkeeping.md` |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — ledger software and its edition, receipt capture app, payroll provider, whether the tax return is prepared in-house or handed to a preparer — affects `software.md` and every handoff
- **Conventions** — account numbering scheme, class/department/tracking-category structure, journal memo format, naming of exported statement files — affects `bookkeeping.md` and every entry produced
- **Locale** — jurisdiction and sub-jurisdiction, currency, date format, decimal and thousands separators, language of statement labels — affects `tax.md`, `sales-tax.md`, `currency.md`
- **Risk posture** — appetite on deductions and grey positions, whether to book an estimate or hold the period open for the document, tolerance for an unresolved item at close — affects `close.md` and `tax.md`
- **Output format** — summary vs full-account statements, comparative columns, whether every answer shows the journal entry, internal vs client-facing register — affects `statements.md`
- **Work order** — bank-feed rules first vs manual coding first, whether entries are posted directly or proposed for review, who approves a write-off — affects Output Gates and `software.md`
- **Integrations** — which banks have feeds, payment processors, e-commerce and point-of-sale platforms, expense and payroll tools pushing data in — affects `reconciliation.md`
- **Restrictions** — accounts the agent must never post to, periods locked, related-party transactions needing approval, industry rules such as client-money or trust accounts — affects everything
- **Cadence** — reconciliation frequency, close calendar, receivables review, filing calendar, stock and asset counts — every accepted cadence becomes a row in the `## Due` table of `memory.md`

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Booking a processor payout as revenue | The deposit is net of fees, refunds, and chargebacks — revenue and expenses are both understated, and margin is permanently wrong | Gross revenue, then each deduction to its own account (`reconciliation.md`) |
| Coding a whole loan payment to expense | Overstates expense and never reduces the liability, so the loan balance in the books drifts from the lender's | Split: principal to the loan account, interest to interest expense (`bookkeeping.md`) |
| Sales tax collected recorded as revenue | Inflates revenue and hides money that belongs to a tax authority | Liability on collection, cleared when the return is paid (`sales-tax.md`) |
| Owner draws coded as an expense | Overstates costs, understates equity, and produces a return that is wrong in both directions | Equity draw account (`owner-pay.md`) |
| Transfers between the entity's own accounts booked as income and expense | Double-counts on both sides; revenue looks bigger than it was | A transfer never touches the income statement (`bookkeeping.md`) |
| Payroll posted as one net-pay expense | Hides gross wages, withholdings, and employer taxes, and the payroll return will never tie | Full gross-to-net entry, every liability on its own line (`payroll.md`) |
| Plugging a reconciliation difference to "ask my accountant" | The plug becomes permanent and the real error keeps compounding underneath it | Locate it with the divisible-by-9 and divisible-by-2 tests, then the date-range bisect (`reconciliation.md`) |
| Leaving uncategorized or suspense balances at close | The income statement is wrong by exactly that amount, and nobody who reads it can tell | Empty both before locking (Rule 8) |
| Bank-feed rules set to auto-add | Miscodings post silently and are discovered a year later, across a filed period | Rules propose, a human confirms — auto-add only for a fixed-amount, single-vendor match (`software.md`) |
| Inventory purchases expensed on payment under accrual | Margin swings with buying instead of selling; the inventory account never ties to a count | Asset on purchase, COGS on sale (`inventory.md`) |
| Accruing nothing because the invoice has not arrived | The period misses its own costs and next period carries two months of them | Accrue the estimate, then follow one discipline (→ Adjusting Entries) |
| Starting a cleanup with the oldest month | Every downstream balance moves after each fix, so the same months get redone repeatedly | Reconcile forward from the last known-good balance (`cleanup.md`) |
| Reusing last year's rate, limit, or threshold | Wage bases, mileage rates, contribution limits, and reporting thresholds are indexed or legislated and move | Look up every rate for the filing year; store the year alongside the figure |
| Recording a customer deposit as revenue | Revenue recognized before delivery, and the obligation to refund is invisible | Deferred revenue until the performance obligation is satisfied (`revenue.md`) |
| One chart of accounts account per vendor | The account list becomes a vendor list nobody can read, and the P&L loses meaning | Accounts for decisions, tracking categories or classes for detail (`bookkeeping.md`) |

## Where Experts Disagree

- **Cash vs accrual for a small business.** Cash basis is simpler and matches what a sole trader feels; accrual is the only basis that tells you whether last month made money. The frontier is not size but structure: inventory, deferred revenue, or work billed in a different period from when it is done make cash-basis reports actively misleading. Tax rules can also remove the choice — in the US the gross-receipts test forces accrual above an inflation-indexed ceiling in the low tens of millions, so check it for the year rather than assuming.
- **How many accounts belong in the chart.** One school splits finely so the P&L answers questions directly; the other keeps 30-50 accounts and pushes detail into classes, departments, or tracking categories. The deciding test is not taste: create an account when you will make a different decision because of the split, and a tag when you only want to filter. Fine charts stop working the moment two people code into them.
- **LIFO.** Permitted under US GAAP and prohibited under IFRS, and the US conformity rule means adopting it for tax forces it in the books too. It defers tax while prices rise and traps you in a lower reported profit and a stale inventory value. Reasonable only for a US-only entity with rising costs and no prospect of IFRS reporting or a sale process (`inventory.md`).
- **Estimates at close vs waiting for the document.** Waiting produces an accurate period that arrives too late to act on; estimating produces a timely period that will move. The frontier is materiality (Rule 4) and reversibility: estimate what reverses next month and is below threshold, wait for anything that changes a filing or a covenant.
- **Direct vs indirect cash flow statement.** Standard setters prefer the direct method; almost nobody produces it, because the indirect method falls out of two balance sheets and a P&L while the direct method needs cash flows tagged at source. Produce indirect for reporting; build the direct-method view only when someone is actually managing collections and payments from it (`statements.md`).

## Security & Privacy

**Credentials:** this skill never asks for, stores, logs, or transmits banking passwords, accounting-software logins, e-file PINs, national ID numbers, or payroll provider keys. Where a reference is genuinely needed, only a pointer is stored: `keychain:bank-main`, `1password:Work/Xero`, `env:PAYROLL_API_KEY`.

**Local storage:** the chart of accounts, coding rules, period status, asset register, filing history, and generated artifacts stay in `~/Clawic/data/accountant/` on this machine, plus account rows in the shared `~/Clawic/data/finances/`. Account nicknames, last four digits, tax registration numbers, ledger codes, and amounts only — never a full account number or a national ID.

**Guardrails:** nothing is posted to a locked or filed period; corrections are reversing entries (Rule 7). Any figure destined for a filing is stated with its source document and the year its rules were looked up.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/accountant (install if the user confirms):
- `cfo` — forecasting, runway, budgets, board and lender reporting built on top of these books
- `invoices` — filing and auditing the supplier invoices that become these entries
- `invoice` — issuing invoices to clients, which become receivables here
- `expenses` — day-to-day and shared spending capture before it reaches the ledger
- `billing` — building the payment and subscription systems whose payouts get reconciled here

## Feedback

- If useful, star it: https://clawic.com/skills/accountant
- Latest version: https://clawic.com/skills/accountant

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/accountant.
