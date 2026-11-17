# Foreign Currency — Rates, Revaluation, And Foreign Operations

Two different problems wear the same name. Recording a transaction in another currency is arithmetic; consolidating a foreign operation is a translation method. Confusing them produces gains and losses in the wrong statement.

**Before booking anything in another currency**, read `## Books` in `~/Clawic/data/accountant/memory.md` for the declared functional currency and `## Coding Rules` for the rate source in use. Two rate sources for the same currency produce differences nobody can reconcile.

## Functional Currency Comes First

The functional currency is the currency of the **primary economic environment** in which the entity operates — not the owner's preference and not the reporting currency. Indicators, in order of weight:

1. The currency that mainly influences sales prices and the market the entity competes in
2. The currency that mainly influences labor, material, and other operating costs
3. Secondary: the currency in which financing is obtained and receipts are retained

Once determined it changes only when the underlying facts change, and the change is applied prospectively. Document the determination and its date — it is the assumption every subsequent figure rests on, and most software will not let it be changed after the first transaction (`software.md`).

**Reporting currency** can differ from the functional currency; that difference is what translation exists to bridge.

## Which Rate, When

| Item | Rate |
|---|---|
| Transaction on the day it occurs | Spot rate on the transaction date; an average for the period is acceptable for high-volume, evenly spread transactions when rates are not volatile |
| Monetary balances at period end — cash, receivables, payables, loans | Closing rate |
| Non-monetary items at historical cost — fixed assets, inventory, prepaid | Historical rate at acquisition; they are never retranslated |
| Non-monetary items at fair value | Rate at the date fair value was measured |
| Equity contributions and draws | Historical rate on the date of the transaction |

**The monetary/non-monetary split is the whole rule.** A machine bought for 100,000 EUR when EUR/USD was 1.10 stays at 110,000 USD forever; the unpaid supplier balance for the same machine is retranslated at every close and generates FX movement until it is paid.

## Realized And Unrealized

```
Invoice a customer 10,000 EUR at 1.10        Dr AR 11,000 USD  / Cr Revenue 11,000 USD
Period end, rate 1.14, still unpaid          Dr AR    400 USD  / Cr Unrealized FX gain 400
Payment received, rate 1.12                  Dr Cash 11,200 USD / Cr AR 11,400 / Dr Realized FX loss 200
```

- Revenue is fixed at the transaction rate and **never** restated. Everything after it is an FX movement, not a change in sales. Adjusting revenue for rate movement is the most common error in multi-currency books.
- **Unrealized** gains and losses come from retranslating open balances at period end; **realized** ones crystallize on settlement. Both go to the income statement — normally in other income and expense, below the operating result, because they are not operating performance.
- Keep them in **separate accounts**. A single combined FX account cannot answer "how much of this is still exposed", which is the only question the balance is useful for.
- Revaluation runs at every close, on every monetary balance in a non-functional currency, including foreign bank accounts. Software usually automates it and posts to an account nobody watches — know which one and review it monthly (`software.md`).
- Reconcile a foreign-currency bank account **in its own currency first**, then revalue. Reconciling against the functional-currency ledger balance mixes a transaction problem with a rate problem and solves neither (`reconciliation.md`).

## Rate Sources And Consistency

- Pick one source — the central bank's published rate is the usual default and is what most authorities accept — and use it for everything. Record which source and which time of day in `## Coding Rules`.
- Several tax authorities **mandate** a specific rate for tax purposes (a monthly published rate, or the customs rate for imports), which can differ from the accounting rate. That difference is a reconciling item, not an error.
- The rate a bank actually gives is the spot rate plus a spread. Booking at the bank's rate blends an FX movement with a bank charge; booking at the reference rate and the difference as a fee is more useful and matches what the bank statement supports.
- Payment processors settling in a different currency from the sale create the same split: the difference between the transaction rate and the settlement rate is FX, not a processing fee (`reconciliation.md`).

## Translating A Foreign Operation

Applies when a subsidiary or branch has a **different functional currency** from the reporting currency. This is translation, and it does not touch profit.

| Item | Rate | Where the difference goes |
|---|---|---|
| Assets and liabilities | Closing rate | Cumulative translation adjustment in equity |
| Income and expenses | Rate at transaction date, or the period average | Same |
| Equity | Historical rates | Same |

- The balancing figure — the **cumulative translation adjustment** — sits in other comprehensive income and accumulates in equity. It moves to profit only when the operation is disposed of.
- **Remeasurement** is the different case: an entity keeps records in one currency but its functional currency is another. Then the monetary/non-monetary rules above apply and the difference **does** hit profit. Getting these two backwards is the classic consolidation error, and it moves real money between profit and equity.
- Intercompany balances are eliminated on consolidation, but the FX on them is not automatically eliminated — a long-term intercompany loan that is effectively part of the net investment is treated differently from a trading balance.

## Working Across Borders

- **Withholding tax** on cross-border payments for services, royalties, interest, or dividends is deducted by the payer, is often reducible by treaty, and requires a residence certificate to claim the reduced rate. Book the gross expense and the withholding as a tax receivable or expense — booking only the net understates both the cost and the tax credit.
- **Transfer pricing** applies to any transaction between related entities across a border, and both sides must be at arm's length with documentation. A management fee or an intercompany loan set at a round number and never supported is the standard finding.
- **Permanent establishment**: an employee, a fixed place of business, or a dependent agent concluding contracts in another country can create a taxable presence there. It is a legal determination with retroactive consequences — escalate the moment it is plausible (SKILL.md, Escalate).
- **Import duty and import VAT** arrive from carriers and customs rather than the supplier; duty is never recoverable and belongs in inventory cost, import VAT is usually recoverable (`inventory.md`, `sales-tax.md`).

## Digital Assets

Where the entity holds or accepts cryptocurrency, the mechanics resemble foreign currency but the classification does not:

- It is generally **not** cash and not a foreign currency for accounting purposes — most frameworks treat holdings as an intangible or, where the framework permits, at fair value with movements in profit.
- **Every disposal is a taxable event in most regimes**, including paying a supplier or converting between assets, with gain or loss measured against the cost basis of the specific units disposed of.
- Cost basis tracking (per lot, with a consistently applied disposal order) is the entire difficulty. Without it, no gain can be computed and no return can be supported.
- Accepting crypto as payment records revenue at the fair value in the functional currency **on the day of receipt**; everything after that is a holding gain or loss, not revenue.

**Write when this file produced something durable**: the functional currency determination and the rate source → `artifacts/policy-currency.md` with its `## Boxes` line, and the source in `## Coding Rules`. A foreign account → `~/Clawic/data/finances/accounts.md` with its currency. A withholding tax certificate, a treaty position, or an intercompany arrangement → `artifacts/` and `## Open Items` until supported. Revaluation posted at close → the close row in `closes/<year>.md` (`memory-template.md`).
