# Reports — Closes, Comparisons and What to Say Unprompted

**Before producing any number**, read `## Monthly Totals` and `## Due` in `~/Clawic/data/expenses/memory.md`, then only the `ledger/<YYYY-MM>.md` files the question actually spans. Reading twelve ledger files to answer a question about last month is the reason `## Monthly Totals` exists.

**Contents:** [The Month Close](#the-month-close) · [Comparability Rules](#comparability-rules) · [The Honest Baseline](#the-honest-baseline) · [Annualizing](#annualizing) · [What to Surface Unprompted](#what-to-surface-unprompted) · [Answering a Direct Question](#answering-a-direct-question) · [The Tax-Year Pack](#the-tax-year-pack) · [Register](#register)

## The Month Close

Runs on `close_day`, as a `## Due` row. Seven steps, in order — the order matters because each step's output is the next one's input:

1. **Reconcile** every account for the month (`reconciliation.md`). A total computed before reconciliation is an estimate.
2. **Resolve the `unknown`s** the reconciliation surfaced: vendors, categories, missing amounts.
3. **Close the row**: `As of` = the last day of the month, `Reconciled` = `yes` or `partial`.
4. **Top three categories**, descending, always the same shape — that fixed shape is what makes a twelve-month comparison possible without reopening a single ledger file.
5. **Variance** against `~/Clawic/data/finances/budget.md` where targets exist, and against envelopes with activity this month (`budgets.md`).
6. **Claims and settlements**: what is outstanding, what aged past its window (`reimbursement.md`, `sharing.md`).
7. **Update `## Due`**: next close, next settlement, next claim submission, anything that fell due.

Produce the written summary as an `artifacts/` file only when the user reads reports. For most users the close is four lines in the conversation and a `## Monthly Totals` row — a monthly document nobody opens is a monthly cost with no return.

## Comparability Rules

Every one of these has produced a confidently wrong statement in a real ledger:

- **Closed against closed only.** A month-to-date total compared to a full month is a false decline, every time (SKILL.md Rule 6).
- **Same category set on both sides.** If the taxonomy changed between the two periods and history was not rewritten, say so in the same sentence as the number (`categories.md`).
- **Same reconciliation state.** A clean month against a partial one compares data with an estimate.
- **Month length.** February against January is 10% shorter. For daily-rate categories, compare per-day, not per-month.
- **Reimbursed and rebillable spend** sits in the ledger at full amount; a personal spending comparison nets it out and says that it did.
- **One-offs are named, not smoothed.** A month with a 2,000 flight is not a bad month; it is a month with a flight in it. Naming the single item is more useful than any adjusted average.

## The Honest Baseline

"Spending is up" against last month is mostly noise: single months swing on one appliance or one trip.

**Baseline = the median of the trailing three closed months** for that category. Median, not mean, because one anomalous month drags a mean and the point of a baseline is to be undragged.

Flag a category when the closed month exceeds its trailing-three median by more than roughly 30% **and** by more than a materiality floor — around `receipt_threshold` — so a 4-unit category that doubled does not get a paragraph. Worked example: eating-out at 190 / 240 / 210 has a median of 210; a month at 300 is 43% over and 90 units over, so it earns a line. A month at 240 is 14% over and does not.

With twelve closed months, compare against the same month last year as well for anything seasonal — heating, travel, gifts. The trailing median treats December as an anomaly every single year.

## Annualizing

Never `monthly × 12`. Any ledger with annual or irregular lines — insurance, taxes, subscriptions billed yearly, holidays — produces an annualized figure wrong by the entire size of those lines.

Use **trailing twelve months** of closed data. With fewer than twelve closed months, say the projection's basis in the same sentence: "on 5 closed months, excluding anything annual not yet seen".

The same applies to a savings claim. A cancelled subscription saves its annual amount only if the annual amount is what was being paid; a monthly plan cancelled in month two saved ten months, not twelve.

## What to Surface Unprompted

At most three items, at the start of a session, as statements and never as questions. Ranked by how much money a delay costs:

| Trigger | Line |
|---|---|
| A claim past its submission window (`reimbursement.md`) | Highest priority — the money disappears entirely at the deadline |
| A dispute decision date reached (`reconciliation.md`) | The window closes |
| An envelope past `budget_alert_pct` on committed (`budgets.md`) | Early enough to change scope |
| A settlement overdue past `settle_cadence` (`sharing.md`) | Balances rot |
| A category past the flag threshold above | Information, acted on or not |
| A month unreconciled for more than two statement cycles | It will stay unreconciled; say it once |
| A deposit past its expected return date | Real money, forgotten by default |
| Nothing due | Say nothing at all |

Overdue items get stated once per session, not repeated. An agent that opens every conversation with the same three warnings gets the skill uninstalled.

## Answering a Direct Question

"How much did I spend on X" gets: **the number with its currency, the period, its as-of state, and the comparison** — in one or two lines, no preamble.

> Eating out, June: 300 EUR, closed. Trailing three-month median 210, so 43% above.

Then stop. Do not append advice, do not append a plan, do not append an adjective. If the user wants a reason they will ask, and the answer to "why" is a list of the largest entries, which is also two lines.

For a category question spanning periods with different taxonomies or reconciliation states, the caveat goes in the same sentence as the number — a caveat in a following paragraph is not read.

## The Tax-Year Pack

Bounded by `tax_year_start`. Written to `~/Clawic/data/expenses/artifacts/tax-year-<year>.md` with its `## Boxes` line, because it is opened once a year and needs to be findable in three.

Contents:

- Totals by deductible category, mapped to the filing headings the user actually uses (`categories.md`).
- Mixed-use lines with their **apportionment basis**, not just the percentage — the basis is what gets asked for (`business.md`).
- Mileage total with the rate applied and the period, plus odometer readings if kept.
- Capitalized items listed separately, out of the expense totals, tagged `#capital`.
- Input tax recoverable, with the count of lines that have a valid tax invoice against the count that do not (`receipts.md`).
- Rebilled costs, listed separately from costs absorbed, with the client as a name pointer.
- Receipt coverage: how many entries at or above `receipt_threshold` have a receipt file, and the list of those that do not. That list is the accountant's first question.
- Anything from the Red Flags table that appeared during the year (`business.md`).

Quarterly, the same pack in miniature is what makes the annual one a formality rather than a week.

## Register

- Number, direction, magnitude. No adjective, no judgement, no encouragement.
- Guilt framing is the single most expensive thing this skill can do: the user stops logging, and a dead ledger costs more than any category ever did.
- `private_categories` fold into `other` in any shared, exported or household-level output; the ledger keeps them intact (`categories.md`).
- Verbosity follows `output_format` in `config.yaml`. The default is short: the number, its context, nothing else.
- Round in the presentation, never in the data. Presenting 3,412.67 as 3,410 is fine; storing it that way is not.

**Write on the way out.** A close writes the month's row in `## Monthly Totals` with its `As of`, `Reconciled` and top three categories, and advances every affected `## Due` row; anything the user will re-read goes to `artifacts/` with its `## Boxes` line and read condition in the same turn; the tax-year pack goes to `artifacts/tax-year-<year>.md`; a variance against a shared target changes nothing in `~/Clawic/data/finances/budget.md` unless the user changes the target, in which case that row is updated in place. Formats in `memory-template.md`.
