# Cashflow — Buffer, Set-Aside, Concentration

Scope: making irregular income behave like a salary, and stopping the practice from being one client's decision away from zero. Personal money decisions beyond the practice are `money`; bookkeeping and the close are `accountant`.

**Before any cashflow answer**, read `income/<year>.md` (all closed months this year and last), `## Engagements` for committed revenue, and `config.yaml` for `runway_months_target`, `tax_setaside_pct` and `client_concentration_cap_pct`. A buffer figure quoted without the real monthly cost base is decoration.

**Contents:** [The Four Accounts](#the-four-accounts) · [Pay Yourself a Salary](#pay-yourself-a-salary) · [The Buffer](#the-buffer) · [Tax Set-Aside](#tax-set-aside) · [Sinking Funds](#sinking-funds) · [Concentration Risk](#concentration-risk) · [Forecasting 13 Weeks](#forecasting-13-weeks) · [The Bad Quarter](#the-bad-quarter) · [Benefits You Now Fund Yourself](#benefits-you-now-fund-yourself)

## The Four Accounts

The structure that removes most freelance money anxiety, because each question has one account that answers it.

| Account | Holds | Rule |
|---|---|---|
| Business current | Incoming client payments, business costs | Everything arrives here; nothing personal leaves it |
| Tax set-aside | `tax_setaside_pct` of every cleared payment | Never spent, never counted as runway, never borrowed from (SKILL.md Rule 3) |
| Buffer | `runway_months_target` × monthly costs | Touched only in the trigger conditions below |
| Personal current | The fixed monthly salary you pay yourself | This is the only number personal budgeting ever sees |

Registered in the shared `~/Clawic/data/finances/accounts.md` as references only, never account numbers. Mixing personal and business money costs deductions and accountant hours every single year; separating it is one afternoon.

## Pay Yourself a Salary

- **Set a fixed monthly transfer** from business current to personal, sized at `(conservative annual take-home) ÷ 12`, where conservative means the trailing 12 months minus the best month.
- **Never vary it with the month.** A good month funds the buffer; a bad month draws from it. The transfer stays flat, which is the entire point — personal spending calibrates to whatever it sees, and a 14,000 month teaches expensive habits.
- **Raise it once a year**, when the trailing twelve months support it, not after one strong quarter.
- Owner draws versus payroll is an entity and jurisdiction question with real tax consequences (`taxes.md`); the discipline above applies whichever mechanism is used.

## The Buffer

`buffer target = runway_months_target × (personal monthly costs + business monthly costs)`.

- **Business costs count.** Insurance, tools, accountant and subscriptions keep billing during a dry month; a personal-only buffer runs out early.
- **The tax set-aside is not buffer.** It is a payable with a date on it.
- **Withdraw only for**: a dry month where the salary transfer cannot be covered, a funded holiday or sick period (→ Sinking Funds), or a deliberate investment with a payback case. Not for equipment envy and not for a client's late payment — that is a collections problem (`getting-paid.md`).
- **Refill first, before any discretionary spend, until the target is met.** The rebuild is the highest-return use of a good month, because it is what lets the practice refuse bad work.
- **Sizing**: 3 months is the minimum that lets you say no; 6 is the default; 9-12 for a practice with long sales cycles, one dominant client, or dependents.

## Tax Set-Aside

- **Move it the day the payment clears.** A standing rule beats a monthly intention: money in the working account is spent by definition.
- **Sizing** `tax_setaside_pct`: the default 30% covers income tax plus self-employment or social contributions for many mid-income sole traders, but the right number is jurisdiction- and entity-specific and can be materially higher. Compute it once from an actual estimate (`taxes.md`) and record it in `config.yaml` rather than leaving the default in place.
- **VAT and sales tax are not yours at any point.** If registered, they are collected on behalf of the authority; keep them in the same account and consider the balance untouchable.
- **Under-setting is the classic first-year failure**: year one's tax bill can arrive with a payment-on-account for year two attached, so the first bill is larger than the first year's liability. Ask what the jurisdiction does on the first filing before deciding the percentage.
- **Reconcile quarterly** against the real estimate and adjust the percentage, rather than discovering a gap at the filing deadline.

## Sinking Funds

Named future costs, funded monthly from business income, so they never become emergencies.

| Fund | Sizing | Note |
|---|---|---|
| Holiday | Days you intend to take × day rate, or the equivalent salary months | Unfunded holiday becomes no holiday (`capacity.md`) |
| Sick days | 5-10 days a year at the day rate as a minimum | The practice has no sick pay; this is that |
| Equipment | Replacement cost ÷ expected life in months | A dead laptop is not an emergency, it is a Tuesday |
| Insurance and professional fees | Annual premiums ÷ 12 | Renewals cluster and are big enough to hurt in one month |
| Training and conferences | An annual figure decided in advance | Otherwise it is always the thing that gets cut |
| Bad debt | 1-3% of revenue, once the practice has any history | Makes the eventual write-off a line item, not a shock (`disputes.md`) |

## Concentration Risk

`concentration = largest client's trailing-12-month revenue ÷ total trailing-12-month revenue`, recomputed monthly from `income/<year>.md`.

| Level | Meaning | Action |
|---|---|---|
| <40% | Healthy | Keep the two active channels running |
| 40-60% | Warning | Pipeline restarts now, while the big client is happy — that is the only moment it is easy |
| 60-70% | Dangerous | Their reorg is your unemployment; every quote you send is negotiated from weakness |
| >70% | Employment without the protections | Also a live classification exposure (`classification.md`): a single client, exclusive, long-running, is exactly the fact pattern |

De-risking sequence, in order: keep a second client alive even at a lower rate → convert the big client to a retainer with a real notice period (a contractual buffer, not a moral one) → raise the rate on new work so the same income needs fewer hours → deliberately release capacity to sell. Never de-risk by resenting the big client; they are usually the best client you have.

## Forecasting 13 Weeks

The only forecast a solo practice needs, refreshed weekly during the pipeline hour.

1. Opening cash.
2. **Committed inflows**: signed engagements, by expected payment date, not invoice date. Apply the observed DSO from `income/<year>.md`, not the contracted terms.
3. **Probable inflows**: pipeline value × its stage probability. Never count anything unquoted.
4. **Outflows**: salary transfer, business costs, tax payment dates from `## Due`, sinking-fund contributions.
5. **The line to watch is the lowest weekly balance**, not the ending balance. A 13-week forecast that ends healthy and dips below zero in week 6 is a crisis with a happy ending.

Quarterly tax payments and annual insurance renewals are the two outflows that most often produce that dip. They are both in `## Due` precisely so the forecast can see them coming.

## The Bad Quarter

In order. The order is the content.

1. **Cut discretionary business spend** — subscriptions first, and cancel rather than pause (the shared `finances/subscriptions.md` is the list, and it is always longer than remembered).
2. **Hold the salary transfer**, drawing from the buffer, and do not reduce it while the buffer exists: personal instability makes selling worse.
3. **Collect** — every overdue invoice, every unbilled hour, every completed milestone not yet invoiced. Most practices in a cash squeeze are owed a month's revenue.
4. **Sell** at full rate (`pipeline.md`, dry-spell protocol). Rate cuts are permanent; scope cuts are not.
5. **Only then** consider deferring a tax payment through an official arrangement — never by silently not paying — or short-term financing, with the cost stated as an annual percentage before signing anything.
6. **Never** dip into the tax set-aside. It is the one line that turns a bad quarter into a bad year with penalties attached.

## Benefits You Now Fund Yourself

Every one of these was inside a salary and is now inside the rate (`rates.md`). Cost them and put the sum into `business_costs_per_year`.

| Benefit | How a freelancer funds it |
|---|---|
| Holiday and public holidays | Priced into the rate, held in the holiday sinking fund |
| Sick pay | Sick-day fund; income-protection insurance above a threshold you can define (`insurance.md`) |
| Pension | A deliberate monthly contribution to a self-employed scheme; jurisdiction-specific and often tax-advantaged (`taxes.md`) |
| Health cover | Private cover where the country requires it; a real cost line, not an afterthought |
| Parental leave | Statutory support for the self-employed varies hugely; assume nothing and check locally before it is needed (`capacity.md`) |
| Equipment and software | Equipment sinking fund |
| Training | Annual training budget, decided in advance |
| Employer social contributions | Now yours, and inside `tax_setaside_pct` |

**After any cashflow work**, write the month row into `income/<year>.md` when the month closes (invoiced, collected, billable hours, hours worked, largest client share, DSO), and recompute concentration and effective rate in the same turn. **Buffer target, salary figure and sinking-fund sizes** are declarations: they go into `config.yaml`, not `memory.md`. **Any tax, VAT, renewal or payment date** discovered goes to `## Due`. **Business accounts and subscriptions** go to the shared `~/Clawic/data/finances/`, as references only.
