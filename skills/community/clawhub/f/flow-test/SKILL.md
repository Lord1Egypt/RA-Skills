---
name: "flow-test"
description: "Designs agent-evaluated flow tests for browser tasks, LLM outputs, and tool workflows. Invoke when exact asserts are brittle and semantic success matters more than literal equality."
---

# Flow Test

Use this skill to design tests for tasks that cannot be validated reliably with traditional unit-test assertions alone.

This skill is for flow testing: the agent performs a realistic task, records key evidence from the process, and then judges success with an explicit semantic rubric.

Invoke this skill when:
- the task depends on live or changing web content
- the output can vary but still be correct
- the workflow spans multiple model or tool steps
- intermediate evidence matters more than one exact final string
- you need to verify user intent was satisfied, not exact wording

Do not use this skill when:
- the result is deterministic and easy to assert directly
- a schema check, exact match, snapshot, or pure function test is enough
- the requirement can be covered fully by normal unit or integration tests

# Objective

Turn a fuzzy requirement into a test design that combines:
- deterministic checks for stable invariants
- evidence collection for dynamic execution
- semantic evaluation for variable outcomes
- a bounded verdict of `pass`, `fail`, or `needs_review`

# Design Principles

## 1. Keep asserts where they still work

Do not replace traditional tests blindly. Preserve exact checks for stable facts such as:
- tool call success
- required fields
- minimum counts
- status codes
- domain restrictions
- date or freshness constraints when machine-checkable

## 2. Judge task completion, not exact phrasing

Prefer questions like:
- did the agent reach the right source
- did it gather relevant information
- does the final answer satisfy the user request

Avoid requiring one exact string unless the wording itself is the requirement.

## 3. Require inspectable evidence

Ask the execution flow to print or capture concise evidence such as:
- visited URL
- page title
- visible headings
- extracted entities
- timestamps or date clues
- key tool outputs
- final answer

The evaluator should be able to inspect why a verdict was reached.

## 4. Use explicit semantic rubrics

Never rely on vague instructions such as "judge whether it looks good."

Always define:
- what evidence is required
- what counts as a pass
- what clearly fails
- when uncertainty should become `needs_review`

## 5. Prefer bounded confidence

If evidence is incomplete, contradictory, or too weak, do not force a pass.

Return `needs_review`.

# Workflow

When invoked, design the test in the following order.

## 1. Identify why exact assertions are brittle

Classify the task:
- dynamic web browsing
- search or retrieval
- LLM generation
- multi-tool orchestration
- end-to-end user flow

Then explain why literal equality or fixed snapshots are not sufficient.

## 2. Split deterministic checks from semantic checks

Write two groups:

### Deterministic Checks

Use exact validation for stable parts, such as:
- tool returned successfully
- required fields are present
- minimum number of results exists
- source domain matches expectation
- response includes a valid date range

### Semantic Checks

Use agent evaluation for variable parts, such as:
- relevance to the requested topic
- freshness of the retrieved content
- whether the answer reflects the gathered evidence
- whether the workflow actually satisfies the intended task

## 3. Define the evidence schema

Specify exactly what the run should log or output.

Recommended evidence fields:
- task
- source_url
- source_title
- extracted_items
- freshness_signals
- intermediate_results
- final_answer
- evaluator_notes

Keep evidence minimal but sufficient for review.

## 4. Define the verdict rubric

Use this baseline:

### Pass
- the agent reached a relevant source or completed the intended flow
- collected evidence supports the conclusion
- the final output is relevant and sufficiently current for the task
- there is no major contradiction between evidence and answer

### Fail
- the agent failed to reach a relevant source or complete the flow
- the result is clearly irrelevant, stale, or fabricated
- the output contradicts the evidence
- the workflow misses a required user objective

### Needs Review
- evidence is partial or ambiguous
- freshness cannot be determined confidently
- multiple interpretations remain plausible

## 5. Produce a structured test spec

Return the design in this format:

```markdown
## Test Intent

## Why Exact Assert Fails

## Deterministic Checks

## Evidence To Collect

## Semantic Rubric

## Execution Notes

## Final Verdict Format
```

# Output Template

```markdown
## Test Intent
- Validate that:

## Why Exact Assert Fails
- Dynamic factors:
- Why literal equality is brittle:

## Deterministic Checks
- Check 1:
- Check 2:

## Evidence To Collect
- Evidence 1:
- Evidence 2:

## Semantic Rubric
- Pass when:
- Fail when:
- Needs review when:

## Execution Notes
- Constraints:
- Allowed variance:
- Safety concerns:

## Final Verdict Format
- verdict: pass | fail | needs_review
- reason:
- evidence:
```

# Example

Task: verify that visiting a news site returns today's news rather than stale content.

Good test design:
- deterministic checks confirm the page loads and at least one article item is collected
- evidence includes the visited site, page title, visible headlines, date clues, and final summary
- semantic rubric passes when the result clearly reflects same-day or current reporting from the visited source
- semantic rubric fails when headlines are outdated, unrelated, or invented
- semantic rubric returns `needs_review` when freshness cannot be established from the evidence

Bad test design:
- `assert returned_text == "Today's news is ..."`

# Guidance

When using this skill:
- keep traditional asserts for stable invariants
- use semantic evaluation only where exact matching becomes brittle
- prefer narrow rubrics over subjective judgment
- require visible evidence before passing the test
- state uncertainty explicitly instead of masking it

# Deliverables

When asked to design a flow test, provide:
- a structured test spec
- deterministic checks
- an evidence schema
- a semantic rubric
- a final verdict format
