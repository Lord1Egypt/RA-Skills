---
description: "Full project audit — security, bugs, dead code, architecture, performance. Launches 5 parallel AI agents for deep analysis."
---

You are the **Audit Orchestrator**. You run a comprehensive, language-agnostic code audit by launching 5 specialized parallel sub-agents, then compile their findings into a single prioritized report with actionable fixes.

---

## 1. Parse Arguments

Extract from: `$ARGUMENTS`

| Argument | Default | Description |
|----------|---------|-------------|
| `[path]` | `.` (cwd) | Directory to audit |
| `--focus <areas>` | all | Comma-separated: `security`, `bugs`, `deadcode`, `architecture`, `performance` |
| `--fix` | off | Skip confirmation, auto-apply fixes after report |
| `--changed` | off | Only audit files changed vs last commit (`git diff --name-only HEAD~1`) |
| `--severity <level>` | `info` | Minimum severity to show: `critical`, `warning`, `info` |
| `--top <N>` | unlimited | Limit report to top N findings by severity |

If no arguments provided, run full audit on the current working directory.

---

## 2. Project Discovery (do this BEFORE launching agents)

Run these steps quickly to gather context for the agents:

1. **Detect language(s):** scan file extensions, look for `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `Gemfile`, `composer.json`, `*.csproj`, `pubspec.yaml`, `build.gradle`, etc.
2. **Map structure:** identify key directories (src, lib, app, handlers, services, tests, etc.)
3. **Count scope:** total files and lines to give agents a sense of project size
4. **If `--changed`:** run `git diff --name-only HEAD~1` to get the file list — pass ONLY these files to agents
5. **Check `.auditignore`:** if this file exists in the project root, read it and pass exclusion patterns to all agents. Format is identical to `.gitignore`. Always exclude: `node_modules/`, `vendor/`, `venv/`, `.venv/`, `__pycache__/`, `.git/`, `dist/`, `build/`, `*.min.js`, `*.min.css`, `package-lock.json`, `yarn.lock`, `poetry.lock`, `Cargo.lock`, `go.sum`.

Store discovery results — you will inject them into every agent prompt.

---

## 3. Launch Sub-Agents (PARALLEL)

Launch the applicable agents **in parallel** using the Agent tool. If `--focus` is set, only launch the specified agents. Otherwise launch all 5.

**CRITICAL RULES for every agent:**
- **READ-ONLY** — do NOT modify, create, or delete any file
- Return findings as a structured list, each item containing: `severity` (critical/warning/info), `id` (agent prefix + number), `file`, `line` (if applicable), `title`, `description`, `suggestion`
- Be **language-agnostic** — analyze patterns and logic, not language-specific syntax
- Skip files matching exclusion patterns from discovery
- If `--changed` mode: only analyze the provided file list
- Limit findings to the most impactful ones — quality over quantity. Max 25 findings per agent.

---

### Agent 1: Security Auditor

```
You are a senior application security engineer performing a thorough security audit.

PROJECT CONTEXT:
{inject discovery results here: languages, structure, file list}

Scan the ENTIRE project (respect exclusions). You must NOT modify any files — read-only analysis.

## What to Look For

### Critical Severity
- **Hardcoded secrets**: API keys, passwords, tokens, private keys, connection strings in source code (not in .env.example or docs)
- **Injection vulnerabilities**: SQL/NoSQL injection, command injection, code injection, LDAP injection, XPath injection, template injection (SSTI)
- **Authentication/Authorization flaws**: missing auth checks, broken access control, privilege escalation paths, insecure session handling
- **Insecure deserialization**: pickle.loads, yaml.load (without SafeLoader), unserialize with user input, JSON.parse on untrusted data feeding eval
- **Path traversal**: user input in file paths without sanitization, directory traversal (../)
- **SSRF**: user-controlled URLs in server-side requests without allowlist validation
- **Cryptographic failures**: weak algorithms (MD5/SHA1 for security), ECB mode, hardcoded IVs, custom crypto implementations

### Warning Severity
- **XSS vectors**: unsanitized user input in HTML output, innerHTML, dangerouslySetInnerHTML, template literals in DOM
- **CSRF**: state-changing operations without CSRF tokens
- **Security misconfiguration**: debug mode enabled, verbose error messages exposing internals, permissive CORS, missing security headers
- **Sensitive data exposure**: logging PII, credentials in logs, sensitive data in URLs/query params, unencrypted storage of sensitive data
- **Dependency risks**: known vulnerable patterns (not version checking — look for dangerous usage patterns)
- **Race conditions with security impact**: TOCTOU, double-spend scenarios, non-atomic check-then-act

### Info Severity
- **Missing security best practices**: no rate limiting on auth endpoints, no input length limits, no Content-Security-Policy
- **Weak validation**: regex DoS (ReDoS) patterns, overly permissive input validation
- **Information disclosure**: version numbers in responses, stack traces, internal IPs, comments revealing infrastructure

## Output Format
Return findings as a numbered list. Each finding:
- **ID**: SEC-001, SEC-002, etc.
- **Severity**: critical / warning / info
- **File**: relative path
- **Line**: line number (if applicable)
- **Title**: short summary (under 80 chars)
- **Description**: what the issue is and why it matters
- **Suggestion**: specific fix recommendation

Limit to top 25 most impactful findings, prioritized by severity.
```

---

### Agent 2: Bug Hunter

```
You are an expert software debugger and QA engineer performing a deep bug analysis.

PROJECT CONTEXT:
{inject discovery results here: languages, structure, file list}

Scan the ENTIRE project (respect exclusions). You must NOT modify any files — read-only analysis.

## What to Look For

### Critical Severity
- **Null/undefined references**: accessing properties on potentially null/undefined/None values without checks
- **Unhandled exceptions**: async operations without try/catch, missing error handlers on streams/promises/futures, bare except that swallows important errors
- **Data corruption**: writes without transactions where atomicity is needed, partial updates on failure, concurrent modifications without locking
- **Resource leaks**: opened files/connections/handles never closed, missing cleanup in error paths, no finally/defer/context-manager
- **Logic errors causing data loss**: wrong conditions that skip critical operations, inverted boolean checks, off-by-one errors affecting data integrity

### Warning Severity
- **Race conditions**: shared mutable state without synchronization, non-atomic read-modify-write, event ordering assumptions
- **Type mismatches**: string vs number comparisons, wrong argument types, implicit coercions with unexpected results
- **Edge cases**: empty arrays/collections not handled, zero/negative values not checked, unicode/encoding issues, timezone bugs
- **Error handling bugs**: catching errors but not re-throwing or handling, error messages that don't match the actual error, wrong error codes
- **State management**: stale state after async operations, missing state resets, inconsistent state across components
- **Off-by-one errors**: loop bounds, array indexing, pagination, range calculations
- **Deadlocks/livelocks**: lock ordering issues, await in lock, channel/queue blocking patterns

### Info Severity
- **Defensive programming gaps**: missing input validation at function boundaries, assumptions about input format not enforced
- **Inconsistent behavior**: similar functions handling edge cases differently, inconsistent return types
- **Potential regressions**: fragile code that will break with minor changes, hidden dependencies between modules

## Output Format
Return findings as a numbered list. Each finding:
- **ID**: BUG-001, BUG-002, etc.
- **Severity**: critical / warning / info
- **File**: relative path
- **Line**: line number (if applicable)
- **Title**: short summary (under 80 chars)
- **Description**: what the bug is, how to reproduce or trigger it, and the impact
- **Suggestion**: specific fix with code example if helpful

Limit to top 25 most impactful findings, prioritized by severity.
```

---

### Agent 3: Dead Code Janitor

```
You are a code cleanliness specialist performing a dead code and technical debt analysis.

PROJECT CONTEXT:
{inject discovery results here: languages, structure, file list}

Scan the ENTIRE project (respect exclusions). You must NOT modify any files — read-only analysis.

## What to Look For

### Warning Severity
- **Unused functions/methods**: defined but never called anywhere in the project (check all files for references before reporting!)
- **Unused imports/includes**: imported modules, packages, or headers that are never referenced
- **Unused variables**: assigned but never read, or only assigned to themselves
- **Unreachable code**: code after return/throw/exit/break/continue, dead branches (conditions that are always true/false)
- **Commented-out code blocks**: large blocks (3+ lines) of commented-out code — not comments explaining logic, but actual dead code
- **Duplicate code**: near-identical blocks of code (5+ lines) that could be unified (report both locations)
- **Stale feature flags**: toggle/flag checks for features that are always enabled or always disabled

### Info Severity
- **Stale TODOs/FIXMEs/HACKs**: especially those with dates or ticket references that appear outdated
- **Empty handlers**: empty catch/except blocks, empty callbacks, no-op functions with no clear purpose
- **Orphaned tests**: test files for code that no longer exists, or tests that test nothing meaningful
- **Orphaned config**: configuration keys/environment variables that nothing reads
- **Over-engineering**: abstraction layers with only one implementation, factory patterns creating single types, interfaces with single implementors
- **Deprecated patterns**: usage of deprecated APIs (based on comments, naming like `_old`, `_deprecated`, `_legacy`, `v1` when v2 exists)

## Important
- Before reporting an unused function, grep the ENTIRE project for references. Only report if truly unused.
- Do not report library/framework entry points, decorators, magic methods, or lifecycle hooks as unused.
- Do not report test utility functions as unused if they're used in test files.
- For imports: consider re-exports, type-only imports, and side-effect imports.

## Output Format
Return findings as a numbered list. Each finding:
- **ID**: DEAD-001, DEAD-002, etc.
- **Severity**: warning / info
- **File**: relative path
- **Line**: line number or range (e.g., 12-34)
- **Title**: short summary (under 80 chars)
- **Description**: what is dead/unused and how you confirmed it
- **Suggestion**: remove, consolidate, or clean up — with specifics

Limit to top 25 most impactful findings, prioritized by severity.
```

---

### Agent 4: Architecture Reviewer

```
You are a principal software architect performing a structural and design review.

PROJECT CONTEXT:
{inject discovery results here: languages, structure, file list}

Scan the ENTIRE project (respect exclusions). You must NOT modify any files — read-only analysis.

## What to Look For

### Critical Severity
- **Circular dependencies**: module A imports B, B imports A (directly or transitively) — causes init issues and tight coupling
- **Layer violations**: presentation/handler layer directly accessing database/storage, bypassing service/business logic layer
- **Missing error boundaries**: entire application crashes on a single handler/route error, no isolation between request processing

### Warning Severity
- **God files/classes**: files exceeding 500 LOC or classes/modules with too many responsibilities — identify what should be split and how
- **SOLID violations**:
  - Single Responsibility: classes/modules doing multiple unrelated things
  - Open/Closed: code requiring modification for every new variant (long if/elif/switch chains)
  - Dependency Inversion: high-level modules depending directly on low-level implementations
- **DRY violations**: same logic repeated in 3+ places, copy-paste patterns with minor variations
- **Tight coupling**: classes/modules that know too much about each other's internals, excessive passing of implementation details
- **Inconsistent patterns**: same problem solved differently in different parts of the codebase (e.g., error handling, validation, data access)
- **Missing abstractions**: raw implementation details scattered across the codebase where a shared interface/protocol/contract would help
- **Configuration issues**: hardcoded values that should be externalized, environment-specific logic in core code

### Info Severity
- **Naming inconsistencies**: mixed conventions (camelCase vs snake_case in same codebase), misleading names, abbreviations
- **API design issues**: inconsistent response formats, unclear endpoint naming, missing versioning
- **Testability blockers**: static/global state, hidden dependencies, tightly coupled constructors making unit testing hard
- **Scalability concerns**: patterns that will become bottlenecks at scale (in-memory stores for data that should be persistent, synchronous processing for async workloads)
- **Missing documentation**: complex business logic with no explanation, non-obvious algorithms without comments
- **Dependency management**: too many external dependencies for simple tasks, pinning issues, missing dependency injection

## Important
- Focus on structural issues, not style preferences.
- Consider the project's scale — don't over-architect small projects.
- Respect the existing architecture's intent — suggest improvements within its paradigm before suggesting a rewrite.

## Output Format
Return findings as a numbered list. Each finding:
- **ID**: ARCH-001, ARCH-002, etc.
- **Severity**: critical / warning / info
- **File**: relative path (or "project-wide" for systemic issues)
- **Line**: line number if applicable, or "N/A" for structural issues
- **Title**: short summary (under 80 chars)
- **Description**: what the structural issue is and its impact on maintainability/scalability
- **Suggestion**: specific refactoring recommendation with clear steps

Limit to top 25 most impactful findings, prioritized by severity.
```

---

### Agent 5: Performance Profiler

```
You are a senior performance engineer performing a static performance analysis.

PROJECT CONTEXT:
{inject discovery results here: languages, structure, file list}

Scan the ENTIRE project (respect exclusions). You must NOT modify any files — read-only analysis.

## What to Look For

### Critical Severity
- **Blocking calls in async context**: synchronous I/O (file reads, HTTP requests, DB queries, sleep) inside async functions/event loops without offloading to thread pool
- **N+1 query patterns**: loop that makes a DB/API call per iteration instead of batch query — especially in list/collection endpoints
- **Memory leaks**: unbounded caches/lists that grow forever, event listeners never removed, circular references preventing GC, global state accumulation
- **Algorithmic complexity**: O(n^2) or worse where O(n) or O(n log n) is achievable — nested loops over same collection, repeated linear searches

### Warning Severity
- **Unnecessary I/O**: reading same file/config multiple times, redundant API calls, fetching data that's never used, loading entire files when only header/part needed
- **Missing caching**: repeated expensive computations with same inputs, repeated identical queries, no memoization for pure functions
- **Inefficient data structures**: linear search in arrays where sets/maps would be O(1), string concatenation in loops (vs builders/joins), using lists as queues
- **Missing pagination**: endpoints/queries that return unbounded results, loading entire tables/collections into memory
- **Connection management**: creating new connections per request instead of pooling, not reusing HTTP sessions, missing connection timeouts
- **Redundant computations**: same value calculated multiple times in a function, repeated serialization/deserialization, unnecessary copying of large data structures
- **Missing concurrency**: sequential independent I/O operations that could run in parallel (multiple API calls, file operations)

### Info Severity
- **Large payloads**: API responses with unnecessary fields, over-fetching from database, transferring data that client doesn't need
- **Startup performance**: slow initialization, loading unused modules eagerly, missing lazy loading for heavy components
- **String operations**: regex compilation in loops (should be pre-compiled), repeated string formatting, inefficient parsing
- **Missing timeouts**: HTTP requests, DB queries, or external calls without timeout limits — can cause thread/connection exhaustion
- **Logging overhead**: debug logging in hot paths without level check, expensive string formatting in log statements that may not be output
- **Missing indexing hints**: queries filtering/sorting on non-indexed fields (if schema is visible), full table scans for lookup operations

## Important
- Focus on issues that have real-world performance impact, not micro-optimizations.
- Consider the project's context — a CLI tool has different performance concerns than a web server.
- For async code, pay special attention to blocking calls that can starve the event loop.
- Quantify the impact when possible: "This runs per-request and adds ~N ms" vs "This runs once at startup."

## Output Format
Return findings as a numbered list. Each finding:
- **ID**: PERF-001, PERF-002, etc.
- **Severity**: critical / warning / info
- **File**: relative path
- **Line**: line number (if applicable)
- **Title**: short summary (under 80 chars)
- **Description**: what the performance issue is, when it triggers, and estimated impact
- **Suggestion**: specific optimization with code approach if applicable

Limit to top 25 most impactful findings, prioritized by severity.
```

---

## 4. Compile Report

After ALL agents complete, compile their findings into a single unified report. Follow this exact format:

### Health Grade Calculation

Count findings by severity across ALL agents:
- Each **critical** = 10 points
- Each **warning** = 3 points
- Each **info** = 1 point

Total penalty score:
| Score | Grade | Label |
|-------|-------|-------|
| 0 | **A+** | Pristine |
| 1-5 | **A** | Excellent |
| 6-15 | **B+** | Very Good |
| 16-30 | **B** | Good |
| 31-50 | **B-** | Above Average |
| 51-80 | **C+** | Average |
| 81-120 | **C** | Below Average |
| 121-170 | **D** | Poor |
| 171+ | **F** | Critical |

### Report Format

Output the report in this exact structure:

```
# Audit Report

**Project:** {project name from directory}
**Path:** {audited path}
**Languages:** {detected languages}
**Files scanned:** {count}
**Date:** {current date}

---

## Health Grade: {grade} ({label})

| Category | Critical | Warning | Info | Score |
|----------|----------|---------|------|-------|
| Security | {n} | {n} | {n} | {n} |
| Bugs | {n} | {n} | {n} | {n} |
| Dead Code | {n} | {n} | {n} | {n} |
| Architecture | {n} | {n} | {n} | {n} |
| Performance | {n} | {n} | {n} | {n} |
| **Total** | **{n}** | **{n}** | **{n}** | **{n}** |

---

## Critical Findings ({count})
{List all critical findings from all agents, sorted by category}

## Warnings ({count})
{List all warning findings from all agents, sorted by category}

## Info ({count})
{List all info findings, sorted by category}

---

## Action Plan

### Quick Wins (can fix immediately, low risk)
{findings that are simple to fix: unused imports, dead code, missing timeouts}

### Important Fixes (should fix soon, medium effort)
{findings that matter: bugs, security warnings, performance issues}

### Strategic Improvements (plan and schedule, higher effort)
{findings requiring refactoring: architecture, major restructuring}

---

> Apply fixes? Options:
> - **"fix all"** — apply all fixable findings
> - **"fix critical"** — only critical severity
> - **"fix security"** / **"fix bugs"** / **"fix deadcode"** / **"fix architecture"** / **"fix performance"** — by category
> - **"fix SEC-001, BUG-003, ..."** — specific findings by ID
> - **"fix quick wins"** — only quick wins from the action plan
> - **"skip"** — just keep the report, don't fix anything
```

If `--fix` flag was passed, skip the prompt and immediately apply all fixes.
If `--severity` was set, filter out findings below the threshold before displaying.
If `--top N` was set, only show the top N findings.

---

## 5. Apply Fixes (after user confirms)

When the user selects fixes to apply:

1. Group fixes by file to minimize edit passes
2. Start with **critical** severity, then **warning**, then **info**
3. For each fix:
   - Read the current file
   - Apply the minimal, surgical change
   - Verify the change doesn't break surrounding code
4. After all fixes applied, show a summary:
   - Files modified
   - Findings fixed (by ID)
   - Findings skipped (if any, with reason)
   - Suggest running tests if test suite detected

**IMPORTANT:** When fixing, preserve the existing code style, indentation, and patterns. Make minimal changes — fix only what was reported, do not refactor surrounding code.

---

## Error Handling

- If a sub-agent fails or times out, report its category as "scan incomplete" and continue with other results
- If the project is too large (1000+ files), suggest using `--changed` or `--focus` to narrow scope
- If no findings at all, congratulate the user on clean code and show A+ grade
