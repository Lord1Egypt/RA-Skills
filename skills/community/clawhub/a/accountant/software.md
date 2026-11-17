# The Ledger System — Setup, Feeds, And Migration

Accounting software does not do accounting; it enforces some rules, hides others, and has a small set of features that cause most of the damage in small-business books.

**Before changing anything structural**, read `ledger_software` in `~/Clawic/data/accountant/config.yaml` — it decides which mechanics and feature names below apply — plus `chart-of-accounts.md` and `## Systems` in `~/Clawic/data/accountant/memory.md`, for which feeds and integrations push data in. A new integration posting into the same accounts as an existing one is the standard cause of duplicated revenue.

## Setup Decisions That Are Expensive To Reverse

| Decision | Why it is hard to change later | Get it right by |
|---|---|---|
| Fiscal year end | Reports, comparatives, and locked periods are built on it | Matching the tax year unless there is a real seasonal reason |
| Base currency | Usually immutable after the first transaction | Setting the functional currency, not the owner's preferred one (`currency.md`) |
| Accounting basis for reporting | Reports built on one basis mislead when read as the other | Declaring it and labelling every export (SKILL.md Rule 2) |
| Account numbering scheme | Renumbering rewrites every report definition and rule | Leaving gaps of 10 (`bookkeeping.md`) |
| Tracking categories, classes, or departments | Retro-tagging history is manual, transaction by transaction | Deciding the second dimension before the first month is coded |
| Multi-entity vs one file per entity | Separating a combined file later is a reconstruction | One file per legal entity, always |
| Inventory module on or off | Turning it on mid-year needs opening quantities and costs | Deciding from the costing method (`inventory.md`) |
| Sales tax configuration | Wrongly configured tax silently misstates every invoice | Setting rates per jurisdiction and product class (`sales-tax.md`) |

## Bank Feeds And Rules

Feeds are a productivity tool and a data-quality risk in the same feature.

- **Rules propose; a human confirms.** Auto-add is acceptable only for a fixed-amount, single-vendor, single-account match — a monthly software charge that never varies. Everything else posts silently, and silent miscoding is discovered a year later across a filed period (SKILL.md, Traps).
- The feed is **not** the source of truth. Reconcile to the statement (`reconciliation.md`); feeds drop transactions, re-date them, and occasionally re-import a month.
- **Matching is not coding.** Marking a feed line as matched to an existing invoice is correct; letting the feed create a second transaction for an invoice already recorded is how AR is paid twice in the ledger and never in reality.
- Review rules quarterly. A rule written for a vendor that changed what it sells keeps coding correctly-shaped nonsense.
- A feed that stops delivering is invisible unless someone looks: an account with no transactions for a period is a `## Open Items` line, not a quiet month.

## Features That Cause Most Of The Damage

| Feature | Trap | Correct use |
|---|---|---|
| Undeposited funds / payments received | Grows forever when receipts are recorded individually and the bank shows one deposit | Group receipts into deposits mirroring the actual bank credit (`reconciliation.md`) |
| "Ask my accountant" / suspense account | Becomes a permanent plug nobody revisits | Empty it before every close (SKILL.md Rule 8) |
| Opening balance equity | Absorbs conversion plugs invisibly | Should be zero once conversion is complete; a balance is unfinished migration |
| Deleting vs voiding | Deleting removes the audit trail and can alter a filed period | Void, or reverse (SKILL.md Rule 7) |
| Backdating into a closed period | Permitted by default in most systems | Set and enforce the closing date lock |
| Merging accounts or vendors | Irreversible in several systems, and it rewrites history | Export first; retire rather than merge where possible |
| Recurring transaction templates | Keep posting after the contract ends | Every template has an end date; reviewed at close (`recurring-entries.md`) |
| Multi-currency revaluation | Runs automatically and posts to accounts nobody watches | Know which account it posts to and review it monthly (`currency.md`) |
| Automatic sales tax calculation | Correct only if the product classes and addresses are configured | Verify against a known transaction per jurisdiction, per year |
| Class or department tracking left optional | Half-tagged data cannot be reported on | Make it required, or do not use it at all |
| Inventory adjustments outside the module | Breaks the register-to-ledger tie | All movement through the module (`inventory.md`) |

## User Access

- One login per person, always. Shared logins destroy the audit trail, which is the only evidence of who did what.
- Restrict who can edit closed periods, delete transactions, add users, and change bank details — those four permissions cover most of the internal risk.
- Remove access the day someone leaves, including integrations and API tokens they created (`audit.md`).
- The accountant's or bookkeeper's access is named and scoped like anyone else's; a shared owner login given "temporarily" is never withdrawn.

## Migration And Conversion

The most dangerous project in bookkeeping, because errors land in opening balances and every subsequent period inherits them.

1. **Pick the conversion date** — a period end, ideally the fiscal year end. Mid-year conversions need both systems reconciled at the switch and produce two half-year reports that must be combined manually.
2. **Close and lock the old system** through the conversion date. Migrating from unreconciled books migrates the problem (`cleanup.md`).
3. **Take the trial balance** as at the conversion date. This is the authority for everything that follows.
4. **Enter opening balances** dated the day before the first period in the new system, with receivables and payables as **individual open items**, not lumps — a lump makes the subledger permanently untieable.
5. **Enter open inventory items and the asset register** with their own detail: quantities and costs, and cost plus accumulated depreciation per asset. A single lump for either destroys the ties permanently (SKILL.md ties).
6. **Reconcile the new system's trial balance to the old one, line by line.** They must agree exactly. Any difference sitting in opening balance equity is unfinished work, not a rounding.
7. **Run both systems for one period** where the stakes justify it, and compare the results before decommissioning.
8. **Keep the old system's data exported and readable** for the full retention window — general ledger, trial balances, and the document archive. Access to the old platform will end; the export is what survives (`tax.md`).

Historical detail is normally **not** migrated: opening balances plus an exported archive of the old ledger is the standard, and importing years of history usually creates duplicates and broken links rather than continuity.

## Integrations

- Every integration that creates transactions is a second bookkeeper. Know for each one: which accounts it posts to, gross or net, whether it creates invoices or journals, and how it handles refunds and fees.
- The classic duplication: a payment processor integration **and** a bank feed both creating a transaction for the same money. One should create the sale and the fee, the other should only match the payout (`reconciliation.md`).
- Test any new integration in one period and reconcile before trusting it, then record what it does in `## Systems`.
- Payroll, point of sale, e-commerce, and expense tools each need a mapped destination account before the first sync, not after.

**Write when this file produced something durable**: the software, feeds, and integrations in use, with what each posts → `## Systems`. A migration plan or its conversion reconciliation → `artifacts/migration-<system>.md` with its `## Boxes` line, and the engagement in `~/Clawic/data/projects/<project>.md` if it spans months. A feed rule worth keeping consistent → `## Coding Rules`. A feed that stopped, or an unresolved conversion difference → `## Open Items` (`memory-template.md`).
