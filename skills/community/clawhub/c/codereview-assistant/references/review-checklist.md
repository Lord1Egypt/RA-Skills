# Code Review Checklist

## Pre-Review

- [ ] PR description exists and explains the "why"
- [ ] PR is appropriately sized (< 400 lines changed)
- [ ] CI/CD checks are passing
- [ ] Branch is up to date with target branch

## Correctness

- [ ] Logic is correct and handles edge cases
- [ ] No obvious bugs or off-by-one errors
- [ ] Error handling is appropriate
- [ ] No infinite loops or recursion risks
- [ ] Concurrency issues considered

## Security

- [ ] No hardcoded credentials or secrets
- [ ] Input validation on all user-controllable data
- [ ] SQL injection prevention (parameterized queries)
- [ ] Authentication/authorization properly enforced
- [ ] Sensitive data not logged
- [ ] No IDOR (Insecure Direct Object Reference)
- [ ] Output encoding for XSS prevention

## Testing

- [ ] Tests exist for new/changed logic
- [ ] Test coverage is adequate
- [ ] Tests actually test the right behavior
- [ ] No commented-out tests
- [ ] Edge cases covered
- [ ] Happy path covered

## Performance

- [ ] No N+1 query patterns
- [ ] Appropriate indexing on database access
- [ ] No memory leaks
- [ ] Large data sets handled efficiently
- [ ] Lazy loading used where appropriate

## Maintainability

- [ ] Code follows project style conventions
- [ ] Variable/function names are descriptive
- [ ] Functions are reasonably sized (< 50 lines ideal)
- [ ] No deeply nested code (> 3 levels)
- [ ] DRY principle followed
- [ ] No commented-out code
- [ ] Comments explain "why", not "what"

## API Design (if applicable)

- [ ] RESTful conventions followed
- [ ] Appropriate HTTP methods used
- [ ] Status codes are correct
- [ ] Error responses are consistent
- [ ] Versioning strategy followed

## Dependencies

- [ ] New dependencies are necessary
- [ ] Dependencies are from trusted sources
- [ ] No transitive dependency vulnerabilities
- [ ] Dependencies are at stable versions

## Documentation

- [ ] Public APIs have documentation
- [ ] Complex logic is explained
- [ ] README updated if needed
- [ ] Breaking changes documented
