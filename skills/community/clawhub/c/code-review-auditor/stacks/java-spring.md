# Java / Spring Review Rules

Use for Java, Spring Boot, Spring MVC/WebFlux, Spring Security, Spring Data, JPA/Hibernate, Maven, and Gradle projects.

## Bugs And Reliability

- Check `@Transactional` placement, propagation, read-only misuse, self-invocation bypass, async boundaries, and lazy-loading outside sessions.
- Look for swallowed exceptions in controllers, listeners, scheduled jobs, and transaction boundaries.
- Check nullability contracts, `Optional` misuse, mutable shared state in singleton beans, and static caches.
- Verify time handling uses explicit timezone/clock where business logic depends on time.
- Review resource handling for streams, files, HTTP clients, database cursors, and executors.

## Security

- Verify Spring Security configuration order, public routes, CSRF decisions, CORS, method security, and object-level authorization.
- Check whether tenant/user ownership is enforced in service or query layer, not only in UI.
- Look for unsafe SpEL, reflection, deserialization, file path use, redirects, and upload handling.
- Check secrets in `application*.yml`, properties, tests, Docker files, and logs.
- Validate password/token handling, JWT audience/issuer/expiry checks, and refresh-token lifecycle.

## Architecture

- Controllers should orchestrate HTTP concerns, not own domain rules.
- Services should avoid becoming transaction scripts for unrelated use cases.
- Domain logic should not depend directly on Spring annotations unless the project intentionally uses that style.
- Repositories should not leak persistence entities into layers where DTOs/domain objects are expected.
- Avoid circular Spring bean dependencies and hidden lifecycle coupling.

## Performance

- Check JPA N+1, eager loading, unbounded repository methods, missing pagination, and large object graphs.
- Look for blocking calls in WebFlux/reactive flows.
- Review connection pool use, transaction duration, batch writes, and inefficient mapping loops.

## Testing

- Prefer focused unit tests for domain rules, slice tests for web/data layers, and integration tests for transaction/security behavior.
- Flag tests that bypass Spring Security or transaction behavior while claiming end-to-end coverage.
