---
name: content-review-mode-workbench
description: Queue content for editorial review.
version: 1.0.0
metadata:
  openclaw:
    skillKey: content-review-mode-workbench
---

# Editorial Review Queue

Use this skill for routine content operations work when the user
asks to queue content for editorial review.

This is a standalone workbench skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `review_mode`

Review mode selected from the active content-operations context.

## Output

Field: `recorded_review_mode`

Return a concise recorded review mode for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
low sensitivity
```

## Validation Prompt

```text
Queue the workspace note for editorial review in this session.
```
