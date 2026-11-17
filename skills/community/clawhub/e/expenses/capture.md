# Capture — Getting Entries In and Keeping Them Honest

Everything here writes to `~/Clawic/data/expenses/ledger/<YYYY-MM>.md`. **Before the first entry of a session**, read `## Categories` and `## Vendor Rules` in `~/Clawic/data/expenses/memory.md` — or `categories.md` if `## Boxes` points there — so the same vendor does not get two categories in one week.

**Contents:** [The Cost of Delay](#the-cost-of-delay) · [The Six Fields](#the-six-fields) · [Parsing What the User Actually Says](#parsing-what-the-user-actually-says) · [Backfilling After a Lapse](#backfilling-after-a-lapse) · [Cash](#cash) · [Refunds, Deposits and Duplicate Charges](#refunds-deposits-and-duplicate-charges) · [Charges That Are Not Expenses Yet](#charges-that-are-not-expenses-yet) · [One Receipt, Several Categories](#one-receipt-several-categories) · [Edge Cases That Corrupt Totals](#edge-cases-that-corrupt-totals)

## The Cost of Delay

The same entry costs about ten seconds at the counter and several minutes three weeks later, and the late version arrives without the two fields that mattered: which category it really was, and why the money was spent. Amounts are recoverable from a statement forever. Purpose and category are recoverable for about a week, then they are guesses.

So: never hold an entry back for a missing field, never ask a clarifying question before writing it, and never propose a tracking system to someone who just told you they bought lunch. Write the row, say the running total for the category if it is interesting, stop.

## The Six Fields

Date · amount with currency · vendor · category · payer · payment method. Plus, when they apply: beneficiaries, tags, receipt filename, purpose.

| Field | Default when not stated | Never |
|---|---|---|
| Date | Today, in the local timezone where the money was spent | Posting date (SKILL.md Rule 2) |
| Amount | — the one thing that must be stated | A converted number with the original discarded |
| Vendor | `unknown` | Silently guessed from the category |
| Category | The vendor rule; else the category this vendor got last time; else `other`, flagged | A new category invented on the spot (`categories.md`) |
| Payer | The user | Omitted on a shared entry |
| Method | The account the user uses most, from `~/Clawic/data/finances/accounts.md` | A card number |

`unknown` is a real value and a flag for the next reconciliation pass. A row with three `unknown`s is still worth more than no row: the statement will fill the amount and the date, and the vendor will jog the rest.

## Parsing What the User Actually Says

Resolution order, no questions asked at any step:

1. **Amount and currency.** A bare number is `home_currency`. A number with a symbol resolves to the currency of `platform.jurisdiction` when the symbol is ambiguous (`$`), and gets flagged in the row rather than queried.
2. **Vendor.** The proper noun. If there is none ("coffee"), the vendor is the category word itself and the row is flagged for the reconciliation pass, which will name it from the statement.
3. **Category.** Vendor rule → last category this vendor got → the noun they used, if it is already a category → `other`.
4. **Date.** "Yesterday", "Tuesday", "on the trip" resolve against today; a date more than 40 days back is treated as a backfill, not a slip of the tongue.
5. **Tags.** An active trip or project envelope tags every entry that plausibly belongs to it — say so in the same line so a wrong tag gets corrected immediately.

One question maximum, and only when the entry cannot be written at all — which in practice means the amount is missing.

## Backfilling After a Lapse

Most logs die in week three and get resurrected as a pile of receipts. The resurrection fails when it is attempted from memory: recall reconstructs the memorable purchases and drops the frequent small ones, so the rebuilt month is both incomplete and biased toward the entries the user already feels bad about.

Procedure:

1. Pull the card and bank statements for the gap, not the receipt pile. The statement is complete; the pile is not.
2. Import or transcribe every line, tagged `#reconstructed`. Categories come from vendor rules alone — do not try to remember.
3. Only now open the receipt pile, and only for entries at or above `receipt_threshold`, business entries, and shared entries. Attach the filenames.
4. Cash spend in the gap is unrecoverable. Book the withdrawals as a single `#cash-unlogged` entry per month, not as invented purchases.
5. Mark the affected months `Reconciled: partial` in `## Monthly Totals`, so a later comparison does not treat them as clean.

A reconstructed month is a usable month for totals and a bad month for category analysis. Say that once when reporting on it.

## Cash

Cash defeats every tracker because nothing external records it. The only method that survives is the periodic count:

```
unlogged cash = (previous count + withdrawals in the period) − logged cash spend − current count
```

Count on `close_day`. Book the difference as one entry, dated the count date, vendor `cash`, category `cash-unlogged`, tag `#cash-unlogged`. Do **not** distribute it across categories — a plausible distribution is a fabricated one, and it will be compared against next month as if it were data.

If `cash-unlogged` runs above roughly a tenth of monthly spend, the useful move is not more discipline: it is fewer cash purchases, or an explicit weekly cash allowance treated as spent on withdrawal (`Where Experts Disagree` in SKILL.md).

## Refunds, Deposits and Duplicate Charges

| Event | How it books | Why not the obvious way |
|---|---|---|
| Full refund | Negative row, original category, tag `#refund-of-<original date>`, dated the refund date | As income it corrupts the category total and makes the month look like it earned money (SKILL.md Rule 5) |
| Partial refund | Negative row for the refunded part only; the original row is never edited | Editing the original erases what was actually paid and breaks the statement match |
| Price adjustment or discount applied later | Negative row, same treatment as a partial refund | — |
| Chargeback filed | Row stays; add tag `#disputed` and a `## Due` line for the decision date | Deleting a disputed charge means nothing chases it |
| Security or rental deposit paid | Row tagged `#deposit`, category `deposits`, plus a `## Due` line for the expected return date | Booked as an expense it inflates the month and then inflates it again when returned as "income" |
| Deposit returned | Negative row against `deposits`, closing to zero | — |
| Deposit forfeited | Move it: negative row in `deposits`, positive row in the real category | The loss belongs where the decision was made |
| Double charge by the merchant | Two rows if both are on the statement, the second tagged `#disputed` | Deleting one hides real money that has left the account |
| The user genuinely bought two coffees | Two rows, no flag | A dedupe rule that eats real repeats is worse than none (`reconciliation.md`) |

## Charges That Are Not Expenses Yet

- **Pre-authorization holds** — hotels, fuel pumps, car rentals. The hold is not a purchase. Log the final charge when it posts; a hold logged as an expense produces a phantom entry the statement will never match.
- **Pending card transactions** — real, but the amount can still change (tips, fuel). Log with tag `#pending` and confirm at reconciliation.
- **Installments and buy-now-pay-later** — the expense is the **full amount on the purchase date**, in the purchase category. The instalments are transfers, not expenses. Otherwise a 1,200-unit sofa appears as twelve entries the size of a grocery run and never shows up in any category analysis.
- **A transfer between the user's own accounts** — never an expense, whatever the statement calls it.
- **A gift card or voucher bought** — default: expense at purchase, tag `#giftcard`, redemption logged at zero. For business use the opposite applies in most jurisdictions, where the deductible event is redemption, not purchase — verify before treating a bought card as a business cost.
- **Points, miles and loyalty redemptions** — zero cost unless the points were bought for money (`currency.md`).

## One Receipt, Several Categories

A supermarket run with a frying pan in it is two entries, not one, whenever the non-food part is material or business-relevant. Both rows carry the same receipt filename and the same `#split-receipt-<date>` tag, and their amounts must sum **exactly** to the receipt total — check it before writing, because a split that does not sum will never be found again.

Below roughly the value of `receipt_threshold` divided by ten, splitting is not worth the tokens: put the whole thing in the dominant category. Materiality is the test, not purity.

## Edge Cases That Corrupt Totals

- **Tips and service charges** go in the same row as the meal unless the user is explicitly tracking tipping, in which case they are a tag, not a category.
- **Fees** — FX fees, ATM fees, late fees, card annual fees — get their own `fees` category, always. Buried inside the purchase they are invisible, and they are the most cuttable spend in most ledgers.
- **Reimbursed and rebillable spend stays in the ledger** with its `#claim` or `#billable` tag. Removing it makes the claim untraceable; the report is what nets it out (`reports.md`).
- **Shared entries stay at their full amount** in the ledger. The user's share is a derived number, computed from the group block, never a second row (`sharing.md`).
- **A purchase on the last day of a month that posts in the next** belongs to the month it was made (Rule 2); flag it so the reconciliation of both months expects it.

**Write on the way out.** Every entry lands in `ledger/<YYYY-MM>.md` in the same turn it is spoken; a wallet count writes its `#cash-unlogged` row and its next-count date in `## Due`; a backfill sets `Reconciled: partial` on the months it touched; a new vendor decision writes its rule to `## Vendor Rules`; a deposit or a disputed charge writes its `## Due` line. Formats in `memory-template.md`.
