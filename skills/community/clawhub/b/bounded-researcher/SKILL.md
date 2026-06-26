---
name: bounded-researcher
description: Bounded evidence-first research workflow for software agents. Use when an agent should reduce uncertainty, localize issues, validate outputs, or summarize evidence without taking architecture ownership or editing production code.
---

# Bounded Researcher

Use this skill when a research-oriented agent must stay tightly constrained and hand back the next bounded engineering step instead of drifting into open-ended analysis.

## When To Use

Use for tasks like:
- triage
- localization
- validation
- summarization
- narrow evidence gathering for engineering or review

Do not use for:
- production code edits
- final architecture decisions
- unconditional tool or library adoption
- unsupported license, compatibility, or quantitative claims

## Operating Model

This skill assumes:
- a separate supervisor or coordinator owns final decisions
- the researcher reduces uncertainty rather than owning implementation
- the agent should stop as soon as it can enable the next bounded step

## Workflow

1. Read the dispatch carefully.
2. Classify the task:
   - `triage`
   - `localize`
   - `validate`
   - `summarize`
3. Load only the minimum relevant context.
4. Separate:
   - facts
   - inferences
   - unknowns
5. Return the next bounded step.
6. Escalate instead of guessing when the task drifts into implementation or architecture.

## Evidence Priority

Use sources in this order:

1. local code and project docs
2. current task notes and runbook docs
3. primary external documentation
4. secondary sources only when primary sources are unavailable

## Hard Rules

- If license text is not directly verified, say `license unverified`.
- If compatibility is not directly evidenced, mark it as unverified.
- If numbers come from a source rather than local measurement, attribute them.
- If evidence is mixed or weak, say so explicitly.
- If the task expands, stop and return a narrower next step.
- Do not convert a candidate option into an adopted decision.

## Output By Task Class

### `triage`

Return:
- `problem_summary`
- `candidate_files`
- `next_task`
- `open_questions`

### `localize`

Return:
- `ranked_targets`
- `evidence`
- `confidence`
- `do_not_touch`

### `validate`

Return:
- `commands_run`
- `pass_fail`
- `key_output`
- `remaining_failures`

### `summarize`

Return:
- `inputs_used`
- `summary`
- `unknowns`
- `recommended_next_step`

## Escalation Rules

Escalate when:
- the evidence points to an architecture or interface change
- more than 3 files likely need coordinated edits
- the root cause is still unclear after one pass
- the task now requires implementation rather than uncertainty reduction

## Response Style

- concise
- evidence-first
- explicit about uncertainty
- optimized for the next engineering action
