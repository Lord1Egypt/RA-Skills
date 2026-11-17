# The Paper — Terms Worth Insisting On, Clauses Worth Striking

Scope: what a freelance agreement must contain, what to strike from a client's template, who owns the work, and how AI assistance is declared. Drafting a full contract document clause by clause is `contract`; managing signed ones over time is `contracts` (the skill). Nothing here is legal advice for a specific jurisdiction — the escalation line is at the bottom.

**Before reviewing or drafting any agreement**, read `## Engagements` in `~/Clawic/data/freelance/memory.md` for the terms already in force with this client, `risk_posture.red_lines` in `config.yaml`, and `artifacts/msa-standard.md` if `## Boxes` names one. Re-negotiating a clause you already won last year is an own goal.

**Contents:** [The Minimum Viable Agreement](#the-minimum-viable-agreement) · [MSA Plus SOW](#msa-plus-sow) · [Red-Line List](#red-line-list) · [IP and Who Owns the Work](#ip-and-who-owns-the-work) · [NDAs](#ndas) · [Scope, Acceptance and Revisions](#scope-acceptance-and-revisions) · [Termination](#termination) · [AI Assistance Disclosure](#ai-assistance-disclosure) · [Data Protection](#data-protection) · [Signature and Order Mechanics](#signature-and-order-mechanics) · [When to Get a Lawyer](#when-to-get-a-lawyer)

## The Minimum Viable Agreement

Ten items. An engagement missing any of them has an unpriced risk in it; missing three or more, the dispute has already been designed (SKILL.md Rule 7).

| Item | Written as | What its absence costs |
|---|---|---|
| Parties | Legal entity names, not brand names | Suing or invoicing the wrong company |
| Scope | Deliverables, each with an acceptance criterion | "Not what we wanted", forever, for free |
| Out of scope | An explicit list of the nearby things not included | Every adjacent request is assumed included |
| Price and basis | Number, currency, `engagement_basis`, and what triggers extra | Silent rate erosion |
| Payment schedule | Deposit `deposit_pct`, milestones, `payment_terms_days`, late interest | Unpaid exposure with no lever (`getting-paid.md`) |
| Revisions | A count, and the price of further rounds | Infinite revision as a business model |
| Change control | Written change order, priced, before the work | Scope creep with no paper trail |
| IP and portfolio | Assignment on final payment, plus the portfolio carve-out | Nothing to show; sometimes nothing transferred |
| Termination | Notice by both sides, and payment for work done | Cancelled mid-project, unpaid |
| Liability cap | Capped at fees paid, exclusions for indirect loss | A 5,000 project carrying a 5,000,000 risk |

## MSA Plus SOW

For any client likely to give more than one project, split the paper:

- **MSA** — the legal frame, signed once: IP, confidentiality, liability, termination, governing law, insurance, dispute route.
- **SOW** — per engagement: deliverables, acceptance, dates, price, schedule. One page, signed by email if the MSA allows it.
- **Why**: the second project starts in days instead of weeks, and the negotiation that was already won is not reopened per project.
- **Precedence clause**: state which document wins on conflict. Without it, a purchase order's fine print silently overrides the MSA — and purchase orders almost always carry the client's standard terms on the back.

## Red-Line List

Ordered by expected cost, not by how alarming the wording is. This is the order to spend negotiating capital in.

| Clause | The problem | Ask for |
|---|---|---|
| Unlimited liability / broad indemnity | One clause can exceed the lifetime value of the client, and no insurance covers all of it | Cap at fees paid (or 1-2× fees), exclude indirect and consequential loss, indemnity limited to your own IP infringement and gross negligence |
| IP over everything you touch | Assigns your pre-existing tools, libraries and methods, so the next client's project infringes | Assign the deliverable only; licence your pre-existing and general-purpose materials, perpetual and non-exclusive |
| Termination for convenience, immediate, unpaid | The project ends at the client's convenience with work delivered and unpaid | Notice period, payment for work performed to termination, non-refundable deposit |
| Exclusivity / non-compete on your practice | Bans the rest of your book with no compensation | Delete, or accept a narrow one only inside a retainer that pays for it |
| Payment terms of 60-90 days, or pay-when-paid | Financing their operations from your cash | `payment_terms_days`, deposit, milestones, interest clause (`getting-paid.md`) |
| Acceptance at the client's sole discretion | Payment becomes optional | Objective acceptance criteria, plus deemed acceptance after N days of silence |
| Unlimited revisions or "until satisfied" | Unbounded work at a fixed price | A revision count and a price per further round |
| Non-solicit of the client's staff and clients | Often reasonable; over-broad versions block your whole sector | Limit to people you actually worked with, 12 months |
| Governing law and venue on the far side of the world | Recovery becomes economically impossible | Your jurisdiction, or a neutral one with an arbitration or mediation step |
| Assignment of the contract without consent | You end up working for a company you did not choose | Consent required, not unreasonably withheld |
| Their insurance requirement | Sometimes exceeds what a solo can buy at a sane price | Negotiate the limit to what is proportionate (`insurance.md`) |

**Negotiating stance**: pick the top three for the size of the deal and concede the rest gracefully. A freelancer who red-lines eleven clauses on a 4,000 project reads as expensive to work with; one who calmly caps liability and fixes IP reads as professional.

## IP and Who Owns the Work

The single most misunderstood area, and the one where the default surprises both sides.

- **No written assignment usually means no transfer.** In the US, "work made for hire" applies to employees, or to nine enumerated categories of commissioned work *with a signed written agreement*; ordinary freelance deliverables mostly fall outside it, so absent an assignment the freelancer retains copyright. Most other common-law and civil-law systems similarly require the transfer in writing. The client believing otherwise is not an assignment.
- **This cuts both ways.** A client who paid and got no assignment may have no right to modify or resell the work — which is a delivery failure, not a win. Put the assignment in.
- **Assignment on final payment**, not on delivery. Until the invoice clears, the licence is what they hold; it is the strongest non-litigious lever in existence (`disputes.md`).
- **Carve out your reusable materials**: frameworks, libraries, templates, snippets and methods created before or independently of the engagement. Grant a perpetual, non-exclusive licence to use them inside the deliverable, and keep ownership.
- **Third-party components**: name the licences in the deliverable. Shipping a copyleft library into a client's proprietary product without saying so is a real liability, and often an indemnity trigger you personally signed.
- **Moral rights** (attribution and integrity) cannot be assigned in several jurisdictions, and can only be waived in some. Where they exist and matter, say so rather than promising a total transfer you cannot deliver.
- **AI-generated content has a weaker copyright position**: purely machine-generated output has been held unprotectable in several jurisdictions, with protection depending on demonstrable human authorship. That matters when the contract promises to assign copyright in the deliverable — you cannot assign what does not exist. Keep human authorship real and documented, and never promise exclusivity over output you cannot control. The UK is the notable outlier, giving computer-generated works a statutory author (the person who made the arrangements for the creation), so the answer follows the governing law: name which law the assignment clause runs under before promising a full transfer.
- **Portfolio carve-out** goes in the same clause, at the tier agreed (`positioning.md`).

## NDAs

- **Mutual by default.** A one-way NDA where only you are bound is a signal about the whole relationship.
- **Bounded**: a definition of confidential information that excludes what is public, already known, or independently developed; a term of 2-5 years (indefinite for genuine trade secrets only); and a carve-out for legally compelled disclosure.
- **Refuse residual-knowledge bans.** A clause forbidding you from using general skill and experience gained is unworkable for a freelancer with clients in the same sector, and occasionally unenforceable — but you will still be arguing about it.
- **Never sign an NDA before hearing the pitch** unless the deal is real; an NDA to receive an unpaid brief is a way to make a decline expensive.
- Signing an NDA does not create the engagement. Scope and price come after.

## Scope, Acceptance and Revisions

- **Every deliverable gets an observable acceptance criterion.** "A responsive site" is a mood; "renders without horizontal scroll at 320px, Lighthouse performance ≥85 on the listed pages" is testable. This is the single highest-leverage sentence in a freelance contract.
- **Deemed acceptance**: silence for N working days (5-10 is normal) after delivery counts as acceptance. Without it, an unresponsive client freezes the final payment indefinitely.
- **Revision counts are counted per deliverable, in writing**, with a stated price for further rounds. "Two rounds of consolidated feedback" also solves the problem of five stakeholders sending contradictory comments separately.
- **Change orders are the mechanism, not a complaint.** A one-paragraph note — what changed, the price, the new date, their written yes — turns scope creep into revenue. Anything worth more than an hour goes through it. Handling the relationship around repeated creep is `clients`.

## Termination

- **Both sides**, with the same notice, typically 14-30 days on a project and 30-60 on a retainer.
- **Payment on termination**: everything performed to date, plus a non-refundable deposit, plus (for retainers) the notice period whether or not work is requested.
- **Kill fee** on fixed-price work cancelled before completion: a stated percentage of the remaining fee, commonly 25-50%. Its purpose is to price the hole left in a booked calendar, and it is much easier to agree at signature than at cancellation.
- **Handover obligations** belong in the clause too: what gets delivered on termination, in what format, and paid at what rate. "Cooperate with transition" without a rate is unpaid work.

## AI Assistance Disclosure

Follow `ai_disclosure` and the contract, in that order — a contractual term always wins over the default.

- **Contract-level**: the safest position is a short clause stating that AI tools may be used in production of the work, that all output is human-reviewed, that no client confidential data is submitted to third-party tools without consent, and that the freelancer remains fully responsible for the deliverable.
- **Regulatory**: the EU AI Act's transparency obligations for AI-generated or manipulated content apply from August 2026, with disclosure duties on deployers of certain systems and marking obligations for synthetic content; penalties scale with turnover. In the US there is no federal disclosure statute, but the FTC treats deceptive AI claims as consumer protection violations, and several states have their own rules. Confirm the current position for `tax_jurisdiction` and the client's location before advising, and note that the client's own sector rules may be stricter than either.
- **Confidentiality is the sharper risk than disclosure**: pasting a client's code, data or documents into a third-party tool can breach the NDA and data-protection law regardless of what any AI clause says. Get consent, or use tooling the client has approved.
- **Liability does not shift.** You are responsible for what you deliver; "the model wrote it" is not a defence, and a company has already been held to what its chatbot told a customer.
- **The fraud line** (SKILL.md Rule 9): assisted work reviewed by a human is a tool. A fabricated portfolio piece, a synthetic persona standing in for a person, an AI-written review, or promising human-only work while delivering unreviewed output is misrepresentation.

## Data Protection

- Handling personal data of the client's users makes you a **processor** in GDPR-style regimes: a written data-processing agreement is required, covering purpose, duration, security measures, sub-processors, deletion at the end, and breach notification.
- **Sub-processors include your tools** — hosting, analytics, transcription, AI services. Naming them is the part freelancers usually miss, and it is the part that gets audited.
- **International transfers** need a lawful basis (adequacy or standard contractual clauses) when data leaves the origin region.
- **Delete at the end of the engagement** and say you have. Keeping a client's production dump "in case" is an unfunded liability sitting on your laptop.
- Minimum hygiene regardless of regime: full-disk encryption, a password manager, MFA on everything client-related, and no client data in personal accounts.

## Signature and Order Mechanics

- **Electronic signature is valid** for ordinary commercial contracts in the major regimes (eIDAS in the EU, ESIGN/UETA in the US, and equivalents elsewhere); a typed name in an email accepting stated terms is often enough to form a contract. A few document types are excluded, which is a reason to check rather than to print.
- **A purchase order is not the contract** — it usually incorporates the client's standard terms by reference. Read what the PO references, and make the precedence clause point at your paper.
- **Start of work is itself acceptance** in many systems: beginning work on a verbal instruction can create a contract on whatever terms are provable, which are usually theirs. Either get the signature or send a written confirmation of terms and start only after they say yes in writing.
- **A tool acting in your name binds you.** Electronic-transaction law (ESIGN/UETA in the US and equivalents elsewhere) treats an automated agent operating inside the authority you gave it as capable of forming a contract, so "the assistant sent it" is not a defence. Nothing is accepted, signed or committed by an automated flow, and anything drafted on your behalf is read before it goes (SKILL.md Rule 9).
- **Store the executed version** where you can find it in a dispute; record the key terms in `## Engagements` so no contract has to be reopened to answer "what were the terms".

## When to Get a Lawyer

The escalation table. Everything above is a practitioner's checklist; these are the situations where a few hundred spent on advice is the cheap option.

| Signal | Why |
|---|---|
| Contract value above roughly a quarter of annual income | The downside is now practice-ending |
| Uncapped liability or indemnity the client will not cap | The one clause that can exceed everything you own |
| Foreign governing law or a jurisdiction you cannot practically litigate in | Rights you cannot enforce are not rights (`international.md`) |
| Regulated sector work: health, finance, children, safety-critical | Sector rules override general contract practice |
| Exclusivity, equity, revenue share, or an employment-shaped clause | Mixed employment/commercial law, and equity paperwork is its own field |
| An ex-employer's non-compete or IP clause is in play | Jurisdiction-specific, fact-specific, and expensive to get wrong (`going-independent.md`) |
| An actual dispute with a letter from their lawyer | Stop drafting replies; get advice before responding (`disputes.md`) |

**After any negotiation**, write to `## Engagements` in `~/Clawic/data/freelance/memory.md`: the terms actually agreed — basis, rate, deposit, `payment_terms_days`, notice, revision count, liability cap, portfolio-rights tier. **When a clause set is accepted**, save it to `~/Clawic/data/freelance/artifacts/msa-standard.md` (or `redlines-<client>.md` for a client-specific negotiation), with every secret and identifier replaced by its pointer, and add its `## Boxes` line in the same turn — deriving these clauses costs a negotiation, and nobody should pay it twice. **Any renewal or notice window** goes into `## Due` as a dated row.
