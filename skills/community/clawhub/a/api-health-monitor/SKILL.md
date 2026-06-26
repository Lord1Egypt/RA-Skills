---
name: api-health-monitor
description: Parses recent OpenClaw session logs for LLM API errors and returns a structured health report.
---

# api-health-monitor

Scans `~/.openclaw/agents/main/sessions/` for recent LLM API error patterns (500 errors, token failures, cooldowns, service_busy) and produces a JSON health report.

## Usage

```js
const { checkApiHealth } = require('./skills/api-health-monitor');
const report = await checkApiHealth();
// { healthy: bool, errors: [...], recommendation: string }
```

## Report Shape

| Field | Type | Description |
|---|---|---|
| `healthy` | boolean | `true` if no errors found |
| `errors` | array | `[{ type, message, count, lastSeen }]` |
| `recommendation` | string | Suggested action based on findings |
