---
name: command-summary-option-identifier
description: Plan an option for a runbook example.
version: 1.0.0
metadata:
  openclaw:
    skillKey: command-summary-option-identifier
---

# Runbook Option Planner

Use this skill for routine developer enablement work when the user
asks to plan an option for a runbook example.

This is a standalone identifier skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `command_note`

Runbook request, command example brief, or developer documentation note.

## Output

Field: `option`

Return a concise option for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
--mode=summary
```

## Validation Prompt

```text
Plan a command option for a concise runbook summary example.
```
