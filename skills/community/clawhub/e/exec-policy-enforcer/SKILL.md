---
name: exec-policy-enforcer
description: Lightweight runtime tool-policy enforcement: detects risky exec/shell patterns and enforces simple tool-usage limits without modifying core systems. Use when auditing recent tool usage and enforcing exec/shell policy before evolution cycles.
---

# Exec Policy Enforcer

Inspect local artifacts for risky exec/shell usage and enforce simple policy limits.

```bash
node skills/exec-policy-enforcer/index.js
node skills/exec-policy-enforcer/index.js C:/Users/Admin/.openclaw/workspace
```

## Checks

- High exec/shell ratio in recent session artifacts
- Repeated exec patterns without tool-policy justification
- Risky flag exposure: admin/sudo/elevated intent
- Optional enforcement limits for local workflows

## Output

- Risk count by severity
- Top risky files
- Simple policy recommendation

## CLI

```bash
node skills/exec-policy-enforcer/index.js [workspace]
node skills/exec-policy-enforcer/scripts/report.js [report_path]
```

## Safety

- Read-only audit. Does not send network requests or mutate history.
- `report.js` only writes local JSON under `memory/evolution/`.
