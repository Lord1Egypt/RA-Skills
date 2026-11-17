# Trades — Per-Trade Norms, Rights and Benchmarks

Scope: what changes when the same freelance business is run in a different trade — the unit of sale, the revision convention, the rights model, and the trap that trade keeps hitting. The pricing arithmetic itself is `rates.md`; choosing a niche inside a trade is `positioning.md`.

**Before applying anything here**, read `trade` in `~/Clawic/data/freelance/config.yaml` and open only that section. If `trade` is unset, infer it from `## Practice` and `## Engagements` in `memory.md` and **say in one line which trade's norms you are applying** — a statement, not a question. Every trade inherits the invariants below; only its own four columns change.

**Contents:** [What the Trade Does Not Change](#what-the-trade-does-not-change) · [The Norms Table](#the-norms-table) · [Software, Data and Infrastructure](#software-data-and-infrastructure) · [Design and Brand](#design-and-brand) · [Writing and Content](#writing-and-content) · [Marketing, SEO and Paid Media](#marketing-seo-and-paid-media) · [Photo, Video and Audio](#photo-video-and-audio) · [Illustration and Licensed Creative](#illustration-and-licensed-creative) · [Translation and Localization](#translation-and-localization) · [Consulting, Coaching and Training](#consulting-coaching-and-training) · [Operations, Admin and Bookkeeping](#operations-admin-and-bookkeeping) · [A Trade Not Listed Here](#a-trade-not-listed-here) · [Where the Benchmark Actually Lives](#where-the-benchmark-actually-lives)

## What the Trade Does Not Change

The floor arithmetic (SKILL.md Rule 1), the paper order (Rule 7), deposits and the two-week exposure ceiling (Rule 8), concentration (Rule 5) and the set-aside on receipt (Rule 3) are identical in every trade. Believing otherwise — "that is fine for consultants, my field works differently" — is the most expensive trade-specific belief there is. Four things genuinely differ: the **unit of sale**, the **revision convention**, the **rights model** (assignment or licence), and **where a credible benchmark comes from**.

## The Norms Table

| Trade | Unit of sale | Revision norm | Rights model |
|---|---|---|---|
| Software, data, infrastructure | Day or sprint; fixed price per defined deliverable | Defect fixes inside a warranty window; anything else is a change order | Assignment of the deliverable on payment; pre-existing libraries licensed, not sold |
| Product and UX design | Project phase, or day | 2 rounds of consolidated feedback | Assignment of final files; source files priced separately |
| Brand and graphic design | Project with named deliverables | 2-3 rounds, then hourly | Assignment plus a written usage definition for marks |
| Copy and content | Per piece against a target length; retainer per month | 1-2 rounds | Assignment on payment; ghostwriting waives credit explicitly |
| SEO, paid media, marketing | Monthly retainer with a reporting cadence | Not applicable — the deliverable is a cycle | Client owns accounts, pixels and data throughout |
| Photography | Shoot or day, plus a licence | Selects, then one retouching round | **Licence**: usage, territory, duration, exclusivity |
| Video, motion, audio | Per finished minute, or per production day | 2 rounds before picture lock; after lock it is re-quoted | Licence or assignment; music, stock and talent licensed separately |
| Illustration | Per image, plus a licence | 1 round at sketch, 1 at final | Licence by usage; full assignment is a premium, never the default |
| Translation and localization | Per source word; per hour for review | One query round, then corrections only | Assignment on payment; translation-memory ownership stated |
| Consulting and strategy | Day, engagement, or retainer | The deliverable is a decision — one review pass | Report assigned; methods, models and templates stay yours |
| Coaching and training | Session, cohort, or delivery day plus prep | Not applicable | Materials licensed for internal use, never assigned |
| Ops, VA, bookkeeping | Monthly block of hours, or per process | Not applicable — an SLA replaces revisions | Client owns the data and the accounts at all times |
| Any trade not listed | Derive all four before quoting | — | — (→ A Trade Not Listed Here) |

## Software, Data and Infrastructure

- **The estimate is what is really being bought.** Decompose to tasks of ≤1 day and quote a range with contingency (`rates.md`); a single number is heard as a cap, and every discovery after that is your loss.
- **Warranty window, not free maintenance**: a stated period of defect fixes against the acceptance criteria, then a separate support agreement. Without the boundary, "just a small bug" becomes an unpaid retainer with no end date.
- **Blocked time is billable or the date moves.** Access, environments, credentials and reviewers arrive late on most engagements; state which of the two happens, in the contract, before it does.
- **Third-party licences travel with the deliverable.** Name every copyleft or commercially-restricted dependency at handover — shipping one silently into a proprietary product is a live indemnity trigger you personally signed (`contracts.md`).
- **ML and data work cannot promise a performance number.** Milestone on the process — dataset, baseline, metric, evaluation protocol, cut-off — because the accuracy lives in the client's data, not in your effort.
- **Handover is a deliverable with a price**: runbook, architecture note, credentials transferred as pointers, and a named owner on their side.

## Design and Brand

- **A round is consolidated feedback from one named decision-maker.** Unlimited stakeholders are what turn "two rounds" into six; write the name into the contract, not just the count.
- **Source and editable files are a separate priced deliverable.** They hand over the ability to change the work forever, which is a different product from the finished artefact.
- **Present live, never email the deck.** Work presented with its reasoning gets approved; work emailed gets critiqued by whoever opens it first. Bill the presentation as part of the phase.
- **Concept counts are a trap.** Three concepts triple the work and halve your conviction in each; one argued direction with variations converts better and prices better.
- **Brand work carries a usage definition even when assigned**: which entities may use the mark, what happens on a rebrand, and what happens if the business is sold.

## Writing and Content

- **Per word rewards padding and punishes editing.** Price per piece against a target length, or per day for editorial and structural work.
- **The brief is the spec**: audience, angle, sources, length, approver, and whether a keyword governs. A missing brief is what produces the "not our voice" rewrite that no revision count covers.
- **Ghostwriting is a written credit waiver and prices higher, not lower** — the portfolio value is part of what is being sold, and losing it has to be paid for (`positioning.md` on anonymized proof).
- **Kill fee on commissioned work** cancelled after the pitch was accepted, commonly 25-50% of the fee (`contracts.md`).
- **Research, interviews and source-gathering are line items.** They are usually the largest hidden block in a content project and the first thing a client assumes is free.

## Marketing, SEO and Paid Media

- **Never guarantee rankings, traffic or leads.** Guarantee inputs and cadence — audits delivered, changes shipped, tests run, a written analysis — because the outcome depends on their product, budget and competitors as much as on your work.
- **Media spend does not flow through your account** unless the contract prices the float and the risk. The client's card on the client's account keeps chargebacks, VAT treatment and cashflow out of your practice (`cashflow.md`).
- **A percentage-of-spend fee rewards spending, not performance.** A flat retainer plus an optional bonus on a metric the client already reports is the cleaner structure and the easier renewal.
- **Accounts, pixels, domains and data stay in the client's ownership from day one.** Holding them creates a hostage relationship, ends badly, and breaches several platforms' terms.
- **The reporting cadence is the retainer's visible product.** A monthly written analysis ending in the decision it implies is what makes renewal automatic; a dashboard link is what makes it a line item to cut.
- **Three months is the minimum honest engagement** where attribution windows and seasonality apply — quote anything shorter as a diagnostic audit, not as a campaign.

## Photo, Video and Audio

- **The licence is the product; the shoot is its cost.** Price on usage — media, territory, duration, exclusivity — because the same day's work is worth several multiples for a national campaign than for one web page.
- **Usage expansion is a re-licence, not a favour.** Put the extension price in the original agreement so "can we also use it on billboards" already has a number.
- **State the footage-to-runtime ratio you assumed** when quoting per finished minute; edit time scales with source material, and an unstated assumption is an unpaid one.
- **Raw footage, project files and stems are priced separately or excluded.** Handing them over ends the recurring work and the version control with it.
- **Every asset is licensed to someone**: music, stock, fonts, talent. Name who holds each licence and for how long, or the client inherits an unlicensed asset the day it expires.
- **Picture lock is a contractual moment**, not a mood. It is the only defence against infinite tweaks, and the re-quote after it should be in the same clause.
- **Model and property releases** are the freelancer's obligation to obtain in most commercial work, and their absence surfaces years later when the image is reused.

## Illustration and Licensed Creative

- **Full assignment is a premium product, not the default.** Selling all rights forever removes every future relicence; price it well above a bounded licence and say plainly what the client is buying.
- **Sketch approval is a gate**: one round at sketch, one at final. A change of direction after sketch approval is a new commission with a new price.
- **The kill fee scales with the stage** — lower at sketch, near-full at final — and it is agreed at commission, never at cancellation.
- **Credit and portfolio rights are part of the price.** An uncredited, unpublishable job is worth more money, not less.
- **AI-generated components are declared in this trade specifically.** Many clients, agents and licensing platforms prohibit them contractually, and output with no defensible human authorship cannot be assigned — you would be promising to transfer something that may not exist (`contracts.md`, SKILL.md Rule 9).

## Translation and Localization

- **Per source word.** The target count is unknowable at quoting time and languages expand or contract by up to a third between pairs.
- **The CAT-tool match grid is the real negotiation.** Repetitions and fuzzy matches are discounted on a published grid; know which grid you accepted, and price the fact that a 100% match still has to be read in context — unreviewed matches are where errors ship.
- **Translation, review, MT post-editing and transcreation are four services at four prices.** Being paid a post-editing rate for what is actually a retranslation is this trade's standard squeeze; check a sample before accepting the rate.
- **Translation memory and glossary ownership belong in the contract.** They are an asset, and whoever holds them holds the next job.
- **Certified, sworn or notarized translation is a regulated status** in many jurisdictions, with its own liability and its own insurance question (`insurance.md`). It cannot be delivered by someone who does not hold it.
- **Publish a minimum charge and a rush band.** Short jobs are where this trade loses money, one 40-word request at a time.

## Consulting, Coaching and Training

- **The deliverable is a decision, not a document.** Where the client already tracks the number, price against it (`rates.md`, value basis); a report priced by page count is bought as a commodity.
- **Discovery is paid.** A fixed-price, fixed-length diagnostic ending in a recommendation is simultaneously the qualification step, the best proposal you can write, and revenue.
- **Training is delivery days plus preparation**, and first-time preparation is a multiple of the delivery day. The second delivery of the same material is nearly pure margin — which is exactly why materials are licensed for internal use and never assigned.
- **Cancellation terms on booked days need a date-based sliding scale.** A training day cancelled at a week's notice cannot be resold, and that is the loss being priced.
- **Advice drifting into implementation without a re-scope** is the fastest route to being paid as a doer while still being blamed as the adviser.

## Operations, Admin and Bookkeeping

- **An SLA replaces the revision count**: response time, turnaround, coverage hours, and a written definition of "urgent".
- **Access is the risk.** Least privilege, individual accounts inside the client's own systems, and every credential handled as a pointer (SKILL.md Data paragraph) — never a shared password, never their data in your personal accounts.
- **Monthly hour blocks expire or roll exactly once, stated in writing** — the same clause every retainer needs (`rates.md`).
- **Process documentation is billable and it raises the ceiling**, because it lets you sell a setup instead of hours and makes cover possible when you take holiday (`capacity.md`).
- **Regulated bookkeeping, payroll or tax filing work** may require registration, supervision or a licence in the jurisdiction, and it carries its own cover requirement (`insurance.md`, `taxes.md`).

## A Trade Not Listed Here

Derive the four columns before quoting, in this order: (1) **unit of sale** — what the buyer believes they are buying (a thing, a day, a cycle, or a right); (2) **revision convention** — how "done" is agreed and what a change costs; (3) **rights model** — whether the trade sells ownership or licenses usage, and which of the two holds the margin; (4) **benchmark source** (→ below). A trade whose rights model you cannot state in one sentence is a trade being underpriced, because licensing is where the margin usually hides.

## Where the Benchmark Actually Lives

Trade rate numbers age within a year and swing by country, buyer type and specialism, so this file carries none. Sources ranked by reliability: your own `## Win/Loss` log → recruiter and agency bill rates for the same skill in the same city → a professional body's or union's published rate survey (design, translation, illustration and journalism all have one) → peers asked about one specific recent engagement rather than surveyed → marketplace prices, adjusted heavily downward and read as a floor signal only (`platforms.md`, `rates.md`). A benchmark without a date and a source is a rumour.

**When the user states their trade**, write `trade` in `~/Clawic/data/freelance/config.yaml`. **When they state a convention they hold to** — revision count, rights model, minimum charge, rush band, SLA — write it under `conventions:` in the same file: it is a declaration, and it governs every quote from then on. **A benchmark, licence structure or trade norm learned the hard way** goes to `## Pain Points` in `memory.md` with its date and source. **A reusable licence, SLA or scope wording** becomes `~/Clawic/data/freelance/artifacts/<kebab-name>.md` with its `## Boxes` line in the same turn.
