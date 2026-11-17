# Proposals and Statements of Work

Scope: turning a qualified lead into a document they can sign. What to charge is `pricing.md`; qualification is `pipeline.md`; the legal language of the agreement itself is the `contract` skill.

Read the lead's row in `## Pipeline`, any `artifacts/proposal-*.md` from a similar engagement, and `rate_card_file` if it is set, before writing a line.

**Contents:** [What a Proposal Is For](#what-a-proposal-is-for) · [The Shape](#the-shape) · [Deliverables Are Nouns](#deliverables-are-nouns) · [The Exclusions Section](#the-exclusions-section) · [Three Options, Not One Price](#three-options-not-one-price) · [Terms That Belong in Every Proposal](#terms-that-belong-in-every-proposal) · [Sending and Closing](#sending-and-closing) · [Paid Discovery](#paid-discovery)

## What a Proposal Is For

Not persuasion — the decision to work with you was made on the discovery call. A proposal exists to make the yes easy to defend internally, and to fix the boundary of the work before anybody is emotionally committed to it. Judge every paragraph against those two jobs; a page about your philosophy serves neither.

Corollary: the proposal is the last cheap moment to say no. Anything you are uneasy about becomes ten times more expensive to raise after the deposit clears.

## The Shape

One to three pages, in this order, because it is the order a buyer reads in:

1. **The problem, in their words.** Quote them from the call. If they do not recognise their own situation in the first paragraph, nothing after it lands.
2. **The outcome.** What is true when this is done, stated as an observable state, not an activity.
3. **Deliverables.** The nouns they receive (below).
4. **Exclusions.** What is explicitly not included (below).
5. **Approach and timeline.** Phases with dates, and what you need from them by when — the client's obligations are half of every timeline that slips.
6. **Price and terms.** The number, the deposit, the payment schedule, `payment_terms_days`, what triggers a change order.
7. **Next step.** One action, one date. "Sign here by the 14th and we start the 21st."

Bio, credentials and case studies go at the end or in a link. They are reassurance, not argument.

## Deliverables Are Nouns

The single highest-leverage edit in the whole document. Activities are unbounded; artefacts are countable.

| Vague (an activity) | Bounded (an artefact) |
|---|---|
| "SEO optimisation" | "One technical audit document, up to 20 prioritised fixes, implemented on up to 15 templates" |
| "Ongoing support" | "Up to 10 hours per month, weekdays, responded to within one business day" |
| "Brand strategy" | "Positioning statement, messaging matrix for three audiences, one 60-minute presentation" |
| "Website redesign" | "Six unique page designs, desktop and mobile, two revision rounds each, plus a component sheet" |

Every deliverable carries a quantity and a revision count. "Two rounds of revisions, a third is a change order" prevents more disputes than any other sentence in the document — and it only works if the rounds are defined as consolidated feedback, not as individual comments arriving over three weeks.

## The Exclusions Section

Longer than feels comfortable, and it is the section clients read most carefully. It protects them too: the exclusion is where they discover they needed something, while there is still time to buy it.

Standard candidates: content and copy, photography and licensing, third-party subscriptions and their costs, hosting, translation, accessibility remediation beyond the stated standard, training, post-launch support, work on systems you cannot access, anything requiring a stakeholder who has not been named, and rush work outside agreed hours.

Each exclusion gets a price or a "quoted separately". An exclusion with no route to buying it reads as a refusal; an exclusion with a price reads as a menu.

## Three Options, Not One Price

A single number invites a yes/no decision, which turns into a negotiation about the number. Three options change the question to "which one", and they let the buyer self-select on budget without either side losing face.

| Option | What it is | Why it exists |
|---|---|---|
| Reduced | The core deliverable only, at a real price — never a token discount | Gives the budget-constrained buyer a yes that does not cost you rate |
| Recommended | What you actually think they should buy; the middle position visually and in price | Where most buyers land, which is the point |
| Extended | Recommended plus the obvious next thing — measurement, training, a support period | Occasionally taken, and it makes Recommended read as moderate rather than expensive |

Rules: the options differ in **scope**, never in quality or care; the price gaps are meaningful (roughly 0.6× and 1.6× the recommended figure is a workable starting shape, tuned to what each scope actually costs); and none of the three is priced below the floor in `config.yaml`. Three options only work if you would be happy to deliver any of them.

## Terms That Belong in Every Proposal

Short lines in the proposal; the enforceable version lives in the contract (`contract`).

- **Deposit**: `deposit_pct` before the calendar slot is held, stated as a line item rather than a condition — it reads as a step, not as distrust.
- **Payment schedule**: for anything over roughly a month, split it — deposit, one or two milestone payments, balance on delivery. Never a single payment on completion; that puts every hour of the work on your balance sheet.
- **Terms**: `payment_terms_days` from invoice date, with the late-payment consequence named (`getting-paid.md`).
- **Change orders**: what triggers one, and that dates move with scope. One sentence: "Additional work is quoted separately and may move the delivery date."
- **Client obligations**: named approver, feedback turnaround, access provided by a date. Late feedback moves the deadline by at least the delay — say so here, not later.
- **Validity**: the price holds for 14 or 30 days. This is not a pressure tactic; it stops a proposal being accepted six months later at last year's rate.
- **Cancellation**: what is owed if they stop. Work completed plus the current phase is the common shape.

## Sending and Closing

- Send it when you said you would. Missing the first deadline you set is the loudest signal in the process.
- Send it as an attachment or a link with a two-line email, not a document pasted into a wall of text.
- Offer a 15-minute walkthrough. Buyers who walk through a proposal sign more of them, because objections surface in conversation rather than in silence.
- Name the decision date and what happens after it: "If I don't hear by the 14th, the September start goes to someone else and the next slot is October."
- Follow up on the schedule in `pipeline.md`. Do not redesign the proposal because they went quiet; silence is almost never about the document.

## Paid Discovery

When the scope genuinely cannot be known, selling a fixed-price discovery is better than guessing, and better than an hourly build:

- A defined artefact — an audit, a technical plan, a costed roadmap — at a real fee, delivered in one to two weeks.
- It is valuable standing alone: they can take it to another supplier. That is what makes it honest, and it is why the price can be real.
- It converts because it de-risks their decision, and it lets you price the build from evidence rather than optimism.
- Credit some or all of it against the build if they proceed — decide the policy once, write it in `config.yaml` under `commercial`, and apply it consistently.

**Write before you move on:** a proposal that wins gets saved to `~/Clawic/data/clients/artifacts/proposal-<client>.md` — the actual document with prices intact, secrets stripped, plus one line on why it won — and its `## Boxes` line in `memory.md` in the same turn; deriving a proposal shape that converts takes years and nobody should pay for it twice. Update the lead's stage and next date in `## Pipeline`, and on a win, create the roster row, the project file at `~/Clawic/data/projects/<project>.md`, and the contact rows in `~/Clawic/data/contacts/contacts.md`.
