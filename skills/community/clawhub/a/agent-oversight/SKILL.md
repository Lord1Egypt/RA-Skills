---
name: agent-oversight
description: Comprehensive AI agent oversight and management skill. Monitors sub-agents, manages file edit coordination, logs failures, kills hung sessions, and maintains oversight records.
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      bins: [python3]
    always: false
---

# Agent Oversight

Manages and monitors AI sub-agents. Keeps Beta's workspace clean, coordinated, and error-free.

## Usage

```bash
python3 oversight.py --status
python3 oversight.py --list-sessions
python3 oversight.py --kill-hung
```

## Features

- Session monitoring (active/idle/hung)
- File edit coordination (prevents conflicts)
- Failure logging to memory/learnings.md
- Automatic kill for >5min hung sessions
- Coordination rules enforcement

## Coordination Rules

1. Read file before editing
2. Exact oldText matching required
3. One agent per file at a time
4. Log all failures to learnings.md
