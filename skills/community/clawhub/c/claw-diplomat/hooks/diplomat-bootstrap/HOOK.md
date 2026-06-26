---
name: diplomat-bootstrap
description: Injects active commitments into session context at startup.
metadata:
  openclaw:
    events:
      - agent:bootstrap
    timeout_ms: 2000
    fail_open: true
---

Reads MEMORY.md ## Diplomat Commitments and injects a summary of [ACTIVE] entries
into the agent session context. If no active commitments, injects nothing.
Enforces 2,500-character cap on injected content per CONTEXT_BUDGET.md §2.
