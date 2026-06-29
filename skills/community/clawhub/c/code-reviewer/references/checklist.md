# Code Review Checklist

## 1. Security

### Injection Attacks
- [ ] SQL queries use parameterized statements / prepared statements (no string concatenation)
- [ ] No OS command execution with user input (`os.system`, `exec`, `Runtime.exec`, `child_process.exec`)
- [ ] Template engines use auto-escaping (no `dangerouslySetInnerHTML`, `{!! !!}`, `innerHTML` with user data)
- [ ] No eval on user input (`eval()`, `Function()`, `new Function()`)

### Authentication & Authorization
- [ ] Passwords hashed with bcrypt/scrypt/argon2 (not MD5/SHA1/plaintext)
- [ ] JWT tokens validated for signature, expiry, and issuer
- [ ] Authorization checks present on every protected route/endpoint
- [ ] No hardcoded credentials, API keys, or tokens in source code
- [ ] Secrets loaded from environment variables or secret managers

### Data Exposure
- [ ] Sensitive data not logged (passwords, tokens, PII, credit card numbers)
- [ ] API responses do not leak internal field names or stack traces
- [ ] HTTPS enforced; no mixed content
- [ ] CORS configured restrictively (no `Access-Control-Allow-Origin: *` on sensitive endpoints)

### File Operations
- [ ] File paths validated against traversal attacks (no `../` in user-controlled paths)
- [ ] Upload restrictions: file type, size, and content validation
- [ ] Download paths restricted to allowed directories

### Dependencies
- [ ] No known vulnerable dependencies (checked via `npm audit` / `pip audit` / `snyk`)
- [ ] Dependency versions pinned (no floating `*` or `latest`)

---

## 2. Performance

### Database
- [ ] No N+1 query patterns (queries inside loops)
- [ ] Database indexes exist for frequently queried columns
- [ ] Pagination applied to list endpoints (no unbounded `SELECT *`)
- [ ] ORM queries select only needed columns (no `SELECT *` when only 2 fields used)

### Algorithms & Data Structures
- [ ] No O(n^2) or worse inside hot paths / loops
- [ ] Appropriate data structures used (Set for lookups instead of Array.includes)
- [ ] No unnecessary re-computation of the same value inside loops

### Memory
- [ ] No memory leaks (event listeners removed, intervals cleared, connections closed)
- [ ] Large collections streamed rather than loaded entirely into memory
- [ ] No unnecessary object retention in long-lived scopes (closures, globals, singletons)

### Concurrency
- [ ] Async operations not blocking the event loop (no sync I/O in async contexts)
- [ ] Database connections released properly (try/finally or using context managers)
- [ ] Race conditions addressed (proper locking / atomic operations)

---

## 3. Code Quality

### Readability
- [ ] Variable/function names are descriptive and self-documenting
- [ ] Functions do one thing (Single Responsibility)
- [ ] No dead code (unused variables, functions, imports, unreachable code)
- [ ] No magic numbers / strings (use named constants)
- [ ] Consistent naming convention (camelCase / snake_case per language convention)

### Complexity
- [ ] Functions under 50 lines (refactor if longer)
- [ ] Cyclomatic complexity under 10 per function (use `scripts/analyze_complexity.py`)
- [ ] Nesting depth under 4 levels (extract early returns / guard clauses)
- [ ] Parameter count under 5 (use parameter objects if more)

### Duplication
- [ ] No copy-pasted code blocks (DRY principle)
- [ ] Shared logic extracted into reusable functions/modules
- [ ] No duplicated string literals / magic constants

### Architecture
- [ ] Proper separation of concerns (controller/service/repository layers)
- [ ] No business logic in presentation layer (views/templates/controllers)
- [ ] Dependencies injected (not hard-wired / globally accessed)
- [ ] No circular dependencies between modules

---

## 4. Error Handling

### Coverage
- [ ] External calls wrapped in try/catch (network, file, database, subprocess)
- [ ] Promise rejections handled (no unhandled `.then()` without `.catch()`)
- [ ] Error states tested (not just happy path)
- [ ] No empty catch blocks (`catch {}` or `except: pass`)

### Quality
- [ ] Errors logged with context (what operation, what input, what failed)
- [ ] Custom error types used for domain errors (not generic Error/Exception)
- [ ] Error messages user-friendly (no stack traces or internal details exposed)
- [ ] Errors not swallowed silently (at minimum logged)

### Resilience
- [ ] Retry logic for transient failures (network, rate limits)
- [ ] Circuit breakers / timeouts for external service calls
- [ ] Graceful degradation when optional services unavailable
- [ ] Idempotency for retry-safe operations

---

## 5. Testing

### Coverage
- [ ] Unit tests exist for business logic
- [ ] Integration tests exist for API endpoints
- [ ] Edge cases tested (empty input, null, boundary values, large input)
- [ ] Error paths tested (not just happy path)

### Quality
- [ ] Tests are independent (no shared mutable state, no order dependency)
- [ ] Test names describe the scenario and expected outcome
- [ ] No flaky tests (time-dependent, race conditions, external service calls)
- [ ] Mocks/stubs used for external dependencies (not real DB/API calls in unit tests)
- [ ] Test data is realistic and representative

### Maintainability
- [ ] Test setup is minimal and clear (Arrange-Act-Assert pattern)
- [ ] No test logic duplication (use test factories/builders)
- [ ] Tests run fast (unit tests under 1s each)

---

## 6. Documentation

### Code Level
- [ ] Public API functions/classes documented (JSDoc, docstrings, GoDoc)
- [ ] Complex algorithms explained with comments (why, not what)
- [ ] TODO/FIXME comments include issue numbers and context
- [ ] No outdated comments (comments that contradict the code)

### Project Level
- [ ] README exists with setup/run/test instructions
- [ ] Environment variables documented (`.env.example`)
- [ ] API changes reflected in API documentation (OpenAPI/Swagger)
- [ ] Breaking changes noted in CHANGELOG
