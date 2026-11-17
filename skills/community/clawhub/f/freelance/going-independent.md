# Going Independent — The Transition

Scope: the decision and the first 90 days. The question is never "am I good enough", it is "do I have a buffer, a first client, and a clean exit".

**Before advising**, read `## Practice`, `## Rates` and `## Due` in `~/Clawic/data/freelance/memory.md`, and `config.yaml` for `runway_months_target`, `target_income` and `tax_jurisdiction`. A transition plan written without the buffer number is a mood.

**Contents:** [The Go Test](#the-go-test) · [Runway Arithmetic](#runway-arithmetic) · [Leaving Cleanly](#leaving-cleanly) · [Order of Setup](#order-of-setup) · [The First 90 Days](#the-first-90-days) · [Part-Time First](#part-time-first) · [Going Back](#going-back)

## The Go Test

Five conditions. Three or fewer met means keep the job and freelance on the side (→ Part-Time First).

| Condition | Passing looks like | Why it is on the list |
|---|---|---|
| Buffer | `runway_months_target` × (personal + business monthly costs) in cash, tax set-aside excluded | Below three months, the next bad client is unrefusable (SKILL.md Rule 4) |
| First client | One signed or verbally committed engagement worth ≥1 month of costs, starting within 6 weeks | The hardest part of freelancing is the first sale, and it is much harder with no income |
| Rate floor | Derived (Rule 1) and validated against at least two real quotes or market data points | A floor nobody has tested against a buyer is a wish |
| Exit is clean | Notice period, non-compete, IP and moonlighting clauses read (→ Leaving Cleanly) | The employer clause is the single most common way a launch gets legally expensive |
| Health and admin | Insurance path known, tax registration path known, both costed into `business_costs_per_year` | These are non-negotiable expenses discovered too late by most first-year freelancers |

## Runway Arithmetic

`months = liquid cash ÷ (personal monthly costs + business monthly costs)`. Three corrections almost everybody skips:

- **The first invoice is not the first month's income.** Work in month 1, invoice at month end, `payment_terms_days` on top, plus the average slip: cash typically lands 6-10 weeks after starting. Add that gap to the runway requirement, do not average it away.
- **The tax set-aside is not runway.** Money owed to a tax authority sitting in the current account is an overdraft with a date on it (Rule 3).
- **Business costs start before revenue.** Insurance, accountant, tools, entity registration, hardware, and any platform membership. Sum them into `business_costs_per_year` before computing the floor, or every quote is under-priced by that amount.

Worked: personal 2,200/mo, business 700/mo, target buffer 6 months → 17,400 cash, plus a 2-month income gap already inside those 6. With one signed client covering month 2 onward, 4 months of buffer is defensible; with nothing signed, 6 is the floor.

## Leaving Cleanly

Read the employment contract before the resignation letter, not after. The clauses that matter, in order of how much damage they do:

| Clause | What to check | Typical outcome |
|---|---|---|
| IP assignment | Whether it covers work made outside hours and off equipment, and whether anything you plan to sell was built on their time | Anything built during employment on their kit is usually theirs; rebuild clean or get a written release |
| Non-compete | Duration, geography, and defined scope of "competing" | Enforceability varies enormously by jurisdiction — some make them void or ban them for most workers, others enforce a reasonable one. Get local advice before assuming either extreme |
| Non-solicit | Clients and colleagues, separately | Usually the enforceable one even where non-competes are not; it is also the one that hits a freelancer's first pipeline hardest |
| Moonlighting | Whether outside work needs written consent | Get consent in writing before the side work, not after the first invoice |
| Notice and garden leave | Length, and whether the notice period is paid | Paid notice is free runway; do not shorten it to be nice |
| Your employer as first client | Whether their procurement can even contract an individual, and the classification risk of doing the same job as a contractor | Common and often good — but it starts the practice at 100% concentration (Rule 5) and is the textbook misclassification pattern (`classification.md`) |

Do not announce the practice publicly before the notice conversation. Do line up the first client — approaching people you already know is not solicitation of the employer's clients, and the distinction is worth keeping crisp.

## Order of Setup

Everything here is cheap and fast except where noted; the order matters because each step unblocks the next.

1. **Decide the entity** — sole trader by default, incorporate on the trigger in `taxes.md`, and note that some clients' procurement will not contract an individual at all.
2. **Register for tax** in `tax_jurisdiction`, including VAT/GST if the threshold is close or registration is voluntary and advantageous (`taxes.md`).
3. **Separate the money** — a business account and a tax set-aside account, recorded in the shared `~/Clawic/data/finances/accounts.md`. Mixed personal and business money costs an accountant's hours every year and loses deductions.
4. **Contract template** ready before the first conversation, not during it (`contracts.md`).
5. **Insurance** — professional indemnity at minimum, because the first enterprise client will ask for a certificate and procurement will not wait (`insurance.md`).
6. **Invoicing and time tracking** chosen and tested with a 1-unit dry run.
7. **Proof, not a portfolio site** — three outcomes with numbers, publishable anywhere (`positioning.md`).
8. **Pipeline before the last day** — the channel list and the first fifteen conversations (`pipeline.md`).

## The First 90 Days

| Weeks | Priority | Failure mode it prevents |
|---|---|---|
| 1-2 | Deliver the first engagement flawlessly, and get the terms right rather than the price high | The first client becomes the first testimonial or the first dispute |
| 1-12 | Two selling hours every working day, without exception, even fully booked | The month-4 cliff: everyone's first crisis, caused by stopping selling while delivering |
| 3-4 | Ask the first client for a written testimonial and a named referral, at the moment of delivery | The moment of maximum goodwill is the delivery, not the invoice |
| 5-8 | Second client signed, whatever the size, to break 100% concentration | One client is not a practice (Rule 5) |
| 9-12 | Close month 3 in `income/<year>.md` and recompute billable hours and effective rate from real data | Year-one rates are almost always set on fictional utilization (Rule 2) |

From day one, write what most people reconstruct later, each into its own box: hours worked versus hours billed into the month row of `~/Clawic/data/freelance/income/<year>.md`, every quote and its outcome into `## Win/Loss` in `memory.md`, and where each lead came from into the `Source` column of `## Pipeline`. Three months of that data changes the rate more than any negotiation tactic.

## Part-Time First

The low-risk path, and the correct answer when the Go Test scores 3 or less.

- **Rate discipline is harder, not easier.** Side work priced as "extra money" sets the anchor for the full-time practice. Quote the derived floor from the start, even when the salary makes it unnecessary.
- **Capacity ceiling**: realistically 8-12 productive freelance hours a week alongside full-time employment. Beyond that, quality drops on both sides and the employer notices.
- **The switch trigger** is arithmetic: side income ≥ `target_income ÷ 12` for three consecutive months, or a client offering committed hours that the job blocks. Not enthusiasm.
- Check the moonlighting and IP clauses first (→ Leaving Cleanly). A side practice built on an employer's IP terms can be unsellable later.

## Going Back

Deciding to return to employment is a business decision, not a defeat, and it has a signature: three consecutive quarters below `target_income ÷ 4` with pipeline coverage under 2×, or a health cost the practice cannot fund. Wind down deliberately — finish or hand over engagements, keep the entity dormant rather than dissolving it if the jurisdiction makes reactivation cheap, and record why in `artifacts/` so the decision is not re-argued from feelings in two years.

**After a transition decision** — go, delay, part-time, or return — write it to `~/Clawic/data/freelance/artifacts/decision-<topic>.md` with the numbers it was based on and what was rejected, add its `## Boxes` line, and put the buffer target, first-client date and any notice-period date into `## Due` in `memory.md`.
