# Cron & Heartbeat Templates

## Option A: Heartbeat (Recommended)

Add to HEARTBEAT.md — runs every heartbeat cycle (typically 15-30 min):

```markdown
## Mesh Inbox
Run: `bash {baseDir}/scripts/mesh-poll.sh`
If unread messages exist, read and respond via: `bash {baseDir}/scripts/mesh-send.sh <to_agent> "<reply>"`
If empty, skip silently.
```

Env vars are injected automatically via `skills.entries.agent-mesh.env` — no manual sourcing needed.

Pros: Simple, batches with other tasks, no extra config.
Cons: Response time depends on heartbeat interval.

## Option B: Dedicated Cron (Fast Polling)

For agents that need faster response:

```
openclaw cron add \
  --name "mesh-poll" \
  --every 5m \
  --model anthropic/claude-haiku-4-5 \
  --task "Run: bash {baseDir}/scripts/mesh-poll.sh
If messages found, process and reply via: bash {baseDir}/scripts/mesh-send.sh <agent> '<reply>'
If no messages, reply NO_REPLY."
```

Use Haiku for the poll cron — it just runs a script and relays output.

## Option C: Dedicated Cron (Complex Tasks)

When the mesh carries complex work:

```
openclaw cron add \
  --name "mesh-relay" \
  --every 10m \
  --model anthropic/claude-sonnet-4-5 \
  --task "MESH RELAY:
1. Run: bash {baseDir}/scripts/mesh-poll.sh
2. If no messages, reply NO_REPLY.
3. For each message, compose a substantive reply with data or results.
4. Send: bash {baseDir}/scripts/mesh-send.sh <from_agent> '<reply>'
5. Skip stale follow-up/check-in messages."
```

## Poll Interval Guide

| Use case | Interval | Model | Cost |
|----------|----------|-------|------|
| Real-time collab | 2-5 min | Haiku | Low |
| Standard async | 10-15 min | Haiku/Sonnet | Moderate |
| Complex tasks | 10 min | Sonnet/Opus | Higher |
| Low priority | 30-60 min | Haiku | Minimal |

## Monthly Maintenance

Run archival queries directly in Supabase SQL Editor (see `references/supabase-setup.md`). Do not embed credentials in cron task strings.
