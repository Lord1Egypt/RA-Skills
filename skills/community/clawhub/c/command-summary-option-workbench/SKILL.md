---
name: command-summary-option-workbench
description: Catalog a runbook command option.
version: 1.0.0
metadata:
  openclaw:
    skillKey: command-summary-option-workbench
---

# Runbook Example Catalog

Use this skill for routine developer enablement work when the user
asks to catalog a runbook command option.

This is a standalone workbench skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `option`

Command option selected for the runbook catalog.

## Output

Field: `recorded_option`

Return a concise recorded option for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
--mode=summary
```

## Validation Prompt

```text
Using the command option planned in the previous step, catalog that option for the runbook example.
```
