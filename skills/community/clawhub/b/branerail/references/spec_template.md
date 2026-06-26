# Architectural Specification Template

Use this template when designing any new component or system. Fill it out completely before prompting Claude Code. This is your contract with the AI.

---

## Component Name
[e.g., Order Processing Service, User Authentication, Payment Gateway Integration]

## Overview (2-3 sentences)
What does this component do? Who depends on it?

---

## Purpose and Scope

### What Problem Does This Solve?
- List the core use cases.
- What pain points are we addressing?

### What Is Out of Scope?
- What are we explicitly NOT handling?
- What's delegated to other components?

---

## Data Model

### Inputs
**Description**: What data does this accept?

| Field | Type | Required | Constraints | Example |
|-------|------|----------|-------------|---------|
| orderId | string | yes | UUID format, max 36 chars | `"ORD-2026-04-27-12345"` |
| amount | number | yes | Positive, 2 decimal places | `99.99` |
| currency | string | yes | ISO 4217 code | `"USD"` |

### Outputs
**Description**: What data does this produce?

| Field | Type | Constraints | Example |
|-------|------|-------------|---------|
| transactionId | string | UUID format | `"TXN-2026-04-27-67890"` |
| status | enum | PENDING, COMPLETED, FAILED | `"COMPLETED"` |
| timestamp | ISO 8601 | UTC | `"2026-04-27T10:30:45Z"` |

---

## State and Ownership

### State Owned by This Component
- List every mutable piece of data this component owns.
- Example: Order status, payment confirmation, retry count.

| State | Owner | Type | Persistence | Mutable By | Read By |
|-------|-------|------|-------------|-----------|---------|
| Order Status | Order Service | enum | Database | Order Service | All services |
| Payment Receipt | Payment Service | JSON | Database + Cache | Payment Service | Order Service, UI |
| Retry Count | Payment Service | integer | In-memory | Payment Service | Payment Service only |

### State Read (Not Owned)
- What data does this read but not modify?
- Where does it read from?

| State | Owner | Source | Freshness | Fallback |
|-------|-------|--------|-----------|----------|
| User Preferences | User Service | API call | Real-time | Cached defaults |
| Inventory Levels | Inventory Service | Cache | 5 min old | Query DB if missing |

### Consistency Model
- Is this eventually consistent or strongly consistent?
- How are conflicts resolved?

Example:
```
Order status is strongly consistent (single source of truth in DB).
Payment cache can be stale up to 5 minutes; conflicts resolved by 
reading from DB on mismatch.
```

---

## Critical Paths and Performance

### Happy Path (Success Scenario)
1. User submits order.
2. Order Service validates and stores order.
3. Order Service calls Payment Service.
4. Payment Service charges gateway; stores receipt.
5. Order Service updates status to COMPLETED.
6. Notification Service queues confirmation email.

**Target Latency**: p50 < 500ms, p95 < 2s, p99 < 5s

### Alternative Paths (Common Scenarios)
- **Retry**: What if payment gateway times out?
- **Fallback**: What if cache is down?
- **Degradation**: What if a non-critical service is slow?

### Bottlenecks and Constraints
- Database write latency: ~10ms per order
- Payment gateway API: ~2s per transaction
- Queue throughput: 1000 events/sec max
- Memory: Caching 10K orders (assume 1KB each = 10MB)

---

## Failure Modes and Recovery

Define what can go wrong and how you respond.

| Failure | Probability | Impact | Detection Method | Recovery Strategy | Time to Recover |
|---------|-------------|--------|------------------|-------------------|-----------------|
| Payment gateway timeout | High (5%) | Order stuck in PENDING | Timeout after 5s | Retry 3x with exponential backoff | < 30s |
| Database connection lost | Medium (0.1%) | Cannot write state | Connection error | Circuit breaker; queue locally | < 10s (auto-failover) |
| Cache miss under load | Medium (1%) | Reads hit DB directly | Latency spike | Return data from DB; repopulate cache | < 1s |
| Invalid input (bad amount) | High (2%) | Reject order | Schema validation | Log, reject with error, alert | Immediate |
| Cascade from downstream | Medium (0.5%) | Cannot notify user | Notification service down | Queue message, retry later | < 1 hour |
| Concurrency conflict | Low (0.01%) | Two orders claim same slot | Constraint violation | Detect, rollback, retry | < 5s |

---

## Observability

### Logging Strategy
**What gets logged?** Every operation with context.

```json
{
  "timestamp": "2026-04-27T10:30:45.123Z",
  "service": "order-processor",
  "operation": "process_payment",
  "severity": "INFO",
  "orderId": "ORD-2026-04-27-12345",
  "customerId": "CUST-67890",
  "amount": 99.99,
  "status": "success",
  "latency_ms": 450,
  "retries": 0,
  "trace_id": "tr-abc123def456"
}
```

**Log Levels**:
- ERROR: Failed operation (payment rejected, DB connection lost)
- WARN: Degraded operation (retry attempt 2 of 3, cache miss)
- INFO: Normal operation (payment succeeded, order created)
- DEBUG: Detailed traces (SQL queries, network calls)

### Metrics to Emit

| Metric | Type | Labels | Target |
|--------|------|--------|--------|
| orders_processed | Counter | status=COMPLETED/FAILED/PENDING | 1000/sec |
| payment_latency | Histogram | gateway=stripe | p50=500ms, p99=2s |
| payment_errors | Counter | error_type=timeout/invalid/gateway | < 5% |
| cache_hit_ratio | Gauge | cache_name=orders | > 80% |
| queue_depth | Gauge | queue_name=notifications | < 1000 |

### Alerting Rules

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| Payment Error Rate High | errors > 5% for 5 min | P2 | Notify on-call, check gateway status |
| Database Connection Lost | connection errors > 0 for 1 min | P1 | Page on-call, failover to standby |
| Queue Backlog | queue_depth > 5000 for 10 min | P2 | Scale notification workers, alert |
| Latency Degradation | p99 latency > 10s for 5 min | P2 | Check downstream services, page |

---

## Dependencies

### External Services

| Service | Endpoint | Timeout | Fallback | SLA |
|---------|----------|---------|----------|-----|
| Payment Gateway | stripe.com/v1/charges | 5s | Queue and retry | 99.9% |
| User Service | internal/users | 2s | Cached profile | 99.99% |
| Notification Service | internal/notify | 1s (async) | Queue, retry later | 99% |

### Internal Dependencies

| Component | Why | Failure Mode | Mitigation |
|-----------|-----|--------------|-----------|
| Order Database | Store order state | Cannot write | Write to backup, retry |
| Cache Layer | Speed up reads | Return stale or hit DB | Degrade gracefully |
| Message Queue | Decouple notification | Queue overload | Backpressure, drop old messages |

### Dependency Graph
```
Order Service
  ├─ Database (write order state)
  ├─ Cache (read recent orders)
  ├─ Payment Service (charge user)
  │  └─ Payment Gateway (external)
  └─ Notification Service (send confirmation)
```

**Blast Radius**:
- If Payment Service ↓: Orders can't complete (critical)
- If Cache ↓: Reads slower but still work (non-critical)
- If Notification Service ↓: Orders complete but users don't get email (degraded)

---

## Testing Strategy

### Unit Tests
- [ ] Input validation (valid/invalid amounts, currencies)
- [ ] State transitions (PENDING → COMPLETED)
- [ ] Error handling (timeout, invalid input)

### Integration Tests
- [ ] Order → Payment → Notification flow
- [ ] Database write and read
- [ ] Cache invalidation

### Failure Mode Tests
- [ ] Payment gateway timeout → retry
- [ ] Invalid input → reject gracefully
- [ ] Cascade from downstream → queue and retry

### Load Tests
- [ ] 1000 orders/sec sustained
- [ ] 10K concurrent users
- [ ] Cache hit ratio under load

### Chaos Tests
- [ ] Kill payment service; verify graceful fallback
- [ ] Corrupt cache; verify DB fallback
- [ ] Introduce latency (3s delay); verify timeouts work

---

## Scaling and Limits

### Current Constraints
- Database: ~100 connections, 1000 queries/sec
- Cache: 100MB memory, 10K objects
- Payment gateway API: Rate limit 500 req/sec

### Projected Growth
- Month 1: 100 orders/sec
- Month 6: 500 orders/sec
- Year 1: 1000+ orders/sec

### Scaling Plan
- Add read replicas to database at month 6.
- Shard by user ID at year 1.
- Distribute cache across Redis cluster.
- Use async processing for non-critical paths.

---

## Security

### Authentication & Authorization
- Order Service calls Payment Service: mTLS + signed tokens
- User can only see their own orders: check user_id in request
- Payment Service never logs sensitive data (amount OK, card number NOT OK)

### Input Validation
- Amount: Must be positive number, 2 decimals, max 999,999.99
- Currency: Must be valid ISO 4217 code
- UserId: Must be valid UUID

### Data Protection
- Encrypt payment receipt in database (at-rest encryption)
- HTTPS for all external API calls
- Secrets (API keys) in environment variables, never in code

---

## Deployment and Rollback

### Deployment Checklist
- [ ] All tests passing (unit, integration, load)
- [ ] Database migrations tested
- [ ] Monitoring and alerts in place
- [ ] Runbook documented
- [ ] Rollback plan tested

### Rollback Strategy
- If new code causes > 5% error rate, auto-rollback
- If latency degradation > 50%, manual rollback
- Keep previous 2 versions running for quick switch

---

## Questions Answered

### Where Does State Live?
Order Service is the single source of truth for order status. Payment Service owns payment receipt. Cache is a read-only replica of recent orders from Order Service database.

### Where Does Feedback Live?
Every operation logs with context (orderId, status, latency, errors). Metrics are emitted (order count, latency p50/p95/p99, error rate). Alerts fire on error rate > 5% or latency > 10s.

### What Breaks If I Delete This?
If Order Service is deleted, no orders can be created (critical). If Payment Service is deleted, orders queue locally and retry later (degraded but recoverable). If Cache is deleted, reads hit database directly (slower but functional).

---

## Sign-Off

| Role | Name | Date | Notes |
|------|------|------|-------|
| CTO / Tech Lead | | | Approved design |
| Engineering Lead | | | Approved implementation plan |
| Ops / SRE | | | Approved monitoring and runbook |
| Product | | | Approved user impact and rollout |

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-04-27 | [Your Name] | Initial spec |
| | | | |
