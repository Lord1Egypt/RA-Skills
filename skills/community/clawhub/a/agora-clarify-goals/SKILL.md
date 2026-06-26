---
name: clarify-goals
description: |
  Clarify a vague request into purpose, constraints, success criteria, unknowns,
  and next-step readiness. Activate before planning or implementation when the
  real objective is still blurry.
version: 0.1.0
---

# Clarify Goals

## Purpose

Turn a vague request into an actionable brief.

This skill exists to prevent false starts.
Do not proceed into planning, coding, or debate until the core decision is clear enough to state plainly.

## Activate when

Use this skill when any of the following are true:
- the request is broad, fuzzy, or overloaded
- the user asks for a solution before the underlying goal is clear
- multiple success criteria are implied but not distinguished
- the team is jumping into execution with different problem frames
- a debate is starting, but the actual decision is not yet visible

## Do not use when

Skip this skill when:
- the task already has a crisp decision question
- constraints and success criteria are explicit
- the user is asking for straightforward execution on a settled plan

## Required questions

Always extract answers for these five fields:

1. Purpose
- What must be different as a result of this work?
- What real problem is being solved?

2. Constraints
- What limits the space? Time, risk, dependencies, policy, tooling, social cost.

3. Success criteria
- What observable outcome would count as success?
- What would Descartes later be able to verify?

4. Unknowns
- What materially important facts are missing?
- Which assumptions are currently doing too much work?

5. Decision posture
- Is this mainly a clarification, decision, ideation, review, or governance problem?

## Procedure

### Step 1 — Restate the request plainly
Rewrite the request in one sentence without embellishment.
If you cannot do this, the request is not yet clear.

### Step 2 — Separate goal from solution
Identify where the user has stated a preferred solution before proving it is the right problem frame.
Call this out explicitly.

### Step 3 — Extract the five fields
Fill Purpose, Constraints, Success Criteria, Unknowns, Decision Posture.

### Step 4 — Identify the blocking ambiguity
Name the one ambiguity that most threatens good judgment if ignored.

### Step 5 — Recommend next workflow
Route to one of:
- frame-the-decision
- compare-options
- doubt-list
- assumption-audit
- minority-report
- court-review
- dialectic overlay
- skeptic overlay
- genealogy overlay
- court overlay

## Output artifact

```markdown
## Clarification Brief

### Request in Plain Language
- ...

### Purpose
- ...

### Constraints
- ...

### Success Criteria
- ...

### Unknowns
- ...

### Decision Posture
- Clarification / Decision / Ideation / Review / Governance

### Blocking Ambiguity
- ...

### Recommended Next Step
- Skill or overlay: ...
- Why: ...
```

## Guardrail

Do not proceed into implementation or deep planning if any of these are still missing:
- a concrete purpose
- at least one success criterion
- the main blocking ambiguity

If clarity is insufficient, stop and say so.
A fast wrong start is worse than a slow correct frame.

## Failure modes

Common failure modes:
- treating a requested solution as the real goal
- listing vague aspirations instead of measurable success criteria
- flattening multiple decisions into one blob
- hiding key unknowns because they are inconvenient
- routing directly to dialectic when simple clarification would suffice

## Escalation points

Escalate to the user when:
- competing purposes cannot both be optimized
- the key constraint is political or organizational rather than technical
- success criteria conflict with each other
- the user must choose which ambiguity to resolve first

## Completion condition

This skill is complete only when the output makes the next workflow obvious.
If the next step is still ambiguous, clarification is incomplete.
