---
name: DateGuard
version: 1.0.0
description: "Date/time anti-pattern scanner -- detects timezone bugs, naive datetime usage, hardcoded timestamps, non-ISO formats, incorrect epoch handling, DST-unsafe comparisons, and temporal anti-patterns"
homepage: https://dateguard.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udcc5",
      "primaryEnv": "DATEGUARD_LICENSE_KEY",
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

# DateGuard -- Date/Time Anti-Pattern Scanner

DateGuard scans codebases for date/time anti-patterns, timezone bugs, naive datetime usage, hardcoded timestamps, non-ISO formats, incorrect epoch handling, DST-unsafe comparisons, locale-dependent parsing, and temporal storage issues. It uses regex-based pattern matching against 90 date/time-specific patterns across 6 categories, lefthook for git hook integration, and produces markdown reports with actionable remediation guidance. 100% local. Zero telemetry.

## Commands

### Free Tier (No license required)

#### `dateguard scan [file|directory]`
One-shot date/time quality scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 30 date/time quality patterns against each file (free tier limit)
4. Calculates a date/time quality score (0-100) per file and overall
5. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
6. Outputs findings with: file, line number, check ID, severity, description, recommendation
7. Exit code 0 if score >= 70, exit code 1 if date/time quality is poor
8. Free tier limited to first 30 patterns (TZ + NF categories)

**Example usage scenarios:**
- "Scan my code for timezone issues" -> runs `dateguard scan .`
- "Check this file for date anti-patterns" -> runs `dateguard scan src/server.ts`
- "Find naive datetime usage" -> runs `dateguard scan src/`
- "Audit date/time handling in my project" -> runs `dateguard scan .`
- "Check for DST-unsafe date math" -> runs `dateguard scan .`

### Pro Tier ($19/user/month -- requires DATEGUARD_LICENSE_KEY)

#### `dateguard scan --tier pro [file|directory]`
Extended scan with 60 patterns covering timezone, formatting, epoch precision, and date arithmetic.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier pro
```

**What it does:**
1. Validates Pro+ license
2. Runs 60 date/time patterns (TZ, NF, EP, DA categories)
3. Detects epoch precision bugs (ms vs seconds confusion)
4. Identifies DST-unsafe date arithmetic
5. Full category breakdown reporting

#### `dateguard scan --format json [directory]`
Generate JSON output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format json
```

#### `dateguard scan --format html [directory]`
Generate HTML report for browser viewing.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format html
```

#### `dateguard scan --category EP [directory]`
Filter scan to a specific check category (TZ, NF, EP, DA, CP, ST).

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --category EP
```

### Team Tier ($39/user/month -- requires DATEGUARD_LICENSE_KEY with team tier)

#### `dateguard scan --tier team [directory]`
Full scan with all 90 patterns across all 6 categories including comparison/parsing and storage/serialization.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --tier team
```

**What it does:**
1. Validates Team+ license
2. Runs all 90 patterns across 6 categories
3. Includes comparison/parsing checks (string date comparison, == on Date objects)
4. Includes storage/serialization checks (VARCHAR for dates, missing timezone in DB)
5. Full category breakdown with per-file results

#### `dateguard scan --verbose [directory]`
Verbose output showing every matched line and pattern details.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --verbose
```

#### `dateguard status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" status
```

## Check Categories

DateGuard detects 90 date/time anti-patterns across 6 categories:

| Category | Code | Patterns | Description | Severity Range |
|----------|------|----------|-------------|----------------|
| **Timezone Handling** | TZ | 15 | Missing timezone in datetime creation, implicit local timezone, hardcoded offsets, timezone conversion without DST handling | medium -- high |
| **Naive Formatting** | NF | 15 | Non-ISO date formats in APIs, locale-dependent parsing, ambiguous MM/DD vs DD/MM, toString() on dates | low -- high |
| **Epoch & Precision** | EP | 15 | Millisecond vs second confusion, Y2038 risk, timestamps as strings, floating point timestamps, epoch 0 sentinels | low -- medium |
| **Date Arithmetic** | DA | 15 | Manual +86400 day math, month arithmetic ignoring varying lengths, leap year bugs, DST-crossing calculations | medium -- high |
| **Comparison & Parsing** | CP | 15 | Lexicographic date string comparison, Date == comparison, unparsed user input, timezone-unaware comparisons | medium -- high |
| **Storage & Serialization** | ST | 15 | VARCHAR for timestamps in SQL, missing timezone in stored dates, JSON.stringify on Date, hardcoded date strings | low -- high |

## Tier-Based Pattern Access

| Tier | Patterns | Categories |
|------|----------|------------|
| **Free** | 30 | TZ, NF |
| **Pro** | 60 | TZ, NF, EP, DA |
| **Team** | 90 | TZ, NF, EP, DA, CP, ST |
| **Enterprise** | 90 | TZ, NF, EP, DA, CP, ST + priority support |

## Scoring

DateGuard uses a deductive scoring system starting at 100 (perfect):

| Severity | Point Deduction | Description |
|----------|-----------------|-------------|
| **Critical** | -25 per finding | Severe temporal bug (Y2038, data loss from timezone) |
| **High** | -15 per finding | Significant quality problem (naive datetime, DST math) |
| **Medium** | -8 per finding | Moderate concern (ambiguous formats, missing timezone) |
| **Low** | -3 per finding | Informational / best practice suggestion |

### Grading Scale

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| **A** | 90-100 | Excellent date/time handling |
| **B** | 80-89 | Good handling with minor issues |
| **C** | 70-79 | Acceptable but needs improvement |
| **D** | 60-69 | Poor date/time quality |
| **F** | Below 60 | Critical temporal problems |

- **Pass threshold:** 70 (Grade C or better)
- Exit code 0 = pass (score >= 70)
- Exit code 1 = fail (score < 70)

## Configuration

Users can configure DateGuard in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "dateguard": {
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
- If license key is invalid or expired, show clear message with link to https://dateguard.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If an invalid category is specified with --category, show available categories

## When to Use DateGuard

The user might say things like:
- "Scan my code for timezone issues"
- "Check my date/time handling"
- "Find naive datetime usage"
- "Detect DST-unsafe date math"
- "Are there any hardcoded timestamps?"
- "Check for missing timezone handling"
- "Audit my date/time practices"
- "Find ambiguous date formats"
- "Check for epoch precision bugs"
- "Scan for date/time anti-patterns"
- "Run a date/time quality audit"
- "Generate a date/time quality report"
- "Check if dates are stored properly in my database schema"
- "Find Date objects compared with == instead of getTime()"
- "Check my code for Y2038 risks"
