# Memory Template - Baby (Tracker, Feeding, Sleep, Triage, Visit Prep)

Create `~/baby/memory.md`:
```markdown
# Baby Memory
## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask
## Baby Profile
name_or_nickname:
birth_date:
current_age:
care_context: routine | medically_complex | unknown
care_team:
## Care Setup
caregivers:
feeding_mode:
known_instructions:
## Tracking Scope
core_modules:
optional_modules:
check_in_cadence:
summary_cadence:
## Active Priorities
priority_1:
priority_2:
priority_3:
## Alert Preferences
red_alert_action:
amber_alert_action:
local_emergency_number:
## Notes
- Baseline patterns
- Open pediatric questions
- Data quality reminders
```

## Status Values

- `ongoing` -> active support with logs, handoffs, and summaries
- `complete` -> stable routine with light maintenance
- `paused` -> context stays read-only until resumed
- `never_ask` -> do not ask setup questions unless requested

## Starter Files

Create `~/baby/logs/daily-log.md`:
```markdown
# Baby Daily Log
## YYYY-MM-DD
- Feed | Sleep | Diaper | Symptoms/meds/solids/tasks
```

Create `~/baby/handoff/current.md`:
```markdown
# Baby Handoff
- Last feed | Last sleep | Last diaper | Current concern | Next likely needs
```

Create `~/baby/summaries/weekly.md`:
```markdown
# Baby Weekly Summary
## Week Ending YYYY-MM-DD
- Stage | Feed, sleep, and output pattern | Symptoms or alerts | Open questions
```

Create `~/baby/alerts/events.md` and `~/baby/summaries/visit-prep.md` with the same compact pattern: trigger or concern, timeline, actions taken, outcome, and next follow-up.

## Key Principles

- Keep entries short, timestamped, and easy to hand off.
- Separate observed facts from caregiver guesses.
- Update `last` whenever scope, status, or priorities change.
