---
name: errorlens
description: Error handling & exception safety analyzer -- scans codebases for empty catches, swallowed exceptions, missing error boundaries, unhandled rejections, generic error types, and unsafe error patterns across all languages
homepage: https://errorlens.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udd0d",
      "primaryEnv": "ERRORLENS_LICENSE_KEY",
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

# ErrorLens -- Error Handling & Exception Safety Analyzer

ErrorLens scans codebases for dangerous error handling patterns: empty catch blocks, swallowed exceptions, missing error boundaries, unhandled promise rejections, generic error types, missing finally blocks, bare except clauses, error message information leaks, unchecked error returns, and missing error propagation. Covers JS/TS, Python, Java, Go, Rust, and C#. Uses regex-based pattern matching against 90+ error handling anti-patterns, lefthook for git hook integration, and produces markdown reports with actionable remediation recommendations. 100% local. Zero telemetry.

## Commands

### Free Tier (No license required)

#### `errorlens scan [file|directory]`
One-shot error handling scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/errorlens.sh" scan [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 90+ error handling pattern checks against each file
4. Respects .gitignore and allowlist files
5. Calculates an error safety score (0-100) per file and overall
6. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
7. Outputs findings with: file, line number, check ID, severity, description, recommendation
8. Exit code 0 if score >= 70, exit code 1 if too many issues found
9. Free tier limited to 5 files per scan

**Example usage scenarios:**
- "Scan my code for error handling issues" -> runs `errorlens scan .`
- "Check this file for empty catch blocks" -> runs `errorlens scan src/api.ts`
- "Find swallowed exceptions in my project" -> runs `errorlens scan src/`
- "Are there unsafe error patterns in my code?" -> runs `errorlens scan .`
- "Check for missing error boundaries" -> runs `errorlens scan .`

#### `errorlens hook`
Install git pre-commit hooks that scan staged files for error handling issues before every commit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/errorlens.sh" hook install
```

**What it does:**
1. Copies lefthook config to project root
2. Installs lefthook pre-commit hook
3. On every commit: scans all staged files for error handling issues, blocks commit if critical/high findings, shows remediation advice

#### `errorlens report [directory]`
Generate a markdown error handling report with findings, severity breakdown, and remediation steps.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/errorlens.sh" report [directory]
```

**What it does:**
1. Runs full scan of the directory
2. Generates a formatted markdown report from template
3. Includes per-file breakdowns, error safety scores, remediation priority
4. Output suitable for code reviews and quality audits

### Pro Tier ($19/user/month -- requires ERRORLENS_LICENSE_KEY)

#### `errorlens watch [directory]`
Continuous monitoring mode that watches for file changes and re-scans automatically.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/errorlens.sh" watch [directory]
```

**What it does:**
1. Validates Pro+ license
2. Watches directory for file modifications
3. Re-scans changed files automatically on save
4. Displays live error handling score updates
5. Useful for development-time feedback

#### `errorlens ci [directory]`
CI/CD integration mode with strict exit codes and machine-readable output.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/errorlens.sh" ci [directory]
```

**What it does:**
1. Validates Pro+ license
2. Runs full scan with no file limit
3. Outputs findings in CI-friendly format
4. Exit code 0 = pass (score >= 70), 1 = fail
5. Supports severity threshold configuration
6. Suitable for GitHub Actions, GitLab CI, Jenkins, etc.

### Team Tier ($39/user/month -- requires ERRORLENS_LICENSE_KEY with team tier)

#### `errorlens team-report [directory]`
Aggregate team-level error handling metrics and trends.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/errorlens.sh" team-report [directory]
```

**What it does:**
1. Validates Team+ license
2. Scans entire directory with full pattern set
3. Generates aggregate metrics per category (EC, SE, EB, GE, RP, IL)
4. Shows per-directory breakdown for team ownership analysis
5. Includes trend data if previous baselines exist
6. Reports team-wide error handling maturity score

#### `errorlens baseline [directory]`
Establish a baseline of known error handling issues for incremental improvement tracking.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/errorlens.sh" baseline [directory]
```

**What it does:**
1. Validates Team+ license
2. Scans directory and records all current findings as baseline
3. Saves baseline to .errorlens-baseline.json
4. Future scans only report NEW issues not in the baseline
5. Useful for legacy codebases with known accepted patterns
6. Enables incremental error handling improvement tracking

#### `errorlens status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/errorlens.sh" status
```

## Detected Error Handling Patterns

ErrorLens detects 90+ error handling anti-patterns across 6 categories:

| Category | Examples | Severity |
|----------|----------|----------|
| **Empty Catches (EC)** | Empty catch blocks in JS/TS/Java/C#/Python, catch with only comments, catch with only pass, catch-all without logging | Critical/High |
| **Swallowed Exceptions (SE)** | Catch blocks that don't rethrow/log, exception variable unused, catch that returns null/undefined/false silently, ignored error callbacks | Critical/High |
| **Error Boundaries (EB)** | Missing React error boundaries, missing Express error middleware, missing global handlers, unhandled promise rejections, window.onerror | High/Medium |
| **Generic Errors (GE)** | Throwing generic Error/Exception, bare except in Python, catching Throwable in Java, catching Object in TS, overly broad error types | High/Medium |
| **Resource & Propagation (RP)** | Missing finally for resource cleanup, unchecked error returns in Go, missing error propagation (? in Rust), ignored Result types, missing defer/close | High/Medium |
| **Information Leak (IL)** | Stack traces in HTTP responses, error.message in API responses, console.error with sensitive data, verbose errors in production, raw exception details to users | High/Medium |

## Configuration

Users can configure ErrorLens in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "errorlens": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "high",
          "ignorePatterns": ["**/test/**", "**/fixtures/**", "**/*.test.*"],
          "ignoreChecks": [],
          "allowlistFile": ".errorlens-allowlist",
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
- Supports scanning all file types in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = clean (score >= 70), 1 = issues detected (for CI/CD integration)

## Error Handling

- If lefthook is not installed and user tries `hook install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://errorlens.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If .errorlens-allowlist is missing, skip allowlist filtering gracefully

## When to Use ErrorLens

The user might say things like:
- "Scan my code for error handling issues"
- "Find empty catch blocks in my project"
- "Check for swallowed exceptions"
- "Are there missing error boundaries?"
- "Scan for unsafe error patterns"
- "Find unhandled promise rejections"
- "Check if my error handling is correct"
- "Detect bare except clauses"
- "Run an error handling audit"
- "Set up pre-commit hooks for error handling"
- "Generate an error handling report"
- "Find catch blocks that don't rethrow"
- "Check for generic error types"
- "Scan for information leaks in error messages"
- "Audit my code for exception safety"
- "Find missing finally blocks"
- "Check for unchecked error returns in Go"
- "Baseline existing error handling issues"
