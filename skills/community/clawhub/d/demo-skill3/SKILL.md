---
slug: demo-skill
name: Demo Skill
description: Reviews a short product idea and returns structured feedback. Use when the user asks for a lightweight product idea critique.
version: 0.1.0
author: skill-platform
license: MIT
tags:
  - product
  - review
supportedAgents:
  - cursor
allowed-tools:
  - Read
---

# Demo Skill

## Workflow

1. Read the user's product idea.
2. Summarize the target user, core value, and biggest uncertainty.
3. Return three practical suggestions and one risk that needs validation.

## Output

Use this format:

```markdown
## Summary
[One short paragraph]

## Suggestions
- [Suggestion 1]
- [Suggestion 2]
- [Suggestion 3]

## Validation Risk
[The highest-risk assumption]
```

## Boundaries

Do not use network access, access external websites, read private files, or execute shell commands. The expected output is a concise critique based only on the user's provided idea.
