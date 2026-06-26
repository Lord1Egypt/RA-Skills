# FlowForge Generic Rubric — 220 Criteria

You are the Rubric QA Agent. Score the implementation against all 220 criteria below.
Inspect the actual code in the repository AND the forge workspace files (implementation_plan.json, spec.md, progress.log). Answer YES or NO for each. No partial credit.

## Output Format

```markdown
# Rubric Report — 220 Criteria

**Score: X/220**

## T: Trajectory & Process (20)
| # | Criterion | Score |
|---|-----------|-------|
| T1 | ... | YES/NO |
...

## A: Architecture & Design (40)
| # | Criterion | Score |
|---|-----------|-------|
| A1 | ... | YES/NO |
...

## Final Score: X/200 (XX%)
**Verdict**: SHIP (≥198) | NEEDS WORK (165–197) | MAJOR REWORK (<165)
```

---

## T: Trajectory & Process (20 criteria)

T1. Implementation followed the phases in implementation_plan.json in the correct order — no phases skipped or reordered without documented rationale
T2. Each subtask was verified before moving to the next — no bulk "just ship it all" commits
T3. The final implementation matches the spec.md requirements — no undocumented scope additions or removals
T4. The agent investigated existing code before writing new code — no duplicate utilities or reimplemented existing functions
T5. No unnecessary file rewrites — files modified only when the subtask required it
T6. Implementation plan phases were not collapsed or merged without justification
T7. The agent used consistent patterns from the existing codebase — naming, module structure, error handling style all match surrounding code
T8. Tool/library choices match what was specified in the plan — no surprise new dependencies introduced without rationale
T9. Function signatures match what was specified in the implementation plan
T10. No scope creep — the agent built what was asked, not extra features that weren't in the spec
T11. Verification criteria in implementation_plan.json were actually checked — not just assumed passing
T12. When the agent deviated from the plan, it documented why in a comment or log
T13. No circular rework — the agent did not implement, then undo, then re-implement the same thing
T14. Module boundaries established in Phase 1 / infrastructure phase were respected throughout
T15. The agent did not introduce global state or side effects not present in the spec
T16. Test files were written alongside implementation, not as an afterthought after all code was written
T17. Import/dependency graph matches what the spec described — no hidden cross-module dependencies
T18. The agent handled the hardest/riskiest subtask first within each phase, not last (fail fast principle)
T19. Error handling was implemented inline as each module was built — not added as a final pass
T20. The final state of the codebase reflects a single coherent implementation, not layered patches on top of each other

## A: Architecture & Design (40 criteria)

A1. Clear separation of concerns — modules have single responsibilities
A2. No circular dependencies between modules
A3. Business logic separated from I/O and infrastructure
A4. Configuration externalized via environment variables, not hardcoded
A5. Consistent naming conventions throughout (files, functions, variables)
A6. Directory structure is logical and navigable
A7. Entry points are clearly defined and documented
A8. Public API surface is minimal — only what's needed is exported
A9. Abstractions are at the right level — not too leaky, not too opaque
A10. Dependencies are explicit, not hidden or implicit
A11. Side effects are isolated and predictable
A12. State management is consistent and explicit
A13. No god objects/modules that do everything
A14. Interfaces/behaviours defined where multiple implementations exist
A15. Cross-cutting concerns (logging, auth, metrics) handled consistently
A16. Feature flags or compile-time config used for optional behavior
A17. Backwards compatibility considered for public interfaces
A18. Extension points exist without requiring core changes
A19. Data flow through the system is easy to trace
A20. No unnecessary coupling between unrelated modules
A21. Domain model reflects real-world concepts accurately
A22. Infrastructure code (DB, HTTP) isolated from domain logic
A23. Error types are structured and meaningful, not stringly typed
A24. Async/concurrent code is clearly marked and reasoned about
A25. Race conditions considered and addressed where relevant
A26. Memory management is explicit where needed (buffers, caches)
A27. Resource cleanup is guaranteed (files, connections, processes)
A28. Retry logic is centralized, not scattered across the codebase
A29. Timeouts are defined at every external call boundary
A30. Circuit breakers or backpressure exist for critical external dependencies
A31. Module interfaces are stable — implementation can change without callers knowing
A32. Versioning strategy exists for APIs that external systems consume
A33. No dead code in the critical path
A34. Feature code is not mixed with test utilities or dev tooling
A35. Build system is clean — no unused dependencies in manifest
A36. Dependency versions are pinned appropriately
A37. No transitive dependency conflicts
A38. Monorepo vs. polyrepo decision is consistent with team structure
A39. Code ownership is clear — no orphaned modules
A40. Architecture matches the scale requirements (not over/under-engineered)

## B: Code Quality (40 criteria)

B1. Functions are short — do one thing, fit in one screen
B2. No functions longer than 50 lines without strong justification
B3. Variable names are descriptive — no single-letter names outside loops
B4. No magic numbers — constants are named and explained
B5. No commented-out code in production paths
B6. No TODO/FIXME in critical paths without linked issues
B7. Consistent formatting throughout (linter/formatter enforced)
B8. No unused imports or variables
B9. No unnecessary type casts or unsafe coercions
B10. Pattern matching / switch exhaustiveness checked
B11. Guard clauses used to reduce nesting
B12. Early returns used to reduce nesting
B13. No deeply nested conditionals (max 3 levels)
B14. DRY — repeated logic is extracted, not copy-pasted
B15. WET where appropriate — no premature abstraction
B16. Pure functions preferred where side effects aren't needed
B17. No global mutable state
B18. Immutable data structures used where possible
B19. Collections iterated functionally (map/filter/reduce) not imperatively where idiomatic
B20. String interpolation/formatting done safely (no injection risk)
B21. Numeric types match domain (int vs float vs decimal for money)
B22. Date/time handling is timezone-aware where needed
B23. Encoding/decoding (JSON, binary) validated at boundaries
B24. Null/nil handling is explicit — no silent null propagation
B25. Optional/maybe types used instead of nullable where idiomatic
B26. No silent error swallowing — errors always logged or propagated
B27. Function signatures match their documentation
B28. Return types are consistent — no sometimes-nil, sometimes-value
B29. No boolean traps — boolean args replaced with options/enums where ambiguous
B30. No flag arguments that change function behavior fundamentally
B31. Recursion has clear base cases and termination guarantees
B32. Loops have clear termination conditions
B33. Concurrency primitives used correctly (locks, channels, actors)
B34. No busy-waiting or polling where events/callbacks exist
B35. I/O operations are appropriately buffered
B36. Large data processing is streamed, not loaded into memory wholesale
B37. Regex patterns are compiled once, not recreated on every call
B38. String concatenation in hot paths uses efficient builder patterns
B39. Cryptographic operations use vetted libraries, not homebrew
B40. Random number generation uses appropriate source (secure vs. fast)

## C: Testing (40 criteria)

C1. Unit tests exist for all public functions
C2. Unit tests are isolated — no real I/O, DB, or network
C3. Tests are deterministic — same result every run
C4. Tests are fast — unit suite runs in under 30 seconds
C5. Integration tests exist for all external dependencies
C6. Integration tests cover happy path and error paths
C7. Test names describe the scenario, not the implementation
C8. Tests follow Arrange-Act-Assert or Given-When-Then structure
C9. No test logic in production code
C10. No production secrets in test fixtures
C11. Test data is minimal — only what the test needs
C12. Fixtures and factories used for complex test data
C13. Mocks/stubs are used sparingly — prefer real implementations where fast
C14. Mock contracts match the real interface (no lying mocks)
C15. Edge cases tested: empty input, max size, zero, negative
C16. Boundary conditions tested: off-by-one, limits
C17. Error paths tested: invalid input, missing data, timeouts
C18. Concurrency tested where relevant: race conditions, ordering
C19. Tests are readable without needing to read the implementation
C20. No test depends on execution order
C21. No test has hidden dependencies on global state
C22. Test coverage is meaningful — not just line coverage chasing
C23. Critical paths have 100% branch coverage
C24. Tests exist for all fixed bugs (regression tests)
C25. Performance-sensitive paths have benchmark tests
C26. Load/stress tested where relevant
C27. Contract tests exist for external API integrations
C28. Snapshot tests used where output format must be stable
C29. Tests run in CI on every commit
C30. Flaky tests are tracked and fixed, not disabled
C31. Test doubles (mocks/stubs/fakes) documented so it's clear what's real
C32. Parameterized tests used for multiple similar scenarios
C33. Tests cover authentication and authorization paths
C34. Tests verify error messages and codes, not just status
C35. Database tests use transactions that roll back
C36. File system tests use temp directories
C37. Time-dependent tests use frozen/mocked clocks
C38. External service tests use recorded responses (VCR/cassettes) or mocks
C39. Test helpers and utilities are in a dedicated test support module
C40. Test suite has a clear README or guide for running locally

## D: Error Handling & Resilience (30 criteria)

D1. All errors are handled — no unhandled exceptions in production paths
D2. Error messages are actionable — tells the user what went wrong and how to fix it
D3. Error messages don't leak sensitive data (stack traces, credentials, PII)
D4. Errors are logged with enough context to debug (request ID, user, timestamp)
D5. Error types distinguish user errors from system errors from programming errors
D6. HTTP status codes match the error type (4xx vs 5xx)
D7. Retry logic exists for transient failures (network, DB locks)
D8. Retry logic has exponential backoff with jitter
D9. Maximum retry count is bounded — no infinite retry loops
D10. Circuit breakers exist for external service calls
D11. Circuit breaker state is observable (metrics, logs)
D12. Timeout is set on every external call
D13. Fallback behavior defined when dependencies are unavailable
D14. Graceful degradation — partial functionality vs total failure
D15. Panic/crash recovery exists at process boundaries
D16. Dead letter queues or error queues for async failures
D17. Database transactions rolled back on error
D18. Partial writes are detected and handled (idempotency keys)
D19. Input validation at every public boundary
D20. Input validation errors return useful messages to callers
D21. File/network resources closed in finally/defer/after blocks
D22. Process supervision restarts crashed workers
D23. Health check endpoint reflects actual dependency health
D24. Startup errors fail fast with clear messages
D25. Shutdown is graceful — in-flight requests complete
D26. Data corruption detected early — assertions on invariants
D27. External API errors surfaced to callers, not swallowed
D28. Rate limit responses handled — backoff, not crash
D29. Memory/disk exhaustion handled — not silently OOM'd
D30. Cascading failure prevented — bulkheads between subsystems

## E: Security (20 criteria)

E1. No secrets in source code or version control
E2. No secrets in logs
E3. Authentication required on all protected routes
E4. Authorization checked at the resource level, not just route level
E5. Input sanitized before use in queries (SQL injection prevention)
E6. Input sanitized before rendering (XSS prevention)
E7. CSRF protection on state-changing endpoints
E8. Rate limiting on authentication endpoints
E9. Sensitive data encrypted at rest where required
E10. TLS/HTTPS enforced — no plaintext sensitive data in transit
E11. Passwords hashed with modern algorithm (bcrypt/argon2/scrypt)
E12. Tokens have appropriate expiry
E13. Token rotation supported
E14. File uploads validated for type and size
E15. Directory traversal prevented in file operations
E16. Third-party dependencies audited for known vulnerabilities
E17. Principle of least privilege applied to DB connections and service accounts
E18. Audit log exists for sensitive operations
E19. Error responses don't reveal internal structure to external callers
E20. Dependency pinning prevents supply chain attacks

## F: Documentation (15 criteria)

F1. README covers: what it is, how to set up, how to run, how to test
F2. Architecture decision records (ADRs) exist for non-obvious decisions
F3. Public API documented with types, params, return values, errors
F4. Complex algorithms have inline explanation comments
F5. Non-obvious business rules documented in code comments
F6. Configuration options documented with examples and defaults
F7. Deployment/infrastructure documented
F8. Runbook exists for common operational tasks
F9. Changelog maintained
F10. Contributing guide exists for open-source projects
F11. Code examples provided for non-trivial integrations
F12. Glossary of domain terms where the domain is complex
F13. Diagrams for complex data flows or state machines
F14. External dependencies listed with version and purpose
F15. Known limitations documented

## G: Observability (15 criteria)

G1. Structured logging used (JSON or key-value, not free text)
G2. Log levels used consistently (debug/info/warn/error)
G3. Request IDs propagated through all log lines for a request
G4. Key business events logged (user signup, order placed, payment failed)
G5. Metrics emitted for latency, throughput, error rate on critical paths
G6. Health check endpoint returns meaningful status
G7. Readiness vs liveness probes distinguished
G8. Distributed tracing spans created for cross-service calls
G9. Trace IDs propagated through async boundaries
G10. Dashboards or alerts defined for key metrics
G11. Error rates alerted on — not just discovered in logs
G12. Latency p95/p99 tracked, not just averages
G13. Dependency health visible in monitoring
G14. Feature flag state observable without code changes
G15. Log volume is appropriate — not silent, not noisy
