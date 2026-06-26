---
name: debate-learning-workflow
description: Run evidence-backed multi-agent debates (A/B/Opponent3/Judge) with 20-40 rounds, loophole analysis, and universal actionable lesson extraction.
---

# Debate Learning Workflow

Use this skill to run structured, high-rigor debates that produce transferable learning.

## Core Rules
- Minimum 20 rounds per topic.
- Judge-gated continuation if critical loopholes remain.
- Hard stop at 40 rounds.
- Openings must include **Claim + Evidence + Source**.
- Unsupported openings are invalid and must be revised.
- Every round logs:
  - loophole found
  - why loophole exists
  - concrete fix for next round

## Roles
- Debater A
- Debater B
- Opponent3 (alternative/challenger model)
- Judge (evidence quality + unresolved uncertainty)

## Output Files
- Topic file: `~/Desktop/debate/YYYY-MM-DD-topic.md`
- Daily index: `~/Desktop/debate/YYYY-MM-DD-index.md`
- Lessons append target: `~/Desktop/lessons.md`

## Universalization Quality Gate
Every generalized lesson must include:
1) Trigger condition
2) Loophole/failure pattern
3) Root cause
4) Corrective action
5) Measurable metric/threshold
6) Boundary conditions
7) Transfer examples in at least 2 other fields

If any field is missing, lesson is INVALID and must be rewritten.
