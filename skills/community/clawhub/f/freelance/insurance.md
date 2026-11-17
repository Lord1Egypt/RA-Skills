# Insurance — Cover a Solo Practice Actually Needs

Scope: which policies matter, what each one pays for, how to read a client's insurance clause, and how to keep a claim payable. Costing premiums into the rate is `rates.md`; funding holiday, sick days and pension is `cashflow.md` and `capacity.md`.

**Before advising**, read `## Insurance` and `## Due` in `~/Clawic/data/freelance/memory.md` (what is held, at what limit, when it renews), `## Engagements` for any contractual cover requirement already agreed, and `tax_jurisdiction`, `business_entity` and `business_costs_per_year` in `config.yaml`. Advice given without the current policy list recommends what is already bought.

**Contents:** [The Cover Map](#the-cover-map) · [Claims-Made Is the Distinction That Matters](#claims-made-is-the-distinction-that-matters) · [Sizing the Limit](#sizing-the-limit) · [Reading a Client's Insurance Clause](#reading-a-clients-insurance-clause) · [The Certificate Drill](#the-certificate-drill) · [What Is Never Covered](#what-is-never-covered) · [Income Protection](#income-protection) · [Buying and Renewing](#buying-and-renewing) · [Notifying a Claim or a Circumstance](#notifying-a-claim-or-a-circumstance) · [Buying Order on a Small Budget](#buying-order-on-a-small-budget)

## The Cover Map

| Cover | Pays for | Buy it when |
|---|---|---|
| Professional indemnity (errors and omissions) | Defence costs and damages when your work or advice causes the client financial loss — the freelancer's core policy and the one contracts name | Before the first client contract, and always before advisory or specification work |
| Public liability (general liability) | Injury to a third party, or damage to their property | Any on-site work, client premises, events, or visitors to your workspace |
| Cyber | Breach response, notification, forensics, extortion, and third-party claims | You hold client personal data, credentials or production access — the same fact pattern that makes you a processor (`contracts.md`) |
| Employers' liability | Injury to people working under your control; legally compulsory in some jurisdictions from the first person | You take on anyone, including a "self-employed" helper — status is decided by the facts, not by their invoice (`classification.md`) |
| Equipment and portable kit | Laptop, camera, tools, away from home and in transit | Home contents policies routinely exclude business use and business equipment; check the wording before assuming cover exists |
| Legal expenses / tax investigation | Solicitor and accountant fees for a dispute or an audit | Cheap, and one enquiry usually repays several years of premium |
| Income protection | A monthly benefit after a deferred period when you cannot work | Dependents, a mortgage, or a practice that cannot survive a quiet quarter (→ Income Protection) |
| Life or critical illness | A lump sum against dependents or debt | Only where someone depends on the income; it is a personal-finance decision, not a practice one (`money`) |
| Product liability | Harm caused by a physical product supplied | Goods, hardware, anything shipped |
| Anything else a contract names | — | Ask which loss the clause is meant to answer, then price it. An exotic requirement is negotiable far more often than the freelancer assumes (→ Reading a Client's Insurance Clause) |

## Claims-Made Is the Distinction That Matters

Professional indemnity is almost always **claims-made**: it covers claims *made* while the policy is live, not work done while it was live. Three consequences nobody explains at the point of sale:

- **A gap erases the past.** Cancel in March and a claim arriving in April about work from two years ago is uninsured, however faithfully the premiums were paid at the time.
- **The retroactive date is the real start of cover.** It has to sit at or before your earliest chargeable work; switching insurer without carrying that date back silently deletes years of history, which is why the cheaper renewal quote is sometimes not cover at all.
- **Run-off is the exit.** A run-off policy bought when you stop practising keeps claims-made cover alive for past work, usually for a term matched to the limitation period for claims under the governing law (six years in England, jurisdiction-specific elsewhere). Price it before deciding to close a practice or return to employment (`going-independent.md`).

Public liability is generally occurrence-based — the incident date decides, so it can be dropped without a tail. Knowing which of the two a policy is tells you whether cancelling it is free or expensive.

## Sizing the Limit

- **The limit answers the client's plausible loss, not the invoice.** A 4,000 engagement inside a payments flow can break something worth a hundred times that; a 40,000 rebrand rarely destroys anything but time.
- **Match the contractual liability cap to the policy limit.** Capped at fees paid with a policy above it is coherent; an uncapped indemnity is uninsured by definition beyond the limit, which is why capping it is the first red line (`contracts.md`).
- **Per-claim versus aggregate.** An aggregate limit is the total for the whole policy year and two claims share it. A client's clause almost always means per-claim — check which one your certificate states before answering their form.
- **Defence costs inside or outside the limit** is the largest quality difference between two policies at the same premium: inside means legal fees eat the money meant for the damages.
- Cheapest honest calibration: the highest limit any current contract demands, rounded up one step. Procurement rarely accepts less than it asked for, and buying twice in a year costs more than buying once.

## Reading a Client's Insurance Clause

| Requirement | What it means | Move |
|---|---|---|
| A limit far above the contract value | An enterprise supplier template applied unmodified | Ask for a limit proportionate to the work and offer the certificate you hold; most procurement functions have a documented exception path |
| "Additional insured" | Their entity added to your policy | Common in the US, often chargeable, sometimes unavailable on a small policy — confirm with the insurer before agreeing to it |
| Waiver of subrogation | Your insurer gives up its right to recover from them | Usually granted on request, but agreeing without telling the insurer can prejudice the policy |
| Maintain cover for N years after completion | A run-off obligation with a real cost after the work ends | Price the tail into the fee, or negotiate the term down |
| Certificate before the PO is raised | An onboarding gate, not a formality | Buy the policy before signing; onboarding is 1-3 weeks and the invoice clock does not start until it clears (`getting-paid.md`) |
| Cover that cannot exist for a solo — employers' liability with no staff, huge product liability for a service | A copied template | Say so plainly and offer the nearest real equivalent; an inapplicable line is the easiest one for them to strike |

Never state a limit you do not hold. Certificates are checked, and a false statement on a supplier form is a contractual problem and sometimes a criminal one.

## The Certificate Drill

The request always arrives on a deadline, so keep it to minutes. The insurer's portal issues the certificate; the fields anyone checks are policy type, limit, period of cover and named insured — and the named insured must match the legal entity on the contract exactly, which is where freelancers trading through a company get caught (`taxes.md`). Keep the certificate's location, insurer, limit and renewal date in `## Insurance`, because an expired certificate stops a payment run as effectively as it stops cover.

## What Is Never Covered

- **Liabilities you assumed by contract** beyond what the law would have imposed. A broad indemnity clause is typically excluded — the clause you signed is not the clause the insurer underwrote.
- **Deliberate acts, fraud, and circumstances already known** and not disclosed at inception or renewal.
- **Unpaid invoices.** No policy pays for a client who will not pay (`disputes.md`).
- **Work outside the declared activity or territory.** Activities, turnover and the countries you work in are underwriting facts: adding a new discipline, or a first US client, without telling the insurer is the quiet way a claim gets declined. **How the work is produced is part of that declaration** — some wordings now carry AI exclusions or conditions, so AI-assisted delivery is disclosed to the insurer as well as to the client (SKILL.md Rule 9, `contracts.md`).
- **Fines and penalties**, including regulatory ones in most wordings. Cyber policies differ specifically on whether data-protection fines are insurable where local law allows it — this is a wording to read, not to assume.

## Income Protection

- **The benefit is capped**, commonly at 50-70% of net earnings, and it is underwritten on *provable* income: a practice that just incorporated or just started is assessed on a low figure, whatever it currently earns.
- **The deferred period is the price lever.** Set it to what the sick-day fund plus the buffer actually covers (`cashflow.md`) rather than to the shortest option offered; each step longer cuts the premium materially.
- **Own-occupation versus any-occupation** decides whether the policy ever pays. Own-occupation pays when you cannot do *your* work; any-occupation pays only when you cannot do any work at all, and it is the definition behind most declined claims.
- **Guaranteed versus reviewable premiums**: reviewable is cheaper now and repriced later, usually at the age when switching has become hard.
- State sickness support for the self-employed ranges from a real allowance to nothing, and eligibility usually depends on contributions made long before the illness (`taxes.md`).

## Buying and Renewing

- **A broker normally costs nothing extra** and earns its place on professional indemnity, where wordings differ far more than premiums do.
- **Declare accurately**: activities, turnover, largest single contract value, territories worked in, and whether you subcontract. Under-declaring turnover to save a small premium is the cheapest way to lose a large claim.
- **Never lapse.** Continuous cover is what protects past work; a two-week gap between insurers is a multi-year hole (→ Claims-Made).
- **Premiums are a business cost.** Add them into `business_costs_per_year`, which makes the rate floor stale the day a policy is bought or repriced (SKILL.md Rule 1, `rates.md`).
- **Renewal is a repricing moment, not a direct debit.** Re-shop every 2-3 years while carrying the retroactive date across, and re-check the limit against the largest contract signed since the last renewal.

## Notifying a Claim or a Circumstance

- **The duty is to notify circumstances, not only claims.** A complaint, a threatened claim, an angry message about a defect: report it as soon as it is known. Late notification is the most common reason a valid claim is refused.
- **Do not admit liability** or agree in writing to a fix that concedes negligence before the insurer says so — most policies make that a breach of condition. Responding factually and commercially is fine; conceding fault is not (`disputes.md`).
- **Assemble the same pack a payment dispute needs**: contract, scope, acceptance criteria, approvals, delivery evidence, and the chronology.
- A notification changes a clause far more often than it changes the craft — the lesson belongs in the template (`contracts.md`), not only in the memory of it.

## Buying Order on a Small Budget

Buy in expected-loss order, not alphabetically: professional indemnity first, because it is both what clients demand and what ends practices; then whichever of public liability or cyber matches how the work is actually done — on-site, or handling client data; then equipment; then income protection the moment anyone depends on the income. A practice with no client demanding cover, no on-site presence and no client data can defensibly run bare for its first months — but the exposure is said out loud and put in `## Due` with a review date, never left as a default nobody chose.

**After any insurance event** — a policy bought, renewed, repriced, or a client requirement learned — write the row in `## Insurance` in `~/Clawic/data/freelance/memory.md`: cover, insurer, limit, premium with its currency, renewal date, and which contract requires it. **The renewal date and any run-off or review obligation** become rows in `## Due`. **A contractual cover requirement** also goes into that engagement's row in `## Engagements`, because it outlives the negotiation and nobody re-reads the MSA. **The premium total** updates `business_costs_per_year` in `config.yaml` and the floor is recomputed in the same turn (`rates.md`). Policy numbers and broker references are identifiers and may be stored; insurer portal logins are credentials and are stored only as `<kind>:<locator>` pointers.
