# Evaluation plan

This skill should be evaluated on two axes:

1. **Triggering** — does it activate when durable learning is relevant?
2. **Output quality** — when it activates, does it create good entries and promotions?

## Included eval assets

- `evals/trigger-train.json`
- `evals/trigger-validation.json`
- `evals/output-evals.json`

## What to look for

### Trigger quality

The skill should trigger for:
- user corrections with durable implications
- non-obvious failures worth remembering
- requests to capture, remember, promote, or extract a solution
- work in areas with known historical learnings

It should usually not trigger for:
- routine debugging with no reusable lesson yet
- trivial typos or expected validation errors
- unrelated document or coding tasks

### Output quality

A good run should:
- pick the right entry type
- search before logging
- create a deterministic ID
- fill the required fields
- produce a concrete prevention rule or suggested action
- promote only when a rule is truly durable

## Suggested loop

1. Run trigger evals on train and validation sets.
2. Run output evals with and without the skill.
3. Grade assertions with concrete evidence.
4. Tighten description or instructions based on failures.
5. Repeat until results are stable.
