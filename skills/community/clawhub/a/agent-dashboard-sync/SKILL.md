---
name: agent-dashboard-sync
description: Sync OpenClaw fleet runtime/heartbeat/cron status to Cloudflare KV and serve dashboard-ready data via Worker API. Use when setting up or operating the Agent Fleet Dashboard data plane (collector, KV schema, Worker ingest/read API, crontab scheduling, and migration away from Git-backed high-frequency state).
---

# Agent Dashboard Sync

Operate dashboard data sync as a no-LLM pipeline.

## Hard Rules

1. Keep high-frequency state out of Git commits.
2. Use Cloudflare Worker + KV for runtime sync.
3. Run collector from local cron (`*/2 * * * *`) and do not call LLM in collector path.
4. Never commit or print production tokens/secrets in files, logs, or screenshots.
5. Do not publish absolute paths in skill docs; use relative paths or placeholders (`<PROJECTS_ROOT>`, `<SHARED_ROOT>`).

## Scope Boundary

- This skill owns: collector, Worker ingest/read API, KV schema, cron deployment, dashboard data source wiring.
- This skill does not own: cross-agent protocol, constitution governance, Discord routing rules.

## KV Data Contract (v1)

- `fleet:registry`
- `fleet:heartbeat:<agent_id>`
- `fleet:cron:<agent_id>`
- `fleet:runtime:<agent_id>`
- `fleet:events:recent`
- `fleet:updated_at`

See `references/schema.md` for payload shape.

## Minimal Rollout

1. Deploy Worker + KV namespace.
2. Configure dashboard env to `cloudflare` mode.
3. Install collector cron on each node with unique `AGENT_ID`.
4. Verify `/health`, then `/fleet`, then dashboard UI.

## Security Checklist

- Store `INGEST_TOKEN` and `READ_TOKEN` as worker secrets.
- Keep dashboard read token server-side (`DASHBOARD_READ_TOKEN`), never client-exposed.
- Keep `NEXT_PUBLIC_*` vars non-sensitive only.
- Redact tokens before sharing commands/logs.

## Runbook Links

- Worker setup and command sequence: `references/worker-setup.md`
- Collector and crontab setup: `references/collector-cron.md`
- Env variable matrix: `references/env-matrix.md`
- Data schema reference: `references/schema.md`
- Security policy for all agents: `references/security-rules.md`
