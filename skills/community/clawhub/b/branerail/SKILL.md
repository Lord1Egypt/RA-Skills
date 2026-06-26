---
name: SystemDesign
description: CTO-level architectural advisor for AI-native development. Use this skill whenever you encounter code design decisions, architecture discussions, system resilience questions, or any work touching: "architecture", "design", "scale", "dependencies", "state", "failure", "blast radius", "refactor", "migrate", "optimize", "resilience", "consistency", "observability", "bottleneck", "coupling", "monolith", "microservices", "distributed", "concurrency", "data flow", "system design", or any prompt suggesting code-first thinking when design-first thinking is needed. This skill integrates with Claude Code to review generated code for architectural soundness, define design systems via design.md, and guide teams toward CTO-level thinking. Trigger aggressively on architectural questions—this is where AI adds the most leverage.
---

# SystemDesign Skill: CTO-Level Agent for AI-Native Development

**Core principle**: AI generates code at lightspeed. Your job is to conduct the orchestra, not play a single instrument. In an AI-native world, architectural thinking—not syntactic fluency—separates valuable builders from those building houses of cards.

---

## When to Trigger This Skill

Use this skill for:

1. **Architecture from scratch**: Building new systems without a design blueprint
2. **Code quality audits**: Reviewing AI-generated code for architectural soundness
3. **Resilience analysis**: Understanding failure modes and cascade effects
4. **State and data flow**: Clarifying ownership, mutations, and consistency
5. **Scaling decisions**: Planning for growth, identifying bottlenecks
6. **Refactoring and migration**: Restructuring existing systems safely
7. **Observability and feedback loops**: Designing monitoring and alerting
8. **Design system definition**: Creating DESIGN.md for AI agent consistency
9. **Dependency mapping**: Understanding what breaks when something is removed
10. **Concurrency and consistency**: Handling race conditions, distributed state

**Trigger keywords (use liberally)**:
- architecture, design, system design, blueprint
- scale, scaling, growth, bottleneck
- failure, resilience, fault tolerance, crash
- state, stateful, state management, ownership
- blast radius, cascade, coupling, tight coupling, loose coupling
- data flow, data consistency, sync, eventual consistency
- refactor, rewrite, migration, monolith, microservices
- observability, monitoring, logging, alerting, tracing
- optimize, performance, latency, throughput
- dependency, dependent, independent, circular dependency
- concurrency, race condition, deadlock, locking, mutex
- distributed, consensus, replication, consistency
- single point of failure, SPOF, redundancy
- contract, interface, API, contract drift
- DESIGN.md, design system, design tokens, brand consistency
- code review, audit, architectural review
- Claude Code, code generation, AI-generated code

---

## Part 1: The Three Pillars of Systems Thinking

Before shipping any logic, answer these three questions with certainty. If you cannot, your system is fragile.

### Pillar 1: Where Does State Live?

**The Question**: What is the single source of truth for each mutable piece of data?

**Why It Matters**: Multiple components claiming ownership creates race conditions, sync bugs, and silent data corruption. AI-generated code often scatters state without a coherent strategy.

**Audit Process**:

1. **Inventory mutable state**: Every piece of data that changes (user profiles, order status, inventory counts, cache entries, feature flags, session tokens).
2. **Identify authoritative owner**: For each, which component is *first* to modify it?
3. **Check for replicas**: Do other components maintain copies? If yes:
   - Is this for performance (caching) or redundancy (failover)?
   - What is the reconciliation strategy?
   - Who wins in a conflict?
4. **Trace mutation paths**: When data changes, does every replica update? How?

**Architecture Patterns**:

| Pattern | Use When | Trade-offs |
|---------|----------|-----------|
| **Single Source of Truth (DB)** | Correctness is critical (payments, inventory, auth) | Higher latency (must hit DB) |
| **Write-Through Cache** | High read volume, acceptable write latency | Must update cache after DB |
| **Write-Back Cache** | Low write latency needed | Risk of cache loss before sync |
| **Event Sourcing** | Need audit trail and point-in-time recovery | Complexity, eventual consistency |
| **CQRS** | Read/write patterns differ radically | Query model sync complexity |
| **Distributed Consensus** | Sync state across replicas (e.g., etcd, Raft) | Complex, higher latency |

**Red Flags**:
- "State is in A, but B caches it for performance."
- Multiple components modify the same data.
- No explicit ownership declared.
- Circular dependencies (A owns X, B owns Y, A reads Y to compute X).
- Cache invalidation strategy is "just invalidate everything."

**Code Review Checklist**:
- [ ] Every mutable variable has a declared owner.
- [ ] Non-owners read from the owner, not from stale copies.
- [ ] Writes go to the owner first, then propagate (if at all).
- [ ] Conflict resolution rules exist (write wins, read latest, timestamp-based).
- [ ] State schema is versioned; migrations are explicit.

---

### Pillar 2: Where Does Feedback Live?

**The Question**: How do you know if your system is working? What alerts you to failures?

**Why It Matters**: A system without visibility is failing silently. By the time a user reports it, the damage may be irreversible.

**Audit Process**:

1. **Identify critical operations**: Data writes, API calls, job scheduling, external integrations, state syncs.
2. **Define success and failure**: What does "working" look like for each operation?
3. **Instrument for visibility**:
   - Structured logging (JSON, key-value pairs, not printf blobs).
   - Metrics (counters, latencies, error rates).
   - Distributed tracing (request ID propagation, span correlation).
   - Alerts (threshold-based, anomaly-based, custom rules).
4. **Test observability**: Can you reconstruct a failure from logs alone?

**Logging Strategy**:

```
✅ GOOD: Structured, contextual
{
  "timestamp": "2026-04-27T10:30:45Z",
  "service": "order-processor",
  "operation": "process_payment",
  "orderId": "order_12345",
  "customerId": "cust_67890",
  "status": "failed",
  "error": "payment_gateway_timeout",
  "retries_attempted": 3,
  "latency_ms": 5000,
  "trace_id": "tr_abc123def456"
}

❌ BAD: Unstructured, no context
[ERROR] Payment failed. Retrying...
```

**Metrics to Track**:
- Request count (by endpoint, by status)
- Request latency (p50, p95, p99)
- Error rate (by type, by service)
- Queue depth (for async jobs)
- Cache hit ratio
- State sync lag (for replicated data)
- Deployment frequency, lead time, MTTR

**Alerting Strategy**:
- **Threshold-based**: Error rate > 5% for 5 minutes
- **Anomaly-based**: Latency 3σ above baseline
- **Custom logic**: "If payment failures increase 10x in 1 hour, alert"
- **Escalation**: Page on-call for P1 (data loss, security), alert for P2 (degraded, slow)

**Red Flags**:
- "We log errors, but only when explicitly caught."
- No monitoring for silent failures (cron job that didn't run, queue that got stuck).
- Logs with data but no context (what was being attempted?).
- Alerts that trigger *after* customer impact.
- "We'll debug when users report issues."

**Code Review Checklist**:
- [ ] Every I/O operation logs success/failure with context.
- [ ] All error paths are instrumented (not just happy path).
- [ ] Request IDs propagate across service boundaries.
- [ ] Metrics are emitted (count, latency, errors).
- [ ] Alerts are defined for SLO violations.
- [ ] Logs are queryable (not syslog blobs; structured, indexed).

---

### Pillar 3: What Breaks If I Delete This?

**The Question**: Can you trace the blast radius of every component?

**Why It Matters**: If you cannot articulate what happens when a piece is removed, you do not truly understand the system.

**Audit Process**:

1. **Pick a component** (service, module, function, data store, queue).
2. **Simulate deletion**:
   - What calls into it?
   - What depends on its output?
   - What happens to dependents if it's gone?
3. **Continue recursively**: Trace cascading effects.
4. **Identify single points of failure** (SPOF): Components with no fallback.
5. **Measure blast radius**: How many users, transactions, or features are affected?

**Blast Radius Analysis**:

```
Scenario: Delete the cache layer

A: Web → Cache → DB

If cache is deleted:
  - Reads go directly to DB (slower, but correct)
  - Throughput drops 10x
  - DB CPU spikes
  - Users on slow connections timeout
  - Blast radius: ALL users
  - Mitigation: Circuit breaker (fail fast instead of timing out)

Scenario: Delete the notification service

Orders → Notification Service → Email / SMS

If notification service is deleted:
  - Orders still process (good)
  - Users don't get confirmation emails (bad UX)
  - Blast radius: Marketing, customer trust
  - Mitigation: Queue notifications, retry asynchronously
```

**Dependency Mapping**:

| Component | Depends On | Depended On By | Fallback? | SPOF? |
|-----------|-----------|----------------|-----------|-------|
| Auth Service | DB | All services | No | YES |
| Payment Gateway | External API | Orders | Retry + queue | Partial |
| Cache | In-memory store | API | Direct DB read | No |
| Notification | Message queue | Orders, Users | Queue message | No |

**Red Flags**:
- "I'm not sure what would break."
- Circular dependencies (A needs B, B needs A).
- Hidden dependencies through side effects, globals, or environment variables.
- No clear contract for a component (what are its inputs, outputs, failure modes?).
- A component has no fallback (single point of failure).

**Code Review Checklist**:
- [ ] Each component has explicit dependencies declared (imports, config, injected).
- [ ] No hidden global state.
- [ ] No circular dependencies.
- [ ] Fallback strategies exist for external dependencies.
- [ ] Circuit breakers or bulkheads isolate failures.
- [ ] Blast radius is documented (what features fail if this goes down?).
- [ ] The deletion test passes (you can mentally trace the impact).

---

## Part 2: The Design Process Before Code

These practices slow you down. They save you from building on sand.

### 1. Sketch the Architecture (Before Prompting AI)

**Workflow**:

1. **Draw boxes** for major components (services, databases, caches, queues, external APIs).
2. **Draw arrows** for data flow (what data moves where, in what direction, how often).
3. **Label arrows** with data structures and frequency (e.g., "User order JSON, ~1000/sec").
4. **Identify state owners** on the diagram (which box is authoritative for each type of data).
5. **Mark external dependencies** (what lives outside your control? What can fail?).
6. **Add fallbacks** (what happens if that dependency is down?).

**Example Diagram**:

```
                    Client
                      |
                [API Gateway]
                /     |      \
            Order   User    Payment
            Service Service Service
              |       |        |
            [Order DB] [User DB] [Payment Gateway]
              |       |
            [Cache]  [Cache]
              |
           [Message Queue]
              |
          [Notification Service]
              |
         [Email / SMS Provider]

Blast radius analysis:
- If Order Service ↓: Can't create orders (orders = core feature)
- If User Service ↓: Can't login (cascade fail)
- If Cache ↓: Slower reads, but queries still work
- If Email Provider ↓: Orders process, confirmations queue, retried
```

**Checkpoint**: Can you sketch this in 5 minutes and explain it to someone else? If not, you don't understand it yet. Do not prompt AI.

---

### 2. Write a Design Document (DESIGN.md for Systems, Spec for Features)

Use **design.md** for visual design systems. Use **architectural specs** for system design.

#### For Visual Design Systems: Create DESIGN.md

DESIGN.md is a format specification that combines machine-readable design tokens (YAML front matter) with human-readable design rationale in markdown prose, allowing AI agents to generate on-brand interfaces without needing repeated explanations.

**DESIGN.md Structure**:

```markdown
---
name: ProductName
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  accent: "#B8422E"
  success: "#2E7D32"
  error: "#C62828"
  neutral: "#F7F5F2"
typography:
  h1:
    fontFamily: "Public Sans"
    fontSize: "3rem"
    fontWeight: "700"
  body:
    fontFamily: "Public Sans"
    fontSize: "1rem"
    lineHeight: "1.5"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "32px"
rounded:
  sm: "4px"
  md: "8px"
  lg: "16px"
---

## Visual Intent

Describe the aesthetic and emotional tone: minimalist, bold, approachable, professional.

## Color Usage

Explain the semantic meaning of each color and when to use it.

## Typography

Explain font choices and when to use each scale.

## Component Patterns

Define behavior for buttons, cards, forms, modals, etc.

## Accessibility

Document WCAG AA/AAA compliance, contrast ratios, keyboard navigation.
```

**Validation**: Use Google's design.md CLI tool to validate the file, check WCAG contrast ratios, and export tokens to Tailwind or W3C DTCG format.

#### For System Architecture: Write an Architectural Spec

```markdown
# [Component Name] Specification

## Purpose
One sentence. What does this do?

## Inputs
- Data structure(s), format, size limits, example payloads

## Outputs
- Data structure(s), format, example payloads

## State Ownership
- What state does this own?
- What state does it read (from where)?
- How are conflicts resolved?

## Critical Path
- Happy path: input → process → output
- Timeline and latency targets

## Failure Modes
| Failure | Probability | Impact | Detection | Recovery |
|---------|-------------|--------|-----------|----------|
| Network timeout | High | Partial | Timeout + log | Retry with exponential backoff |
| Disk full | Medium | Total | No space error | Alert, manual intervention |
| Invalid input | High | Partial | Schema validation | Reject + log |
| Cascade from dependency | High | Partial | Dependency error | Fallback or circuit break |

## Observability
- Logs: what events are logged?
- Metrics: what is measured?
- Alerts: what triggers escalation?

## Constraints
- Performance targets (latency p99, throughput)
- Scaling limits (max concurrent, max data size)
- Dependencies (what must be running first)

## Questions Answered
- Where does state live? [Describe single source of truth]
- Where does feedback live? [Describe observability]
- What breaks if I delete this? [Describe blast radius]
```

**Checkpoint**: If you cannot fill this out without guessing, the design is incomplete. Do not proceed.

---

### 3. Run the Deletion Test (Mentally)

For each component:

```
[ ] What calls this?
[ ] What does this output to?
[ ] What happens to those dependents if this is gone?
[ ] Are there fallbacks?
[ ] How many users are affected?
[ ] How long until they notice?
```

---

### 4. Manual Re-implementation (After AI Generates Code)

**Workflow**:
1. Read the AI-generated code carefully.
2. Close the file.
3. Rewrite it from memory.
4. Compare. What did you forget? What did AI do differently?

**Frequency**: Weekly for critical code, monthly for infrastructure.

---

## Part 3: AI as a Probabilistic Collaborator

**Key distinction**: Compilers are deterministic. LLMs are probabilistic.

A compiler follows provably correct rules. You trust it without auditing the machine code.

An LLM makes choices based on statistical likelihood. It can introduce:
- Subtle auth bypasses (a check that *looks* correct).
- Off-by-one errors in business logic.
- Silent failures (error handling that looks comprehensive but misses edge cases).
- Race conditions (generated code doesn't account for concurrency).

**Your role**: Auditor and architect.

---

## Part 4: Code Review Checklist for AI-Generated Code

When Claude Code or another agent generates code, audit it against these criteria:

### Spec Compliance
- [ ] Does it satisfy all requirements in the spec?
- [ ] Does it handle all failure modes listed?
- [ ] Are all success criteria met?

### State and Data
- [ ] Is state ownership clear? Single source of truth?
- [ ] Are mutations idempotent (safe to retry)?
- [ ] Is there a reconciliation strategy if replicas diverge?
- [ ] Are schema changes versioned?

### Error Handling
- [ ] Are all error paths logged?
- [ ] Does it fail fast or degrade gracefully?
- [ ] Are retries with backoff used for transient failures?
- [ ] Is there a circuit breaker for cascading failures?

### Observability
- [ ] Are all critical operations logged with context?
- [ ] Are metrics emitted (latency, errors, throughput)?
- [ ] Are request IDs propagated across services?
- [ ] Are alerts defined for SLO violations?

### Dependencies
- [ ] Are dependencies explicit (injected, not global)?
- [ ] Can they be mocked for testing?
- [ ] Are there fallbacks for external dependencies?
- [ ] Are circular dependencies eliminated?

### Concurrency and Consistency
- [ ] Are race conditions handled (locks, atomicity, transactions)?
- [ ] Is eventual consistency explained?
- [ ] Are critical sections protected?
- [ ] Is deadlock possible?

### Testing
- [ ] Is the happy path tested?
- [ ] Are failure modes tested (timeout, invalid input, cascade)?
- [ ] Is concurrency tested?
- [ ] Are edge cases covered?

### Performance and Scaling
- [ ] Does latency meet targets (p50, p95, p99)?
- [ ] Can it scale to projected load?
- [ ] Are bottlenecks identified and planned for?
- [ ] Is caching used appropriately?

### Security
- [ ] Are inputs validated?
- [ ] Is there auth/authz?
- [ ] Are secrets never logged?
- [ ] Is SQL injection / XSS / CSRF prevented?

---

## Part 5: Architectural Anti-Patterns (What Not to Do)

| Anti-Pattern | Failure Mode | Fix |
|---|---|---|
| **No State Ownership** | Race conditions, sync bugs, data corruption | Designate a single owner for each data type |
| **Scattered State** | Inconsistency, silent failures, hard to debug | Centralize or use consensus protocol |
| **Silent Failures** | User reports bug hours later; data is corrupted | Instrument everything; alert on anomalies |
| **Circular Dependencies** | Can't isolate changes; cascading failures | Restructure to acyclic dependency graph |
| **Single Point of Failure (SPOF)** | One component down = entire system down | Add redundancy, fallbacks, bulkheads |
| **Implicit Dependencies** | Hidden globals, env vars, side effects | Make dependencies explicit; inject them |
| **Premature Optimization** | Complex code, fragile systems, maintenance nightmare | Simplify first, optimize after measurement |
| **Tight Coupling** | Can't change one service without affecting others | Loosen via async, contracts, versioning |
| **No Monitoring** | System fails silently; rollbacks are expensive | Instrument every critical operation |
| **Cache Invalidation** | "There are only 2 hard things in CS..." | Explicit invalidation or TTL; measure hit ratio |

---

## Part 6: The Full Development Workflow

### Pre-Code Phase (Do This Alone, Not With AI)

1. **Understand the problem**: What are we solving? Who benefits? Success criteria?
2. **Sketch the architecture**: Draw boxes and arrows. Identify state owners.
3. **Answer the three pillars**: State? Feedback? Blast radius?
4. **Write the spec**: Inputs, outputs, state ownership, failure modes, observability.
5. **Identify risks**: What could go wrong? What needs monitoring?

### Code Generation Phase (With Claude Code)

6. **Provide spec to Claude Code**: Reference the spec in your prompt. Make it a constraint.
7. **Include DESIGN.md**: If generating UI, include your DESIGN.md in the context.
8. **Ask Claude Code to include observability**: "Log every operation with context. Emit metrics."
9. **Request explicit error handling**: "Handle these failure modes: [list them]."

### Code Review Phase (Manual, By You)

10. **Run the audit checklist** against generated code.
11. **Verify the three pillars**: State? Feedback? Blast radius?
12. **Check for edge cases**: Does it handle the failure modes in the spec?
13. **Validate observability**: Can you see what's happening?

### Deployment Phase

14. **Run the deletion test**: Mentally trace impact if this is removed.
15. **Verify monitoring**: Are alerts firing as expected?
16. **Monitor the three pillars** in production.

### Post-Deployment (Learning Phase)

17. **Reimplement manually** (one piece per week): Force yourself to understand.
18. **Update the spec**: Document surprises, edge cases, lessons learned.
19. **Iterate**: Refactor architectural mistakes early; they compound.

---

## Part 7: Concurrency and Distributed Systems

These are the hardest problems. Think deeply.

### Concurrency Patterns

**Mutex / Lock**:
- Use: Protecting critical sections (update, delete).
- Risk: Deadlock if acquired in different order.
- Test: Run with high concurrency, long durations.

**Atomic Operations**:
- Use: Single operations that must not race (increment, compare-and-swap).
- Risk: Complex to reason about; easy to miss a step.
- Test: Formal verification tools if critical.

**Immutable Data**:
- Use: Sharing data without locks (functional style).
- Risk: Performance overhead (copying).
- Benefit: No race conditions.

**Channels / Queues**:
- Use: Decoupling producer from consumer.
- Risk: Queue overload, backpressure, ordering.
- Benefit: Loose coupling, async processing.

**Transactions**:
- Use: Multi-step operations that must all succeed or all fail.
- Risk: Deadlock, rollback complexity, performance.
- Guarantee: ACID (Atomicity, Consistency, Isolation, Durability).

### Distributed Systems Patterns

**Consensus (Raft, Paxos)**:
- Use: Replicating state across nodes.
- Risk: Network partitions, split brain, complexity.
- Guarantee: All replicas agree on state.

**Eventual Consistency**:
- Use: High availability, accepting temporary divergence.
- Risk: Users see stale data; conflicts possible.
- Recovery: Conflict resolution rules.

**Event Sourcing**:
- Use: Audit trail, point-in-time recovery.
- Risk: Complexity, eventual consistency.
- Benefit: Can replay history.

**CQRS (Command Query Responsibility Segregation)**:
- Use: Read/write models differ radically.
- Risk: Query model sync lag.
- Benefit: Independent scaling.

**Circuit Breaker**:
- Use: Failing fast when a dependency is down.
- Risk: Stale data if fallback used too long.
- Benefit: Prevents cascade failures.

---

## Part 8: Claude Code Integration Workflow

### Initializing a Project with SystemDesign

1. **Create a DESIGN.md** (for UI consistency):
   ```bash
   # Ask Claude Code to generate DESIGN.md
   "Create a DESIGN.md file that defines our brand colors, typography, and component patterns."
   ```

2. **Create architectural specs** (for system design):
   ```bash
   # Ask Claude Code to scaffold spec documents
   "Generate spec templates for each major component: auth, payment, notifications."
   ```

3. **Link specs to prompts**:
   ```
   You are a CTO-level code generator.
   
   When I ask you to build [feature], first:
   1. Reference the spec at /specs/[feature].md
   2. Verify your code satisfies all requirements.
   3. Implement the failure modes listed.
   4. Include structured logging for every operation.
   
   If building UI:
   1. Reference /DESIGN.md for colors, typography, components.
   2. Ensure all generated UI respects those tokens.
   3. Check WCAG AA contrast ratios.
   ```

### Prompting Claude Code for Architectural Code

**Good Prompt**:
```
Using the spec at /specs/order-processing.md:

1. Implement the order processing service.
2. All state mutations go through OrderStore (single source of truth).
3. Implement retry logic with exponential backoff for payment gateway failures.
4. Log every operation: orderId, status, latency, errors.
5. Emit metrics: order count, latency p50/p95/p99, error rate.
6. Add a circuit breaker: if payment fails >5% of the time, fail fast.
7. Handle the failure modes in the spec: timeout, invalid input, gateway down, database error.
```

**Why It Works**:
- Clear constraints (spec).
- Explicit error handling.
- Observability requirements (logs, metrics).
- Resilience pattern (circuit breaker).
- Failure modes enumerated.

---

## Part 10: Advanced Architectural Patterns (SOTA)

Move beyond simple client-server models into resilient, high-scale patterns.

### 10.1 Cell-Based Architecture (Bulkheading at Scale)
- **Concept**: Divide your system into "cells" (independent instances of the whole stack). 
- **Benefit**: If one cell fails, only a fraction of users are affected. 
- **Use When**: You hit the "blast radius" limit of a single global monolith/microservice set.

### 10.2 Sidecar / Service Mesh
- **Concept**: Offload cross-cutting concerns (logging, auth, retries) to a separate process.
- **Benefit**: Business logic stays clean; infrastructure logic is centralized and versioned.
- **Use When**: You have multiple languages/services needing consistent observability.

### 10.3 Strangler Fig Pattern
- **Concept**: Incrementally wrap legacy code with new services until the old ones are redundant.
- **Benefit**: Zero-downtime migration of massive legacy systems.
- **Use When**: Refactoring a system too large to "restart" from scratch.

### 10.4 Eventual Consistency & Sagas (Distributed Transactions)
- **Concept**: Use a sequence of local transactions (Sagas) to coordinate a distributed task.
- **Benefit**: No long-lived locks; high availability.
- **Use When**: You need atomicity across multiple databases/services.

---

## Part 11: The Cloud-Native Resilience Suite

Advanced techniques for self-healing systems.

### 11.1 Adaptive Throttling
- **Concept**: Instead of a hard rate limit, services reduce throughput based on backend latency.
- **Benefit**: Prevents "death spirals" where retries overwhelm a slow system.

### 11.2 Chaos Engineering (The Ultimate Test)
- **Concept**: Intentionally inject failures into production (latency, termination).
- **Benefit**: Proves the "Blast Radius" theory in real-world conditions.
- **Exercise**: If you can't run the Chaos Test, you haven't answered Pillar 3.

### 11.3 Graceful Degradation (Feature Toggles)
- **Concept**: When a dependency fails, switch to a "light" version of the feature.
- **Example**: If the "Recommendations" service is down, show "Popular Items" (static) instead.

---

## Part 12: Evaluation Rubric (Is This System Sound?)

Score yourself 0-3 on each:

| Criterion | 0 - Fragile | 1 - Risky | 2 - Solid | 3 - Resilient |
|-----------|-----------|----------|---------|--------------|
| **State Ownership** | Multiple owners or scattered | Some replicas without strategy | Single owner, clear replicas | Central authority + audit trail |
| **Observability** | No logging or metrics | Logs exist but unstructured | Structured logs, basic metrics | Full tracing, anomaly detection |
| **Failure Handling** | No fallbacks, cascades fail | Some fallbacks, partial coverage | All critical failures handled | Self-healing, circuit breakers |
| **Blast Radius** | Don't know what's coupled | Loosely mapped | Well documented | Tested via chaos engineering |
| **Testing** | No tests | Happy path only | Happy + failure cases | Concurrency, performance, chaos |
| **Scaling** | Doesn't scale | Scales to 10x | Scales to 100x with planning | Horizontal scaling built-in |
| **Dependency Clarity** | Hidden globals, side effects | Some explicit, some implicit | All dependencies injected | Versioned contracts, no surprises |
| **Code Quality** | Unreadable, no comments | Readable but dense | Clear intent, documented | Self-documenting, easy to extend |

**Target Score**: 2+ on all dimensions. Anything below 1 is a risk.

---

## Summary: What Remains Human in an AI-Native World

AI will replace typing. It will not replace thinking.

The most valuable builders will be those who:
- **Refuse to atrophy their judgment.**
- **Design before coding.**
- **Use AI as an amplifier for architecture**, not a substitute for understanding.
- **Build for resilience, not just functionality.**
- **Instrument everything; monitor relentlessly.**
- **Trace blast radius; understand coupling.**

The shift from "coder" to "conductor" is not optional. It is the price of remaining relevant.

---

## Quick Reference: The Three Pillars Checklist

### Pillar 1: Where Does State Live?
- [ ] Single owner for each data type
- [ ] Non-owners read from owner
- [ ] Conflict resolution rules exist
- [ ] Replicas are explicit and versioned
- [ ] Schema changes are migrations, not surprises

### Pillar 2: Where Does Feedback Live?
- [ ] Every critical operation is logged
- [ ] Logs are structured and searchable
- [ ] Metrics are emitted (latency, errors, throughput)
- [ ] Alerts are defined for SLO violations
- [ ] You can reconstruct a failure from logs

### Pillar 3: What Breaks If I Delete This?
- [ ] Dependencies are explicit
- [ ] No circular dependencies
- [ ] Fallbacks exist for external services
- [ ] Blast radius is documented
- [ ] You can trace impact mentally

**If you can answer yes to all 15, your system is sound.**
