---
name: Calendar Planner
slug: calendar-planner
version: 1.0.0
homepage: https://clawic.com/skills/calendar-planner
description: Plan work and life across Google Calendar, Outlook, Apple Calendar, and CalDAV with CLI adapters, conflict repair, and weekly reviews.
changelog: "Initial release with multi-calendar CLI playbooks, Life Grid planning rules, and local scripts for merge, guard, and weekly review workflows."
metadata: {"clawdbot":{"emoji":"C","requires":{"bins":["python3","jq"]},"os":["linux","darwin","win32"],"configPaths":["~/calendar-planner/"]}}
---

# Calendar Planner

Calendar planner for work, family, health, travel, deep work, and recovery across multiple command-line calendar adapters.

## Setup

On first use, read `setup.md` for integration guidelines. Answer the immediate planning question first, ask before creating `~/calendar-planner/`, and ask before writing to any calendar or sending invites.

## When to Use

User needs calendar planning, schedule repair, weekly planning, time blocking, meeting triage, family logistics, appointment placement, or multi-calendar cleanup. Use when the real job is reconciling commitments and constraints across Google Calendar, Outlook, Apple Calendar, and CalDAV from CLI-capable tools.

This skill should return one defended plan, explicit trade-offs, and a safe action sequence. It is stronger than generic scheduling help when calendars disagree, priorities collide, or the user needs a whole-week repair instead of one more event.

## Architecture

Local continuity is optional and only created with user consent.

```text
~/calendar-planner/
├── memory.md        # User-stated planning rules and activation preferences
├── calendars.md     # Provider map, calendar names, and write boundaries
├── rules.md         # Buffers, focus rules, recurring constraints
├── plans.md         # Current week plans and reschedule decisions
└── inbox.md         # Loose commitments that still need placement
```

## Quick Reference

Load only what improves the current planning decision. Start with protocol and commands; add memory only if the user wants continuity.

| Topic | File |
|-------|------|
| Setup and activation | `setup.md` |
| Optional continuity memory | `memory-template.md` |
| Life Grid planning method | `planning-protocol.md` |
| Domain-specific planning heuristics | `life-domains.md` |
| CLI adapter recipes | `commands.md` |
| Merge normalized event exports | `calendar_merge.py` |
| Audit overlaps and buffer failures | `calendar_guard.py` |
| Generate weekly planning summary | `week_plan.py` |

## Requirements

Use the lightest adapter that matches the user's stack. Only install the provider tools needed for the current workflow.

| Need | CLI / Tool | Notes |
|------|------------|-------|
| Google Calendar | `gcalcli` | Uses Google Calendar API via the user's own OAuth client |
| Outlook / Microsoft 365 | Microsoft Graph PowerShell | Use delegated calendar scopes only |
| Apple Calendar | `osascript` | Automates Calendar.app on macOS |
| CalDAV and iCloud sync | `khal` plus `vdirsyncer` | Sync locally, then plan from local state |
| Local analysis | `python3` and `jq` | Required for merge, guard, and week review scripts |

## Core Rules

### 1. Start from the decision, not the CRUD action
- First answer what should stay, move, cancel, protect, or defer.
- Ask only for facts that change placement: hard deadline, travel time, attendee constraints, or protected hours.
- Use `planning-protocol.md` to convert messy requests into a placement decision.

### 2. Separate hard commitments from flexible blocks
- Classify every item as hard, flexible, hold, prep, travel, or recovery before reshuffling the calendar.
- Flexible blocks can move; hard commitments do not move without explicit approval.
- Use `life-domains.md` to prevent work tasks from silently overrunning family, health, or sleep constraints.

### 3. Merge all visible calendars before moving anything
- Read every in-scope calendar first, including shared or family calendars only if the user put them in scope.
- Treat hidden calendars as risk, not as empty time.
- Use `calendar_merge.py` when you have multiple normalized exports and need one timeline.

### 4. Protect buffers, prep, and follow-through
- Add setup, commute, context switch, follow-up, and decompression time around meetings and appointments.
- A schedule with no buffers is fake capacity.
- Use `calendar_guard.py` to catch overlaps, short gaps, and overloaded days before proposing changes.

### 5. Writes require explicit approval and narrow scope
- Ask before creating, updating, deleting, or sending invites through any adapter.
- Default to a draft plan or dry-run command sequence first.
- Keep read-only and write-enabled calendars separate in the local continuity notes if the user opts into continuity.

### 6. Keep memory explicit and minimal
- Save only user-stated rules, recurring commitments, protected hours, and activation preferences.
- Do not store attendee lists, detailed event notes, or private descriptions unless the user asks for that continuity.
- Use `memory-template.md` only after the user agrees to local persistence.

### 7. End with an execution-ready plan
- Every answer should finish with chosen slot(s), remaining conflicts, follow-ups, or a weekly repair plan.
- If multiple options remain, rank them and explain the winner in one sentence.
- Use `week_plan.py` or the adapter recipes in `commands.md` when a terminal workflow makes the answer more reliable.

## Life Grid Protocol

See `planning-protocol.md` for the full method.

- Intake: capture the real outcome, not just the requested event.
- Map: place each item into hard, flexible, prep, travel, or recovery.
- Defend: protect non-negotiables before offering new slots.
- Repair: if the week is already broken, show what to move, cancel, or downgrade.
- Close: leave the user with one recommended plan and the exact next command or calendar action.

## Common Traps

- Solving only the meeting request -> school pickup, travel, medication, or focus constraints break later.
- Moving events before reading every in-scope calendar -> hidden conflicts and trust damage.
- Treating recurring blocks as either sacred or disposable by default -> brittle plans or calendar chaos.
- Packing meetings with no setup or recovery space -> fake capacity and late-day collapse.
- Writing to shared calendars without approval -> surprises other people and creates social debt.
- Saving too much private detail locally -> unnecessary privacy risk with no planning upside.

## External Endpoints

Only the adapter the user explicitly chooses should talk to a remote service. Use one provider path at a time so data movement stays understandable.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.googleapis.com/calendar/v3/* | event metadata for requested Google calendar reads or writes | Google Calendar operations through `gcalcli` |
| https://graph.microsoft.com/v1.0/* | event metadata for requested Outlook or Microsoft 365 reads or writes | Calendar operations through Microsoft Graph PowerShell |
| user-configured CalDAV server | event metadata for configured calendars | Calendar sync through `vdirsyncer` and local use through `khal` |

No other data is sent externally.

## Security & Privacy

**Data that stays local:**
- Optional planning memory in `~/calendar-planner/`
- Normalized event exports and review outputs produced by `calendar_merge.py`, `calendar_guard.py`, and `week_plan.py`
- Apple Calendar automation through Calendar.app on macOS

**Data that may leave your machine:**
- Calendar metadata sent through the Google, Microsoft, or CalDAV adapter the user explicitly chooses

**This skill does NOT:**
- Create, move, or delete calendar items without approval
- Send invites or update shared calendars silently
- Infer hidden rules from unrelated files or conversations
- Access email, contacts, or tasks unless the user explicitly expands scope

## Trust

By using this skill with Google Calendar, Microsoft Graph, or CalDAV adapters, calendar metadata is sent to those services through the configured CLI tools. Only install if you trust those providers and the local machine running the commands.

## Scope

This skill ONLY:
- Plans and audits schedules across user-approved calendars
- Produces dry-run commands, normalized planning files, and local review reports
- Persists minimal planning context after explicit user consent

This skill NEVER:
- Modifies its own skill file
- Auto-accepts invites or auto-reschedules people without approval
- Widens access from one calendar to another without confirmation
- Stores credentials in local memory files

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `daily-planner` - Daily plan shaping, sequencing, and realistic task placement.
- `schedule` - General scheduling workflows when the user does not need full calendar repair.
- `assistant` - Chief-of-staff style execution across tasks, messages, and planning.
- `productivity` - Focus systems, prioritization, and anti-overload operating rules.
- `remember` - Long-term continuity for user-stated constraints and recurring patterns.

## Feedback

- If useful: `clawhub star calendar-planner`
- Stay updated: `clawhub sync`
