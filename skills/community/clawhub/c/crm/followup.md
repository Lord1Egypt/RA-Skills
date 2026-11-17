# Follow-Up — Cadence, Recency, and the Overdue List

Most value lost in a CRM is not lost to competitors; it is lost to silence. This file produces one artifact: the short list of people who need something from you today, and the reason.

**Contents:** [The Overdue Sweep](#the-overdue-sweep) · [Tiering, Decided Once](#tiering-decided-once) · [Next Step Discipline](#next-step-discipline) · [Reasons To Reach Out](#reasons-to-reach-out) · [Trigger Events](#trigger-events) · [Cadence Inside A Live Deal](#cadence-inside-a-live-deal) · [Reconnecting After A Long Silence](#reconnecting-after-a-long-silence) · [Logging Without Friction](#logging-without-friction) · [What Not To Automate](#what-not-to-automate)

**Before producing any follow-up list**, read `## People` in `memory.md` (or `people.md` once it has split) for tiers, `interactions/<year>.md` for recency, `## Pipeline` for live deals, and `do-not-contact.md` — the suppression check happens before a name is spoken, not before a message is sent (SKILL.md Rule 8).

## The Overdue Sweep

Run it at the start of any "who should I contact" question, in this order. Each step has a different urgency, and mixing them produces a list nobody acts on.

1. **Deals with an overdue next step** — the next-step date is before today. Highest value on the list, always.
2. **Deals with no next step at all** — route to the stall protocol (`pipeline.md`), not to a message.
3. **Live-deal contacts with no interaction in 14 days** — a deal can be on schedule and going cold at the same time.
4. **Tier A with no interaction in 14 days** — clients and the ten people who move your year.
5. **Tier B past `stale_days`** (default 90) — reconnection candidates, batched, not urgent.
6. **Anyone whose trigger event fired** (below) — the highest-response contacts in the whole list.

A contact with an open deal is governed by the deal, never by the stale sweep (SKILL.md) — one person, one row on the list, or both get ignored.

Cap the output at ten. A twenty-name list is a to-do list; a ten-name list is an afternoon.

## Tiering, Decided Once

| Tier | Test | Touch every | If you miss it |
|---|---|---|---|
| A | A live deal, a paying client, or someone whose call you would take at any hour | 1-2 weeks | Something is slipping now |
| B | Past clients, warm network, dormant opportunities, referrers | Quarter | Reconnection work, no apology required |
| C | Worth keeping, no rhythm | Yearly, or on a trigger | Nothing — a C contact is not a debt |

- Tier is a **stored field, not a judgment made at read time** — otherwise the sweep is different every week. It lives in the person's row in `## People` in `memory.md` (`people.md` after the split), keyed by the lowercased email; a person with no row is unassigned and swept as tier B.
- **Referrers are tier A even with no deal in sight.** In most solo and small-team businesses, referral is the highest-conversion source in `metrics.md`, and it is the only one that goes quiet without any visible signal.
- Demote deliberately: overwrite the `Tier` cell on their row in `## People` and set `Since` to today, in the same turn you decide it. A tier-A contact who stops being one is fine; a tier-A contact who quietly gets tier-C treatment is how relationships end without anyone deciding to end them.
- ~20 tier-A contacts is the practical ceiling for one person at a two-week cadence: 20 people × 26 touches a year is already a part-time job. If the list is longer than that, tiering has become wishful.

## Next Step Discipline

- **Every interaction ends with a next step and a date, or an explicit reason there is none.** This is the same rule as SKILL.md Rule 3, applied at the conversation level rather than the deal level.
- The next step is **the buyer's**, whenever one exists. "They send the security questionnaire by Friday" beats "I follow up Friday", because only the first tells you something when it does not happen.
- Never leave a call without the next date **on a calendar the other person can see**. A CRM task nobody else can see is a reminder, not a commitment.
- "Follow up in a while" is not a next step; neither is "keep warm". Both mean the deal is a contact (`pipeline.md`).

## Reasons To Reach Out

Ranked by response rate, best first. The ladder matters more than the wording: a good reason with clumsy phrasing beats a polished "just checking in", which is a request for attention with nothing offered.

1. **Something they said would happen, happened** — their launch shipped, their funding closed, their quarter ended.
2. **Something changed in their world that you can act on** — a job change, a new role in their team, a regulation in their sector.
3. **You have something specific for them** — an intro, a result from a similar client, an answer to the objection they raised last time.
4. **A promise you made** — "I said I would send this in March."
5. **A deadline of yours that is honestly theirs too** — a price change, a capacity window. Only real ones; a manufactured deadline that passes teaches them your deadlines are fake.
6. **Nothing to say but the relationship matters** — say exactly that, in one line, with no ask. It works precisely because it is rare and honest.

Writing the message itself, sequences and campaigns: `outreach`.

## Trigger Events

A trigger converts a cold contact into a warm one for about two weeks. Watching for them is worth more than any cadence rule.

| Trigger | Why it converts | The move |
|---|---|---|
| Job change | New budget, new mandate, ninety days to look effective — and your old champion is now a warm lead at a new company **and** a new contact has appeared at the old one | Congratulate within a week; open a new organization record, keep the old one live |
| Funding round | Money exists that did not exist last month | Reach in the first month, before the queue forms |
| New leader in a function you sell to | New leaders replace tools and vendors early | First 60 days |
| Their competitor did something | Relevance you did not have to manufacture | Only with a specific observation, never a link dump |
| A conference or event you both attend | A meeting is cheap to ask for | Book before the event, not during |
| Their contract renewal date (yours or a competitor's) | The one date on which switching is easy | One full sales cycle before it |
| A reply that says "not now, try in Q3" | They named the date, so it is theirs | Store it as a dated next step immediately — this is the highest-conversion re-open in a solo pipeline |

Whatever the source — a mailing list, a news alert, a `follow` feed — the trigger only counts once it is a dated next step on a record.

## Cadence Inside A Live Deal

- **Match their pace, then add one step.** If a buyer replies in a day, a week of silence from you reads as disinterest; if they reply in ten days, three messages in a week reads as desperation.
- After a proposal, the useful rhythm is roughly: day 2 (confirm receipt, offer a review call), day 5-7 (one substantive addition — a reference, a phased option), day 14 (the breakup message, `pipeline.md`). Silence between those is deliberate, not neglect.
- **Never send two messages with no new information.** Each contact carries something: an answer, an option, a piece of evidence, a decision they need to make.
- Change channel before changing frequency. Two unanswered emails then a phone call outperforms four emails, in every business where the phone is still answered.
- When a deal goes quiet, the person to contact is often not the one who went quiet: the champion's silence usually means an internal blocker, and the signer has no idea you exist.

## Reconnecting After A Long Silence

- The gap is not a debt and does not need an apology. "It has been a year, here is why I thought of you" is complete.
- Use the record: the last interaction line tells you what they cared about, which is what makes a two-year-old relationship resumable. This is the payoff of `interactions/<year>.md` and the reason one line of substance beats "good call".
- **Ask nothing on the first message back.** The reconnection and the ask are two different messages, days apart.
- If two reconnection attempts get nothing across a year, demote to tier C and stop; the record stays, the rhythm ends. That decision goes into their `Tier` cell in `## People`, not into a resolution to try harder.

## Logging Without Friction

The best logging system is the one that survives a bad week. In descending order of survival:

1. **One line, immediately after the conversation**, into `interactions/<year>.md` — 15 seconds, while the substance is intact.
2. **BCC to the CRM** for email (`email_logging: bcc`) — captures the thread with no discipline required; the BCC address is a credential (`memory-template.md`).
3. **Inbox sync** (`email_logging: sync`) — complete, unreadable, and it ingests personal mail nobody consented to store (`privacy.md`).
4. **Batch entry at week's end** — the format that loses the substance. When it is the only realistic option, log the next step only and accept that the history is gone.

Voice-to-text after a call, then one line extracted from it, beats all four for people who hate typing — the transcript is not the record, the line is.

**Write in the same turn as the conversation**: the interaction row in `interactions/<year>.md` with its next step, the deal's next-step field in `## Pipeline`, a tier change in their row in `## People`, a role or channel change in the shared `~/Clawic/data/contacts/contacts.md`, and a `## Due` update if a recurring sweep ran (`memory-template.md`).

## What Not To Automate

- **Never automate the first touch of a tier-A relationship.** A templated message to someone who knows you is a downgrade they will notice.
- Never automate anything against records that have not passed a bounce and dedupe sweep (`hygiene.md`).
- Never automate a "just checking in" sequence: it manufactures the exact contact that reduces response rates for the contacts that matter.
- Automate the *detection* — overdue lists, trigger alerts, renewal dates — and keep the sending human (`automation.md`).
