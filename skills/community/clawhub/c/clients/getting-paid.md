# Getting Paid

Scope: everything between "the work is done" and "the money is in the account" — terms, deposits, the chase, stop-work, and the client who will not pay. Setting the price is `pricing.md`; creating and numbering the invoice document is the `invoice` skill.

Read `## Receivables` in `~/Clawic/data/clients/memory.md` (or `receivables.md` once split out) at the start of any money conversation, and check `## Due` for the invoicing day and the receivables sweep.

**Contents:** [Design Out the Problem First](#design-out-the-problem-first) · [Invoice Hygiene](#invoice-hygiene) · [The Ladder, in Detail](#the-ladder-in-detail) · [Stop-Work](#stop-work) · [Late-Payment Interest and Costs](#late-payment-interest-and-costs) · [Collections and Small Claims](#collections-and-small-claims) · [Cash-Flow Instruments](#cash-flow-instruments) · [DSO](#dso)

## Design Out the Problem First

Most non-payment is prevented before the invoice exists:

- **Deposit before the calendar slot** (`deposit_pct`, SKILL.md Rule 2). It is the cheapest test of whether the buyer can actually buy, and it removes the worst case entirely: full delivery, zero payment.
- **Split anything longer than a month** into deposit, milestones and balance. Never one payment on completion — that puts the whole engagement on your balance sheet and hands the client all the leverage at the end.
- **Shorter terms for smaller clients.** Net 30 is the commercial default; net 7 or 14 is normal and accepted for small suppliers, and the shorter number is worth more than a higher rate on slow terms.
- **Invoice the moment the milestone is met**, not at month end. Days of delay at your end are added to their days, and payment cycles are calendar-driven — an invoice that misses their run date waits a full cycle.
- **PO number before starting, in enterprises.** No PO, no payable invoice, and they will not raise one retroactively (`onboarding.md`).
- **Final deliverable on final payment** where the work permits. Files, access, or the production deploy transfer when the balance clears; state it in the proposal so it is a known term, not a hostage-taking.

## Invoice Hygiene

Rejections are almost always administrative, and each one costs a full payment cycle:

- Correct legal entity name and billing address, exactly as they gave it.
- PO number, project code and cost centre where required, in the field they require.
- Sent to accounts payable, with the client contact copied. An invoice sent only to your contact sits in a personal inbox during their holiday.
- One deliverable per line, matching the proposal's wording — a line item the buyer cannot map to what they approved gets queried, and a queried invoice is a paused invoice.
- Due date written as a date, not as "net 30". People pay dates.
- Payment methods, including bank details for the currency being invoiced. For cross-border work, state who bears transfer and conversion costs — it was agreed in the proposal (`pricing.md`).
- Sequential numbering with no gaps, and a copy retained. Tax authorities in most jurisdictions require both.

## The Ladder, in Detail

The rungs and their dates are in SKILL.md's Payment Ladder table, which is canonical. What each rung is actually for:

- **Due date.** Assume it was lost, not refused. A friendly one-line resend costs nothing and clears a meaningful share of late invoices, because most are genuinely mislaid.
- **+3.** Ask whether it was *received and entered into the system* — a process question, easy to answer, and it flushes out the missing PO or the wrong entity name without accusing anyone.
- **+7.** Second notice, referencing the payment term in the agreement and naming the date interest begins. Neutral tone, new subject line so it is not buried in the old thread.
- **+14.** Phone. This is the rung that moves money, because email is asynchronous and easy to defer. Ask one question: "when will it be paid?" Get a date, then email a one-line confirmation of the date they gave. The call moves it; the email makes it a commitment.
- **+21.** Stop-work notice, below.
- **+45.** Formal demand, then collections or small claims.

Two rules that make the ladder work at all: **run it on the calendar regardless of how you feel about the client**, and **record every rung in `## Receivables`**. A chase that only happened in the user's head is why an invoice reaches day 60 with no escalation history — and the escalation history is what makes the later steps credible.

## Stop-Work

The most effective single instrument, and the most under-used.

- **Send it in writing, factually, with a date**: "Work on the project will pause from Monday 3 August until invoice 0042 is settled. I'll pick straight back up the day it clears."
- **Address the client contact and copy their manager.** Nothing about it is threatening; it is a supplier managing exposure, and the internal escalation is the point — your contact often cannot pay you but can make someone else prioritise it.
- **Check the contract first.** A suspension right is standard, and knowing whether yours is written changes the wording, not the decision.
- **Actually stop.** A stop-work notice you do not honour is worse than none: it proves the ladder has no final rung, and every future rung is discounted.
- **Do not delete, disable or take anything hostage** beyond pausing your own labour. Deleting work, revoking a live client's access, or disabling a running system is a different act with legal consequences, and it converts a collections problem into a liability.
- Say what resumption looks like. The message should read as a pause with a clear ending, not as a threat.

## Late-Payment Interest and Costs

Statutory anchors worth knowing, because naming them changes the tone of a chase from a request into an entitlement:

- **EU**: the Late Payment Directive (2011/7/EU) gives business creditors statutory interest at the ECB reference rate plus at least eight percentage points, plus a fixed recovery sum of at least 40 EUR per invoice, and caps agreed payment terms for most B2B transactions at 60 days. It applies whether or not the contract mentions it. Member-state implementations vary in detail — verify the local rate before quoting a figure.
- **UK**: the Late Payment of Commercial Debts (Interest) Act 1998 gives Bank of England base rate plus 8%, plus fixed compensation of £40, £70 or £100 depending on the size of the debt, plus reasonable recovery costs.
- **US**: no general statutory right for private contracts — interest comes from your contract terms, so a late-payment clause is worth having. The Prompt Payment Act covers federal contracts only.
- **Contractual late fees** (commonly 1.5% per month in US practice) are only enforceable if they are in the signed agreement, and only up to local usury limits.

Charging the interest is optional and often waived for a good client; **naming it in the +7 notice is not**. It signals that the ladder has rungs and that the invoice is an obligation with a cost attached.

## Collections and Small Claims

When the ladder is exhausted:

1. **Formal demand letter** — the debt, the invoice, the dates, the interest accrued, and a deadline (commonly 7-14 days) before further action. Sent by a trackable method.
2. **Cost-benefit before escalating.** Below roughly one day of your rate, the recovery is rarely worth the hours; write it off deliberately, record the write-off in the client's `contact-log/<client-slug>.md` and its `Health` cell in `## Roster`, and change the terms that allowed it rather than pursuing it.
3. **Small claims / equivalent** is designed to be used without a lawyer, has a monetary ceiling that varies by jurisdiction, and requires exactly what your records already contain: a signed scope, the invoice, the delivery evidence, and the chase history. This is the concrete payoff of writing down every rung.
4. **Collections agencies** typically take a substantial percentage of what they recover, and the relationship is over the moment you instruct one. Suitable for genuinely bad debt, not for a slow payer worth keeping.
5. **Never** threaten anything you are not prepared to do, never discuss the debt publicly or with their other suppliers, and never let the tone become personal — it damages your position if it ever reaches a decision-maker or a judge.

Then close the loop internally: record the bad debt in the client's `contact-log/<client-slug>.md` and its `Health` cell in `## Roster`, and add the pattern to `## Declined Leads` so the same shape of client is caught earlier (`pipeline.md`).

## Cash-Flow Instruments

- **Escrow** for first engagements with an unknown client, on platforms or via a third party. It costs a percentage and removes the worst outcome entirely.
- **Card or direct-debit on file** for retainers, charged on `invoicing_day`. It converts a monthly chase into a monthly notification, and it is the single biggest reduction in collections effort available to a small supplier.
- **Milestone billing** over milestone-free projects, always. Each milestone that is paid is exposure retired.
- **Early-payment discount** (a small percentage for payment within a few days) works with some organisations and is ignored by most; it is worth offering, never worth relying on.
- **Invoice factoring** converts receivables into cash at a discount. Rarely right for a solo operator — it prices your collections problem rather than fixing it.

## DSO

Days sales outstanding = **(accounts receivable ÷ revenue over the period) × days in the period**.

Worked example: 12,000 EUR outstanding, 60,000 EUR invoiced over 90 days → (12,000 ÷ 60,000) × 90 = 18 days. Against net-30 terms that is healthy; the number to watch is the trend and its relationship to your terms. DSO drifting toward and past your stated terms means the ladder is not being run, not that clients changed.

Compute it at the quarterly portfolio review from `revenue/<year>.md` and `## Receivables` (`portfolio.md`).

**Write before you move on:** every invoice sent gets a row in `## Receivables` in `memory.md` (or `receivables.md` once split out) with amount, currency, issue date and due date; every chase rung updates the `Last chase` cell the same day; a paid invoice has its receivables row **deleted** and a line appended to `~/Clawic/data/clients/revenue/<year>.md`; a stop-work notice, a write-off or a bad debt goes into the client's `Health` cell in `## Roster` and their `contact-log/<client-slug>.md`; a demand letter or chase sequence that worked goes to `artifacts/script-late-payment.md` with its `## Boxes` line; the invoicing day and the weekly receivables sweep live in `## Due`.
