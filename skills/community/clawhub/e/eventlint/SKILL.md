---
name: EventLint
version: 1.0.0
description: "Event & message queue anti-pattern analyzer -- detects producer/consumer issues, schema problems, dead letter queue gaps, ordering failures, and observability gaps in event-driven architectures (Kafka, RabbitMQ, SQS, NATS, Redis Pub/Sub)"
homepage: https://eventlint.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udce8",
      "primaryEnv": "EVENTLINT_LICENSE_KEY",
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

# EventLint -- Event & Message Queue Anti-Pattern Analyzer

EventLint scans codebases for event-driven architecture anti-patterns, producer/consumer issues, schema validation gaps, dead letter queue misconfigurations, ordering and delivery failures, and observability gaps across Kafka, RabbitMQ, SQS, NATS, and Redis Pub/Sub. It uses regex-based pattern matching against 90 event-specific patterns across 6 categories, lefthook for git hook integration, and produces markdown reports with actionable remediation guidance. 100% local. Zero telemetry.

## Commands

### Free Tier (No license required)

#### `eventlint scan [file|directory]`
One-shot event architecture quality scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 30 event architecture patterns against each file (free tier limit)
4. Calculates an event architecture quality score (0-100) per file and overall
5. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
6. Outputs findings with: file, line number, check ID, severity, description, recommendation
7. Exit code 0 if score >= 70, exit code 1 if event quality is poor
8. Free tier limited to first 30 patterns (PP + CP categories)

**Example usage scenarios:**
- "Scan my code for event issues" -> runs `eventlint scan .`
- "Check this file for consumer anti-patterns" -> runs `eventlint scan src/consumer.ts`
- "Find missing dead letter queues" -> runs `eventlint scan src/`
- "Audit my Kafka configuration" -> runs `eventlint scan .`
- "Check for message ordering problems" -> runs `eventlint scan .`

### Pro Tier ($19/user/month -- requires EVENTLINT_LICENSE_KEY)

#### `eventlint scan --tier pro [file|directory]`
Extended scan with 60 patterns covering producer, consumer, schema, and dead letter patterns.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier pro
```

**What it does:**
1. Validates Pro+ license
2. Runs 60 event architecture patterns (PP, CP, MS, ED categories)
3. Detects schema validation gaps and breaking changes
4. Identifies dead letter queue misconfigurations
5. Full category breakdown reporting

#### `eventlint scan --format json [directory]`
Generate JSON output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format json
```

#### `eventlint scan --format html [directory]`
Generate HTML report for browser viewing.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format html
```

#### `eventlint scan --category ED [directory]`
Filter scan to a specific check category (PP, CP, MS, ED, OD, EO).

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --category ED
```

### Team Tier ($39/user/month -- requires EVENTLINT_LICENSE_KEY with team tier)

#### `eventlint scan --tier team [directory]`
Full scan with all 90 patterns across all 6 categories including ordering/delivery and observability.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --tier team
```

**What it does:**
1. Validates Team+ license
2. Runs all 90 patterns across 6 categories
3. Includes ordering & delivery detection (dual-write, missing outbox, race conditions)
4. Includes event observability checks (no tracing, missing metrics, no audit trail)
5. Full category breakdown with per-file results

#### `eventlint scan --verbose [directory]`
Verbose output showing every matched line and pattern details.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --verbose
```

#### `eventlint status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" status
```

## Check Categories

EventLint detects 90 event architecture anti-patterns across 6 categories:

| Category | Code | Patterns | Description | Severity Range |
|----------|------|----------|-------------|----------------|
| **Producer Patterns** | PP | 15 | Fire-and-forget publish, missing keys, no schema validation, acks=0 | medium -- critical |
| **Consumer Patterns** | CP | 15 | No idempotency, auto-ack, unbounded prefetch, blocking handlers | low -- critical |
| **Message Schema** | MS | 15 | No schema registry, unversioned, breaking changes, loose typing | low -- critical |
| **Error & Dead Letter** | ED | 15 | Missing DLQ, infinite redelivery, swallowed exceptions, no poison handling | low -- critical |
| **Ordering & Delivery** | OD | 15 | Dual-write, no outbox, missing dedup, saga without timeout | low -- critical |
| **Event Observability** | EO | 15 | No tracing, missing metrics, no audit trail, no alerting | low -- medium |

## Tier-Based Pattern Access

| Tier | Patterns | Categories |
|------|----------|------------|
| **Free** | 30 | PP, CP |
| **Pro** | 60 | PP, CP, MS, ED |
| **Team** | 90 | PP, CP, MS, ED, OD, EO |
| **Enterprise** | 90 | PP, CP, MS, ED, OD, EO + priority support |

## Scoring

EventLint uses a deductive scoring system starting at 100 (perfect):

| Severity | Point Deduction | Description |
|----------|-----------------|-------------|
| **Critical** | -25 per finding | Severe reliability issue (message loss, infinite redelivery, dual-write) |
| **High** | -15 per finding | Significant event problem (missing DLQ, auto-ack, no idempotency) |
| **Medium** | -8 per finding | Moderate concern (missing correlation ID, unversioned schema) |
| **Low** | -3 per finding | Informational / best practice suggestion |

### Grading Scale

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| **A** | 90-100 | Excellent event architecture quality |
| **B** | 80-89 | Good architecture with minor issues |
| **C** | 70-79 | Acceptable but needs improvement |
| **D** | 60-69 | Poor event architecture quality |
| **F** | Below 60 | Critical event architecture problems |

- **Pass threshold:** 70 (Grade C or better)
- Exit code 0 = pass (score >= 70)
- Exit code 1 = fail (score < 70)

## Configuration

Users can configure EventLint in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "eventlint": {
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
- If license key is invalid or expired, show clear message with link to https://eventlint.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If an invalid category is specified with --category, show available categories

## When to Use EventLint

The user might say things like:
- "Scan my code for event issues"
- "Check my message queue patterns"
- "Find missing dead letter queues"
- "Detect fire-and-forget publishing"
- "Are there any consumer anti-patterns?"
- "Check for schema validation gaps"
- "Audit my Kafka configuration"
- "Find ordering and delivery issues"
- "Check for dual-write problems"
- "Scan for event observability gaps"
- "Run an event architecture audit"
- "Generate an event quality report"
- "Check if my consumers have idempotency"
- "Find missing DLQ configuration"
- "Check my code for auto-ack issues"
