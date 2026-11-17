# Going Multi-Country: Entities, Transfer Pricing, and FX

Every country you touch adds a permanent compliance obligation that outlives the reason you entered it. Enter deliberately, and know the exit cost before the entry cost.

## Hire First, Incorporate Later

| Situation | Vehicle |
|---|---|
| 1–3 people in a country, no local contracts | Employer of record (EOR) |
| Genuine independent contractors, bounded projects | Contractor agreements — but apply the control test: who sets the hours, provides the tools, and directs the method |
| Local sales team closing local contracts, or a growing team | Local entity |
| Local IP development, government incentives, or regulated activity | Local entity, with counsel on structure |

The crossover is arithmetic, not fashion: compare `EOR cost per employee per year × headcount` against `entity setup + annual accounting, payroll, audit and filing costs`. Compute it with real quotes; the crossover typically arrives at a handful of employees in one country, but the entity's ongoing compliance cost is the part teams forget.

**Permanent establishment** is the trap underneath: a salesperson habitually concluding contracts abroad, or a fixed place of business, can create a taxable presence for the parent even with no entity. An EOR does not eliminate PE risk from sales activity. Ask the question before the first sales hire in a country, not after the first tax notice.

## Transfer Pricing

- Once two entities exist, every service one provides the other must be priced at arm's length, documented in an **intercompany services agreement signed before the first intercompany invoice**, and supported by a benchmarking study.
- Routine back-office and R&D support services are commonly priced cost-plus. The markup must come from a benchmarking study for that function and geography — a rule-of-thumb percentage is exactly what an auditor challenges.
- Consequence of getting it wrong: the same profit taxed in two countries, plus penalties, plus a documentation exercise done retroactively under deadline.
- Documentation is cheap while the structure is simple. It is a project once there are three entities and history.

## Funding a Subsidiary

- Capital contribution vs intercompany loan changes the tax profile: a loan needs a real interest rate, real documentation, and runs into thin-capitalization limits; equity is simpler but harder to pull back.
- Fund on a schedule the local entity can actually spend, and keep the local balance thin. Cash parked in a subsidiary can be slow or costly to repatriate, and withholding tax may apply to dividends, interest, and royalties — treaty relief usually requires the right forms filed in advance.
- Loss-making subsidiaries paid on cost-plus still report a taxable profit locally. Model the local tax even when the group loses money.

## FX Exposure

Two distinct exposures, often confused:

- **Transaction exposure** — a real cash flow in a currency that is not yours: a contract billed in EUR, a payroll paid in GBP. This one can cost you money.
- **Translation exposure** — restating a foreign entity's balance sheet at the reporting rate. This one moves reported equity and rarely moves cash.

Hedging sequence:
1. **Natural hedge first**: match the currency of costs to the currency of revenue. A EUR-billing customer base funding EUR payroll needs no derivative.
2. **Contract terms next**: bill in your functional currency, or add an FX adjustment clause on multi-year contracts.
3. **Forwards last**, and only against contracted exposures. Hedging a forecast is speculation with paperwork.

Trigger to hedge at all: when a 10% adverse move in the exposed currency would cost more than one month of net burn. Below that, the hedging program costs more attention than the exposure costs money.

## Multi-Currency Accounting

- Each entity has a functional currency. Transactions convert at the rate on the date; period-end balances revalue at the closing rate; the P&L usually consolidates at an average rate. The difference lands as an FX gain or loss that is not operating performance — report it on its own line, or every variance analysis becomes a currency debate.
- Set `currency` in config as the reporting currency and state it on every artifact. A board pack that mixes currencies without saying so is a Red Flag for reconciliation.
- Intercompany balances must eliminate exactly on consolidation. They rarely do on the first close after an entity opens; reconcile monthly while the volume is small, and keep intercompany elimination on the close checklist.

## VAT / GST and Indirect Tax

- Registration thresholds abroad are far lower than US sales-tax thresholds, and several digital-services regimes require registration from the first sale to a consumer.
- B2B cross-border sales frequently use the reverse charge, shifting the obligation to the customer — but only with a valid customer VAT number on file and on the invoice. Invoice format requirements are substantive: a non-compliant invoice can deny your customer's deduction, and they will ask you to reissue.
- EU one-stop-shop style regimes let one registration cover many countries for qualifying sales; ask the advisor whether the model qualifies before registering in each country separately.

## Operating Reality

- Opening a local bank account can take weeks to months and often requires a local director or in-person signing. Start it before you need to run payroll.
- Local payroll providers, statutory benefits, and mandatory notice periods vary enormously; termination costs in most of Europe and Latin America dwarf US assumptions, and they land as cash out before any saving arrives.
- Statutory filings and audits are often mandatory for small local entities regardless of size. Budget the annual compliance cost per entity as a fixed line, and dissolve dormant entities — an unused subsidiary keeps filing obligations and diligence questions alive for years.
