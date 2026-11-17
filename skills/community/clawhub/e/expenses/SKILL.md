---
name: Expenses
slug: expenses
version: 1.0.2
description: Logs, splits, categorizes and reports spending — daily expenses, shared costs, reimbursements, receipts, project and trip budgets. Use when the user paid for something and wants it recorded, when a bill has to be split and someone told what they owe, when a group trip or shared flat needs settling up, when a client owes money back and the claim has to be assembled, when they ask where their money went or why a category jumped, when a renovation, wedding or trip budget needs a remaining number, when something was paid in another currency, when a refund, deposit or duplicate charge has to be booked, or when the log no longer matches the card statement. Not for net worth or debt planning (`personal-finance-tracker`), zero-based budgeting (`zero-based-budgeting`), subscription inventories (`subscriptions`), issuing invoices (`invoice`), OCR archiving of supplier invoices (`invoices`), payment software (`billing`), or bookkeeping (`accountant`).
homepage: https://clawic.com/skills/expenses
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 💸
    os:
    - linux
    - darwin
    - win32
    displayName: Expenses
    configPaths:
    - ~/Clawic/data/expenses/
    - ~/Clawic/data/finances/
    - ~/Clawic/data/contacts/
    - ~/Clawic/profile.yaml
    - ~/expenses/
    - ~/clawic/expenses/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/expenses/
      - ~/Clawic/data/finances/
      - ~/Clawic/data/contacts/
      - ~/Clawic/profile.yaml
      - ~/expenses/
      - ~/clawic/expenses/
---

**Data.** At the start of every session, read `~/Clawic/data/expenses/config.yaml` (what the user declared) and `~/Clawic/data/expenses/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — that index *is* the list of files; never work from a list of names memorized here, because most boxes get created after this skill was written. Read `~/Clawic/data/finances/` before any question about budgets, recurring charges, or which account something was paid from. If none of it exists, work from defaults and say nothing about it. If data sits at an old location (`~/expenses/` or `~/clawic/expenses/`), move it to `~/Clawic/data/expenses/`, and say in one line that you moved it and from where. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens.

**Write before the session ends** whenever it produced something durable: an expense, a refund or a deposit; a split and the balances it moved; a settlement; a claim that changed status; a category or vendor rule; a budget envelope or its burn; a month close or a reconciliation pass; or something the user will want to read again — a settlement statement, a month or tax-year report, a written policy. `memory-template.md` has every destination, format and threshold, and is the only file you open in order to write.

**What belongs to other skills' boxes, not to this one.** Recurring charges, payment accounts and cards, and the household budget go to the shared `~/Clawic/data/finances/` (`subscriptions.md`, `accounts.md`, `budget.md`) — one row per item, amounts carrying their currency, so the same numbers answer whoever asks. People you split with go to `~/Clawic/data/contacts/contacts.md`; here they appear as a name only. Trip bookings already recorded in `~/Clawic/data/bookings/` are read, never re-entered — the locator lives there, the money lives here. Formats and the full write protocol travel in `memory-template.md`, because the user may have none of those skills installed.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. Store the pointer and strip the value: `keychain:amex-personal`, `1password:Personal/Chase/login`, `env:PLAID_TOKEN`. Card numbers, CVVs, PINs and banking logins are never data; the last four digits and the card's nickname are.

Money tracking dies from friction, not from bad math. Record the entry in one line, name the number, and stop. Never open with an interview about how they want to track things: log what they just said, use the defaults, and let the shape emerge from the entries. Report numbers with their currency and their as-of date, and never wrap a total in an opinion about the spending. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale, country) → the Configuration table default.

## When To Use

- Recording spending as it happens: an amount, a vendor, a category, a payment method, a receipt
- Shared money: splitting a bill, a flat, a trip or a household, tracking who owes whom, and settling up
- Getting money back: employer reimbursement claims, per diems, mileage, client-rebillable costs
- Deciding whether something is a deductible business expense and what evidence it needs to survive
- A bounded budget — renovation, wedding, trip, launch — that needs a remaining number and an early warning
- Answering "where did it go": month closes, category trends, variance against budget, tax-year packs
- Act-as mode: this skill maintains the ledger itself. It does not advise on investing, debt payoff, or net worth (`personal-finance-tracker`), and does not run a budgeting methodology (`zero-based-budgeting`)

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "I just paid €12 for lunch" | One line, six fields, into this month's ledger box; no follow-up questions | `capture.md` |
| Weeks of receipts piled up unlogged | Backfill by statement, not by memory; mark reconstructed entries as such | `capture.md` |
| Cash keeps vanishing from the log | Count the wallet, book the difference as one `cash-unlogged` entry | `capture.md` |
| "What category is this?" / misc is bloating | The decision test, then a vendor rule so it is never asked twice | `categories.md` |
| Split the dinner / the flat / the trip | Who paid vs who benefited are two fields; then the balance table | `sharing.md` |
| "Who owes who, and how do we settle?" | Net the balances, then minimize transfers — never pay round-robin | `sharing.md` |
| Work owes me money | Claim packet, policy limits, submission deadline, status ladder | `reimbursement.md` |
| Per diem or mileage instead of receipts | Rate × units, and which receipts stop being needed | `reimbursement.md` |
| "Can I deduct this?" | Business purpose test, mixed-use apportionment with a stored basis | `business.md` |
| Rebilling a cost to a client | At cost or with markup, and which tax rides on it | `business.md` |
| Receipt handling, or one went missing | Naming, retention clock, tax invoice vs card slip, the missing-receipt note | `receipts.md` |
| Renovation/wedding/trip budget | Envelope with contingency; committed money counts before it is paid | `budgets.md` |
| "Are we over budget?" | Burn rate against elapsed share, not against calendar feel | `budgets.md` |
| Spending on a trip, several currencies | Daily burn, trip envelope, per-person share, post-trip summary | `travel.md` |
| Paid in a foreign currency | Three fields — original, rate, rate date — and which rate is correct | `currency.md` |
| Log does not match the card statement | Match by amount+date window; classify each gap before fixing any | `reconciliation.md` |
| CSV export from a bank to import | Column mapping, sign convention, dedupe key, pending rows | `reconciliation.md` |
| Month end, quarter end, tax year end | Close sequence, variance, what to surface unprompted | `reports.md` |
| Refund, chargeback, deposit, duplicate charge | Negative entry against the original month and category (Rule 5) | `capture.md` |
| Anything else about spending | Answer with the number, its currency and its as-of date, then write the entry to its box | — |

Coverage map: `capture.md` getting entries in · `categories.md` the taxonomy · `receipts.md` evidence and retention · `sharing.md` split and settle · `reimbursement.md` claiming from an employer · `business.md` deductibility and rebilling · `budgets.md` bounded envelopes · `travel.md` trip spending · `currency.md` foreign money · `reconciliation.md` matching against the bank · `reports.md` closes and analysis.

## Core Rules

1. **Log now, complete later; never the reverse.** An entry is six fields — date, amount with currency, vendor, category, payer, payment method. A field you do not have is written as `unknown` and the entry still goes in. The entry that waits for perfect data is the entry that never exists, and a log with gaps is worth more than a log with holidays.
2. **Transaction date, not posting date.** Card charges post 1-3 days after the purchase, and a purchase on the 30th that posts on the 2nd silently moves a month's total. Store the date the money was committed; keep the posting date only when reconciling (`reconciliation.md`).
3. **Every amount carries its currency, in the value.** `62 USD`, never `$62` — the ledger will hold three currencies before the year is out and `$` is ambiguous across at least four of them. A foreign entry stores three fields, always: original amount with its currency, the rate as home-per-unit-foreign, and the rate date. Home amount = original × rate: 8,400 JPY at 0.0062 EUR/JPY = 52.08 EUR. Storing only the converted number destroys the entry the first time someone asks what the actual price was (`currency.md`).
4. **Who paid and who owes are different fields.** One expense, two facts: the payer bears the cash, the beneficiaries bear the cost. Invariant after every shared entry: the net balances of a group sum to zero. If they do not, one split is wrong — find it before adding anything else (`sharing.md`).
5. **A refund is a negative entry, not income.** Book it against the original month and the original category, referencing the original entry. Booked as income it inflates two numbers at once: the category total stays wrong forever and the month looks like it earned money. Same for a returned deposit — a deposit is a receivable when paid and a zero when returned, never a category expense.
6. **Never compare a month-to-date number against a closed month.** Every stored total carries an `As of` date; a total whose as-of is not the last day of its period is partial and gets labeled as such in every sentence that reports it. Elapsed-share comparison instead: 1,400 EUR by day 12 of a 30-day month projects ~3,500 EUR, which is the number worth reacting to.
7. **Categories are stable or every comparison is a lie.** Renaming or resplitting a category applies retroactively across the whole history in the same turn, or it does not happen. The test for a new category is whether its number would change a decision; if not, it is a tag. `other` above ~5% of monthly spend means the taxonomy is broken, not that the month was unusual (`categories.md`).
8. **Evidence is captured at payment or lost.** At or above `receipt_threshold` an entry is incomplete without a receipt pointer, and a business or reimbursable entry additionally needs the business purpose written at the time — reconstructing purpose months later is the part that fails an audit, not the amount (`receipts.md`).

## Output Gates

Before delivering a number, a settlement, a claim or a report:

- Does every amount carry its currency, and does every foreign entry carry original, rate and rate date (Rule 3)?
- Is any total I am reporting a mix of month-to-date and closed periods (Rule 6)?
- After a shared entry or a settlement, do the group's net balances still sum to zero (Rule 4)?
- Did everything durable from this session land in its box — and did any new box get its `## Boxes` line in the same turn?
- Did I strip every card number, PIN, login and token from anything pasted in, leaving a `<kind>:<locator>` pointer in its place?
- Did I report the number without an opinion attached to it?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/expenses/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| home_currency | text (ISO 4217) | `profile.yaml` currency, else USD | Currency every total, budget and report converts to; entries always keep the currency actually paid alongside (Rule 3) |
| tax_year_start | text (MM-DD) | 01-01 | Boundary of the business year in `reports.md` and the start of the retention clock in `receipts.md` |
| receipt_threshold | number (home currency) | 75 | Amount at or above which an entry is flagged incomplete without a receipt pointer (Rule 8) |
| close_day | number (1-28) | 1 | Day the previous month is closed and reported; writes the recurring row in the `## Due` table |
| settle_cadence | week \| month \| trip \| on_request | month | How often shared balances are netted and a settlement statement is offered (`sharing.md`) |
| default_split | equal \| by_income \| custom | equal | Split applied when the user names people but not proportions (`sharing.md`) |
| budget_alert_pct | number (50-100) | 80 | Share of an envelope at which spend is flagged unprompted, including committed-but-unpaid money (`budgets.md`) |
| mileage_rate | number (home currency per km or mi) | none | Rate used to turn distance into money; while unset, say that the jurisdiction's official rate for the year must be checked before quoting one (`reimbursement.md`) |
| private_categories | list | none | Categories excluded from any shared, exported or household-level report; their totals fold into `other` |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — how entries arrive (dictated in chat, a running inbox file, bank CSV import, receipt photos) and whether imports are trusted without review — affects `capture.md` and `reconciliation.md`
- **Conventions** — category naming style, tag scheme for projects and trips, ledger cut (month vs week), file naming for receipts — affects `categories.md` and `receipts.md`
- **Platform** — jurisdiction and its retention and receipt rules, locale and date format, distance unit, which cards and accounts exist — affects `business.md`, `receipts.md` and `reimbursement.md`
- **Safety posture** — what may leave the machine, which categories are private, whether balances are shown to a group or only to the user — affects `reports.md` and `sharing.md`
- **Output format** — report verbosity, whether every answer carries a trend line, register (numbers-only vs commentary) — affects `reports.md`
- **Cadence** — month close day, settlement rhythm, claim submission day, tax quarter dates, budget review — affects the `## Due` table
- **Split policy** — standing rules per group (rent by room size, groceries equal, one person always fronts) — affects `sharing.md`

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Designing the category system before logging anything | Two weeks of design, zero entries, and the categories turn out wrong anyway because they were guessed | Log flat for two weeks, then derive categories from what actually appeared (`categories.md`) |
| Splitting round-robin — everyone pays everyone | A five-person trip settles in up to 20 transfers, so nobody finishes and the balances rot | Net first, then minimize: any group of n settles in at most n−1 transfers (`sharing.md`) |
| Booking a refund as income | The category total is now wrong in both directions and the month reads as profitable | Negative entry against the original month and category (Rule 5) |
| Converting a foreign amount and keeping only the result | The original price is gone, so a disputed charge cannot be matched and the rate cannot be audited | Store original, rate, rate date (Rule 3, `currency.md`) |
| Reconstructing business purpose at tax time | Amounts survive reconstruction; purpose does not, and purpose is what is actually challenged | Write the purpose in the entry at payment (Rule 8, `business.md`) |
| Treating a project budget as spent-so-far | Signed quotes and deposits are already committed; the envelope is gone before the cash is | Track committed and paid separately (`budgets.md`) |
| Accepting the terminal's offer to charge in your home currency | Dynamic currency conversion embeds a markup, commonly 3-7%, on top of the card's own FX | Always pay in the local currency (`travel.md`) |
| Waiting for the full receipt pile before claiming | Employer claim windows expire, commonly 30-90 days; an expired claim is a donation | Submit on `close_day` cadence, partial packets included (`reimbursement.md`) |
| One "shared" category for a couple or a flat | It answers how much was spent but never who owes whom, which is the only question that gets asked | Payer plus beneficiaries per entry (Rule 4) |
| Recategorizing history "from now on" | Every month-over-month comparison across the boundary is silently invalid | Retroactive across the whole history, or not at all (Rule 7) |
| Importing a bank CSV without a dedupe key | The same coffee appears three times across three imports and the month is unusable | Dedupe on date + amount + last four of the account (`reconciliation.md`) |
| Guilt framing on a total | The user stops logging, which costs more than any single category ever did | Report the number and the trend; the judgment is theirs |

## Where Experts Disagree

- **Granular vs broad categories.** Broad (8-15) survives years and gets maintained; granular answers questions broad cannot ("coffee", "kids' activities"). The frontier is decision value: split a category only when its own number would change a behavior, and use tags for everything else you want to slice by later (`categories.md`).
- **Log everything vs log what matters.** Complete logs enable reconciliation and audits; partial logs (over a floor, say 10 units of home currency, plus all business and shared spend) survive longer because they cost less. A user who needs tax evidence or shared settlement has no choice — those must be complete; discretionary personal spend can run on a floor.
- **Split by income vs split equally.** Equal is defensible and frictionless; proportional is fairer when incomes differ by more than roughly 2×, and it is the standing rule that most often goes unwritten and then gets relitigated. Whichever is chosen, write it down as a group rule before the first disagreement, not during it (`sharing.md`).
- **Cash tracking.** One school logs every cash purchase; the other withdraws a fixed amount, treats the withdrawal as spent, and never itemizes it. The second is more honest about what people actually sustain — but it destroys category data for the cash portion, which matters for anyone whose deductible spend is partly cash.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/expenses (install if the user confirms):
- `personal-finance-tracker` — net worth, cashflow and debt, which read these totals as input
- `subscriptions` — the recurring-charge inventory in the shared `finances/` box
- `invoice` — issuing invoices to clients, where rebillable costs end up
- `accountant` — bookkeeping, financial statements and tax filing beyond expense evidence
- `travel-planning` — the trip itself; this skill covers what the trip costs

## Feedback

- If useful, star it: https://clawic.com/skills/expenses
- Latest version: https://clawic.com/skills/expenses

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/expenses.
