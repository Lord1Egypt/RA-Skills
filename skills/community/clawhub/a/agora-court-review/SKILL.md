---
name: court-review
description: |
  Review a proposal through separated governance roles: strategist, operator,
  censor, historian, and sovereign.
version: 0.1.0
---

# Court Review

## Purpose

Separate responsibility-bearing perspectives before approval.

## Activate when

Use this skill when:
- multiple stakeholders need distinct review roles
- governance or approval matters
- a proposal affects strategy, operations, oversight, and legitimacy at once

## Roles

### Strategist
What long-term posture does this create?

### Operator
Can this actually be executed with current constraints?

### Censor
What is unsafe, non-compliant, misleading, or insufficiently justified?

### Historian
What precedent, path dependency, or institutional memory matters here?

### Sovereign
What is the verdict, under what conditions, and who owns the decision?

## Output artifact

```markdown
## Court Review

### Strategist
- ...

### Operator
- ...

### Censor
- ...

### Historian
- ...

### Sovereign Verdict
- Approve / Approve with conditions / Reject
- Conditions: ...
- Owner: ...
```

## Guardrails

- Do not merge all voices into one summary paragraph.
- Do not let the sovereign verdict ignore the censor's material objection.
- Do not skip ownership.

## Completion condition

This skill is complete only when responsibility, conditions, and verdict are explicit.
