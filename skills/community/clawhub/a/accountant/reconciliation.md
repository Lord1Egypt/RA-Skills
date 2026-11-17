# Reconciliation — Making The Ledger Match Reality

Reconciliation is the only proof a set of books describes anything real. Everything downstream — statements, filings, valuations — inherits its result.

**Before starting**, read `~/Clawic/data/finances/accounts.md`: which accounts exist, which ledger account each maps to, and when each was last reconciled. An account nobody has reconciled for four months is not a reconciliation task, it is a cleanup task (`cleanup.md`).

**Contents:** [The Two Adjusted Balances](#the-two-adjusted-balances) · [Bank And Card](#bank-and-card) · [Payment Processors](#payment-processors) · [Clearing And Undeposited Funds](#clearing-and-undeposited-funds) · [Subledger To Ledger](#subledger-to-ledger) · [Finding A Difference](#finding-a-difference) · [Items That Are Allowed To Remain](#items-that-are-allowed-to-remain) · [Cadence](#cadence)

## The Two Adjusted Balances

Never chase a transaction before both sides are computed. The comparison is between two *adjusted* figures, not between a statement and a ledger:

```
Adjusted bank  = statement closing balance
               + deposits in transit
               − payments issued but not presented
               ± bank errors

Adjusted books = ledger closing balance
               + amounts the bank collected that you had not recorded (interest, direct receipts)
               − charges you had not recorded (fees, returned items, standing orders)
               ± ledger errors
```

Reconciled means these two are **equal to the cent**. Anything left is a finding with a name, an amount, and an owner — never a rounding and never a plug (SKILL.md Rule 3).

## Bank And Card

- Work from the **statement**, not the feed. Bank feeds drop, duplicate, and re-date transactions; the statement is the document a tax authority or a lender will ask for.
- Reconcile to the statement's own closing date, not to the month end, when the statement cycle differs — then carry the gap days explicitly. A card cycle ending on the 18th means a month-end balance needs the 19th-to-31st transactions added, and that computed figure is what gets accrued.
- **Card accounts are liabilities.** A card with money owed has a credit balance; if the ledger shows it as a debit, the sign convention is wrong and every card reconciliation will be out by twice the balance.
- Foreign-currency accounts reconcile in the **account's own currency** first, then get revalued (`currency.md`). Reconciling a EUR account against its USD ledger balance mixes a transaction problem with a rate problem, and neither gets solved.
- Uncleared items older than the local staleness rule (commonly six months for a check) are written back, not left forever: Dr the payment account / Cr the original expense or a stale-item account, with a note. Unpresented payments from three years ago are the classic sign nobody has ever truly reconciled.

## Payment Processors

The single largest source of misstated revenue in small businesses. The deposit is a **net** figure, and booking it as revenue understates revenue, expenses, refunds, and tax.

The correct shape, using the processor's own settlement report as the source:

```
Dr  Processor clearing        gross sales
  Cr Revenue                                 gross sales
  Cr Sales tax payable                       tax collected, if collected by the platform

Dr  Processing fees           fees
Dr  Refunds / contra-revenue  refunds
Dr  Chargebacks + fees        disputes
  Cr Processor clearing                      total deductions

Dr  Bank                      payout received
  Cr Processor clearing                      payout received
```

- **The clearing account balance is the reconciliation.** After every payout clears, it should equal only in-transit funds — typically the last two days of sales. A growing balance means a payout was never matched; a negative balance means a payout was booked with no sales behind it.
- **Reserves and holdbacks** (common with high-risk or new merchants) sit in the clearing account or a separate receivable until released. Treating a holdback as a fee overstates costs permanently.
- **Marketplace platforms** that collect and remit sales tax change the entry: the tax never becomes your liability, but the gross revenue still does. Booking only the net payout as revenue understates turnover, which is what registration thresholds are measured against (`sales-tax.md`).
- **Multi-currency processors** settle in one currency and sell in several; the difference between the transaction rate and the settlement rate is an FX gain or loss, not a fee (`currency.md`).

## Clearing And Undeposited Funds

- A clearing account exists to absorb **timing**, and its correct resting state is zero or a known in-transit amount. Any clearing account with a permanent balance is holding an unfinished entry.
- Undeposited funds (the "money received but not yet in the bank" account) must be grouped into deposits that mirror the **actual bank deposit**. Three checks banked together are one deposit line in the ledger; recorded separately, they will never match a single bank credit and the account grows forever.
- **Payroll clearing** works the same way: the payroll provider's total debit is one bank line and many ledger lines. The clearing account nets to zero on every run (`payroll.md`).
- Inter-entity or inter-account transfers use a transfer or due-to/due-from account and are matched on **both** sides in the same session. Half a transfer is indistinguishable from income.

## Subledger To Ledger

At every close, four totals must equal their control accounts. This is not a reconciliation of documents but of two views of the same ledger, and it fails for exactly one reason: someone posted a journal straight to the control account.

| Subledger | Control account | Break means |
|---|---|---|
| Open invoices (aging total) | Accounts receivable | A journal posted to AR, or an invoice written off outside the subledger (`receivables.md`) |
| Open bills (aging total) | Accounts payable | An accrual posted to AP instead of accrued liabilities (`payables.md`) |
| Stock valuation report | Inventory | A purchase expensed, or a count adjustment made in one place (`inventory.md`) |
| Asset register | Fixed assets and accumulated depreciation | A disposal made in the world and not the register (`fixed-assets.md`) |

## Finding A Difference

In order, cheapest first:

1. **Arithmetic tests on the difference** — divisible by 9 (transposition), by 2 (wrong side), equal to a single transaction amount (a missing leg). Same tests as the trial balance (`bookkeeping.md`).
2. **Date-range bisect** — reconcile the first half of the period, then the half that breaks. Four passes isolates one entry in a year.
3. **Duplicate scan** — same amount, same counterparty, within a few days. Feed re-imports and manual entry on top of a matched feed item are the usual cause.
4. **Sign scan** — refunds entered as payments, or a credit note entered as an invoice. This produces a difference of exactly twice the item.
5. **Boundary scan** — a transaction dated the 1st that the bank shows on the last day of the prior month. Correct the ledger date; never adjust the bank.
6. **Last resort: rebuild the account** from the statement for the period, line by line. Anything that survives all five is usually a transaction that exists in one place only.

A difference that cannot be located and is **below** the materiality threshold (SKILL.md Rule 4) may be written off to a named difference account with a note — once, with the amount, the date, and what was ruled out. A difference that recurs, or that grows across periods, is escalated, not written off (SKILL.md, Escalate).

## Items That Are Allowed To Remain

| Item | Why it is fine | When it stops being fine |
|---|---|---|
| Deposits in transit | Banked after the cutoff | Not cleared within a few business days |
| Unpresented payments | Sent, not cashed | Past the local staleness period |
| Last two days of processor sales | Settlement lag | The lag exceeds the processor's stated payout schedule |
| A known timing difference on a card cycle | Statement cycle ≠ month end | Nobody has computed the gap-day amount |

Everything else that remains is an error.

**Write when this file produced something durable**: the reconciliation date for every account touched → `Last reconciled` in `~/Clawic/data/finances/accounts.md`. A newly discovered account → a row in the same file. A difference that is explained but not yet fixed, or written off → `## Open Items`. A recurring vendor charge noticed while reconciling → `~/Clawic/data/finances/subscriptions.md`. A processor's settlement quirk that will repeat → `## Coding Rules` (`memory-template.md`).
