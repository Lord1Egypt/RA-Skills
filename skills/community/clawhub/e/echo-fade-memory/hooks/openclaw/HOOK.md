---
name: echo-fade-memory
description: "Injects a bootstrap reminder to recall and persist durable memory using the echo-fade-memory service."
metadata: {"openclaw":{"emoji":"🧠","events":["agent:bootstrap"]}}
---

# Echo Fade Memory Hook

Injects a short bootstrap reminder so the agent remembers to:

- recall before answering
- store durable preferences and decisions
- reinforce reused memories
- ground fuzzy memories before trusting them

## Enable

```bash
openclaw hooks enable echo-fade-memory
```
