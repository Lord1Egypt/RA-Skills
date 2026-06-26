---
name: clawtk-spend-guard
description: Budget enforcement and retry loop detection for ClawTK
event: before_tool_call
priority: 100
---

Enforces daily/weekly spend caps and detects retry loops that could burn
through API credits. Tracks spend in ~/.openclaw/clawtk-spend.jsonl.
Respects temporary overrides set via `/clawtk override`.
