---
name: CacheLint
version: 1.0.0
description: "Caching anti-pattern analyzer -- detects Redis/Memcached misuse, TTL problems, cache invalidation failures, stampedes, architecture issues, and security hygiene gaps in application-level caching"
homepage: https://cachelint.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\uddc4\ufe0f",
      "primaryEnv": "CACHELINT_LICENSE_KEY",
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

# CacheLint -- Caching Anti-Pattern Analyzer

CacheLint scans codebases for application-level caching anti-patterns: Redis/Memcached misuse, missing cache invalidation after writes, TTL problems, cache stampede risks, architecture issues, and security hygiene gaps. It uses regex-based pattern matching against 90 caching-specific patterns across 6 categories, lefthook for git hook integration, and produces markdown reports with actionable remediation guidance. 100% local. Zero telemetry.

**Note:** CacheLint focuses on application-level caching (Redis calls, Memcached operations, local cache usage, invalidation logic, TTL management). It does NOT analyze HTTP cache headers.

## Commands

### Free Tier (No license required)

#### `cachelint scan [file|directory]`
One-shot caching quality scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 30 caching patterns against each file (free tier limit)
4. Calculates a caching quality score (0-100) per file and overall
5. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
6. Outputs findings with: file, line number, check ID, severity, description, recommendation
7. Exit code 0 if score >= 70, exit code 1 if caching quality is poor
8. Free tier limited to first 30 patterns (CI + TE categories)

**Example usage scenarios:**
- "Scan my code for caching issues" -> runs `cachelint scan .`
- "Check this file for cache anti-patterns" -> runs `cachelint scan src/cache-service.ts`
- "Find missing cache invalidation" -> runs `cachelint scan src/`
- "Audit cache TTL settings" -> runs `cachelint scan .`
- "Check for Redis misuse" -> runs `cachelint scan .`

### Pro Tier ($19/user/month -- requires CACHELINT_LICENSE_KEY)

#### `cachelint scan --tier pro [file|directory]`
Extended scan with 60 patterns covering invalidation, TTL, stampede, and Redis misuse.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier pro
```

**What it does:**
1. Validates Pro+ license
2. Runs 60 caching patterns (CI, TE, CS, RM categories)
3. Detects cache stampede risks and Redis anti-patterns
4. Identifies KEYS * usage, missing pipelines, unbounded lists
5. Full category breakdown reporting

#### `cachelint scan --format json [directory]`
Generate JSON output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format json
```

#### `cachelint scan --format html [directory]`
Generate HTML report for browser viewing.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format html
```

#### `cachelint scan --category CS [directory]`
Filter scan to a specific check category (CI, TE, CS, RM, CA, SH).

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --category CS
```

### Team Tier ($39/user/month -- requires CACHELINT_LICENSE_KEY with team tier)

#### `cachelint scan --tier team [directory]`
Full scan with all 90 patterns across all 6 categories including architecture and security.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --tier team
```

**What it does:**
1. Validates Team+ license
2. Runs all 90 patterns across 6 categories
3. Includes cache architecture checks (N+1 gets, mixed strategies, no abstraction)
4. Includes security & hygiene (PII in keys, missing TLS, no encryption)
5. Full category breakdown with per-file results

#### `cachelint scan --verbose [directory]`
Verbose output showing every matched line and pattern details.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --verbose
```

#### `cachelint status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" status
```

## Check Categories

CacheLint detects 90 caching anti-patterns across 6 categories:

| Category | Code | Patterns | Description | Severity Range |
|----------|------|----------|-------------|----------------|
| **Cache Invalidation** | CI | 15 | Missing invalidation after writes, stale data, wrong write ordering | medium -- critical |
| **TTL & Expiry** | TE | 15 | Missing TTL, infinite cache, no jitter, hardcoded magic numbers | low -- high |
| **Cache Stampede** | CS | 15 | No lock on miss, thundering herd, missing singleflight, no stale-while-revalidate | low -- critical |
| **Redis/Store Misuse** | RM | 15 | KEYS *, FLUSHALL, no pipeline, missing pooling, synchronous calls | low -- critical |
| **Cache Architecture** | CA | 15 | N+1 gets, no abstraction, mixed strategies, no error fallback | low -- high |
| **Security & Hygiene** | SH | 15 | PII in keys, no TLS, missing encryption, no monitoring, key injection | low -- critical |

## Tier-Based Pattern Access

| Tier | Patterns | Categories |
|------|----------|------------|
| **Free** | 30 | CI, TE |
| **Pro** | 60 | CI, TE, CS, RM |
| **Team** | 90 | CI, TE, CS, RM, CA, SH |
| **Enterprise** | 90 | CI, TE, CS, RM, CA, SH + priority support |

## Scoring

CacheLint uses a deductive scoring system starting at 100 (perfect):

| Severity | Point Deduction | Description |
|----------|-----------------|-------------|
| **Critical** | -25 per finding | Severe risk (stampede, KEYS *, FLUSHALL, wrong write order) |
| **High** | -15 per finding | Significant problem (missing invalidation, no TTL, N+1 gets) |
| **Medium** | -8 per finding | Moderate concern (no jitter, missing pooling, mixed strategies) |
| **Low** | -3 per finding | Informational / best practice suggestion |

### Grading Scale

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| **A** | 90-100 | Excellent caching quality |
| **B** | 80-89 | Good caching with minor issues |
| **C** | 70-79 | Acceptable but needs improvement |
| **D** | 60-69 | Poor caching quality |
| **F** | Below 60 | Critical caching problems |

- **Pass threshold:** 70 (Grade C or better)
- Exit code 0 = pass (score >= 70)
- Exit code 1 = fail (score < 70)

## Configuration

Users can configure CacheLint in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "cachelint": {
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
- If license key is invalid or expired, show clear message with link to https://cachelint.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If an invalid category is specified with --category, show available categories

## When to Use CacheLint

The user might say things like:
- "Scan my code for caching issues"
- "Check my cache invalidation logic"
- "Find missing TTL on cache entries"
- "Detect cache stampede risks"
- "Are there any Redis anti-patterns?"
- "Check for KEYS * usage in production code"
- "Audit my caching architecture"
- "Find security issues in cache usage"
- "Check for PII in cache keys"
- "Scan for missing cache invalidation"
- "Run a caching quality audit"
- "Generate a cache health report"
- "Check if my Redis calls use pipelines"
- "Find N+1 cache get patterns"
- "Check my code for cache stampede vulnerabilities"
