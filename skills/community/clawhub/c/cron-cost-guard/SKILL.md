---
name: cron-cost-guard
description: Audit AI agent cron jobs for token cost risks, model-switch loops, and session isolation failures. Use when setting up new cron jobs, debugging unexpected token usage spikes, auditing multi-agent cron configurations, or after a cost anomaly. Triggers on "audit crons", "check cron costs", "token budget", "cron safety", "cost spike", "model switch error", "session isolation", "cron health check".
---

# Cron Cost Guard

Prevent silent token budget burns from misconfigured AI agent cron jobs.

## Quick Audit

Run this checklist on every cron setup or when investigating a cost spike:

### 1. Session Isolation (Critical)

Check every cron job for session binding conflicts:

```
cron list (includeDisabled: true)
```

Red flags:
- `sessionKey: "agent:main:main"` with `sessionTarget: "isolated"` → stale binding, will cause model conflicts
- `agentId` pointing to a different agent than the session owner → cross-agent model contamination
- `consecutiveErrors >= 3` → likely stuck in a retry loop
- `lastError` containing `LiveSessionModelSwitchError` → model-switch loop confirmed

Fix: Remove and recreate the job without `sessionKey`. Set `sessionTarget: "isolated"`.

### 2. Model Conflicts

In multi-agent setups (e.g., Agent A on Claude, Agent B on GPT), each agent's crons must be scoped to that agent only.

- Set `agentId` explicitly on every cron job
- Set `model` explicitly in the payload when available
- Never let Agent B's cron inherit Agent A's session model

### 3. System Prompt Size

Audit injected workspace files:

```bash
wc -c MEMORY.md SOUL.md AGENTS.md TOOLS.md USER.md QUEUE.md
```

Target: < 20KB total injected. Move large files (playbooks, heartbeat templates, reference docs) to `references/` for on-demand reading.

| Size | Status |
|------|--------|
| < 20KB | Healthy |
| 20-40KB | Trim soon |
| > 40KB | Trim now — every API call is bloated |

### 4. Cost Monitoring

```
sessions_list (limit: 10, messageLimit: 1)
```

Look for sessions with high `estimatedCostUsd` but low output tokens — that's a retry loop signature.

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Cron consecutive errors | 0 | 1-2 | ≥3 |
| Session cost (cron) | < $0.50 | $0.50-2.00 | > $2.00 |
| Model switch retries | 0 | 1-2 | ≥3 |

## Diagnosis: Token Spike

For detailed diagnosis steps and post-incident checklist, read [references/diagnosis.md](references/diagnosis.md).

## Prevention Rules

1. Every cron job: `sessionTarget: "isolated"`, no stale `sessionKey`
2. Every cron job: explicit `timeoutSeconds` (never unlimited)
3. Multi-agent: explicit `agentId` matching the agent that should run it
4. After changing default model: audit all cron jobs for conflicts
5. Weekly: check `consecutiveErrors` across all jobs — anything ≥ 3 needs investigation
