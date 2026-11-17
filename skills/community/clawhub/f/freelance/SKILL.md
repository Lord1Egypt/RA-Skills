---
name: Freelance
slug: freelance
version: 1.0.2
description: 'Runs an independent freelance or contractor practice as a business: rate floor, pipeline, cash buffer, taxes, and the paper. Use when going freelance or weighing quitting a job for it, when setting or raising an hourly or day rate, when the pipeline is empty and work dried up, when income swings and a buffer or tax set-aside has to be sized, when one client is too much of the revenue, when a client asks for free spec work, rewrites your contract, or sends an NDA you should not sign, when payment is late, disputed, or a project has to be walked away from, when self-employment tax, VAT registration, invoicing abroad, or IR35 and worker-classification tests come up, when insurance, sick days, holiday, or a pension has to be self-funded, and when the next step is subcontracting, productizing, or an agency. Not for managing one client relationship (`clients`), Upwork (`upwork`) or Fiverr (`fiverr`) tactics, drafting the contract document (`contract`), or issuing invoices (`invoice`).'
homepage: https://clawic.com/skills/freelance
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 💻
    os:
    - linux
    - darwin
    - win32
    displayName: Freelance
    configPaths:
    - ~/Clawic/data/freelance/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/data/finances/
    - ~/Clawic/profile.yaml
    - ~/freelance/
    - ~/clawic/freelance/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/freelance/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/data/finances/
      - ~/Clawic/profile.yaml
      - ~/freelance/
      - ~/clawic/freelance/
---

**Data.** At the start of every session, read `~/Clawic/data/freelance/config.yaml` (what the user declared) and `~/Clawic/data/freelance/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read `~/Clawic/data/contacts/contacts.md` before naming or writing to any client, prospect, referrer or subcontractor. If none of it exists, work from defaults and say nothing about it. If data sits at an old location (`~/freelance/` or `~/clawic/freelance/`), move it to `~/Clawic/data/freelance/`, and say in one line that you moved it and from where.

**Write before the session ends** whenever it produced something durable: a rate set or raised; a quote sent, won or lost, with the reason; an engagement started, renewed, repriced or ended; a month's billings, collections and billable hours; a payment term, deposit or notice period agreed; a tax, VAT or insurance date; a client, referrer or subcontractor met; a contract clause that was accepted or refused; a decision about niche, entity or channel; or something the user will re-read — a rate card, a proposal template, an MSA, a case study, an outreach message that got replies. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**People go to the shared contact book `~/Clawic/data/contacts/contacts.md`, engagements to `~/Clawic/data/projects/<project>.md`, and business accounts and tool subscriptions to `~/Clawic/data/finances/`** — not here. This box keeps the commercial terms nobody else owns (rate, basis, committed hours, payment terms, notice, portfolio rights) and points at those records by name. Duplicating a client into two boxes is how two skills start contradicting each other.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. A pasted contract, invoice or portal export is dense with them. Store the pointer and strip the value: `1password:Work/Stripe/live`, `env:WISE_TOKEN`, `keychain:upwork`, `file:~/Documents/tax/utr.txt`.

Freelancing fails on arithmetic far more often than on craft: a rate set from what feels askable, a year with 1,200 billable hours priced as if it had 2,080, one client at 70% of revenue, and tax spent before it was owed. Give the number and the formula behind it, name the exposure in weeks of unpaid work, and say what the downside case looks like — the practice has no employer absorbing it. Work from defaults immediately: never open with questions about their rate, their country, or how proactive to be. The one exception to silence is `tax_jurisdiction` — while it is unset, say which country's rules you are applying before giving tax, classification or late-payment guidance. That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale, country) → the Configuration table default.

## When To Use

- Deciding to go independent, or running the practice: rate, pipeline, capacity, cash buffer, benefits, time off
- Money mechanics of self-employment: tax set-aside, quarterly or annual filings, VAT/GST registration, entity choice, deductions, retirement
- The paper: what to insist on before starting, what to strike from a client's template, IP and portfolio rights, AI-assistance disclosure, insurance a client demands
- Getting paid: deposits, milestones, terms, late payment, non-payment, disputes, and cross-border invoicing and currency
- Status and compliance: employee-versus-contractor tests, IR35, umbrella companies, an ex-employer's non-compete, moonlighting
- Growth decisions: raising rates, productizing, retainers, subcontracting, turning solo work into an agency
- Mode: **advise** by default. **Act-as** only when drafting on the user's behalf — a quote, a chase message, a clause, an outreach note — and never sending, signing or committing to a number the user has not seen
- Not for running one client relationship day to day (`clients`), Upwork or Fiverr platform tactics (`upwork`, `fiverr`), drafting the contract document itself (`contract`), issuing invoices (`invoice`), or pricing a product rather than your labour (`pricing`)

## Quick Reference

| Situation | Play | Depth |
|-----------|------|-------|
| "Should I quit my job and go freelance?" | Runway months and the first-client test before the resignation, not after | `going-independent.md` |
| "What should I charge?" | Rate floor from take-home target, costs, tax and real billable hours (Rule 1) | `rates.md` |
| Fixed-price quote, unknown scope | Three-point estimate × contingency, priced against the floor, capped by a change-order clause | `rates.md` |
| Win rate feels too high, or nobody says no | Raise until the loss rate bites: 20% up survives losing 17% of wins (Rule 6) | `rates.md` |
| No work coming in | Channel mix and coverage ratio first, discounting last | `pipeline.md` |
| Choosing or leaving a marketplace | Take rate plus lead cost as an all-in commission; the exit clause decides if it is a channel or a cage | `platforms.md` |
| "What do I even sell, to whom?" | Niche by problem and buyer, not by tool; proof beats positioning copy | `positioning.md` |
| Client sent their contract or an NDA | Red-line list in order of cost: IP, indemnity, termination, exclusivity, payment | `contracts.md` |
| Who owns the work; can it go in the portfolio | Written assignment on payment, plus a named portfolio carve-out — no assignment, no transfer | `contracts.md` |
| Client demands proof of insurance | Which cover, what limit, and what it actually pays for | `insurance.md` |
| Invoice overdue, or client gone quiet on money | Escalation ladder with statutory interest and a stop-work trigger | `getting-paid.md` |
| Refusal to pay, chargeback, or a bad-faith dispute | Evidence pack, leverage that still exists, and the recovery route by amount | `disputes.md` |
| Income lumpy; can't tell what is affordable | Buffer, tax set-aside and salary-to-self, in that order (Rules 3-4) | `cashflow.md` |
| One client is most of the revenue | Concentration cap and the de-risking sequence (Rule 5) | `cashflow.md` |
| Tax, entity, VAT, deductions, retirement | Set-aside on receipt; entity decided by profit level and liability, not by vibes | `taxes.md` |
| "Am I actually self-employed here?" | Control, substitution and financial-risk tests; IR35, ABC, umbrella | `classification.md` |
| Foreign client, foreign currency, withholding | Source rules, reverse charge, treaty forms, and the rail that keeps the FX spread | `international.md` |
| Overbooked, burnt out, or need time off | Utilization target, capacity ceiling, funded holiday and sick days | `capacity.md` |
| Income is capped by hours | The four levers, each with its break-even | `scaling.md` |
| First subcontractor, or white-label work | Margin, liability chain and who owns the client | `scaling.md` |
| Norms and rates of a specific trade | Deliverable conventions, revision norms and the trap that trade keeps hitting | `trades.md` |
| Anything else freelance | Answer directly, then state the effect on rate floor, weeks of unpaid exposure, or client concentration | — |

Coverage map: `going-independent.md` the transition · `positioning.md` niche and proof · `pipeline.md` finding work · `platforms.md` marketplaces · `rates.md` pricing your labour · `contracts.md` the paper · `insurance.md` cover · `getting-paid.md` terms and collection · `disputes.md` non-payment and conflict · `cashflow.md` buffer, tax set-aside, concentration · `taxes.md` self-employment tax and entity · `classification.md` contractor status · `international.md` cross-border work · `capacity.md` utilization and time off · `scaling.md` beyond hours-for-money · `trades.md` per-trade norms.

## Core Rules

1. **Rate floor is derived, never guessed.** `pre-tax profit needed = take_home_target ÷ (1 − tax_setaside_pct)`; `billings needed = pre-tax profit + business_costs`; `floor = billings ÷ billable_hours_per_year`. Worked: 60,000 take-home, 30% set-aside, 12,000 costs, 1,200 billable hours → 60,000 ÷ 0.70 = 85,714; + 12,000 = 97,714; ÷ 1,200 = **81/hour**. Quote below the floor and the work is a donation with extra steps. Currency comes from `currency`; the floor is recomputed whenever a term in it changes (`rates.md`).
2. **Billable hours are not working hours.** A full-time year is ~1,840 worked hours (46 weeks × 40); sold hours land at **1,100-1,400** for an established solo, lower in year one, because selling, admin, invoicing, learning and gaps are unpaid. `billable_hours_per_year` defaults to 1,200 and is replaced by the user's own trailing figure once `income/<year>.md` holds three months (`capacity.md`).
3. **Tax moves on the day money clears, not on the day it is due.** Transfer `tax_setaside_pct` of every received payment to a separate account the same day. A set-aside kept in the working account is spent by definition — the deadline arrives after the money is gone (`taxes.md`).
4. **Buffer before growth.** Target `runway_months_target × (personal monthly costs + business monthly costs)` in cash, and count the tax set-aside as somebody else's money, never as runway. Below three months of buffer, the practice takes bad clients, because it has to (`cashflow.md`).
5. **No client above `client_concentration_cap_pct` of trailing-12-month revenue.** Compute it monthly from `income/<year>.md`. Crossing 40% means the pipeline restarts now, at 60% the relationship is an unwritten employment with none of the protections, and above 70% their budget freeze is your redundancy (`cashflow.md`, `classification.md`).
6. **Raise the rate until losses appear.** A rate rise of factor `k` leaves revenue intact while the win rate holds above `old_win_rate ÷ k`: +20% survives a drop from 60% to 50% wins, +50% survives 60% → 40%. Winning nearly everything is the diagnostic — 8 of the last 10 quotes accepted means the number is under market. Raise on new quotes first, existing clients on renewal with notice (`rates.md`; the conversation with an existing client is `clients`).
7. **Paper before work, always in this order:** scope with acceptance criteria and a revision count → price and payment schedule → signed agreement or a cleared deposit → first hour of work. Unsigned work is unenforceable goodwill; several jurisdictions now also make the written contract itself the freelancer's statutory remedy (`contracts.md`, `getting-paid.md`).
8. **Keep unpaid exposure under two weeks of billings.** Exposure = value delivered since the last cleared payment. Fix it with deposit (`deposit_pct`, minimum 30% and 50% for an unvetted client), milestone invoicing, and `payment_terms_days` short enough that a slip is visible before the next milestone starts. Stop-work is a clause, not a threat improvised mid-project (`getting-paid.md`).
9. **Disclose AI assistance per `ai_disclosure`, and never let it touch identity.** Assisted drafting reviewed by a human is a tool; a fabricated portfolio piece, an AI-written review, or a persona standing in for a person is fraud and ends the account and sometimes the career. The EU AI Act's transparency duties on AI-generated content apply from August 2026; US exposure runs through FTC deception rules and state law, not a federal disclosure statute (`contracts.md`).

## Practice Health Numbers

The six numbers that describe a freelance practice. Compute from `income/<year>.md` and `## Engagements`; anything red gets named in the answer, not saved for a quarterly review.

| Number | Formula | Healthy | Red |
|---|---|---|---|
| Effective rate | collected ÷ **all** hours worked, billable or not | ≥70% of the quoted rate | <50% — the unbilled half is the business, and it is unpriced |
| Utilization | billable hours ÷ available hours | 50-65% solo (agencies run 70-80% because someone else sells) | >75% sustained = no selling is happening; the cliff is one project away |
| Client concentration | largest client ÷ trailing-12-month revenue | <40% | >60% (Rule 5) |
| Runway | cash ÷ monthly personal + business costs, excluding tax set-aside | ≥`runway_months_target` | <3 months |
| DSO | average days from invoice issued to cash cleared | ≤`payment_terms_days` + 7 | >45 days, or any invoice past 60 |
| Pipeline coverage | value of live opportunities ÷ revenue target for the period | 3-4× | <2× — start selling before the current project ends, not after |

## Income Levers

Four ways past an hours-for-money ceiling, in ascending order of how much has to change. Each break-even is the test; the detail and the failure modes are in `scaling.md`.

| Lever | Break-even test | Cost of pulling it |
|---|---|---|
| Raise the rate | Rule 6: holds while win rate stays above `old ÷ k` | Cheapest lever; nothing else changes |
| Sell fewer, larger engagements | Fixed sales cost per engagement drops; retainer at ≥3 months beats the same revenue in one-offs | Concentration climbs — recheck Rule 5 |
| Productize | A repeatable scope beats bespoke once the same deliverable has been quoted ~5 times and delivery variance is under ~20% | Discovery gets replaced by marketing; different skill entirely |
| Subcontract | Profitable when `(client rate − sub rate) × sub hours > your hours spent managing × your rate` — a 30-40% gross margin is the usual floor for it to be worth the risk | You now carry their errors, their invoices, and the client's expectations |

## Client Red Flags

Observable signals, before the contract. Any two together means a deposit at 50% or a decline; the ones marked **stop** are declines on their own.

| Signal | What it predicts | Action |
|---|---|---|
| "Free test task" beyond ~1 hour of work | Unpaid delivery, often to several candidates at once | Paid discovery or paid pilot, capped and scoped |
| "Exposure", equity-only, or "we'll pay from revenue" | **stop** — no funding, or no intention | Decline; keep the reply short and reusable |
| Won't sign anything, "we can keep this simple" | No enforceable scope; the dispute has already been designed | No paper, no work (Rule 7) |
| Pushes to move off-platform before contract | Escrow and dispute rights disappear with it | Refuse until a contract and deposit exist outside (`platforms.md`) |
| Budget arrives only after the proposal is written | Free consulting as a procurement method | Ask for the range before scoping; no range, no proposal |
| Deadline set before scope is discussed | The overrun is already yours | Price the deadline as risk, or decline |
| Rewrites your invoice terms unilaterally, or "our system pays in 90 days" | Financing their operations from your account | Terms in the contract, deposit, and interest clause (`getting-paid.md`) |
| Talks about hours, tools, and being online 9-5 | **stop** on the classification side — this is employment | `classification.md` before quoting |
| Prior freelancer left mid-project, nobody says why | Non-payment or scope chaos, repeating | Ask directly; verify with the predecessor if reachable |
| Requests your credentials, or asks you to invoice a third party | Fraud pattern | Never; escalate to platform or decline (`disputes.md`) |

## Output Gates

Before sending a quote, accepting an engagement, or advising on a number:

- Is the price at or above the derived rate floor, in the user's `currency`, with the assumed billable hours stated (Rule 1)?
- For fixed price: is contingency in the number, and is a change-order clause in the scope (`rates.md`)?
- Does the engagement name a deposit, a payment schedule, terms in days, and what stops if payment stops (Rule 8)?
- Does taking this work push any Practice Health number red — concentration, utilization, DSO?
- Has status been checked when the work is on-site, exclusive, managed, or long-running (`classification.md`)?
- Is every deliverable defined by an acceptance criterion and a revision count, rather than by a satisfaction adjective?
- Did anything durable come out of this — a rate, a quote outcome, an engagement term, a month's numbers, a date, a person, a reusable document? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/freelance/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| trade | text | none | Selects the section of `trades.md` used for deliverable norms, revision conventions and rate benchmarks |
| currency | text (ISO code) | from `profile.yaml`, else USD | Currency of every rate, quote, buffer and threshold; written into every stored amount |
| target_income | number (currency/year, take-home) | none | Numerator of the rate floor (Rule 1); while unset, the floor is shown as a formula with the user's own number left blank |
| billable_hours_per_year | number (600-1800) | 1200 | Denominator of the rate floor and of every utilization calculation (Rule 2) |
| business_costs_per_year | number (currency/year) | 0 | Added to billings needed in Rule 1: tools, insurance, accountant, hardware, platform fees |
| engagement_basis | hourly \| daily \| fixed \| retainer \| value | hourly | Unit every quote, rate card and estimate is expressed in, and which section of `rates.md` leads |
| payment_terms_days | number (0-60) | 14 | Terms written into quotes and contracts, the DSO target, and when the escalation ladder starts (`getting-paid.md`) |
| deposit_pct | number (0-100) | 30 | Deposit demanded before work starts; Rule 8 raises it to 50 for an unvetted client |
| tax_jurisdiction | text (country, plus state/region) | none | Which tax, classification, VAT and late-payment regime applies; while unset, name the assumed jurisdiction before answering |
| business_entity | sole-trader \| llc \| s-corp \| ltd \| umbrella \| other | sole-trader | Whether guidance covers payroll, distributions, corporation tax and filings, or personal self-employment only (`taxes.md`) |
| tax_setaside_pct | number (15-45) | 30 | Share of every cleared payment moved to the tax account (Rule 3) and the rate-floor gross-up (Rule 1) |
| runway_months_target | number (1-24) | 6 | Buffer target in Rule 4 and the go/no-go line in `going-independent.md` |
| client_concentration_cap_pct | number (10-100) | 40 | Threshold that triggers the de-risking sequence in Rule 5 |
| ai_disclosure | proactive \| on-request \| contractual | proactive | Whether an AI-assistance line ships with deliverables by default, only when asked, or exactly as the contract defines |
| rate_card_file | path | none | Long-form rate card or service menu at `~/Clawic/data/freelance/artifacts/<file>`; overrides the ad-hoc price list |
| tone_file | path | none | Voice guide at `~/Clawic/data/freelance/artifacts/<file>`; governs proposals, outreach and chase messages |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — invoicing, time tracking, contract e-sign, accounting, proposal tooling, where the portfolio lives — affects which artifacts get produced and in what format
- **Conventions** — quote and proposal structure, deliverable naming and handover format, revision counts, how a change order is issued — affects `contracts.md` and every generated document
- **Platform and locale** — jurisdiction, working language, time zones they will take calls in, holiday calendar — affects `international.md`, `taxes.md`, availability advice
- **Risk posture** — will they start without a signature, minimum deposit, standing red lines (unlimited liability, all-IP-including-tools, exclusivity), whether to chase or write off — affects `contracts.md` and the escalation ladder
- **Work order and review gates** — whether discovery (paid or not) has to happen before any number is quoted, whether the paper is settled before or after the price conversation, and whether every proposal, chase message and clause is shown to the user before it is sent — affects the sequence in `pipeline.md`, `rates.md` and `contracts.md`, and every act-as draft
- **Chosen channels** — which marketplaces, agencies, job boards, communities or referral partners are actually in use — affects `pipeline.md` and `platforms.md`
- **Exclusions** — industries or clients they refuse, no-spec-work rule, an ex-employer's non-compete or IP clause still in force, subcontracting allowed or not — affects lead triage and `classification.md`
- **Output register** — proposal voice, whether prices are itemized or single-line, how much reasoning to show a client — governed by `tone_file`
- **Cadence** — pipeline review, invoice run, rate review, tax dates, insurance renewal, bookkeeping — every accepted cadence becomes a row in the `## Due` table of `memory.md`

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Pricing from the ex-salary hourly | Salary hours were paid whether or not they were sold, and had employer tax, holiday, sick pay and pension inside them | Derive the floor (Rule 1); it usually lands 2-3× the salary hourly and that is arithmetic, not greed |
| Quoting hours for a fixed-price job | The client buys the estimate as a cap and every discovery is your loss | Fixed price with contingency and a change-order clause, or hourly with an estimate range (`rates.md`) |
| Discounting to win a slow month | The rate is now anchored for the whole relationship, and the slow month recurs on schedule | Keep the rate, cut scope, or spend the week selling (`pipeline.md`) |
| Spending gross income | Tax, holiday, sick days and equipment are all inside that number | Set aside on receipt (Rule 3); pay yourself a fixed monthly figure (`cashflow.md`) |
| One big client and no pipeline | Their reorg is your unemployment, with no notice and no severance | Cap at 40% and keep selling during the good months (Rule 5) |
| Signing the client's MSA unread because it is "standard" | Standard templates are drafted for their side: unlimited indemnity, all-IP-including-pre-existing-tools, unilateral termination, no cap | Red-line list in cost order (`contracts.md`) |
| Assuming the client owns the work automatically | Outside employment, US work-made-for-hire covers only nine enumerated categories with a signed writing; without assignment the freelancer still owns it — which also means nothing was delivered | Written assignment on final payment, plus a portfolio carve-out |
| Starting work on a verbal yes | Nothing to enforce, and in several jurisdictions the missing contract is itself the violation | Deposit cleared or signature received first (Rule 7) |
| Treating an overdue invoice as a relationship problem | Days age silently and the ladder gets started once recovery is already hard | Fixed ladder on fixed days, statutory interest applied, stop-work at the contracted point (`getting-paid.md`) |
| Full-time on-site for one client for a year | Classification risk, both directions, plus a practice with no other clients | Test it early (`classification.md`); keep a second client alive |
| No holiday, then a forced two-week gap | Unfunded time off becomes an income hole and then a health event | Price the holiday into the rate; fund it as a sinking line (`capacity.md`) |
| Taking the marketplace rate as the market rate | Marketplace floors are set by global supply and the take rate, not by the value delivered | Compare against direct-client rates for the same trade before concluding a rate is unwinnable (`platforms.md`) |
| Waiting for the portfolio to be ready | Proof is a case study of work already done, not a redesign of the site | Publish three outcomes with numbers and start selling (`positioning.md`) |
| Hiring a subcontractor to fix an overbooking | Managing costs hours nobody billed, and quality problems arrive as your problem | Margin test in Income Levers first; raise the rate before adding people (`scaling.md`) |

## Where Experts Disagree

- **Hourly versus value pricing.** Hourly caps upside and rewards slowness; value pricing needs a quantified business outcome and a buyer who will discuss it. The frontier is measurability: revenue or cost effects the client already tracks → value; craft work with no attributable number → day rate with a scoped deliverable. Fixed price without contingency loses under both schools.
- **Niching down.** Specialists command a premium and shorten the sales cycle; generalists survive a sector collapsing. Frontier: how many buyers exist in the niche — under a few hundred reachable buyers, the niche is a hobby, and diversification is not indecision (`positioning.md`).
- **Marketplaces as a channel.** Some practices treat Upwork or Fiverr as a permanent acquisition channel with a known commission; others as a one-year bootstrap to be exited. Decide on all-in commission plus the exit clause, not on prestige (`platforms.md`).
- **Incorporating early.** Liability protection and tax efficiency are real, but so are filing costs, payroll and accountancy. The usual trigger is a profit level where the tax saving exceeds the compliance cost, plus any client that will not contract with an individual — jurisdiction-specific, so it is `tax_jurisdiction`'s answer, not a universal one (`taxes.md`).
- **Chasing versus writing off.** Some write off anything under a few hundred and protect the reputation; others pursue every debt because the ones who do get paid first. Boundary: cost of recovery against amount, and whether the client is a repeat name in the market (`disputes.md`).

## Security & Privacy

**Credentials:** this skill never asks for, stores, logs or transmits banking, platform, tax-portal or payment-processor credentials. Contracts, invoices and portal exports pasted in are scrubbed to `<kind>:<locator>` pointers before anything is written.

**Local storage:** rates, engagements, income history, pipeline and generated documents stay in `~/Clawic/data/freelance/` on this machine, plus people in the shared `~/Clawic/data/contacts/`, engagements in `~/Clawic/data/projects/` and account references in `~/Clawic/data/finances/`. Names, terms and amounts only — no account numbers, tax identifiers or client confidential material.

**Guardrails:** nothing is sent, signed, filed or committed on the user's behalf. Drafts of quotes, chase messages and clauses are presented for review; the user sends them.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/freelance (install if the user confirms):
- `clients` — running an individual client relationship: onboarding, scope creep, the difficult conversation
- `contract` — drafting the agreement document itself, clause by clause
- `invoice` — issuing invoices, numbering, tax lines and payment tracking
- `upwork` — Upwork-specific profile, proposals and scoring
- `pricing` — pricing a product or a packaged offer rather than your own labour

## Feedback

- If useful, star it: https://clawic.com/skills/freelance
- Latest version: https://clawic.com/skills/freelance

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/freelance.
