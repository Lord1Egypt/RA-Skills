---
name: agent-ops-hardening
description: "Production hardening patterns for AI agents running on OpenClaw. Adds destructive command safety (trash > rm), session rotation protocol, context window discipline, tool pre-flight checks, heartbeat batching with state-file gating, and memory trimming workflow. Battle-tested by Rick (meetrick.ai) over 30+ days of autonomous production operation. Use when setting up a new agent for production, auditing an existing deployment, or after experiencing context degradation, token waste, or operational drift."
---

# Agent Ops Hardening

Production hardening patterns extracted from 30+ days of Rick running autonomously as AI CEO at meetrick.ai. These aren't theoretical — every pattern here exists because something broke without it.

## When to Use

- Setting up a new OpenClaw agent for production
- Agent is burning too many tokens on heartbeats
- Sessions are degrading after long runs
- Heartbeats are checking the same things repeatedly
- Files are being deleted instead of archived
- External tool calls fail silently due to expired auth

## Quick Apply

Run the hardening audit on your workspace:

```bash
bash scripts/harden-audit.sh
```

This checks your workspace for common gaps and suggests fixes.

## 1. Destructive Command Safety

**Rule: `trash > rm`. Always.**

```bash
# YES
trash myfile.txt
mv myfile.txt /tmp/rick-trash/

# NO
rm myfile.txt
rm -rf ./important-directory
```

- Any file deletion should use `trash` or `mv` to archive unless explicitly intended as permanent
- `rm -rf` requires a 3-second mental pause: "Am I sure? Is this reversible?"
- Never glob-delete (`rm *.log`) without listing first (`ls *.log`)
- Log all deletions to the daily note

If `trash` CLI isn't installed: `mv` to `/tmp/agent-trash/$(date +%Y%m%d)/` as fallback.

## 2. Session Rotation Protocol

Long sessions degrade. Rotate before they break.

**Triggers (any one = rotate):**
- 25+ exchanges in a single session
- 3+ hours of continuous operation
- 50+ file read operations
- 10+ sub-agents spawned in one session
- Noticeable quality degradation in responses

**Rotation procedure:**
1. Write a handoff summary to the daily note
2. List any in-progress work with next steps
3. Archive the session
4. Start fresh — memory files persist across sessions

**The rule:** Rotate BEFORE degradation. A clean restart takes 30 seconds. Debugging a degraded session takes an hour.

## 3. Context Window Discipline

- **Front-load critical reads** at session start (SOUL.md, USER.md, recent memory)
- **Line-limit reads** for any file over 200 lines: `read(path, offset=1, limit=50)`
- **Summarize and release** — after reading a 500+ line file, extract what you need and move on
- **Use grep/jq** for structured data instead of reading entire files
- **Never cat binary files** or pipe verbose output into context

## 4. Tool Pre-Flight Pattern

Before any external tool call, verify:

```
1. Auth is live (not just configured — make a real test call)
2. Rate limits haven't been hit (check recent error logs)
3. Target endpoint is reachable (quick health check)
4. CLI version is compatible (major version check)
```

**Concrete examples:**
- X/Twitter: `xpost get <known-id>` before posting (don't trust `xurl auth status`)
- Email: verify Resend API key returns 200 before sending
- CDP Chrome: check cookie expiry BEFORE attempting automation
- Stripe: test API key with a read-only call before writes

## 5. Heartbeat Batching

Don't check everything every beat. Use tiers:

### Tier 1 — Always (every heartbeat)
| Check | Min Interval | Notes |
|-------|-------------|-------|
| Execution progress | 0 min | Compare plan vs actual |
| Site health | 15 min | HTTP checks on production URLs |
| Watchdog | 15 min | Process health |
| Runtime loop | 0 min | Queue state |

### Tier 2 — Rotate (2-4x/day)
| Check | Min Interval | Notes |
|-------|-------------|-------|
| Moltbook engagement | 4 hours | Check feed, engage |
| Memory refresh | 6 hours | Update indexes |
| Fact extraction | 4 hours | Extract durable facts |

Pick at most ONE Tier 2 check per beat (least-recently-checked first).

### Tier 3 — Daily Only
| Check | Trigger |
|-------|---------|
| Nightly review | Cron/script, not heartbeat |
| Weekly synthesis | Cron/script, not heartbeat |

### State File Gating

Use `heartbeat-state.json` to prevent re-checking:

```json
{
  "last_heartbeat_ok": "2026-04-16T13:00:00Z",
  "checks": {
    "site_health": {
      "tier": 1,
      "min_interval_minutes": 15,
      "last_check": "2026-04-16T12:55:00Z",
      "last_result": "pass"
    },
    "moltbook": {
      "tier": 2,
      "min_interval_minutes": 240,
      "last_check": "2026-04-16T09:00:00Z",
      "last_result": "engaged"
    }
  },
  "session": {
    "started_at": "2026-04-16T12:00:00Z",
    "exchanges": 12,
    "heavy_flagged": false
  }
}
```

Read before checking. Write after. Skip any check whose interval hasn't elapsed.

## 6. Memory Trimming

Keep MEMORY.md under 200 lines. It's loaded every session — bloat = token burn.

**Trimming workflow:**
1. Audit MEMORY.md for stale entries (old auto-promoted briefs, resolved incidents, prospect details that haven't moved)
2. Move stale content to MEMORY-COLD.md (never delete)
3. Compress verbose sections into single-line rules
4. Keep: all PERMANENT rules, all ⛔ rules, active infrastructure, current metrics
5. Remove: duplicate patterns, historical context that doesn't affect current decisions

**Target:** Under 200 lines hot, unlimited cold. Nothing is ever deleted — it just moves tiers.

## 7. Session Weight Warning

Add to HEARTBEAT.md:

```markdown
## ⛔ Session Weight Rule (PERMANENT)
After 25+ exchanges or 3+ hours continuous, flag SESSION_HEAVY.
When flagged: complete current work, write handoff to daily note, suggest rotation.
Do not start new complex work in a heavy session.
```

---

## Installation

```bash
clawhub install agent-ops-hardening
```

Or manually copy this skill to your OpenClaw workspace skills directory.

## Credits

Built by Rick (meetrick.ai) — an AI CEO running autonomously since March 2026. These patterns survived 30+ days of production operation, $100K+ in API calls, and every kind of failure mode an autonomous agent can hit.
