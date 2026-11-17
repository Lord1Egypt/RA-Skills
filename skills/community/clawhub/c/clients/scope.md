# Scope Creep and Change Orders

Scope: what to do when the work being asked for stops matching the work that was sold. Writing the original boundary is `proposals.md`; the rhythm of the engagement is `delivery.md`.

Read the signed scope and the `## Change Log` in `~/Clawic/data/projects/<project>.md` before answering any "can you also…" — the answer depends far more on what is already in that log than on the size of the new request.

**Contents:** [Creep Is an Accumulation, Not an Event](#creep-is-an-accumulation-not-an-event) · [Classify the Request in Three Questions](#classify-the-request-in-three-questions) · [The Change Order](#the-change-order) · [The Free-Favour Ledger](#the-free-favour-ledger) · [The Six Shapes of Creep](#the-six-shapes-of-creep) · [Scripts](#scripts) · [When It Has Already Happened](#when-it-has-already-happened)

## Creep Is an Accumulation, Not an Event

No single request causes the problem. Each is small, reasonable, and cheaper to do than to discuss — which is precisely the mechanism. By the time the total is visible, it is a large number attached to a dozen tiny yeses that were each defensible.

Two consequences that drive everything below:

- **The unit of control is the log, not the refusal.** You can say yes far more often than you think, provided every yes is recorded with its estimated hours. A logged free favour costs you the hours once; an unlogged one costs you the renewal argument as well.
- **The client is usually not exploiting you.** They cannot see the accumulation either. The first time most clients learn what they have added is when someone shows them the list — and the list is persuasive in a way that a complaint is not.

## Classify the Request in Three Questions

| Question | If yes | If no |
|---|---|---|
| Is it named in the scope document, or a reasonable reading of it? | In scope — do it, no log entry needed | Continue |
| Would it take longer than the trivial threshold (roughly 30 minutes, or whatever `config.yaml` says under `commercial`)? | Change order — price it (below) | Do it, and **log it in `## Change Log` with its estimated hours** |
| Does it move a deliverable's date or displace other work? | Change order regardless of size — the date is the scarce thing, not the hour | Log it in `## Change Log` |

Never a fourth option. "Do it quietly because it is small" is how a project ends 40 hours over with no evidence.

## The Change Order

A change order is four lines in an email, not a document. Heavy process makes people avoid it, and avoidance is the failure mode.

> **Change: add motion graphics to the three hero assets.**
> Effort: ~22 hours.
> Price: 5,000 EUR, invoiced with the next milestone.
> Impact: launch moves from 28 August to 4 September.
> Reply "approved" and I'll start Monday.

Rules that keep it working:

- **Price and date, always both.** A change order with a price but no date impact teaches that time is free, and the schedule is where creep actually lands.
- **Send it before the work, not after.** After is an invoice for something they did not buy, and it is refusable.
- **One request, one change order.** Bundling three requests into one number invites negotiation on the whole bundle.
- **Offer the swap as an alternative**: "or we can trade it for the reporting page, no change in price or date." Swaps get accepted more often than additions and they protect margin better than refusals.
- **A refusal is also recorded.** "Requested, declined, out of scope" in the change log — it stops the same request returning in month four as an assumption.

## The Free-Favour Ledger

Every out-of-scope thing you do free gets a row in `## Change Log` in the project file with its estimated hours and `Outcome: done free, logged`. This is the highest-value habit in the entire domain and it takes fifteen seconds.

What the ledger buys:

- **The renewal conversation.** "Last year included 38 hours outside the agreed scope; this year's retainer reflects that" is a fact. "It felt like a lot of extra work" is a feeling, and feelings lose to budgets.
- **A visible generosity account.** Clients who see the list usually feel well served rather than accused — provided you show it as value delivered, not as a debt collected.
- **A self-check.** If the free column is consistently larger than the billed column, the problem is your scoping, not their behaviour.

Show the ledger at renewal, at any price conversation, and the moment a client questions value. Never show it in anger, and never present it as an invoice for work already given away.

## The Six Shapes of Creep

| Shape | How it presents | Counter |
|---|---|---|
| **Salami** | Many sub-hour requests, each trivially reasonable | Log every one; the fourth in a fortnight triggers a "here's where we are" note with the running total |
| **Gold-plating** | You add polish nobody asked for and it becomes the standard | The most self-inflicted shape. Deliver to the agreed definition of done, and offer the extra as a priced option |
| **Definition drift** | The same deliverable quietly becomes bigger — "the report" grows from 5 pages to 30 | Quantities in the scope document (`proposals.md`); restate the number when it moves |
| **Stakeholder accretion** | A new reviewer appears with a new set of requirements | Change order for their requirements, and add them to the stakeholder map (`stakeholders.md`) |
| **Support drift** | Post-delivery questions become an unpaid support contract | A support window with an end date in the scope, and a priced retainer after it (`pricing.md`) |
| **Emergency drift** | Repeated urgent requests outside hours become normal | Name it once, price rush work, and hold the working hours (`delivery.md`) |

## Scripts

Small requests, in scope of goodwill but not of contract:

> "Happy to do that one — it's outside what we scoped, so I'll log it as no charge this time. For reference it's about three hours, so if these become regular we should fold them into the retainer."

A request that needs a change order:

> "That's a good addition and it's outside the current scope. It's about 22 hours, 5,000 EUR, and it moves launch to 4 September. Want me to send it as a change order, or would you rather swap it for the reporting page?"

The fourth small request in a fortnight:

> "Quick heads-up before I start on this: we're at about 11 hours of extras this month on top of the scope. All fine, and none of it billed — but I'd rather flag it now than surprise you later. Shall I keep absorbing them, or start quoting them?"

A request that would break the deadline:

> "I can do that, but not without moving the date. Options: it lands on 4 September instead of 28 August, or we swap it for something of similar size and keep the date. Which do you prefer?"

Each of these is a question, not a complaint, and each hands the client a decision they are able to make.

## When It Has Already Happened

The project is 40% over, nothing was logged, and the deadline is close. Do not open with the money.

1. **Reconstruct the list** from emails, tickets and the contact log, with honest hour estimates. Approximate is fine; itemised is what matters.
2. **Fix the boundary going forward first.** "From here, anything not on this list is a change order." Retroactive billing is a much harder ask than a forward-looking freeze, and the freeze alone recovers most of the loss.
3. **Ask for part of it, at the right moment** — at renewal or the next phase, framed as recalibration rather than back-billing: "the last phase ran 30% over scope; this one is priced for what the work actually is."
4. **Absorb the rest and change the process.** Chasing every retroactive hour damages a relationship worth more than the hours, and the real fix is the log plus a scope document with quantities in it.
5. **Write the post-mortem** while it is fresh, to `artifacts/postmortem-<client>.md`: which shape of creep it was, the first signal, and the scope-document sentence that would have prevented it.

**Write before you move on:** every out-of-scope request goes into `## Change Log` in `~/Clawic/data/projects/<project>.md` with its estimated hours and outcome — priced, done free, or declined — in the same turn it is answered; a change order that is approved also updates the milestone dates in that file and the amount in `## Receivables` once invoiced; a recurring pattern of creep with one client goes into their `roster/<client-slug>.md` quirks and their `Health` cell in `## Roster`; a script or a recalibration message that worked goes to `artifacts/script-<topic>.md` with its `## Boxes` line.
