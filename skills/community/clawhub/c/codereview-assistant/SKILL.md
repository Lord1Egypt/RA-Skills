---
name: code-review
description: >
  Code review best practices and workflow skill.
  Use when: reviewing pull requests, performing peer code review, setting up code review standards,
  or improving code quality processes.
  Triggers: code review, PR review, pull request review, peer review, code quality,
  review standards, lint, static analysis.
  Provides: review checklist templates, focus areas by language/framework,
  review comment guidelines, approval criteria, and severity classification.
---

# Code Review Skill

A structured approach to code review that balances thoroughness with efficiency.

## Core Principles

1. **Review the code, not the author** — Assume good intent, focus on the work.
2. **Be specific and constructive** — Every comment should have a clear action.
3. **Prioritize by severity** — Not all issues are equal.
4. **Approve with confidence** — Don't approve code you wouldn't want to maintain.

## Review Focus Areas

### 🔴 Critical — Must Fix Before Merge
- Security vulnerabilities (SQL injection, auth bypass, secrets in code)
- Data loss risks (missing validations, unguarded deletions)
- Race conditions and concurrency bugs
- Breaking production failures

### 🟡 Important — Should Fix Before Merge
- Error handling gaps
- Performance issues (N+1 queries, missing indexes, memory leaks)
- Missing test coverage for critical paths
- Inconsistent error responses
- Code that violates team conventions

### 🟢 Nit — Consider Fixing
- Naming that could be clearer
- Commented-out code
- Minor formatting inconsistencies
- Overly complex one-liners

## Review Workflow

### Step 1: Understand the Context
1. Read the PR description and linked issues/tickets
2. Check what the PR is trying to accomplish
3. Understand the scope of changes

### Step 2: Scan First Pass
Quick scan for:
- Obvious bugs or logic errors
- Security concerns
- Missing tests
- Breaking changes

### Step 3: Deep Review
For each changed file:
1. Read the diff carefully
2. Cross-reference with design documents
3. Check for side effects on existing functionality
4. Verify test coverage

### Step 4: Classify and Comment
For each issue found, classify:
```
[🔴 CRITICAL] <title>
Description of the issue.
Suggested fix: <action>
```

```
[🟡 IMPORTANT] <title>
Description of the issue.
Suggested fix: <action>
```

```
[🟢 NIT] <title>
Optional suggestion.
```

### Step 5: Make a Decision

| Condition | Decision |
|-----------|----------|
| No critical issues, minor nits | ✅ **Approve** |
| Important issues need fixing | 🔄 **Request Changes** |
| Critical issues found | ❌ **Request Changes** (block merge) |
| Need context/clarification | 💬 **Comment** (don't approve yet) |

## PR Description Checklist

A good PR description should have:

- [ ] **What** — Brief summary of the change
- [ ] **Why** — Business or technical motivation
- [ ] **How** — High-level approach taken
- [ ] **Testing** — How the change was tested
- [ ] **Screenshots** — UI changes (before/after)
- [ ] **Breaking Changes** — Any API or contract changes
- [ ] **Related Issues** — Links to tickets

## Review Comment Templates

### Starting a Review
```
I've reviewed this PR. Here's my feedback:

**Looking at:** [files/modules]
**Tested locally:** [yes/no with details]
```

### Approving
```
✅ **Approve** — Code looks good, ready to merge.
Minor suggestions (non-blocking):
- [nit 1]
- [nit 2]
```

### Requesting Changes
```
🔄 **Request Changes** — Please address the following before merging:

**Critical:**
1. [issue] — [fix suggestion]

**Important:**
2. [issue] — [fix suggestion]
```

### Blocking Merge
```
❌ **Blocking Merge** — This PR introduces a critical issue that must be resolved:

[Detailed description of the critical issue]
```

## Per-Language/Framework Notes

### Go
- Check `error` handling on every function call
- Verify `context.Context` propagation
- Look for `defer` resource cleanup
- Check goroutine leaks (use `go vet`)
- Review SQL query construction (avoid string concatenation)

### TypeScript/Node.js
- Check async/await error handling
- Verify input validation on API handlers
- Look for memory leak patterns (event listeners not removed)
- Check dependency injection patterns
- Review `any` type usage

### Python
- Check exception handling
- Verify database connection cleanup
- Look for proper `with` statement usage
- Review decorator usage for side effects
- Check type hints completeness

### Java/Kotlin
- Check exception handling and logging
- Verify resource cleanup (try-with-resources)
- Review Spring annotations usage
- Look for thread safety issues
- Check transaction boundaries

## Automation Complement

Code review augments (not replaces) automated tools:
- **Linters** — Formatting, style conventions
- **Type checkers** — Type safety
- **SAST scanners** — Security vulnerability detection
- **Coverage tools** — Test coverage metrics

Always verify what the automation missed.

## File Structure

```
code-review/
├── SKILL.md
└── references/
    ├── review-checklist.md
    ├── comment-templates.md
    ├── severity-classification.md
    └── per-language-notes/
        ├── go.md
        ├── typescript.md
        ├── python.md
        └── java.md
```
