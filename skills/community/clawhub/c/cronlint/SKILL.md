---
name: CronLint
version: 1.0.0
description: "Scheduled task & cron job anti-pattern analyzer -- detects overlapping execution risks, timezone scheduling errors, missing error recovery, resource contention, lifecycle management issues, and observability gaps in cron jobs, schedulers, and periodic task code"
homepage: https://cronlint.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\u23f0",
      "primaryEnv": "CRONLINT_LICENSE_KEY",
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

# CronLint -- Scheduled Task & Cron Job Anti-Pattern Analyzer

CronLint scans codebases for scheduled task and cron job anti-patterns: overlapping execution risks, timezone scheduling errors, missing error recovery, resource contention, lifecycle management issues, and observability gaps. It uses regex-based pattern matching against 90 scheduling-specific patterns across 6 categories, lefthook for git hook integration, and produces markdown reports with actionable remediation guidance. 100% local. Zero telemetry.

**Note:** CronLint focuses on cron jobs, schedulers (node-cron, APScheduler, Quartz, Celery beat, Bull/BullMQ), setInterval/setTimeout scheduling, Kubernetes CronJobs, and periodic task code. It detects anti-patterns in scheduling logic, not HTTP cron endpoints.

## Commands

### Free Tier (No license required)

#### `cronlint scan [file|directory]`
One-shot scheduling quality scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 30 scheduling patterns against each file (free tier limit)
4. Calculates a scheduling quality score (0-100) per file and overall
5. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
6. Outputs findings with: file, line number, check ID, severity, description, recommendation
7. Exit code 0 if score >= 70, exit code 1 if scheduling quality is poor
8. Free tier limited to first 30 patterns (OE + TZ categories)

**Example usage scenarios:**
- "Scan my code for cron job issues" -> runs `cronlint scan .`
- "Check this file for scheduling anti-patterns" -> runs `cronlint scan src/scheduler.ts`
- "Find overlapping cron execution risks" -> runs `cronlint scan src/`
- "Audit timezone handling in scheduled tasks" -> runs `cronlint scan .`
- "Check for missing error handling in cron jobs" -> runs `cronlint scan .`

### Pro Tier ($19/user/month -- requires CRONLINT_LICENSE_KEY)

#### `cronlint scan --tier pro [file|directory]`
Extended scan with 60 patterns covering overlap, timezone, error recovery, and resource contention.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier pro
```

**What it does:**
1. Validates Pro+ license
2. Runs 60 scheduling patterns (OE, TZ, ER, RC categories)
3. Detects missing error recovery and retry logic in scheduled jobs
4. Identifies resource contention: every-minute crons, unbounded queries, no rate limiting
5. Full category breakdown reporting

#### `cronlint scan --format json [directory]`
Generate JSON output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format json
```

#### `cronlint scan --format html [directory]`
Generate HTML report for browser viewing.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format html
```

#### `cronlint scan --category OE [directory]`
Filter scan to a specific check category (OE, TZ, ER, RC, LM, OB).

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --category OE
```

### Team Tier ($39/user/month -- requires CRONLINT_LICENSE_KEY with team tier)

#### `cronlint scan --tier team [directory]`
Full scan with all 90 patterns across all 6 categories including lifecycle and observability.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --tier team
```

**What it does:**
1. Validates Team+ license
2. Runs all 90 patterns across 6 categories
3. Includes lifecycle management checks (graceful shutdown, orphaned tasks, stale entries)
4. Includes observability checks (missing metrics, no duration logging, no alerting)
5. Full category breakdown with per-file results

#### `cronlint scan --verbose [directory]`
Verbose output showing every matched line and pattern details.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --verbose
```

#### `cronlint status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" status
```

#### `cronlint patterns`
List all detection patterns with their IDs, severities, and descriptions.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" patterns
```

## Check Categories

CronLint detects 90 scheduled task anti-patterns across 6 categories:

| Category | Code | Patterns | Description | Severity Range |
|----------|------|----------|-------------|----------------|
| **Overlapping Execution** | OE | 15 | Missing locks, concurrent runs, no mutex, no pid file check | low -- critical |
| **Timezone & Scheduling** | TZ | 15 | Hardcoded TZ, DST risks, UTC confusion, midnight pitfalls | low -- high |
| **Error & Recovery** | ER | 15 | No try/catch, missing retry, silent failure, no dead letter queue | low -- critical |
| **Resource Contention** | RC | 15 | Every-minute cron, no rate limit, unbounded queries, memory risk | low -- critical |
| **Lifecycle Management** | LM | 15 | No graceful shutdown, orphaned tasks, stale entries, no health check | low -- high |
| **Observability** | OB | 15 | No duration logging, no metrics, no alerting, no execution history | low -- high |

## Tier-Based Pattern Access

| Tier | Patterns | Categories |
|------|----------|------------|
| **Free** | 30 | OE, TZ |
| **Pro** | 60 | OE, TZ, ER, RC |
| **Team** | 90 | OE, TZ, ER, RC, LM, OB |
| **Enterprise** | 90 | OE, TZ, ER, RC, LM, OB + priority support |

## Scoring

CronLint uses a deductive scoring system starting at 100 (perfect):

| Severity | Point Deduction | Description |
|----------|-----------------|-------------|
| **Critical** | -25 per finding | Severe risk (overlapping execution, silent failure, resource abuse) |
| **High** | -15 per finding | Significant problem (missing locks, DST scheduling, no error handling) |
| **Medium** | -8 per finding | Moderate concern (hardcoded TZ, missing retry, no rate limiting) |
| **Low** | -3 per finding | Informational / best practice suggestion |

### Grading Scale

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| **A** | 90-100 | Excellent scheduling quality |
| **B** | 80-89 | Good scheduling with minor issues |
| **C** | 70-79 | Acceptable but needs improvement |
| **D** | 60-69 | Poor scheduling quality |
| **F** | Below 60 | Critical scheduling problems |

- **Pass threshold:** 70 (Grade C or better)
- Exit code 0 = pass (score >= 70)
- Exit code 1 = fail (score < 70)

## Configuration

Users can configure CronLint in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "cronlint": {
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
- If license key is invalid or expired, show clear message with link to https://cronlint.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If an invalid category is specified with --category, show available categories

## When to Use CronLint

The user might say things like:
- "Scan my code for cron job issues"
- "Check my scheduled task logic"
- "Find overlapping execution risks"
- "Detect timezone problems in schedulers"
- "Are there any cron anti-patterns?"
- "Check for missing error handling in cron jobs"
- "Audit my scheduling architecture"
- "Find resource contention in batch jobs"
- "Check for missing job observability"
- "Scan for graceful shutdown issues"
- "Run a scheduling quality audit"
- "Generate a cron health report"
- "Check if my jobs have overlap protection"
- "Find silent failure patterns in scheduled tasks"
- "Check my code for DST scheduling vulnerabilities"
