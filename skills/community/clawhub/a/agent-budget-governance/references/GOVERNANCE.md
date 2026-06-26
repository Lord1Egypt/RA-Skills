# Agent Governance Framework

_Established: 2026-02-28_

## Philosophy

Trust-based autonomy with accountability. Agents start with mesh privileges
(can spawn each other directly), keep them by being responsible with budget,
and lose them through waste.

## Architecture

```
         Loki (orchestrator + auditor)
        / |    \    \
   Archie Sara  Kit  Liv
     ↔     ↔    ↔    ↔   (mesh: agents can spawn each other within budget)
```

### Hierarchy

- **Loki** is the general. Always has full spawn rights. Audits budgets on heartbeat.
- **All other agents** have mesh privileges by default — they can spawn each other
  directly without routing through Loki.
- Mesh privileges are **earned and maintained** through responsible budget use.

## Budget System

### Daily Token Budget

Each agent has a daily token budget (output tokens, since that's the primary cost driver).
Budget resets at midnight AEST.

| Agent   | Daily Budget (output tokens) | Model        | Rationale |
|---------|------------------------------|--------------|-----------|
| Loki    | unlimited                    | Opus         | Orchestrator, no cap |
| Archie  | 50,000                       | Sonnet       | Analysis tasks, moderate |
| Sara    | 50,000                       | Sonnet       | Content drafting |
| Kit     | 50,000                       | Sonnet       | Engineering tasks |
| Liv     | 50,000                       | Sonnet       | Marketing/scheduling |

### Budget Tracking

Each agent reads their budget file at session start:
`agents/<agent_name>/BUDGET.json`

Schema:
```json
{
  "daily_limit_output_tokens": 50000,
  "today": "2026-02-28",
  "used_output_tokens": 0,
  "spawns": [],
  "status": "active",
  "warnings": []
}
```

### Enforcement Levels

1. **Green (< 80%)** — Normal operation. Agent can spawn freely.
2. **Yellow (80-100%)** — Warning logged. Agent should finish current work and stop spawning.
3. **Red (> 100%)** — Over budget. Agent MUST NOT spawn other agents. Route through Loki.
4. **Demoted** — Persistent overspend. Agent loses mesh privileges entirely. All cross-agent
   calls must go through Loki until trust is re-earned.

### How Agents Self-Report

After each spawn or significant task, the agent updates their BUDGET.json:
- Increment `used_output_tokens` with the tokens from the completed task
- Add spawn record to `spawns[]` array
- Check if they've crossed a threshold

### Loki's Audit (Heartbeat)

During heartbeat, Loki:
1. Reads each agent's `BUDGET.json`
2. Cross-references with actual session logs (trust but verify)
3. Resets daily counters at midnight
4. Flags agents approaching limits
5. Demotes agents with 3+ consecutive days of overspend
6. Reports anomalies to Nissan

### Demotion & Rehabilitation

**Demotion triggers:**
- 3 consecutive days over budget
- Single day at >200% budget
- Spawning after being in Red status

**Demotion effect:**
- `allowAgents` set to `[]` in openclaw.json
- Agent can only be invoked BY Loki, cannot spawn others
- Status set to `"demoted"` in BUDGET.json

**Rehabilitation:**
- Agent demonstrates good behaviour for 5 days through Loki-mediated calls
- Loki recommends reinstatement to Nissan
- Nissan approves → mesh privileges restored

### Governance Log

All budget events, demotions, and reinstatements logged in:
`agents/governance/log.jsonl`

Format:
```json
{"ts": "2026-02-28T06:00:00+11:00", "agent": "sara", "event": "daily_reset", "details": {"previous_used": 42000}}
{"ts": "2026-02-28T14:30:00+11:00", "agent": "kit", "event": "warning", "details": {"used": 41000, "limit": 50000, "pct": 82}}
{"ts": "2026-03-01T06:00:00+11:00", "agent": "kit", "event": "demotion", "details": {"reason": "3 consecutive days over budget"}}
```

## Future: Hard Enforcement (Phase 2)

Build a middleware that intercepts `sessions_spawn` at the gateway level:
- Check caller agent's budget before allowing spawn
- Block with clear error message if over budget
- Log all spawn attempts (allowed and denied)
- Package as OpenClaw PR when stable

## Rules for Agents

Every agent's AGENTS.md must include:

```
## Budget Rules
- Read `agents/<your_name>/BUDGET.json` at session start
- Track your output token usage honestly
- Do NOT spawn other agents if your status is "red" or "demoted"
- Update BUDGET.json after completing spawned tasks
- If you need help but are over budget, write to your OUTBOX.md — Loki will route it
```
