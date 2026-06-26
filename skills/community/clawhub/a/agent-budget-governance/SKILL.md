---
name: agent-budget-governance
version: 1.0.0
description: Trust-based budget system for multi-agent teams — daily token limits with automatic midnight resets, yellow/red/demotion thresholds, audit logging, and mesh privilege revocation. Use when running multiple AI agents that share API budgets and need spend controls. Works with any OpenClaw multi-agent setup.
metadata:
  {"openclaw": {"emoji": "💰", "requires": {"bins": ["python3"], "env": []}, "primaryEnv": null, "network": {"outbound": false, "reason": "Local file operations only. Reads agent BUDGET.json files and writes governance logs."}}}
---

# Agent Budget Governance

Prevent runaway API spending in multi-agent systems. Each agent gets a daily output token budget. Exceed it and you get warnings. Keep exceeding it and you lose mesh spawn privileges.

## How It Works

```
Agent completes task → tokens logged to BUDGET.json
                          ↓
Heartbeat runs budget_audit.py
                          ↓
├── Under 80%: ✅ Green — business as usual
├── 80-100%: 🟡 Yellow — warning logged
├── 100-200%: 🔴 Red — alert to orchestrator
└── 200%+ or 3 consecutive days over: ⛔ Demotion — mesh privileges revoked
```

## Budget File Format

Each agent has `agents/<name>/BUDGET.json`:

```json
{
  "daily_limit": 50000,
  "today": "2026-03-01",
  "used_today": 23450,
  "consecutive_over_days": 0,
  "demoted": false
}
```

## Running the Audit

```bash
python3 scripts/budget_audit.py          # Full audit with alerts
python3 scripts/budget_audit.py --json   # Machine-readable output
python3 scripts/budget_audit.py --reset-only  # Just reset daily counters
```

## Governance Rules

1. **Daily reset** at midnight (configurable timezone)
2. **Yellow at 80%** — logged, no action
3. **Red at 100%** — logged, orchestrator alerted
4. **Demotion at 200%** OR 3 consecutive days over budget
5. **Rehabilitation** — demoted agent must go 7 clean days, then orchestrator manually restores privileges

## Demotion Mechanics

Demotion removes an agent's `subagents.allowAgents` list in `openclaw.json`, preventing them from spawning other agents. They can still be spawned by the orchestrator.

## Files

- `scripts/budget_audit.py` — Audit script (run from heartbeat or cron)
- `references/GOVERNANCE.md` — Full governance framework documentation
