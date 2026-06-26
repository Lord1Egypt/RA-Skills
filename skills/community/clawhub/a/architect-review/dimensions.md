# Architecture Review Dimensions

Each `## Dimension:` section below defines one review dimension.
The skill dynamically parses this file — add, remove, or modify dimensions as needed.

---

## Dimension: Modularity and Boundaries

- **id**: modularity
- **model**: (inherit)
- **description**: Domain decomposition clarity, module coupling, dependency direction, and encapsulation of internal details.

### Scoring Criteria

| Score | Definition |
|-------|-----------|
| 9-10 | Clear bounded contexts; modules communicate only through well-defined interfaces; dependency inversion applied; no circular dependencies |
| 6-8 | Reasonable module boundaries exist but some leakage; a few cross-cutting concerns handled inconsistently |
| 3-5 | Modules exist in name only; significant coupling; shared mutable state across boundaries |
| 0-2 | Monolithic ball of mud; no discernible module boundaries; everything depends on everything |

### Checklist

- [ ] Each OpenSpec domain maps to a distinct module/package
- [ ] No circular dependency between top-level modules
- [ ] Internal types are not exported across module boundaries
- [ ] Dependency direction follows the dependency rule (inward toward domain)
- [ ] Shared kernel (if any) is explicit and minimal

### Common Anti-patterns

- God module that handles multiple unrelated domains
- Leaky abstractions exposing database schemas across boundaries
- Bi-directional dependencies between peer modules
- "Util" packages that become a dumping ground

---

## Dimension: Data Flow and State Management

- **id**: dataflow
- **model**: (inherit)
- **description**: Data flow direction clarity, state consistency guarantees, event sourcing correctness, and command/query separation.

### Scoring Criteria

| Score | Definition |
|-------|-----------|
| 9-10 | Unidirectional data flow; single source of truth for each piece of state; clear CQRS boundaries where applicable; event ordering guaranteed |
| 6-8 | Data flow is mostly clear but some state is duplicated without sync mechanisms; minor consistency gaps |
| 3-5 | Multiple sources of truth; state synchronization is ad-hoc; race conditions possible |
| 0-2 | No discernible data flow direction; global mutable state everywhere; consistency is accidental |

### Checklist

- [ ] Each piece of state has a single owner/source of truth
- [ ] Data transformations are explicit (not hidden side effects)
- [ ] Async operations have clear ordering/consistency guarantees
- [ ] Read and write paths are separable (even if not fully separated)
- [ ] State transitions map to OpenSpec scenarios

### Common Anti-patterns

- Prop drilling through 5+ layers without intermediate state management
- Shadow state that drifts from the canonical source
- Fire-and-forget mutations with no confirmation of success
- Implicit dependencies on execution order

---

## Dimension: Scalability

- **id**: scalability
- **model**: (inherit)
- **description**: Horizontal/vertical scaling capability, bottleneck identification, resource efficiency, and growth readiness.

### Scoring Criteria

| Score | Definition |
|-------|-----------|
| 9-10 | Stateless services easily horizontally scalable; data partitioning strategy defined; no single points of bottleneck; load tested |
| 6-8 | Can scale with some effort; known bottlenecks have mitigation paths; session affinity limited to specific areas |
| 3-5 | Scaling requires significant rework; in-memory state prevents horizontal scaling; single database without sharding strategy |
| 0-2 | Architecture fundamentally prevents scaling; hard-coded single-instance assumptions; no caching strategy |

### Checklist

- [ ] Stateless request handling (or explicit stateful component isolation)
- [ ] Database access patterns support read replicas / sharding
- [ ] Hot paths identified and optimized (caching, batching, pagination)
- [ ] Resource limits defined (connection pools, memory bounds, queue depths)
- [ ] Growth scenarios from OpenSpec have corresponding scaling strategies

### Common Anti-patterns

- In-process session state preventing horizontal scaling
- N+1 query patterns in critical paths
- Unbounded queues or lists that grow with data volume
- Single-writer bottleneck without partitioning strategy

---

## Dimension: Fault Tolerance and Resilience

- **id**: resilience
- **model**: (inherit)
- **description**: Failure isolation, graceful degradation, retry/idempotency, circuit breaking, and recovery strategies.

### Scoring Criteria

| Score | Definition |
|-------|-----------|
| 9-10 | Bulkhead isolation between components; circuit breakers on external calls; idempotent operations; graceful degradation paths defined; chaos-tested |
| 6-8 | Major failure modes handled; retries with backoff; some degradation paths but not comprehensive |
| 3-5 | Basic error handling exists but failures cascade; no circuit breaking; retry storms possible |
| 0-2 | No failure isolation; single component failure brings down the system; no retry logic; no timeouts |

### Checklist

- [ ] External service calls have timeouts and circuit breakers
- [ ] Retries are idempotent and use exponential backoff
- [ ] Failure in one module does not cascade to unrelated modules
- [ ] Graceful degradation defined for each critical dependency
- [ ] OpenSpec error scenarios have corresponding implementation

### Common Anti-patterns

- Unbounded retries without backoff causing thundering herd
- Missing timeouts on network calls
- Single point of failure with no fallback
- Error swallowing (catch-all with no action)

---

## Dimension: Security

- **id**: security
- **model**: opus
- **description**: Authentication/authorization correctness, data protection, attack surface minimization, and secure defaults.

### Scoring Criteria

| Score | Definition |
|-------|-----------|
| 9-10 | Defense in depth; least privilege enforced; input validation at all boundaries; secrets management; security headers; audit logging |
| 6-8 | Auth properly implemented; most inputs validated; some hardening but gaps in secondary paths |
| 3-5 | Basic auth exists but authorization is coarse; some unvalidated inputs; secrets in config files |
| 0-2 | No authentication on sensitive endpoints; SQL injection / XSS possible; secrets in code; no encryption |

### Checklist

- [ ] All endpoints enforce authentication and authorization per OpenSpec requirements
- [ ] Input validation at every trust boundary (API, message queue, file upload)
- [ ] Secrets managed externally (not in code or config files in repo)
- [ ] Data encrypted at rest and in transit where required
- [ ] OWASP Top 10 mitigations in place for web-facing surfaces
- [ ] Audit trail for sensitive operations

### Common Anti-patterns

- Broken access control (horizontal privilege escalation)
- Mass assignment / over-posting without allowlists
- Hardcoded credentials or API keys
- Missing rate limiting on authentication endpoints
- Trusting client-side validation alone

---

## Dimension: Observability

- **id**: observability
- **model**: (inherit)
- **description**: Logging/metrics/tracing coverage, alerting strategy, debugging capability, and operational readiness.

### Scoring Criteria

| Score | Definition |
|-------|-----------|
| 9-10 | Structured logging with correlation IDs; RED metrics on all services; distributed tracing; actionable alerts with runbooks; dashboards for key flows |
| 6-8 | Logging exists and is searchable; basic metrics; some tracing; alerts exist but may be noisy |
| 3-5 | Unstructured logs; minimal metrics; no tracing; alerting is reactive (on customer report) |
| 0-2 | Insufficient logging; no metrics; impossible to trace a request across services; flying blind |

### Checklist

- [ ] Structured logging with consistent fields (timestamp, level, correlation_id, service)
- [ ] Request/Error/Duration (RED) metrics for each service boundary
- [ ] Distributed tracing across async boundaries
- [ ] Alerts defined for SLO violations (not just errors)
- [ ] Key OpenSpec scenarios are traceable end-to-end

### Common Anti-patterns

- Logging sensitive data (PII, credentials)
- Alert fatigue from noisy thresholds
- Metrics without labels/dimensions (cannot slice by tenant/endpoint)
- Missing correlation between logs, metrics, and traces

---

## Dimension: Developer Experience

- **id**: devex
- **model**: (inherit)
- **description**: API consistency, documentation completeness, onboarding cost, local development ergonomics, and contribution friction.

### Scoring Criteria

| Score | Definition |
|-------|-----------|
| 9-10 | Consistent API naming and patterns; comprehensive docs; one-command local setup; fast feedback loops; clear contribution guide |
| 6-8 | APIs mostly consistent; docs cover main paths; local setup works with some manual steps; tests run reasonably fast |
| 3-5 | Inconsistent APIs; docs are outdated or sparse; local setup is painful; slow CI feedback |
| 0-2 | No API conventions; no docs; environment setup takes days; tribal knowledge required |

### Checklist

- [ ] API naming follows consistent conventions across all modules
- [ ] Error responses are uniform and machine-parseable
- [ ] README covers setup, development, testing, and deployment
- [ ] Local development environment can be started with <= 3 commands
- [ ] OpenSpec serves as living documentation (kept in sync)

### Common Anti-patterns

- Inconsistent naming (camelCase in one API, snake_case in another)
- Documentation that contradicts the code
- "Works on my machine" with no containerized dev environment
- Tests that require external services without mocks/stubs

---

## Dimension: Spec-Code Consistency

- **id**: spec_consistency
- **model**: (inherit)
- **description**: Deviation analysis between OpenSpec definitions and actual implementation — missing requirements, unspecified behaviors, and drift.

### Scoring Criteria

| Score | Definition |
|-------|-----------|
| 9-10 | Every OpenSpec requirement has corresponding implementation; no unspecified behaviors; scenarios map to tests; spec is actively maintained |
| 6-8 | Most requirements implemented; a few gaps or undocumented behaviors; spec mostly current |
| 3-5 | Significant gaps between spec and code; many unspecified behaviors; spec is stale |
| 0-2 | Spec and code have diverged completely; spec is fiction; implementation has major unspecified behaviors |

### Checklist

- [ ] Each Requirement in OpenSpec has identifiable implementation code
- [ ] Each Scenario maps to at least one test case
- [ ] No implemented behavior lacks a corresponding spec requirement
- [ ] Spec uses RFC 2119 keywords consistently (SHALL vs SHOULD vs MAY)
- [ ] Delta specs exist for recent changes (changes/ directory maintained)

### Common Anti-patterns

- "Ghost requirements" — specified but never implemented
- "Dark features" — implemented but never specified
- Spec written once and never updated as code evolves
- Scenarios that are untestable as written (vague THEN clauses)
