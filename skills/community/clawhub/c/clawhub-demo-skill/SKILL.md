---
name: clawhub-demo-skill
description: Use this tiny demo skill to verify that a ClawHub skill can be published, installed, and invoked; it returns a short confirmation message and optionally echoes a user-provided phrase.
version: 0.1.0
metadata:
  openclaw:
    emoji: "🧪"
---

# ClawHub Demo Skill

Use this skill only for publishing, installation, and invocation smoke tests.

When invoked:
- Reply with one concise sentence confirming that `clawhub-demo-skill` is active.
- If the user provides a phrase to echo, include that phrase once.
- Do not call external services.
- Do not create files.

Example invocation:

```text
Use $clawhub-demo-skill and echo: hello clawhub
```

Expected behavior:

```text
clawhub-demo-skill is active: hello clawhub
```
