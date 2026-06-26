---
name: doccoverage
description: Documentation coverage & quality analyzer — detects undocumented public functions, missing JSDoc/docstrings/godoc/Javadoc, incomplete parameter descriptions, README gaps, CHANGELOG issues, and doc quality problems across JS/TS, Python, Go, Java, Ruby
homepage: https://doccoverage.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udcdd",
      "primaryEnv": "DOCCOVERAGE_LICENSE_KEY",
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

# DocCoverage -- Documentation Coverage & Quality Analyzer

DocCoverage scans codebases for undocumented public functions, missing JSDoc/docstrings/godoc/Javadoc/YARD, incomplete parameter descriptions, outdated README sections, missing CHANGELOG entries, and documentation quality gaps. It uses regex-based pattern matching against 85+ documentation patterns across JS/TS, Python, Go, Java, and Ruby. Lefthook integration for git hooks, markdown coverage reports with doc quality scoring.

## Commands

### Free Tier (No license required)

#### `doccoverage scan [file|directory]`
One-shot documentation coverage scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/doccoverage.sh" scan [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Auto-detects language from file extensions (JS/TS, Python, Go, Java, Ruby)
3. Finds all source files with public/exported functions, classes, and types
4. Runs 85+ documentation coverage patterns against each file
5. Calculates a documentation coverage score (0-100) per file and overall
6. Outputs findings with: file, line number, check ID, severity, description, recommendation
7. Exit code 0 if passing (score >= 70), exit code 1 if issues found
8. Free tier limited to 5 files per scan

**Example usage scenarios:**
- "Check my code for missing documentation" -> runs `doccoverage scan .`
- "Are my exported functions documented?" -> runs `doccoverage scan src/`
- "Scan this file for missing JSDoc" -> runs `doccoverage scan src/utils.ts`
- "Check documentation coverage of my Python module" -> runs `doccoverage scan mymodule/`

### Pro Tier ($19/user/month -- requires DOCCOVERAGE_LICENSE_KEY)

#### `doccoverage hooks install`
Install git pre-commit hooks that scan staged files for documentation gaps before every commit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/doccoverage.sh" hooks install
```

**What it does:**
1. Validates Pro+ license
2. Copies lefthook config to project root
3. Installs lefthook pre-commit hook
4. On every commit: scans all staged files for missing documentation, blocks commit if critical/high findings, shows remediation advice

#### `doccoverage hooks uninstall`
Remove DocCoverage git hooks.

```bash
bash "<SKILL_DIR>/scripts/doccoverage.sh" hooks uninstall
```

#### `doccoverage report [directory]`
Generate a markdown documentation coverage report with findings, severity breakdown, and remediation steps.

```bash
bash "<SKILL_DIR>/scripts/doccoverage.sh" report [directory]
```

**What it does:**
1. Validates Pro+ license
2. Runs full scan of the directory
3. Generates a formatted markdown report from template
4. Includes per-file breakdowns, coverage scores, language-specific guidance
5. Output suitable for documentation reviews and team standards audits

#### `doccoverage coverage [directory]`
Calculate documentation coverage percentage across the codebase.

```bash
bash "<SKILL_DIR>/scripts/doccoverage.sh" coverage [directory]
```

**What it does:**
1. Validates Pro+ license
2. Identifies all public/exported functions, classes, types, and interfaces
3. Checks each for presence of documentation (JSDoc, docstring, godoc, etc.)
4. Calculates per-file and overall documentation coverage percentages
5. Reports coverage by language, by category, and overall

### Team Tier ($39/user/month -- requires DOCCOVERAGE_LICENSE_KEY with team tier)

#### `doccoverage policy [directory]`
Enforce organization-specific documentation policies on codebases.

```bash
bash "<SKILL_DIR>/scripts/doccoverage.sh" policy [directory]
```

**What it does:**
1. Validates Team+ license
2. Loads custom policies from ~/.openclaw/openclaw.json (doccoverage.config.customPolicies)
3. Enforces organization-specific rules (e.g., all public APIs must have @example, all @param must include type)
4. Combines custom policies with built-in patterns for comprehensive scanning
5. Outputs SARIF-compatible results

#### `doccoverage sarif [directory]`
Generate SARIF JSON output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/doccoverage.sh" sarif [directory]
```

**What it does:**
1. Validates Team+ license
2. Runs full scan of the directory
3. Outputs findings in SARIF 2.1.0 JSON format
4. Compatible with GitHub Code Scanning, Azure DevOps, and other SARIF consumers

#### `doccoverage changelog [directory]`
Verify CHANGELOG completeness and consistency.

```bash
bash "<SKILL_DIR>/scripts/doccoverage.sh" changelog [directory]
```

**What it does:**
1. Validates Team+ license
2. Scans CHANGELOG.md or HISTORY.md for completeness
3. Checks for missing version entries, empty sections, broken date formats
4. Verifies recent git tags have corresponding changelog entries
5. Reports changelog health with specific remediation suggestions

#### `doccoverage status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/doccoverage.sh" status
```

## Detected Documentation Gaps

DocCoverage detects 85+ documentation quality patterns across 6 categories:

| Category | Examples | Severity |
|----------|----------|----------|
| **Missing Function/Method Docs** | Exported functions without JSDoc, public methods without docstrings, Go exported functions without godoc, Java public methods without Javadoc, Ruby public methods without YARD | Critical/High |
| **Incomplete Documentation** | JSDoc missing @param tags, docstrings missing Args section, @deprecated without replacement, missing @returns, generic placeholder docs | High/Medium |
| **README & Project Docs** | Missing README.md, README without installation section, missing CONTRIBUTING.md, missing LICENSE, outdated badges, empty README sections | High/Medium |
| **API Documentation** | REST endpoints without docs, GraphQL types without descriptions, OpenAPI missing descriptions, missing error response docs | High/Medium |
| **Type & Interface Docs** | Exported TypeScript interfaces without docs, enum values without descriptions, generic type parameters without docs | Medium/Low |
| **Comment Quality** | Obvious/redundant comments, commented-out code blocks, outdated comments, TODO without ticket reference, FIXME older than threshold | Medium/Low |

## Configuration

Users can configure DocCoverage in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "doccoverage": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "high",
          "customPolicies": [],
          "excludePatterns": ["**/test/**", "**/examples/**", "**/vendor/**"],
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
- Pattern matching only -- no AST parsing, no external dependencies
- Supports scanning multiple languages in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = passing (score >= 70), 1 = issues found (for CI/CD integration)
- Scoring: critical=25, high=15, medium=8, low=3 point deductions from 100

## Error Handling

- If lefthook is not installed and user tries `hooks install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://doccoverage.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If language cannot be determined from extension, skip the file gracefully

## When to Use DocCoverage

The user might say things like:
- "Check my code for missing documentation"
- "Are my public functions documented?"
- "Scan for missing JSDoc comments"
- "What is the documentation coverage of my project?"
- "Check if my Python docstrings are complete"
- "Scan for undocumented exported functions"
- "Generate a documentation coverage report"
- "Set up pre-commit hooks for doc coverage"
- "Check my README for missing sections"
- "Verify my CHANGELOG is up to date"
- "Are there any TODO comments without ticket references?"
- "Find commented-out code in my project"
- "Check TypeScript interfaces for missing docs"
