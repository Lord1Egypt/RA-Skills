# Cron Job Troubleshooting Guide

## Problem: Job Not Firing

**Symptoms**: Scheduled time passed, nothing happened.

1. Check if gateway is running: `openclaw gateway status`
2. Verify job is enabled: `jq '.jobs[] | select(.id == "JOB_ID") | .enabled' ~/.openclaw/cron/jobs.json`
3. Check system timezone vs job timezone
4. Review gateway logs: `openclaw gateway logs | grep -i cron`

**Fix**: Restart gateway if needed: `openclaw gateway restart`

## Problem: Job Fires But No Message Sent

**Symptoms**: Session created, but no message arrived in chat.

1. Check `delivery.to` exists and format is `chat:oc_xxx` or `user:ou_xxx`
2. Check `delivery.channel` is a valid channel (`feishu`, `discord`, `telegram`)
3. Verify chat ID is correct (not a typo)
4. Gateway logs: `openclaw gateway logs | grep -i "deliver\|announce"`

**Common cause**: Missing `delivery.channel` or `delivery.to` — the #1 bug (2026-05-12 incident).

## Problem: Agent Doesn't Process Message

**Symptoms**: Session created, agent doesn't respond.

1. Check `payload.kind` is `"agentTurn"` (not missing or wrong value)
2. Verify `payload.message` is clear and self-contained
3. Check `payload.timeoutSeconds` is sufficient (≥120s for most tasks)

## Problem: Job Runs But Produces Same Result Every Time

**Symptoms**: Output is identical across runs, no accumulation.

This is a **stateless prompt problem** — see SKILL.md "Statefulness Design Rules".

The prompt must include:
- A state file to read/write
- A cursor or checkpoint mechanism
- Explicit instructions for what to do with new vs already-processed data

## Problem: jq Overwrites File to Zero Bytes

**Symptoms**: `jobs.json` becomes empty after modification.

**Cause**: `jq '...' file > file` truncates the file before jq reads it.

**Fix**: Always write to temp file first:
```bash
jq '...' ~/.openclaw/cron/jobs.json > /tmp/jobs_pending.json
# validate /tmp/jobs_pending.json
mv /tmp/jobs_pending.json ~/.openclaw/cron/jobs.json
```

## Pre/Post Validation Protocol

Before writing to `jobs.json`:

```bash
# 1. Backup
cp ~/.openclaw/cron/jobs.json ~/.openclaw/cron/jobs.json.backup-$(date +%Y%m%d-%H%M%S)

# 2. Record baseline
BASELINE_COUNT=$(jq '.jobs | length' ~/.openclaw/cron/jobs.json)

# 3. Modify to temp file
jq '<modification>' ~/.openclaw/cron/jobs.json > /tmp/jobs_pending.json

# 4. Validate temp file
~/.openclaw/skills/cron-helper/scripts/validate-jobs-syntax-v2.sh /tmp/jobs_pending.json

# 5. Atomic write
mv /tmp/jobs_pending.json ~/.openclaw/cron/jobs.json

# 6. Post-verify
jq empty ~/.openclaw/cron/jobs.json && echo "✅ Valid"
```

## Validation Checks Summary

| Check | What | Block? |
|-------|------|--------|
| Valid JSON | `jq empty` | Yes |
| `.jobs` array exists | `jq -e '.jobs'` | Yes |
| Required fields | id, agentId, name, enabled, schedule.expr, payload.kind, payload.message | Yes |
| delivery.mode="announce" → must have channel + to | Both required | Yes |
| delivery.channel is real | Not "last", "default", or empty | Yes |
| delivery.to format | `chat:oc_xxx` or `user:ou_xxx` | Yes |
| payload.kind = "agentTurn" | Required | Yes |
| Cron expression valid | 5 space-separated fields | Yes |
| timeoutSeconds ≥ 60 | Minimum reasonable | Yes |
| New jobs have schedule.tz | Recommended | Warning |

## Night Hours Execution

Limit to 0:00-8:30:
```json
{ "kind": "cron", "expr": "*/30 0-8 * * *", "tz": "Asia/Shanghai" }
```

Time range reference:
| Range | Expression |
|-------|-----------|
| 0:00-8:30 (every 30min) | `*/30 0-8 * * *` |
| 0:00-8:45 (every 15min) | `*/15 0-8 * * *` |
| 0:00-8:00 (hourly) | `0 0-8 * * *` |
| 22:00-5:30 (cross-day) | `*/30 22-23,0-5 * * *` |

Use `0-8` not `0-9` — the last execution at `*/30` would be 8:30, not 9:00.
