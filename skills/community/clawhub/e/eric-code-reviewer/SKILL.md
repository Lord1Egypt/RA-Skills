---
name: code-reviewer
description: "Automated code review for pull requests and code snippets. Analyzes code quality, security vulnerabilities, performance issues, and best practices across Python, JavaScript/TypeScript, Java, Go, Rust, and Shell scripts. Use when the user wants to: (1) Review a PR before merging, (2) Check a code snippet for bugs or anti-patterns, (3) Get security audit of code changes, (4) Improve code quality with actionable suggestions, (5) Ensure consistency with project style guides. Best for developers, teams wanting automated pre-merge reviews, and anyone who wants a second pair of eyes on their code."
version: 1.0.0
homepage: https://clawhub.ai
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins:
        - git
---

# Code Reviewer

Automated code review analysis for quality, security, performance, and best practices.

## When to Use

✅ **USE this skill when:**

- "Review this code for bugs"
- "Check my PR before I submit it"
- "Is there any security issue in this function?"
- "Can you optimize this code?"
- "Review this git diff"
- "Does this follow [language] best practices?"
- "Compare these two implementations"

❌ **DON'T use this skill when:**

- Need full test suite generation → use a testing skill
- Need architectural design review → use architecture skills
- Need deployment pipeline review → use CI/CD skills
- The code is proprietary/sensitive and shouldn't be shared

## Review Checklist

For every code review, the agent checks **in this order**:

### 1. 🔴 Critical (must fix)

| Check | What to look for |
|-------|-----------------|
| **SQL Injection** | String concatenation in queries, unescaped user input |
| **XSS** | Unsanitized output in HTML/templates, `dangerouslySetInnerHTML` |
| **Command Injection** | `os.system()`, `exec()`, `subprocess(shell=True)` with user input |
| **Path Traversal** | `../../` in file paths, unsanitized filenames |
| **Sensitive Data** | Hardcoded API keys, passwords, tokens, secrets |
| **Unvalidated Input** | Missing type checks, no boundary validation on arrays/buffers |

### 2. 🟡 Important (should fix)

| Check | What to look for |
|-------|-----------------|
| **Null/Undefined** | Missing null checks, no Optional/Maybe wrapping |
| **Error Handling** | Bare `except:`, swallowed exceptions, no error context |
| **Race Conditions** | Shared state without locks, async without mutexes |
| **Resource Leaks** | Unclosed files, connections, handles |
| **Type Safety** | Implicit casts, `any` types, missing generics |
| **Dead Code** | Unused variables, imports, unreachable branches |

### 3. 🟢 Nice to have

| Check | What to look for |
|-------|-----------------|
| **Naming** | Vague names (`data`, `tmp`, `foo`), inconsistent casing |
| **Comments** | Stale/no comments, commented-out code |
| **Duplication** | Repeated logic that should be a function |
| **Logging** | Missing context in log messages, wrong log level |
| **Tests** | Missing edge cases, no test for the change |

## Workflow

### Step 1: Accept Input

The agent accepts code in these forms:

- **Pasted code block**: "Review this function: \`\`\`python ..."
- **File path**: "Review src/app.js"
- **Git diff**: "Review my uncommitted changes" → runs `git diff`
- **GitHub PR URL**: "Review https://github.com/user/repo/pull/42"
- **Branch comparison**: "Review changes between main and feature-branch"

### Step 2: Analyze

For each code segment:

1. Identify the language and framework
2. Run the checklist above
3. Cross-reference common anti-patterns for the language
4. Check for performance traps (N+1 queries, O(n²) in loops, etc.)

### Step 3: Report

Present findings in order of severity with:

```
## 🔴 Critical
- [Line 42] SQL Injection: f-string used in SQL query. Use parameterized queries.

## 🟡 Important
- [Line 15] Missing null check: `user.getName()` may throw if user is None

## 🟢 Suggestion
- [Line 88] Duplicate logic with lines 12-20 — extract to helper function
```

### Step 4: Offer Fixes (Optional)

The agent can:
- Show the fix inline
- Generate a patch file
- Apply changes directly (with confirmation)

## Language-Specific Rules

### Python
- Prefer f-strings over `.format()` or `%`
- Use `with` for resource management
- Type hints on function signatures
- List comprehensions over `map`/`filter`
- Avoid mutable default arguments

### JavaScript / TypeScript
- `const` over `let`, never `var`
- Prefer early returns over nested ifs
- Use `===` not `==`
- Async/await over raw promises
- Avoid `any` in TypeScript

### Java
- Use `Optional` over null returns
- Prefer try-with-resources
- Favor composition over inheritance
- Use interface types, not concrete types

### Go
- Always check errors
- Use `go fmt` conventions
- Prefer `defer` for cleanup
- Avoid global state

### Shell / Bash
- Quote all variable expansions
- Use `set -euo pipefail` in scripts
- Prefer `[[ ]]` over `[ ]`
- Avoid parsing `ls` output

## Examples

> **User**: "Review this Python function" + code block
> **Agent**: Runs checklist → finds SQL injection. Reports 🔴 Critical with fix
>
> **User**: "Check my current git diff"
> **Agent**: Runs `git diff`, reviews changes, lists findings
>
> **User**: "Is this TypeScript safe?" + code block
> **Agent**: Checks types, null safety, anti-patterns → 🟡 reports `any` misuse

## Notes

- For large PRs, focus on changed lines only
- Flag false positives transparently
- If a file is too large, review the most critical areas first
