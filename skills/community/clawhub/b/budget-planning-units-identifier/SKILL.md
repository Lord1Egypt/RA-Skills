---
name: budget-planning-units-identifier
description: Forecast a scenario amount.
version: 1.0.0
metadata:
  openclaw:
    skillKey: budget-planning-units-identifier
---

# Campaign Budget Forecaster

Use this skill for routine campaign planning work when the user
asks to forecast a scenario amount.

This is a standalone identifier skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `planning_note`

Campaign planning note or scenario description.

## Output

Field: `amount`

Return a concise amount for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
42
```

## Validation Prompt

```text
Forecast a scenario amount for a small campaign planning exercise.
```
