---
name: apishield
description: API endpoint security auditor — scans route definitions for missing auth, rate limiting, CORS issues, and input validation holes
homepage: https://apishield.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udd12",
      "primaryEnv": "APISHIELD_LICENSE_KEY",
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

# APIShield -- API Endpoint Security Auditor

APIShield scans your API route definitions for security vulnerabilities including missing authentication middleware, rate limiting gaps, input validation holes, CORS misconfigurations, and exposed debug endpoints. It supports Express, FastAPI, Flask, Django, Rails, and Next.js. All scanning happens locally using regex-based pattern matching -- no code is sent to external servers.

## Commands

### Free Tier (No license required)

#### `apishield scan [file|directory]`
One-shot security audit of API route files.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/apishield.sh" scan [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Auto-detects the framework (Express, FastAPI, Flask, Django, Rails, Next.js)
3. Finds all route definition files (excluding .git/, node_modules/, dist/, build/, vendor/, __pycache__)
4. Runs 20+ security checks against each route file
5. Outputs findings with: file, line number, check name, severity, description
6. Calculates a security score (0-100)
7. Free tier: limited to scanning up to 5 route files
8. Exit code 0 if score >= 70, exit code 1 if score < 70 or critical issues found

**Example usage scenarios:**
- "Scan my API routes for security issues" -> runs `apishield scan .`
- "Check this Express app for missing auth" -> runs `apishield scan src/routes/`
- "Audit my FastAPI endpoints" -> runs `apishield scan app/`
- "Are my API endpoints secure?" -> runs `apishield scan .`

### Pro Tier ($19/user/month -- requires APISHIELD_LICENSE_KEY)

#### `apishield scan [file|directory]` (unlimited)
Full security audit with no file limit and all 20+ checks enabled.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/apishield.sh" scan [target]
```

**What it does (beyond free):**
1. Unlimited route file scanning
2. Full 20+ security checks including rate limit analysis, CORS validation, input validation, CSRF, SQL injection risk
3. Detailed remediation advice per finding

#### `apishield hooks install`
Install git pre-commit hooks that scan staged route files for security issues before every commit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/apishield.sh" hooks install
```

**What it does:**
1. Validates Pro+ license
2. Copies lefthook config to project root
3. Installs lefthook pre-commit hook
4. On every commit: scans staged route files (.js, .ts, .py, .rb) for security issues, blocks commit if critical issues found

#### `apishield hooks uninstall`
Remove APIShield git hooks.

```bash
bash "<SKILL_DIR>/scripts/apishield.sh" hooks uninstall
```

#### `apishield report [directory]`
Generate a markdown security audit report.

```bash
bash "<SKILL_DIR>/scripts/apishield.sh" report [directory]
```

**What it does:**
1. Validates Pro+ license
2. Runs full scan of the directory
3. Generates a formatted markdown report with severity breakdown
4. Includes per-endpoint findings, security score, and remediation steps
5. Output written to APISHIELD-REPORT.md

### Team Tier ($39/user/month -- requires APISHIELD_LICENSE_KEY with team tier)

#### `apishield inventory [directory]`
Generate a complete API endpoint inventory/catalog.

```bash
bash "<SKILL_DIR>/scripts/apishield.sh" inventory [directory]
```

**What it does:**
1. Validates Team+ license
2. Discovers all API endpoints across the codebase
3. Catalogs: HTTP method, path, framework, auth status, rate limiting, validation
4. Outputs a markdown table of all endpoints
5. Useful for API documentation and security reviews

#### `apishield compliance [directory]`
Map findings to OWASP Top 10 API Security Risks.

```bash
bash "<SKILL_DIR>/scripts/apishield.sh" compliance [directory]
```

**What it does:**
1. Validates Team+ license
2. Runs full security scan
3. Maps each finding to relevant OWASP API Security Top 10 categories
4. Produces a compliance report showing coverage and gaps
5. Categories: Broken Object-Level Auth, Broken Authentication, Excessive Data Exposure, Lack of Resources & Rate Limiting, Broken Function-Level Auth, Mass Assignment, Security Misconfiguration, Injection, Improper Asset Management, Insufficient Logging

## Detected Security Issues

APIShield checks for 20+ security issues across 6 frameworks:

| Check | Description | Severity |
|-------|-------------|----------|
| Missing Auth Middleware | Routes without authentication middleware | Critical |
| Debug Endpoints Exposed | /debug, /test, /admin without auth | Critical |
| SQL Injection Risk | String interpolation in SQL queries | Critical |
| Sensitive Data Exposure | Routes returning passwords/tokens/secrets | High |
| Missing Rate Limiting | Public endpoints without rate limit middleware | High |
| CORS Misconfiguration | Access-Control-Allow-Origin: * or overly permissive CORS | High |
| Missing Input Validation | Routes accepting req.body/params without validation | High |
| Missing CSRF Protection | State-changing endpoints without CSRF tokens | High |
| Overly Permissive Methods | app.all() or wildcard method handlers | Medium |
| Error Handling Leaks | Routes that might expose stack traces | Medium |
| Missing HTTP Security Headers | No helmet/security headers middleware | Medium |
| Insecure Direct Object Refs | Route params used directly in DB queries | Medium |

## Configuration

Users can configure APIShield in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "apishield": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "high",
          "excludePatterns": ["**/node_modules/**", "**/dist/**", "**/.git/**"],
          "reportFormat": "markdown"
        }
      }
    }
  }
}
```

## Important Notes

- **Free tier** works immediately with no configuration (limited to 5 route files)
- **All scanning happens locally** -- no code is sent to external servers
- **License validation is offline** -- no phone-home or network calls
- Supports Express, FastAPI, Flask, Django, Rails, and Next.js
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = secure (score >= 70), 1 = issues found (for CI/CD integration)

## Error Handling

- If lefthook is not installed and user tries `hooks install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://apishield.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no route files found in target, report clean scan with info message
- If framework cannot be auto-detected, try all framework patterns

## When to Use APIShield

The user might say things like:
- "Scan my API routes for security issues"
- "Check if my endpoints have authentication"
- "Are my Express routes secure?"
- "Audit my FastAPI endpoints for vulnerabilities"
- "Generate an API security report"
- "Check for CORS misconfigurations"
- "Find endpoints missing rate limiting"
- "Map my API security to OWASP Top 10"
- "Generate an API inventory"
- "Set up security checks on my commits"
- "Check for SQL injection risks in my routes"
- "Find debug endpoints that are exposed"
