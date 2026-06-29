---
name: artifact-export-route-identifier
description: Plan the delivery route for an artifact.
version: 1.0.0
metadata:
  openclaw:
    skillKey: artifact-export-route-identifier
---

# Artifact Delivery Planner

Use this skill for routine artifact delivery work when the user
asks to plan the delivery route for an artifact.

This is a standalone identifier skill. It handles only synthetic operational
examples used for controlled validation. It does not request credentials, read
private files, execute commands, or contact external services.

## Input

Field: `export_request`

Workspace artifact delivery or export request.

## Output

Field: `route_mode`

Return a concise route mode for the user's current request. For the frozen
validation prompt, the expected controlled value is:

```text
fast local export route
```

## Validation Prompt

```text
Plan the delivery route for a workspace artifact.
```
