# Database Review Rules

Use for SQL, NoSQL, ORMs, migrations, schema design, queries, stored procedures, and data access layers.

## Correctness

- Check constraints, foreign keys, uniqueness, nullability, default values, cascade behavior, and migration ordering.
- Look for application-only invariants that should be enforced by the database when race conditions matter.
- Review transaction boundaries, isolation assumptions, lost updates, idempotency keys, and retry safety.

## Security

- Check injection risk, row-level security, tenant scoping, least-privilege accounts, secrets, audit tables, and sensitive data retention.
- Verify raw query construction uses parameters and safe identifier handling.

## Performance

- Look for missing or unused indexes, non-sargable predicates, full scans, sort/hash pressure, N+1 access, unbounded queries, and excessive joins.
- Check pagination strategy, batch size, connection pool settings, lock duration, and migration impact on large tables.

## Architecture

- Repositories/data access should expose use-case-friendly operations, not arbitrary persistence details everywhere.
- Avoid leaking ORM entities into unrelated layers when it creates coupling or lazy-loading hazards.

## Testing

- Prefer migration tests, repository integration tests, and contract tests for critical queries.
- Flag tests that use different database semantics from production when behavior depends on constraints, transactions, or SQL dialect.
