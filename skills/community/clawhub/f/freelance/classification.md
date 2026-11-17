# Classification — Are You Actually Self-Employed Here?

Scope: the tests that decide whether an engagement is genuine self-employment or disguised employment, who bears the risk, and how to structure work so the answer is defensible. The employment side of a career decision is `career`; the contract wording is `contracts.md`.

**Before advising**, read `tax_jurisdiction` and `business_entity` in `config.yaml`, `## Engagements` for duration, exclusivity and committed hours, and the concentration figure from `income/<year>.md`. **While `tax_jurisdiction` is unset, name the regime you are applying first** — the tests differ enough that the wrong country's answer inverts the conclusion.

**Contents:** [Why It Matters](#why-it-matters) · [The Universal Factors](#the-universal-factors) · [The Regimes](#the-regimes) · [The Self-Check](#the-self-check) · [Structuring a Defensible Engagement](#structuring-a-defensible-engagement) · [Umbrella and Intermediary Arrangements](#umbrella-and-intermediary-arrangements) · [When the Client Gets It Wrong](#when-the-client-gets-it-wrong) · [Ex-Employer as Client](#ex-employer-as-client) · [Permanent Establishment](#permanent-establishment)

## Why It Matters

Misclassification is not a paperwork problem; it reallocates money and rights in both directions.

| Consequence | Who pays |
|---|---|
| Back social contributions, payroll tax, interest and penalties | Usually the client, sometimes both, occasionally the intermediary |
| Loss of deductions and the entity's tax treatment for the engagement | The freelancer |
| Retroactive employment rights: holiday pay, notice, unfair dismissal, minimum wage | Claimed by the worker against the client |
| Contract terminated abruptly to remove the risk | The freelancer, with no notice |
| Blanket policies ("no contractors, agency only") | The whole market for that client |

The asymmetry that matters in practice: **the client's risk is money, yours is the engagement**. A client who discovers exposure mid-contract fixes it by ending the contract, which is why the check happens before quoting, not after a year.

## The Universal Factors

Every regime weighs some version of the same list. No single factor decides; the overall picture does.

| Factor | Points to self-employment | Points to employment |
|---|---|---|
| Control | You decide how and when the work is done | They set hours, methods, supervision, tools |
| Substitution | You may send a qualified substitute, in practice as well as on paper | Personal service is required |
| Financial risk | Fixed price, you fix defects at your cost, you can lose money | Paid for time regardless of outcome |
| Equipment | Your own | Theirs, and their systems |
| Integration | Delivering a defined project | On the org chart, in team rituals, with an internal title |
| Mutuality of obligation | No obligation to offer or accept future work | Continuing expectation of work and availability |
| Exclusivity | Other clients, actively | One client, effectively full-time, for a long period |
| Business trappings | Own insurance, marketing, invoices, other clients, entity | None of the above; looks like a payroll worker with a different payment method |

**Duration and exclusivity are the two that quietly move an engagement over the line.** A three-week defined project for one client is fine; the same client, five days a week, eighteen months later, with a laptop they issued and a place in the standup, is employment however the contract is worded — and the label on the contract is the weakest evidence in every regime.

## The Regimes

| Regime | Test | Who decides |
|---|---|---|
| US federal (IRS) | Common-law control test in three categories — behavioural control, financial control, type of relationship. Form SS-8 requests an official determination | The IRS on the facts; the client's classification is only their opinion |
| California and similar states | **ABC test**: worker is an employee unless (A) free from control, (B) performing work **outside the hiring entity's usual course of business**, and (C) customarily engaged in an independently established trade. Prong B is the hard one, with statutory exemptions for many professional services | Statute; the exemptions are specific and worth reading |
| US Department of Labor (FLSA) | Economic-reality multi-factor analysis; the applicable rule has changed with administrations | Federal, for wage-and-hour purposes, separately from the IRS |
| UK — off-payroll (IR35) | Control, substitution, mutuality of obligation. Since April 2021, for medium and large private-sector clients and the public sector, **the client makes the status determination** and issues a Status Determination Statement; the fee-payer deducts tax if inside. For small clients, the contractor's own company decides | Client, unless the client is small |
| EU member states | National tests for "false self-employment" (Scheinselbstständigkeit, falso autónomo, and equivalents), typically weighting economic dependence — a single dominant client is often itself a criterion. The Platform Work Directive adds presumption rules for platform-mediated work | National authority or labour court |
| Elsewhere | Similar factor tests; some countries add a bright-line dependence percentage | Local authority |

Regimes are independent: an engagement can be a contractor relationship for one tax purpose and employment for another. Never generalize one determination to all of them.

## The Self-Check

Ten questions. Six or more "employment" answers means restructure the engagement or price the risk before signing.

1. Does the client set your working hours, or approve time off?
2. Do you work at their premises on their schedule, on their equipment, with their accounts?
3. Would they refuse a competent substitute?
4. Are you paid for time regardless of deliverables, with no financial risk?
5. Is there any prohibition on serving other clients, in the contract or in practice?
6. Do you appear in their org chart, directory or team page, with an internal title?
7. Do you attend internal management, performance or planning meetings as a member?
8. Has the engagement run continuously for more than about a year at near-full-time?
9. Is this client more than 70% of your revenue?
10. Would an outsider watching for a week be unable to tell you from an employee?

## Structuring a Defensible Engagement

The controls, cheapest first. Most cost nothing except being deliberate.

- **Contract for a deliverable**, not for availability: defined scope, acceptance criteria, an end date, and a renewal that is negotiated rather than automatic.
- **Keep a real substitution right** and never undermine it in practice.
- **Use your own equipment and accounts** where the client's security policy allows; where it does not, note the reason in writing — a security mandate is a much better explanation than a preference.
- **Invoice from the business** with your own numbering, terms and interest clause.
- **Keep at least one other client alive**, even a small one. It is the single most persuasive fact available (`pipeline.md`).
- **Decline internal-employee trappings**: performance reviews, internal titles, team-building, an internal email as your only identity, holiday requests. Being cooperative about these is what creates the exposure.
- **Take real financial risk**: fixed-price elements, defects fixed at your cost, your own insurance (`insurance.md`).
- **Break long engagements** with genuine gaps and a renegotiated scope, rather than an unbroken rolling extension.
- **Document it once, at signature**, in a short note stored in `artifacts/` with the factors and the reasoning. That note is the evidence if the question ever arrives.

## Umbrella and Intermediary Arrangements

When a contract is determined inside off-payroll rules, or the client only pays through an intermediary.

- **Umbrella**: you become their employee for the engagement; they run payroll, deduct tax and social contributions, and take a margin. Legitimate, and sometimes the only way to take the work.
- **Read what the margin actually is** and whether employer costs are being passed to you by inflating the assignment rate — quote and compare on **net take-home**, not on headline day rate, which is the only comparison that means anything here.
- **Avoid anything promising unusually high take-home** through loans, annuities, offshore structures or "non-taxable allowances". Those schemes have repeatedly ended with the worker owing years of back tax personally, long after the promoter disappeared.
- **Agency of record / employer of record** services do the same job for cross-border engagements, and are the standard answer when a foreign client cannot contract an individual (`international.md`).
- Inside-scope work still counts as revenue for concentration and utilization, but it usually cannot carry your normal deductions — recompute the effective rate before comparing it to a direct engagement.

## When the Client Gets It Wrong

- **Blanket determinations** ("all contractors are inside") are common and are a client risk-management choice, not a legal finding. They can be challenged through the client's status-disagreement process where the regime provides one, with reference to the actual working practices.
- **A determination you disagree with** is answered with facts — substitution, control, other clients, financial risk — in writing, not with an argument about the label.
- **If the client insists on employment-like working practices while paying contractor rates**, that is a pricing question and eventually a decline (`disputes.md` for terminating).
- **Never accept a contract term making you liable for the client's tax reclassification costs** without a cap and advice: it moves their entire exposure onto a person with no payroll department (`contracts.md`, red-line list).

## Ex-Employer as Client

The most common misclassification pattern in existence, and often still worth doing.

- Doing the same job, for the same manager, on the same systems, immediately after resigning is the textbook fact pattern in every regime.
- Make it defensible: a different, defined scope; a project with an end; your own equipment where possible; a gap between employment ending and the contract starting; and other clients within the first quarter.
- Watch the concentration number from day one — this engagement usually starts at 100% (`cashflow.md`).
- Some jurisdictions apply extra scrutiny or specific rules to a former employer engaging a former employee as a contractor. Check before signing rather than after the first filing.

## Permanent Establishment

Relevant the moment a client is in another country (`international.md` for the money side).

- A freelancer working from their own country for a foreign client does **not** usually create a taxable presence for that client — but habitually concluding contracts on their behalf, or operating as their dependent agent, can.
- Working *inside* the client's country for an extended period can create obligations for you: local registration, local tax residency, and sometimes a work-authorization question.
- Long on-site engagements abroad are exactly where a professional opinion is cheap relative to the risk (`taxes.md`, escalation table).

**After any classification assessment**, write the conclusion into `## Engagements` in `~/Clawic/data/freelance/memory.md` as a note on the engagement row (regime applied, determination, date), and save the reasoning to `~/Clawic/data/freelance/artifacts/classification-<client>.md` with the factors as they actually stood, adding its `## Boxes` line in the same turn. **Any determination the client issues, or any review or renewal date tied to it**, becomes a dated row in `## Due`.
