# Working File Templates — Accountant

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/accountant/config.yaml` | Key by key, read-modify-write |
| Entity context, systems, period status, registrations, open items, due dates, box index | `~/Clawic/data/accountant/memory.md` | Rewritten in place; stays small |
| The chart of accounts actually in use | `~/Clawic/data/accountant/chart-of-accounts.md` | Born as its own file the first time a chart exists — it is read whole, every time something is coded |
| Standing rules for coding a recurring transaction, and which accrual discipline each account uses | `## Coding Rules` in `memory.md`; `~/Clawic/data/accountant/coding-rules.md` past the split | One row per rule |
| Recurring journal entries and amortization schedules — prepaids, deferred revenue, depreciation runs | `~/Clawic/data/accountant/recurring-entries.md` | Born with the first schedule; read at every close |
| Periods closed, with their trial-balance and headline totals | `~/Clawic/data/accountant/closes/<year>.md` | Append-only, cut by year, born with the first close |
| Returns and statutory filings actually submitted, with totals and confirmation references | `~/Clawic/data/accountant/filings/<year>.md` | Append-only, cut by year, born with the first filing |
| Fixed asset register: cost, in-service date, method, life, accumulated depreciation, disposal | `## Fixed Assets` in `memory.md`; `~/Clawic/data/accountant/asset-register.md` past the split | One row per asset |
| Headline results per period — revenue, gross margin, net income, closing cash | `## Results` in `memory.md`; `~/Clawic/data/accountant/results.md` past the split | One row per period |
| Entities whose books are kept here, beyond the first | `## Books` in `memory.md`; `~/Clawic/data/accountant/entities.md` from the second | One row per entity |
| Bank, card, loan, and payment-processor accounts: institution, last four, ledger account, last reconciled | `~/Clawic/data/finances/accounts.md` (**shared**) | One row per account, every source in one place |
| A recurring vendor charge recognized as a standing commitment | `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row per service |
| The budget the actuals are compared against | `~/Clawic/data/finances/budget.md` (**shared**) | One row per line, per period |
| A named human — a client, their tax preparer, a vendor's billing contact | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, keyed by the `Key` column; a file per person past 15 |
| A cleanup, migration, or implementation engagement that spans months | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project |
| Things you produced that get re-read — accounting policies, a position taken and why, the close procedure, an audit or lender package, a produced statement set, a reasonable-compensation determination, a cleanup plan, a restatement memo, the log of an examination, the record of a handover taken over from a predecessor | `~/Clawic/data/accountant/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| **Anything durable this table does not name** | `~/Clawic/data/accountant/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind, including anything the user pastes | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| An account was reconciled, or a difference was found and explained | `Last reconciled` in `~/Clawic/data/finances/accounts.md`; the explanation in `## Open Items` if it is not yet resolved |
| A bank, card, loan, or processor account was discovered, opened, or closed | Its row in `~/Clawic/data/finances/accounts.md` |
| A period was closed and locked | A row in `closes/<year>.md`, and the period in `## Period Status` |
| Headline figures for a period were produced | `## Results` |
| A return was filed, or a payment to a tax authority was made | A row in `filings/<year>.md`, and the next date in `## Due` |
| A tax or statutory registration was obtained, changed, or ended | `## Registrations` |
| A coding decision was made that will repeat | `## Coding Rules` |
| The chart of accounts was created, extended, or renumbered | `chart-of-accounts.md` |
| A recurring accrual, prepaid, deferred-revenue, or depreciation schedule was set up | `recurring-entries.md` |
| An asset was capitalized, revalued, or disposed of | `## Fixed Assets` |
| A recurring vendor charge was recognized as a standing commitment | Its row in `~/Clawic/data/finances/subscriptions.md` |
| A budget was agreed or revised | `~/Clawic/data/finances/budget.md` |
| A named person was identified — client, preparer, vendor billing contact | Their row in `~/Clawic/data/contacts/contacts.md` |
| A policy, position, procedure, package, or plan came out of the session | `artifacts/` |
| A cleanup or migration engagement was scoped or advanced | `~/Clawic/data/projects/<project>.md` |
| The user declared a preference | Its key in `config.yaml` |
| Recurring work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except the chart of accounts, recurring entries, closes, filings, artifacts, and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings, and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/accountant/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite. The mapping is fixed: `## Coding Rules` → `coding-rules.md`, `## Fixed Assets` → `asset-register.md`, `## Results` → `results.md`, `## Books` → `entities.md`.
4. Never leave a copy behind. If the same figure ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

The chart of accounts, recurring entries, closes, filings, and artifacts are the exception: each is born as its own file whatever its size, because each is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Accounting texts are dense in them: a bank letter carries the full account number, a payroll export carries national IDs, a software migration note carries the login. Replace each value before writing, in this shape: `<kind>:<locator>`.

`keychain:bank-main` · `1password:Work/Xero` · `bitwarden:Accounting/Payroll` · `env:PAYROLL_API_KEY` · `vault:finance/efile` · `file:~/Documents/efile.p12`

When the user pastes something to save, strip each secret value before writing and leave the pointer visible: `login: <1password:Work/Xero>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: legal and trading names, tax registration numbers (EIN, VAT, GST, UTR), ledger account codes and names, account nicknames and last four digits, institution names, invoice and check numbers, amounts and dates, filing confirmation references, customer and vendor names, asset serial numbers. **Secrets, strip them**: online banking and accounting-software passwords, multi-factor seeds and backup codes, full bank account and routing or IBAN digits, full card numbers, expiry and CVV, e-file and self-select PINs, national identification numbers of any person including the owner, direct-deposit instructions, bank-feed and payroll API tokens, and any scan or export that contains one of these.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [chart-of-accounts.md](#chart-of-accountsmd) · [recurring-entries.md](#recurring-entriesmd) · [closes/](#closes) · [filings/](#filings) · [shared accounts box](#shared-accounts-box) · [shared subscriptions box](#shared-subscriptions-box) · [shared budget box](#shared-budget-box) · [shared contacts box](#shared-contacts-box) · [shared projects box](#shared-projects-box) · [artifacts/](#artifacts) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/accountant/` if it does not exist.

```yaml
jurisdiction: US-CA
accounting_basis: accrual
reporting_framework: us-gaap
entity_type: s-corp
fiscal_year_end: 12-31
base_currency: USD
ledger_software: xero
materiality_pct: 0.5
capitalization_threshold: 2500
close_target_days: 8
chart_of_accounts: ~/Clawic/data/accountant/chart-of-accounts.md

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  account_numbering: "1000 assets, 2000 liabilities, 3000 equity, 4000 revenue, 5000 COGS, 6000 expenses"
  tracking_categories: [Department, Project]
work_order:
  posting: propose-then-confirm
restrictions:
  never_post_to: ["3200 Retained Earnings"]
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Accountant Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Chart of accounts (54 accounts) → `chart-of-accounts.md`; read before coding anything or naming an account
- Recurring entries (7 schedules) → `recurring-entries.md`; read at every close, before posting adjustments
- Closes 2026 (6 periods) → `closes/2026.md`; read before closing a period or comparing months
- Filings 2026 (9 filed) → `filings/2026.md`; read before any return, and before answering "did we file that"
- Asset register (22 assets) → `asset-register.md`; read before capitalizing, depreciating, or disposing
- Revenue recognition policy → `artifacts/policy-revenue-recognition.md`; read whenever an unusual contract is booked
- Reasonable compensation determination 2026 → `artifacts/reasonable-comp-2026.md`; read before changing owner pay

## Due
| What | Every | Last run | Next due |
|---|---|---|---|
| Bank and card reconciliation | month | 2026-06-30 | 2026-07-31 |
| Month-end close | month, 8 business days after end | 2026-06-11 | 2026-07-13 |
| Payroll tax deposit | semiweekly, per the deposit schedule | 2026-07-22 | 2026-07-29 |
| Sales tax return | quarter | 2026-07-20 | 2026-10-20 |
| Estimated income tax | quarter | 2026-06-15 | 2026-09-15 |
| Contractor information returns | year, by Jan 31 | 2026-01-28 | 2027-01-31 |
| Stock count | quarter | 2026-06-30 | 2026-09-30 |

## Books
Northwind Studio LLC, S-corp election, US-CA, FY ends 12-31, accrual, Xero since 2024-01.

## Systems
Xero, two bank feeds (operating, savings), Stripe and a card processor, Gusto for payroll, receipts via the mobile app.

## Period Status
Closed and locked through 2026-06. 2026-07 open; card account unreconciled from 2026-07-16.

## Registrations
| Type | Authority | Number | Frequency | Since |
|---|---|---|---|---|
| Sales tax | CA CDTFA | 123-456789 | quarterly | 2024-03 |
| Payroll | IRS + CA EDD | EIN 12-3456789 | semiweekly deposits, quarterly return | 2024-01 |

## Coding Rules
| What it looks like | Account | Accrual discipline | Note |
|---|---|---|---|
| Stripe payout | 1050 Stripe clearing, not revenue | n/a | gross revenue and fees booked from the Stripe report, payout clears the account |
| AWS invoice | 6210 Hosting | reverse-next-period | invoice always arrives after close |
| Landlord ACH | 6100 Rent | post-against-liability | accrual stands, invoice posts to the liability |

## Fixed Assets
| Asset | In service | Cost | Method | Life | Accumulated | Disposed |
|---|---|---|---|---|---|---|
| MacBook Pro M4 | 2025-11-04 | 3,200 USD | straight-line | 3 yr | 800 USD | — |

## Results
| Period | Revenue | Gross margin | Net income | Closing cash | Basis |
|---|---|---|---|---|---|
| 2026-Q1 | 184,300 USD | 71% | 22,100 USD | 96,400 USD | accrual |
| 2026-Q2 | 201,750 USD | 69% | 18,900 USD | 88,200 USD | accrual |

## Open Items
- 2026-07-16 card difference 412.55 USD, not yet located; suspect a duplicated refund
- Three transactions awaiting the client's answer on business purpose, total 1,240 USD

## How They Work
Wants the journal entry, not the theory. Signs off on write-offs personally. Hates being asked for documents twice.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. A missed filing date costs money, so this table outranks whatever else the session was about. Every recurring thing this skill schedules belongs here.
- **`## Period Status`**: one line for the last locked period plus every account that is not reconciled and since when. This is what Rule 3 reads before answering any "how are we doing" question.
- **`## Results`**: one row per period, always the same shape, always labelled with its basis. Re-checking an open period **overwrites** its row; never a second row for the same period. A period whose books were later corrected gets its row updated, not appended.
- **`## Coding Rules`**: the `Accrual discipline` column is not optional — it is what stops the same cost being counted twice (SKILL.md, Adjusting Entries).
- Amounts always carry their currency inside the value (`3,200 USD`), because a foreign-currency entity's rows sit in the same tables.
- These headings are exactly the ones the split-out files inherit, so a split stays a copy-paste.

| Status | Meaning |
|---|---|
| `ongoing` | Still learning the entity, its chart, and its habits |
| `complete` | Chart, cadence, and treatment decisions are all recorded |

## chart-of-accounts.md

Born the first time a chart exists — never invented preemptively, and never a copy of a generic template. If the user's ledger already has one, this file records what is actually there.

```markdown
# Chart of Accounts — Northwind Studio LLC
*Read before coding a transaction or creating an account. Source: Xero, exported 2026-07-26.*

| Code | Account | Type | Used for | Notes |
|---|---|---|---|---|
| 1010 | Operating checking | Asset | main account | reconciled monthly |
| 1050 | Stripe clearing | Asset | payout timing | must be near zero after each payout clears |
| 1200 | Accounts receivable | Asset | control account | never post journals directly (SKILL.md ties) |
| 1500 | Equipment | Asset | items ≥ 2,500 USD | paired with 1590 |
| 1590 | Accumulated depreciation — equipment | Contra-asset | | |
| 2100 | Accounts payable | Liability | control account | |
| 2200 | Sales tax payable | Liability | tax collected | cleared by the return |
| 2300 | Deferred revenue | Liability | prepaid engagements | schedule in recurring-entries.md |
| 3100 | Member capital | Equity | contributions | |
| 3150 | Member draws | Contra-equity | owner withdrawals | never an expense |
| 4000 | Services revenue | Revenue | | |
| 5000 | Contractor costs | COGS | delivery labor | |
| 6210 | Hosting | Expense | | |
```

- **A new account is created only for a distinction that changes a decision.** Everything else is a class, department, or tracking category (SKILL.md, Where Experts Disagree).
- Record retired accounts as a `retired: <date>` note rather than deleting the row: closed periods still reference them.
- Where the user's declared numbering scheme differs from the one above, follow theirs — `config.yaml` holds the scheme, this file holds the accounts.

## recurring-entries.md

Every schedule that has to be posted again next period. Read at every close, before any adjustment is written.

```markdown
# Recurring Entries
*Read at every close. Updated 2026-07-26.*

| Schedule | Entry | Amount per period | Periods | Started | Ends | Remaining balance |
|---|---|---|---|---|---|---|
| Insurance prepaid | Dr 6400 Insurance / Cr 1300 Prepaid | 275 USD | 12 | 2026-03-17 | 2027-03-16 | 2,200 USD |
| Acme retainer deferral | Dr 2300 Deferred revenue / Cr 4000 Revenue | 4,000 USD | 6 | 2026-05-01 | 2026-10-31 | 12,000 USD |
| Equipment depreciation | Dr 6800 Depreciation / Cr 1590 Accum. dep. | 89 USD | 36 | 2025-11-04 | 2028-10-31 | 2,400 USD |
```

- The remaining balance column is the tie: it must equal the balance of the prepaid or deferred account after the entry posts. If it does not, one of the two is wrong and the schedule is the more likely one.
- A schedule that has run out is deleted from the table and its final period noted in the close row — a schedule list that only grows gets posted past its end.

## closes/

One file per year, at `~/Clawic/data/accountant/closes/<year>.md`, cut by the period's own year so a year-over-year comparison never spans two files by accident.

```markdown
# Closes — 2026

| Period | Closed on | Locked | Trial balance | Adjustments posted | Left open | Notes |
|---|---|---|---|---|---|---|
| 2026-05 | 2026-06-09 | yes | balanced | 6 | — | first month with the deferred revenue schedule |
| 2026-06 | 2026-07-11 | yes | balanced | 4 | 412.55 USD card difference, tracked in `## Open Items` | closed with the difference disclosed, not plugged |
```

- `Locked` records whether the software's closing date was actually set. A close that was calculated but not locked is not a close (SKILL.md Rule 8).
- Anything left unresolved is named in the row, not smoothed over. This column is the first thing an auditor reads and the first thing the next cleanup needs.

## filings/

One file per year, at `~/Clawic/data/accountant/filings/<year>.md`, cut by the year the filing was submitted.

```markdown
# Filings — 2026

| Filed on | What | Period | Authority | Amount | Reference | Paid |
|---|---|---|---|---|---|---|
| 2026-04-15 | Estimated income tax Q1 | 2026-Q1 | IRS | 6,400 USD | conf 2026-9931 | yes |
| 2026-04-20 | Sales tax return | 2026-Q1 | CA CDTFA | 3,118 USD | conf CDT-88214 | yes |
| 2026-07-20 | Sales tax return | 2026-Q2 | CA CDTFA | 3,402 USD | conf CDT-90776 | yes |
```

- One row per submission, including nil returns — proving a nil return was filed is exactly the case where the record is needed.
- The amount is what the return said, not what was paid, when they differ; a difference goes in `## Open Items` until it clears.
- An amended return is a new row referencing the original, never an edit of it.

## Shared accounts box

Lives at `~/Clawic/data/finances/accounts.md`, shared with every skill that touches money — the user may have none of them installed, so the format travels with this skill.

```markdown
# Accounts

| Account | Institution | Type | Last four | Currency | Ledger account | Last reconciled | Access reference |
|---|---|---|---|---|---|---|---|
| Operating checking | Mercury | bank | 4471 | USD | 1010 | 2026-06-30 | keychain:bank-main |
| Business card | Amex | card | 1009 | USD | 2050 | 2026-06-30 | 1password:Work/Amex |
| Stripe | Stripe | processor | — | USD | 1050 | 2026-07-15 | env:STRIPE_KEY_NAME |
```

- **Identity is `Account` + `Institution`.** Read the file before adding; if that pair is there, update the row in place — it is yours. Never a second row for the same account.
- **`Last reconciled` is this skill's column and its main contribution to the shared box**: every other skill can then see whether a balance is trustworthy. Update it the moment a reconciliation finishes (SKILL.md Rule 3).
- **Closure is part of the inventory.** When an account is closed, delete the row and note the date and final balance in `## Open Items`. A list that only grows stops being an inventory.
- **Amounts and balances carry their currency inside the value** (`4,120 USD`), because rows from other providers arrive in other currencies and someone will add the column up.
- **Foreign columns win.** If the file already exists with a different header, match it and put anything extra in the last column. Never rewrite its header, and never touch a row this skill did not create.
- **Scale cut**: one table while there are ≤15 accounts. Past that, one file per account at `~/Clawic/data/finances/accounts/<account>.md` with the same fields, and `accounts.md` stays as the index (`Account | Institution | Type | → file`). Count before adding the row that would cross it; if the folder already looks like that, follow it.
- Never a full account, routing, IBAN, or card number here — the last four and a `<kind>:<locator>` pointer at most.

## Shared subscriptions box

Lives at `~/Clawic/data/finances/subscriptions.md`. A vendor charge becomes a row here the second time the same vendor bills the same thing — recurring commitments are exactly what a P&L review keeps rediscovering.

```markdown
# Subscriptions

| Service | Category | Amount | Cycle | Next charge | Paid with | Notes |
|---|---|---|---|---|---|---|
| Xero (Northwind) | software | 78 USD | monthly | 2026-08-04 | card ••1009 | coded to 6220 |
```

- **Identity is `Service`**, with the account name in parentheses when one provider bills two accounts separately. Read before adding; if the row exists, update it in place.
- **Amounts carry their currency inside the value** (`78 USD`, not `$78`); an estimated amount carries the date of the estimate in `Notes`.
- **Cancellation deletes the row** and the date goes in `## Open Items`. **No scale cut**: this file stays one table however many rows it holds, because summing it in one read is its only job. If another skill has split it anyway, follow what is there.
- **Foreign columns win**, and never touch a row this skill did not write.

## Shared budget box

Lives at `~/Clawic/data/finances/budget.md`. Written only when the user actually runs against a budget; variance analysis without one is a comparison to last month, which belongs in `## Results`.

```markdown
# Budget — 2026

| Line | Ledger account | Period | Budget | Basis | Notes |
|---|---|---|---|---|---|
| Contractor costs | 5000 | monthly | 14,000 USD | accrual | rises to 18,000 from September |
```

- **Identity is `Line` + `Period`.** Update in place; a revised budget replaces the figure and notes the revision date, it does not add a row.
- Actuals are never written here — they live in `## Results` and in the ledger. A budget file holding actuals goes stale the first time an entry is corrected.
- **Foreign columns win**; never touch a row this skill did not write.

## Shared contacts box

Lives at `~/Clawic/data/contacts/contacts.md`, shared with every skill that touches people. Only a **named human** goes here — the client company or vendor itself stays in `## Books` or the ledger, and duplicating the organization in both is how two skills start contradicting each other.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|---|---|---|---|---|---|---|
| Dana Ortiz | dana@ortizcpa.com | Tax preparer, Ortiz CPA | email | prepares the annual return; wants the trial balance and the asset register by Feb 20 | 2026-07-14 | — |
```

- **Identity is the `Key` column**, written into the row and never left implicit: lowercased email, falling back to a handle, falling back to `<kebab-name>` plus a stable disambiguator. `Preferred channel` is the *kind* of channel, not the address, so it can never serve as the key. Read before adding; if the key is there, update that row in place and **extend** `Context` rather than replacing it — another skill wrote what is already in it.
- Delete a row only when the person is no longer a contact at all, not when one engagement ends.
- **Foreign columns win**: match the header that exists, put anything extra in the last column, and never touch a row this skill did not write.
- **Scale cut**: one table while there are ≤15 people; past that — or the moment one person no longer fits in a row — a `~/Clawic/data/contacts/<name>.md` per person with the same fields as headings, and `contacts.md` stays as the index with the `File` column pointing at each one. Count before adding the row that would cross it; if the folder already looks like that, follow it and never fold it back into one table.
- Never a national ID, a date of birth, or bank details here, whatever the role.

## Shared projects box

Lives at `~/Clawic/data/projects/<project>.md`, one file per project, shared with every skill that tracks work. Used for engagements that span months: a catch-up, a software migration, an audit, a first-year setup.

```markdown
## Accounting workstream
| Date | Milestone | Status | Note |
|---|---|---|---|
| 2026-05-04 | 2024 reconciled forward to 2025-06 | done | opening balances agreed to the prior return |
| 2026-07-01 | Xero conversion balances loaded | in progress | AR subledger still 1,140 USD out |
```

- **Identity is the filename**, one `.md` per project from the first, named after the project as a slug. Read it before appending; create it only when no file for that project exists under any spelling.
- Append under an `## Accounting workstream` heading, creating it if the file exists without one. Never restructure a project file written by another skill.
- **A finished project's file is never deleted** — it is the record of what was done. Closure is a `status:` line inside the file.
- Figures stay in this skill's boxes; the project file carries milestones and references, never a second copy of the numbers.

## artifacts/

One file per thing, at `~/Clawic/data/accountant/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **accounting policy** (capitalization, revenue recognition, costing method, materiality), **position taken and why**, **close procedure**, **audit or lender package**, **produced statement set**, **reasonable-compensation determination**, **cleanup plan**, **restatement memo**, **examination log** (`examination-log-<year>.md`, one dated line per request and per document provided), **predecessor handover** (`handover-<date>.md`, what was received and what was not). Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Policy — revenue recognition
*Read whenever a contract is not a plain time-and-materials engagement. Written 2026-05-12.*

Scope: fixed-fee engagements with milestone billing.
Treatment: revenue recognized as milestones are accepted; billing ahead of acceptance sits in 2300 Deferred revenue.
Why: the performance obligation is the accepted milestone, not the signed contract.
Rejected: recognizing on invoice — it would have pulled 47,000 USD into the wrong quarter.
Reviewed: annually at year-end close, or when a contract shape changes.
```

```markdown
# Reasonable compensation — 2026
*Read before changing owner pay or filing the annual return. Written 2026-01-22.*

Determination: 96,000 USD salary, remainder as distributions.
Basis: role scope, hours, three comparable local postings with their sources and dates, prior-year revenue.
Documents: comparables saved with their retrieval dates; the calculation, step by step.
Review: annually, and whenever the role or revenue changes materially.
```

If the engagement is tracked as a project, the artifact stays here and the project file references it by name — never two copies.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`coding-rules.md` — `## Coding Rules`. The reason this file exists is the accrual-discipline column: without it, the same standing cost gets double-counted every time a new session picks the other convention.

`asset-register.md` — `## Fixed Assets`, plus a `## Disposals` heading once anything is sold or scrapped. Its cost and accumulated-depreciation totals must equal their ledger accounts at every close (SKILL.md ties).

`results.md` — `## Results`, one row per period, oldest first.

`entities.md` — `## Books`, one row per entity: legal name, type, jurisdiction, fiscal year end, basis, software, and which shared accounts belong to it. A second entity is the moment this file appears; two entities inside one `memory.md` is how transactions end up in the wrong books.
