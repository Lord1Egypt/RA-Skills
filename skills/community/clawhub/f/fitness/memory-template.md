# Memory Template — Fitness

Files live in `~/Clawic/data/fitness/`. Three files, three jobs: `config.yaml` = declared preferences (Configuration table in SKILL.md), `memory.md` = what the agent observed and derived, `log.md` = the session record everything else is computed from.

## memory.md

```markdown
# Fitness Memory

## Status
status: ongoing
last: YYYY-MM-DD

## Baselines
<!-- Derived from log.md; recompute when they shift, keep the date -->
| Metric | Value | As of |
|---|---|---|
| e1RM squat | 120 kg | YYYY-MM-DD |
| e1RM bench | 85 kg | YYYY-MM-DD |
| Resting HR (7-morning avg) | 58 bpm | YYYY-MM-DD |
| Attendance (done/planned, last 4 weeks) | 10/12 | YYYY-MM-DD |

## Context
<!-- Goal as stated, schedule reality vs plan, equipment actually available -->

## Injury History and Exclusions
<!-- Movements to substitute and why; past injuries that gate loading -->

## Preferences
<!-- Observed, by preference area: schedule, exclusions, risk posture, data sources, coaching register -->

---
*Updated: YYYY-MM-DD*
```

## log.md

One line per session, append-only. Enough to compute e1RM trends and attendance; rep-by-rep detail belongs to the `gym` skill.

```markdown
# Training Log

YYYY-MM-DD | lower | squat 3x8 @ 100kg RIR2 · RDL 3x10 @ 80kg RIR3 | felt: normal | sleep 7h
YYYY-MM-DD | cardio | 40 min Zone 2 bike | RHR 57
YYYY-MM-DD | missed | planned upper — travel
```

Log missed sessions as `missed` with the reason: attendance rate and Rule 6 gap lengths are computed from them.

## Status Values

| Value | Meaning |
|-------|---------|
| `ongoing` | Still learning their training context |
| `complete` | Baselines and context well established |
