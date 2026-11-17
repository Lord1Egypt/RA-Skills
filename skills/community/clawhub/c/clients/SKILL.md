---
name: Clients
slug: clients
version: 1.0.2
description: 'Manages client relationships end to end for freelancers, consultants, and agencies: qualifying leads, scoping, onboarding, scope creep, getting paid. Use when a prospect enquires and the call is whether to take them, when a proposal or SOW has to be scoped and priced, when onboarding needs access, stakeholders and approvals, when the client keeps adding "one small thing", when an invoice is late and the chase has to escalate, when a client goes quiet or the relationship is decaying, when rates have to go up on an existing client, when an engagement is renewing, expanding, or ending, and when a client has to be fired or a hard conversation drafted. Covers retainers versus project work, change orders, procurement, handover, and referrals. Not for drafting the contract itself (`contract`), issuing invoices (`invoice`), filing received invoices (`invoices`), a personal contact book (`people`), running an agency as a business (`agency`), or platform tactics on Upwork (`upwork`).'
homepage: https://clawic.com/skills/clients
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 💼
    os:
    - linux
    - darwin
    - win32
    displayName: Clients
    configPaths:
    - ~/Clawic/data/clients/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
  openclaw:
    requires:
      config:
      - ~/Clawic/data/clients/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
---

**Data.** At the start of every session, read `~/Clawic/data/clients/config.yaml` (what the user declared) and `~/Clawic/data/clients/memory.md` (what you observed, plus its `## Boxes` index and its `## Due` table). Open any file `## Boxes` names the moment the condition written on its line applies — that index *is* the list of files; never work from a list of names memorised here, because most boxes are created after this skill was written. Before saying anything about a named person, read `~/Clawic/data/contacts/contacts.md`; before anything about a live engagement, read its `~/Clawic/data/projects/<project>.md`. If none of it exists, work from the defaults below and say nothing about it. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens.

**Write before the session ends** whenever it produced something durable: a lead in or out, a client won, paused, or retired, a rate or terms change, a stakeholder learned, a meeting or decision, a change order, an invoice sent, chased, or paid, a renewal or end date, a concentration number — or something the user will read again: a winning proposal, an onboarding checklist, a rescue plan, a script that worked, a handover, a post-mortem. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**People and projects live in shared boxes, not here.** Every human at a client goes to `~/Clawic/data/contacts/contacts.md` — one row, `name | role | preferred channel | context`, identified by **email or handle**. Read that file before adding: if the address is already there, update that row in place, never append a second one, and never touch a row this skill did not write. When someone leaves, delete their row and note the date in `memory.md` — a contact list that only grows stops being one. Table until ~15 people; past that, one file per person at `~/Clawic/data/contacts/<name>.md`, with `contacts.md` left as the index. If the file already exists with different columns, match its columns and add anything missing as a trailing note; never rewrite its header. Every engagement with a start, an end and milestones goes to `~/Clawic/data/projects/<project>.md`, one file from the first, identified by the project name; the client is referenced there **by name only**. Duplicating a person or a project into the clients box is the fastest way to make two skills contradict each other.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be kept. Clients hand over logins constantly at kickoff; store the pointer and drop the value: `1password:Clients/Acme/wp-admin`, `keychain:acme-sftp`, `env:ACME_API_TOKEN`.

Client work fails at the seams, not in the craft: the thing that was never written down, the favour that became the baseline, the invoice nobody chased. Be specific and dated — a name, an amount with its currency, a date, a next step with an owner. Draft what the user will send; never send it, never quote a price the user has not set, never accept a change on their behalf. Work from defaults immediately: no interview about their business, their rates, or how they like to work. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale, timezone) → the Configuration table default.

## When To Use

- Mode: **act-as** — this skill runs the user's client system and drafts what goes to the client. The user sends, signs, and commits; it never does
- A lead arrived and the decision is whether to take it, what to charge, and what to write back
- Kicking off: scope document, access, stakeholder map, approval chain, working agreement
- Running a live engagement: status cadence, decisions, change orders, expectation management, bad news
- Money: deposits, terms, a late invoice, a stop-work call, a rate rise, collections
- The relationship itself: a client going quiet, a rescue, a firing, a renewal, an ending, a referral, a testimonial
- Portfolio questions: concentration, capacity, which clients to keep, whether to take one more
- Not for drafting or reviewing contract language (`contract`), issuing or numbering invoices (`invoice`), archiving invoices received from suppliers (`invoices`), a personal address book (`people`) or personal relationship tracking with no commercial engagement behind it (`crm`), running an agency as a business — hiring, utilisation, team structure (`agency`), or the consulting problem-solving method itself (`consultant`). This skill is the commercial relationship with a paying client, from lead to ending

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "Someone enquired — should I take it?" | Score against the decline list before pricing anything; the answer is often no | `pipeline.md` |
| Writing the proposal or statement of work | Three-option ladder, deliverables as nouns, exclusions section longer than you want | `proposals.md` |
| Setting or raising a price | Effective hourly rate first, then the model; rises get a date and a reason, never a negotiation | `pricing.md` |
| Just won it — what now | Deposit before calendar; access, stakeholders, approval chain, working agreement, kickoff | `onboarding.md` |
| Enterprise procurement, vendor portal, security questionnaire | Treat it as its own mini-project with its own timeline; it delays first payment, not first work | `onboarding.md` |
| "Who actually decides here?" | Map champion, economic buyer, blocker, and user; the org chart is not the map | `stakeholders.md` |
| Running the week: status, meetings, decisions | Status on cadence unasked; every decision written back within a day | `delivery.md` |
| Delivering bad news, a delay, or a no | Bad news early is a status update; bad news late is a breach | `delivery.md` |
| "Can you just add one small thing?" | Change order, priced or logged — never both free and invisible | `scope.md` |
| Invoice is late, or the client stopped paying | The ladder in Payment Ladder below, on dates, no improvisation | `getting-paid.md` |
| Client is hostile, chaotic, ghosting, or abusive | Rescue plan with a review date, or the exit procedure; both are written | `difficult-clients.md` |
| Renewal, expansion, referral, testimonial | Ask at the moment of delivered value, not at the moment of need | `retention.md` |
| Engagement is ending, well or badly | Handover pack, final invoice, access revoked, post-mortem, reference secured | `offboarding.md` |
| One client is most of the income; capacity is full | Concentration share, utilisation, and the replace-or-shrink decision | `portfolio.md` |
| Anything else about a client | Answer from the roster and the contact log, then name the next step, its owner, and its date | — |

Coverage map: `pipeline.md` leads and qualification · `proposals.md` scoping and winning · `pricing.md` rates and models · `onboarding.md` kickoff and procurement · `stakeholders.md` client-side politics · `delivery.md` running the engagement · `scope.md` creep and change orders · `getting-paid.md` cash · `difficult-clients.md` rescue and exit · `retention.md` renewals and referrals · `offboarding.md` endings · `portfolio.md` client mix and capacity.

## Core Rules

1. **Read the roster before you speak about a named client.** `## Roster` in `memory.md` (or the file its `## Boxes` line points to), the contact rows, the project file, and the client's `contact-log/` entry. Answering from the conversation alone recreates the amnesia the user installed this to end — and the second time you ask what their payment terms are, you have taught them the system does not work.
2. **Nothing starts before the paper and the deposit.** Signed scope plus `deposit_pct` of the fee received (default 50% on a first engagement, 30% once a client has paid twice on time) before a calendar slot is held. The deposit is not about cash flow; it is the cheapest test of whether the buyer can actually buy. Skip it only when `contract_required` is false and the amount is below one day of work.
3. **Anything not in the scope document is a change order.** Price it or log it, never neither. A logged free favour still gets its estimated hours written into the project's change log — that ledger is the whole argument at renewal, and it is why "we've done 40 unbilled hours" beats "it feels like a lot" (`scope.md`).
4. **Chase on dates, not on feeling.** The ladder below runs on the calendar from the due date, with no step skipped and no step delayed because the conversation feels awkward. Each rung is written; a chase that happened only in your head did not happen.
5. **Concentration is a number you compute, not a feeling.** Share = client revenue over the trailing 12 months ÷ total revenue over the same 12 months. Above `concentration_limit_pct` (default 30%) it is a standing risk item in `## Due`; above 50% the user has an employer without any of employment's protections, and the fix is pipeline, not loyalty (`portfolio.md`).
6. **Status goes out unasked, on `status_cadence`.** A client who has to ask how it is going has already spent a day worrying, and worry converts into scope questions and slow approvals. Cheapest insurance in the whole domain: three lines — done, next, blocked-on-you — on a fixed day.
7. **Every decision gets written back the same day, to the person who made it.** "Confirming: we're going with B, which moves the launch to the 14th; tell me by Thursday if that's wrong." Silence against a written, dated restatement is worth something later; a verbal agreement is worth nothing.
8. **Price changes get notice and a reason, never a negotiation in the moment.** Announce 30-60 days out, in writing, effective at the next renewal or next project — not mid-delivery. "From 1 October my rate is X" is a statement; "would you be okay with a rise?" invites a counter you then have to accept.

## Payment Ladder

Canonical for this skill; run from the invoice due date, one rung per step, every rung recorded in `## Receivables`. Detail, escalation letters, and what to do when they simply will not pay: `getting-paid.md`.

| Day | Move | Channel |
|---|---|---|
| Due date | "Invoice 0042 is due today, here it is again" — one line, no apology, attachment re-sent | Email to accounts payable, cc the client contact |
| +3 | Confirm it was *received and entered*, not whether it was paid — most late invoices are lost, not refused | Email, reply in the same thread |
| +7 | Second notice naming the late-payment term from the contract and the date interest starts | Email, new subject line |
| +14 | Phone the AP contact, then email a one-line summary of the call — the call is what moves it, the email is what proves it | Phone, then email |
| +21 | Written stop-work notice: work pauses on a named date until the balance clears; keep it factual and unemotional | Email to the client contact and their manager |
| +45 | Formal demand, then a collections agency or small-claims filing; statutory interest and fixed recovery costs apply in the UK and the EU (see `getting-paid.md`) | Letter or legal channel |

## Warning Signals

The domain's tell is that every disaster announces itself weeks early in a way that looks like nothing. Each row is a signal you can observe, not a mood.

| Signal | What it usually means | Move |
|---|---|---|
| "We'll sort the paperwork later, can you start Monday?" | The buyer cannot sign, or intends the terms to stay negotiable | No start without paper; offer a small paid discovery instead (`pipeline.md`) |
| Deposit is "in process" for more than a week | They cannot pay, or you are not in their AP system yet | Stop before delivery, not after; check procurement onboarding (`onboarding.md`) |
| The approver never attends the call | You are talking to a messenger; every decision will be re-litigated | Get the economic buyer into one meeting or reprice for the delay (`stakeholders.md`) |
| Requests arrive by direct message at night, outside the tracker | The working agreement was never really adopted | Restate the channel once, in writing, then only answer in it (`delivery.md`) |
| Three "quick things" in a fortnight | Scope is drifting by accretion; nobody will notice until margin is gone | Log the hours, then convert the fourth into a change order (`scope.md`) |
| Approval times doubling | Priority is dropping internally, or your champion is losing standing | Ask the champion directly what changed; check for a reorg (`stakeholders.md`) |
| An invoice is late for the first time from a client who never was | Their cash has turned, and you are a supplier they can stretch | Tighten terms on the *next* invoice, do not wait for a pattern (`getting-paid.md`) |
| Feedback shifts from the work to your process or attitude | Someone internal is building a case, usually to justify a switch | Rescue plan with a named review date (`difficult-clients.md`) |
| Silence from an active client for longer than the status cadence | Project deprioritised, budget frozen, or your contact has left | One direct question, then a dated pause proposal (`retention.md`) |
| They want set hours, their equipment, and exclusivity | Employment dressed as contracting; classification exposure for both sides | Push back on control terms, not on the fee (`pipeline.md`) |
| Anything else that feels off | Write down the observable behaviour and its date in the contact log | Two entries of the same behaviour is a pattern; act on the second, not the fifth |

## Engagement Models

One default, with the switch condition. Break-evens and how to move a client from one to another: `pricing.md`.

| Model | Default when | What breaks it |
|---|---|---|
| Fixed-price project | Scope can be written as deliverables with an end date — the default (`engagement_default`) | Discovery is genuinely unknown; then sell a paid discovery first and price the build after |
| Monthly retainer | Work is continuous, the client needs availability, and you want predictable revenue | Retainer used as an unlimited pass; cap hours or scope and state whether unused hours roll over |
| Hourly / day rate | You cannot control the scope and the client accepts open-ended cost | It caps income at your hours and makes efficiency a pay cut; use as a bridge, not a business |
| Value-based fee | The outcome has a number the client already believes and you can influence it | The client must own the number; without an agreed baseline it becomes a fixed fee with an argument attached |
| Equity or revenue share | Never as the whole fee; only on top of a rate that covers costs | Illiquid, unenforceable in practice for a small holder, and it converts a client into a co-founder relationship |

## Output Gates

Before sending anything to a client, or ending a session that touched one:

- Does every commitment in this message have an owner, a date, and a deliverable that is a noun?
- Is any amount written with its currency, and any estimate marked as an estimate with its date?
- Did I check the roster, the contact rows, and the project file before asserting anything about this client's terms, people, or history?
- If this changes scope, price, or a date, is it going out as a written change order rather than buried in a friendly paragraph?
- Am I about to send, sign, or accept on the user's behalf? Stop — draft it and hand it over.
- **Persistence:** is everything durable from this session written to its box — roster row, contact row, project file, `contact-log/<client>.md`, `## Receivables`, `## Due`, `artifacts/` — with a `## Boxes` line for any file created in this same turn?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/clients/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| engagement_default | project \| retainer \| hourly \| value | project | The model proposed first in Engagement Models and priced first in `proposals.md` |
| payment_terms_days | number (0-90) | 30 | Terms written into every proposal and invoice line, and the zero point of the Payment Ladder |
| deposit_pct | number (0-100) | 50 | Share required before work starts (Rule 2); 0 disables the deposit gate |
| status_cadence | weekly \| biweekly \| monthly \| on-milestone | weekly | Frequency of the unasked status note (Rule 6) and the silence threshold in Warning Signals |
| invoicing_day | number (1-28) | 1 | Day of month invoices go out; seeds the recurring row in `## Due` |
| concentration_limit_pct | number (0-100) | 30 | Share of trailing-12-month revenue above which a client is flagged as risk (Rule 5, `portfolio.md`) |
| contract_required | bool | true | Whether work may begin on a written email confirmation instead of a signed document |
| no_go_list | list | none | Sectors or work types to decline outright; applied at the top of qualification in `pipeline.md` |
| rate_card_file | path | none | Long-form rates and packages at `~/Clawic/data/clients/<file>`; overrides ad-hoc pricing in proposals |
| voice_file | path | none | How the user writes to clients (register, length, sign-off) at `~/Clawic/data/clients/<file>`; overrides the default plain register in every draft |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — invoicing, e-signature, project tracker, time tracking, scheduling and the shared-drive convention the client work runs on; affects where `onboarding.md` sends access and where invoice references point
- **Conventions** — client slug and project-code style, file naming, proposal and status-report structure, invoice reference format; affects every artifact name and the roster
- **Communication** — default channel, response-time promise, meeting length and preferred day, language and formality per client, out-of-hours policy; affects `delivery.md` and every draft
- **Commercial** — rate floor, discount and rush-surcharge policy, retainer rollover rule, kill-fee stance, currency for quotes; affects `pricing.md` and `proposals.md`
- **Risk posture** — hardness on stop-work, tolerance for unsigned starts, appetite for a rescue versus an exit, how many missed payments end a relationship; affects `getting-paid.md` and `difficult-clients.md`
- **Cadence** — portfolio review rhythm, dormant-client re-contact window, rate-review month, testimonial-ask timing; affects the `## Due` table

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Starting on a verbal yes to keep momentum | The one client who exploits it is the one who will not sign afterwards, and you have already spent the leverage | Paid discovery or a one-page signed scope; momentum is not consideration (Rule 2) |
| Absorbing small extras to seem easy to work with | Generosity read as capacity: the extras become the baseline and the renewal is priced off the inflated version | Do it and log it in the project's `## Change Log`, or price it — never do it invisibly (Rule 3) |
| Discounting to win, planning to "make it up later" | The discount anchors the relationship's price forever and the later work is quoted against it | Cut scope to hit the budget, keep the rate; a smaller yes protects the rate (`pricing.md`) |
| Chasing an invoice only when cash is needed | The chase then reads as your problem, not their obligation, and lands 40 days late | Fixed ladder from the due date, run regardless of your balance (Payment Ladder) |
| Letting the loudest client set the week | Attention flows to conflict, so the quiet profitable client gets the leftovers and quietly leaves | Cadence per client, set in advance and defended (`delivery.md`) |
| Treating the day-to-day contact as the decision maker | The real approver arrives at the end with objections nobody rehearsed | Map the buyer at kickoff and get them in one meeting (`stakeholders.md`) |
| Waiting until renewal to mention the extra work you did | Nobody buys a bill retroactively; goodwill is not evidence | The change log, written as it happens, is the renewal argument (`scope.md`) |
| Firing a client in the message where you are angry | Bridges burn in an industry that runs on referral, and unpaid balances stop being collectable | Exit script with a notice period, handover, and final invoice (`offboarding.md`) |
| Filling the calendar with the client who is 60% of income | Every hour spent there is an hour not spent replacing them, which is the actual work | Concentration first, then capacity (Rule 5, `portfolio.md`) |
| Keeping the client's history in your head and the chat log | The system exists precisely because that history is what makes the next conversation good | Roster row, contact rows, contact log — written the same session |
| Reopening a scope decision because the client seems unhappy | It teaches that pushback reverses decisions, and the next one arrives sooner | Restate the written decision, offer a change order as the path forward |

## Where Experts Disagree

- **Fire the bad client, or fix them.** The exit school says a client who disrespects boundaries never stops and the margin is illusory once you count unpaid hours; the rescue school points out that most "bad clients" are badly onboarded ones and that a rewritten working agreement fixes a large share. The frontier is *what kind* of bad: process problems (unclear approvals, wrong channel, no scope doc) are usually yours to fix; behaviour problems (abuse, repeated non-payment, dishonesty) are not fixable by better process (`difficult-clients.md`).
- **Retainers versus projects.** Retainers give predictable revenue and cheaper client acquisition; projects give higher effective rates and a natural exit. The real split is who bears the variance — a retainer transfers scope variance to you unless it is capped, which is why capped retainers behave like projects and uncapped ones behave like employment.
- **Hourly billing.** One camp treats hourly as unprofessional because it prices effort rather than outcome and punishes speed; the other keeps it for genuinely unbounded work, where a fixed price is just a bet the client did not agree to. Both agree that hourly with no cap and no scope is the worst of every option.
- **Niching down.** Specialists get higher rates and shorter sales cycles; generalists survive a sector's bad year. The disagreement is mostly about portfolio size: below roughly five clients, a niche concentrates risk that a generalist spreads (`portfolio.md`).

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/clients (install if the user confirms):
- `contract` — drafting the agreement this skill assumes is signed
- `invoice` — creating and numbering the invoices this skill tracks
- `projects` — running the delivery plan inside an engagement
- `people` — the personal contact book behind the shared `contacts/` box
- `negotiate` — the live negotiation of a price or a term

## Feedback

- If useful, star it: https://clawic.com/skills/clients
- Latest version: https://clawic.com/skills/clients

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/clients.
