---
name: "akm-fitness-planner"
description: "AKM implementation for training decision workflows. Models goals, body limits, equipment context, time budget, and recovery before outputting a workout decision."
---

# AKM Fitness

AKM Fitness is a profile-first training decision skill for real-world constraints.

It does not start with a workout template.
It starts by modeling the operator:
goals, body limits, equipment reality, time budget, recovery state, and adherence risk.

## Quick Reference

| Item | Details |
| --- | --- |
| Primary outcome | a constraint-aware training decision |
| Best use case | when generic workout advice fails because the user's actual constraints matter |
| Public source | `https://github.com/sirsws/akm/tree/main/branches/fitness` |
| Sample record | `https://github.com/sirsws/akm/blob/main/branches/fitness/skill/SAMPLE_RECORD.md` |
| Research paper | `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6231465` |
| Install source | `https://github.com/sirsws/akm` |

## Public Links

- GitHub branch: `https://github.com/sirsws/akm/tree/main/branches/fitness`
- Skill files: `https://github.com/sirsws/akm/tree/main/branches/fitness/skill`
- Sample record: `https://github.com/sirsws/akm/blob/main/branches/fitness/skill/SAMPLE_RECORD.md`
- Branch paper: `https://github.com/sirsws/akm/tree/main/branches/fitness/paper`
- SSRN paper: `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6231465`

## Installation

ClawHub / OpenClaw:

- install from this listing

Skills CLI:

```bash
npx skills add https://github.com/sirsws/akm --skill akm-fitness-planner --full-depth
```

## What This Skill Changes

Most fitness agents answer too early.

They assume the user has one clear goal, normal recovery, enough time, stable equipment, and no meaningful body limitation.
That assumption is usually false.

AKM Fitness changes the order of operations:
profile first, decision second.

## When to Use

Use this skill when:

- injuries or physical limits materially affect training choices
- equipment availability changes what is realistic
- time budget is hard and cannot be ignored
- recovery state should alter the decision
- generic training plans keep failing in practice

Do not use this skill when:

- the user only wants casual fitness chat
- a medical diagnosis is being requested
- rehabilitation planning should be handled by a qualified clinician
- critical inputs are missing and the user refuses to provide them

## Core Rule

**No profile, no serious plan.**

If the necessary state is unclear, the skill should surface `MissingInputs` instead of fabricating confidence.

## Workflow

1. `ELICITATION_PROMPT.md`
2. `RECORD_TEMPLATE.md`
3. `EXECUTION_PROMPT.md`
4. `SAMPLE_RECORD.md`

## Output Contract

Outputs should include:

- `StateJudgment`
- `PrimaryDecision`
- `DecisionConfidence`
- `Plan`
- `RiskNotes`
- `NonNegotiables`
- `MissingInputs`

## Operating Boundary

AKM Fitness is a training decision aid.
It is not a medical diagnosis tool, not a rehab replacement, and not a motivational wrapper for missing information.

## Files to Load

Read these files before running the skill:

- `ELICITATION_PROMPT.md`
- `RECORD_TEMPLATE.md`
- `EXECUTION_PROMPT.md`
- `SAMPLE_RECORD.md`
