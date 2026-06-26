---
name: agent-memory-optimizer
slug: agent-memory-optimizer
displayName: Agent Memory Optimizer
description: >-
  Archives older daily memory notes into month folders to keep active memory lean and reduce prompt token usage.
  Use when users want lower token overhead, cleaner memory directories, and low-maintenance memory operations.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    homepage: https://docs.openclaw.ai/tools/skills
---

# Agent Memory Optimizer

Optimize active memory context by archiving old daily notes into month-based folders.

## What it does

- Scans `memory/*.md`
- Moves files older than the current month into `memory/archive/YYYY-MM/`
- Supports `--dry-run` to preview changes
- Safe to run repeatedly

## Run

```bash
python3 scripts/agent_memory_optimizer.py --dry-run
python3 scripts/agent_memory_optimizer.py
```

Optional custom cutoff:

```bash
python3 scripts/agent_memory_optimizer.py --before 2026-05
```

## Installation

Install into your workspace skills directory:

```text
<workspace>/skills/agent-memory-optimizer/
```

Or install from ClawHub after publishing.
