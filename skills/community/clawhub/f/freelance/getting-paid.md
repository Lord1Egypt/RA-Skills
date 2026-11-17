# Getting Paid — Terms, Collection, and the Ladder

Scope: the payment system — deposits, milestones, terms, rails, and the escalation that turns an overdue invoice into cash. A refusal to pay or a bad-faith dispute is `disputes.md`; issuing the invoice document is `invoice`; the relationship conversation around a late client is `clients`.

**Before advising on a payment problem**, read `## Engagements` in `~/Clawic/data/freelance/memory.md` for the agreed terms and deposit, and the DSO column of `income/<year>.md`. The contracted terms decide which rung of the ladder is available.

**Contents:** [Terms That Get Paid](#terms-that-get-paid) · [Exposure Math](#exposure-math) · [Deposits and Milestones](#deposits-and-milestones) · [Invoice Hygiene](#invoice-hygiene) · [The Escalation Ladder](#the-escalation-ladder) · [Statutory Late Payment](#statutory-late-payment) · [Freelancer Protection Laws](#freelancer-protection-laws) · [Payment Rails](#payment-rails) · [Procurement and Enterprise Clients](#procurement-and-enterprise-clients) · [Retainers and Subscriptions](#retainers-and-subscriptions)

## Terms That Get Paid

| Term | Default | Why |
|---|---|---|
| Deposit | `deposit_pct`, 50% for an unvetted client | Filters non-buyers, funds the start, and is the only money guaranteed to arrive |
| Payment terms | `payment_terms_days`, 14 by default | Terms are a discount you are giving; 30 days is a norm, not a law of nature. Ask for 14 and settle at 30 |
| Late interest | Statutory rate where one exists, else 1.5%/month | Its job is to be quotable in the second chase, not to earn interest |
| Stop-work trigger | Work pauses at overdue + 7 days, stated in the contract | The only lever that works while the project is still wanted |
| Final payment | Before final files, credentials, or deployment | Assignment on payment (`contracts.md`) makes this contractual, not petty |
| Currency and who pays fees | Stated explicitly | Otherwise the transfer arrives short and the difference is silently yours (`international.md`) |

## Exposure Math

`exposure = value of work delivered since the last cleared payment`. Keep it under **two weeks of billings** (SKILL.md Rule 8).

Worked: a 14,000 fixed-price project at 620/day equals about 23 days of work. Undivided, exposure peaks at 14,000 — nine weeks of billings on one client's goodwill. With 40% deposit and three milestones, peak exposure is roughly 2,800: one week. Same client, same contract value, one third of the risk, decided by the payment schedule alone.

For hourly and retainer work the equivalent is **invoice frequency**: weekly or fortnightly invoicing on a new client, monthly only after they have paid twice on time.

## Deposits and Milestones

- **No deposit, no start.** The exception is an established client with a clean payment history, and even then only for work under a week.
- **A deposit is non-refundable** and the contract says so; otherwise it is a loan you extended.
- **Milestones follow the work decomposition**, not the calendar: deliverable-linked payments cannot be argued down by "we haven't seen anything yet". Three to five milestones is the sweet spot; more creates admin, fewer creates exposure.
- **Never let the final payment be the largest.** A 40/30/30 split leaves 30% at risk at the moment leverage is lowest; 50/30/20 is better for a new client.
- **Time-and-materials with a cap** invoices on a fixed cycle regardless of milestones — the cap is what the client is protecting, the cycle is what protects you.

## Invoice Hygiene

Half of "late" invoices were never payable. Before chasing anything, check the invoice itself:

- Correct legal entity, correct billing contact, and the **PO number if their system requires one** — the most common silent rejection in enterprise accounts payable.
- Due date as a **date**, not "net 30". Ambiguity buys them a fortnight.
- The deliverable described in their language, matching the SOW line items, so the approver recognizes what they signed.
- Tax treatment correct: VAT/GST line, reverse-charge note, or exemption reference (`taxes.md`, `international.md`).
- Payment details complete, with a reference the client's system will echo back.
- **Sent to accounts payable, not only to your contact**, and on the day the milestone completed — an invoice sent a week late arrives in the next payment run, which can cost a month.

## The Escalation Ladder

Fixed days, fixed steps, no improvisation. Warm through step 3, formal from step 4. Each step is a separate message, and every one of them is short.

| Day | Step | Content |
|---|---|---|
| Due − 3 | Reminder | One line, friendly, invoice attached again. Catches the "it was never approved" case while it is still cheap |
| Due + 1 | Notice | States it is now overdue, restates the due date, asks for a payment date |
| Due + 7 | Chase to a second channel | Contact plus accounts payable, phone if email is silent. Ask a question that requires an answer: "which payment run is it in?" |
| Due + 7 | **Stop work** | Per the contract, in writing, calmly, with what resumes on payment. Deliverables and access are withheld under the payment-conditional licence (`contracts.md`) |
| Due + 14 | Formal demand | Letter naming the contract clause, the amount, accrued statutory interest and recovery costs, and a deadline of 7 days |
| Due + 21-30 | Final notice before action | States the next step precisely: platform dispute, mediation, small claims, collections, or a solicitor's letter. Only name a step you will take |
| Due + 30 | Act | `disputes.md` decides which route by amount and jurisdiction |

Rules that make the ladder work: never skip a rung, never send an angry message, never accept a promise without a date, and never restart the clock because they replied. Every step goes in writing even when it happened by phone — a one-line "confirming our call" email is the evidence.

## Statutory Late Payment

Where it exists, it is free leverage: quoting the statute converts a chase from a favour into a legal position.

| Regime | Entitlement | Notes |
|---|---|---|
| EU (Late Payment Directive 2011/7/EU, as implemented locally) | Statutory interest at the ECB reference rate + at least 8 percentage points, plus a minimum fixed recovery sum (€40 or local equivalent), plus reasonable recovery costs | Default terms are 30 days; longer than 60 requires express agreement and must not be grossly unfair. National implementations vary — check the local act |
| UK (Late Payment of Commercial Debts (Interest) Act 1998) | Bank of England base rate + 8%, plus fixed compensation of £40/£70/£100 by debt size, plus reasonable recovery costs | Applies to B2B by default, even if the contract is silent |
| US | No general federal statute for private B2B; contractual interest governs, and state prompt-pay laws apply mainly to construction and public contracts | Freelancer-specific statutes are the stronger route (→ next section) |
| Elsewhere | Varies widely | Check the local regime before quoting a number; state the assumption when `tax_jurisdiction` is unset |

Charging interest is a decision, not an obligation: mentioning the entitlement in the formal demand is usually worth more than the money it produces.

## Freelancer Protection Laws

A growing set of jurisdictions gives independent workers statutory rights that override a weak contract. Where one applies, it is the strongest and cheapest lever available.

- **New York City (Freelance Isn't Free Act, 2017) and New York State (2024)**: written contract required above a threshold value, payment within the contracted date or 30 days of completion, protection against retaliation, and double damages plus attorney's fees on a successful claim.
- **Illinois (Freelance Worker Protection Act, effective 1 July 2024)** and **Minnesota**, with similar structures; more states and cities have followed or proposed versions.
- **EU Platform Work Directive** and national self-employment statutes affect platform-mediated work specifically; the Late Payment Directive covers the rest.
- Practical consequence: **the written contract is often itself the statutory obligation**, and its absence is the client's violation rather than your oversight. Check whether one applies in the client's location before assuming a small debt is uncollectable.

Verify the current text and thresholds for the specific location — these statutes are new and changing.

## Payment Rails

Choose per invoice by size and route; the fee difference on a single large invoice can exceed a day's billings.

| Rail | Typical cost | Speed | Use when |
|---|---|---|---|
| Domestic bank transfer | Near zero | 0-2 days | Default for domestic invoices |
| SEPA (euro area) | Near zero | 1 day | Default inside the euro area |
| International wire (SWIFT) | Fixed fee each side, plus intermediary deductions, plus the bank's FX spread | 1-5 days | Large invoices where the fixed fee is small in percentage terms — always specify who pays charges (`OUR` vs `SHA`) |
| FX-specialist transfer services | Low percentage fee near the interbank rate | 0-2 days | The usual best value for cross-border invoices (`international.md`) |
| Card / payment links | ~1.5-3.5% plus fixed fee, more cross-border | Instant | Small invoices, or when speed is worth the fee; check chargeback exposure (`disputes.md`) |
| PayPal and similar wallets | Percentage fee plus a currency-conversion spread that stacks on top | Instant | Only when the client insists; the conversion spread is the expensive part |
| Marketplace escrow | The platform's take rate | Per release | Platform contracts, where it also buys dispute protection (`platforms.md`) |

Rules: **never absorb the transfer cost silently** — state who pays fees in the contract. **Never accept overpayment followed by a request to refund the difference**; that is the classic overpayment scam. And never give a client bank details in an editable document — invoice-redirection fraud works by changing them in transit, which is why the details should also be confirmable by a channel the client already trusts.

## Procurement and Enterprise Clients

Large clients do not pay late out of malice; they pay late because a step was skipped. The sequence, done before the first invoice:

1. **Vendor onboarding** — supplier form, tax form, bank verification, sometimes an insurance certificate (`insurance.md`). Allow 1-3 weeks.
2. **Purchase order issued** before work starts. In most enterprise systems an invoice without a valid PO cannot be paid at all, regardless of who approves it.
3. **Know the payment run schedule** — weekly, fortnightly or monthly. An invoice submitted the day after a run waits a full cycle, which makes the submission date worth more than the chase.
4. **Get the AP contact and the portal login** at onboarding, not during the chase.
5. **Their standard terms will be 45-90 days.** Negotiate at contract stage where possible; where it is not, price the financing cost in and shorten the milestone cycle instead.

## Retainers and Subscriptions

- **Invoice in advance**, at the start of the period. A retainer billed in arrears is just hourly work with a bigger exposure.
- **Automatic renewal with a notice window**, and the notice date recorded in `## Due` — an unnoticed renewal or an unnoticed cancellation are equally expensive.
- **Define what happens to unused capacity** (expires or rolls one month) and what a pause means (`rates.md`).
- **Price increases on a retainer** need contractual notice, usually 30-60 days; the conversation is `clients`.

**After any payment event**, write it in the same turn: the DSO and collected figures into `income/<year>.md` when the month closes; a term, deposit or notice change into its row in `## Engagements`; a chase that worked or failed, and any procurement quirk (portal, PO rule, payment-run day) into `## Pain Points` — it is the knowledge that stops the next invoice to that client being late for the same reason. **A recurring invoice run, a retainer renewal or a notice window** becomes a row in `## Due`.
