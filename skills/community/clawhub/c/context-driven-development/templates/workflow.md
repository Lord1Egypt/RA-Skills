# Workflow

## Development Methodology

[e.g., TDD (Test-Driven Development) with trunk-based development]

## Git Workflow

### Branching Strategy

- `main` — Production-ready code, always deployable
- `feature/<name>` — Feature development branches
- `fix/<name>` — Bug fix branches

### Commit Convention

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:** feat, fix, docs, refactor, test, chore

### Pull Requests

- [ ] All tests pass
- [ ] Code review from at least one team member
- [ ] No merge commits; rebase before merge

## Testing Requirements

| Type | Target | Notes |
|------|--------|-------|
| Unit Tests | 80% coverage | For all business logic |
| Integration Tests | Critical paths | API endpoints, database operations |
| E2E Tests | Happy paths | Core user journeys |

## Quality Gates

Before merging:
- [ ] All tests pass
- [ ] Linting passes with no errors
- [ ] Type checking passes
- [ ] No security vulnerabilities (npm audit / pip-audit)
- [ ] Coverage threshold met

## Deployment

| Environment | Trigger | URL |
|-------------|---------|-----|
| Preview | PR opened | Auto-generated |
| Staging | Merge to main | staging.example.com |
| Production | Manual release | example.com |

## Code Review Checklist

- [ ] Code is readable and follows project conventions
- [ ] Tests cover new functionality
- [ ] No obvious security issues
- [ ] Documentation updated if needed
- [ ] No unnecessary complexity
