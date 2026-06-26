---
name: concurrencyguard
description: Race condition & concurrency safety analyzer -- detects unprotected shared state, missing locks, TOCTOU vulnerabilities, async/await pitfalls, thread-unsafe singletons, and deadlock-prone patterns across all languages
homepage: https://concurrencyguard.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\u26a1",
      "primaryEnv": "CONCURRENCYGUARD_LICENSE_KEY",
      "requires": {
        "bins": ["git", "bash", "python3", "jq"]
      },
      "configPaths": ["~/.openclaw/openclaw.json"],
      "install": [
        {
          "id": "lefthook",
          "kind": "brew",
          "formula": "lefthook",
          "bins": ["lefthook"],
          "label": "Install lefthook (git hooks manager)"
        }
      ],
      "os": ["darwin", "linux", "win32"]
    }
  }
user-invocable: true
disable-model-invocation: false
---

# ConcurrencyGuard -- Race Condition & Concurrency Safety Analyzer

ConcurrencyGuard scans codebases for concurrency hazards: unprotected shared state, missing mutex/locks, TOCTOU vulnerabilities, async/await pitfalls, thread-unsafe singletons, missing transaction isolation, data races in goroutines, unguarded lazy initialization, non-atomic read-modify-write, and deadlock-prone lock ordering -- across JS/TS, Python, Java, Go, Rust, and C#. It uses regex-based pattern matching against 90+ concurrency safety patterns, lefthook for git hook integration, and produces markdown reports with actionable remediation recommendations. 100% local. Zero telemetry.

## Commands

### Free Tier (No license required)

#### `concurrencyguard scan [file|directory]`
One-shot concurrency safety scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/concurrencyguard.sh" scan [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 90+ concurrency safety patterns against each file
4. Respects .gitignore and allowlist files
5. Calculates a concurrency safety score (0-100) per file and overall
6. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
7. Outputs findings with: file, line number, check ID, severity, description, recommendation
8. Exit code 0 if score >= 70, exit code 1 if too many issues found
9. Free tier limited to 5 files per scan

**Example usage scenarios:**
- "Scan my code for race conditions" -> runs `concurrencyguard scan .`
- "Check this file for concurrency issues" -> runs `concurrencyguard scan src/server.go`
- "Find thread safety problems in my project" -> runs `concurrencyguard scan src/`
- "Are there any deadlock risks in my code?" -> runs `concurrencyguard scan .`
- "Check for missing locks" -> runs `concurrencyguard scan .`
- "Find TOCTOU vulnerabilities" -> runs `concurrencyguard scan .`

#### `concurrencyguard hook install`
Install git pre-commit hooks that scan staged files for concurrency issues before every commit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/concurrencyguard.sh" hook install
```

**What it does:**
1. Copies lefthook config to project root
2. Installs lefthook pre-commit hook
3. On every commit: scans all staged files for concurrency hazards, blocks commit if critical/high findings, shows remediation advice

#### `concurrencyguard hook uninstall`
Remove ConcurrencyGuard git hooks.

```bash
bash "<SKILL_DIR>/scripts/concurrencyguard.sh" hook uninstall
```

#### `concurrencyguard report [directory]`
Generate a markdown concurrency safety report with findings, severity breakdown, and remediation steps.

```bash
bash "<SKILL_DIR>/scripts/concurrencyguard.sh" report [directory]
```

**What it does:**
1. Runs full scan of the directory
2. Generates a formatted markdown report from template
3. Includes per-file breakdowns, concurrency safety scores, remediation priority
4. Output suitable for code reviews and architecture audits

### Pro Tier ($19/user/month -- requires CONCURRENCYGUARD_LICENSE_KEY)

#### `concurrencyguard watch [directory]`
Continuous file-watching mode that re-scans on every file change.

```bash
bash "<SKILL_DIR>/scripts/concurrencyguard.sh" watch [directory]
```

**What it does:**
1. Validates Pro+ license
2. Watches directory for file changes using filesystem events
3. Re-scans changed files automatically
4. Reports new concurrency issues in real time
5. Ideal for active development sessions

#### `concurrencyguard ci [directory]`
CI/CD integration mode with strict exit codes and machine-readable output.

```bash
bash "<SKILL_DIR>/scripts/concurrencyguard.sh" ci [directory]
```

**What it does:**
1. Validates Pro+ license
2. Runs full scan of the directory
3. Outputs machine-readable results with exit codes for CI systems
4. Exit 0 = clean, exit 1 = critical/high issues, exit 2 = medium issues
5. Compatible with GitHub Actions, GitLab CI, Jenkins, CircleCI

### Team Tier ($39/user/month -- requires CONCURRENCYGUARD_LICENSE_KEY with team tier)

#### `concurrencyguard team-report [directory]`
Generate an aggregate team-level concurrency safety report with trend data.

```bash
bash "<SKILL_DIR>/scripts/concurrencyguard.sh" team-report [directory]
```

**What it does:**
1. Validates Team+ license
2. Runs full scan with aggregation by module/package
3. Generates team-level metrics (hotspot files, worst categories, trend indicators)
4. Includes per-developer breakdown when git blame data is available
5. Suitable for sprint retrospectives and architecture reviews

#### `concurrencyguard baseline [directory]`
Establish a baseline of known concurrency issues for allowlisting.

```bash
bash "<SKILL_DIR>/scripts/concurrencyguard.sh" baseline [directory]
```

**What it does:**
1. Validates Team+ license
2. Scans directory and records all current findings as baseline
3. Saves baseline to .concurrencyguard-baseline.json
4. Future scans only report NEW issues not in the baseline
5. Useful for legacy codebases with known accepted concurrency patterns

#### `concurrencyguard status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/concurrencyguard.sh" status
```

## Detected Concurrency Patterns

ConcurrencyGuard detects 90+ concurrency safety patterns across 6 categories:

| Category | Examples | Severity |
|----------|----------|----------|
| **Shared State (SS)** | Global mutable variables, unprotected static fields, module-level mutable state, shared variables without volatile/atomic, global object mutation in worker threads | Critical/High |
| **Locking & Mutex (LK)** | Missing synchronized in Java, missing lock in C#, missing mutex.Lock() in Go, Lock without Unlock, nested locks (deadlock risk), missing RWMutex, spin locks in user code | Critical/High |
| **TOCTOU & Atomicity (TC)** | Check-then-act without synchronization, file exists then open, read-modify-write without CAS, double-checked locking without volatile, non-atomic counters | Critical/High |
| **Async/Await Pitfalls (AW)** | Await in loop (sequential not parallel), missing await, async void, fire-and-forget promises, race conditions after await, missing Promise.all | High/Medium |
| **Thread Safety (TS)** | Thread-unsafe singleton, HashMap without sync, non-thread-safe datetime, mutable defaults shared across threads, lazy init without double-check | High/Medium |
| **Deadlock & Starvation (DL)** | Inconsistent lock ordering, holding lock across external call, channel without timeout, unbuffered channel in goroutine, missing select/default, lock held across await | Critical/High |

## Configuration

Users can configure ConcurrencyGuard in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "concurrencyguard": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "high",
          "ignorePatterns": ["**/test/**", "**/fixtures/**", "**/*.test.*"],
          "ignoreChecks": [],
          "allowlistFile": ".concurrencyguard-allowlist",
          "reportFormat": "markdown"
        }
      }
    }
  }
}
```

## Important Notes

- **Free tier** works immediately with no configuration
- **All scanning happens locally** -- no code is sent to external servers
- **License validation is offline** -- no phone-home or network calls
- Pattern matching only -- no AST parsing, no external dependencies beyond bash
- Supports scanning JS/TS, Python, Java, Go, Rust, and C# in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = clean (score >= 70), 1 = issues detected (for CI/CD integration)

## Error Handling

- If lefthook is not installed and user tries `hook install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://concurrencyguard.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If .concurrencyguard-allowlist is missing, skip allowlist filtering gracefully

## When to Use ConcurrencyGuard

The user might say things like:
- "Scan my code for race conditions"
- "Find concurrency bugs in my project"
- "Check for thread safety issues"
- "Are there any deadlock risks in my code?"
- "Scan for missing locks or mutexes"
- "Find TOCTOU vulnerabilities"
- "Check my async/await code for pitfalls"
- "Find unprotected shared state"
- "Detect data races in my Go code"
- "Check for thread-unsafe singletons"
- "Scan for concurrency issues before I push"
- "Set up pre-commit hooks for concurrency checking"
- "Generate a concurrency safety report"
- "Find missing synchronization in my Java code"
- "Check for non-atomic operations"
- "Detect deadlock-prone lock ordering"
