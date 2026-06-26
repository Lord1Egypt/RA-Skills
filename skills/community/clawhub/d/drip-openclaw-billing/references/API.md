# Drip OpenClaw Billing API Reference (v1.1.0)

## Primary flow (recommended)

1) `POST /v1/runs` start run  
2) `POST /v1/events` emit tool/event timeline  
3) `POST /v1/usage` emit billable usage  
4) `PATCH /v1/runs/:id` finalize status

Use idempotency keys for retry-safe writes.

## OpenClaw identity flow (lightweight)

Use `X-OpenClaw-Identity` with `/openclaw/*` endpoints for lightweight usage tracking.

## Minimal payload guidance

Allowed metadata examples:
- provider name
- endpoint name
- status code
- latency ms
- hashed request fingerprints (`queryHash`)

Do not send:
- raw prompts or model outputs
- auth tokens / credentials
- personal data
- raw request/response bodies

## Failure strategy

- Fail-open for telemetry writes in user-facing paths (configurable)
- Keep idempotency key stable across retries
- Mark run `FAILED` with compact error code when terminal failure occurs

## Verification checklist

- Run appears in Drip dashboard
- Event count matches tool invocation count
- Usage meters increment correctly
- No duplicate usage writes under retry
