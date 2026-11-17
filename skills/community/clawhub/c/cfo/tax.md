# Tax Exposure, Credits, and the Filing Calendar

Tax is the area where the cheapest action taken on time becomes the most expensive problem taken late. Nothing here is a tax opinion: it is what a CFO must recognize and route to a licensed advisor. Every current-law figure on this page is stated **as of July 2026**; rules and thresholds change, so confirm before modeling anything.

## Credits Worth Real Cash

- **R&D credit, payroll offset (US)**: qualified small businesses can apply the federal research credit against employer payroll taxes rather than income tax, with a cap that was raised to $500,000 per year for tax years beginning after 2022 and still at that level as of July 2026. That is cash for a company with no profit, and it is the most commonly unclaimed item on a startup's return. It requires a contemporaneous study and a timely filed return — retroactive claims are harder and sometimes impossible.
- **State-level credits and grants** exist in many jurisdictions and stack with the federal credit; ask the advisor which apply where employees actually sit.
- Capitalization rules for research expenditure in the US changed in 2022 and again in 2025 (position as of July 2026). The consequence to model is counterintuitive: under a capitalization regime a company with no book profit can still owe cash tax. Ask the advisor which regime applies to the current year before assuming a zero-tax forecast.

## Sales Tax, VAT, and Nexus

- Post-*Wayfair* (2018), US economic nexus is commonly triggered at **$100,000 of sales or 200 transactions per state per year** (as of July 2026), though several states have since dropped the transaction test and thresholds differ. You register where your customers are, not where you sit.
- SaaS taxability varies by state: the same subscription is taxable in some and exempt in others. This is a state-by-state determination, not a company-wide policy.
- Exposure accrues unnoticed: uncollected tax becomes a company liability plus penalties and interest, and it is a routine diligence finding that gets escrowed or deducted from price. A **voluntary disclosure agreement** typically limits the lookback period and abates penalties — the tool exists precisely for the company that discovers the problem itself.
- Outside the US, VAT/GST registration thresholds are lower and digital-services rules apply from the first sale in several regimes.

## Payroll and Remote Work

- An employee working from a state or country creates registration, withholding, and often income-tax nexus for the company there. Remote hiring is a tax decision disguised as a recruiting decision.
- Register before the first payroll in a new jurisdiction; late registration penalties are per-period and accumulate quietly.
- Reimbursement and per-diem rules, and the taxability of remote-work stipends, differ by jurisdiction — one policy applied globally is one policy wrong in several places.

## Equity Tax Exposure

- **409A** governs the strike price; the failure mode is tax exposure for every grantee, not a company penalty.
- **83(b)**: 30 days from purchase, no extensions.
- **ISO exercises** create an AMT preference item; **NSO exercises** create ordinary income with employer withholding — payroll must be warned before a large exercise.
- **QSBS (Section 1202)**: the classic conditions are original-issue stock in a domestic C corporation with gross assets under $50M at issuance, an active-business test, and a 5-year hold, with the gain exclusion capped at the greater of $10M or 10× basis. 2025 legislation added a tiered holding-period schedule and a higher cap for stock issued after enactment, so eligibility now depends on issuance date (figures as of July 2026). Every founder question here goes to counsel — the difference between qualifying and not is the entire tax bill on an exit.
- Converting from an LLC to a C corporation, or the reverse, changes QSBS eligibility and the holding-period clock. Never model it as a formality.

## Entity and Franchise Tax

- C corporation is the default for venture-backed companies: investors' fund structures usually cannot hold pass-through interests, and QSBS requires a C corp. LLCs suit bootstrapped and cash-distributing businesses.
- Delaware franchise tax has two calculation methods; the authorized-shares method produces the alarming bill that arrives every spring, while the assumed-par-value-capital method usually produces a far smaller one for a startup with many authorized shares. Recalculate rather than paying the first number on the notice.
- Keep the entity structure reviewed before revenue makes restructuring expensive; reorganizations are cheap when there is nothing to move.

## Filing Calendar

| Recurring item | Typical timing |
|---|---|
| Contractor information returns (1099-NEC) | End of January |
| Employee wage statements (W-2) | End of January |
| ISO exercise reporting (Form 3921) | Same season as wage statements |
| Federal and state income tax returns, or extensions | Spring, with extensions common for startups |
| Delaware franchise tax | Annually, spring |
| Sales tax / VAT returns | Monthly or quarterly, per jurisdiction |
| R&D credit study and claim | With the return; the study starts during the year |
| 83(b) elections | 30 days from purchase — event-driven, never calendar-driven |

Put every recurring row in the close calendar so it is owned by a date rather than by memory.

## The Rule

Hire a startup-experienced tax advisor by first revenue, or by the first employee in a second jurisdiction, whichever comes first. Every item on this page is cheap to do on time and expensive to fix retroactively, and none of them are decisions the finance function should make alone (SKILL.md Human-in-the-Loop).
