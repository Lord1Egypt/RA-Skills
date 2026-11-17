# CRM Workflows & Relationship Management

Best practices for being an effective personal CRM assistant with Dex. These patterns help users nurture professional relationships systematically.

## Table of Contents

- [Outcome Workflow Contract](#outcome-workflow-contract)
- [Categorize or Reorganize a Network](#categorize-or-reorganize-a-network)
- [Turn Notetaker Output into CRM Actions](#turn-notetaker-output-into-crm-actions)
- [Audit and Clean Up a CRM](#audit-and-clean-up-a-crm)
- [Follow Up After an Event](#follow-up-after-an-event)
- [Run a Relationship Review](#run-a-relationship-review)
- [Prepare Multiple Meetings](#prepare-multiple-meetings)
- [Build a Target Contact List](#build-a-target-contact-list)
- [Meeting Prep Workflow](#meeting-prep-workflow)
- [Post-Meeting Follow-Up](#post-meeting-follow-up)
- [Calendar Coordination](#calendar-coordination)
- [Correspondence Research](#correspondence-research)
- [Web Research](#web-research)
- [Contact Organization Strategy](#contact-organization-strategy)
- [Note-Taking Best Practices](#note-taking-best-practices)
- [Follow-Up Cadences](#follow-up-cadences)
- [Network Nurturing Patterns](#network-nurturing-patterns)
- [Bulk Operations](#bulk-operations)

---

## Outcome Workflow Contract

Use the same operating pattern for broad, outcome-oriented requests:

1. **Define scope** — Resolve the goal, time window, timezone, source artifact, and whether archived contacts are included. Default to active contacts when the user does not mention archived records, and state that assumption.
2. **Inspect current state** — Read existing contacts, taxonomy, notes, reminders, calendar context, or email metadata before proposing changes.
3. **Build a dry run** — Show evidence, confidence, ambiguities, counts, and the exact records or fields that would change.
4. **Confirm writes** — Group related low-risk changes into one clear confirmation. Keep destructive or externally visible actions separately confirmed.
5. **Execute safely** — Re-resolve current IDs, use the smallest sufficient payloads, respect batch limits, and continue past isolated failures when safe. Treat a timed-out create as an unknown outcome: look for the new record before retrying unless the tool explicitly guarantees an identical retry is idempotent.
6. **Verify** — Re-read representative or changed records and report succeeded, skipped, ambiguous, and failed items.

Treat “analyze,” “recommend,” “audit,” “prepare,” and “show me” as read-only requests. Never turn a suggestion into a write without the user asking for that change. If the user says “all,” exhaust pagination and disclose any single-batch limits or truncation that prevent a complete result.

Prefer evidence-backed classifications. Never infer sensitive traits such as health, religion, ethnicity, sexual orientation, or political affiliation. Keep unsupported or conflicting cases in a review queue instead of forcing a category.

---

## Categorize or Reorganize a Network

Use this playbook for requests such as “categorize all my contacts,” “organize my network,” or “put everyone into useful buckets.”

1. **Inventory the taxonomy** — Page through tags and groups and list custom fields before proposing new ones.
2. **Choose the right structure**:
   - Use tags for non-exclusive attributes, sources, and contexts.
   - Use groups for cohorts, communities, organizations, or projects.
   - Use an autocomplete custom field for a controlled, usually mutually exclusive classification.
   - Check whether the proposed labels mix dimensions such as role, relationship type, source, or lifecycle; use tags or separate fields when more than one label can be true.
3. **Define the scope** — State active versus archived contacts and whether notes may be read as classification evidence.
4. **Pilot the taxonomy** — Classify a representative sample before the full network when categories are new or subjective.
5. **Classify with evidence** — Use explicit contact fields, existing taxonomy, and only the minimum note context needed. Record a short reason and separate high-confidence, needs-review, and unclassified contacts.
6. **Preview the changes** — Show new taxonomy items, assignment counts, ambiguous examples, and any proposed removals.
7. **Apply after approval** — Create only missing definitions, batch memberships or field values within tool limits, then verify counts and a sample of changed contacts.

Default to additive organization. Do not remove existing tags, groups, or custom-field values merely because they do not fit the new taxonomy. Require a separate preview and confirmation for normalization or removals. Do not treat a keyword mention as proof that a person belongs to a category.

For a complete-network run, checkpoint progress by page or batch so partial failures can be retried without duplicating successful work. Summarize large previews in chat and preserve the complete proposed assignment manifest as a machine-readable artifact when the execution surface supports one; do not dump private note excerpts into the preview.

---

## Turn Notetaker Output into CRM Actions

Use this playbook for a pasted summary, transcript, or exported artifact from a notetaker.

1. **Acquire the source** — Use the attached or pasted artifact. If no connector or artifact is available, ask the user to attach, paste, or export it; never imply direct access to the notetaker.
2. **Establish meeting identity** — Determine the meeting time, timezone, title, and candidate attendees. Calendar data can help resolve the event, but an invite does not prove attendance.
3. **Resolve people** — Match external attendees by exact email first, then name plus company. Exclude the user, rooms, bots, and recording services. Ask before linking an ambiguous person or creating a missing contact.
4. **Check for duplicates** — Inspect recent notes around the meeting time and topic before creating another note.
5. **Separate the proposed outputs**:
   - Shared discussion, decisions, and context → one concise note linked with `contact_ids`.
   - Contact-specific or private context → a separate note only for the relevant person.
   - Explicitly stated role, company, or contact-detail changes → proposed contact updates.
   - Future-effective or incomplete changes → note the context and optionally propose a reminder; do not overwrite current fields early.
   - Clear commitments with an owner and due date → proposed reminders.
   - A confirmed interaction with an existing cadence → optional keep-in-touch completion.
6. **Preview everything together** — Show note content and linked contacts, field deltas, reminder text/dates, and cadence completions.
7. **Write after approval** — List note types, create the note or notes with the actual `event_time`, then apply separately approved updates and reminders.
8. **Verify** — Re-read created notes and changed contacts; report unresolved attendees or action items.

Summarize rather than storing a verbatim transcript. Distinguish facts from interpretation, preserve action-item ownership, and do not invent due dates. Omit unrelated sensitive discussion and third-party details that do not help the user manage the relationship.

Resolve relative dates such as “Friday” from the meeting timestamp and timezone, then show the derived date in the preview. When the source gives only a range such as “next week,” ask for a date or present a clearly labeled suggestion for confirmation.

When several people attended the same meeting, prefer one shared note unless the content differs materially by person. Never duplicate the full summary onto every contact as separate notes.

---

## Audit and Clean Up a CRM

Use this playbook for “clean up my CRM,” “find problems,” or “make my contacts consistent.”

1. Inventory active and, when requested, archived contacts separately.
2. Review potential problems:
   - Duplicate emails or phone numbers and likely duplicate names
   - Missing names, contact methods, company, role, or location
   - Contacts outside the agreed taxonomy
   - Near-duplicate tag, group, or custom-field definitions
   - Old interactions, contacts with no interaction date, and open reminders
   - Conflicting information across fields and recent notes
3. Divide findings into:
   - **Safe suggestions** — formatting or additive organization with clear evidence
   - **Reversible actions** — archive, restore, or additive taxonomy changes
   - **Needs judgment** — ambiguous identity, conflicting facts, or subjective categorization
   - **Destructive actions** — merge, delete, remove membership, or delete a taxonomy definition
4. Present counts and exact records before changing anything.
5. Apply only approved categories of fixes and verify each class of change.

Do not merge solely because names match. Do not replace missing values with guesses, erase conflicting values, or convert a cleanup request into deletion. Prefer archive over delete and preserve unsupported cases for review.

---

## Follow Up After an Event

Use this playbook for a conference, dinner, cohort, class, or other multi-person event:

1. Obtain the roster from a calendar event, attached list, spreadsheet, or user-provided names.
2. Resolve existing contacts by exact email first and keep ambiguous names separate.
3. Exclude the user, rooms, mailing lists, bots, and service accounts.
4. Preview missing contacts before batch creation; do not create a contact from a name alone unless the user approves that limited record.
5. Reuse or propose an event group/tag using the user’s existing naming conventions.
6. Create one shared event note for common context, then add individual notes only where the interaction differed.
7. Propose specific reminders for promised follow-ups. Do not invent commitments or due dates.
8. Verify the created contacts, memberships, notes, and reminders.

Keep contact creation, organization, note logging, and reminders visible as separate deltas even when the user confirms them together. Dex email search is read-only; offer drafts as text when useful but never imply that Dex sent outreach.

---

## Run a Relationship Review

Use this playbook for weekly reviews, neglected-network scans, or “who should I reach out to?”

1. Confirm the relationship segment, inactivity threshold, and time horizon.
2. Start with `dex_list_upcoming_reminders_and_birthdays` when the question is about a window ("this week", "the next month"). One call returns the birthdays, open reminders, and keep-in-touch contacts due in it — already the answer to "who should I reach out to this week?". Widen with `days: 30`. Note it excludes ALREADY-overdue reminders; add `dex_list_reminders` with `is_overdue: true` when the review is meant to catch up rather than look ahead.
3. Use structured filters to shortlist contacts by explicit criteria beyond cadence. Review contacts with no recorded interaction separately because date filters exclude them.
4. Inspect only the notes and reminders needed to understand the shortlist.
5. Weigh relationship importance, open commitments, current opportunity context, existing cadence, and recent email/calendar evidence when requested.
6. Return a prioritized list with:
   - Why the contact is relevant now
   - Last known context
   - Open commitment or reminder
   - Suggested next action
   - Confidence or missing information
7. Keep the review read-only unless the user asks to create reminders, change cadence, or archive contacts.

Do not rank people from inactivity alone or treat a missing date as neglect. Avoid presenting speculative relationship quality as fact.

---

## Prepare Multiple Meetings

Use this playbook for “prepare my day,” “brief me for this week,” or another calendar window:

1. List calendar events for the exact timezone-aware window.
2. Identify meetings that benefit from relationship context; skip personal blocks and events without relevant external attendees.
3. Resolve attendees to Dex contacts by email where possible.
4. Fetch event details, contact history, reminders, and bounded email metadata only as needed.
5. Prioritize near-term or high-impact meetings if the window is too large for full enrichment.
6. Produce a chronological agenda with:
   - Time, account, location, and join details
   - Attendees and unresolved identities
   - Relationship context and last relevant interaction
   - Open commitments
   - Suggested talking points
   - Missing preparation inputs

This workflow is read-only by default. Do not reschedule events, change attendees, create reminders, or update contacts unless the user separately requests those changes.

---

## Build a Target Contact List

Use this playbook for requests such as “find investors near New York,” “build an advisor shortlist,” or “group founders I know in climate.”

1. Translate the request into explicit criteria and distinguish required filters from preferences.
2. Use `dex_filter_contacts` for structured AND conditions and `dex_search_contacts` with `near` for geographic proximity plus an optional keyword.
3. For OR logic, run separate bounded searches or filters and deduplicate by contact ID.
4. Review supporting contact details only for the shortlist.
5. Return ranked candidates with evidence, caveats, and unresolved criteria.
6. Create a group, apply a tag, set a field, or add reminders only after showing the exact members and changes.

Do not claim a filter is exhaustive when it used a bounded single-batch search. Avoid inferring investment focus, expertise, or intent without explicit evidence.

---

## Meeting Prep Workflow

When a user says "I have a meeting with X" or "Prep me for a call with X":

1. **Search** for the contact by name
2. **Get full details** with `include_notes: true` for recent interaction history
3. **Check reminders** to find any pending follow-ups related to this contact
4. **Fetch the calendar event** when the user wants live attendee, conferencing, or recurrence details
5. **Search recent correspondence** when email context would improve the brief
6. **Check web research** with `dex_get_contact_research`; if nothing is stored and the user wants public background, offer `dex_research_contacts` (paid, takes a minute or more)
7. **Synthesize a brief** covering:
   - Who they are (role, company, relationship context)
   - Last interaction (when, what was discussed)
   - Pending items (action items from last meeting, open reminders)
   - Shared context (groups in common, tags, custom field data)
   - Meeting logistics and attendees, when requested
   - Relevant recent email threads, identified as snippets rather than full bodies
   - Suggested talking points based on history

**Example output format:**

```
## Meeting Brief: Jane Doe
VP Engineering at Acme Corp | Tagged: Investor, YC Batch

**Last Contact:** Feb 15 — Coffee meeting
- Discussed their Series A timeline (targeting Q3)
- You offered to intro them to your LP contacts

**Pending:**
- Reminder (Mar 1): Send LP intro email
- Open action: Share your fundraising deck

**Suggested Topics:**
- Follow up on LP intro status
- Ask about Q3 fundraising progress
- Discuss technical partnership opportunity
```

---

## Post-Meeting Follow-Up

After a user logs a meeting or says "I just met with X":

1. **Create a note** on the contact's timeline with:
   - Appropriate note type (Meeting, Call, Coffee, etc.)
   - `event_time` set to when the meeting happened
   - Content capturing key discussion points and action items
2. **Create reminders** for any follow-up actions
3. **Update contact details** if new info was shared (new role, company change, etc.)
4. **Apply tags/groups** if the relationship context changed
5. **Complete keep-in-touch cadence** with `dex_complete_keep_in_touch` only when the interaction actually occurred

---

## Calendar Coordination

Use calendar tools as an external-state workflow:

1. List or search events across connected accounts
2. Reuse the event's returned `email` as `account_email`; for create/update/delete, also use `account_provider` when one address exists under both providers
3. Confirm the exact event, account, schedule, and attendee impact before a write
4. For updates, fetch current state first because `attendees` replaces the full list
5. State clearly when a recurring-series ID will affect every occurrence

For timed events, provide both endpoints with explicit offsets and an IANA timezone. For all-day events, remember that `end_date` is exclusive. Creating an event may send invitations; deleting an organized event may cancel it for everyone.

`dex_update_calendar_event` cannot move an event to a different connected account. A cross-account transfer is a two-write workflow: fetch the original, confirm and create a faithful replacement on the target account, then separately confirm deletion of the original. Warn that organizer identity, attendee RSVP state, conferencing data, and provider notifications may not carry over unchanged.

---

## Correspondence Research

Use `dex_search_emails` to find live message metadata across connected Google and Microsoft accounts:

- Search with plain names, companies, domains, or topics
- Add explicit `after` and `before` bounds for recency-sensitive questions
- Do not use provider operators such as `from:` or `to:`
- Describe results as metadata and snippets, not full message bodies
- Do not offer to send email; Dex only searches correspondence

---

## Web Research

Dex Research produces a cited note about a contact from the public web — who they are, current focus, background, interests — plus structured findings (LinkedIn, website, email, phone):

- Read first: `dex_get_contact_research` returns stored notes for up to 10 contacts at no cost
- Run second: `dex_research_contacts` researches up to 5 contacts per call. It is paid and slow (a minute or more per contact, run in parallel), so confirm before researching more than a couple of contacts and chunk larger sets
- Notes under 30 days old come from cache; use `force: true` only on an explicit request for a fresh run
- Quote bullets with their `[[n]]` citations resolved into `sources`, and flag `identity_confidence` below `high`
- Empty `linkedin` / `website` fields are filled by the run itself (`applied`); `pending` email and phone findings need the user's confirmation before `dex_update_contact`
- `in_progress` means a run is already underway for that contact — read it back later rather than running again

---

## Contact Organization Strategy

Guide users toward a consistent organizational system:

### Tags — Use for Attributes and Contexts

Tags are flat labels that cut across groups. Effective tag patterns:

- **How you met**: "Conference 2026", "LinkedIn", "Warm Intro", "College"
- **Professional role**: "Investor", "Founder", "Engineer", "Designer"
- **Relationship quality**: "Close Friend", "Acquaintance", "Dormant"
- **Action-oriented**: "Needs Follow-up", "Potential Hire", "Reference"

### Groups — Use for Relationship Clusters

Groups represent collections of related contacts. Effective group patterns:

- **Organizations**: "Acme Corp Team", "YC W26 Batch"
- **Personal circles**: "Book Club", "Running Group", "Dinner Crew"
- **Project-based**: "Board Members", "Advisory Council", "Launch Partners"
- **Networking**: "SF Tech Scene", "NYC Finance"

### Custom Fields — Use for Structured Data

When users track specific data points across contacts:

- **Pipeline tracking**: "Deal Stage" (autocomplete: Prospect → Closed)
- **Dates**: "Last Contract Date", "Anniversary" (datepicker)
- **Categories**: "Expertise Area", "Investment Focus" (autocomplete)
- **Free text**: "Referral Source", "Internal Notes" (input)

---

## Note-Taking Best Practices

Effective CRM notes capture information that future-you will need:

### Structure

```
[Key discussion points]
[Decisions made]
[Action items — who owes what]
[Personal context worth remembering]
```

### What to Capture

- **Action items** with clear ownership ("I will send the deck by Friday")
- **Decisions made** ("Agreed to move forward with Option B")
- **Personal context** ("Mentioned daughter starting college in fall")
- **Relationship signals** ("Seemed excited about collaboration", "Mentioned they're job hunting")
- **Next steps** ("Reconnect after their board meeting in April")

### What to Skip

- Information already in the contact record (job title, company — update the contact instead)
- Trivial logistics ("Met at Starbucks on 5th Ave")
- Verbatim transcripts — summarize the key points

### Note Types

Always use the most specific note type available:

- **Meeting** — In-person or video meetings
- **Call** — Phone or voice calls
- **Coffee** — Informal catch-ups
- **Note** — General observations, research notes, or async context

---

## Follow-Up Cadences

Help users establish systematic follow-up patterns:

### Suggested Cadences by Relationship Type

| Relationship                   | Cadence         | `keep_in_touch` value |
| ------------------------------ | --------------- | --------------------- |
| Close professional contacts    | Every 2-4 weeks | `14 days` or `1 mon`  |
| Active networking contacts     | Monthly         | `1 mon`               |
| Investors / Board members      | Monthly         | `1 mon`               |
| Dormant but valuable           | Quarterly       | `3 mons`              |
| Seasonal (holidays, birthdays) | Yearly          | `1 year`              |

### Setting Up Relationship Cadence

When a user wants to "stay in touch" with someone:

1. Ask how often they want to check in
2. Set `dex_update_contact.keep_in_touch` to the matching Dex interval
3. After a real interaction, use `dex_complete_keep_in_touch` so the cadence resets
4. Use `snooze_days` only to defer without recording a touch

Use `never` when the user explicitly does not want cadence reminders and `unset` to clear the cadence choice.

### Setting Up a Recurring Task

Use a recurring reminder when the user is tracking a specific repeated action rather than a general relationship cadence:

1. Ask how often the task should repeat
2. Create a reminder with the appropriate `recurrence`
3. Set `due_at_date` to the next desired due date
4. Link it to the contact with `contact_id` when applicable

**Example** (`dex_create_reminder`):

```json
{
  "text": "Monthly check-in — see how the product launch went",
  "due_at_date": "2026-04-01",
  "contact_id": "c1",
  "recurrence": "monthly"
}
```

---

## Network Nurturing Patterns

### The "Touch Base" Flow

When a user wants to re-engage dormant contacts:

1. Use `dex_filter_contacts` with `last_interaction_before` and any requested tag, group, company, or location criteria
2. Page through all matching contacts
3. Review contacts with no recorded interaction separately because date bounds exclude them
4. For each, check existing notes for context
5. Suggest a personalized reason to reach out based on their history

For cleanup requests, do not equate inactivity with “clearly stale.” Review open reminders, starred status, active opportunity/context signals, and—when useful—recent email/calendar metadata. Present exact archive and retain lists with reasons, then obtain confirmation before `dex_archive_contacts` or cadence changes. Never substitute `dex_delete_contacts` for a request to archive.

### The "Batch Organize" Flow

When a user wants to organize their CRM:

1. List all existing tags and groups to understand current structure
2. Filter contacts by category, company, tag, group, or custom field
3. Create new tags/groups as needed
4. Bulk assign using `dex_add_tags_to_contacts` / `dex_add_contacts_to_group`

### The "Duplicate Cleanup" Flow

When a user suspects duplicates:

1. Search by name fragments to find potential duplicates
2. Get full details of suspected duplicates to compare
3. Present differences to the user
4. Merge with user confirmation
5. Read `mergedContactIds` from the response because Dex keeps the oldest record, not the first input ID

---

## Bulk Operations

Several tools support batch operations for efficiency:

- **Tags**: `dex_add_tags_to_contacts` / `dex_remove_tags_from_contacts` — apply or remove tags on multiple contacts at once
- **Groups**: `dex_add_contacts_to_group` / `dex_remove_contacts_from_group` — manage group membership in bulk
- **Custom Fields**: `dex_set_custom_field_values` — set field values on multiple contacts
- **Create**: `dex_create_contact` — create up to 100 contacts per call
- **Archive/Restore**: `dex_archive_contacts` — reversibly change up to 500 contacts per call; archiving more than 20 in one call requires `confirm: true` and a matching `expected_count`
- **Delete**: `dex_delete_contacts` — remove multiple contacts
- **Merge**: `dex_merge_contacts` — merge multiple duplicate groups simultaneously

When performing bulk operations, resolve current IDs, show the intended count and delta, process within tool limits, and explicitly confirm destructive operations. Prefer archive over delete when the user may need recovery.
