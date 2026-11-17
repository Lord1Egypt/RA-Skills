# Node / TypeScript Review Rules

Use for Node.js, TypeScript, Express, Fastify, NestJS, serverless handlers, package scripts, and JS/TS libraries.

## Bugs And Reliability

- Check missing `await`, unhandled promises, promise fan-out without bounds, and error paths that skip cleanup.
- Look for event-loop blocking work, global mutable state, process-level side effects, and non-idempotent retries.
- Verify strictness assumptions: `strictNullChecks`, `noImplicitAny`, unsafe casts, `any`, `unknown`, and non-null assertions.
- Check timezone, decimal, bigint, JSON serialization, and input normalization behavior.

## Security

- Check request validation, schema parsing, auth middleware ordering, object-level authorization, and tenant scoping.
- Look for command injection, path traversal, unsafe dynamic imports/eval, prototype pollution, SSRF, open redirects, and unsafe regex.
- Verify secrets are not exposed to client bundles, logs, `.env.example`, tests, Docker images, or build output.
- Review CORS, cookie flags, session storage, JWT validation, password hashing, rate limiting, and CSRF where browser cookies are used.

## Architecture

- Route handlers/controllers should delegate business logic.
- Keep domain/application logic independent from HTTP framework objects unless intentionally simple.
- Avoid service locators, ambient context, broad utility modules, and import cycles.
- Prefer typed contracts at boundaries: DTOs, schemas, message payloads, persistence rows.

## Performance

- Look for sequential independent IO, N+1 API/database calls, excessive JSON parsing/stringifying, and unbounded concurrency.
- Check stream handling for large files and response payloads.
- Review cache keys for tenant/user scoping and invalidation.

## Testing

- Ensure validation, authorization, error paths, async failures, and integration boundaries are tested.
- Flag brittle snapshot tests and mocks that hide contract drift.
