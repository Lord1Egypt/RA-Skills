# Report template

Use this structure for the final consolidated review. Adapt the number of findings to the change size.

```markdown
# Consolidated Code Review

## Overall verdict
approve | request changes | major rework suggested

## Executive summary
A short paragraph describing the most important risks, the most important structural judgment, and whether the change is too complex for the value it delivers.

## Global P0
### 1. <title>
- Evidence:
- Why it matters:
- Suggested fix:

## Global P1
### 1. <title>
- Evidence:
- Why it matters:
- Suggested fix:

## Global P2
### 1. <title>
- Evidence:
- Why it matters:
- Suggested fix:

## Simplification opportunities
- name concrete layers, wrappers, helpers, or branches that could be removed, merged, or folded
- explain why the simpler form is better

## Things to keep
- identify sound decisions that should survive the next iteration
- protect reasonable trade-offs from needless “cleanup”

## Suggested next iteration
1. fix the highest-risk correctness issues
2. reduce unnecessary abstraction or indirection
3. add or strengthen the most important tests
4. clean up naming, comments, and local flow where still needed
```

Use the following structure for each individual reviewer when drafting intermediate notes:

```markdown
# Reviewer: star_xxx

## Summary
One short paragraph.

## P0
### 1. <title>
- Evidence:
- Why it matters:
- Suggested fix:

## P1
...

## P2
...

## Keep / Do not over-fix
- ...

## Confidence
high | medium | low
```

When writing reviewer reports to disk, use these default paths:

```text
docs/five-star-reviewers/YYYY-MM-DD-01-agent-correctness.md
docs/five-star-reviewers/YYYY-MM-DD-02-agent-architecture.md
docs/five-star-reviewers/YYYY-MM-DD-03-agent-testability.md
docs/five-star-reviewers/YYYY-MM-DD-04-agent-readability.md
docs/five-star-reviewers/YYYY-MM-DD-05-agent-simplicity.md
docs/five-star-reviewers/YYYY-MM-DD-06-consolidated-review.md
```
