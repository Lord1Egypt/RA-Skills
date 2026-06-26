---
name: dreamcycle
description: >
  AI Agent Self-Reflection Engine — scan session logs, detect failure patterns,
  analyze recurrence trends, and suggest automated fixes.
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      anyBins:
        - pip3
        - pip
    primaryEnv: ""
    emoji: 🔄
    homepage: https://github.com/qize-auto/dreamcycle
    tags:
      - agent-self-reflection
      - debugging
      - auto-fix
      - session-analysis
      - failure-detection
    category: development
---

# DreamCycle

Detect, analyze, and auto-repair failure patterns from AI agent session logs.

## When to use

Use DreamCycle when:
- An agent has been running for a while and you want to check for recurring failures
- Session logs are accumulating and you want trend analysis
- You suspect the same error keeps happening but no one is tracking it
- You want automated fix suggestions for known failure patterns
- After making changes to agent configuration, to verify nothing regressed

## How it works

DreamCycle is a **retrospective debugger** for AI agents. It scans your agent's
session log files in three phases:

```
Session Logs → Scan → Analyze → Fix
```

1. **Scan** — Extracts failure, pattern, and lesson signals from JSON session files
2. **Analyze** — Detects recurring patterns (appearing 2+ times) and trends
   (up/down/stable compared to previous scans)
3. **Fix** — Maps known failure patterns to automated fix suggestions with
   confidence scores

## Installation

```bash
pip install dreamcycle
```

## Usage

```bash
# Basic diagnostic: scan last 2 days of sessions
dreamcycle diagnose ~/.openclaw/sessions/

# Scan last 7 days
dreamcycle diagnose ~/my-agent/logs/ --days 7

# JSON output for programmatic use
dreamcycle diagnose ./sessions/ --output json

# Version info
dreamcycle version
```

## Example output

```
━━━ DreamCycle Diagnose ━━━
Scanned:    42 sessions (last 2 days)
Signals:    156 total (failures: 78, patterns: 52, lessons: 26)
━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 Top Recurring Patterns
  [12x] "timeout" → ⚡ high
    Fix: add retry_with_backoff (confidence: 85%)
  [8x]  "ModuleNotFoundError" → ⚡ high
    Fix: pip install <module> (confidence: 95%)

📈 Trends
  ↑ timeout: 12x (up from 5x last scan)
  ↓ ModuleNotFoundError: 8x (down from 15x)

🔧 Auto-Fix Summary
  ✅ 2/4 patterns have automated fixes
  ❌ 2 patterns need manual review
```

## Requirements

Only `python3` and `pip`. Zero external dependencies — DreamCycle uses only
the Python standard library.

## Notes

- Session files must be JSON format with a `messages` array containing
  `role`/`content` fields
- First run establishes a baseline; trends appear starting from the second run
- Trend data is stored at `~/.dreamcycle/scan_history.json`
