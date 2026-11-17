# Inventory And COGS — Making Margin Mean Something

Inventory is the account where profit hides. Every unit on the shelf is an expense that has not happened yet, and every costing choice moves profit between periods.

**Before any inventory work**, read `## Coding Rules` in `~/Clawic/data/accountant/memory.md` for the declared costing method and count cadence, and `## Due` for the next count. Changing method silently between periods makes the comparative meaningless and, in most regimes, requires disclosure or permission.

## Perpetual Or Periodic

| | Perpetual | Periodic |
|---|---|---|
| Inventory account | Updated at every purchase and sale | Updated only at the count |
| COGS | Posted with each sale | Derived at period end |
| Requires | Item-level system, disciplined receiving | A count |
| Shrinkage | Visible as the gap between the system and the count | Invisible — it is inside COGS by construction |
| Fits | Anything with stock value above a few months of profit | Very small or slow-moving stock |

Periodic COGS formula: **opening inventory + purchases + freight-in + duty − purchase returns and allowances − closing inventory**. Everything unaccounted for — theft, breakage, miscounting, unrecorded samples — lands in COGS invisibly, which is exactly why a growing business outgrows periodic.

Under accrual, purchases are an **asset** on receipt and become COGS on sale. Expensing purchases at payment makes margin swing with buying rather than selling and leaves the inventory account permanently untieable (SKILL.md, Traps).

## Costing Methods

| Method | Cost assigned to a sale | Effect while prices rise | Availability |
|---|---|---|---|
| Specific identification | The actual unit's cost | Exact | Serialized or unique goods only |
| FIFO | Oldest cost | Higher profit, higher tax, balance sheet near current cost | Everywhere |
| Weighted average | Total cost ÷ total units, recomputed at each purchase under perpetual | Smooths both | Everywhere |
| LIFO | Newest cost | Lower profit, lower tax, balance sheet stuck at old costs | US GAAP only; prohibited under IFRS |

- **Weighted average worked**: 100 units at 10 plus 50 units at 16 → total 1,800 ÷ 150 = 12.00 per unit. Sell 60 → COGS 720, remaining 90 units at 1,080. Under perpetual, recompute after every receipt; under periodic, once at period end from the whole period's purchases.
- **The LIFO conformity rule** in the US: using LIFO for tax forces it in the financial statements too. That is a lasting commitment, not a year-by-year election, and it makes the balance sheet's inventory figure progressively less informative (SKILL.md, Where Experts Disagree).
- Method is declared once in `config.yaml` terms and written as a policy artifact with the date it was adopted. A change is a change in accounting policy, usually applied retrospectively and disclosed.

## What Belongs In Cost

Capitalize into inventory every cost of getting goods to their present location and condition:

- Purchase price net of trade discounts and rebates
- Freight-in, insurance in transit, customs duty and non-recoverable import taxes
- Direct handling and conversion labor, and for manufacturers, allocated production overhead

Exclude — these are period expenses, not inventory:

- Freight-out to the customer (a selling cost)
- Storage of finished goods, unless storage is part of the production process
- Abnormal waste, idle capacity, and rework beyond the normal rate
- Administrative overhead and selling costs
- Recoverable input tax (`sales-tax.md`)

**Landed cost matters more than people expect.** Goods at 100 with 12 freight, 6 duty, and 2 insurance have a unit cost of 120, not 100 — and a 40% "margin" computed from the invoice price is actually 25%. Allocate landed costs by value or by weight, consistently, and state which.

## Write-Downs

Inventory is carried at the **lower of cost and net realizable value** — the estimated selling price less the costs to complete and sell. Under US GAAP, LIFO and retail-method inventories use lower of cost or market instead, which has ceiling and floor bounds; everything else uses NRV.

```
Dr Cost of goods sold or Inventory write-down expense
  Cr Inventory (or an inventory valuation allowance)
```

- Test at least annually, and immediately on an observable trigger: a discontinued line, damage, a competitor price cut, a returned batch, or stock older than its sales cycle.
- **Reversals**: prohibited under US GAAP — the written-down amount becomes the new cost. Required under IFRS when the reason no longer exists, capped at original cost. This is a genuine framework divergence, not a preference.
- Obsolescence provisions built from an aging of stock (units held longer than X months) are defensible; a flat percentage of the balance is not, for the same reason a flat bad-debt percentage is not (`receivables.md`).

## Counting

- Count at least annually, at or near period end, with a documented procedure: count sheets without system quantities pre-printed, two people on high-value items, and a recount of every variance above the materiality threshold.
- **Freeze movement during the count**, or record what moved and adjust for it. Goods received during a count are the classic source of a variance that nobody can reproduce afterwards.
- Cycle counting — counting a subset continuously so everything is counted a few times a year — beats one annual count for anything with real turnover, and it converts a shutdown into a routine.
- The adjustment is Dr shrinkage expense (or COGS) / Cr inventory, posted in the period counted, with the count sheet retained. A count variance that is quietly absorbed into COGS without an entry leaves the register and the ledger permanently apart.
- Persistent shrinkage above a few percent is a control problem, not a costing problem (`audit.md`).

## Goods In Transit, Consignment, And Returns

| Situation | Whose inventory | Trigger |
|---|---|---|
| Shipped FOB shipping point | The buyer's, from dispatch | Include in-transit purchases at period end |
| Shipped FOB destination | The seller's, until delivery | Exclude from the buyer's count |
| Consignment stock | The consignor's, until sold to the end customer | Never in the consignee's inventory, however it sits on their shelf |
| Sale with a right of return | Revenue recognized net of expected returns; a return asset is recognized for the goods expected back | Estimate from the entity's own return history (`revenue.md`) |
| Customer-owned materials being worked on | Not the entity's inventory at all | Only the conversion work is revenue |

## Manufacturing And Work In Progress

- Three inventory accounts, not one: raw materials → work in progress → finished goods. Costs flow between them, and only the finished-goods movement becomes COGS.
- WIP carries materials issued, direct labor, and applied overhead. Overhead is applied on a stated driver (machine hours, labor hours, units) at a rate set from budget, and the difference between applied and actual is a variance closed at period end — to COGS if immaterial, allocated across inventory and COGS if not.
- **Standard costing** is legitimate and efficient, but the variances are the information: a favorable price variance next to an unfavorable usage variance usually means a cheaper input that wastes more.
- A manufacturer that reports gross margin without absorbing production overhead into inventory is overstating current profit whenever production exceeds sales.

**Write when this file produced something durable**: the costing method, landed-cost allocation basis, or the obsolescence policy → `artifacts/policy-inventory.md` with its `## Boxes` line. A count and its adjustment → `## Open Items` if unexplained, and the count date in `## Due`. A write-down and its trigger → `## Open Items` plus the entry. The count cadence → `## Due` (`memory-template.md`).
