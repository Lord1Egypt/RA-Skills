---
name: agent-self-care
description: |
  Autonomous agent health, optimization, and cleanup. Use when: (1) running scheduled cron jobs for agent maintenance, (2) responding to "optimize", "cleanup", "health check", "clear stalls", or "self-maintain" requests, (3) performing BMAD-style retrospective and continuous improvement, (4) checking sub-agent sessions, process health, memory usage, and context bloat, (5) ensuring fast response times and autonomous operation. This skill handles all self-optimization workflows including stale session cleanup, context compaction, and performance monitoring.
---

# Agent Self-Care

Autonomous health monitoring and optimization for OpenClaw agents. Runs on cron or triggers manually.

## Workflow

### 1. Check Sub-Agents

```bash
subagents action=list
```

Kill any stale sub-agents:
- Running >30 min without progress
- In "waiting" state
- Failed/errored

### 2. Check Processes

```bash
process action=list
```

Kill hanging processes:
- Running >10 min in background
- No output in 5 min

### 3. Check Session Health

```bash
session_status
```

Metrics to watch:
- Context usage >80% → trigger compaction
- Tokens growing unbounded
- Session age >2 hours → suggest refresh

### 4. Run Optimization Script

Execute `scripts/optimize.sh` which:
- Clears completed cron job artifacts
- Rotates logs if >50MB
- Reports health metrics

### 5. BMAD Retrospective (every 10 runs)

After 10 executions, run:
- Score last task 1-10
- Identify gaps
- Document improvements in `memory/daily/YYYY-MM-DD.md`
- Feed learnings into next run

## Cron Schedule

Recommended: Every 5 minutes for active agents.

```json
{
  "name": "agent-self-care",
  "schedule": {"kind": "every", "everyMs": 300000},
  "payload": {"kind": "agentTurn", "message": "Run agent-self-care skill"},
  "sessionTarget": "isolated",
  "enabled": true
}
```

## Output Format

Report after each run:

```
🔧 Self-Care Report
- Sub-agents: X active, Y killed
- Processes: X running, Y cleared
- Context: X% used
- Health: ✅ GOOD / ⚠️ WARNING
- Retrospective: SKIP / COMPLETE
```

## Key Principles

1. **Always clean** - Never leave stalled sub-agents or processes
2. **Proactive** - Don't wait for user to ask
3. **Document** - Log issues and improvements
4. **BMAD** - Continuous self-evaluation every 10 runs
5. **Fast** - Complete in <30 seconds
