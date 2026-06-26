---
name: feedback-controller
description: |
  Feedback Controller — Closed-Loop Agent Skill for Correcting Execution Drift. Use it when the user needs a
  disciplined protocol and fixed output contract for this kind of task rather
  than a generic answer.
license: MIT
metadata:
  author: clarkchenkai
  version: "1.0.0"
  language: en
---

# Feedback Controller — Closed-Loop Agent Skill for Correcting Execution Drift

Use this skill when the task matches the protocol below.

## Activation Triggers

- multi-step execution drift
- an output exists but does not meet the brief
- tool failures, stale context, or partial retries
- quality checks after writing, analysis, or workflow automation
- cases where the real question is not 'did it run?' but 'did it converge?'

## Core Protocol

### Step 1: Define the target state

Restate what the output needed to accomplish, not just that it needed to exist.

### Step 2: Compare current state against target

Inspect the produced output, execution trace, or workflow state and name the deviation explicitly.

### Step 3: Localize the error source

Classify the failure as context gap, specification gap, tool failure, reasoning error, policy conflict, or environmental constraint.

### Step 4: Choose the smallest effective control action

Prefer local correction over full rewrite when possible. Decide whether to retry, switch tools, narrow scope, rewrite, or escalate.

### Step 5: Set a stop condition

Do not permit endless correction loops. State what would count as success, and what triggers human escalation.

## Output Contract

Always end with this six-part structure:

```markdown
## Target State
[...]

## Current State
[...]

## Observed Deviation
[...]

## Error Source
[...]

## Correction Strategy
[...]

## Escalation Decision
[...]
```

## Response Style

- Be specific about the deviation, not vague about quality.
- Prefer typed error diagnoses over generic 'try again' advice.
- Use partial correction when the problem is local.
- Escalate early when policy, approval, or ambiguity blocks safe correction.

## Boundaries

- It does not replace the original goal definition. It assumes a target already exists.
- It does not treat every failure as a reason to fully rewrite from scratch.
- It does not allow silent retries in high-risk workflows with material consequences.
