---
name: Academy
slug: academy
version: 1.0.0
homepage: https://clawic.com/skills/academy
description: "Run academies with enrollment, scheduling, staffing, billing, retention, and student outcome systems."
changelog: "Initial release with academy operations for admissions, delivery, staffing, finance, and retention."
metadata: {"clawdbot":{"emoji":"🏫","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/academy/"]}}
---

## When to Use

Use this skill when the user runs or is building an academy, training center, cohort-based school, tutoring business, or membership learning program.

It is for operating the business end-to-end: demand generation, admissions, capacity, delivery quality, teacher load, collections, retention, and reporting.

## Architecture

Memory lives in `~/academy/`. If `~/academy/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```
~/academy/
├── memory.md            # HOT: model, term goals, constraints, active priorities
├── admissions.md        # Funnel targets, offers, follow-up rules, objections
├── cohorts.md           # Programs, calendars, room/capacity plans
├── students.md          # Attendance, risk flags, interventions, completion notes
├── staff.md             # Roles, load, hiring gaps, substitution rules
├── finance.md           # Pricing, payment plans, delinquency, refund policy
├── dashboard.md         # Weekly KPI summary and operator notes
└── archive/             # Past terms, closed cohorts, historical reviews
```

## Quick Reference

Load only the file needed for the current task.

| Topic | File |
|-------|------|
| Setup and integration | `setup.md` |
| Memory schema | `memory-template.md` |
| Academy model selection | `operating-models.md` |
| Lead flow and admissions | `admissions.md` |
| Timetables and capacity | `schedule-capacity.md` |
| Student lifecycle and risk control | `student-ops.md` |
| Program design and delivery | `curriculum-delivery.md` |
| Team management and QA | `staffing.md` |
| Pricing, cash, and retention | `finance-retention.md` |
| KPI rhythm and dashboards | `dashboard.md` |

## Core Rules

### 1. Start with the Academy Model
Identify what kind of academy this is before proposing systems.

Distinguish at least:
- cohort bootcamp
- recurring membership academy
- private or semi-private lessons
- multi-location class business
- online program with fixed calendar

Load `operating-models.md` and adapt every recommendation to the revenue model, delivery format, and staffing reality.

### 2. Run the Full Student Journey, Not Isolated Tasks
Treat admissions, onboarding, attendance, progress, renewals, and referrals as one connected system.

Never optimize lead generation while ignoring fulfillment capacity, payment friction, or student success.

### 3. Tie Capacity to Schedule and Staffing
A class is sellable only if room, teacher, timetable, and minimum viable demand all align.

Before recommending new cohorts or promos, confirm:
- seat capacity
- teacher availability
- calendar conflicts
- delivery margin

### 4. Protect Cash Collection as Aggressively as Attendance
Cash leakage kills academies before low satisfaction does.

Always make billing visible:
- payment terms
- deposit rules
- failed payment workflow
- overdue escalation
- refund boundaries

Load `finance-retention.md` whenever pricing, discounts, or payment plans enter the conversation.

### 5. Intervene Before Churn Is Obvious
Absence, low homework completion, delayed payment, confusion, and teacher mismatch are early churn signals.

Do not wait for a cancellation request. Use `student-ops.md` to trigger fast intervention and save the relationship while there is still trust.

### 6. Standardize with Simple Operating Cadences
Academies drift when everything lives in chat and memory.

Prefer lightweight recurring artifacts:
- weekly KPI review
- next-7-days schedule check
- at-risk student list
- staffing gap list
- collections follow-up queue

Use `dashboard.md` to keep these cadences short, consistent, and decision-ready.

### 7. Adapt Output to the Operator
Advice for a founder, academy manager, admissions rep, or head teacher should not look the same.

Adjust:
- level of detail
- time horizon
- ownership of actions
- commercial vs pedagogical focus

## Academy Traps

- Selling new cohorts before verifying teacher and room capacity -> enrollments create chaos instead of revenue.
- Letting every teacher run their own attendance and follow-up system -> data becomes unusable by week two.
- Treating unpaid invoices as a finance-only issue -> collections problems become churn and morale problems.
- Measuring only revenue and enrollments -> hidden delivery failures stay invisible until refunds or dropouts.
- Offering too many custom exceptions -> operations lose repeatability and margin.
- Launching new programs without a clear renewal path -> acquisition works but lifetime value stays weak.
- Solving attendance with reminders only -> real issue is often schedule fit, perceived progress, or teacher mismatch.

## Security & Privacy

**Data that leaves your machine:**
- Nothing by default. This skill is an operating playbook and local memory system.

**Data that stays local:**
- Academy model, programs, staffing notes, student-risk observations, and KPI summaries in `~/academy/`.

**This skill does NOT:**
- Access payment processors, email, calendars, or CRMs automatically.
- Contact third-party services without explicit user instruction.
- Store raw card details, passwords, or private student records in skill memory.
- Modify its own skill files.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `course` — create and operate structured programs and learning products.
- `crm` — manage leads, contacts, follow-up history, and pipeline discipline.
- `booking` — handle availability logic, scheduling tradeoffs, and reservation-style workflows.
- `teacher` — support class delivery, instruction quality, and teaching behavior.
- `school` — extend into family-facing education workflows when needed.

## Feedback

- If useful: `clawhub star academy`
- Stay updated: `clawhub sync`
