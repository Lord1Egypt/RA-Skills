---
name: code-review-assistant
description: AI-powered code review assistant that analyzes pull requests for bugs, security issues, performance problems, and style violations with actionable feedback.
metadata:
  tags: ["code-review", "pull-request", "quality", "security", "development"]
---

# Code Review Assistant

Perform thorough AI-powered code reviews on pull requests or local changes. Analyzes diffs for bugs, security vulnerabilities, performance issues, maintainability concerns, and style violations. Provides actionable, specific feedback — not generic advice.

## Usage

```
"Review the current PR"
"Review the changes on this branch vs main"
"Review these specific files for security issues"
"Do a deep review of the authentication changes"
```

## How It Works

### 1. Gather Changes

Collect the diff and context:

```bash
# PR review
gh pr diff <number> --color=never

# Branch review
git diff main...HEAD

# Staged changes
git diff --cached
```

Also gather:
- File history (recently changed = higher risk)
- Test coverage for changed files
- Related open issues or previous reviews

### 2. Multi-Pass Analysis

Each pass focuses on a different concern:

**Pass 1 — Correctness:**
- Logic errors (off-by-one, null handling, race conditions)
- Edge cases not covered (empty input, boundary values, overflow)
- Error handling gaps (uncaught exceptions, missing error propagation)
- State management issues (stale closures, mutation of shared state)
- Concurrency bugs (deadlocks, data races, missing synchronization)

**Pass 2 — Security:**
- Injection vulnerabilities (SQL, command, XSS, template)
- Authentication/authorization gaps
- Sensitive data exposure (logs, errors, responses)
- Insecure cryptography or random number generation
- Missing input validation at trust boundaries
- Hardcoded secrets or credentials

**Pass 3 — Performance:**
- N+1 query patterns
- Missing or incorrect caching
- Unnecessary allocations in hot paths
- Blocking operations in async contexts
- Missing pagination or unbounded queries
- Inefficient algorithms (quadratic loops on large data)

**Pass 4 — Maintainability:**
- Complex functions that should be split (cyclomatic complexity >10)
- Missing or misleading names
- Dead code or unreachable branches
- Duplicated logic that should be extracted
- Missing types or overly broad types (any, Object)
- Tight coupling between modules

**Pass 5 — Testing:**
- Changed logic without corresponding test changes
- Test quality (testing implementation vs behavior)
- Missing edge case tests
- Flaky test patterns (timing, ordering, external deps)
- Adequate error path coverage

### 3. Severity Classification

Each finding gets a severity:

- 🔴 **Must Fix**: Bug, security issue, data loss risk, crash
- 🟡 **Should Fix**: Performance issue, maintainability concern, missing test
- 🟢 **Consider**: Style improvement, minor optimization, suggestion
- 💡 **Nitpick**: Optional improvement, personal preference

### 4. Actionable Feedback

Every comment includes:
- **What**: The specific issue found
- **Where**: Exact file and line number
- **Why**: Why this is a problem (not just "this is bad")
- **How**: Concrete fix suggestion with code

### 5. Summary

Overall assessment with:
- Risk level (safe to merge / needs changes / needs redesign)
- Top 3 most important findings
- Positive observations (good patterns, improvements)
- Suggested follow-up items (not blocking merge)

## Output

```
## Code Review Summary

**Risk Level:** 🟡 Needs Changes (2 must-fix, 4 should-fix)
**Files Reviewed:** 12 files, +342/-89 lines

### 🔴 Must Fix

1. **SQL Injection in user search** — `src/api/users.ts:47`
   The search query interpolates user input directly:
   ```typescript
   // Current (vulnerable)
   db.query(`SELECT * FROM users WHERE name LIKE '%${query}%'`)
   // Fix: use parameterized query
   db.query('SELECT * FROM users WHERE name LIKE $1', [`%${query}%`])
   ```

2. **Race condition in balance update** — `src/services/wallet.ts:112-118`
   Read-then-write without transaction. Two concurrent requests
   can both read the same balance and overwrite each other.
   Fix: wrap in a database transaction with SELECT FOR UPDATE.

### 🟡 Should Fix

3. **N+1 query in order listing** — `src/api/orders.ts:23`
   Each order triggers a separate query for user details.
   Use a JOIN or batch load users by ID.

4. **Missing error handling** — `src/services/payment.ts:67`
   API call result is not checked for errors before accessing `.data`.

[...]

### 👍 Good Stuff
- Clean separation of concerns in the new service layer
- Comprehensive input validation on the registration endpoint
- Good use of TypeScript discriminated unions for payment status

### 📋 Follow-up (non-blocking)
- Consider adding request rate limiting to the search endpoint
- The `formatDate` utility is duplicated in 3 files — extract to shared utils
```

## Configuration

The review depth adapts to PR size:
- **Small** (<100 lines): Full deep review, every line examined
- **Medium** (100-500 lines): Focused review on high-risk areas
- **Large** (500+ lines): Architectural review + spot-check critical paths, suggest splitting PR

## Integration

Works with:
- GitHub PRs (via `gh` CLI)
- GitLab MRs (via `glab` CLI)
- Local git branches (via `git diff`)
- Patch files (via `git apply --stat`)
