# deadcode

<p align="center">
  <img src="https://img.shields.io/badge/patterns-60+-blue" alt="60+ patterns">
  <img src="https://img.shields.io/badge/languages-5-purple" alt="5 languages">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/install-clawhub-blue" alt="ClawHub">
  <img src="https://img.shields.io/badge/zero-telemetry-brightgreen" alt="Zero telemetry">
</p>

<h3 align="center">Find the code nobody uses. Remove it before it rots.</h3>

<p align="center">
  <a href="https://deadcode.pages.dev">Website</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#supported-languages">Languages</a> &middot;
  <a href="https://deadcode.pages.dev/#pricing">Pricing</a>
</p>

---

## Your codebase has dead code. A lot of it.

Studies show 10-30% of code in a typical project is dead. Unused exports. Orphan files nobody imports. Commented-out blocks from three sprints ago. Console.log statements that survived code review. Functions with `pass` as the body. CSS classes that match no element.

Dead code is not harmless. It slows onboarding. It confuses grep. It inflates bundles. It creates false positives in security scans. And it grows.

**DeadCode finds the rot before it spreads.** Pre-commit hooks. Local scanning. 60+ patterns across 5 language categories. Zero data leaves your laptop.

## Quick Start

```bash
# 1. Install via ClawHub (free)
clawhub install deadcode

# 2. Scan your repo
deadcode scan

# 3. Install pre-commit hooks (Pro)
deadcode hooks install
```

That's it. Every commit is now scanned for dead code before it lands.

## What It Does

### Scan source files for dead code
One command to scan any file, directory, or your entire repo. 60+ regex patterns detect dead code across JavaScript/TypeScript, Python, Go, CSS/SCSS, and general code cruft.

### Block commits with pre-commit hooks
Install a lefthook pre-commit hook that scans every staged source file. If dead code is detected, the commit is blocked with a clear cleanup message.

### Generate dead code reports
Produce markdown reports with severity breakdowns, orphan file detection, and cleanup priority. Ideal for tech debt tracking and sprint planning.

### Find orphan files
Detect files that are never imported, required, or referenced by any other file. Excludes entry points, test files, and config files automatically.

### Manage ignore rules
Define organization-specific ignore patterns and check IDs. Skip known false positives without disabling entire categories.

### SARIF output for CI/CD
Generate SARIF v2.1.0 output compatible with GitHub Code Scanning, Azure DevOps, and other CI systems.

## How It Compares

| Feature | DeadCode | ts-prune ($0) | knip ($0) | vulture ($0) | deadcode (Go) ($0) |
|---------|:--------:|:-------------:|:---------:|:------------:|:-------------------:|
| JavaScript/TypeScript | Yes | Yes | Yes | No | No |
| Python dead code | Yes | No | No | Yes | No |
| Go dead code | Yes | No | No | No | Yes |
| CSS/SCSS dead code | Yes | No | No | No | No |
| Multi-language scan | Yes | No | Partial | No | No |
| Pre-commit hooks | Yes | No | No | No | No |
| Orphan file detection | Yes | No | Yes | No | No |
| Zero config scan | Yes | Config required | Config required | Yes | Yes |
| Offline license validation | Yes | N/A | N/A | N/A | N/A |
| Local-only (no cloud) | Yes | Yes | Yes | Yes | Yes |
| Zero telemetry | Yes | Yes | Yes | Yes | Yes |
| SARIF output | Yes | No | No | No | No |
| ClawHub integration | Yes | No | No | No | No |
| Price (individual) | Free/$19/mo | Free | Free | Free | Free |

## Supported Languages

DeadCode detects 60+ dead code patterns across 5 language categories:

### JavaScript/TypeScript

| Check | Severity | Description |
|-------|----------|-------------|
| Unused exports | Critical | Exported functions/classes/constants never imported elsewhere |
| Orphan files | High | Files never imported or required by any other file |
| console.log/debug | Medium | Console statements left in production code |
| Commented-out code | Medium | Large blocks of commented-out code |
| Unreachable code | High | Code after return/throw/break/continue statements |
| Empty function bodies | Medium | Functions with empty bodies (no-op) |
| Unused variables | High | Variables declared but never referenced |
| Dead switch cases | Medium | Switch case branches with no code |
| Deprecated markers | Low | @deprecated JSDoc tags indicating dead code |
| Empty catch blocks | Medium | Catch blocks that swallow errors silently |
| TODO/FIXME/HACK | Low | Comments indicating incomplete or temporary code |
| Triple-slash refs | Low | Stale triple-slash reference directives |

### Python

| Check | Severity | Description |
|-------|----------|-------------|
| Unused functions | High | Functions defined but never called in module |
| Unused imports | High | Imports that are never used |
| pass-only bodies | Medium | Functions/classes with only `pass` as body |
| Commented-out code | Medium | Large blocks of commented-out code |
| Unreachable code | High | Code after return/raise/break |
| __all__ mismatches | Medium | Exports in __all__ that don't match definitions |
| Empty except blocks | Medium | Except blocks that silently swallow exceptions |
| Dead else branches | Low | Unreachable else branches |

### Go

| Check | Severity | Description |
|-------|----------|-------------|
| Unused imports | High | Imports not used in the file |
| Dead exported funcs | High | Exported functions never called from tests or packages |
| Unreachable code | High | Code after return/panic statements |
| Empty function bodies | Medium | Functions with empty bodies |
| Commented-out code | Medium | Large blocks of commented-out code |
| Empty init() | Medium | init() functions that do nothing |

### CSS/SCSS

| Check | Severity | Description |
|-------|----------|-------------|
| Unused selectors | High | CSS classes/IDs never referenced in source files |
| Empty rule blocks | Medium | Selectors with no declarations |
| Duplicate selectors | Medium | Same selector declared multiple times |
| Commented-out styles | Low | Large blocks of commented-out CSS |
| !important overuse | Medium | More than 5 !important declarations in a file |
| Unused CSS variables | High | Custom properties defined but never referenced |
| Empty media queries | Medium | Media queries with no rules inside |
| Vendor prefixes | Low | Vendor prefixes that autoprefixer should handle |

### General

| Check | Severity | Description |
|-------|----------|-------------|
| Orphan files | High | Files not imported/referenced by any other file |
| Large comment blocks | Medium | 10+ consecutive comment lines |
| TODO/FIXME density | Medium | More than 5 TODO/FIXME/HACK per file |
| Debug/test code | High | Debug or test code left in production files |
| Feature flag remnants | Medium | Feature flags referencing removed features |
| Placeholder text | Low | Lorem ipsum, TODO: implement, and other placeholder text |

## Pricing

| Feature | Free | Pro ($19/user/mo) | Team ($39/user/mo) |
|---------|:----:|:------------------:|:-------------------:|
| One-shot dead code scan | 5 files | Unlimited | Unlimited |
| 60+ detection patterns | Yes | Yes | Yes |
| Auto-detect languages | Yes | Yes | Yes |
| Pre-commit hooks | | Yes | Yes |
| Dead code reports | | Yes | Yes |
| Orphan file detection | | Yes | Yes |
| Custom ignore rules | | | Yes |
| SARIF output | | | Yes |
| CI/CD integration | | | Yes |
| Cross-repo analysis | | | Yes |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "deadcode": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
        "config": {
          "severityThreshold": "high",
          "ignorePatterns": ["**/test/**", "**/fixtures/**", "**/*.spec.*"],
          "ignoreChecks": ["DC-JS-011"],
          "reportFormat": "markdown"
        }
      }
    }
  }
}
```

## Ecosystem

DeadCode is part of the ClawHub code quality suite:

- **[EnvGuard](https://envguard.pages.dev)** -- Pre-commit secret detection
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

## Privacy

- 100% local -- no code sent externally
- Zero telemetry
- Offline license validation
- Pattern matching only -- no AST parsing, no external dependencies

## License

MIT
