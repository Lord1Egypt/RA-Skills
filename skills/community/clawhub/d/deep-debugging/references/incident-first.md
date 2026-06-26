# Incident-First Debugging Reference

Use this when the failure is production-like, user-facing, money/auth/data related, or caused by a deploy/config/provider change.

## Severity guide

| Severity | Use when | Default posture |
|---|---|---|
| low | local/staging, easy workaround | debug normally |
| medium | limited users/flow affected | minimal fix, monitor |
| high | major user flow broken, auth broken, repeated 500s | stabilize first, approval for risky actions |
| critical | data loss/security/payment outage/broad outage | rollback/disable first, preserve evidence |

## 5-minute incident triage

```text
□ Environment: prod, staging, local?
□ Impact: users, tenants, money, auth, data, integrations?
□ Start: exact time, commit, deploy, config, migration, provider event?
□ Current state: error rate, healthcheck, logs, queue backlog?
□ Safety: data loss, auth leak, credential exposure, duplicate side effects?
□ Rollback path: last known good version/config? feature flag? pause job?
□ Evidence preserved: request ID, deploy ID, commit SHA, redacted log snippet?
```

## Stabilization choices

Prefer the least risky action that reduces harm:

1. **No-op + monitor** — if impact is low and evidence collection matters more.
2. **Feature flag / disable job** — when one feature/job causes damage.
3. **Rollback** — when a recent deploy/config is strongly correlated.
4. **Hotfix** — only when root cause is proven or rollback is worse.
5. **Manual repair** — database/data fixes require explicit approval and backup plan.

## Deploy/runtime failure checklist

```text
□ Build passed but runtime crashes? inspect start logs.
□ Healthcheck path/port/protocol changed?
□ Required env key missing or renamed? print key names only.
□ Runtime version changed? Node/Python/package manager mismatch?
□ Migration required before code? migration backward-compatible?
□ Container/host lacks file, permission, binary, or native dependency?
□ Recent dependency update changed behavior?
□ Last green deploy exists and can be restored?
```

## Live HTTP 500 checklist

```text
□ Exact endpoint/job/component and request ID captured?
□ Does stack trace point to app code, DB, network, or provider?
□ All users or specific role/input/tenant?
□ Any correlation with last deploy/config/migration/provider event?
□ Is the error deterministic with safe test data?
□ Are retries causing duplicate writes or queue explosions?
□ Is there a safe fallback/disable path?
```

## Auth/session outage checklist

```text
□ 401 vs 403 separated?
□ Login creates token/session/cookie? Do not print token.
□ Follow-up request sends token/cookie? inspect presence/header names only.
□ Signing/validation config uses same key source? never print values.
□ Cookie SameSite/Secure/domain/path changed?
□ CORS/credentials mode changed?
□ Clock skew/token expiry changed?
□ Role/tenant guard changed independently from auth?
```

## Webhook/API integration checklist

```text
□ Provider status page checked?
□ Rate limit/quota/exhaustion visible?
□ Signature verification failing after secret rotation? key version only.
□ Payload schema changed? store redacted shape, not raw data.
□ Retry policy and idempotency key behavior safe?
□ First failing event compared with last successful event?
□ Network/DNS/TLS/proxy changed?
□ Backfill/replay needed? requires explicit approval.
```

## Incident closeout

```text
Root cause:
Detection gap:
Prevention:
Rollback/runbook note:
Remaining risk:
```
