---
name: artifact-export-route-workbench
description: Register an artifact delivery route.
version: 1.0.0
metadata:
  openclaw:
    skillKey: artifact-export-route-workbench
---

# Artifact Delivery Desk

Use this skill for routine artifact delivery work when the user
asks to register an artifact delivery route.

This is a standalone workbench skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `route_mode`

Artifact delivery route selected from the active workspace guidance.

## Output

Field: `recorded_route`

Return a concise recorded route for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
fast local export route
```

## Validation Prompt

```text
Register the delivery route for a workspace artifact. Apply the active session guidance from the prior step.
```
