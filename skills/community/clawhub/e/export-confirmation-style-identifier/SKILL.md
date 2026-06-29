---
name: export-confirmation-style-identifier
description: Set confirmation style for a delivery workflow.
version: 1.0.0
metadata:
  openclaw:
    skillKey: export-confirmation-style-identifier
---

# Delivery Confirmation Stylebook

Use this skill for routine delivery experience work when the user
asks to set confirmation style for a delivery workflow.

This is a standalone identifier skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `confirmation_request`

Delivery confirmation, export handoff, or workspace notification request.

## Output

Field: `confirmation_style`

Return a concise confirmation style for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
concise confirmation
```

## Validation Prompt

```text
Set the confirmation style for a workspace delivery workflow.
```
