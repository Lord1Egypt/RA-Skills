# Agent Dashboard Sync - Security Rules (Publish-Safe)

Apply these rules to all agents using this skill.

## A. Secret Hygiene (Mandatory)

1. Never hardcode tokens, keys, passwords, cookies, or session identifiers in repo files.
2. Never paste raw secrets in chat screenshots, logs, or commit messages.
3. Use placeholders in docs/examples: `<REDACTED>`, `<INGEST_TOKEN>`, `<READ_TOKEN>`.
4. Store runtime secrets only in secret managers (`wrangler secret`, Vercel env, system keychain).
5. Rotate secrets immediately if exposed in chat/log/git history.

## B. Environment Variable Policy

1. Only non-sensitive values may use `NEXT_PUBLIC_*`.
2. Keep `DASHBOARD_READ_TOKEN`, `INGEST_TOKEN`, `REPORT_TOKEN` server-side only.
3. Validate env presence at startup; fail fast with clear error if missing.
4. Separate production and development secrets; never reuse by default.

## C. Transport & Auth

1. Require HTTPS for all ingest/read endpoints.
2. Require Bearer auth on `POST /ingest` and `GET /fleet`.
3. Reject unauthenticated/invalid token requests with `401`.
4. Enforce payload size limit and JSON schema validation.
5. Add basic rate limiting (per IP or token) for ingest endpoint.

## D. Data Minimization

1. Send only operational telemetry (status/heartbeat/cron/runtime/events).
2. Do not include chat content, user PII, or credential-bearing command output.
3. Truncate long `last_error` fields and redact obvious secret patterns.
4. Keep events ring buffer bounded (e.g., max 200/500) to reduce exposure.

## E. Logging & Auditing

1. Never log full Authorization headers or secret env values.
2. Log only request metadata needed for troubleshooting (timestamp, agent_id, status code).
3. Add clear audit events for auth failures and schema validation failures.
4. Retain minimal logs; define retention period explicitly.

## F. Deployment Controls

1. Deploy only from trusted local project roots; in published docs use `<PROJECTS_ROOT>` placeholder, not absolute paths.
2. Require explicit human confirmation before production token changes.
3. Use least privilege Cloudflare token scopes.
4. Pin compatibility date and review release notes before upgrades.

## G. Cron / Collector Rules (No-LLM Path)

1. Collector must be deterministic script; no LLM/API inference calls.
2. Run at fixed interval (recommended `*/2 * * * *`).
3. On failure, retry next schedule; do not spin loops.
4. Write concise local logs and avoid sensitive payload dumps.

## H. Publication Gate (Before releasing skill)

1. Run secret scan against skill folder and references.
2. Verify all examples use placeholders, not real domains/tokens where sensitive.
3. Verify no `.env`, `.dev.vars`, or credential files are included.
4. Run a second-person review checklist before publish.

## I. Incident Response (If leak suspected)

1. Revoke/rotate exposed tokens immediately.
2. Redeploy Worker with new secrets.
3. Invalidate old dashboard env values and redeploy.
4. Record incident summary + prevention action in operations notes.
