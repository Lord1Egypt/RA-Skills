---
name: api-integration
description: Integrate third-party APIs with auth, retries, timeouts, and logging.
metadata:
  author: RedHat Dev
  version: 1.0.0
  owner: RedHat Dev Agent
  category: fullstack
---

# SKILL: api-integration

## Purpose
Integrate external APIs safely (auth, retries, timeouts, error handling, logging) and expose them via a clean internal interface.

## When to Use
- A system must call a third-party REST/WebSocket API.
- You need a reusable client module with predictable behavior.
- You must handle rate limits and transient failures.

## Inputs
- `api_spec` (required, object|string): base URL, endpoints, schemas, rate limits.
- `auth_method` (optional, enum: `none|api_key|oauth|jwt|hmac`).
- `secrets_source` (optional, string): where tokens/keys come from (env/secret manager).
- `error_policy` (optional, string): retry/backoff rules and non-retryable errors.

## Steps
1. Validate API contract and identify required headers/auth.
2. Implement a client module:
   - explicit base URL
   - request timeouts
   - retry with bounded backoff (only for safe/idempotent calls by default)
   - rate limit handling
3. Normalize errors into a stable internal shape.
4. Add logging hooks (request id, endpoint, status, latency; never log secrets).
5. Add tests:
   - mocked responses for determinism
   - at least one failure-path test

## Validation
- Secrets are sourced only from configuration (not hardcoded).
- Retry policy is explicit and bounded.
- Errors are deterministic and observable.

## Output
- Client module path(s)
- Config/env contract
- Usage example (internal call pattern)

## Safety Rules
- Do not paste tokens/keys into code or logs.
- Do not rely on â€œbest effortâ€ network calls without timeouts.
- Avoid `curl | sh` or ad-hoc install scripts as part of integration.

## Example
Integrate â€œVendorAPIâ€:
- `api_spec`: `{ base_url: "...", endpoints: ["/v1/items"] }`
- Output: `src/integrations/vendor/client.ts` with retries and mocked tests.
