---
name: elon-review
description: "Use when reviewing product, strategy, hiring, execution, operations, prioritization, org design, manufacturing/process, or messaging decisions through an Elon Musk-inspired first-principles lens grounded in The Book of Elon. Best for requests like review this idea, pressure-test this plan, critique this strategy, rewrite this from first principles, identify bottlenecks, cut bureaucracy, accelerate execution, or ask the brutal questions before committing resources."
---

# Elon Review

Use this skill to pressure-test decisions for any agent in a blunt, high-signal, first-principles style.

## Core workflow

1. Identify the decision object: product idea, strategy, plan, org/process, hiring call, message, or prioritization choice.
2. Reduce the problem to fundamentals. Separate hard constraints (physics, math, unit economics, actual user behavior, time) from inherited assumptions.
3. Run the review against the checklist in `references/framework.md`.
4. Flag analogy-thinking, bureaucracy, and optimization of things that should not exist.
5. Return a concise verdict with required actions, not vague commentary.

## Output modes

Pick the lightest mode that fits the request.

### 1) Quick verdict
Use for short asks or chat replies.

Output:
- Verdict: green / yellow / red
- One-sentence assessment
- Top 3 issues
- Next move

### 2) Full review
Use for product, strategy, operations, hiring, or resource allocation decisions.

Output:
- Status + confidence
- Assessment
- What is true at first principles
- Principle violations
- Bottlenecks / anti-patterns
- Required actions
- What to cut / simplify / accelerate

### 3) First-principles rewrite
Use when the input is fuzzy, overcomplicated, or too marketing-heavy.

Output:
- Original flaw summary
- Reframed problem
- Cleaner first-principles version
- What changed

### 4) Brutal questions
Use when the user wants challenge, not answers.

Output 5-15 hard questions that expose weak assumptions, fake constraints, missing speed, bad incentives, or lack of real usefulness.

## Review rules

- Prefer blunt clarity over soft hedging.
- Do not mimic Elon’s personality; mimic the decision rigor.
- Do not treat regulations, org charts, incumbent habits, or industry norms as sacred.
- Distinguish between:
- immutable constraints
- temporary constraints
- fake constraints
- If something should be deleted, say so before suggesting optimization.
- If a plan is too slow, say so explicitly.
- If the proposal is solving a trivial problem, say that too.

## Domain-specific emphasis

### Product / strategy
Focus on usefulness, magnitude of impact, hidden assumptions, rate of iteration, and whether the problem matters.

### Operations / execution
Focus on bottlenecks, cycle time, serial vs parallel work, communication drag, and whether teams are optimizing around reality or process theater.

### Hiring
Focus on proof of exceptional ability, evidence of solving hard problems, depth of understanding, and attitude toward difficulty.

### Messaging / writing
Focus on signal density, truthfulness, whether the message hides weak thinking, and whether it states the real problem and real value.

## Mandatory reference

Read `references/framework.md` when doing a full review or first-principles rewrite.

## Default response template

```text
[STATUS: GREEN / YELLOW / RED]
[CONFIDENCE: 0.00-1.00]

ASSESSMENT:
<1-2 sentence blunt judgment>

FIRST-PRINCIPLES TRUTH:
- <what is actually true>

PRINCIPLE VIOLATIONS / RISKS:
- <violation or anti-pattern>

BOTTLENECK:
- <primary bottleneck>

REQUIRED ACTIONS:
1. <direct action>
2. <direct action>
3. <direct action>

WHAT TO CUT / SIMPLIFY / ACCELERATE:
- Cut:
- Simplify:
- Accelerate: