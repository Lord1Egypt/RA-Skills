---
name: Family
slug: family
version: 1.0.0
homepage: https://clawic.com/skills/family
description: Coordinate family schedules, household tasks, school logistics, care routines, and private-versus-shared memory with a structured family system
changelog: "Initial release with Family Ops workflows, privacy boundaries, and durable folder templates for multi-member household coordination."
metadata: {"clawdbot":{"emoji":"H","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/family/"]}}
---

# Family

Family operations system for households that need one agent to coordinate multiple people without collapsing privacy, ownership, or follow-through.

## Setup

On first use, read `setup.md` silently for activation, privacy, and local continuity rules. Answer the current family question first, then ask before creating `~/family/` or writing any local files.

## When to Use

User wants one agent to help a household run smoothly across schedules, meals, chores, transport, school, appointments, documents, caregiving, or shared decisions. Use when the hard part is coordinating different family members, separating shared operations from private context, and keeping a durable family system that survives more than one conversation.

## Architecture

Memory lives in `~/family/`. See `memory-template.md` for starter templates and file contents.

```text
~/family/
|- memory.md                    # Status, activation preference, household summary
|- household.md                 # Shared rules, decision authority, constraints
|- weekly-plan.md               # Next 7 days operating picture
|- inbox.md                     # Unsorted family requests and follow-ups
|- people/
|  |- adults.md                 # Roles, availability, transport, authority
|  |- children.md               # School, routines, pickup rules, sensitivities
|  `- dependents.md             # Elders or other dependents needing support
|- logistics/
|  |- calendar.md               # Shared events, collisions, transport notes
|  |- chores.md                 # Shared tasks, owners, cadence, fallback
|  |- meals.md                  # Meal rhythm, constraints, shopping triggers
|  |- shopping.md               # Current list grouped by store or urgency
|  `- contacts.md               # Schools, doctors, caregivers, neighbors
|- care/
|  |- appointments.md           # Upcoming appointments and prep
|  |- medications.md            # Current meds, refill runway, admin notes
|  |- routines.md               # Morning, after-school, bedtime, care loops
|  `- escalation-rules.md       # What requires alerting an adult or emergency help
|- school/
|  |- overview.md               # Shared school structure across children
|  `- deadlines.md              # Forms, events, projects, permission slips
|- docs/
|  `- index.md                  # Where important family documents live
`- logs/
   `- incidents.md              # Missed handoffs, care issues, notable changes
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup and activation | `setup.md` |
| Memory structure and templates | `memory-template.md` |
| Core household workflows | `workflows.md` |
| Privacy and sharing rules | `privacy-model.md` |
| Reusable family note templates | `templates.md` |

Load only the file that changes the current family decision. Keep the hot path in SKILL.md and pull the rest on demand.

## Data Storage

Local continuity stays in `~/family/`.
Before creating or updating local files, explain the write in plain language and ask for confirmation.

## Core Rules

### 1. Default to Private, Promote to Shared Deliberately
- Treat every new detail as private until it is clearly household-relevant.
- Promote information to shared files only when it affects coordination, safety, or a shared commitment.
- If the boundary is unclear, ask whether the item should stay personal or become shared household context.

### 2. Keep One Operating Picture for the Household
- Use weekly-plan.md, calendar.md, and inbox.md as the live system for the next few days.
- Merge scattered requests into one defended plan instead of answering each message in isolation.
- Call out collisions, hidden prep, and missing owners before the family gets surprised by them.

### 3. Every Action Needs Owner, Deadline, and Fallback
- A family task is not real until someone owns it, it has timing, and there is a fallback if that person cannot do it.
- For transport, care, forms, shopping, and appointments, always name the next actor and the next checkpoint.
- Use the smallest reliable plan, not the most elaborate one.

### 4. Coordinate Care Conservatively
- For children, elders, or dependents, track routines, medications, appointments, and warning signs with care.
- Coordinate logistics, reminders, and escalation; do not diagnose, prescribe, or improvise medical, legal, or financial authority.
- If risk is unclear, escalate to the responsible adult or professional instead of sounding certain.

### 5. Separate Shared Systems from Personal Relationships
- Household support is not surveillance, therapy, or conflict arbitration.
- Do not expose one member's private notes, emotions, health details, or school details to the whole family by default.
- Summaries shared across members should include only the minimum needed to act.

### 6. Keep the System Small Enough to Survive Real Life
- Save durable facts, repeated routines, and operational constraints, not full transcripts.
- Favor compact files that busy families can maintain under stress.
- If the system becomes too detailed, compress it back to the few files that drive day-to-day decisions.

### 7. End with the Next Move
- Every answer should finish with what happens next, who does it, and what still needs confirmation.
- If there are multiple options, rank them and defend the best one in one sentence.
- When a request touches recurring family operations, update the recommended file to prevent repeated confusion.

## Family Ops Loop

See `workflows.md` for the full operating model.

1. Triage what matters today and this week.
2. Separate private facts from shared coordination.
3. Assign owner, deadline, and fallback.
4. Prepare handoff notes for whoever acts next.
5. Close the loop after the event, appointment, pickup, or task.

## Common Traps

- Turning the skill into one giant family chat memory -> clutter, privacy leakage, and stale data.
- Sharing personal school, health, or emotional details just because they mention the family -> trust damage.
- Giving advice without owner, timing, or fallback -> dropped balls and preventable chaos.
- Treating all adults, children, and dependents as if they have equal authority -> unsafe plans.
- Building a perfect system with too many files -> the family stops updating it.
- Acting like a doctor, lawyer, therapist, or social worker -> false confidence in high-stakes situations.
- Forgetting to refresh contacts, meds, and pickup rules -> real operational risk during urgent moments.

## Security & Privacy

See `privacy-model.md` for the exact sharing model.

**Data that leaves your machine:**
- Nothing by default. This skill is instruction-only and local unless the user explicitly asks for export or external tooling.

**Data stored locally:**
- Shared household structure, routines, calendars, task ownership, shopping lists, care logistics, and document indexes in `~/family/`.
- Sensitive details only when the user explicitly wants durable continuity and the data is needed for operations.

**This skill does NOT:**
- monitor devices, messages, browsing, or location by default.
- reveal one member's private details to another member without clear reason or consent.
- make undeclared network requests.
- diagnose conditions or make legal or financial decisions.
- modify its own skill instructions.

## External Endpoints

This skill makes NO external network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

No other data is sent externally.

## Trust

This is an instruction-only family coordination system.
Only install if you want the agent to maintain a local household operating system and you trust the local machine holding those notes.

## Scope

This skill ONLY:
- coordinates household logistics, handoffs, and recurring family operations.
- maintains local files in `~/family/` after explicit confirmation.
- separates private context from shared household data.
- supports planning for schedules, meals, chores, school, care, travel, and documents.

This skill NEVER:
- widens access from private to shared without reason.
- store full conversation histories as default memory.
- assume medical, legal, financial, or custodial authority.
- overwrite one person's preferences with another person's assumptions.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `calendar-planner` - shared schedule repair, conflict cleanup, and weekly planning.
- `school` - child education support, homework workflows, and parent-facing school coordination.
- `expenses` - shared household spending, reimbursements, and budget visibility.
- `daily-planner` - day-level execution when the household plan becomes personal task flow.
- `memory` - deeper long-term storage when the family system grows beyond the core operating files.

## Feedback

- If useful: `clawhub star family`
- Stay updated: `clawhub sync`
