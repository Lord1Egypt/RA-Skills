---
name: AsyncGuard
version: 1.0.0
description: "Async/await anti-pattern analyzer -- detects promise misuse, async resource leaks, event loop blocking, missing cancellation, async error patterns, and coordination issues"
homepage: https://asyncguard.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\u26a1",
      "primaryEnv": "ASYNCGUARD_LICENSE_KEY",
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

# AsyncGuard -- Async/Await Anti-Pattern Analyzer

AsyncGuard scans codebases for async/await anti-patterns, promise misuse, async resource leaks, event loop blocking, missing cancellation support, async error handling gaps, and coordination issues. It uses regex-based pattern matching against 90 async-specific patterns across 6 categories, lefthook for git hook integration, and produces markdown reports with actionable remediation guidance. 100% local. Zero telemetry.

## Commands

### Free Tier (No license required)

#### `asyncguard scan [file|directory]`
One-shot async safety scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 30 async patterns against each file (free tier limit)
4. Calculates an async safety score (0-100) per file and overall
5. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
6. Outputs findings with: file, line number, check ID, severity, description, recommendation
7. Exit code 0 if score >= 70, exit code 1 if async quality is poor
8. Free tier limited to first 30 patterns (PM + AR categories)

**Example usage scenarios:**
- "Scan my code for async issues" -> runs `asyncguard scan .`
- "Check this file for promise misuse" -> runs `asyncguard scan src/server.ts`
- "Find resource leaks in my async code" -> runs `asyncguard scan src/`
- "Audit async patterns in my project" -> runs `asyncguard scan .`
- "Check for missing cancellation" -> runs `asyncguard scan .`

### Pro Tier ($19/user/month -- requires ASYNCGUARD_LICENSE_KEY)

#### `asyncguard scan --tier pro [file|directory]`
Extended scan with 60 patterns covering promise misuse, resource leaks, event loop blocking, and cancellation.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier pro
```

**What it does:**
1. Validates Pro+ license
2. Runs 60 async patterns (PM, AR, EL, CA categories)
3. Detects event loop blocking (sync I/O, sync crypto)
4. Identifies missing cancellation and abort handling
5. Full category breakdown reporting

#### `asyncguard scan --format json [directory]`
Generate JSON output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format json
```

#### `asyncguard scan --format html [directory]`
Generate HTML report for browser viewing.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format html
```

#### `asyncguard scan --category EL [directory]`
Filter scan to a specific check category (PM, AR, EL, CA, AE, AC).

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --category EL
```

### Team Tier ($39/user/month -- requires ASYNCGUARD_LICENSE_KEY with team tier)

#### `asyncguard scan --tier team [directory]`
Full scan with all 90 patterns across all 6 categories including async error patterns and coordination.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --tier team
```

**What it does:**
1. Validates Team+ license
2. Runs all 90 patterns across 6 categories
3. Includes async error pattern detection (swallowed rejections, async forEach, empty catch)
4. Includes coordination checks (unbounded concurrency, missing backpressure, no rate limit)
5. Full category breakdown with per-file results

#### `asyncguard scan --verbose [directory]`
Verbose output showing every matched line and pattern details.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --verbose
```

#### `asyncguard status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" status
```

## Check Categories

AsyncGuard detects 90 async anti-patterns across 6 categories:

| Category | Code | Patterns | Description | Severity Range |
|----------|------|----------|-------------|----------------|
| **Promise/Future Misuse** | PM | 15 | Unhandled promises, async executor, nested .then chains, deferred antipattern | medium -- critical |
| **Async Resource Leaks** | AR | 15 | Unclosed connections, missing dispose, dangling streams, leaked timers | medium -- critical |
| **Event Loop Blocking** | EL | 15 | Sync file I/O, sync crypto, CPU loops, sync child process | low -- critical |
| **Cancellation & Abortion** | CA | 15 | Missing AbortSignal, orphaned tasks, no cleanup on unmount | medium -- critical |
| **Async Error Patterns** | AE | 15 | Swallowed rejections, empty .catch, async forEach, missing try/catch | medium -- critical |
| **Async Coordination** | AC | 15 | Unbounded Promise.all, missing semaphore, no backpressure, no rate limit | medium -- critical |

## Tier-Based Pattern Access

| Tier | Patterns | Categories |
|------|----------|------------|
| **Free** | 30 | PM, AR |
| **Pro** | 60 | PM, AR, EL, CA |
| **Team** | 90 | PM, AR, EL, CA, AE, AC |
| **Enterprise** | 90 | PM, AR, EL, CA, AE, AC + priority support |

## Scoring

AsyncGuard uses a deductive scoring system starting at 100 (perfect):

| Severity | Point Deduction | Description |
|----------|-----------------|-------------|
| **Critical** | -25 per finding | Severe async issue (resource leaks, unhandled rejections, blocking I/O) |
| **High** | -15 per finding | Significant async problem (missing cancellation, no error handler) |
| **Medium** | -8 per finding | Moderate concern (coordination issues, missing backpressure) |
| **Low** | -3 per finding | Informational / best practice suggestion |

### Grading Scale

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| **A** | 90-100 | Excellent async code quality |
| **B** | 80-89 | Good async patterns with minor issues |
| **C** | 70-79 | Acceptable but needs improvement |
| **D** | 60-69 | Poor async quality |
| **F** | Below 60 | Critical async problems |

- **Pass threshold:** 70 (Grade C or better)
- Exit code 0 = pass (score >= 70)
- Exit code 1 = fail (score < 70)

## Configuration

Users can configure AsyncGuard in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "asyncguard": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "medium",
          "ignorePatterns": ["**/test/**", "**/fixtures/**", "**/*.test.*"],
          "ignoreChecks": [],
          "reportFormat": "text"
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
- Supports scanning all file types in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = pass (score >= 70), 1 = fail (for CI/CD integration)
- Output formats: text (default), json, html

## Error Handling

- If lefthook is not installed and user tries hooks, prompt to install it
- If license key is invalid or expired, show clear message with link to https://asyncguard.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If an invalid category is specified with --category, show available categories

## When to Use AsyncGuard

The user might say things like:
- "Scan my code for async issues"
- "Check my promise handling"
- "Find resource leaks in async code"
- "Detect event loop blocking"
- "Are there any missing cancellation handlers?"
- "Check for unhandled promise rejections"
- "Audit my async error handling"
- "Find missing AbortController usage"
- "Check for synchronous I/O in async functions"
- "Scan for async anti-patterns"
- "Run an async code audit"
- "Generate an async safety report"
- "Check if my fetch calls have abort signals"
- "Find empty catch handlers"
- "Check my code for async coordination issues"
