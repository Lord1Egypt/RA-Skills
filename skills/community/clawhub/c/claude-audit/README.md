# /audit

**Full-spectrum project audit for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). 5 parallel AI agents. Zero config. Any language.**

One command scans your entire codebase for security vulnerabilities, bugs, dead code, architecture issues, and performance problems — then offers to fix them.

```
/audit
```

```
# Audit Report

Project: my-app
Health Grade: B- (Above Average)

| Category     | Critical | Warning | Info | Score |
|--------------|----------|---------|------|-------|
| Security     | 1        | 3       | 2    | 21    |
| Bugs         | 2        | 1       | 0    | 23    |
| Dead Code    | 0        | 4       | 6    | 18    |
| Architecture | 0        | 2       | 3    | 9     |
| Performance  | 1        | 0       | 1    | 11    |
| Total        | 4        | 10      | 12   | 82    |

> Apply fixes? [fix all / fix critical / fix security / skip]
```

---

## How It Works

`/audit` launches **5 specialized AI agents** that run in parallel:

| Agent | Role | Looks For |
|-------|------|-----------|
| **Security Auditor** | AppSec engineer | Hardcoded secrets, injections, auth flaws, SSRF, XSS, crypto issues |
| **Bug Hunter** | QA engineer | Null refs, race conditions, resource leaks, logic errors, edge cases |
| **Dead Code Janitor** | Cleanup specialist | Unused imports/functions/variables, commented-out code, stale TODOs, duplicates |
| **Architecture Reviewer** | Principal architect | SOLID/DRY violations, circular deps, god classes, coupling, layer violations |
| **Performance Profiler** | Performance engineer | N+1 queries, blocking async calls, memory leaks, missing caching, O(n^2) algorithms |

All agents scan read-only. Nothing is modified until you explicitly approve fixes.

---

## Installation

### One-line install

```bash
curl -fsSL https://raw.githubusercontent.com/atobones/claude-audit/main/install.sh | bash
```

The installer will ask whether to install globally (all projects) or locally (current project only).

### Manual install

Copy `audit.md` to your Claude Code commands directory:

**Global** (available in all projects):
```bash
mkdir -p ~/.claude/commands
curl -fsSL https://raw.githubusercontent.com/atobones/claude-audit/main/audit.md -o ~/.claude/commands/audit.md
```

**Project-level** (available in this repo only):
```bash
mkdir -p .claude/commands
curl -fsSL https://raw.githubusercontent.com/atobones/claude-audit/main/audit.md -o .claude/commands/audit.md
```

### Verify

Open Claude Code in your terminal and type:
```
/audit
```

---

## Usage

### Full audit (default)
```
/audit
```
Scans the entire project with all 5 agents.

### Audit specific directory
```
/audit src/
```

### Focus on specific areas
```
/audit --focus security,bugs
/audit --focus performance
/audit --focus deadcode,architecture
```

### Audit only changed files (fast)
```
/audit --changed
```
Only scans files modified since the last commit. Great for pre-PR checks.

### Auto-fix mode
```
/audit --fix
```
Skips the confirmation prompt and immediately applies all fixes.

### Filter by severity
```
/audit --severity critical
/audit --severity warning
```

### Show top N findings only
```
/audit --top 10
```

### Combine flags
```
/audit src/ --focus security,bugs --severity warning --changed
```

---

## The Report

After all agents finish scanning, you get a unified report with:

### Health Grade (A+ to F)

Your project gets a grade based on the number and severity of findings:

| Grade | Score | Meaning |
|-------|-------|---------|
| A+ | 0 | Pristine — no issues found |
| A | 1-5 | Excellent |
| B+ | 6-15 | Very Good |
| B | 16-30 | Good |
| B- | 31-50 | Above Average |
| C+ | 51-80 | Average |
| C | 81-120 | Below Average |
| D | 121-170 | Poor |
| F | 171+ | Critical — needs immediate attention |

### Prioritized Findings

Every finding includes:
- **ID** — unique identifier (e.g., `SEC-001`, `BUG-003`, `PERF-007`)
- **Severity** — critical / warning / info
- **Location** — file path and line number
- **Description** — what the issue is and why it matters
- **Suggestion** — specific, actionable fix

### Action Plan

Findings are grouped into:
- **Quick Wins** — fix in minutes, low risk (dead imports, stale TODOs)
- **Important Fixes** — fix soon, medium effort (bugs, security warnings)
- **Strategic Improvements** — plan and schedule (architecture, major refactors)

---

## Fixing Issues

After the report, choose what to fix:

```
fix all                        # Fix everything
fix critical                   # Only critical severity
fix security                   # Only security findings
fix bugs                       # Only bug findings
fix deadcode                   # Only dead code findings
fix architecture               # Only architecture findings
fix performance                # Only performance findings
fix SEC-001, BUG-003, PERF-007 # Specific findings by ID
fix quick wins                 # Only quick wins from action plan
skip                           # Keep the report, don't fix
```

Fixes are applied surgically — minimal changes, preserving your code style.

---

## Customization

### .auditignore

Create a `.auditignore` file in your project root to exclude paths from scanning. Uses `.gitignore` syntax:

```gitignore
# Skip generated code
generated/
*.generated.ts

# Skip vendor
third_party/

# Skip test fixtures
tests/fixtures/
```

These paths are always excluded automatically:
- `node_modules/`, `vendor/`, `venv/`, `.venv/`, `__pycache__/`
- `.git/`, `dist/`, `build/`
- `*.min.js`, `*.min.css`
- Lock files (`package-lock.json`, `yarn.lock`, `poetry.lock`, `Cargo.lock`, `go.sum`)

---

## Supported Languages

`/audit` is language-agnostic. It analyzes patterns, logic, and structure — not syntax. It works with any language Claude Code supports, including:

Python, JavaScript, TypeScript, Go, Rust, Java, C#, C/C++, Ruby, PHP, Swift, Kotlin, Dart, Elixir, Scala, and more.

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI or IDE extension
- Claude model with Agent support (Opus, Sonnet)

---

## Examples

### Pre-PR security check
```
/audit --focus security --changed
```

### Quick cleanup before release
```
/audit --focus deadcode --fix
```

### Full audit of a microservice
```
/audit services/auth/ --severity warning
```

### Architecture review of the whole project
```
/audit --focus architecture
```

---

## FAQ

**How long does a full audit take?**
Depends on project size. Small projects (< 50 files): ~1-2 minutes. Medium (50-200): ~2-4 minutes. Large (200+): consider using `--focus` or `--changed`.

**Does it modify my code?**
Never during scanning. Only after you explicitly choose which fixes to apply.

**Does it work with monorepos?**
Yes. Point it at a specific directory: `/audit packages/api/`

**Can I run it in CI?**
Not directly (Claude Code is interactive), but you can use the report format as a template for CI integration.

**Will it find all bugs?**
No tool finds everything. `/audit` catches common patterns and anti-patterns through static analysis. It complements, not replaces, testing, linting, and manual review.

---

## Contributing

Issues and PRs welcome at [github.com/atobones/claude-audit](https://github.com/atobones/claude-audit).

Ideas for new agents or checks? Open an issue.

---

## License

MIT
