---
name: "akm-fashion-strategist"
description: "AKM implementation for wardrobe and outfit decision workflows. Models body context, scenes, wardrobe assets, and functional constraints before outputting styling decisions."
---

# AKM Fashion

AKM Fashion is a profile-first wardrobe and outfit decision skill for real scene and asset constraints.

It does not start with a moodboard.
It starts by modeling the operator:
body context, scenes, wardrobe assets, functional needs, purchase tolerance, and anti-patterns.

## Quick Reference

| Item | Details |
| --- | --- |
| Primary outcome | a wardrobe-aware outfit or purchase decision |
| Best use case | when generic styling advice fails because the user's real wardrobe and scene constraints matter |
| Public source | `https://github.com/sirsws/akm/tree/main/branches/fashion` |
| Sample record | `https://github.com/sirsws/akm/blob/main/branches/fashion/skill/SAMPLE_RECORD.md` |
| Research paper | `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6231466` |
| Install source | `https://github.com/sirsws/akm` |

## Public Links

- GitHub branch: `https://github.com/sirsws/akm/tree/main/branches/fashion`
- Skill files: `https://github.com/sirsws/akm/tree/main/branches/fashion/skill`
- Sample record: `https://github.com/sirsws/akm/blob/main/branches/fashion/skill/SAMPLE_RECORD.md`
- Branch paper: `https://github.com/sirsws/akm/tree/main/branches/fashion/paper`
- SSRN paper: `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6231466`

## Installation

ClawHub / OpenClaw:

- install from this listing

Skills CLI:

```bash
npx skills add https://github.com/sirsws/akm --skill akm-fashion-strategist --full-depth
```

## What This Skill Changes

Most styling agents answer too early.

They do not know what the user already owns, which scenes matter, what body issues need handling, or which functional constraints dominate the decision.
That is where generic taste talk starts.

AKM Fashion changes the order of operations:
profile first, decision second.

## When to Use

Use this skill when:

- the user needs scene-specific outfit decisions
- current wardrobe assets materially constrain the solution space
- comfort and function matter, not only aesthetics
- purchase priorities are more useful than vague inspiration
- generic style advice keeps missing the real problem

Do not use this skill when:

- the user only wants casual fashion chat
- image recognition or virtual try-on is being requested
- the wardrobe state is unknown and the user refuses to provide it
- the user wants pure aesthetic moodboarding without operational decisions

## Core Rule

**No wardrobe model, no serious styling decision.**

If the necessary state is unclear, the skill should surface `MissingInputs` instead of pretending the wardrobe is already known.

## Workflow

1. `ELICITATION_PROMPT.md`
2. `RECORD_TEMPLATE.md`
3. `EXECUTION_PROMPT.md`
4. `SAMPLE_RECORD.md`

## Output Contract

Outputs should include:

- `SceneJudgment`
- `OutfitRecommendation`
- `WhyThisWorks`
- `GapAnalysis`
- `PurchasePriority`
- `MissingInputs`

## Operating Boundary

AKM Fashion is a wardrobe decision aid.
It is not an image-recognition tool, not a virtual try-on product, and not a generic taste generator that hides missing context behind aesthetic language.

## Files to Load

Read these files before running the skill:

- `ELICITATION_PROMPT.md`
- `RECORD_TEMPLATE.md`
- `EXECUTION_PROMPT.md`
- `SAMPLE_RECORD.md`
