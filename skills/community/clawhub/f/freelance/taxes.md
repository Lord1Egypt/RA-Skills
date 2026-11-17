# Taxes and Entity — Self-Employment Money Mechanics

Scope: what a freelancer owes, when, through which legal structure, and what is deductible. Bookkeeping mechanics and the close are `accountant`; cross-border VAT and withholding are `international.md`.

**Before any tax answer**, read `tax_jurisdiction`, `business_entity`, `tax_setaside_pct` and `currency` in `config.yaml`, and `## Due` in `~/Clawic/data/freelance/memory.md`. **While `tax_jurisdiction` is unset, name the country whose rules you are applying before answering** — tax advice for the wrong country is worse than none. Rates, thresholds and deadlines change every year: treat every figure here as a structure to verify, not a current number.

**Contents:** [The Three Taxes](#the-three-taxes) · [Entity Choice](#entity-choice) · [Estimated Payments](#estimated-payments) · [VAT and Sales Tax](#vat-and-sales-tax) · [Deductions](#deductions) · [Retirement](#retirement) · [Records and Retention](#records-and-retention) · [When to Hire an Accountant](#when-to-hire-an-accountant) · [Jurisdiction Notes](#jurisdiction-notes)

## The Three Taxes

Every freelancer, everywhere, is dealing with some combination of three things. Naming which one a question is about prevents most confusion.

| Tax | What it is | Freelancer's exposure |
|---|---|---|
| Income tax | On profit (revenue minus allowable costs), at personal or corporate rates | The one everyone expects |
| Social contributions | Pension, health and unemployment systems — self-employment tax, National Insurance, cotisations, cuota de autónomos | The one that surprises: often a flat or near-flat charge on profit, sometimes payable even at low income |
| Consumption tax | VAT, GST, sales tax, charged to the client and remitted | Never your money; registration is threshold- or election-based (→ VAT) |

**Effective total burden for a mid-income sole trader commonly lands somewhere between 25% and 45% of profit** once income tax and social contributions are combined — the spread across countries and income levels is genuinely that wide, which is why `tax_setaside_pct` must be computed from an actual estimate rather than left at the 30% default.

## Entity Choice

Decided by three things: liability exposure, the tax difference at your profit level, and whether clients will contract with an individual.

| Structure | Fits | Costs | Watch |
|---|---|---|---|
| Sole trader / sole proprietor / autónomo | Default, low profit, low liability work | Cheapest and fastest to register | Unlimited personal liability; insurance carries the risk instead (`insurance.md`) |
| Single-member LLC (US) | Liability separation without corporate complexity | Formation and annual state fees | Taxed as a sole proprietor by default; the liability shield is the point, not tax |
| S-corp election (US) | Higher profit, where a reasonable salary plus distributions reduces self-employment tax | Payroll, filings, accountant — commonly a few thousand a year | Only worth it once the saving clearly exceeds those costs; "reasonable salary" is enforced |
| Limited company (UK/IE and similar) | Higher profit, clients that will not contract individuals, or liability concerns | Accounts, corporation tax, payroll or dividends admin | Off-payroll rules can neutralize the tax advantage on client-facing contracts (`classification.md`) |
| Umbrella company | Contracts caught by off-payroll rules, or clients who insist | A margin per period | You are effectively an employee for tax with none of the practice's flexibility |
| Partnership | Two or more principals genuinely sharing the practice | Agreement drafting | Joint liability; needs a written partnership agreement before the first disagreement |

**The trigger to incorporate** is arithmetic: incorporate when `annual tax saving > incorporation + accounting + payroll costs`, plus any client that refuses to contract an individual, plus a liability exposure insurance cannot cover. That threshold is jurisdiction-specific — get it computed once, locally, and record the decision in `artifacts/decision-entity.md`.

## Estimated Payments

Tax authorities want the money during the year, not after it.

- **US**: quarterly estimated payments, ordinarily due 15 April, 15 June, 15 September and 15 January of the following year. Safe harbour: paying 100% of the prior year's tax (110% above a higher-income threshold) or 90% of the current year's generally avoids the underpayment penalty. Self-employment tax combines Social Security (up to an annual wage base that rises each year) and Medicare, with half of it deductible against income tax.
- **UK**: Self Assessment filed and paid by 31 January after the tax year ends, with payments on account on 31 January and 31 July, each 50% of the prior year's liability. The first year therefore produces a bill of roughly 150% of the year's tax at once — the classic first-year cashflow shock.
- **EU members** vary: quarterly or monthly prepayments of income tax and social contributions are common, and several charge social contributions on a schedule independent of profit.
- Whatever the regime, put **every payment date in `## Due`** with its amount estimate, and let the 13-week forecast see it (`cashflow.md`).

## VAT and Sales Tax

- **Registration is threshold-based, and thresholds move.** The UK's VAT registration threshold has been £90,000 of taxable turnover since April 2024; other countries range from near-zero (registration from the first invoice) to substantial. Check the current figure for `tax_jurisdiction` before advising, and check whether the threshold is rolling-12-month or calendar-year.
- **Voluntary registration can pay** when clients are businesses that reclaim it and you have input costs to recover; it never pays when clients are consumers, because the price rises or the margin falls.
- **Charge, collect, remit — none of it is income.** Keep VAT collected in the tax account (`cashflow.md`).
- **Cross-border B2B services within the EU** are generally reverse-charged to the customer, who accounts for the VAT; the invoice carries a reverse-charge note and the customer's validated VAT number (`international.md`).
- **US sales tax** rarely applies to professional services but does apply to some digital products and to services in specific states — economic nexus rules mean an out-of-state client can create an obligation. Check per state when selling anything productized.
- **Simplified schemes** exist in several countries (flat-rate percentages, cash accounting, small-business exemptions). They can be worth real money for a low-cost practice; ask an accountant once rather than defaulting.

## Deductions

The principle everywhere: **wholly and exclusively (or ordinary and necessary) for the business**, with a record. The categories a freelancer usually under-claims:

| Category | Typical treatment | Trap |
|---|---|---|
| Home office | A proportion of rent, utilities and internet by floor area or rooms, or a simplified flat rate | Exclusive-use requirements are strict in some regimes; and in a few places a home-office claim can affect a property's tax status on sale |
| Equipment | Deducted or depreciated depending on cost, regime and any immediate-expensing allowance | Personal-use proportion must be excluded |
| Software and subscriptions | Fully deductible when business-only | Shared personal/business plans need apportioning |
| Professional fees | Accountant, legal, contract review | Fees for a personal matter are not business costs |
| Insurance | Professional indemnity, public liability, cyber | Personal health cover has its own, different rules |
| Training | Usually deductible when it maintains or improves the skills of the *current* business | Training that qualifies you for a *new* trade is often not |
| Travel to a client | Deductible; commuting to a habitual workplace usually is not | A long single-client engagement can make their office a habitual workplace |
| Meals and entertainment | Partially deductible at best, and client entertainment is disallowed in several regimes | The most commonly over-claimed line |
| Bad debt | Deductible on accrual accounting where the income was recognized; usually not on cash accounting | You cannot deduct income never recognized (`disputes.md`) |
| Pension contributions | Often the largest legitimate deduction available (→ Retirement) | Annual limits apply |

**Records or it did not happen**: every deduction needs a receipt and a business reason. Filing received invoices and receipts is `invoices`; the ledger treatment is `accountant`.

## Retirement

The benefit most freelancers postpone indefinitely, and usually the biggest tax deduction available.

- **US**: SEP-IRA (simple, employer-style contribution as a percentage of net self-employment income) or Solo 401(k) (higher effective limits at moderate incomes because it combines an employee deferral with an employer contribution; allows a Roth side). Limits are indexed annually — check the current year.
- **UK**: personal pension or SIPP with tax relief at your marginal rate, subject to the annual allowance and carry-forward of unused allowance.
- **EU**: national self-employed schemes plus tax-advantaged private plans; social contributions may already fund a state pension, often at a level worth checking rather than assuming.
- **Mechanically**: contribute monthly by standing order from business income, treated like a tax payment, not from what is left at year end. What is left at year end is nothing, every year.

## Records and Retention

- **Keep**: invoices issued and received, contracts, bank statements, receipts, mileage or travel logs, and the working papers behind any filing.
- **Retention periods** commonly run 4-7 years (US federal generally 3 years from filing with longer windows in specific cases; UK 5 years after the 31 January filing deadline for the self-employed; several EU states 10 years). Use the longest applicable period and forget the distinction.
- **Digital is fine** in most regimes, and mandatory in a growing number — several countries now require digital record-keeping and electronic invoicing for VAT-registered businesses. Check whether `tax_jurisdiction` has a digital-filing mandate in force.
- **Never store a tax identifier, bank number or portal credential** in `~/Clawic/data/` — pointer only (`memory-template.md`).

## When to Hire an Accountant

Almost always worth it by the second year; the fee is deductible and usually smaller than one missed allowance.

| Signal | Why |
|---|---|
| First year of self-employment | Set-up done right costs one fee; unwinding it costs several |
| Considering incorporation | The trigger is arithmetic only a local professional can do accurately |
| Crossing a VAT or registration threshold | Timing and scheme choice have real money in them |
| Any cross-border client or move of residence | Treaty, source and permanent-establishment questions (`international.md`) |
| Revenue growing past a comfortable bookkeeping load | Your hour is billable; theirs is cheaper than yours |
| A letter from the tax authority | Do not answer it alone |

The accountant goes into the shared `~/Clawic/data/contacts/contacts.md` with their role and preferred channel, and their annual fee into `business_costs_per_year`.

## Jurisdiction Notes

Structural facts that change advice, useful for orientation and always to be verified.

- **US**: no VAT; self-employment tax is the surprise; 1099-NEC reporting from clients above a low threshold, and 1099-K from payment platforms at a threshold that has changed repeatedly; state income tax and local business licences add a second layer.
- **UK**: Self Assessment with payments on account; National Insurance for the self-employed; VAT threshold at £90,000 since April 2024; off-payroll rules dominate contracting through a company (`classification.md`).
- **EU generally**: reverse charge for cross-border B2B services; OSS schemes for B2C digital sales; social contributions are frequently the largest single charge and sometimes flat.
- **Spain**: autónomo contributions are banded by real income since 2023 rather than a flat minimum; quarterly IVA and IRPF filings.
- **Germany**: Kleinunternehmerregelung small-business VAT exemption below a turnover threshold; trade tax may apply depending on activity classification.
- **Canada / Australia**: GST/HST and GST registration thresholds with quarterly or annual remittance; instalment regimes for income tax.

**After any tax work**, write every deadline, filing and payment date into `## Due` in `~/Clawic/data/freelance/memory.md` with its cadence. **A computed set-aside percentage, entity, VAT status or jurisdiction is a declaration** — it goes into `config.yaml`, not `memory.md`. **An entity or VAT-registration decision** becomes `artifacts/decision-entity.md` with the numbers behind it, what was rejected and the condition that would revisit it, plus its `## Boxes` line in the same turn.
