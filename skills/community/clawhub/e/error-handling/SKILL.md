---
name: error-handling
description: Deep error handling workflow—taxonomy, user-visible vs internal errors, retries and idempotency, observability, and supportability. Use when standardizing failure modes across APIs, clients, and async workers.
---

# Error Handling

Consistent errors reduce support load and on-call pain. Design a **taxonomy**, **stable codes**, **safe user messaging**, and **operator visibility**—without leaking secrets or stack traces to clients.

## When to Offer This Workflow

**Trigger conditions:**

- Inconsistent HTTP status codes and response bodies
- Retry storms or duplicate side effects from naive retries
- Logs that cannot be tied to user-visible failures

**Initial offer:**

Use **six stages**: (1) classify errors, (2) map to transport, (3) user messaging, (4) retries & idempotency, (5) observability, (6) client SDKs & DX). Confirm REST/GraphQL/gRPC and sync/async patterns.

---

## Stage 1: Classify Errors

**Goal:** Distinguish validation, authentication, authorization, not found, conflict, rate limit, dependency failure, and internal bugs.

**Exit condition:** Table or enum of codes with owning team and meaning.

---

## Stage 2: Map to Transport

**Goal:** Correct HTTP 4xx/5xx; GraphQL errors with extensions; gRPC status codes; optional RFC 7807 Problem Details for JSON APIs.

---

## Stage 3: User Messaging

**Goal:** Actionable copy for end users; opaque support reference id; no internal hostnames, SQL fragments, or stack traces in client responses.

---

## Stage 4: Retries & Idempotency

**Goal:** Retry only safe or idempotent operations; exponential backoff with jitter; align with **idempotency** keys on writes.

---

## Stage 5: Observability

**Goal:** Structured logs with `error.code`, `trace_id`, `user_id` (where allowed); metrics by error class; alerts on error-rate SLO burn.

---

## Stage 6: Client SDKs & DX

**Goal:** Typed errors in SDKs; documented recovery; map codes to user-facing strings in apps consistently.

---

## Final Review Checklist

- [ ] Taxonomy and ownership defined
- [ ] Transport mapping correct and consistent
- [ ] User-safe messages with correlation ids
- [ ] Retry policy matches idempotency story
- [ ] Logs and metrics wired for ops

## Tips for Effective Guidance

- Separate expected validation errors from unexpected 500s in dashboards.
- Pair with **idempotency** for write paths and queues.

## Handling Deviations

- Mobile offline: queue with explicit user-visible sync state.
