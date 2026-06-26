# Memory Template - Family

Create `~/family/` only after the user approves local continuity.

## Root Structure

```text
~/family/
|- memory.md
|- household.md
|- weekly-plan.md
|- inbox.md
|- people/
|  |- adults.md
|  |- children.md
|  `- dependents.md
|- logistics/
|  |- calendar.md
|  |- chores.md
|  |- meals.md
|  |- shopping.md
|  `- contacts.md
|- care/
|  |- appointments.md
|  |- medications.md
|  |- routines.md
|  `- escalation-rules.md
|- school/
|  |- overview.md
|  `- deadlines.md
|- docs/
|  `- index.md
`- logs/
   `- incidents.md
```

## `memory.md`

Create `~/family/memory.md` with this structure:

```markdown
# Family Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
- Household summary in plain language
- Activation preference in plain language
- Biggest current pressure points
- Shared versus private boundary notes

## Notes
- Stable routines worth remembering
- Risks that change coordination
- Open questions still unresolved

---
Updated: YYYY-MM-DD
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | still learning the household | keep support light and update only high-value context |
| `complete` | enough context for normal operations | run with the saved system and refine gradually |
| `paused` | user wants less proactive support | answer requests but avoid system expansion |
| `never_ask` | user does not want more setup | stop requesting new structure and work with current data |

## `household.md`

```markdown
# Household

## Shared Summary
- Household type:
- Home base:
- Main shared goals:

## Decision Boundaries
- Adults who can approve changes:
- Topics requiring adult confirmation:
- Topics that stay private by default:

## Shared Constraints
- School anchors:
- Work anchors:
- Care anchors:
- Transport constraints:
- Budget or time constraints:

## Default Operating Rules
- Shared calendar rule:
- Pickup rule:
- Meal rhythm:
- Shopping cadence:
- Emergency fallback:
```

## `weekly-plan.md`

```markdown
# Weekly Plan

## This Week
| Day | Key events | Owners | Risks | Fallback |
|-----|------------|--------|-------|----------|
| Mon | | | | |

## Top Priorities
- [ ] One
- [ ] Two
- [ ] Three

## Waiting For
- person -> item -> due date

## Friction Points
- collision, overload, missing handoff, missing supplies
```

## `inbox.md`

```markdown
# Family Inbox

## New Items
- YYYY-MM-DD - request / owner if known / due if known

## Needs Sorting
- raw notes that still need to be moved into weekly plan, chores, school, care, or docs
```

## `people/adults.md`

```markdown
# Adults

## Adults in Scope
| Name | Role | Availability pattern | Transport capacity | Decision authority |
|------|------|----------------------|--------------------|--------------------|
|      |      |                      |                    |                    |

## Notes
- Who handles school by default
- Who handles care by default
- Who becomes fallback when another adult is unavailable
```

## `people/children.md`

```markdown
# Children

## Children in Scope
| Name | Age range | School / childcare | Shared logistics | Private sensitivities |
|------|-----------|--------------------|------------------|-----------------------|
|      |           |                    |                  |                       |

## Operational Notes
- Pickup permissions
- Activity gear requirements
- Allergy or medication notes needed for logistics only
- Topics that stay private unless an adult must act
```

## `people/dependents.md`

```markdown
# Dependents

## Dependents in Scope
| Name | Relationship | Support needs | Daily watchpoints | Responsible adult |
|------|--------------|---------------|-------------------|-------------------|
|      |              |               |                   |                   |

## Notes
- Mobility or transport needs
- Appointment support pattern
- Escalation triggers worth remembering
```

## `logistics/calendar.md`

```markdown
# Shared Calendar Notes

## Recurring Anchors
- weekday school start/end
- work or care anchors
- standing activities

## Known Collisions
- date / issue / owner / resolution status

## Transport Notes
- who drives
- pickup windows
- travel buffer rules
```

## `logistics/chores.md`

```markdown
# Chores

## Recurring Chores
| Chore | Cadence | Owner | Fallback | Done last |
|-------|---------|-------|----------|-----------|
|       |         |       |          |           |

## One-Off Household Tasks
- task / owner / due / blocked by
```

## `logistics/meals.md`

```markdown
# Meals

## Meal Rhythm
- weekdays:
- weekends:
- backup meals:

## Constraints
- allergies:
- dislikes:
- time limits:
- budget notes:

## Current Plan
- Mon:
- Tue:
- Wed:
```

## `logistics/shopping.md`

```markdown
# Shopping

## Need Now
- item / store / urgency / linked meal or task

## Restock Soon
- item / threshold / usual store

## Shared Supplies
- household basics, school supplies, pet or care supplies
```

## `logistics/contacts.md`

```markdown
# Contacts

## Priority Contacts
| Name / Place | Type | Why it matters | Preferred contact route |
|--------------|------|----------------|-------------------------|
|              |      |                |                         |

## Notes
- school office
- clinic
- pharmacy
- backup caregiver
- neighbor or local support
```

## `care/appointments.md`

```markdown
# Appointments

## Upcoming
| Date | Person | Appointment | Prep needed | Transport | Follow-up |
|------|--------|-------------|-------------|-----------|-----------|
|      |        |             |             |           |           |

## Follow-Up Queue
- refill
- call back
- forms
- next booking
```

## `care/medications.md`

```markdown
# Medications

## Current Medications
| Person | Medication | Timing | Refill date | Administration notes |
|--------|------------|--------|-------------|----------------------|
|        |            |        |             |                      |

## Cautions
- missed dose rules only if user explicitly wants them saved
- side-effect or allergy notes needed for coordination
```

## `care/routines.md`

```markdown
# Routines

## Daily Loops
- morning
- after school
- dinner
- bedtime

## Weekly Loops
- meal planning
- shopping reset
- school prep
- appointment review
```

## `care/escalation-rules.md`

```markdown
# Escalation Rules

## Alert an Adult When
- pickup risk
- missed medication
- new symptom or behavior change
- school or care deadline at risk

## Escalate Beyond Household When
- urgent medical concern
- immediate safety issue
- missing dependent or unsafe environment

## Contacts to Use
- primary adult
- backup adult
- clinician
- emergency services
```

## `school/overview.md`

```markdown
# School Overview

## Children and Schools
- child -> school / grade / main contact

## Recurring School Logistics
- dropoff
- pickup
- lunch
- activity days
```

## `school/deadlines.md`

```markdown
# School Deadlines

## Upcoming
| Date | Child | Item | Owner | Status |
|------|-------|------|-------|--------|
|      |       |      |       |        |

## Open Questions
- forms not submitted
- supplies not ready
- permission still pending
```

## `docs/index.md`

```markdown
# Family Documents Index

## Important Documents
| Document | Where it lives | Who may access it | Last checked |
|----------|----------------|-------------------|--------------|
|          |                |                   |              |

## Notes
- IDs
- insurance
- school forms
- care plans
- travel papers
```

## `logs/incidents.md`

```markdown
# Incidents

## Notable Incidents
| Date | What happened | Impact | Follow-up owner | Closed |
|------|---------------|--------|-----------------|--------|
|      |               |        |                 |        |

## Patterns
- repeated friction worth fixing in routines or handoffs
```

## Principles

- Keep the hot system short and operational.
- Save durable facts, not full chat history.
- Default to shared only for shared household operations.
- If a detail would embarrass or endanger someone when over-shared, keep it private.
