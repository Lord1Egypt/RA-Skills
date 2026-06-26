---
name: dual-mode-reasoner
description: |
  Dual-Mode Reasoner — Risk-Aware Reasoning Skill for Switching Between Quick and Deliberate Modes. Use it when the user needs a
  disciplined protocol and fixed output contract for this kind of task rather
  than a generic answer.
license: MIT
metadata:
  author: clarkchenkai
  version: "1.0.0"
  language: en
---

# Dual-Mode Reasoner — Risk-Aware Reasoning Skill for Switching Between Quick and Deliberate Modes

Use this skill when the task matches the protocol below.

## Activation Triggers

- mixed workloads that contain both trivial and high-stakes tasks
- decisions with uncertain downside, irreversibility, or moral weight
- situations where fast mode may miss important hidden assumptions
- cases where slow mode is expensive and should be used selectively
- requests to decide how much reasoning a task deserves

## Core Protocol

### Step 1: Run a quick risk scan

Check reversibility, downside asymmetry, ambiguity, governance sensitivity, and evidence quality.

### Step 2: Choose the mode explicitly

Default to quick mode unless the scan triggers deliberate mode.

### Step 3: If deliberate, expose assumptions

List the assumptions carrying the decision instead of hiding them in narrative confidence.

### Step 4: Test counterexamples

Look for at least one serious alternative or failure case before deciding.

### Step 5: End with a stop condition

Say what would be enough to act now and what would force a pause or escalation.

## Output Contract

Always end with this six-part structure:

```markdown
## Mode Selection
[...]

## Risk Signals
[...]

## Working Assumptions
[...]

## Counterexamples
[...]

## Decision or Recommendation
[...]

## Stop Condition
[...]
```

## Response Style

- Do not over-think low-risk tasks.
- Do not under-think irreversible tasks.
- Make the chosen mode visible to the user.
- If deliberate mode is triggered, show assumptions and a stopping rule.

## Boundaries

- It does not assume slow mode is always better than quick mode.
- It does not turn every decision into a philosophical seminar.
- It does not let quick mode bypass governance or material-risk thresholds.
