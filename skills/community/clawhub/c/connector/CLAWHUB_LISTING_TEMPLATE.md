# ClawHub Listing Template (launchthat-openclaw-connector)

Use this template for your public package listing on `https://clawhub.ai/`.

## Title

LaunchThat OpenClaw Connector (Secure Agent Visualization Bridge)

## One-line Summary

Securely streams OpenClaw agent state to LaunchThatBot for live office-style visualization without exposing local secrets or unrelated instance data.

## Description

LaunchThat OpenClaw Connector connects an existing OpenClaw instance to LaunchThatBot using an auth-link flow and scoped ingest token. It sends only canonical operational events (agent status, room movement, and task lifecycle updates) to power real-time visualization dashboards.

This connector is built with least-privilege defaults:

- outbound-only HTTPS calls to LaunchThatBot APIs,
- no shell command execution,
- no arbitrary filesystem access,
- no environment variable enumeration or upload.

## Permissions & Access Model

- **Network:** outbound requests to configured LaunchThatBot base URL only.
- **Filesystem:** optional queue file for resilient delivery (`~/.config/launchthat-openclaw/queue.json` by default).
- **Runtime:** no subprocess execution and no dynamic code evaluation.
- **Secrets:** ingest token and signing secret accepted via env var, secure file, or interactive prompt.

## Data Collected / Sent

### Sent to LaunchThatBot

- `eventId`, `eventType`, `occurredAt`, `idempotencyKey`
- optional `agent`, `room`, `task` canonical fields
- optional event `metadata` map

### Not collected by default

- OpenClaw prompts / chat transcripts
- arbitrary env vars
- unrelated OpenClaw instance state
- local files outside explicitly provided token/secret files

## Security Controls

- token validation server-side with hashed token comparison
- optional HMAC signature enforcement (`OPENCLAW_REQUIRE_SIGNATURE=true`)
- replay-window protection via signed timestamp checks
- server rate limiting for ingest and heartbeat
- idempotency de-duplication per instance/event key
- restrictive queue file permissions (`0700` dir, `0600` file)

## Threat Model (Short)

- **Credential theft risk:** mitigated by env/file secret input and token rotation/revocation.
- **Payload tampering risk:** mitigated by optional HMAC request signatures.
- **Replay risk:** mitigated by signature timestamp skew checks and idempotency keys.
- **DoS / abuse risk:** mitigated by per-instance endpoint rate limits.
- **Data over-collection risk:** mitigated by canonical event schema and explicit non-goals.

## Installation

```bash
pnpm add launchthat-openclaw-connector
```

## Quick Start

```bash
# 1) Create auth link
lt-openclaw-connect auth-link \
  --base-url=https://app.launchthatbot.com \
  --workspace-id=default \
  --instance-name=my-openclaw

# 2) After callback, set secrets
export LAUNCHTHAT_INGEST_TOKEN="<token>"
export LAUNCHTHAT_SIGNING_SECRET="<signing-secret>"

# 3) Run connector
lt-openclaw-connect run \
  --base-url=https://app.launchthatbot.com \
  --workspace-id=default \
  --instance-id=<instanceId>
```

## Operator Checklist

- enable `OPENCLAW_REQUIRE_SIGNATURE=true` in production
- use long random `OPENCLAW_SIGNING_SECRET`
- rotate ingest tokens periodically
- restrict egress to LaunchThatBot domain
- run under dedicated low-privilege OS user

## Support / Disclosure

Security reporting and policy: see `SECURITY.md`.
