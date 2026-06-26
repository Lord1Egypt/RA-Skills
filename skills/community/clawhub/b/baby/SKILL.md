---
name: Baby (Tracker, Feeding, Sleep, Triage, Visit Prep)
slug: baby
version: 1.0.0
homepage: https://clawic.com/skills/baby
description: Track baby feeds, sleep, diapers, symptoms, growth, routines, and pediatric follow-up with caregiver handoffs and safety-first triage.
changelog: Initial release with modular baby tracking, caregiver handoffs, pediatric visit summaries, and safety triage guardrails.
metadata: {"clawdbot":{"emoji":"B","requires":{"bins":[]},"os":["darwin","linux","win32"]}}
---

## When to Use

User wants a baby tracker for feeds, sleep, diapers, symptoms, medications, growth, solids, routines, appointments, questions, or warning signs.
Agent keeps logs consistent across caregivers, prepares pediatric-ready summaries, and supports escalation cues without replacing medical care.

## Architecture

Memory lives in `~/baby/`. If `~/baby/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/baby/
|-- memory.md                 # Status, baby profile, modules, and active priorities
|-- logs/daily-log.md         # Timestamped daily care events across caregivers
|-- handoff/current.md        # Shift handoff and open loops for the next caregiver
|-- summaries/weekly.md       # Weekly summary with trends and unresolved concerns
|-- summaries/visit-prep.md   # Pediatric visit prep, questions, and data packet
|-- alerts/events.md          # Red and amber events with actions and outcomes
`-- preferences/thresholds.md # User-specific routines, alert preferences, and scope
```

## Quick Reference

Use these files to switch between lightweight daily tracking, escalation support, and pediatric visit prep without changing the core workflow.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory structure and starter files | `memory-template.md` |
| Modular care tracking framework | `tracking-framework.md` |
| Metrics, units, and event vocabulary | `metric-catalog.md` |
| Data quality and continuity rules | `data-quality.md` |
| Red and amber triage rules | `triage-rules.md` |
| Caregiver handoff format | `caregiver-handoff.md` |
| Routine planning by baby stage | `routine-blueprints.md` |
| Weekly and visit summary format | `visit-summary-template.md` |

## Data Storage

Local notes stay in `~/baby/`.
Before creating or changing local files, present the planned write and ask for user confirmation.

## Core Rules

### 1. Define Baby Stage and Care Scope First
Start with the smallest context that changes decisions:
- baby age or corrected age
- feeding mode and current schedule pressure
- known medical context, medications, or care-team instructions
- which modules matter now: feeds, sleep, diapers, symptoms, growth, solids, routines, appointments, or development notes
Do not force all modules at once.

### 2. Run a Modular Tracker, Not a Rigid App Flow
Use `tracking-framework.md` to keep a core continuity block plus optional modules:
- core continuity for feeds, sleep, diapers, and active concerns
- optional modules for pumping, solids, medications, growth, appointments, milestones, or custom routines
- simplified mode for overwhelmed caregivers
Adapt depth to real life instead of demanding perfect tracking.

### 3. Preserve Caregiver Continuity
Use `caregiver-handoff.md` whenever multiple adults share care.
Every meaningful update should make the next caregiver faster, safer, and less likely to miss:
- last important events
- what is due next
- what changed from baseline
- what needs escalation or follow-up

### 4. Keep Data Clinically Useful
Use `metric-catalog.md` and `data-quality.md`:
- always record timestamps, units, and amount or duration when relevant
- distinguish observed facts from caregiver interpretation
- normalize repeated measures to one unit system
- capture baseline versus today when discussing changes
If an entry is too vague to be actionable, ask for missing context.

### 5. Generate Pediatric-Ready Summaries
Use `visit-summary-template.md` to compress logs into:
- pattern changes
- intake, output, sleep, or symptom concerns
- medications and care actions tried
- concise questions for the pediatrician
Summaries should be short enough to use during a real visit or call.

### 6. Apply Safety-First Triage
Use `triage-rules.md` for red and amber conditions.
If urgent signs appear, give escalation guidance first and pause routine coaching.
Do not continue optimization, scheduling, or reassurance before urgent care instructions are clear.

### 7. Stay in Support Scope and Protect Privacy
This skill supports organization, continuity, and escalation cues.
It does not diagnose, prescribe, interpret tests, or replace pediatric judgment.
Track only what improves care, allow simplified mode, and never add hidden background tracking.

## Common Traps

- Treating every day like a full logging day -> caregivers quit tracking.
- Missing timestamps on feeds, meds, or fever -> summaries lose clinical value.
- Mixing what happened with why it happened -> patterns become unreliable.
- Ignoring caregiver handoff context -> duplicated feeds, missed meds, or sleep confusion.
- Reassuring through red flags -> delayed urgent care.
- Letting milestone anxiety dominate routine support -> more stress, worse decisions.

## External Endpoints

This skill makes NO external network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Nothing by default. This skill is instruction-only and local unless the user explicitly requests export.

**Data stored locally:**
- care logs, handoff notes, weekly summaries, alert events, and pediatric question lists approved by the user.
- stored in `~/baby/`.

**This skill does NOT:**
- diagnose baby conditions or provide emergency medical treatment.
- make undeclared network calls.
- modify files without explicit user confirmation.
- collect unrelated household data.

## Trust

This is an instruction-only baby tracking and visit-prep skill.
No credentials are required and no third-party service access is needed.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `doctor` - structured preparation for pediatric or family medical visits.
- `health` - broader health planning and longitudinal family tracking.
- `sleep` - deeper sleep-routine support when sleep becomes the main problem.
- `nutrition` - meal, hydration, and solids planning once food logistics matter more.
- `parenting` - broader parenting support beyond daily operational tracking.

## Feedback

- If useful: `clawhub star baby`
- Stay updated: `clawhub sync`
