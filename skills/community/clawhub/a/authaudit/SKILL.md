---
name: AuthAudit
version: 1.0.0
description: "Authentication & authorization pattern analyzer — finds missing auth checks, insecure sessions, broken access control, CSRF gaps, and token handling vulnerabilities"
author: ClawHub
tags: [authentication, authorization, access-control, csrf, session-security, tokens]
license: COMMERCIAL
triggers:
  - "authaudit scan"
  - "authaudit check"
  - "authaudit audit"
tools: [Bash, Read, Glob, Grep]
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udd10",
      "primaryEnv": "AUTHAUDIT_LICENSE_KEY",
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

# AuthAudit -- Authentication & Authorization Pattern Analyzer

AuthAudit scans your codebase for authentication and authorization vulnerabilities including missing auth checks, insecure session handling, broken access control, CSRF gaps, token storage issues, and credential management weaknesses. It supports JavaScript/TypeScript, Python, Ruby, Go, Java, and PHP codebases. All scanning happens locally using regex-based pattern matching -- no code is sent to external servers.

## Check Categories

AuthAudit organizes its 90 security patterns into 6 categories:

### 1. AC -- Authentication Checks (15 patterns)
Detects missing authentication middleware, unprotected routes, bypassed login checks, missing auth decorators, unauthenticated API endpoints, disabled authentication, anonymous access to sensitive resources, and missing multi-factor authentication enforcement.

### 2. SM -- Session Management (15 patterns)
Finds insecure session configuration, missing session expiry, absent session rotation on privilege changes, predictable session IDs, session fixation vulnerabilities, missing Secure/HttpOnly cookie flags, overly long session lifetimes, and sessions stored in insecure locations.

### 3. AZ -- Authorization/Access Control (15 patterns)
Identifies missing role checks, broken object-level authorization (BOLA), insecure direct object references (IDOR), missing permission verification, privilege escalation paths, hardcoded admin roles, missing function-level authorization, and horizontal access control bypasses.

### 4. TK -- Token Handling (15 patterns)
Catches JWT stored in localStorage, tokens transmitted in URL parameters, missing token expiry validation, absent token refresh rotation, weak signing algorithms (none/HS256 with secrets), token leakage in logs, missing audience/issuer validation, and insecure token generation.

### 5. CS -- CSRF Protection (15 patterns)
Detects missing CSRF tokens on state-changing endpoints, absent SameSite cookie flag, GET requests performing side effects, missing Origin/Referer validation, state-changing GET endpoints, disabled CSRF middleware, CORS misconfigurations enabling CSRF, and missing double-submit cookie patterns.

### 6. PW -- Password & Credential Management (15 patterns)
Finds weak password requirements, plaintext password comparison, missing bcrypt/argon2 hashing, absent rate limiting on login endpoints, passwords in query strings, hardcoded credentials, insecure password reset tokens, missing password complexity enforcement, and credential logging.

## Severity Levels

Each finding is classified by severity:

| Severity | Weight | Description |
|----------|--------|-------------|
| **Critical** | 25 points | Active vulnerability that can be immediately exploited |
| **High** | 15 points | Significant security weakness requiring prompt attention |
| **Medium** | 8 points | Security concern to address in upcoming sprints |
| **Low** | 3 points | Best-practice improvement or informational finding |

## Scoring System

AuthAudit calculates a security score from 0 to 100:

- **Starting score:** 100
- **Deductions:** Each finding subtracts points based on severity weight
- **Scaling:** Penalties are scaled relative to codebase size (more files = smaller per-issue impact)
- **Pass threshold:** 70 (score >= 70 = pass, score < 70 = fail)

### Grades

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| **A** | 90 -- 100 | Excellent auth posture |
| **B** | 80 -- 89 | Good, minor improvements needed |
| **C** | 70 -- 79 | Acceptable, several issues to fix |
| **D** | 60 -- 69 | Below threshold, significant concerns |
| **F** | 0 -- 59 | Critical auth vulnerabilities present |

## Commands

### Free Tier (No license required)

#### `authaudit scan [file|directory]`
One-shot authentication and authorization audit of source files.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Finds all source files (excluding .git/, node_modules/, dist/, build/, vendor/, __pycache__)
3. Runs the first 30 auth/authz patterns against each file (free tier limit)
4. Outputs findings with: file, line number, check ID, severity, description, recommendation
5. Calculates a security score (0-100) with letter grade
6. Free tier: limited to 30 of 90 patterns
7. Exit code 0 if score >= 70, exit code 1 if score < 70

**Example usage scenarios:**
- "Scan my code for auth vulnerabilities" -> runs `authaudit scan .`
- "Check for missing authentication" -> runs `authaudit scan src/`
- "Audit my session handling" -> runs `authaudit scan .`
- "Find CSRF vulnerabilities" -> runs `authaudit scan .`
- "Check token security" -> runs `authaudit scan .`

#### `authaudit scan [file|directory] --category AC`
Scan only a specific category.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --category AC
```

#### `authaudit scan [file|directory] --format json`
Output results in JSON format for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --format json
```

### Pro Tier ($19/user/month -- requires AUTHAUDIT_LICENSE_KEY)

#### `authaudit scan [file|directory]` (60 patterns)
Full security audit with 60 patterns enabled (free + pro patterns).

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does (beyond free):**
1. Runs 60 of 90 patterns (all free + pro-tier patterns)
2. Includes advanced session management, token handling, and credential checks
3. Detailed remediation advice per finding
4. HTML report output support

#### `authaudit hooks install`
Install git pre-commit hooks that scan staged files for auth issues before every commit.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" hooks install
```

#### `authaudit hooks uninstall`
Remove AuthAudit git hooks.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" hooks uninstall
```

#### `authaudit report [directory]`
Generate a markdown security audit report.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" report [directory]
```

### Team/Enterprise Tier ($39/user/month -- requires AUTHAUDIT_LICENSE_KEY with team tier)

#### `authaudit scan [file|directory]` (all 90 patterns)
Complete audit with all 90 patterns across all 6 categories.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

#### `authaudit scan [file|directory] --format html`
HTML report with interactive severity filtering.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --format html
```

## Tier-Based Pattern Access

| Tier | Patterns Available | Categories |
|------|-------------------|------------|
| **Free** | 30 (first 5 per category) | AC, SM, AZ, TK, CS, PW |
| **Pro** | 60 (first 10 per category) | AC, SM, AZ, TK, CS, PW |
| **Team** | 90 (all patterns) | AC, SM, AZ, TK, CS, PW |
| **Enterprise** | 90 (all patterns) | AC, SM, AZ, TK, CS, PW |

## Output Formats

- **text** (default) -- Human-readable terminal output with colors and severity icons
- **json** -- Machine-readable JSON for CI/CD pipelines and tooling integration
- **html** -- Self-contained HTML report with severity filtering (Team+)

## Configuration

Users can configure AuthAudit in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "authaudit": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "medium",
          "excludePatterns": ["**/node_modules/**", "**/dist/**", "**/.git/**"],
          "reportFormat": "text",
          "categories": ["AC", "SM", "AZ", "TK", "CS", "PW"]
        }
      }
    }
  }
}
```

## Important Notes

- **Free tier** works immediately with no configuration (30 patterns)
- **All scanning happens locally** -- no code is sent to external servers
- **License validation is offline** -- no phone-home or network calls
- Supports JS/TS, Python, Ruby, Go, Java, and PHP codebases
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = pass (score >= 70), 1 = fail (score < 70 or critical issues)

## Error Handling

- If lefthook is not installed and user tries `hooks install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://authaudit.dev/renew
- If a file is binary, skip it automatically with no warning
- If no source files found in target, report clean scan with info message
- If an invalid category is specified, list valid categories and exit

## When to Use AuthAudit

The user might say things like:
- "Scan my code for authentication issues"
- "Check if my routes have auth middleware"
- "Find missing authorization checks"
- "Audit my session handling"
- "Check for CSRF vulnerabilities"
- "Find insecure token storage"
- "Check for hardcoded credentials"
- "Audit my password handling"
- "Find privilege escalation paths"
- "Check for broken access control"
- "Scan for insecure session configuration"
- "Find JWT vulnerabilities in my code"
- "Check my login flow for security issues"
- "Audit auth patterns in my codebase"
