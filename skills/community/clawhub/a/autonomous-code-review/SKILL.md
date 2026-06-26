# Autonomous Code Review

**Category:** Development  
**Author:** Beta  
**Version:** 1.0.0  
**Runtime:** OpenClaw + Claude/GPT  

## What It Does

Automatically review code for bugs, security issues, performance problems, and style violations. Acts as a tireless first-pass reviewer on any codebase.

## When to Use

- After any significant code change
- Before merging pull requests
- During code review requests
- To catch issues before human reviewers

## Review Checklist

### 🔴 Critical (Block Merge)
- [ ] Security vulnerabilities (SQL injection, XSS, auth bypass)
- [ ] Data corruption risks (race conditions, deadlocks)
- [ ] Authentication/authorization bypasses
- [ ] Secrets hardcoded in source

### 🟡 Important (Should Fix)
- [ ] Performance issues (N+1 queries, inefficient loops)
- [ ] Error handling missing or insufficient
- [ ] Missing input validation
- [ ] Resource leaks (unclosed connections, files)

### 🟢建议 (Nice to Fix)
- [ ] Code style violations
- [ ] Missing documentation
- [ ] Hardcoded values that should be config
- [ ] Overly complex logic

## Usage

```bash
# Review a file
openclaw code review --file src/auth.py

# Review a diff
openclaw code review --diff "main..feature-branch"

# Full repository audit
openclaw code review --repo ./ --exclude "node_modules,dist"
```

## Integration

### GitHub Actions
```yaml
- name: Code Review
  uses: openclaw/code-review-action@v1
  with:
    api-key: ${{ secrets.OPENCLAW_API_KEY }}
```

### Pre-commit Hook
```bash
openclaw code review --staged --fail-on critical
```

## Output Format

```json
{
  "file": "src/auth.py",
  "issues": [
    {
      "severity": "critical",
      "line": 42,
      "rule": "sql-injection",
      "message": "User input directly interpolated into SQL query",
      "fix": "Use parameterized queries instead"
    }
  ],
  "score": 72,
  "summary": "1 critical, 2 important, 3 suggestions"
}
```

## Best Practices

- Run on every commit, not just before merges
- Combine with human review for critical paths
- Track review history to catch recurring issues
- Customize rules per project type
