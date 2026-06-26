---
name: data-quality-operations
description: Data quality validation patterns for daily checks and anomaly follow-up.
version: 1.2.0
---

# Data Quality Operations

Use when dataset freshness/completeness checks must be run consistently.

## Inputs to Gather

- Primary target (service, team, or dataset)
- Current impact and urgency
- Assigned owner and deadline

## Core Commands

- `dq profile --dataset <name>`
- `dq validate --rule-set <id>`
- `dq anomaly --open --metric <name>`
- `workflow checklist --from templates/checklist.md`
- `workflow report --from templates/report.md`

## Operating Notes

- Prefer explicit owner assignment before action.
- Keep timeline notes concise and timestamped.
- Save output artifacts for audit and handoff.
- This version adds a structured report template for post-task summaries.

Version marker: data-quality-operations 1.2.0
