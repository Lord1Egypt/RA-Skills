---
name: backend-architecture
description: Design backend APIs, services, persistence, and observability with security.
metadata:
  author: RedHat Dev
  version: 1.0.0
  owner: RedHat Dev Agent
  category: fullstack
---

# SKILL: backend-architecture

## Purpose
Design backend systems with clear boundaries: API contracts, services, persistence, observability, and security controls.

## When to Use
- Building a new backend or major subsystem.
- Introducing a new API surface (REST/WebSocket).
- You need a concrete module/service layout and DB model.

## Inputs
- `requirements` (required, string|object): endpoints, behaviors, SLAs, compliance needs.
- `constraints` (optional, string[]): security, latency, cost, runtime, stack limits.
- `data_entities` (optional, string[]): core domain objects.
- `integration_points` (optional, string[]): external services/APIs.

## Steps
1. Define API surface:
   - endpoints/events
   - request/response schema
   - error model (codes/messages)
2. Define security model:
   - authentication method
   - authorization rules
   - rate limits and abuse controls
3. Define service/module boundaries:
   - controllers/handlers
   - domain services
   - repositories/adapters
4. Define persistence:
   - schema/tables/collections
   - migrations
   - idempotency model (if needed)
5. Define observability:
   - structured logs
   - request ids
   - audit trail for sensitive actions
6. Define validation plan (tests + CI hooks).

## Validation
- Every endpoint has authz rules or an explicit â€œpublicâ€ justification.
- Inputs are validated; outputs are consistent with schema.
- Failure modes are explicit (timeouts, retries, fallbacks).

## Output
Architecture spec (example schema):
```yaml
api:
  - method: POST
    path: /v1/...
    auth: required
services: ["..."]
data_model: ["..."]
observability: ["logs", "metrics (optional)"]
validation: ["unit tests", "integration tests"]
```

## Safety Rules
- Do not design systems that require storing secrets in source control.
- Avoid introducing new dependencies unless justified.
- Default to safe failure modes (no partial writes without idempotency).

## Example
Requirement: â€œWebhook ingestion with replay protection.â€
Output: includes idempotency key storage, signature verification, and audit logging.
