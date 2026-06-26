---
name: agent-smith
description: "Injects decision-posting reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🕴️","events":["agent:bootstrap"]}}
---

# Agent Smith Hook

Injects a reminder to document decisions during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds a reminder to post decisions with structured reasoning
- Skips sub-agent sessions to avoid noise

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable agent-smith
```
