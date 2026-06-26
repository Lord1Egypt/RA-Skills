---
name: agent-gtd
description: "DEPRECATED — renamed to elephantastic. Install elephantastic instead: clawhub install elephantastic"
version: 1.2.0
deprecated: true
redirect_to: elephantastic
---

# agent-gtd → elephantastic

This skill has been renamed to **elephantastic**.

## Why

Elephantastic is memorable, distinctive, and carries the "never forget" memory metaphor directly in the name. `agent-gtd` was functional but said nothing to anyone who didn't already know what GTD was.

## Migration

```bash
clawhub install elephantastic
```

Then update any agent configurations that reference `agent-gtd` to use `elephantastic` instead. The behavior is identical — just a better name.

*The agent's memory — never forget.*