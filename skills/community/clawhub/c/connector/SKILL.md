---
name: launchthat-openclaw-connector
description: Deprecated legacy connector skill. Use @launchthatbot/connect-openclaw-plugin for all new LaunchThatBot OpenClaw connect flows with configurable permissions.
---

# LaunchThat OpenClaw Connector

> Deprecated: this skill is being phased out.
> Use `@launchthatbot/connect-openclaw-plugin` instead.

## When to use this skill

Use this skill when you need to:

- connect an existing OpenClaw VPS to LaunchThatBot,
- configure secure ingest token + request signing,
- validate heartbeat/ingest/replay behavior,
- troubleshoot connection, auth, or payload issues.

Do not use this skill for:

- deploying OpenClaw infrastructure,
- managing unrelated bot runtime logic,
- reading local secrets outside explicitly provided token/secret inputs.

## Security boundaries

- Outbound-only network calls to LaunchThatBot API endpoints.
- No shell execution from connector runtime.
- No arbitrary filesystem reads (only explicit token/secret files and optional queue file).
- Canonical event schema only (`agent_status_changed`, `agent_moved_room`, `task_started`, `task_completed`, `room_updated`).
- Optional HMAC request signing with timestamp skew checks.

## Source-of-truth policy

- Connector implementation changes must be made in this monorepo package: `packages/launchthat-openclaw-connector`.
- The mirrored `launchthatbot/connect` repo is a distribution mirror, not a primary authoring surface.
- Use the sync workflow/runbook to propagate updates and avoid multi-writer divergence.

## Quick setup workflow

1. Create auth link:

```bash
lt-openclaw-connect auth-link \
  --base-url=https://app.launchthatbot.com \
  --workspace-id=default \
  --instance-name=my-openclaw
```

2. Open returned `authUrl`, capture:
   - `instanceId`
   - `ingestToken`

3. Export secrets:

```bash
export LAUNCHTHAT_INGEST_TOKEN="<token>"
export LAUNCHTHAT_SIGNING_SECRET="<shared-signing-secret>"
```

4. Run connector:

```bash
lt-openclaw-connect run \
  --base-url=https://app.launchthatbot.com \
  --workspace-id=default \
  --instance-id=<instanceId>
```

## Operational checks

- Heartbeat endpoint returns `200`.
- Ingest endpoint returns `ok: true`.
- Replay endpoint returns recent events.
- LaunchThatBot dashboard reflects active connected instance.

## Common troubleshooting

- **401 Invalid token**: refresh callback and rotate ingest token.
- **401 Invalid request signature**: verify `OPENCLAW_SIGNING_SECRET` and clock skew.
- **429 Rate limit exceeded**: reduce burst size/retry cadence.
- **No UI updates**: verify replay endpoint contains events for current instance/workspace.

## Additional resources

- Setup/security details: [README.md](README.md)
- Security policy and disclosure: [SECURITY.md](SECURITY.md)
- ClawHub listing content: [CLAWHUB_LISTING_TEMPLATE.md](CLAWHUB_LISTING_TEMPLATE.md)
- Publish flow: [CLAWHUB_PUBLISH_RUNBOOK.md](CLAWHUB_PUBLISH_RUNBOOK.md)
