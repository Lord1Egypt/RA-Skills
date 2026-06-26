# errorlens

<p align="center">
  <img src="https://img.shields.io/badge/patterns-90+-blue" alt="90+ patterns">
  <img src="https://img.shields.io/badge/categories-6-purple" alt="6 categories">
  <img src="https://img.shields.io/badge/languages-6-orange" alt="6 languages">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/install-clawhub-blue" alt="ClawHub">
  <img src="https://img.shields.io/badge/zero-telemetry-brightgreen" alt="Zero telemetry">
</p>

<h3 align="center">Find the error handling your code is missing. Fix it before users hit it.</h3>

<p align="center">
  <a href="https://errorlens.pages.dev">Website</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#detection-categories">Categories</a> &middot;
  <a href="https://errorlens.pages.dev/#pricing">Pricing</a>
</p>

---

## Your error handling has gaps. Dangerous ones.

Empty catch blocks that silently swallow errors. Bare `except:` clauses that mask bugs. Promise rejections that vanish into the void. Stack traces leaking to HTTP responses. Go errors ignored with `_`. Rust `Result` types silently `.unwrap()`'d in production.

Bad error handling is the leading cause of hard-to-debug production failures. When errors are swallowed, masked, or leaked, your application becomes unpredictable and your security surface expands.

**ErrorLens finds the gaps before they become incidents.** Pre-commit hooks. Local scanning. 90+ patterns across 6 detection categories. Zero data leaves your machine.

## Quick Start

```bash
# 1. Install via ClawHub (free)
clawhub install errorlens

# 2. Scan your repo
errorlens scan

# 3. Install pre-commit hooks
errorlens hook install
```

That's it. Every commit is now scanned for error handling issues before it lands.

## What It Does

### Scan files for error handling anti-patterns
One command to scan any file, directory, or your entire repo. 90+ regex patterns detect unsafe error handling across JavaScript/TypeScript, Python, Java, Go, Rust, and C#.

### Block commits with pre-commit hooks
Install a lefthook pre-commit hook that scans every staged file. If dangerous error patterns are detected, the commit is blocked with a clear remediation message.

### Generate error handling reports
Produce markdown reports with severity breakdowns, pattern categories, and remediation priority. Ideal for code reviews and quality audits.

### Continuous watch mode (Pro)
Monitor your codebase in real-time during development. Get instant feedback when error handling issues are introduced.

### CI/CD integration (Pro)
Run ErrorLens in your CI pipeline with strict exit codes. Block PRs that introduce new error handling anti-patterns.

### Team metrics and baseline (Team)
Track error handling maturity across your team. Baseline existing issues and measure incremental improvement over time.

## How It Compares

| Feature | ErrorLens | ESLint ($0) | SonarQube ($0+) | Semgrep ($0+) | PMD ($0) |
|---------|:---------:|:-----------:|:---------------:|:-------------:|:--------:|
| 90+ error patterns | Yes | ~15 | ~30 | ~20 | ~15 |
| Multi-language | 6 langs | JS/TS only | Many | Many | Java only |
| Pre-commit hooks | Yes | Via plugin | No | Yes | No |
| Baseline/allowlist | Yes | No | Yes | Yes | No |
| Zero config scan | Yes | Config required | Config required | Config required | Config required |
| Offline license | Yes | N/A | Cloud req. | Cloud req. | N/A |
| Local-only (no cloud) | Yes | Yes | Optional | Optional | Yes |
| Zero telemetry | Yes | Yes | No | No | Yes |
| No binary deps | Yes | Node.js | JVM | Python | JVM |
| Score & grades | Yes | No | Yes | No | No |
| ClawHub integration | Yes | No | No | No | No |
| Price (individual) | Free/$19/mo | Free | Free+ | Free+ | Free |

## Detection Categories

ErrorLens detects 90+ error handling anti-patterns across 6 categories:

### Empty Catches -- EC (15 patterns)

| Check | Severity | Languages | Description |
|-------|----------|-----------|-------------|
| EC-001 to EC-003 | Critical | JS/TS/Java/C# | Completely empty catch blocks |
| EC-004 to EC-006 | High | JS/TS/Java | Catch blocks with only comments |
| EC-007 to EC-009 | Critical | Python | Bare except with pass only |
| EC-010 to EC-012 | High | JS/TS/Java/C# | Catch-all without any logging |
| EC-013 to EC-015 | Medium | All | Empty catch in test/spec files |

### Swallowed Exceptions -- SE (15 patterns)

| Check | Severity | Languages | Description |
|-------|----------|-----------|-------------|
| SE-001 to SE-003 | Critical | JS/TS/Java | Catch that returns null/undefined silently |
| SE-004 to SE-006 | High | JS/TS/Python | Exception variable declared but unused |
| SE-007 to SE-009 | High | Java/C# | Catch blocks that don't rethrow or log |
| SE-010 to SE-012 | Medium | Go | Ignored error return values |
| SE-013 to SE-015 | High | All | Silent error callbacks |

### Error Boundaries -- EB (15 patterns)

| Check | Severity | Languages | Description |
|-------|----------|-----------|-------------|
| EB-001 to EB-003 | High | JS/TS | Missing React error boundaries |
| EB-004 to EB-006 | High | JS/TS | Missing Express error middleware |
| EB-007 to EB-009 | High | JS/TS | Unhandled promise rejections |
| EB-010 to EB-012 | Medium | JS/TS | Missing window.onerror/addEventListener |
| EB-013 to EB-015 | High | Python/Java | Missing global exception handlers |

### Generic Errors -- GE (15 patterns)

| Check | Severity | Languages | Description |
|-------|----------|-----------|-------------|
| GE-001 to GE-003 | High | JS/TS | Throwing generic Error() without subclass |
| GE-004 to GE-006 | Critical | Python | Bare except: without exception type |
| GE-007 to GE-009 | Critical | Java | Catching Throwable or Exception broadly |
| GE-010 to GE-012 | High | C# | Catching System.Exception broadly |
| GE-013 to GE-015 | Medium | Go/Rust | Generic error handling without specifics |

### Resource & Propagation -- RP (15 patterns)

| Check | Severity | Languages | Description |
|-------|----------|-----------|-------------|
| RP-001 to RP-003 | High | Java/C# | Missing finally for resource cleanup |
| RP-004 to RP-006 | Critical | Go | Unchecked error return values (err assigned to _) |
| RP-007 to RP-009 | High | Rust | Unsafe .unwrap() on Result/Option types |
| RP-010 to RP-012 | Medium | Go | Missing defer for resource cleanup |
| RP-013 to RP-015 | High | All | Missing error propagation patterns |

### Information Leak -- IL (15 patterns)

| Check | Severity | Languages | Description |
|-------|----------|-----------|-------------|
| IL-001 to IL-003 | Critical | JS/TS | Stack traces in HTTP responses |
| IL-004 to IL-006 | High | JS/TS/Python | Error details in API responses |
| IL-007 to IL-009 | High | Java/C# | Raw exception details to users |
| IL-010 to IL-012 | Medium | All | Verbose error logging with sensitive context |
| IL-013 to IL-015 | High | All | Debug error modes in production config |

## Pricing

| Feature | Free | Pro ($19/user/mo) | Team ($39/user/mo) |
|---------|:----:|:------------------:|:-------------------:|
| One-shot error scan | 5 files | Unlimited | Unlimited |
| 90+ detection patterns | Yes | Yes | Yes |
| Pre-commit hooks | Yes | Yes | Yes |
| Error handling reports | Yes | Yes | Yes |
| Watch mode | | Yes | Yes |
| CI/CD integration | | Yes | Yes |
| Baseline/allowlist | | | Yes |
| Team metrics | | | Yes |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "errorlens": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
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

## Ecosystem

ErrorLens is part of the ClawHub code quality suite:

- **[SecretScan](https://secretscan.pages.dev)** -- Hardcoded secrets & credential leak detection
- **[EnvGuard](https://envguard.pages.dev)** -- Environment variable safety scanning
- **[DepGuard](https://depguard.pages.dev)** -- Dependency vulnerability scanning
- **[ConfigSafe](https://configsafe.pages.dev)** -- Infrastructure configuration auditing
- **[APIShield](https://apishield.pages.dev)** -- API security scanning
- **[DeadCode](https://deadcode.pages.dev)** -- Dead code and unused export detection
- **[TypeDrift](https://typedrift.pages.dev)** -- Type safety drift detection
- **[PerfGuard](https://perfguard.pages.dev)** -- Performance regression detection
- **[GitPulse](https://gitpulse.pages.dev)** -- Git workflow analytics
- **[DocSync](https://docsync.pages.dev)** -- Documentation drift detection
- **[MigrateSafe](https://migratesafe.pages.dev)** -- Database migration safety checking
- **[LicenseGuard](https://licenseguard.pages.dev)** -- License compliance scanning
- **[StyleGuard](https://styleguard.pages.dev)** -- Code style consistency scanning
- **[ErrorLens](https://errorlens.pages.dev)** -- Error handling & exception safety analysis

## Privacy

- 100% local -- no code sent externally
- Zero telemetry
- Offline license validation
- Pattern matching only -- no AST parsing, no external dependencies beyond bash

## License

MIT
