# Severity Classification

## Classification Framework

Every code review comment should be classified by severity. This helps authors prioritize fixes and reviewers focus on what matters.

## Severity Levels

### 🔴 Critical

**Definition:** Must fix before merge. Will cause production issues.

**Examples:**
- Security vulnerability (SQL injection, auth bypass, XSS)
- Data loss potential
- Race condition or deadlock
- Breaking production failure
- PII/sensitive data exposure
- Memory safety issue (buffer overflow in C, etc.)

**Author Response:** Fix immediately or blocking merge

### 🟡 Important

**Definition:** Should fix before merge. Technical debt or risk.

**Examples:**
- Missing error handling
- Unhandled edge case
- Performance issue (N+1, missing index)
- Inadequate test coverage
- Inconsistent API design
- Code that violates project conventions
- Missing logging/monitoring
- Hardcoded configuration values

**Author Response:** Fix or provide justification for deferral

### 🟢 Nit

**Definition:** Consider fixing. Polish/improvement.

**Examples:**
- Naming could be clearer
- Commented-out code
- Minor formatting issue
- Overly complex one-liner
- Could use a helper function
- Missing JSDoc/type comment
- Unused variable

**Author Response:** Fix if easy, otherwise ignore

## Severity Examples by Language

### Go

| Issue | Severity |
|-------|----------|
| `db.Query("SELECT * FROM users WHERE id=" + id)` | 🔴 Critical |
| Missing `defer rows.Close()` | 🔴 Critical |
| Goroutine leak | 🔴 Critical |
| No error check on external call | 🟡 Important |
| Magic numbers without constants | 🟢 Nit |

### TypeScript

| Issue | Severity |
|-------|----------|
| `eval(userInput)` | 🔴 Critical |
| `any` type without documentation | 🟡 Important |
| Missing input validation | 🟡 Important |
| Unused import | 🟢 Nit |
| Inconsistent naming (`userId` vs `user_id`) | 🟢 Nit |

## Triage Decision Tree

```
Is it a security vulnerability?
├── Yes → 🔴 Critical
└── No ↓
Does it cause data loss or corruption?
├── Yes → 🔴 Critical
└── No ↓
Does it crash or break production?
├── Yes → 🔴 Critical
└── No ↓
Does it need significant rework later?
├── Yes → 🟡 Important
└── No ↓
Is it a polish/clarity issue?
├── Yes → 🟢 Nit
└── → 🟢 Nit
```

## Response Time Expectations

| Severity | Author Response Time |
|----------|-------------------|
| 🔴 Critical | Within 1 hour / same day |
| 🟡 Important | Within 1 day |
| 🟢 Nit | Before merge (or ignore) |

## Comment Formatting

```markdown
[🔴 CRITICAL] SQL injection vulnerability
The `name` parameter is concatenated directly into the query.
Use parameterized queries instead: `db.Query("SELECT * FROM users WHERE name=$1", name)`

[🟡 IMPORTANT] Missing error handling
The HTTP client call on line 42 doesn't check for errors.
Add: `if err != nil { return nil, fmt.Errorf("HTTP call failed: %w", err) }`

[🟢 NIT] Unused variable
`result` on line 15 is assigned but never used. Remove or use it.
```
