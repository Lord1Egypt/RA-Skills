# Example: Architecture Review Report

This is a sample output demonstrating how the skill produces a review report.
The example is based on a fictional e-commerce platform with OpenSpec.

---

# Architecture Review Report

**Project**: acme-commerce
**Date**: 2026-05-11
**Spec Source**: openspec/specs/
**Mode**: full

---

## Scoreboard

| Dimension | Score | Verdict |
|-----------|-------|---------|
| Modularity and Boundaries | 8/10 | 🟡 Adequate |
| Data Flow and State Management | 6/10 | 🟠 Needs Improvement |
| Scalability | 7/10 | 🟡 Adequate |
| Fault Tolerance and Resilience | 4/10 | 🟠 Needs Improvement |
| Security | 9/10 | ✅ Excellent |
| Observability | 5/10 | 🟠 Needs Improvement |
| Developer Experience | 7/10 | 🟡 Adequate |
| Spec-Code Consistency | 6/10 | 🟠 Needs Improvement |

**Overall Score**: 6.5/10

---

## Modularity and Boundaries — 8/10 🟡

### Strengths
- Clear domain separation: `orders/`, `inventory/`, `payments/`, `users/` map directly to OpenSpec domains
- Dependency direction is consistent — all modules depend inward toward `core/domain/`
- Internal types (e.g., `OrderAggregate`) are not exposed outside their module

### Weaknesses
- `shared/utils/` has grown to 47 files and is imported by every module — becoming a de facto god module
- `notifications/` depends directly on `orders/` internal types instead of using events

### Recommendations

| # | Priority | Recommendation | Related Spec/Code |
|---|----------|---------------|-------------------|
| 1 | Medium | Split shared/utils/ into focused packages (validation, formatting, http) | src/shared/utils/ |
| 2 | Medium | Replace direct import in notifications/ with domain events from orders/ | Requirement: Order Confirmation Notification |

---

## Data Flow and State Management — 6/10 🟠

### Strengths
- Cart state uses event sourcing pattern with clear append-only log
- API responses follow consistent envelope format

### Weaknesses
- Inventory count is cached in both `orders/` and `inventory/` services with no sync mechanism — can drift
- Order status is updated in 3 places: OrderService, PaymentWebhook handler, and a background job

### Recommendations

| # | Priority | Recommendation | Related Spec/Code |
|---|----------|---------------|-------------------|
| 1 | High | Designate inventory/ as single source of truth for stock counts; orders/ must query it | Requirement: Stock Reservation |
| 2 | High | Consolidate order status transitions into OrderStateMachine; other components emit events, only OrderStateMachine mutates | src/orders/services/OrderService.ts, src/payments/webhooks/stripe.ts |

---

## Fault Tolerance and Resilience — 4/10 🟠

### Strengths
- Payment gateway calls have timeout configuration (30s)
- Idempotency key implemented for payment creation

### Weaknesses
- No circuit breaker on external API calls (shipping provider, email service)
- Retry logic in queue consumers has no backoff — can cause thundering herd on provider recovery
- Inventory reservation has no compensation/rollback on payment failure

### Recommendations

| # | Priority | Recommendation | Related Spec/Code |
|---|----------|---------------|-------------------|
| 1 | High | Add circuit breaker (e.g., opossum) to all external HTTP calls | src/integrations/*.ts |
| 2 | High | Implement exponential backoff with jitter on queue retry | src/workers/orderProcessor.ts |
| 3 | High | Implement saga/compensation: release inventory reservation when payment fails within timeout | Requirement: Payment Failure Handling |

---

## Security — 9/10 ✅

### Strengths
- JWT-based auth with short-lived access tokens + refresh token rotation
- All API inputs validated with zod schemas at controller boundary
- Secrets loaded from environment via vault integration, not in code
- Rate limiting on auth endpoints (5 attempts / minute)

### Weaknesses
- Admin API endpoints lack audit logging for destructive operations

### Recommendations

| # | Priority | Recommendation | Related Spec/Code |
|---|----------|---------------|-------------------|
| 1 | Low | Add audit log entries for all admin PATCH/DELETE operations | Requirement: Admin Actions Audit Trail |

---

## Observability — 5/10 🟠

### Strengths
- Structured JSON logging with consistent timestamp and level fields
- Basic health check endpoints exist

### Weaknesses
- No correlation ID propagated across services — impossible to trace a request end-to-end
- Metrics are limited to default runtime metrics; no business metrics (orders/min, conversion rate)
- No alerting defined; failures detected by customer reports

### Recommendations

| # | Priority | Recommendation | Related Spec/Code |
|---|----------|---------------|-------------------|
| 1 | High | Implement X-Request-ID header propagation across all service boundaries | All services |
| 2 | High | Add RED metrics (Request rate, Error rate, Duration) per endpoint | Requirement: SLA Compliance |
| 3 | Medium | Define SLO-based alerts (e.g., p99 latency > 2s, error rate > 1%) | ops/alerting/ |

---

## Developer Experience — 7/10 🟡

### Strengths
- Consistent REST naming conventions across all services
- Docker Compose setup for local development
- Comprehensive README with setup instructions

### Weaknesses
- No API documentation generated from code (Swagger/OpenAPI)
- Test suite takes 4+ minutes locally; no watch mode configured

### Recommendations

| # | Priority | Recommendation | Related Spec/Code |
|---|----------|---------------|-------------------|
| 1 | Medium | Generate OpenAPI spec from route decorators; serve via /docs | src/api/ |
| 2 | Medium | Add vitest watch mode and split unit/integration test commands | package.json |

---

## Spec-Code Consistency — 6/10 🟠

### Strengths
- Core order flow (place, pay, fulfill) fully implemented per spec
- Scenarios in auth spec map 1:1 to integration tests

### Weaknesses
- Requirement "Partial Refund Processing" specified in spec but not implemented
- Background job for "Abandoned Cart Recovery" exists in code but has no corresponding spec requirement
- 3 spec scenarios in notifications/ have no matching test cases

### Recommendations

| # | Priority | Recommendation | Related Spec/Code |
|---|----------|---------------|-------------------|
| 1 | High | Implement or explicitly defer Requirement: Partial Refund Processing | openspec/specs/payments/spec.md |
| 2 | Medium | Add spec requirement for abandoned cart recovery (currently a dark feature) | src/workers/cartRecovery.ts |
| 3 | Medium | Write tests for notification scenarios: Email Bounce, SMS Fallback, Digest Preference | openspec/specs/notifications/spec.md |

---

## Top Critical Issues

### Issue 1: Fault Tolerance and Resilience (Score: 4/10)

**Root Cause**: External service integrations were added incrementally without a shared resilience strategy. Each integration handles (or doesn't handle) failures independently.

**Impact**: A shipping provider outage cascades into order processing failures; retry storms can amplify partial outages into full outages.

**Suggested Fix**: Introduce a shared HTTP client wrapper with circuit breaker, timeout, and exponential backoff configured by default. Apply to all external calls in src/integrations/.

### Issue 2: Observability (Score: 5/10)

**Root Cause**: Observability was not treated as a first-class concern during initial development. Logging exists but lacks the correlation and metrics needed for production debugging.

**Impact**: Mean-time-to-detect (MTTD) is measured in hours (customer reports), not seconds. Debugging production issues requires reading raw logs without context.

**Suggested Fix**: Add correlation ID middleware as the first priority — this unblocks all downstream observability improvements.

### Issue 3: Data Flow and State Management (Score: 6/10)

**Root Cause**: As the system grew, state ownership was not explicitly assigned. Multiple services evolved to maintain their own copy of shared data.

**Impact**: Inventory drift causes overselling; order status inconsistency causes customer confusion and support burden.

**Suggested Fix**: Introduce explicit ownership: one service owns each piece of state, others subscribe to events or query on demand.

---

## Consolidated Recommendations

| # | Priority | Recommendation | Dimension | Related Spec/Code |
|---|----------|---------------|-----------|-------------------|
| 1 | High | Add circuit breaker to all external HTTP calls | Resilience | src/integrations/*.ts |
| 2 | High | Implement exponential backoff with jitter on queue retry | Resilience | src/workers/orderProcessor.ts |
| 3 | High | Implement saga/compensation for payment failure | Resilience | Requirement: Payment Failure Handling |
| 4 | High | Designate single source of truth for inventory counts | Data Flow | Requirement: Stock Reservation |
| 5 | High | Consolidate order status transitions into state machine | Data Flow | src/orders/ |
| 6 | High | Implement X-Request-ID correlation across services | Observability | All services |
| 7 | High | Add RED metrics per endpoint | Observability | Requirement: SLA Compliance |
| 8 | High | Implement Requirement: Partial Refund Processing | Spec Consistency | openspec/specs/payments/spec.md |
| 9 | Medium | Split shared/utils/ into focused packages | Modularity | src/shared/utils/ |
| 10 | Medium | Define SLO-based alerts | Observability | ops/alerting/ |
| 11 | Medium | Add spec for abandoned cart recovery | Spec Consistency | src/workers/cartRecovery.ts |
| 12 | Medium | Generate OpenAPI documentation | DevEx | src/api/ |

---

## Next Steps

The following dimensions scored <= 6 and are candidates for interactive discussion:

1. **Fault Tolerance and Resilience** (4/10) — No circuit breakers or backoff on external calls
2. **Observability** (5/10) — Missing correlation IDs and business metrics
3. **Data Flow and State Management** (6/10) — Duplicated state without sync
4. **Spec-Code Consistency** (6/10) — Unimplemented requirements and dark features

Would you like to discuss any of these in detail?
