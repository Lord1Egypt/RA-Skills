# Code Review Checklist: Architectural Soundness for Claude Code

Use this checklist when reviewing AI-generated code. A code generation agent can produce syntactically correct code that is architecturally unsound. This checklist surfaces those issues.

---

## Quick Summary (3 Minutes)

Answer these three questions first. If you can't answer all three with confidence, the code needs revision.

- [ ] **Where does state live?** (Single source of truth identified?)
- [ ] **Where does feedback live?** (Logging, metrics, error handling present?)
- [ ] **What breaks if I delete this?** (Blast radius and dependencies clear?)

If any is "No," proceed to the detailed sections below.

---

## Section 1: Spec Compliance

**Goal**: Does the generated code satisfy the specification?

### Requirements Checklist

- [ ] All required inputs are handled
- [ ] All required outputs are produced in the correct format
- [ ] All success criteria are met
- [ ] All failure modes listed in the spec are handled
- [ ] Latency targets are met (or code is on path to meet them)
- [ ] Throughput targets are achievable
- [ ] No requirements are silently omitted

### Questions to Ask

1. Does the code accept all required inputs?
2. Does it reject invalid inputs (too large, wrong format, missing required fields)?
3. Does the output match the spec exactly (field names, types, order)?
4. Does it fail gracefully for all listed failure modes?
5. Does the implementation match the architecture sketched in the design?

### Red Flags

- Code accepts inputs the spec doesn't mention (scope creep).
- Code silently ignores required fields.
- Output structure differs from spec (different field names, missing fields).
- Failure modes in spec are missing from implementation.

---

## Section 2: State and Data Ownership

**Goal**: Is state managed coherently?

### Single Source of Truth

- [ ] Each mutable piece of data has a declared owner
- [ ] Non-owners read from the owner, not from cached copies
- [ ] If replicas exist, reconciliation strategy is explicit
- [ ] Write operations go to the owner first
- [ ] Conflict resolution rules are documented (e.g., "last write wins")
- [ ] State schema is versioned; migrations are explicit

### State Flow Questions

1. **Where does each type of data live?** (Database, cache, memory, etc.)
   - Is it authoritative (source of truth) or a replica?
   - If a replica, how does it stay in sync?

2. **Who can mutate this data?** (One component or many?)
   - If many, how are conflicts detected?
   - What is the conflict resolution rule?

3. **What happens if state is lost?** (Database crashes, cache cleared)
   - Can the system recover?
   - Is there a rollback strategy?

4. **Is state idempotent?** (Safe to retry without side effects)
   - Can the same operation be executed twice without duplication?
   - Example: Creating an order with idempotency key prevents double-billing.

### Code Patterns to Check

```typescript
// ❌ BAD: State scattered across components
let orderStatus = "pending";  // In memory
let paymentStatus = "unpaid"; // In cache
// These can diverge; no single source of truth

// ✅ GOOD: Single source of truth
class OrderService {
  async getOrder(orderId) {
    return await db.orders.findById(orderId); // Read from DB
  }
  
  async updateStatus(orderId, status) {
    // Write to DB first (authoritative)
    await db.orders.update(orderId, { status });
    // Invalidate cache if needed
    await cache.delete(`order:${orderId}`);
  }
}
```

### Red Flags

- Multiple components modify the same data without coordination.
- Cache is updated before database (risk of data loss).
- No explicit conflict resolution rule.
- State is global or implicit (hidden in closures or side effects).
- "State is cached for performance" but invalidation strategy is unclear.

---

## Section 3: Error Handling and Resilience

**Goal**: Does the code handle failures gracefully?

### Failure Mode Coverage

For each failure mode in the spec, verify:

- [ ] Failure is detected (explicit error checking, not silent)
- [ ] Error is logged with context (not just "Error: 500")
- [ ] User sees a meaningful error message (not a stack trace)
- [ ] The system recovers or fails safely (not cascading)

### Retry and Timeout Logic

- [ ] External API calls have timeouts (not infinite wait)
- [ ] Retries are used for transient failures (network, timeout)
- [ ] Retry logic includes exponential backoff (not hammering the service)
- [ ] Max retries are set (not infinite retry loop)
- [ ] Retries only happen for idempotent operations (not for side effects)

### Circuit Breaker Pattern

- [ ] External dependencies are protected by circuit breakers
- [ ] Circuit breaker opens after threshold (e.g., 5 failures)
- [ ] Circuit breaker has fallback behavior (fail fast, use cache, queue)
- [ ] Circuit breaker resets after cooldown period

### Example Patterns

```typescript
// ❌ BAD: No error handling
const result = await paymentGateway.charge(amount);
return result; // Crashes if gateway is down

// ✅ GOOD: Error handling with retry
async function chargeWithRetry(amount, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await paymentGateway.charge(amount);
    } catch (error) {
      if (attempt === maxRetries) throw error; // Last attempt failed
      
      const backoff = Math.min(100 * Math.pow(2, attempt - 1), 5000);
      await sleep(backoff);
    }
  }
}

// ✅ GOOD: Circuit breaker
class PaymentCircuitBreaker {
  private failures = 0;
  private lastFailureTime = null;
  private isOpen = false;
  
  async charge(amount) {
    if (this.isOpen) {
      if (Date.now() - this.lastFailureTime > 60000) {
        this.isOpen = false; // Reset after 1 minute
      } else {
        throw new Error("Circuit breaker is open; payment gateway is down");
      }
    }
    
    try {
      const result = await paymentGateway.charge(amount);
      this.failures = 0; // Reset on success
      return result;
    } catch (error) {
      this.failures++;
      this.lastFailureTime = Date.now();
      
      if (this.failures >= 5) {
        this.isOpen = true;
      }
      throw error;
    }
  }
}
```

### Red Flags

- No error handling (try/catch only if you remember to add it)
- Errors are caught but not logged
- Infinite retry loops
- Retries on non-idempotent operations (creates duplicates)
- No timeout on external calls (hangs forever)
- No circuit breaker (cascading failures)

---

## Section 4: Observability (Logging, Metrics, Tracing)

**Goal**: Can you see what the code is doing?

### Logging

- [ ] All critical operations are logged (create, update, delete, API calls)
- [ ] Logs are structured (JSON, key-value pairs, not printf blobs)
- [ ] Logs include context (orderId, userId, requestId, timestamp)
- [ ] Error logs include the error type and message (not just "failed")
- [ ] Sensitive data is NOT logged (passwords, API keys, payment tokens)
- [ ] Log level is appropriate (ERROR for failures, INFO for normal ops, DEBUG for details)

### Logging Example

```typescript
// ❌ BAD: Unstructured, no context
console.log("Order created");
console.log("Error: " + error);

// ✅ GOOD: Structured with context
logger.info("order_created", {
  orderId: "ORD-12345",
  customerId: "CUST-67890",
  amount: 99.99,
  timestamp: new Date().toISOString(),
  traceId: requestContext.traceId
});

logger.error("payment_failed", {
  orderId: "ORD-12345",
  error: error.message,
  errorType: error.code,
  retryCount: 2,
  timestamp: new Date().toISOString(),
  traceId: requestContext.traceId
});
```

### Metrics

- [ ] Request count is tracked (how many operations per second?)
- [ ] Latency is measured (p50, p95, p99)
- [ ] Error rate is tracked (how often does this fail?)
- [ ] Business metrics are tracked (revenue, orders, conversions)
- [ ] Resource usage is monitored (CPU, memory, database connections)

### Tracing

- [ ] Request IDs propagate across service boundaries
- [ ] Spans are created for each major operation
- [ ] Trace data includes timing (start time, duration)
- [ ] Traces are queryable (can you find a specific request?)

### Red Flags

- Code runs with no logging
- Logs are printf-style (hard to parse, hard to search)
- Logs lack context (what request was this? what user?)
- Errors are logged without type or details
- Sensitive data is logged
- No metrics (no visibility into performance)

---

## Section 5: Dependencies and Coupling

**Goal**: What is this code coupled to?

### Dependency Clarity

- [ ] External dependencies are explicit (injected, not imported)
- [ ] All external services have mocked versions for testing
- [ ] Dependencies are documented (what service? what version?)
- [ ] Version constraints are clear (exactly 1.2.3, or >= 1.2.0?)
- [ ] Circular dependencies are eliminated

### Dependency Graph

For each external dependency, document:

| Dependency | Purpose | Failure Mode | Fallback |
|-----------|---------|--------------|----------|
| Payment Gateway | Charge user | API timeout | Queue and retry later |
| Database | Store state | Connection lost | Circuit breaker, fail fast |
| Cache | Speed up reads | Cache miss | Query database directly |

### Loose Coupling

- [ ] Components communicate via contracts (interfaces), not implementation details
- [ ] Message formats are versioned (can evolve without breaking)
- [ ] Components can be deployed independently (no tight timing requirements)
- [ ] Contracts are backward compatible (new code works with old data)

### Red Flags

- Dependencies are global (hidden, not injected)
- "Imports everywhere" (tight coupling)
- No fallback for external services
- Contracts change without versioning
- Circular dependencies (A depends on B, B depends on A)
- Tight timing assumptions (race conditions)

---

## Section 6: Testing Coverage

**Goal**: Is the code tested?

### Unit Tests

- [ ] Happy path is tested
- [ ] Invalid inputs are tested (null, empty, wrong type)
- [ ] Edge cases are tested (boundary conditions, off-by-one)
- [ ] Dependencies are mocked (isolated from external services)

### Integration Tests

- [ ] Happy path with real dependencies is tested
- [ ] Failure modes are tested (timeout, invalid response, error)
- [ ] Data flows correctly through multiple components
- [ ] State is consistent after operations

### Failure Mode Tests

- [ ] External service timeout is tested (does retry work?)
- [ ] Invalid input is tested (does validation reject it?)
- [ ] Database error is tested (does fallback work?)
- [ ] Cascade failure is tested (does circuit breaker work?)

### Performance Tests

- [ ] Latency targets are met under normal load
- [ ] Code scales to projected load (1000 req/sec, 100K concurrent users)
- [ ] Memory usage is acceptable (no leaks, no unbounded growth)
- [ ] Bottlenecks are identified

### Red Flags

- No tests (hope-driven development)
- Only happy path tested (failures are undetected)
- Dependencies are not mocked (integration test, not unit test)
- No performance testing (discover bottlenecks in production)
- Tests are slow (seconds to run); developers skip them

---

## Section 7: Security Checklist

**Goal**: Does the code have obvious security holes?

### Input Validation

- [ ] All inputs are validated (type, length, format)
- [ ] Large inputs are rejected (DoS prevention)
- [ ] Special characters are escaped (SQL injection, XSS prevention)
- [ ] File uploads are validated (type, size)

### Authentication & Authorization

- [ ] User identity is verified (authentication)
- [ ] User permissions are checked (authorization)
- [ ] Tokens are validated (not expired, not tampered)
- [ ] Secrets are not exposed (environment variables, not hardcoded)

### Data Protection

- [ ] Sensitive data is encrypted at rest (passwords, payment info)
- [ ] Sensitive data is encrypted in transit (HTTPS, not HTTP)
- [ ] Sensitive data is not logged (never log passwords or tokens)
- [ ] Old data is securely deleted (not just marked as deleted)

### API Security

- [ ] Rate limiting is enforced (prevent brute force, DoS)
- [ ] CSRF tokens are used (prevent cross-site request forgery)
- [ ] CORS is configured correctly (not allowing all origins)
- [ ] API keys are rotated regularly

### Red Flags

- Inputs are not validated (trusting user input)
- SQL queries are built with string concatenation (SQL injection risk)
- Secrets are in code (API keys, passwords visible)
- No authentication (anyone can use this API)
- No rate limiting (trivial to DoS)
- Logging includes sensitive data (passwords, tokens leaked in logs)

---

## Section 8: Performance and Scaling

**Goal**: Will this scale?

### Latency

- [ ] Target latency is met (p50, p95, p99)
- [ ] Database queries are indexed (not full table scans)
- [ ] N+1 queries are avoided (fetch related data in one query)
- [ ] Caching is used appropriately (cache frequently accessed data)
- [ ] No unnecessary computation (lazy evaluation, early exits)

### Throughput

- [ ] Can handle projected load (orders/sec, users/sec)
- [ ] Database connection pooling is configured
- [ ] Message queues have sufficient capacity
- [ ] No bottlenecks (identified via profiling, not guessing)

### Scaling

- [ ] Stateless code scales horizontally (add more servers)
- [ ] Data can be sharded (split across databases)
- [ ] Message queues can be scaled (add partitions)
- [ ] No single point of failure (redundancy)

### Example Patterns

```typescript
// ❌ BAD: N+1 queries (slow under load)
async function getOrders(userId) {
  const orders = await db.orders.find({ userId });
  for (const order of orders) {
    order.items = await db.items.find({ orderId: order.id }); // N queries!
  }
  return orders;
}

// ✅ GOOD: Single query with join
async function getOrders(userId) {
  return await db.orders.find({ userId }).populate('items');
}

// ❌ BAD: No caching (hits DB every time)
async function getUser(userId) {
  return await db.users.findById(userId);
}

// ✅ GOOD: Caching with invalidation
async function getUser(userId) {
  const cached = await cache.get(`user:${userId}`);
  if (cached) return cached;
  
  const user = await db.users.findById(userId);
  await cache.set(`user:${userId}`, user, 3600); // 1 hour TTL
  return user;
}
```

### Red Flags

- Latency not measured (hope it's fast)
- N+1 queries (queries per item in a loop)
- Full table scans (no indexes)
- No caching (everything hits the database)
- Code doesn't scale (requires server with more CPU/memory)
- Single point of failure (one database for everything)

---

## Section 9: The Three Pillars (Final Check)

**Goal**: Can you answer these three architectural questions?

### Pillar 1: Where Does State Live?

- [ ] You can identify the single source of truth for each data type
- [ ] All mutations go through the owner first
- [ ] Replicas are explicitly managed (caching, replication)
- [ ] Conflict resolution is defined
- [ ] Rollback or recovery is possible

**Red Flag**: "I'm not sure where [data] lives" or "It might be in two places."

### Pillar 2: Where Does Feedback Live?

- [ ] You can reconstruct a failure from logs alone
- [ ] Every critical operation is logged
- [ ] Logs are structured and queryable
- [ ] Metrics are emitted (latency, errors, throughput)
- [ ] Alerts are defined for SLO violations

**Red Flag**: "If this fails, I won't know until a user complains."

### Pillar 3: What Breaks If I Delete This?

- [ ] You can trace the blast radius
- [ ] Dependencies are documented
- [ ] Fallbacks exist for external services
- [ ] Cascade failures are prevented (circuit breakers)
- [ ] Single points of failure are identified and mitigated

**Red Flag**: "I'm not sure what would break" or "Probably everything."

---

## Approval Criteria

**Code is ready for merge if**:
- [ ] All three pillars are answered with confidence
- [ ] Spec compliance is verified
- [ ] State ownership is clear
- [ ] Error handling covers all failure modes
- [ ] Observability is sufficient (logs, metrics, tracing)
- [ ] No obvious security holes
- [ ] Performance targets are met (or on path to meet)
- [ ] Tests cover happy path + failure modes
- [ ] No circular dependencies or tight coupling

**Code needs revision if**:
- Any answer is "I'm not sure" or "Unclear"
- Failure modes from spec are missing
- No observability (can't see what's happening)
- Security holes (unvalidated input, hardcoded secrets)
- Performance targets not met
- Tests are missing for critical paths

---

## Review Template

Use this template when reviewing code:

```markdown
# Code Review: [Component Name]

## Three Pillars
- [ ] Where does state live? **[Answer]**
- [ ] Where does feedback live? **[Answer]**
- [ ] What breaks if I delete this? **[Answer]**

## Spec Compliance
- [x] All requirements implemented
- [x] All failure modes handled
- [ ] [Issue]: Missing validation for negative amounts

## State & Data
- [x] Single source of truth identified
- [ ] [Issue]: Cache invalidation not explicit

## Error Handling
- [x] External calls have timeout
- [x] Retries use exponential backoff
- [ ] [Issue]: No circuit breaker for payment gateway

## Observability
- [x] Critical operations logged
- [x] Structured logs with context
- [ ] [Issue]: No metrics for order count

## Dependencies
- [x] External dependencies injected
- [x] Fallbacks documented
- [ ] [Issue]: No fallback for cache miss

## Testing
- [x] Happy path tested
- [x] Failure modes tested
- [ ] [Issue]: No concurrency test

## Security
- [x] Input validation present
- [x] Secrets in env vars
- [ ] [Issue]: Rate limiting not implemented

## Performance
- [x] Latency target met (p99 < 2s)
- [ ] [Issue]: N+1 queries detected

## Summary
✅ **APPROVED** with 2 minor issues (metrics, rate limiting) to address before next sprint.
```

---

## Questions to Avoid Letting Slip

1. **"What if this external service is down?"** → Make sure there's a fallback.
2. **"What happens if two users do this simultaneously?"** → Ensure race conditions are handled.
3. **"How do I know if this failed?"** → Verify observability is sufficient.
4. **"Will this scale to 1000 requests/sec?"** → Check performance targets.
5. **"What if the database is full?"** → Ensure error is handled gracefully.
6. **"Can I modify this without breaking other code?"** → Verify loose coupling.
7. **"How long does this take?"** → Verify latency is measured.
8. **"Where does [data] live?"** → Ensure single source of truth.
9. **"Is this tested?"** → Verify tests cover failure modes.
10. **"What could go wrong?"** → Ensure all failure modes are covered.

If you can't answer any of these, ask the code author to clarify before approval.
