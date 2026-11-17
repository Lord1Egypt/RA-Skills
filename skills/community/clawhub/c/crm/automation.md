# Automation — Sync, Workflows, and What to Keep Human

Automation multiplies whatever the data already is. On clean data with a defined process it removes hours; on a dirty database it produces wrong actions at scale, addressed personally, in your name.

**Contents:** [The Order Of Operations](#the-order-of-operations) · [What To Automate](#what-to-automate) · [What Never To Automate](#what-never-to-automate) · [Email Logging](#email-logging) · [Calendar](#calendar) · [Forms And Inbound](#forms-and-inbound) · [Enrichment](#enrichment) · [Webhooks And Two-Way Sync](#webhooks-and-two-way-sync) · [Workflow Rules That Survive](#workflow-rules-that-survive) · [The Automation Inventory](#the-automation-inventory) · [When It Misfires](#when-it-misfires)

**Before switching anything on**, read `## System` in `~/Clawic/data/crm/memory.md` for what is already running and who owns it, and `## Data Health` for the last hygiene pass. An automation built on a database that has not been deduped will send the same person three messages (`hygiene.md`).

## The Order Of Operations

Never out of order, because each step makes the next one safe:

1. **Do it by hand, twenty times.** The rule you would automate is not knowable before that.
2. **Dedupe and bounce-sweep** (`hygiene.md`).
3. **Automate detection** — lists, alerts, flags. Zero blast radius, most of the value.
4. **Automate record-keeping** — logging, field defaults, stage timestamps.
5. **Automate outbound last, narrowly**, and only where a wrong send is survivable.

Most of the benefit lands at step 3. Most of the damage lands at step 5.

## What To Automate

| Automate | Why it is safe | Watch |
|---|---|---|
| Overdue and stalled lists | Read-only; it is the ritual's input (`followup.md`) | Cap the list length or it stops being read |
| Renewal and next-step reminders | Dates you already agreed | Route them somewhere a human actually looks |
| Stage-entered timestamps, `updated`, `created` | Machine data, no judgment | Never let an automation change a stage |
| Field defaults and required-field validation | Prevents dirt at entry (`hygiene.md`) | Defaults that are wrong more than half the time get typed over — or worse, accepted |
| Duplicate check on create | The highest-value automation in a CRM | Match on the identity key, not on name |
| Logging inbound email metadata | Removes the friction that kills adoption (`adoption.md`) | Bodies are a privacy decision, not a convenience one |
| Form → contact with source and consent timestamp | Captures the lawful basis at the only moment it exists (`privacy.md`) | Deduplicate against existing records; forms are a duplicate factory |
| Weekly digest of the six numbers | Keeps the ritual fed (`metrics.md`) | A digest nobody opens is a reason to delete a metric |

## What Never To Automate

- **Stage changes.** A stage is a claim about the buyer; a rule that advances deals on activity guarantees an inflated pipeline (`pipeline.md`).
- **The first touch of a tier-A relationship**, or any message to someone who knows you personally (`followup.md`).
- **Deletion.** Ever. Archive rules are fine; automated deletion turns one bad condition into unrecoverable loss.
- **Merges**, beyond exact-identity-key matches. A fuzzy auto-merge destroys two histories silently (`hygiene.md`).
- **Sending to anything that has not passed the suppression check** (SKILL.md Rule 8).
- **Lead scoring that changes who gets contacted** before ~20 closed deals exist to build the score from (`schema.md`).

## Email Logging

The `email_logging` variable picks one of three, and the trade is privacy against completeness.

| Mode | How | Cost |
|---|---|---|
| `manual` | One line typed after the conversation | Highest quality, lowest coverage; fails in busy weeks |
| `bcc` | A per-account BCC address that files the message against the contact | Good coverage, zero setup risk, opt-in per message. **The BCC address is a credential** — anyone holding it can write records (`memory-template.md`) |
| `sync` | Inbox integration pulls all mail matching known contacts | Complete and unreadable, and it ingests personal correspondence and third parties who never consented (`privacy.md`) |

If `sync` is chosen: limit it to the addresses of known contacts, exclude personal folders, and store metadata (who, when, subject) rather than bodies unless a body is the record of a decision. "Log everything" is a decision about other people's mail, not just your own.

## Calendar

- **A meeting is not an interaction until it happened.** Auto-log from the calendar *after* the end time, never on acceptance, or the log fills with cancelled meetings.
- Attendee email addresses are the highest-yield contact source there is — auto-create external attendees as rows in the shared `contacts.md`, with tier C and source `meeting` in `## People`, and let the human promote them.
- Keep the meeting's **next step in the CRM, not the calendar invite**. Invites are unsearchable six weeks later.
- Booking links write the deal's next step and its date automatically; that single wire removes the most commonly forgotten field (`pipeline.md`).

## Forms And Inbound

- Capture `source`, the page, and the **consent timestamp** at submission — the only moment the lawful basis exists (`privacy.md`).
- **Dedupe on submit.** A returning visitor filling the form again is the single largest duplicate source in inbound-heavy CRMs.
- Route to a person with a dated next step, not to a queue. An inbound lead's response-time sensitivity is measured in hours, and a queue with no owner is a lead with no owner.
- Spam protection before automation: form spam that creates records and triggers sequences means your CRM is now emailing bots and damaging your sending reputation.

## Enrichment

- **Dedupe before enriching** (SKILL.md Traps): enriching four copies costs four credits and produces four disagreeing records.
- Enrich **company-level** attributes freely (size, sector, domain, technology). Personal contact details are the risky end (`privacy.md`).
- Store the **source and date** of every enriched field. Vendor data ages exactly like your own, and you cannot correct what you cannot attribute.
- Never let enrichment overwrite a value confirmed by an interaction. A human-confirmed field always outranks a vendor's guess — encode this as a merge rule, not as a hope (`hygiene.md`).

## Webhooks And Two-Way Sync

Two-way sync is where most CRM automation projects break. The failure modes are specific:

- **Loops**: system A writes to B, B's webhook writes back to A, forever. Break with an origin marker on every write and a rule to ignore your own.
- **Conflicts**: both sides edited the same field. Decide the winner *before* building — usually "the system of record wins" (SKILL.md Rule 1), and the other side is read-only for that field.
- **Idempotency**: every webhook delivery can arrive twice; every retry after a timeout can create a duplicate. Upsert on the identity key or an event id, never blind insert (`import.md`).
- **Ordering**: webhooks arrive out of order, so an update can land before the create. Handle the missing-parent case explicitly rather than dropping the event.
- **Rate limits**: a bulk edit fires one webhook per record and will exhaust a per-second quota. Queue and back off.
- **Silent failure**: the sync stops and nothing tells you for six weeks. Every integration needs a heartbeat — a last-sync timestamp somebody looks at, ideally as a `## Due` row.

Prefer one-way sync in the direction of the record of truth. Two-way is a maintenance commitment, not a setting.

## Workflow Rules That Survive

- **One trigger, one action, one owner.** Chained rules that trigger each other are unreadable within a quarter.
- **Name the rule for what it does and when**, not for the project that created it: `stalled-deal-alert-21d`, not `automation-3`.
- **Every rule has an off switch someone knows about**, and a note of what breaks when it is off.
- **Test on a scratch record**, then on five real ones, then on the database.
- **Review the whole set quarterly**; delete anything that has not fired, or that nobody can explain. Rules whose author left are the most expensive thing in a CRM.

## The Automation Inventory

Keep it in `## System`, or in `artifacts/automations.md` once it passes about ten entries. One line each:

`<name> · trigger · action · owner · last verified · what breaks if off`

Without this, the answer to "why did that email go out" takes an afternoon, and the answer to "can we turn this off" is nobody knows.

## When It Misfires

1. **Turn it off first**, then diagnose. A running rule keeps producing rows while you investigate.
2. **Scope the damage by the batch tag or the timestamp window** — this is why every automated write carries one (`import.md`).
3. **Reverse from the backup, not by hand** (SKILL.md Rule 9).
4. **If messages went out**: acknowledge to the recipients affected, add anyone who complained to `do-not-contact.md`, and check the bounce and complaint rate before sending anything else (`hygiene.md`).
5. **Write the incident into `## Data Health`** with counts, and the fix into the rule's inventory line.

**After any integration change**, write to `## System` in `~/Clawic/data/crm/memory.md`: what is connected, in which direction, who owns it, and the credential's **pointer** — `env:HUBSPOT_TOKEN`, never the token (`memory-template.md`). Add the sync heartbeat and the quarterly rule review to `## Due`, and move the inventory to `artifacts/automations.md` with its `## Boxes` line once it outgrows the section.
