---
name: code-review-plus
description: "Enhanced code review with AI/ML-specific checks, multi-language support, security vulnerability patterns, and integration with automated testing. Covers security, performance, correctness, maintainability, testing, AI/ML, and language-specific best practices."
metadata:
  author: opencode
  version: 2.0
  tags: code-review, security, testing, ai-ml, multi-language
  compatibility: opencode
  license: MIT
---

# Code Review Plus

Enhanced code review covering security, performance, correctness, maintainability, testing, AI/ML, and language-specific best practices.

## Review Dimensions

| Dimension | Focus | Priority |
|-----------|-------|----------|
| Security | Vulnerabilities, auth, data exposure | Critical |
| Performance | Speed, memory, scalability bottlenecks | High |
| Correctness | Logic errors, edge cases, data integrity | High |
| Maintainability | Readability, structure, future-proofing | Medium |
| Testing | Coverage, quality, reliability of tests | Medium |
| AI/ML | Model safety, data leakage, bias | High |
| Language | Idiomatic patterns, best practices | Medium |

## Security Checklist

- [ ] **SQL Injection** — All queries use parameterized statements or ORM
- [ ] **XSS** — User content escaped/sanitized before rendering
- [ ] **CSRF Protection** — State-changing requests require valid CSRF tokens
- [ ] **Authentication** — Protected endpoints verify authentication
- [ ] **Authorization** — Resource access scoped to requesting user
- [ ] **Input Validation** — All external input validated server-side
- [ ] **Secrets Management** — No credentials in source code
- [ ] **Dependency Safety** — Dependencies from trusted sources, no known CVEs
- [ ] **Sensitive Data** — PII/tokens never logged or in error messages
- [ ] **Rate Limiting** — Public/auth endpoints have rate limits
- [ ] **File Upload Safety** — Files validated for type/size, stored outside webroot
- [ ] **HTTP Security Headers** — CSP, X-Content-Type-Options, HSTS set

## AI/ML-Specific Checklist

- [ ] **Data Leakage** — Training data not exposed in predictions
- [ ] **Prompt Injection** — User input not injected into prompts without sanitization
- [ ] **Model Safety** — Output filtering for harmful content
- [ ] **Bias Detection** — Model outputs checked for demographic bias
- [ ] **Cost Control** — API calls budgeted, loops prevented
- [ ] **Fallback Handling** — Graceful degradation when AI services fail
- [ ] **Token Limits** — Input/output token limits enforced
- [ ] **Caching** — Expensive AI calls cached where appropriate
- [ ] **Rate Limiting** — AI API calls rate-limited
- [ ] **Logging** — AI interactions logged for debugging/audit

## Performance Checklist

- [ ] **N+1 Queries** — Database access patterns batched/joined
- [ ] **Unnecessary Re-renders** — Components re-render only when needed
- [ ] **Memory Leaks** — Event listeners, subscriptions cleaned up
- [ ] **Bundle Size** — Dependencies tree-shakeable, large libs loaded dynamically
- [ ] **Lazy Loading** — Heavy components use code splitting
- [ ] **Caching Strategy** — Expensive computations use caching
- [ ] **Database Indexing** — Queries filter/sort on indexed columns
- [ ] **Pagination** — List endpoints use pagination
- [ ] **Async Operations** — Long tasks offloaded to background jobs
- [ ] **Image Optimization** — Proper sizing, modern formats, CDN

## Correctness Checklist

- [ ] **Edge Cases** — Empty arrays, zero values, max values handled
- [ ] **Null/Undefined** — Nullable values checked before access
- [ ] **Off-by-One** — Loop bounds, pagination offsets verified
- [ ] **Race Conditions** — Concurrent access uses locks/transactions
- [ ] **Timezone Handling** — Dates stored in UTC
- [ ] **Unicode** — String ops handle multi-byte characters
- [ ] **Integer Overflow** — Large number arithmetic uses BigInt/Decimal
- [ ] **Error Propagation** — Async errors caught and handled
- [ ] **State Consistency** — Multi-step mutations transactional
- [ ] **Boundary Validation** — Boundary values tested

## Maintainability Checklist

- [ ] **Naming Clarity** — Descriptive names revealing intent
- [ ] **Single Responsibility** — Each function/class does one thing
- [ ] **DRY** — Duplicated logic extracted to utilities
- [ ] **Cyclomatic Complexity** — Low branching complexity
- [ ] **Error Handling** — Errors caught, logged, surfaced meaningfully
- [ ] **Dead Code** — Commented code, unused imports removed
- [ ] **Magic Numbers** — Literals extracted to named constants
- [ ] **Consistent Patterns** — New code follows codebase conventions
- [ ] **Function Length** — Short enough to understand at a glance
- [ ] **Dependency Direction** — Dependencies point inward

## Testing Checklist

- [ ] **Test Coverage** — New logic paths have tests
- [ ] **Edge Case Tests** — Boundary values, empty inputs tested
- [ ] **No Flaky Tests** — Deterministic, no timing reliance
- [ ] **Test Independence** — Tests set up/tear down own state
- [ ] **Meaningful Assertions** — Assert on behavior, not implementation
- [ ] **Test Readability** — Arrange-Act-Assert pattern
- [ ] **Mocking Discipline** — Only external boundaries mocked
- [ ] **Regression Tests** — Bug fixes include reproducing tests

## Language-Specific Patterns

### Python
- Type hints for public functions
- Context managers for resource cleanup
- Virtual environments for dependency isolation
- Black/flake8 formatting
- Docstrings for public APIs

### JavaScript/TypeScript
- ESLint/Prettier formatting
- TypeScript strict mode
- Async/await over raw promises
- Optional chaining for null safety
- Proper error boundaries in React

### Go
- Error handling with errors.Is/As
- Context propagation
- Proper goroutine lifecycle
- gofmt/goimports formatting
- Interface design patterns

## Review Process

| Pass | Focus | Time | What to Look For |
|------|-------|------|------------------|
| First | High-level structure | 2-5 min | Architecture, file organization, API design |
| Second | Line-by-line detail | Bulk | Logic, security, performance, edge cases |
| Third | Edge cases & hardening | 5 min | Failure modes, concurrency, boundary values |

## Severity Levels

| Level | Label | Meaning | Blocks Merge? |
|-------|-------|---------|---------------|
| Critical | `[CRITICAL]` | Security vulnerability, data loss, crash | Yes |
| Major | `[MAJOR]` | Bug, logic error, performance regression | Yes |
| Minor | `[MINOR]` | Future maintenance cost reduction | No |
| Nitpick | `[NIT]` | Style preference, naming suggestion | No |

## Giving Feedback

### Principles

- **Be specific** — Point to exact line and explain issue
- **Explain why** — State risk or consequence
- **Suggest a fix** — Offer concrete alternative or code snippet
- **Ask, don't demand** — Use questions for subjective points
- **Acknowledge good work** — Call out clean solutions
- **Separate blocking from non-blocking** — Use severity labels

### Example Comments

**Bad:**
> This is wrong. Fix it.

**Good:**
> `[MAJOR]` This query interpolates user input directly into SQL (line 42), vulnerable to SQL injection. Consider:
> ```sql
> SELECT * FROM users WHERE id = $1
> ```

## Anti-Patterns

| Anti-Pattern | Description |
|--------------|-------------|
| **Rubber-Stamping** | Approving without reading |
| **Bikeshedding** | Debating variable names while ignoring bugs |
| **Blocking on Style** | Refusing over formatting a linter should enforce |
| **Gatekeeping** | Requiring personal preferred approach |
| **Drive-by Reviews** | One vague comment and disappearing |
| **Scope Creep** | Requesting unrelated refactors |
| **Stale Reviews** | Letting PRs sit for days |
| **Emotional Language** | "This is terrible" or "obviously wrong" |

## NEVER Do

1. **NEVER approve without reading every changed line**
2. **NEVER block a PR solely for style preferences**
3. **NEVER leave feedback without severity level**
4. **NEVER request changes without explaining why**
5. **NEVER review more than 400 lines in one sitting**
6. **NEVER skip the security checklist**
7. **NEVER make it personal**
