# Routines & recap emails

Any of the six actions can run on a schedule. This file is the cross-cutting playbook for setting them up well — referenced from every action's "schedule it" step.

## The deal in one paragraph

A routine is just a scheduled instance of one action with frozen parameters: criteria, assignee, target object, recap channel. Get those four locked in **one** confirmation message, then run on the chosen frequency. After each run, optionally email a short recap of what changed.

## Setup — the one confirmation message

When the user asks to schedule an action, ask **all** the open questions in one message. Never re-prompt one at a time. The exact question set varies by action — see each `action-*.md`. For every routine, you must end up with:

1. **Criteria** — what triggers it? (E.g., "no activity in 7 days" for follow-up tasks.)
2. **Frequency** — daily / weekly / custom. (See defaults below.)
3. **Assignee or owner** — who gets the tasks, who shows up as the actor in custom activities.
4. **Recap channel** — email recap yes/no, and which email if it's not the user's primary.

### Template confirmation message

> I'll run the **{action name}** routine **{frequency}** with these settings:
> - Criteria: **{criteria}**
> - Assignee: **{assignee or "the workspace owner"}**
> - Recap: **{daily email / weekly email / none}**
>
> Say "go" to start, or tell me what to change.

Wait for "go" (or equivalent). Then start.

## Frequency — defaults and warnings

Use these defaults unless the user has a strong reason otherwise:

| Action                                   | Default frequency | Acceptable range            |
|------------------------------------------|-------------------|-----------------------------|
| Multichannel auto-task creation          | Daily             | Daily — weekly              |
| Auto-pipeline movement                   | Daily             | Daily — every 3 days        |
| Auto-report                              | Weekly            | Weekly — monthly            |
| Prospect research (on new records only)  | Daily             | Daily — on-demand           |
| Contact detection                        | Daily             | Daily — weekly              |
| CRM setup / reorg                        | One-time          | Not a recurring routine     |

**Speed-vs-cost warning.** Anything more frequent than daily can rack up API calls and inbox reads. Whenever the user picks a frequency higher than daily (hourly, every 6 hours, etc.), say it once:

> Just a heads-up: running this more often than once a day can push your API usage and slow things down without much benefit, since most signals (replies, meetings) don't change minute to minute. Daily usually nails the same outcome at a fraction of the cost. Still want to go hourly?

If they say yes, do it. Don't litigate.

## Recap emails — the offer and the setup

For every routine, offer a daily or weekly recap email. **Daily routines** → daily recap is sensible. **Weekly routines** → weekly recap. Match the cadence so they get a clean digest, not a flood.

### How to ask

Fold this into the confirmation message:

> Want a short email recap of each run? I can send you a quick digest of what changed.

### What the recap needs

Whichever email connector the user has linked (Gmail, Outlook, etc.), send a single message after each run with:

- **Subject line:** `[Breakcold] {Action} recap — {date}`
- **Top line:** what was done in one sentence (e.g., "Created 12 follow-up tasks across 12 contacts.")
- **A short list of changes:** name of the affected record, what changed, link to the record in Breakcold if available.
- **Anything that needed a human:** "3 contacts I couldn't confidently classify — review here."
- **No marketing fluff.** No "Have a great day!" Just the facts.

### If the user has no email connector

If you don't have an email tool available in the agent runtime, say so once when offering the recap:

> I can run the routine, but I'd need a connected email account (Gmail, Outlook, etc.) to send you the recap. Want to skip the recap for now, or connect email first?

Never block the routine itself on the recap — they're independent.

## Authentication — never re-prompt mid-routine

Run `capabilities_list` once at the start. If it succeeds, never ask the user about credentials again during this routine. If a downstream call returns an auth error, follow the recovery in `fundamentals.md#authentication-never-ask-twice` — surface the reconnect, then resume.

## Idempotency — runs must be safe to repeat

Every action has its own idempotency rules (see each `action-*.md`), but the universal pattern is:

- **Tasks:** before creating, `tasks_list` on the target record. Skip if an open task with the same intent and a due date within 7 days exists.
- **Pipeline moves:** before moving, check the current stage. Skip if already at the destination or further along.
- **Notes:** before adding a research note, scan recent notes on the record for matching content. Update the existing note instead of stacking duplicates.
- **Records:** see `action-contact-detection.md` for the duplicate detection rules.
- **Custom activities:** these are append-only and timestamped; new ones are fine, but don't write one per minor decision — write one per **batch** of decisions per record per run.

If a re-run would produce the same outcome anyway, the user shouldn't notice or pay for it twice.

## Custom activities as the routine's memory

For every routine run, on records the routine touches, write **at most one** `custom_activities_create` summarizing what happened to that record on that run. Use a consistent prefix so future runs can find them:

```
[breakcold-crm:auto-tasks 2026-05-23] Created follow-up task; last activity 9 days ago (email).
[breakcold-crm:auto-pipeline 2026-05-23] Moved Cold → Warm; positive reply detected on email thread.
```

The prefix makes them trivially filterable in the UI and gives the next run shared memory ("I already moved this contact two days ago").

## Telling the user when to expect the next run

After confirming a routine, tell the user the next concrete run time (e.g., "First run tomorrow at 9 AM your time"). If the agent runtime doesn't actually schedule wall-clock events, be honest:

> I'll re-run this whenever you message me with "run the daily" — or whenever the scheduler in {client name} kicks it off.

Honesty here is cheaper than discovering later that the agent runtime can't actually schedule.

## Stopping a routine

When the user says "stop the routine" / "cancel the schedule" / "I'm done with the daily":

1. Confirm which routine (if multiple are running).
2. Stop. Don't ask "are you sure" — they were already explicit.
3. Send one final recap covering everything since the last one.
4. Write a final `custom_activities_create` with prefix `[breakcold-crm:routine-stopped]` on a sample of records so future agents have context.
