# doccoverage

<p align="center">
  <img src="https://img.shields.io/badge/patterns-85+-blue" alt="85+ patterns">
  <img src="https://img.shields.io/badge/languages-5-purple" alt="5 languages">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/install-clawhub-blue" alt="ClawHub">
  <img src="https://img.shields.io/badge/zero-telemetry-brightgreen" alt="Zero telemetry">
  <img src="https://img.shields.io/badge/100%25-local-brightgreen" alt="100% local">
</p>

<h3 align="center">Measure your documentation. Not just generate it.</h3>

<p align="center">
  <a href="https://doccoverage.pages.dev">Website</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#supported-languages">Languages</a> &middot;
  <a href="https://doccoverage.pages.dev/#pricing">Pricing</a>
</p>

---

## Documentation tools generate docs. DocCoverage measures if they exist.

Most documentation tools (documentation.js, typedoc, Sphinx, godoc, Javadoc) generate documentation from existing comments. But they cannot tell you what is *missing*. They cannot measure *coverage*. They cannot enforce *quality*.

DocCoverage is different. It scans your codebase and tells you:
- Which public functions have no documentation at all
- Which JSDoc/docstrings are incomplete (missing @param, @returns, Args, Returns)
- Whether your README has required sections (installation, usage, API)
- Whether your CHANGELOG is up to date
- Whether your comments are actually helpful or just noise

**DocCoverage measures doc coverage and quality before your code ships.** Pre-commit hooks. Local scanning. 85+ patterns across 5 languages. Zero data leaves your laptop.

## Quick Start

```bash
# 1. Install via ClawHub (free)
clawhub install doccoverage

# 2. Scan your repo
doccoverage scan

# 3. Install pre-commit hooks (Pro)
doccoverage hooks install
```

That's it. Every commit is now checked for documentation gaps.

## What It Does

### Scan code for undocumented functions
One command to scan any file, directory, or your entire repo. 85+ regex patterns detect missing JSDoc, docstrings, godoc comments, Javadoc, YARD docs, incomplete parameter descriptions, and documentation quality issues across JS/TS, Python, Go, Java, and Ruby.

### Block commits with pre-commit hooks
Install a lefthook pre-commit hook that scans every staged file. If a documentation gap is detected, the commit is blocked with a clear remediation message.

### Generate coverage reports
Produce markdown reports with coverage percentages, severity breakdowns, and remediation steps. Ideal for documentation reviews and team standards.

### Calculate doc coverage percentage
Get precise documentation coverage metrics: what percentage of your public API is documented, broken down by language, file, and category.

### Enforce documentation policies
Define organization-specific policies (all public APIs must have @example, all @param must include type) and enforce them alongside the built-in 85+ patterns.

### Verify CHANGELOG completeness
Check that your CHANGELOG has entries for recent tags, proper date formatting, and no empty sections.

## How It Compares

| Feature | DocCoverage | documentation.js | typedoc | pydocstyle | golint | Javadoc | inch |
|---------|:-----------:|:-----------------:|:-------:|:----------:|:------:|:-------:|:----:|
| Measures doc *coverage* | Yes | No | No | Partial | Partial | No | Yes |
| Multi-language (5+) | Yes | JS only | TS only | Python only | Go only | Java only | Elixir |
| Missing function docs | Yes | No | No | Yes | Yes | No | Yes |
| Incomplete param docs | Yes | No | No | Yes | No | No | No |
| README section analysis | Yes | No | No | No | No | No | No |
| CHANGELOG verification | Yes | No | No | No | No | No | No |
| Comment quality checks | Yes | No | No | No | No | No | No |
| Pre-commit hooks | Yes | No | No | No | No | No | No |
| Zero config scan | Yes | Config needed | Config needed | Config needed | N/A | N/A | Config needed |
| Doc coverage percentage | Yes | No | No | No | No | No | Yes |
| SARIF output for CI/CD | Yes | No | No | No | No | No | No |
| Offline license validation | Yes | N/A | N/A | N/A | N/A | N/A | N/A |
| Local-only (no cloud) | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Zero telemetry | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| ClawHub integration | Yes | No | No | No | No | No | No |
| Price (individual) | Free/$19/mo | Free | Free | Free | Free | Free | Free |

**Key difference:** Those tools *generate* documentation. DocCoverage *measures* whether documentation exists and whether it is complete.

## Supported Languages

DocCoverage detects 85+ documentation patterns across 5 languages:

### JavaScript / TypeScript

| Check | Severity | Description |
|-------|----------|-------------|
| Exported function without JSDoc | Critical | export function/const without preceding JSDoc block |
| Missing @param tags | High | JSDoc present but @param missing for function parameters |
| Missing @returns tag | High | JSDoc present but @returns missing for non-void functions |
| React component without prop docs | Medium | Exported React component without prop type descriptions |
| TypeScript interface without docs | Medium | Exported interface members without doc comments |

### Python

| Check | Severity | Description |
|-------|----------|-------------|
| Public function without docstring | Critical | def without triple-quote docstring |
| Missing Args section | High | Docstring present but Args: section missing |
| Missing Returns section | High | Docstring present but Returns: section missing |
| __init__ without docstring | Medium | Class constructor without documentation |
| Abstract method without docstring | Medium | Abstract method missing documentation |

### Go

| Check | Severity | Description |
|-------|----------|-------------|
| Exported function without godoc | Critical | Exported func without preceding comment |
| Exported type without godoc | High | Exported type/struct without preceding comment |
| Exported method without godoc | High | Exported method without preceding comment |

### Java

| Check | Severity | Description |
|-------|----------|-------------|
| Public method without Javadoc | Critical | public method without /** ... */ block |
| Missing @param in Javadoc | High | Javadoc present but @param missing |
| Missing @return in Javadoc | High | Javadoc present but @return missing |

### Ruby

| Check | Severity | Description |
|-------|----------|-------------|
| Public method without YARD doc | Critical | def without preceding # comment block |
| Missing @param in YARD | High | YARD doc present but @param missing |
| Missing @return in YARD | High | YARD doc present but @return missing |

## Pricing

| Feature | Free | Pro ($19/user/mo) | Team ($39/user/mo) |
|---------|:----:|:------------------:|:-------------------:|
| One-shot doc scan | 5 files | Unlimited | Unlimited |
| 85+ detection patterns | Yes | Yes | Yes |
| Auto-detect languages | Yes | Yes | Yes |
| Pre-commit hooks | | Yes | Yes |
| Coverage reports | | Yes | Yes |
| Coverage percentage | | Yes | Yes |
| Policy enforcement | | | Yes |
| CHANGELOG verification | | | Yes |
| SARIF output | | | Yes |
| CI/CD integration | | | Yes |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "doccoverage": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
        "config": {
          "severityThreshold": "high",
          "customPolicies": [
            {
              "regex": "export function [a-zA-Z]",
              "severity": "critical",
              "description": "All exported functions must have JSDoc"
            }
          ],
          "excludePatterns": ["**/test/**", "**/examples/**"]
        }
      }
    }
  }
}
```

## Ecosystem

DocCoverage is part of the ClawHub developer tools suite:

- **[EnvGuard](https://envguard.pages.dev)** -- Pre-commit secret detection
- **[DepGuard](https://depguard.pages.dev)** -- Dependency vulnerability scanning
- **[ConfigSafe](https://configsafe.pages.dev)** -- Infrastructure configuration auditing
- **[SQLGuard](https://sqlguard.pages.dev)** -- SQL query safety & injection risk scanning
- **[TestGap](https://testgap.pages.dev)** -- Test coverage gap analysis
- **[DocCoverage](https://doccoverage.pages.dev)** -- Documentation coverage & quality analysis

## Privacy

- 100% local -- no code sent externally
- Zero telemetry
- Offline license validation
- Pattern matching only -- no AST parsing, no external dependencies

## License

MIT
