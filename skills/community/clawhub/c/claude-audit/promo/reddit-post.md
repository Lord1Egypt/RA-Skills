# Title:
I built /audit — one command, 5 parallel AI agents scan your entire codebase (security, bugs, dead code, architecture, performance)

# Body:

I kept running separate linters, security scanners, and profilers, then manually cross-referencing results. Got tired of it, so I built a Claude Code skill that does everything at once.

## What it does

Type `/audit` in Claude Code. Five agents launch in parallel:

| Agent | What it checks |
|---|---|
| Security Auditor | Hardcoded secrets, injections, auth gaps, SSRF, XSS, crypto issues |
| Bug Hunter | Null refs, race conditions, resource leaks, unhandled errors, logic flaws |
| Dead Code Janitor | Unused imports/functions, commented-out code, stale TODOs, duplicates |
| Architecture Reviewer | Circular deps, SOLID/DRY violations, god classes, layer violations |
| Performance Profiler | N+1 queries, blocking async calls, memory leaks, missing caching |

Everything runs **read-only** - nothing is touched until you say so.

## Sample output

```
Audit Report
Health Grade: B- (Above Average)

| Category     | Critical | Warning | Info | Score |
|--------------|----------|---------|------|-------|
| Security     | 1        | 3       | 2    | 21    |
| Bugs         | 2        | 1       | 0    | 23    |
| Dead Code    | 0        | 4       | 6    | 18    |
| Architecture | 0        | 2       | 3    | 9     |
| Performance  | 1        | 0       | 1    | 11    |
| Total        | 4        | 10      | 12   | 82    |
```

After the report, pick what to fix:
- `fix all` / `fix critical` / `fix security` / `fix BUG-003, SEC-001`

## Flags

- `--focus security,bugs` - run only the agents you need
- `--fix` - auto-fix without asking
- `--changed` - only scan files changed since last commit (great before PRs)
- `--severity critical` - filter noise
- `--top 10` - top N issues only

Works with **any language** - Python, JS/TS, Go, Rust, Java, C#, etc.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/atobones/claude-audit/main/install.sh | bash
```

Or manually copy one file to `~/.claude/commands/audit.md`.

**GitHub:** https://github.com/atobones/claude-audit

---

Built this for my own projects, figured others might find it useful. It's v1.0 - planning to add more checks and a CI mode. Issues and PRs welcome.
