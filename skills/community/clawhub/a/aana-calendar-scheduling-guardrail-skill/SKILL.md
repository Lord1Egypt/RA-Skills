# AANA Calendar Scheduling Guardrail Skill

Use this skill before an OpenClaw-style agent creates, updates, cancels, invites, or shares a calendar event.

This is an instruction-only skill. It does not install packages, run commands, write files, call services, persist memory, or schedule events on its own.

## Core Principle

Calendar changes affect other people. Before changing a calendar, verify attendees, timezone, date, duration, title, agenda, location, private notes, recurrence, and explicit approval.

## Required Checks

- exact action: create, update, cancel, invite, reschedule, or share availability
- exact attendees and whether they are internal or external
- timezone, date, start time, end time, duration, and recurrence
- title, agenda, location, conferencing link, and private notes
- whether attendee visibility or guest permissions expose private data
- whether the user approved the exact event change

## Calendar Risk Classes

Treat these as higher risk:

- external attendees, customer meetings, interviews, legal/medical/financial meetings, HR meetings, and executive meetings,
- group aliases, mailing lists, all-hands calendars, public calendars, and broad attendee lists,
- recurring meetings, cancellations, reschedules, and changes that notify attendees,
- private notes, internal agenda details, confidential links, interview feedback, account records, or personal data,
- time-sensitive meetings where timezone ambiguity can cause missed commitments.

## Attendee Rules

Do not create, update, or send invites when:

- attendees are inferred from context rather than explicitly named,
- a group alias may include a broader audience than intended,
- CC-like visibility, guest list visibility, or external guests expose private relationships,
- the event forwards private notes, hidden agenda content, or confidential links to attendees.

Ask before inviting external guests or broad groups.

## Time And Recurrence Rules

Verify timezone, date, duration, and recurrence before any calendar change. Do not assume local timezone when the user, attendees, or meeting context suggests multiple regions.

For recurring events, confirm whether the change applies to one occurrence or the full series.

## Review Payload

When using a configured AANA checker, send only a minimal redacted review payload:

- `calendar_action`
- `attendee_status`
- `time_status`
- `privacy_status`
- `approval_status`
- `calendar_risks`
- `blocker_reason`
- `safe_alternative`
- `recommended_action`

Do not include full calendars, private notes, meeting links, attendee contact details, or unrelated schedule data when a redacted summary is enough.

## Decision Rule

- If details are complete, low-risk, and explicitly approved, proceed.
- If attendees, timezone, date, duration, or recurrence are unclear, ask.
- If private notes, sensitive topics, external attendees, or broad invite lists are involved, narrow or request approval.
- If the action cancels, reschedules, or invites others, require explicit approval.
- If the request is unauthorized, deceptive, or exposes private data, block the calendar change.

## Output Pattern

```text
AANA calendar gate:
- Action: create / update / cancel / invite / reschedule / share_availability
- Attendees: exact / missing / ambiguous / external / group_alias
- Time: confirmed / missing / timezone_unclear / conflicting
- Privacy: clear / private_notes / sensitive / unknown
- Approval: approved / required / unclear / denied
- Decision: proceed / ask / narrow / request_approval / block
```
