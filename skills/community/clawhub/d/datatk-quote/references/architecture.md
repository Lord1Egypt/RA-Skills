# QuoteNode REST Architecture Summary

This document is a concise summary for skill usage. It keeps only the facts needed for REST integration.

## 1. System Role

- QuoteNode is a unified downstream access layer that exposes REST OpenAPI and WebSocket interfaces.
- This skill covers REST only. It does not repeat upstream market-data HTTP or WebSocket protocol details.

## 2. REST Integration Essentials

- Downstream clients pass credentials through the `X-API-KEY` header.
- All external input is treated as untrusted. The server validates `ak`, `endpoint`, `market`, and `instrument` with trimming, length checks, and enum checks.
- HTTP and gRPC entrypoints both pass through the `OpenAPIAuthorize` middleware.

## 3. OpenAPI Middleware Responsibilities

- Extract `ak + endpoint` from the request.
- Derive `market` from the request body:
  - Prefer parsing it from `instrument`.
  - The `Holiday` endpoint uses the `market` field directly.
  - Unknown endpoints are rejected by default.
- Check whether the current AK has access to the requested `market + endpoint` through the authorization snapshot.
- Apply single-node sliding-window rate limiting based on `ak|endpoint|market`.

## 4. Authorization and Limits

- Authorization data is maintained in a snapshot cache by `CustomerRepo`.
- `CustomerUseCase` tries to refresh once at startup and then performs a full refresh every 5 minutes.
- OpenAPI permissions are checked by `ak + market + endpoint`. Requests are rejected if the quota is missing or equal to `0`.
- Historical KLine bar-count limits apply only to KLine endpoints. The limit is injected into context and then enforced later in the business flow.

## 5. REST Contract Source

- The external contract is defined in `api/quote/openapi/v1/openapi.proto`.
- Generated files are under `internal/api/quote/openapi/v1/*` and should not be edited manually.

## 6. How to Use This Reference

- If you need to know which endpoint to call, start with `references/openapi.md`.
- If you need field meanings, read `references/response.md`.
- If you need enum values or error codes, read `references/reference.md`.
