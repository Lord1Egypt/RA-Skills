# Review Categories

Use these categories to classify findings. A finding can mention secondary categories, but it should have one primary category.

## Bugs

Look for functional defects and reliability hazards:

- null, undefined, optional, and empty-state mistakes
- off-by-one errors and incorrect boundary checks
- race conditions, deadlocks, lost updates, and non-idempotent retries
- exception swallowing, overly broad catches, and broken error propagation
- incorrect time, timezone, locale, currency, encoding, or precision handling
- resource leaks, unclosed streams, unbounded memory growth
- broken validation order and inconsistent invariants
- transactional consistency failures

## Security

Look for exploitable behavior, insecure defaults, or security-relevant omissions:

- injection: SQL, NoSQL, command, LDAP, XPath, template, expression language
- SSRF, open redirect, path traversal, unsafe file upload/download
- authentication and authorization bypass
- missing tenant, ownership, role, scope, or object-level checks
- secrets in code, logs, errors, test fixtures, generated files, or client bundles
- weak cryptography, hardcoded keys, insecure randomness, unsafe token handling
- deserialization, prototype pollution, unsafe reflection, unsafe dynamic execution
- sensitive data exposure in logs, telemetry, cache, browser storage, responses
- dependency or container risks that are visible from project files

## Architecture And SOLID

Look for structural risks:

- domain depending on infrastructure or framework details
- controllers, views, routes, or handlers containing business rules
- services that own unrelated responsibilities
- missing boundaries between modules, tenants, contexts, or external integrations
- dependency inversion violations that make core logic hard to test
- excessive coupling, circular dependencies, unstable abstractions
- leaky repositories, anemic domain models where behavior clearly belongs in domain objects
- missing transaction or unit-of-work boundaries

## Code Smells

Find maintainability issues that increase defect risk:

- large methods/classes, deep nesting, duplicated logic
- primitive obsession, long parameter lists, boolean blindness
- feature envy, shotgun surgery, temporal coupling
- inconsistent naming where it harms comprehension
- comments compensating for unclear structure
- unreachable code, dead branches, speculative abstractions
- confusing state mutation or hidden side effects

## Patterns

Recommend design patterns only when the code shows pressure that the pattern would relieve:

- Strategy: branching by behavior that changes independently.
- Factory: object creation contains conditional policy or complex construction.
- Adapter: external API shape leaks into domain or app services.
- Decorator: optional behavior stacks around a stable interface.
- Chain of Responsibility: ordered handlers with clear stop/continue behavior.
- State: behavior changes by lifecycle state and transition rules matter.
- Specification: composable business predicates are duplicated or mixed with persistence.
- Repository: persistence access leaks broadly, and a boundary would simplify callers.
- Unit of Work: multiple writes must commit or roll back together.

Do not recommend a pattern solely because a pattern name could fit. Record the complexity it removes and the complexity it adds.

## Anti-Patterns

Identify anti-patterns only when there is concrete damage:

- global Singleton state causing tests, concurrency, or lifecycle issues
- Service Locator hiding dependencies
- God Object / God Service
- Big Ball of Mud boundaries
- Anemic Domain Model when business behavior is scattered and inconsistent
- Active Record misuse in complex domains
- Golden Hammer pattern use
- cargo-cult abstraction or premature generalization

## Performance

Look for evidence-backed performance risks:

- N+1 database or API calls
- missing indexes or non-sargable predicates
- unbounded queries, pagination gaps, excessive payloads
- sequential IO where independent calls could be bounded and parallelized
- blocking calls in async/event-loop contexts
- unbounded retries, no backoff, no circuit breaking
- excessive allocations, serialization, parsing, reflection, or re-rendering
- cache misuse: stale, unbounded, cross-tenant, or missing invalidation

## Observability

Check whether production behavior can be understood:

- missing structured logs around critical state transitions
- logs without correlation/request/trace IDs
- sensitive data logged
- swallowed errors without metrics or trace context
- no metrics for queue lag, retry count, failure rate, latency, throughput
- missing audit logs for security-sensitive actions
- noisy logs that hide important signals

## Testing And Testability

Look for:

- high-risk code with no focused tests
- brittle tests tied to implementation instead of behavior
- over-mocking that hides integration failures
- nondeterministic time, randomness, concurrency, network, or filesystem use
- test fixtures that bypass real validation
- missing contract tests around external APIs, messaging, persistence, or migrations
- hard-to-test static/global dependencies
