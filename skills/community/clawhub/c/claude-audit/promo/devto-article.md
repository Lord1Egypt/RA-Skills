---
title: "I Built a Claude Code Skill That Launches 5 AI Agents to Audit Your Entire Codebase"
published: false
description: "/audit — one command for security, bugs, dead code, architecture, and performance analysis. Language-agnostic. Zero config."
tags: claudecode, ai, devtools, opensource
cover_image:
---

## The Problem

Every mature project accumulates issues across multiple dimensions: security vulnerabilities, subtle bugs, dead code, architectural drift, and performance bottlenecks.

The typical approach? Run ESLint, then Bandit, then a separate security scanner, then manually review architecture, then profile performance. Each tool has its own config, output format, and learning curve. Cross-referencing results is painful.

I wanted one command that covers everything.

## The Solution: `/audit`

`claude-audit` is a Claude Code skill that launches **5 specialized AI agents in parallel** to scan your entire codebase. Each agent focuses on one domain, scans read-only, and reports back. A main orchestrator compiles everything into a single prioritized report.

```bash
/audit
```

That's it. No config files, no setup, no dependencies.

## How It Works

When you run `/audit`, here's what happens:

### 1. Project Discovery
The orchestrator auto-detects your language(s), maps your project structure, and counts the scope - all before any agent starts scanning.

### 2. Five Agents Launch in Parallel

| Agent | Role | What It Finds |
|---|---|---|
| **Security Auditor** | AppSec engineer | Hardcoded secrets, SQL/command injection, auth flaws, SSRF, XSS, weak crypto |
| **Bug Hunter** | QA engineer | Null refs, race conditions, resource leaks, logic errors, edge cases |
| **Dead Code Janitor** | Cleanup specialist | Unused imports/functions, commented code, stale TODOs, duplicates |
| **Architecture Reviewer** | Principal architect | SOLID/DRY violations, circular deps, god classes, coupling issues |
| **Performance Profiler** | Performance engineer | N+1 queries, blocking async calls, memory leaks, O(n^2), missing caching |

All agents are **read-only** — nothing is modified during the scan.

### 3. Unified Report

The orchestrator compiles findings into a single report with a **Health Grade** from A+ to F:

```
Audit Report

Project: my-api
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

Each finding has a unique ID (`SEC-001`, `BUG-003`), severity, file location, description, and a specific fix suggestion.

### 4. Action Plan

Findings are grouped into:
- **Quick Wins** — fix in minutes (dead imports, stale TODOs)
- **Important Fixes** — fix soon (bugs, security warnings)
- **Strategic Improvements** — plan and schedule (architecture refactors)

### 5. Surgical Fixes

After reviewing the report, you choose what to fix:

```
fix all                    # Everything
fix critical               # Only critical severity
fix security               # Only security findings
fix SEC-001, BUG-003       # Specific findings by ID
fix quick wins             # Low-risk quick wins
skip                       # Just keep the report
```

## Usage Examples

### Full audit
```bash
/audit
```

### Pre-PR security check
```bash
/audit --focus security --changed
```

### Quick cleanup before release
```bash
/audit --focus deadcode --fix
```

### Architecture review
```bash
/audit --focus architecture --severity warning
```

### Top 5 most critical issues
```bash
/audit --top 5 --severity critical
```

## Language-Agnostic

`/audit` works with **any language** Claude Code supports:

Python, JavaScript, TypeScript, Go, Rust, Java, C#, C/C++, Ruby, PHP, Swift, Kotlin, Dart, and more.

It analyzes patterns and logic, not syntax. The same command works whether you're auditing a Django backend, a React frontend, or a Rust CLI tool.

## Installation

One line:

```bash
curl -fsSL https://raw.githubusercontent.com/atobones/claude-audit/main/install.sh | bash
```

Or manually:

```bash
# Global (all projects)
mkdir -p ~/.claude/commands
curl -fsSL https://raw.githubusercontent.com/atobones/claude-audit/main/audit.md \
  -o ~/.claude/commands/audit.md

# Project-level (this repo only)
mkdir -p .claude/commands
curl -fsSL https://raw.githubusercontent.com/atobones/claude-audit/main/audit.md \
  -o .claude/commands/audit.md
```

Open Claude Code and run `/audit`.

## Customization

Create a `.auditignore` file (same syntax as `.gitignore`) to skip paths:

```gitignore
generated/
third_party/
tests/fixtures/
```

Common paths like `node_modules/`, `vendor/`, `dist/`, and lock files are excluded by default.

## What's Next

This is v1.0. On the roadmap:

- Trend tracking (compare health grades over time)
- Baseline mode (only report new findings)
- More granular agent configs
- Community-contributed check patterns

## Try It

- **GitHub:** [github.com/atobones/claude-audit](https://github.com/atobones/claude-audit)
- **Install:** `curl -fsSL https://raw.githubusercontent.com/atobones/claude-audit/main/install.sh | bash`

Star the repo if you find it useful. Issues and PRs welcome — especially ideas for new checks or agent improvements.
