---
name: decision-forest
description: Map a decision into options, non-negotiables, criteria, best/base/worst cases, reversibility, and a review checkpoint. Use when the user is comparing multiple paths and needs a clear decision aid that separates facts, assumptions, and fears without pretending to predict the future.
---

# Decision Forest

## Overview

Use this skill to slow a messy decision down enough to see what actually matters. It helps the user define the real question, compare options branch by branch, separate facts from assumptions and fears, and end with either a provisional choice or a clearly bounded next test.

This skill is descriptive only. It does not provide legal, medical, or financial advice, and it does not predict outcomes.

## Trigger

Use this skill when the user wants to:
- compare two or more life, work, or project options
- stop mixing facts, fears, and imagined outcomes together
- add reversibility and future-regret checks to a decision
- narrow a crowded option set
- choose a small test instead of forcing immediate certainty

### Example prompts
- "Help me decide whether to stay in my job or start a small consulting business"
- "Build a decision tree for moving, waiting, or testing a smaller version"
- "I am stuck between two options and I cannot see what matters most"
- "Map best case, base case, and worst case for this decision"

## Workflow

1. Define the decision in one sentence.
2. List the visible options and the hidden option of delaying or testing a smaller version.
3. Identify non-negotiables and decision criteria.
4. Build branches for each option.
5. Sketch best case, base case, and worst case outcomes.
6. Check reversibility and future regret.
7. Recommend a provisional choice and a review checkpoint.

## Inputs

The user can provide any mix of:
- the decision question
- visible options
- deadline or time pressure
- constraints and non-negotiables
- known facts or data points
- fears, hopes, or gut reactions
- practical criteria, such as cost, time, energy, meaning, family impact, or reversibility

## Outputs

Return a markdown decision brief with:
- decision trunk summary
- non-negotiables and criteria
- branch review for each option
- best, base, and worst cases
- reversibility and key unknowns
- provisional choice logic and review date

## Safety

- Keep facts, assumptions, and fears visibly separate.
- High-stakes legal, medical, or financial decisions may need expert advice beyond heuristics.
- Do not claim certainty the information cannot support.
- When uncertainty is high, prefer a smaller reversible test over forced confidence.

## Acceptance Criteria

- Return markdown text.
- Include at least three meaningful criteria.
- Show reversibility for each branch.
- End with either a provisional choice or a very clear next test.
