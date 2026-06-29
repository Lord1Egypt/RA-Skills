# Design Doc Checklist — D[N] Standard

> Use this checklist for every design document in a D1-DN series.
> A design doc that can't pass this checklist isn't ready for implementation.

---

## Required Sections (every D[N])

### ✅ 1. Goal

- [ ] Problem stated in ≤3 sentences
- [ ] What "done" looks like (measurable, not "it works")
- [ ] Who this document is for (audience)

**Anti-pattern**: Goal that requires reading 3 paragraphs to understand what you're building.

---

### ✅ 2. Non-Goals

- [ ] Explicitly listed (minimum 2 items)
- [ ] Phrased as what this project will NOT do, NOT what it might do later
- [ ] Includes at least 1 item that might be assumed in scope (to prevent scope creep)

**Why it matters**: Non-goals prevent the second-biggest source of project failure — scope creep by assumption.

**Anti-pattern**: "Out of scope: anything not mentioned above." That's not a non-goal, that's avoidance.

---

### ✅ 3. Architecture Diagram

- [ ] Shows all components involved
- [ ] Shows direction of data flow (arrows with labels)
- [ ] Shows external dependencies (third-party APIs, other services)
- [ ] Authentication boundary marked (what's inside the trust boundary, what's outside)
- [ ] Updated when architecture changes — doc must match implementation

**Acceptable formats**: ASCII art, Mermaid, Draw.io export, or linked image with alt-text.

**Anti-pattern**: "See the system diagram in [some other doc]" — this doc must be self-contained.

---

### ✅ 4. API Surface

- [ ] Every endpoint listed: method + path + description
- [ ] Request body schema: field name, type, required/optional, constraints
- [ ] Response body schema: success + all error shapes
- [ ] Error codes: application-level code + HTTP status + user-facing message
- [ ] Auth requirement per endpoint (public / user token / admin token / service-to-service)
- [ ] Rate limit per endpoint (if applicable)

**Example format** (required level of detail):
```
POST /api/v1/orders
Auth: Bearer token (user)
Request:  { item_id: string (required), quantity: number (min: 1, max: 100) }
Response: { order_id: string, status: "pending" | "confirmed" }
Errors:   400 INVALID_QUANTITY / 404 ITEM_NOT_FOUND / 429 RATE_LIMIT_EXCEEDED
```

**Anti-pattern**: "Accepts an order object and returns a result." Not a spec — a wish.

---

### ✅ 5. Data Model

- [ ] Table name and purpose
- [ ] Every column: name, type, nullable, default, constraints
- [ ] Primary key strategy (UUID vs serial vs composite)
- [ ] Foreign key relationships with ON DELETE / ON UPDATE behavior
- [ ] Indexes: which columns are indexed and why
- [ ] For partitioned tables: partition key and strategy
- [ ] TypeScript interface (or equivalent) with types that match DB column types

**Type mapping to flag**:
- PG `NUMERIC` / `DECIMAL` → TypeScript `number` (use `parseFloat`)
- PG `BIGINT` → TypeScript `string` or `bigint` (NOT `number` — precision loss)
- PG `TIMESTAMPTZ` → TypeScript `string` (ISO 8601) or `Date`

**Anti-pattern**: "We'll use a users table with the usual fields."

---

### ✅ 6. Error Handling

- [ ] All error codes defined with names (not just HTTP statuses)
- [ ] Distinction between user-facing errors (safe to display) and internal errors (log only)
- [ ] Retry-safe operations marked (idempotent endpoints)
- [ ] Timeout behavior: what happens if upstream service doesn't respond

**Standard error response shape** (must be consistent across all endpoints):
```json
{
  "error": {
    "code": "ITEM_NOT_FOUND",
    "message": "The requested item does not exist.",
    "request_id": "req_abc123"
  }
}
```

---

### ✅ 7. Security (AuthN / AuthZ)

- [ ] Authentication mechanism: JWT / session / API key / mTLS
- [ ] Token validation: where it happens, what claims are checked
- [ ] Authorization rules: role/permission required per endpoint
- [ ] Trust boundaries: which services can call which without user context
- [ ] Data isolation: how one user's data is prevented from leaking to another
- [ ] Secrets management: where credentials are stored (never in code)

**Anti-pattern**: "Auth is handled by middleware." Where? What claims? What happens when it fails?

---

### ✅ 8. Observability

- [ ] Metrics emitted: name, unit, labels (e.g., `http_requests_total{method, path, status}`)
- [ ] Structured log fields for key operations
- [ ] Distributed trace spans for cross-service calls
- [ ] Alert thresholds: what metric value triggers an alert
- [ ] Dashboard: which metrics are displayed and how

**Why it matters**: If you can't observe it, you can't debug it in production.

---

### ✅ 9. Why This Way (Rationale)

- [ ] ≥2 key architectural decisions explained
- [ ] Each decision includes: what problem it solves + why this solution + why not the obvious alternative
- [ ] No "industry standard" or "best practice" without concrete reasoning

**Anti-pattern**: "We chose PostgreSQL because it's industry standard." Why not MySQL, SQLite, DynamoDB for this specific use case?

---

### ✅ 10. Alternatives Rejected

- [ ] ≥2 alternatives listed
- [ ] Each alternative: what it is + why it was rejected (concrete, not "not a good fit")
- [ ] At least 1 alternative that was seriously considered (not a strawman)

**Why it matters**: Documents the reasoning so future engineers don't re-propose rejected approaches, and so reviewers can challenge the decision if constraints have changed.

---

### ✅ 11. Migration Plan

- [ ] How existing data is migrated (if any)
- [ ] How existing API consumers transition (backwards compatibility window)
- [ ] Migration steps numbered and reversible
- [ ] Estimated migration duration (affects deploy window planning)

**Skip only if**: This is a brand-new system with no existing users or data.

---

### ✅ 12. Rollback Plan

- [ ] Trigger conditions: exactly what failure state means "roll back"
- [ ] Rollback steps numbered (exact commands, not "revert the deployment")
- [ ] DB rollback: snapshot strategy or down-migration path
- [ ] Communication: who gets notified when rollback is triggered

**Anti-pattern**: "We'll roll back if something goes wrong." When? How? Who decides?

---

### ✅ 13. Dependencies

- [ ] External services this system calls (with SLA / uptime assumptions)
- [ ] Internal services this system depends on (with owners)
- [ ] Libraries with version pins for critical dependencies
- [ ] Failure mode: what happens if each dependency is unavailable

---

### ✅ 14. Open Questions

- [ ] Each question has an owner (a person, not "TBD")
- [ ] Each question has a deadline for resolution
- [ ] Blocking questions are clearly marked

**Anti-pattern**: An Open Questions section that never gets resolved. If a question is still open at implementation start, it becomes a decision made by the developer in a hurry.

---

## Review Scoring

Before marking D[N] as approved, count:

| Check | Threshold | Status |
|---|---|---|
| All 14 sections present | All 14 | 🔴 if missing any |
| API surface has exact schemas | 100% of endpoints | 🔴 if any missing |
| Alternatives Rejected has ≥2 | ≥2 | 🔴 if <2 |
| Open Questions have owners | 100% | 🟡 if any "TBD" owner |
| Diagrams are current | Matches code | 🔴 if stale |

---

_Reference for: build-protocol-engineering SKILL.md — Design Doc Series Standard_
_Last updated: 2026-04-30_
