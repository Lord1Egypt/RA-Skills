# Disputes — Non-Payment, Bad Faith, and Walking Away

Scope: what to do when the escalation ladder in `getting-paid.md` has run out — refusal to pay, a manufactured quality complaint, a chargeback, a client who disappears, or an engagement that has to be terminated. The relationship-repair conversation is `clients`.

**Before acting**, read `## Engagements` (terms, deposit, notice, acceptance criteria) and `## Pain Points` in `~/Clawic/data/freelance/memory.md`, plus the executed contract and `artifacts/` for anything about this client. A dispute is won on the paper that already exists, not on the argument.

**Contents:** [Triage in Five Minutes](#triage-in-five-minutes) · [The Evidence Pack](#the-evidence-pack) · [Leverage That Still Exists](#leverage-that-still-exists) · [Recovery Routes by Amount](#recovery-routes-by-amount) · [Quality Disputes](#quality-disputes) · [Chargebacks](#chargebacks) · [The Ghosting Client](#the-ghosting-client) · [Terminating an Engagement](#terminating-an-engagement) · [Writing It Off](#writing-it-off) · [Preventing the Next One](#preventing-the-next-one)

## Triage in Five Minutes

Name the type before choosing a move; the moves are different and mixing them loses both.

| Type | Signal | First move |
|---|---|---|
| Cashflow, not refusal | Apologetic, gives dates, previously paid | Payment plan in writing with dates and interest waived only on adherence |
| Process failure | Missing PO, wrong entity, invoice never entered | Fix the invoice, resubmit, restart the clock (`getting-paid.md`) |
| Manufactured quality complaint | Complaint appears only after the invoice, contradicts prior approvals | Acceptance criteria and the approval trail (→ Quality Disputes) |
| Deliberate non-payment | Silence, moved goalposts, new complaints each round | Stop work, formal demand, choose a route by amount |
| Insolvency | Other suppliers unpaid, filings, staff departures | Speed matters; a claim filed early ranks better than a polite one filed late |
| Fraud | Fake company, stolen identity, redirected bank details, overpayment refund request | Stop all work, report to the platform and the bank, do not negotiate |

## The Evidence Pack

Assemble before writing anything formal. Thirty minutes here decides every route below.

- The **signed contract or the exchange that formed it** — including an email accepting terms, which in most systems is a contract.
- The **scope and acceptance criteria**, plus every change order.
- **Approvals**: each message where the client accepted a deliverable or asked for the next stage. Approval of milestone 2 destroys a complaint about milestone 1.
- **Delivery evidence**: dates, files sent, deployments, access granted.
- **The invoice and the full chase trail**, with dates.
- **Their admissions**: "we'll pay next week", "the work is fine, the budget is frozen". These are worth more than any argument you could construct.
- Everything in one folder, chronological, and a copy of that folder outside any system the client controls — platform, their repository, their drive. **The one-page timeline on top is the artifact**: write it to `~/Clawic/data/freelance/artifacts/dispute-<client>.md` — what happened on what date, which piece of evidence proves each line, and where each piece is stored — and add its `## Boxes` line in the same turn. Amounts and dates belong in it; account numbers and their confidential material do not.

Note what is missing too. A dispute with no acceptance criteria and no signature is a lesson, not a case, and the honest advice is usually to settle cheaply and fix the paper (`contracts.md`).

## Leverage That Still Exists

Ordered by effectiveness. Use them in order; do not fire the last one first.

1. **Unpaid work is unassigned work.** Where the contract assigns IP on final payment, the client's licence to use the deliverable has not begun. Stating this factually, once, resolves a large share of disputes — because their exposure is now bigger than the invoice.
2. **Access and credentials** you legitimately hold as the author. Never sabotage, never delete, never disable something already live: that converts your strong position into a counterclaim, and in some jurisdictions into a criminal matter.
3. **Work in progress and final files** not yet delivered.
4. **Statutory interest and recovery costs**, quoted with the statute (`getting-paid.md`).
5. **Their timeline.** A client with a launch date has more to lose than you do; a client who has already shipped has none.
6. **Reputation routes** — platform reviews, public statement, industry networks. Slow, weak, mostly irreversible, and legally risky if anything said is inaccurate. Truthful factual statements are generally defensible; characterizations invite a defamation counterclaim. Treat as last resort.

## Recovery Routes by Amount

Choose by expected net recovery, not by anger. `expected = amount × probability of collection − cost − your hours × rate`.

| Amount | Route | Cost and speed |
|---|---|---|
| Under ~1 day of billings | Write off after the formal demand | Chasing costs more than the debt (→ Writing It Off) |
| Small, on a platform | Platform dispute / escrow arbitration | Free, weeks, decided on the platform's own record (`platforms.md`) |
| Small to medium | Small claims court | Low fixed fee, designed for self-representation, typically weeks to months; per-claim limits vary by jurisdiction |
| Medium | Mediation, where the contract requires it or both sides prefer speed | Shared cost, days to weeks, preserves the relationship |
| Medium, debtor solvent but unwilling | Collections agency | 10-30% of what they recover, no win no fee usually, and the relationship is over |
| Medium to large | Solicitor's letter before action, then civil claim | Hundreds for the letter, thousands for the claim; the letter alone resolves many cases |
| Any, freelancer-protection jurisdiction | Statutory claim under the local freelance law | Can carry double damages and fee-shifting — check first, it may be the cheapest route (`getting-paid.md`) |
| Client insolvent | File as a creditor immediately | Usually recovers little; speed and correct filing are all you control |
| Cross-border | Depends entirely on the governing-law clause | Often uneconomic — which is why that clause is a red line (`international.md`, `contracts.md`) |

Two constants: a **letter before action** stating amount, basis, deadline and next step resolves a surprising share of disputes at almost no cost; and **every route is cheaper the earlier it starts**.

## Quality Disputes

The complaint that appears only after the invoice.

- **Separate the genuine from the tactical** by timing and specificity: a real quality problem is raised during the work and is describable; a tactical one arrives with the invoice and is a feeling.
- **Answer with the acceptance criteria**, not with a defence of the craft. Either the deliverable meets the written criterion or it does not, and this is precisely what the criterion is for (`contracts.md`).
- **Offer the contracted remedy** — the remaining revision rounds — with a deadline and consolidated feedback. Never open-ended rework; that is how a dispute becomes an unpaid second project.
- **Partial settlement is often correct**: a discount against immediate payment, in writing, marked as full and final settlement of the invoice. Getting 80% today usually beats 100% in five months.
- If the work genuinely fell short, say so, fix it fast, and keep the relationship. Being wrong is cheaper than being right slowly.

## Chargebacks

Card payments can be reversed months later, and the process favours the cardholder.

- Respond within the processor's window with the evidence pack; missing the deadline forfeits automatically.
- Strongest evidence: signed contract, written approvals, delivery timestamps, and any message where the client acknowledged receipt of the work.
- Expect a per-dispute fee whether or not you win, and a rising dispute rate to threaten the payment account itself.
- Prevention: clear descriptor on the statement, invoice numbers that match, written acceptance at delivery, and bank transfer rather than card for large invoices (`getting-paid.md`).

## The Ghosting Client

Silence mid-project, with work delivered and money outstanding.

1. **Stop work immediately**, in writing, per the contract. Continuing to deliver into silence grows the exposure and weakens the position.
2. **Two contacts, two channels, spaced a week apart**, each with a specific question and a date.
3. **Written notice that the engagement will be treated as terminated** on a stated date, with everything performed becoming payable and the deposit retained.
4. **Invoice for work done to that date**, then run the ladder from the top.
5. **Release the calendar slot** rather than holding it: a ghosting client's return date is not a forecast (`pipeline.md`).
6. Document the sequence in `## Pain Points` — a client who ghosted once will be recognized when the enquiry returns in eight months, which it often does.

## Terminating an Engagement

Ending a live engagement deliberately, on your side.

- **Grounds worth using**: non-payment past the contracted trigger, scope changes refused through change control, abuse of you or anyone working with you, illegality, or a classification exposure the client will not fix (`classification.md`).
- **Follow the contract's notice clause exactly.** Terminating outside its terms turns your claim into their counterclaim.
- **Write it short and neutral**: the clause relied on, the effective date, what will be delivered, what is payable, and how handover works. No grievances, no history — the letter may be read by a judge or an arbitrator.
- **Deliver the handover you owe** and invoice it if the contract allows. Professional exits are how a bad engagement fails to become a bad reputation.
- **Settle before ending where possible**: a mutual termination with a payment figure agreed in writing is worth more than a righteous unilateral one.

## Writing It Off

A decision, made on numbers, not a surrender.

- Write off when `amount × collection probability < cost of recovery + your hours × rate`. A day of chasing at your rate is a real cost and belongs in the calculation.
- **Book it**: an uncollectable debt may be deductible depending on entity, accounting basis and jurisdiction — a cash-basis freelancer who never recognized the income usually cannot deduct it again (`taxes.md`, and the bookkeeping treatment is `accountant`).
- **Close the loop internally**: record the amount, the client and the cause in `## Pain Points`, and mark the contact so a future enquiry is priced with a 100% deposit or declined.
- **Extract the rule.** Almost every write-off traces to a missing deposit, a missing acceptance criterion, an unsigned start, or a red flag that was visible and overruled. Change the template, not just the mood.

## Preventing the Next One

The controls, in the order they would have prevented the last dispute: deposit cleared before work → acceptance criteria per deliverable → milestone payments keeping exposure under two weeks → IP assigned on payment → stop-work trigger in the contract → red-flag triage at qualification → the whole record kept in one place from day one.

**After any dispute**, in the same turn: record the outcome, the amount recovered, and the cause in `## Pain Points`; update the engagement row in `## Engagements` with the end date and status; mark the client in the shared `~/Clawic/data/contacts/contacts.md` with the context (never a slur — factual: "40% of invoice written off 2026-05, no acceptance criteria in contract"); and if a template changed as a result, update `artifacts/msa-standard.md` and say which clause was added.
