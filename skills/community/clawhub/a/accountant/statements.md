# Statements — Building Them, Tying Them, Reading Them

Three statements, one set of facts. Each answers a question the other two cannot, and none of them is trustworthy alone.

**Before producing any statement**, read `## Period Status` in `~/Clawic/data/accountant/memory.md` (which accounts are unreconciled and since when) and `## Results` or `results.md` if `## Boxes` points there — a period presented without its comparatives is a number, not a report.

**Contents:** [What Each One Answers](#what-each-one-answers) · [Building The Cash Flow Statement](#building-the-cash-flow-statement) · [Presentation Choices That Change The Read](#presentation-choices-that-change-the-read) · [Ratios That Change A Decision](#ratios-that-change-a-decision) · [Reading A Set Of Statements](#reading-a-set-of-statements) · [Statements For A Lender Or Investor](#statements-for-a-lender-or-investor) · [Framework Differences That Show Up](#framework-differences-that-show-up)

## What Each One Answers

| Statement | Question | Time | Fails to show |
|---|---|---|---|
| Balance sheet | What is owned and owed at one instant | A point | Anything about the period; a balance sheet cannot show performance |
| Income statement | Was value created over the period | A span | Whether any of it turned into money |
| Cash flow statement | Where money actually came from and went | A span | Whether the business is profitable |
| Statement of equity | How the owners' stake changed and why | A span | Required whenever contributions, draws, or distributions moved |

The classic failure mode of a business that dies while profitable is visible only in the third: growing profit, growing receivables, falling cash.

## Building The Cash Flow Statement

Indirect method, because it derives from two balance sheets and a P&L rather than from tagged cash flows.

```
Net income
+ Depreciation, amortization, and other non-cash charges
± Loss / gain on asset disposal        (a gain is subtracted: the cash is in investing)
− Increase in receivables              (+ if they fell)
− Increase in inventory                (+ if it fell)
− Increase in prepaid expenses         (+ if they fell)
+ Increase in payables and accrued liabilities   (− if they fell)
+ Increase in deferred revenue         (− if it fell)
= Cash from operating activities

− Purchases of fixed assets  + proceeds from disposals
= Cash from investing activities

+ Loans drawn  − principal repaid  + owner contributions  − draws and distributions
= Cash from financing activities

Operating + investing + financing + opening cash = closing cash
```

- **The direction rule, once**: an increase in an asset consumes cash; an increase in a liability provides it. Everything above follows from that one line.
- **Closing cash must equal balance sheet cash**, which must equal the sum of reconciled account balances. This is the tie that catches misclassified cash equivalents and unreconciled accounts (SKILL.md ties).
- **Loan payments split**: principal is financing, interest is operating. Putting the whole payment in financing is the most common cash flow error after the sign rule.
- **Non-cash transactions never appear** — an asset acquired on finance, a debt converted to equity, a lease recognized. They are disclosed separately, and omitting the disclosure makes the investing section look implausibly small.
- Direct method presents receipts and payments by category; it is preferred by standard setters and produced by almost nobody, because it needs cash flows tagged at source. Build it only when someone manages collections and payments from it (SKILL.md, Where Experts Disagree).

## Presentation Choices That Change The Read

- **Comparatives are not optional.** A single-period statement cannot be interpreted. Minimum: current period and the same period last year for the P&L; current and prior year-end for the balance sheet.
- **Same basis on both columns.** A cash-basis prior year against an accrual current year is not a comparison; label the basis on every statement (SKILL.md Output Gates).
- **Gross margin needs an honest COGS.** Moving delivery costs into operating expenses inflates gross margin and makes the company look like software. The split is defined once in the chart and never adjusted to flatter a period (`bookkeeping.md`).
- **Common-size** — every P&L line as a percentage of revenue, every balance sheet line as a percentage of total assets — is what makes two periods of different size comparable, and it exposes creep that absolute numbers hide.
- **Materiality in presentation**: aggregate lines below the threshold into "other" and disclose what is in it. Twelve accounts under 1% each make a statement unreadable.
- **Order matters**: current assets before non-current, current liabilities before long-term, operating result before other income. Readers scan for the subtotals, and a non-standard order gets misread rather than examined.

## Ratios That Change A Decision

Formula first, then what the number has to be compared against. A ratio with no comparison — prior period, budget, or industry — is a fact, not information.

| Ratio | Formula | Reads as |
|---|---|---|
| Current ratio | Current assets ÷ current liabilities | Below 1 means current obligations exceed what is expected to become cash within the year |
| Quick ratio | (Current assets − inventory − prepaid) ÷ current liabilities | The same test without assuming stock sells |
| Gross margin | (Revenue − COGS) ÷ revenue | Pricing and delivery efficiency; only meaningful if COGS is defined consistently |
| Net margin | Net income ÷ revenue | What survives everything |
| DSO | (Average receivables ÷ credit sales) × days in period | Days of sales sitting uncollected; compare to stated terms, not to an ideal |
| DIO | (Average inventory ÷ COGS) × days in period | Days of stock held |
| DPO | (Average payables ÷ purchases) × days in period | Days taken to pay; rising DPO is either negotiation or distress |
| Cash conversion cycle | DSO + DIO − DPO | Days of working capital each sales cycle consumes; a negative cycle means customers fund the business |
| Debt to equity | Total liabilities ÷ total equity | Leverage; the covenant version usually excludes owner loans, so read the definition in the agreement |
| Interest cover | Operating profit ÷ interest expense | How far profit can fall before interest is unaffordable |
| Break-even revenue | Fixed costs ÷ gross margin % | The revenue level at which the period makes zero |
| Runway in months | Cash ÷ average monthly net cash burn | Only from the cash flow statement, never from profit (`cfo` owns the forecast) |

Worked example: fixed costs 42,000 per month, gross margin 62% → break-even revenue = 42,000 ÷ 0.62 = 67,742 per month. A 5-point margin fall moves it to 73,684 — an extra 5,942 of revenue needed to stand still, which is the number that makes a discount policy visible.

## Reading A Set Of Statements

In this order, because each step reframes the next:

1. **Cash first**: closing balance and the operating line. Positive profit with negative operating cash means the profit is in receivables, inventory, or an accrual that will not convert.
2. **Revenue quality**: one customer, one month, or one contract carrying the period. Concentration is a risk that no ratio shows.
3. **Gross margin trend** over at least four periods. A one-period move is noise; three periods in one direction is a pricing or cost structure change.
4. **Working capital movement**: the three balances that consume cash. A business growing 30% with 30% more receivables is not funding itself.
5. **Balance sheet oddities**: a suspense balance, an owner loan that grows every month, an asset nobody can identify, accrued liabilities that never clear. Each is an unfinished entry, not a fact.
6. **The equity bridge**: opening equity + net income + contributions − draws = closing equity. If it does not walk, something was posted directly to retained earnings (SKILL.md ties).

## Statements For A Lender Or Investor

- Label them for what they are: **management accounts prepared from the books**, on the stated basis. Never "audited", "reviewed", or "compiled" — those words are attestation engagements reserved to licensed practitioners (SKILL.md, Escalate).
- Include the basis, the period, the currency, comparatives, and the preparation date on every page. A statement without a basis label will be read on whichever basis the reader assumes.
- Expect the covenant definitions to differ from the statement's own subtotals — adjusted EBITDA, working capital, and net debt are contractual terms, not accounting ones. Compute them from the agreement's wording and show the bridge from the statutory figure.
- Save the exact set that was sent to `artifacts/statements-<period>.md` with the date and recipient. When someone asks a question about a figure eight months later, the version they hold is the one that matters.

## Framework Differences That Show Up

Relevant when `reporting_framework` is not `us-gaap`, or when an entity may be sold to or consolidated by a group on another framework.

| Area | US GAAP | IFRS |
|---|---|---|
| Inventory costing | FIFO, weighted average, and LIFO permitted | LIFO prohibited |
| Inventory write-down | Reversal prohibited | Reversal required when the reason no longer exists |
| Development costs | Expensed as incurred, with narrow exceptions | Capitalized when defined criteria are met |
| Fixed asset measurement | Cost model only | Cost or revaluation model |
| Impairment | Two-step, undiscounted cash flows first, reversal prohibited | One-step, recoverable amount, reversal permitted for non-goodwill |
| Statement titles and order | Balance sheet, liquidity order | Statement of financial position, often least-liquid first |

Tax-basis statements are a fourth option: legitimate, cheaper to produce, and unacceptable to most lenders. Label them explicitly.

**Write when this file produced something durable**: headline figures for the period → `## Results`. A statement set actually delivered to someone outside the entity → `artifacts/statements-<period>.md` with its recipient and date, plus its `## Boxes` line. A covenant definition and its bridge → `artifacts/` as a policy. A tie that failed and why → `## Open Items` (`memory-template.md`).
