# Stakeholders — Who Actually Decides

Scope: the client-side politics that determine whether good work gets approved, renewed, or quietly killed. Covers working through agencies and middlemen, and dealing with in-house teams. The people records themselves live in the shared `contacts/` box.

Read `~/Clawic/data/contacts/contacts.md` and `roster/<client-slug>.md` before any meeting with more than one person in it, and before drafting anything that needs approval.

**Contents:** [The Four Roles](#the-four-roles) · [Mapping Them Without Interrogating Anyone](#mapping-them-without-interrogating-anyone) · [The Champion Is a Person With a Career](#the-champion-is-a-person-with-a-career) · [Working Through a Middleman](#working-through-a-middleman) · [In-House Teams](#in-house-teams) · [When Your Contact Leaves](#when-your-contact-leaves) · [Committees and Consensus Buyers](#committees-and-consensus-buyers)

## The Four Roles

An org chart shows reporting lines; it does not show who can stop you. Four roles, and one person can hold several:

| Role | What they control | What they need from you |
|---|---|---|
| **Champion** | Access, internal advocacy, the framing of your work | Ammunition: results in their language, on time, that make them look right for hiring you |
| **Economic buyer** | The budget, and the renewal | A number and a risk position. They rarely care about craft, and pretending otherwise wastes the one meeting you get |
| **Blocker** | A veto that is usually procedural — legal, security, IT, finance | Their requirement satisfied early and in their format. Blockers are almost never personal; they are people with a checklist |
| **User** | Day-to-day adoption, and the informal verdict that reaches the buyer | To be consulted before decisions that change their work, not after |

The engagement fails when any one of the four is unmapped. The most commonly missed is the blocker, because they appear late and only once.

## Mapping Them Without Interrogating Anyone

You do not ask "who is the economic buyer" — you ask process questions that reveal it:

- "Who else will want to see this before it goes out?" — surfaces reviewers and blockers.
- "How did the last project like this get approved?" — surfaces the real path, not the official one.
- "Whose budget does this come from?" — surfaces the buyer without naming the concept.
- "Who would be unhappy if this changed how their team works?" — surfaces users, and future opposition.
- "What is the approval limit before it goes higher?" — a number you write in the roster row and never guess again.

Record the answers in `~/Clawic/data/contacts/contacts.md` as one row per person, and the approval chain in `roster/<client-slug>.md`. Rebuilding this map every quarter, from memory, in front of the client, is the observable symptom of not having written it down.

## The Champion Is a Person With a Career

Everything about how to work with a champion follows from one fact: hiring you was their decision, and it is attached to their standing.

- **Make them look right, publicly and specifically.** Results framed in the language their boss uses, with their name attached to the decision.
- **Never surprise them in front of others.** Bad news goes to the champion privately, first, with the proposed fix. A champion ambushed in a meeting becomes a former champion.
- **Give them the internal artefact**: the three-line summary they can paste into their own update, the slide they can present. Most of your work is judged by people who will only ever see that summary.
- **Watch their standing.** Reorgs, a new manager, a missed target — when your champion's position weakens, your project's priority follows within weeks, regardless of quality. That is what "approval times doubling" in the Warning Signals table is usually measuring.
- **Build a second relationship** before you need it. One relationship at a client is a single point of failure, and the moment to build the second is while everything is fine.

## Working Through a Middleman

Subcontracting to an agency, white-label work, or a client who is themselves an intermediary. Different rules apply:

- **Your client is the middleman, not the end client.** They pay you, they set scope, and they own the relationship. Going around them ends the arrangement, however tempting it is when the end client is confused.
- **Get the non-solicitation terms straight up front**, in both directions. Most agencies require them; know the duration before you sign, because it constrains you after the work ends.
- **Payment is back-to-back or it is not.** "We pay when the client pays" transfers their credit risk to you for free. Push for fixed terms; if you must accept pay-when-paid, price the risk in and cap the wait.
- **Two layers of scope means two layers of drift.** Insist on written scope from the middleman, not a forwarded email from the end client. Whatever the end client says to you directly gets confirmed with the middleman before it is actioned.
- **Ask who presents the work.** If they present, your deliverable needs to be presentable without you, which changes what you build.
- **Be visible or invisible, deliberately.** White-label means no attribution, no case study, no reference — which removes the main non-cash benefit of the work. Price accordingly and negotiate an anonymised case study at signature, when goodwill is highest, rather than at the end.

## In-House Teams

The client's own staff are the most under-managed relationship in outside work, and they decide adoption.

- **Name the fear early**: an external supplier often reads as a judgment on the internal team, or as a precursor to replacing them. Saying "you know this system better than I will, I need you for X" in the first meeting is not diplomacy, it is accuracy.
- **Give them credit in writing**, in the status note the buyer reads.
- **Do not route around them when they are slow.** Escalating past an internal team wins the week and loses the engagement; ask the champion to unblock, framed as a priority question rather than a complaint.
- **When they are hostile**, get the requirement in writing and deliver exactly it. A hostile counterpart with an ambiguous spec is an unbounded liability.
- **Handover is theirs.** Anything you build that they must run gets documented for their level of familiarity, not yours (`offboarding.md`).

## When Your Contact Leaves

The highest-risk event in any engagement, and it arrives with no notice.

1. **Assume nothing survives in writing.** Verbal agreements with the departed contact are gone. Reconstruct the scope, the terms and the approvals from your own records within the first week.
2. **Send a short, factual state-of-play** to the new contact: what was agreed, what is in flight, what is needed from them, what the next payment is. Two paragraphs, no history, no complaint.
3. **Expect a review.** A new manager reviews inherited suppliers; that is their job. Bring the change log and the results, not loyalty.
4. **Re-establish the approval chain immediately** and update `roster/<client-slug>.md` — the old limit almost never carries over.
5. **Delete the departed person's row** in `~/Clawic/data/contacts/contacts.md`, note the date and their replacement in `memory.md`, and add the new contact's row.

## Committees and Consensus Buyers

- A committee cannot say yes; it can only fail to say no. Find the one person whose objection would end it, and resolve that objection privately before the meeting.
- **Pre-wire every decision.** Nothing important should first be heard in the group meeting. The meeting ratifies what individual conversations already settled.
- **Give the committee a decision, not options**, once the pre-wiring is done. A committee handed three options will invent a fourth and adjourn.
- Consensus buyers move slowly and change little afterwards — that stability is the compensation for the slow start. Price the sales cycle in, and put a validity date on the proposal (`proposals.md`).
- If the group keeps expanding, someone is avoiding a decision. Ask the champion directly what is missing rather than adding another meeting.

**Write before you move on:** every person learned — name, role, channel, and how they relate to the decision — goes to `~/Clawic/data/contacts/contacts.md` as one row keyed by their email, updated in place if they are already there and deleted with a dated note in `memory.md` when they leave; the approval chain, limits and pre-wire notes go to `roster/<client-slug>.md`; anything said in a meeting that changes scope, price or a date goes to `contact-log/<client-slug>.md` and the decisions table of `~/Clawic/data/projects/<project>.md` the same day.
