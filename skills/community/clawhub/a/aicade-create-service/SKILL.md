---
name: aicade-create-service
description: Use when preparing signed AICADE gateway service-management requests for service registration, service detail queries, or service disable operations, especially when collecting service metadata, auth config, billing, rate limits, JSON Schemas, serviceId, or signed curl output.
metadata:
  openclaw:
    emoji: "🧩"
    requires:
      bins: [node]
---
`READ BEFORE INSTALL`
This skill covers signed AICADE gateway service management:
1. Register/update service: `POST /admin/gateway/services`
2. Query service detail: `GET /admin/gateway/services/{serviceId}`
3. Disable service: `PATCH /admin/gateway/services/{serviceId}/status?enabled=false`
`READ BEFORE INSTALL`

# aicade-create-service

Use this skill to prepare, validate, and generate signed AICADE gateway service-management requests.

## Core Principle

Treat every operation as a guided, signed flow.

Do not directly generate requests from examples. First ask focused questions, confirm the user's answers, then generate the final JSON or signed curl.

The first time this skill is used in a session, confirm the service-management base URL:

```text
The default service-management base URL is https://aicadegalaxy.com/agent. Should I use this URL?
```

If the user says no, ask for the actual base URL and reuse it for the rest of the session.

## Required Environment

Check local environment before asking the user:

```bash
node {baseDir}/scripts/build-service-request.mjs env-check --operation register
node {baseDir}/scripts/build-service-request.mjs env-check --operation detail
node {baseDir}/scripts/build-service-request.mjs env-check --operation disable
```

Use existing local values without asking again:

- `AICADE_API_KEY`: sent as `X-API-Key`
- `AICADE_API_SECRET_KEY`: used to generate `X-Signature`

Ask only for missing values. `SECRET_KEY` is accepted as a compatibility alias for `AICADE_API_SECRET_KEY`.

## Workflow

### 1. Identify Operation

- **Register/update**: collect and confirm full camelCase registration JSON.
- **Detail**: collect and confirm `serviceId`.
- **Disable**: collect and confirm `serviceId`; do not ask for operator.

### 2. Load References

Read these references when needed:

- `references/register-intake.md` for registration questions
- `references/service-operations-intake.md` for detail and disable questions
- `references/service-management-api.md` for signed API rules, fields, and errors

### 3. Register Intake

Collect registration fields in small groups:

1. Service identity: `serviceId`, `serviceName`, `description`, `tags`
2. Endpoint and route: `endpointUrl`, `requestMethod`, `routePath`, `stripPrefix`, `routeOrder`, `timeoutMs`, `enabled`
3. Outbound auth: `authType`, `authLocation`, `outboundAuth`
4. Contract: `inputSchema`, `outputSchema`
5. Billing: `billingType`, `currency`, prices, limits, `fallbackStrategy`
6. Rate limits: service/user/IP limits and token limits
7. Final review: show assembled JSON and ask for confirmation before generating signed curl

Use camelCase request body fields. Do not emit old snake_case fields such as `service_id`, `endpoint_url`, `input_schema`, or `rate_limits`.

### 4. Validate Register JSON

Before generating signed curl, check:

- `AICADE_API_KEY` and `AICADE_API_SECRET_KEY` are available.
- base URL has been confirmed.
- `serviceId` uses lowercase letters, digits, and hyphens only, length 3-64.
- `endpointUrl` starts with `http://` or `https://`.
- `routePath` starts with `/`; add it if the user omitted it.
- `timeoutMs` is between `1000` and `300000` when set.
- `stripPrefix` is between `0` and `10` when set.
- `inputSchema` and `outputSchema` are present.
- `billing.billingType`, `billing.currency`, and `billing.fallbackStrategy` are present.
- `outboundAuth` exists when `authType` is not `NONE`.

### 5. Generate Requests

Use `scripts/build-service-request.mjs` to print signed curl. The script generates:

- `X-Client-Time`
- `X-Nonce`
- `X-Content-MD5`
- `X-Signature`

The script does not call the remote API; it only prints curl.

## Endpoint Summary

| Operation | Method | Path / Query | Required headers |
| --- | --- | --- | --- |
| Register/update | `POST` | `/admin/gateway/services` | `X-API-Key`, `X-Client-Time`, `X-Nonce`, `X-Content-MD5`, `X-Signature`, `Content-Type` |
| Detail | `GET` | `/admin/gateway/services/{serviceId}` | `X-API-Key`, `X-Client-Time`, `X-Nonce`, `X-Content-MD5`, `X-Signature` |
| Disable | `PATCH` | `/admin/gateway/services/{serviceId}/status?enabled=false` | `X-API-Key`, `X-Client-Time`, `X-Nonce`, `X-Content-MD5`, `X-Signature` |

## Error Handling

If any service-management API returns `401`, treat it as an API key or signature error.

Check:

- `AICADE_API_KEY`
- `AICADE_API_SECRET_KEY`
- signature path
- signature query
- body MD5
- client timestamp and nonce

Do not diagnose `401` as a service registration JSON, `serviceId`, route, billing, or schema problem.

If the API returns `422`, treat it as request validation failure and inspect the JSON field names and values.

## Common Mistakes

- Do not ask for the base URL repeatedly; confirm once per session, defaulting to `https://aicadegalaxy.com/agent`.
- Do not ask for credentials already present in local environment.
- Do not generate unsigned curl.
- Do not use old `/services` endpoints.
- Do not disable with `POST /services/disable`; use signed `PATCH .../status?enabled=false`.
- Do not ask for or send operator headers.
- Do not use snake_case registration fields.
- Do not reuse a previous `serviceId` unless the user confirms it.

## Files Included

- `references/service-management-api.md`
- `references/register-intake.md`
- `references/service-operations-intake.md`
- `scripts/build-service-request.mjs`
- `assets/register-service.template.json`
- `assets/register-service.example.json`
