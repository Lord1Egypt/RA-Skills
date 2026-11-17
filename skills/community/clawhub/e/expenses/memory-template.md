# Working File Templates — Expenses

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/expenses/config.yaml` | Key by key, read-modify-write |
| Current state, closed-month totals, category system, shared balances, due dates, box index | `~/Clawic/data/expenses/memory.md` | Rewritten in place; stays small |
| Individual expense entries | `~/Clawic/data/expenses/ledger/<YYYY-MM>.md` | Append-only, one file per month, from the very first entry — a log never lives in `memory.md` |
| Category list and vendor→category rules | `## Categories` + `## Vendor Rules` in `memory.md` until they outgrow it, then `~/Clawic/data/expenses/categories.md` | Grows by entries |
| Shared groups: split rule, member balances, settlements | `## Shared Balances` in `memory.md` until a group outgrows it, then `~/Clawic/data/expenses/groups/<group>.md` | One block per group |
| People you split with | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person; here they are a name only |
| Reimbursement and rebillable claims with their status | `~/Clawic/data/expenses/claims/<year>.md` | Append-only, cut by year, born as its own file |
| A bounded spend envelope — renovation, wedding, trip, launch, campaign | `~/Clawic/data/expenses/budgets/<kebab-name>.md` | One file per envelope, from the first |
| Receipt images and PDFs | `~/Clawic/data/expenses/receipts/<YYYY-MM-DD>-<vendor>-<amount><CCY>.<ext>` | One file per receipt; the ledger row holds the filename, never the image |
| Things you produced that get re-read — settlement statements, month and tax-year reports, a written split policy, a claim policy summary | `~/Clawic/data/expenses/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Recurring charges and their renewal dates | `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row per subscription |
| Accounts and cards used as payment methods | `~/Clawic/data/finances/accounts.md` (**shared**) | One row per account; nickname and last four only |
| Household or personal budget targets per category | `~/Clawic/data/finances/budget.md` (**shared**) | One row per category |
| Trip bookings and their locators | `~/Clawic/data/bookings/<year>.md` (**shared, read-only here**) | Read to avoid double-entry; the money still gets its ledger row |
| **Anything durable this table does not name** | `~/Clawic/data/expenses/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Three questions decide anything this table does not name, in order: **would another skill want to read it?** → a shared box. **Is it a text read whole when its subject comes up** — a policy, a settlement statement, a report, a decision? → `artifacts/`. **Is it one more row of something that accumulates?** → a section of `memory.md` until the split threshold, then its own box.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| Any purchase, refund, deposit or duplicate charge was reported | A row in `ledger/<YYYY-MM>.md` |
| A backfill or cash count ran (`capture.md`) | The rows, each flagged `reconstructed` or `cash-unlogged` |
| A category was created, renamed, merged, or a vendor rule was settled (`categories.md`) | `## Categories` / `## Vendor Rules` |
| A receipt was captured or a missing-receipt note written (`receipts.md`) | The file in `receipts/`, its filename in the ledger row |
| A cost was split, or balances moved (`sharing.md`) | The `### <group>` block in `## Shared Balances`, and the ledger row with payer and beneficiaries |
| A group settled up (`sharing.md`) | The settlement line in the group block, plus the statement in `artifacts/` if one was produced |
| A person entered a split for the first time | Their row in `~/Clawic/data/contacts/contacts.md` |
| A claim was assembled, submitted, paid or rejected (`reimbursement.md`) | Its row in `claims/<year>.md` |
| Deductibility was decided, or an apportionment basis was derived (`business.md`) | The ledger row's purpose and basis fields; a recurring basis goes to `artifacts/` |
| A budget envelope was created, committed against, or crossed `budget_alert_pct` (`budgets.md`) | `budgets/<name>.md` |
| A trip started, ran or ended (`travel.md`) | `budgets/<trip>.md`, and the per-day burn line |
| A conversion rate was applied to an entry (`currency.md`) | The three currency fields in the ledger row |
| A reconciliation pass ran, or an import landed (`reconciliation.md`) | `## Monthly Totals` `Reconciled` column, plus corrected ledger rows |
| A month, quarter or tax year was closed (`reports.md`) | `## Monthly Totals`, and the report itself in `artifacts/` |
| A recurring charge was discovered | Its row in `~/Clawic/data/finances/subscriptions.md` |
| A new card or account was used | Its row in `~/Clawic/data/finances/accounts.md` |
| The user declared a preference | Its key in `config.yaml` |
| Recurring work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

The ledger, claims, budgets, receipts and artifacts are born as their own boxes — a log is cut by date and an artifact is read whole, so neither belongs inside `memory.md`. Everything else starts as a section of `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file under `~/Clawic/data/expenses/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite. A `# Title` line at the top of the extracted file is cosmetic and holds no data.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Planned splits and their fixed headings: `## Categories` + `## Vendor Rules` → `categories.md` · `## Monthly Totals` → `monthly-totals.md` · one `### <group>` block → `groups/<group>.md`.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. A pasted bank export, a screenshot transcript, a claim portal page or a "here are my cards" message gets every secret value replaced **before** anything is written. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`keychain:amex-personal` · `1password:Personal/Chase/login` · `bitwarden:Bank/Revolut` · `env:PLAID_ACCESS_TOKEN` · `file:~/Documents/bank-export.csv` · `profile:business-card`

In a text, the pointer goes exactly where the value was: `card: <keychain:amex-personal>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: vendor and merchant names, amounts and currencies, dates, category names, card and account **nicknames**, the **last four digits**, bank names, employer claim and expense-report reference numbers, invoice and PO numbers, business VAT/tax registration numbers, booking locators, mileage and odometer readings. **Secrets, strip them**: full card numbers, CVV, PIN, expiry dates, full bank account numbers, IBAN, routing and sort codes, online banking usernames and passwords, one-time codes and 2FA seeds, API tokens for banking or aggregator apps, personal tax identification numbers, and photographs showing the front or back of a card.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [ledger/](#ledger) · [claims/](#claims) · [budgets/](#budgets) · [receipts/](#receipts) · [artifacts/](#artifacts) · [shared finances box](#shared-finances-box) · [shared contacts box](#shared-contacts-box) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/expenses/` if it does not exist.

```yaml
home_currency: EUR
tax_year_start: 01-01
receipt_threshold: 50
close_day: 3
settle_cadence: month
default_split: equal
budget_alert_pct: 80
mileage_rate: 0.26
private_categories: [health, gifts]

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  ledger_cut: month
  tag_prefix: "#"
platform:
  jurisdiction: ES
  distance_unit: km
split_policy:
  settlement_rounding: whole   # none (default, two decimals) | whole units
  flat-lisbon: "rent by room size, groceries equal, utilities equal"
output_format:
  register: numbers-only
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Expenses Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Ledger, monthly (2025-11 →) → `ledger/<YYYY-MM>.md`; read the months a question actually spans, never all of them
- Kitchen renovation envelope → `budgets/kitchen-reno.md`; read on any renovation spend or "how much is left"
- Japan trip → `budgets/japan-2026.md`; read on any trip spend, and to produce the post-trip summary
- Reimbursement claims (2026) → `claims/2026.md`; read before submitting, and on any "did work pay me back"
- Settlement statement, flat-lisbon May → `artifacts/settlement-flat-lisbon-2026-05.md`; read if that settlement is disputed
- Tax-year pack 2025 → `artifacts/tax-year-2025.md`; read for any question about last year's deductions
- Receipts → `receipts/`; open only the filename a ledger row names

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Month close | month, day 3 | 2026-07-03 | 2026-08-03 |
| Settle flat-lisbon | month | 2026-06-30 | 2026-07-31 |
| Submit work claims | month, day 3 | 2026-07-03 | 2026-08-03 |
| Kitchen budget review | week | 2026-07-20 | 2026-07-27 |
| Receipt retention purge | year | 2026-01-10 | 2027-01-10 |

## Monthly Totals
| Month | Total | As of | Reconciled | Top categories | Notes |
|-------|-------|-------|------------|----------------|-------|
| 2026-06 | 2,410 EUR | 2026-06-30 | yes | housing 900 · food 520 · transport 210 | closed |
| 2026-07 | 1,180 EUR | 2026-07-12 | no | housing 900 · food 190 · transport 60 | month-to-date |

## Categories
housing · food · groceries · transport · health · utilities · subscriptions · work · travel · gifts · other

## Vendor Rules
| Vendor match | Category | Notes |
|---|---|---|
| Mercadona, Lidl | groceries | — |
| Renfe, Cabify | transport | work trips get the `#billable` tag |

## Shared Balances
### flat-lisbon
Rule: rent by room size (Ana 40%, user 35%, Tom 25%); everything else equal. Settle monthly.
| Person | Net | Meaning |
|--------|-----|---------|
| Ana | +140 EUR | is owed |
| user | −95 EUR | owes |
| Tom | −45 EUR | owes |
Settlements: 2026-06-30 user→Ana 95 EUR, Tom→Ana 45 EUR (statement in artifacts/)

## How They Work
Logs by voice, in bursts, usually two days late. Cash-heavy on weekends. Wants the number, never the commentary.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. `close_day`, `settle_cadence` and every recurring thing this skill schedules belong here.
- **`## Monthly Totals`**: `As of` is the day the number was read. A row whose `As of` is not the last day of the month is month-to-date and must never be compared against a closed month (SKILL.md Rule 6). Re-reading the current month **overwrites** its row; never a second row for the same month. `Reconciled` says whether the month was matched against the statements — an unreconciled total is an estimate. Amounts always carry their currency. `Top categories` is the top three, descending, always the same shape: that fixed shape is what makes a twelve-month comparison possible without reopening twelve ledger files.
- **`## Categories`**: the live list, one line. Renaming one here means rewriting every ledger file that used the old name in the same turn (SKILL.md Rule 7), or the rename does not happen.
- **`## Shared Balances`**: one `### <group>` block per group. The `Net` column sums to zero after every write — if it does not, a split is wrong and no further entry gets added until it is found. Positive means owed, negative means owes, stated in the `Meaning` column so nobody reads the sign backwards.
- Never store a person's contact details here; only their name, matching the row in `~/Clawic/data/contacts/contacts.md`.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their categories, groups and rhythm |
| `complete` | Categories stable, groups known, closes running on cadence |

## ledger/

One file per month at `~/Clawic/data/expenses/ledger/<YYYY-MM>.md`, created with the first entry of that month. Append-only: corrections are new rows referencing the original, never edits that erase history.

```markdown
# Ledger — 2026-07

| Date | Amount | Home | Rate | Vendor | Category | Tags | Payer | Method | Beneficiaries | Receipt | Purpose |
|------|--------|------|------|--------|----------|------|-------|--------|---------------|---------|---------|
| 2026-07-04 | 12.40 EUR | 12.40 EUR | — | Mercadona | groceries | | user | amex ·1234 | user | | |
| 2026-07-06 | 8400 JPY | 52.08 EUR | 0.0062 @2026-07-06 | Ichiran | food | #japan-2026 | user | visa ·7788 | user, Ana | 2026-07-06-ichiran-8400JPY.jpg | |
| 2026-07-09 | 240.00 EUR | 240.00 EUR | — | Iberia | travel | #billable | user | amex ·1234 | user | 2026-07-09-iberia-240EUR.pdf | client kickoff, Acme (see contacts) |
| 2026-07-11 | −52.00 EUR | −52.00 EUR | — | Zara | shopping | #refund-of-2026-07-02 | user | amex ·1234 | user | | return |
```

- `Amount` is what was paid, in the currency it was paid. `Home` is `home_currency`. `Rate` is home-per-unit-foreign with the date it applied, and is empty when the two currencies match (SKILL.md Rule 3).
- `Beneficiaries` empty means the payer alone. Any other value makes this a shared entry and requires the group block to be updated in the same turn (SKILL.md Rule 4).
- `Purpose` is mandatory on anything tagged `#billable`, `#claim` or business — written at payment, never reconstructed.
- Empty cells are left empty. A field genuinely unknown is written `unknown`, which is a flag for the next reconciliation pass, not a permanent state.
- Flags that live in `Tags`: `#reconstructed` (backfilled from a statement, not from memory), `#cash-unlogged` (the wallet-count difference), `#pending` (seen on the card but not posted), `#refund-of-<date>`, plus the user's own project and trip tags.

## claims/

`~/Clawic/data/expenses/claims/<year>.md`. Cut by year because a claim's life is measured in weeks and its audit life in years.

```markdown
# Claims — 2026

| Claim | Submitted | Period | Lines | Amount | Status | Paid | Ledger tag |
|-------|-----------|--------|-------|--------|--------|------|------------|
| WK-2026-06 | 2026-07-03 | June | 7 | 312.40 EUR | reimbursed | 2026-07-18 | #claim-2026-06 |
| ACME-01 | 2026-07-20 | July | 3 | 340.00 EUR | submitted | — | #billable |
```

Status ladder: `draft` → `submitted` → `approved` → `reimbursed`, plus `rejected` with the stated reason in a note. A rejected claim keeps its row; deleting it loses the reason and the same line gets rejected again next quarter.

## budgets/

One file per envelope at `~/Clawic/data/expenses/budgets/<kebab-name>.md`, created when the envelope is agreed, not when the first money moves. Trips, renovations, weddings, launches and campaigns all use this shape.

```markdown
# Kitchen renovation
*Read on any renovation spend, and on "how much is left". Opened 2026-05-02.*

Envelope: 18,000 EUR · Contingency: 2,700 EUR (15%) · Alert at 80%
Project entry: `~/Clawic/data/projects/kitchen-reno.md` (name only — the plan lives there, the money lives here)

| Line | Budgeted | Committed | Paid | Remaining | Note |
|------|----------|-----------|------|-----------|------|
| Cabinets | 7,000 EUR | 7,240 EUR | 3,620 EUR | −240 EUR | quote signed 2026-06-11, 50% deposit paid |
| Appliances | 4,000 EUR | 0 EUR | 0 EUR | 4,000 EUR | not ordered |

Status 2026-07-26: 7,240 EUR committed of 18,000 EUR (40%), 3,620 EUR paid. Contingency untouched.
```

- **Committed counts before it is paid.** A signed quote or a placed order consumes the envelope on the day it is signed; `budget_alert_pct` is measured against committed, not paid (`budgets.md`).
- Every paid line still gets its ledger row with the envelope's tag. This file is the envelope view; the ledger is the record.
- When the envelope closes, write the final variance line and move the file's `## Boxes` condition to "read only for reference".

## receipts/

Files, not text: `~/Clawic/data/expenses/receipts/<YYYY-MM-DD>-<vendor>-<amount><CCY>.<ext>`, lowercase kebab vendor, no spaces. The ledger row holds the filename; nothing else points at these. Two receipts on the same day from the same vendor get `-2` appended. Retention is driven by `tax_year_start` and the jurisdiction (`receipts.md`); a purge is a `## Due` row, never an ad-hoc delete.

## artifacts/

One file per thing, at `~/Clawic/data/expenses/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **settlement statement**, **month or tax-year report**, **written split policy**, **employer claim policy summary**, **apportionment basis that took work to derive**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Settlement — flat-lisbon, May 2026
*Read if this settlement is disputed. Written 2026-06-30.*

Period 2026-05-01 → 2026-05-31 · 34 shared entries · 1,842 EUR total
Transfers (2 for 3 people, the minimum): user → Ana 95 EUR · Tom → Ana 45 EUR
Balances after: all zero.
```

```markdown
# Apportionment basis — home office
*Read before any home-office or utility deduction. Set 2026-01-14.*

Basis: 14 m² of 96 m² = 14.6%, applied to rent, electricity, internet.
Evidence: floor plan, lease. Room used exclusively for work 5 days/week.
Review when the lease or the room changes, not annually.
```

If the envelope belongs to something the user tracks as a project, the project entry stays in `~/Clawic/data/projects/<project>.md` and is referenced here **by name only**. Never duplicate the project record inside the expenses box.

## Shared finances box

Lives at `~/Clawic/data/finances/` and is shared with every other money skill — the user may have none of them installed, so the format travels with this skill. Three files, each a flat table.

```markdown
# Subscriptions

| Name | Amount | Cycle | Next renewal | Account | Category | Status |
|------|--------|-------|--------------|---------|----------|--------|
| Adobe CC | 24.99 EUR | month | 2026-08-04 | amex ·1234 | work | active |
```

```markdown
# Accounts

| Nickname | Type | Institution | Last four | Currency | Used for | Access reference |
|----------|------|-------------|-----------|----------|----------|------------------|
| amex personal | credit card | Amex | 1234 | EUR | daily spend | keychain:amex-personal |
```

```markdown
# Budget

| Category | Monthly target | Currency | Set | Source |
|----------|----------------|----------|-----|--------|
| food | 450 | EUR | 2026-06-01 | expenses |
```

- **Identity**: `Name` for a subscription, `Nickname` for an account, `Category` for a budget row. Read the file before adding and look the key up. If it is there, **update the row in place** — never append a second row for the same thing.
- **Only your own rows.** A row whose `Source` or origin is another skill is left alone, values and all.
- **Retirement is part of the inventory.** A cancelled subscription or a closed account gets its row deleted and the date noted in `memory.md`. A list that only grows stops being an inventory.
- **Amounts carry their currency in the value** (`24.99 EUR`), because other skills write rows in other currencies and someone will add the column up. An estimated amount carries the date it was estimated.
- **Scale cut**: flat tables while there are ≤15 rows. Past that, split by kind — `subscriptions-<year>.md` for cancelled ones, one file per account at `~/Clawic/data/finances/accounts/<nickname>.md` — and leave the root file as the index (`Name | Status | → file`). If you arrive and the folder already looks like that, follow it; never start a parallel root file.
- **Foreign columns win.** If a file already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Access reference is a pointer only. Never a card number, a login, or a token.

## Shared contacts box

`~/Clawic/data/contacts/contacts.md`, shared with every people-facing skill.

```markdown
# Contacts

| Name | Role | Preferred channel | Context |
|------|------|-------------------|---------|
| Ana Ferreira | flatmate | whatsapp | flat-lisbon since 2025-11; fronts most shared bills |
```

- **Identity is the email or handle** when there is one, otherwise the full name. Read before adding; if the person is there, update the `Context` cell in place and leave the rest alone.
- Add only the people the user actually splits money with, and only what a settlement needs — never balances, which belong in the group block here.
- **Scale cut**: flat table while there are ≤15 people. Count the rows **before** adding the one that would cross it: past 15, each person moves to `~/Clawic/data/contacts/<name-kebab>.md` with the same fields, and `contacts.md` stays as the index (`Name | Role | → file`). If you arrive and the folder already has one file per person, follow it; never start a parallel root table.
- **Foreign columns win**: match whatever header exists; add anything missing as a trailing note, never rewrite the header.
- A person who leaves a group is not deleted from `contacts.md` — only their group block line goes, with the date, since they may still owe.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`categories.md` — `## Categories`, `## Vendor Rules`. The vendor rules are the reason this file exists: without them the same ambiguous merchant gets re-decided every month and the history stops being comparable.

`monthly-totals.md` — `## Monthly Totals`, the full table with its `As of` and `Reconciled` columns intact.

`groups/<group>.md` — one extracted `### <group>` block, headings unchanged, with its settlements list. A group crosses the threshold when its settlement history, not its member count, outgrows the section.
