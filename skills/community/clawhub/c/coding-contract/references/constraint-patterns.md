# Constraint Patterns Reference

Use this reference when writing Section 4 (Constraint Layer) of a spec.
Copy relevant patterns and adapt to the specific domain. This is a catalog,
not a checklist — include only constraints that apply to the feature.

## Table of Contents

1. [Performance Patterns](#performance-patterns)
2. [Degradation Patterns](#degradation-patterns)
3. [Boundary Condition Patterns](#boundary-condition-patterns)
4. [Threading & Concurrency Patterns](#threading--concurrency-patterns)
5. [Security Patterns](#security-patterns)
6. [State & Persistence Patterns](#state--persistence-patterns)
7. [Error Handling Patterns](#error-handling-patterns)

---

## Performance Patterns

### API / Service Latency

| Metric | Typical Targets | Measurement |
|--------|----------------|-------------|
| API response (p50) | < 50 ms | Endpoint load test |
| API response (p95) | < 200 ms | Endpoint load test |
| API response (p99) | < 500 ms | Endpoint load test |
| Database query | < 20 ms (simple), < 100 ms (complex) | Query analyzer |
| Cache hit | < 5 ms | Redis latency monitor |
| Cache miss penalty | < 2x baseline | Comparative test |

### Throughput

| Scenario | Target | Test Method |
|----------|--------|-------------|
| HTTP API | 1000+ req/s per instance | k6, Artillery, locust |
| Message processing | 10,000+ msg/s per consumer | Producer/consumer benchmark |
| Batch job | Process 1M records in < 1 hour | End-to-end timing |
| File upload | 100 MB/s sustained | Direct upload test |

### Resource Usage

| Resource | Typical Limit | Context |
|----------|--------------|---------|
| Memory per instance | < 512 MB (container), < 2 GB (VM) | RSS after warm-up |
| CPU per request | < 10 ms CPU time | Flame graph analysis |
| Disk I/O | Sequential read > 100 MB/s | fio benchmark |
| Connection pool | Max 20 DB connections | Pool exhaustion test |

---

## Degradation Patterns

### Dependency Failure Matrix

| Dependency State | Behavior | Example |
|------------------|----------|---------|
| **Healthy** | Normal path, full features | All services operational |
| **Degraded (slow)** | Timeout fallback, cached data, reduced freshness | Cache returns stale data with warning header |
| **Degraded (partial)** | Disable non-critical features, core path works | Payment down → browse still works, checkout blocked |
| **Unavailable** | Circuit breaker open, fail fast with clear error | Return 503 with retry-after header |

### Common Fallback Strategies

| Strategy | When to Use | Implementation |
|----------|-------------|----------------|
| **Cache fallback** | Read-heavy, stale data acceptable | Return cached value with `X-Cache: stale` header |
| **Static fallback** | Configuration or content data | Serve last-known-good default |
| **Simplified logic** | Complex computation | Skip ML model, use heuristic rule |
| **Queue & retry** | Write operations | Persist to dead-letter queue, retry with backoff |
| **Graceful reduction** | Resource exhaustion | Reduce batch size, lower quality, partial results |
| **Feature toggle off** | Non-critical feature | Disable feature, hide UI element, log metric |

### Circuit Breaker Configuration

| Parameter | Typical Value | Description |
|-----------|--------------|-------------|
| Failure threshold | 5 errors in 60 seconds | Trip breaker after this many failures |
| Timeout duration | 5 seconds | Consider call failed after this time |
| Recovery timeout | 30 seconds | Wait before attempting half-open test |
| Half-open requests | 1 request | Test with this many requests in half-open state |

---

## Boundary Condition Patterns

### Input Validation

| Category | Check | Error Response |
|----------|-------|----------------|
| **Null / Undefined** | Reject at API boundary | `400 Bad Request`, field-level error |
| **Empty collection** | Return empty result, not error | `200 OK` with `[]` |
| **Empty string** | Reject if meaningful; accept if optional | `400` if required; allow `""` if optional |
| **Max length** | Enforce on all string inputs | `400` with max length info |
| **Max payload** | Check Content-Length or body size | `413 Payload Too Large` |
| **Type mismatch** | Schema validation at entry point | `400` with type error detail |
| **Range validation** | Numeric fields: min, max | `400` with allowed range |
| **Enum validation** | Unknown enum value rejected | `400` with allowed values |
| **Format validation** | Email, UUID, date format | `400` with format specification |
| **Duplicate detection** | Unique key violation | `409 Conflict` with existing resource |

### Concurrency Boundaries

| Scenario | Expected Behavior |
|----------|-------------------|
| **Concurrent reads** | Safe without locking (immutable data or read replicas) |
| **Concurrent writes to same record** | Optimistic locking with version field; last write wins rejected |
| **Concurrent creates with same unique key** | Idempotency key deduplication; second request returns existing |
| **Rate limit exceeded** | `429 Too Many Requests` with `Retry-After` header |
| **Resource pool exhausted** | Queue with timeout; fail with `503` if queue full |
| **Distributed race condition** | Atomic compare-and-swap or distributed lock with TTL |

### Data Volume Boundaries

| Scenario | Limit | Behavior |
|----------|-------|----------|
| **Max page size** | 100 items | Reject larger with `400` |
| **Max export rows** | 100,000 | Stream response; reject larger with `400` |
| **Max file upload** | 50 MB | Reject with `413` |
| **Max batch operation** | 1,000 items | Reject larger; suggest chunking |
| **Max nested depth** | 10 levels | Reject circular/deep nesting |
| **Max total result set** | 10,000 | Paginate; return total count |

---

## Threading & Concurrency Patterns

### Execution Context Model

| Model | Use Case | Risk |
|-------|----------|------|
| **Single-threaded event loop** | I/O-bound, high concurrency | CPU-intensive tasks block loop |
| **Thread pool (fixed)** | CPU + I/O mixed | Thread exhaustion, context switching overhead |
| **Coroutine / async** | Many concurrent I/O operations | Complex error handling, debugging |
| **Actor model** | Stateful entities with message inbox | Mailbox overflow, ordering assumptions |
| **Fork-join** | Parallel decomposition of large task | Split overhead, load imbalance |

### Synchronization Patterns

| Pattern | When to Use |
|---------|-------------|
| **Mutex / Lock** | Short critical sections, low contention |
| **Read-Write Lock** | Read-heavy, rare writes |
| **Atomic operations** | Counters, flags, simple state changes |
| **Channel / Queue** | Producer-consumer, backpressure handling |
| **Semaphore** | Resource pool limiting |
| **Barrier** | Parallel phases requiring synchronization point |
| **CAS loop** | Lock-free updates to single variable |

### Common Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Holding lock during I/O** | Blocks all other threads | Release lock before I/O, re-acquire after |
| **Nested locks** | Deadlock risk | Always acquire in same order, or use timeout |
| **Unbounded queues** | OOM under load | Use bounded queue with rejection policy |
| **Thread-local for request context** | Leaks in async/coroutine models | Use explicit context propagation |
| **Fire-and-forget without timeout** | Resource leak | Always set timeout on async operations |

---

## Security Patterns

### Authentication Patterns

| Pattern | Use Case | Notes |
|---------|----------|-------|
| **JWT (stateless)** | Microservices, SPA | Short expiry (15 min), refresh token rotation |
| **Session cookies** | Server-rendered web apps | HttpOnly, Secure, SameSite=Strict |
| **API keys** | Service-to-service | Rate limit per key, allow key rotation |
| **mTLS** | Internal service mesh | Certificate expiry monitoring |
| **OAuth 2.0 + OIDC** | Third-party login | PKCE for SPAs, state parameter for CSRF |

### Authorization Patterns

| Pattern | Use Case |
|---------|----------|
| **RBAC (Role-Based)** | Few roles, clear permissions (admin, user, guest) |
| **ABAC (Attribute-Based)** | Fine-grained, context-aware (department + time + location) |
| **Resource-level ACL** | Per-object permissions (user owns this document) |
| **Policy engine (OPA)** | Complex, changing rules; centralized decision |

### Input Security

| Check | Implementation |
|-------|----------------|
| **SQL injection** | Parameterized queries only; never string concatenation |
| **NoSQL injection** | Validate query operators; sanitize user input |
| **Command injection** | Never pass user input to shell; use exec with array args |
| **XSS prevention** | Output encoding on all user content; CSP headers |
| **Path traversal** | Canonicalize paths; reject `..`; whitelist allowed directories |
| **SSRF prevention** | Validate URLs against allowlist; block internal IPs |
| **XML External Entity** | Disable XXE parsing; use JSON instead |

### Secrets Management

| Secret Type | Storage | Access Pattern |
|-------------|---------|----------------|
| **Database credentials** | Vault / Secret Manager | Runtime injection, rotate monthly |
| **API keys (internal)** | Environment variables | Never log, never commit |
| **API keys (external)** | Encrypted database | Per-customer, rotate on compromise |
| **Encryption keys** | HSM / KMS | Never leave secure enclave |
| **JWT signing keys** | Secure key store | Rotate with grace period for old keys |

---

## State & Persistence Patterns

### Consistency Models

| Model | Use Case | Trade-off |
|-------|----------|-----------|
| **Strong consistency** | Financial transactions, inventory | Higher latency, lower availability |
| **Read-after-write** | User profile update | Slight latency increase |
| **Eventual consistency** | Social feed, analytics | Lower latency, stale reads possible |
| **Causal consistency** | Collaborative editing | Captures happens-before relationships |
| **Monotonic reads** | Timeline / stream | Guarantees forward progress in reads |

### Isolation Levels

| Level | Use When | Anomalies Allowed |
|-------|----------|-------------------|
| **Serializable** | Financial data, inventory | None |
| **Snapshot** | Complex reporting, analytics | Phantom reads (non-blocking) |
| **Read Committed** | General purpose | Non-repeatable reads |
| **Read Uncommitted** | Logging, analytics (rarely) | Dirty reads |

### Caching Strategies

| Strategy | Pattern | Invalidation |
|----------|---------|--------------|
| **Cache-aside** | App checks cache, then DB | TTL + explicit eviction on write |
| **Write-through** | Write to cache and DB synchronously | Automatic (always in sync) |
| **Write-behind** | Write to cache, async to DB | Complex; requires durability guarantee |
| **Read-through** | Cache loads from DB on miss | TTL-based |

---

## Error Handling Patterns

### Error Classification

| Category | Examples | HTTP Status | Client Action |
|----------|----------|-------------|---------------|
| **Client error (input)** | Validation, authentication, authorization | 400, 401, 403 | Fix request, do not retry |
| **Client error (state)** | Conflict, precondition failed | 409, 412 | Resolve conflict, retry |
| **Server error (transient)** | Timeout, rate limit, unavailable | 408, 429, 503 | Exponential backoff retry |
| **Server error (persistent)** | Internal error, not implemented | 500, 501 | Alert operator, limited retry |
| **Data error** | Not found, gone | 404, 410 | Do not retry; adjust logic |

### Retry Policy

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Max retries | 3 | Beyond 3, probability of success drops |
| Base delay | 1 second | Initial wait |
| Backoff multiplier | 2x | Exponential: 1s, 2s, 4s |
| Max delay | 30 seconds | Cap to prevent excessive wait |
| Jitter | +/- 25% | Prevent thundering herd |
| Retryable status codes | 408, 429, 502, 503, 504 | Only retry idempotent operations |

### Error Response Format

```json
{
  "error": {
    "code": "[MACHINE_READABLE_ERROR_CODE]",
    "message": "[Human-readable description]",
    "target": "[field_name or resource_identifier]",
    "details": [
      {
        "code": "[SUB_ERROR_CODE]",
        "message": "[Detail]",
        "target": "[specific_field]"
      }
    ]
  }
}
```

---

## Domain-Specific Adaptation Notes

### Web Backend
- Focus on: HTTP status codes, middleware ordering, CORS, rate limiting
- Degradation: API gateway timeouts, DB connection pool exhaustion

### Mobile App
- Focus on: Offline mode, battery efficiency, background task limits
- Degradation: Network type detection (WiFi/4G/offline), partial sync

### Frontend / SPA
- Focus on: Bundle size, rendering performance, accessibility
- Degradation: Skeleton screens, lazy loading, progressive enhancement

### Data Pipeline / ETL
- Focus on: Exactly-once processing, schema evolution, backfill support
- Degradation: Dead letter queue, partial batch acceptance

### ML / AI Service
- Focus on: Model versioning, inference latency, feature store consistency
- Degradation: Simpler model fallback, cached predictions, async batch

### Embedded / IoT
- Focus on: Memory constraints, power consumption, OTA updates
- Degradation: Reduced sampling rate, feature disablement
