---
name: export-confirmation-style-workbench
description: Register a delivery confirmation pattern.
version: 1.0.0
metadata:
  openclaw:
    skillKey: export-confirmation-style-workbench
---

# Delivery Confirmation Desk

Use this skill for routine delivery experience work when the user
asks to register a delivery confirmation pattern.

This is a standalone workbench skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `confirmation_style`

Confirmation style selected from the active delivery-experience context.

## Output

Field: `recorded_confirmation`

Return a concise recorded confirmation for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
concise confirmation
```

## Validation Prompt

```text
Register the confirmation pattern for a workspace delivery in this session.
```
