# AuthAudit

<p align="center">
  <img src="https://img.shields.io/badge/patterns-90-blue" alt="90 security patterns">
  <img src="https://img.shields.io/badge/categories-6-purple" alt="6 check categories">
  <img src="https://img.shields.io/badge/license-COMMERCIAL-orange" alt="Commercial License">
  <img src="https://img.shields.io/badge/install-clawhub-blue" alt="ClawHub">
  <img src="https://img.shields.io/badge/zero-telemetry-brightgreen" alt="Zero telemetry">
</p>

<h3 align="center">Find authentication and authorization vulnerabilities before attackers do.</h3>

<p align="center">
  <a href="https://authaudit.dev">Website</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#check-categories">Check Categories</a> &middot;
  <a href="https://authaudit.dev/#pricing">Pricing</a>
</p>

---

## Your auth is broken. You just don't know it yet.

A route handler missing `@login_required`. A JWT stored in `localStorage`. A session that never expires. An admin endpoint checking `role === "admin"` with a hardcoded string. A password compared with `===` instead of a timing-safe function.

These are the vulnerabilities that code reviews miss and penetration testers charge thousands to find. By then the endpoint is live and your users' data is exposed.

**AuthAudit scans your codebase for 90 authentication and authorization vulnerabilities across 6 categories. Locally. Before you commit.**

## Quick Start

```bash
# Install via ClawHub (free)
clawhub install authaudit

# Scan your codebase for auth issues
authaudit scan

# Scan a specific directory
authaudit scan src/

# Scan a single file
authaudit scan app/middleware/auth.js

# Scan a specific category only
authaudit scan --category AC

# Output as JSON for CI/CD
authaudit scan --format json

# Install pre-commit hooks (Pro)
authaudit hooks install

# Generate a security report (Pro)
authaudit report

# Verbose output for debugging
authaudit scan --verbose
```

## Check Categories

AuthAudit runs 90 security patterns organized into 6 categories:

### AC -- Authentication Checks (15 patterns)

| Check ID | Description | Severity |
|----------|-------------|----------|
| AC-001 | Route handler without auth middleware | Critical |
| AC-002 | Express/FastAPI endpoint missing auth | Critical |
| AC-003 | Auth decorator bypassed or skipped | Critical |
| AC-004 | Anonymous access enabled on sensitive endpoint | High |
| AC-005 | Authentication disabled in configuration | Critical |
| AC-006 | Missing auth on admin/internal routes | Critical |
| AC-007 | Public endpoint returning sensitive data | High |
| AC-008 | Missing authentication on file upload | High |
| AC-009 | API key authentication without rotation | Medium |
| AC-010 | Basic auth over non-HTTPS | High |
| AC-011 | Auth check after sensitive operation | Medium |
| AC-012 | Optional auth on sensitive resource | Medium |
| AC-013 | Missing MFA enforcement | Low |
| AC-014 | Authentication bypass via parameter | Medium |
| AC-015 | Catch-all route without auth | Low |

### SM -- Session Management (15 patterns)

| Check ID | Description | Severity |
|----------|-------------|----------|
| SM-001 | Session cookie missing Secure flag | High |
| SM-002 | Session cookie missing HttpOnly flag | High |
| SM-003 | Session without expiry/maxAge | Critical |
| SM-004 | No session regeneration after login | High |
| SM-005 | Predictable session ID generation | Critical |
| SM-006 | Session data stored in localStorage | High |
| SM-007 | Session fixation vulnerability | Critical |
| SM-008 | Overly long session lifetime | Medium |
| SM-009 | Missing session invalidation on logout | High |
| SM-010 | Session stored in URL parameters | Critical |
| SM-011 | Missing idle session timeout | Medium |
| SM-012 | Session secret too short or hardcoded | High |
| SM-013 | Concurrent session not limited | Low |
| SM-014 | Session cookie missing SameSite flag | Medium |
| SM-015 | Session data not encrypted | Low |

### AZ -- Authorization/Access Control (15 patterns)

| Check ID | Description | Severity |
|----------|-------------|----------|
| AZ-001 | Missing role/permission check | Critical |
| AZ-002 | Insecure direct object reference (IDOR) | Critical |
| AZ-003 | Hardcoded admin/role check | High |
| AZ-004 | Missing object-level authorization | Critical |
| AZ-005 | Privilege escalation via parameter | High |
| AZ-006 | Missing function-level authorization | High |
| AZ-007 | Horizontal access control bypass | High |
| AZ-008 | Overly permissive wildcard permissions | Medium |
| AZ-009 | Authorization check client-side only | Critical |
| AZ-010 | Missing ownership verification | High |
| AZ-011 | Role assigned without validation | Medium |
| AZ-012 | Disabled authorization middleware | Critical |
| AZ-013 | Mass assignment without field filter | Medium |
| AZ-014 | Path traversal in authorized resource | Medium |
| AZ-015 | Default open access policy | Low |

### TK -- Token Handling (15 patterns)

| Check ID | Description | Severity |
|----------|-------------|----------|
| TK-001 | JWT stored in localStorage | High |
| TK-002 | Token in URL query parameter | Critical |
| TK-003 | JWT with algorithm "none" | Critical |
| TK-004 | Weak JWT signing secret | High |
| TK-005 | Missing token expiry validation | High |
| TK-006 | Token not rotated on refresh | Medium |
| TK-007 | Token logged to console/file | High |
| TK-008 | Missing JWT audience validation | Medium |
| TK-009 | Missing JWT issuer validation | Medium |
| TK-010 | Hardcoded JWT secret key | Critical |
| TK-011 | Token transmitted over HTTP | High |
| TK-012 | Symmetric signing for distributed system | Medium |
| TK-013 | Missing token revocation check | Low |
| TK-014 | Refresh token stored insecurely | High |
| TK-015 | Token scope not validated | Low |

### CS -- CSRF Protection (15 patterns)

| Check ID | Description | Severity |
|----------|-------------|----------|
| CS-001 | CSRF protection explicitly disabled | Critical |
| CS-002 | Missing CSRF token on form | High |
| CS-003 | State-changing GET endpoint | High |
| CS-004 | Missing SameSite cookie attribute | Medium |
| CS-005 | Missing Origin/Referer validation | High |
| CS-006 | CORS with wildcard origin and credentials | Critical |
| CS-007 | GET endpoint with database write | High |
| CS-008 | Missing CSRF middleware | High |
| CS-009 | CSRF token in URL parameter | Medium |
| CS-010 | Custom header check missing | Medium |
| CS-011 | SameSite set to None without Secure | High |
| CS-012 | Form action to external domain | Medium |
| CS-013 | Missing anti-CSRF for AJAX | Low |
| CS-014 | CORS allows all origins | High |
| CS-015 | Preflight request misconfigured | Low |

### PW -- Password & Credential Management (15 patterns)

| Check ID | Description | Severity |
|----------|-------------|----------|
| PW-001 | Password compared with equality operator | Critical |
| PW-002 | Plaintext password storage | Critical |
| PW-003 | Missing bcrypt/argon2/scrypt hashing | High |
| PW-004 | Password in URL query string | Critical |
| PW-005 | Hardcoded password/credential | Critical |
| PW-006 | Weak password length requirement | High |
| PW-007 | No rate limiting on login endpoint | High |
| PW-008 | Password logged to console/file | Critical |
| PW-009 | Credential in environment variable file | High |
| PW-010 | Missing password complexity validation | Medium |
| PW-011 | Insecure password reset token | High |
| PW-012 | Password reset without expiry | Medium |
| PW-013 | Credential in source code comment | Medium |
| PW-014 | MD5/SHA1 used for password hashing | High |
| PW-015 | Password displayed in UI/response | Low |

## Scoring

AuthAudit calculates a security score from 0 to 100:

- **Starting score:** 100
- **Critical finding:** -25 points each
- **High finding:** -15 points each
- **Medium finding:** -8 points each
- **Low finding:** -3 points each

Penalties are scaled relative to codebase size to avoid punishing large projects.

### Grades

| Grade | Score Range | CI/CD Result |
|-------|-------------|--------------|
| **A** | 90 -- 100 | Pass |
| **B** | 80 -- 89 | Pass |
| **C** | 70 -- 79 | Pass |
| **D** | 60 -- 69 | Fail |
| **F** | 0 -- 59 | Fail |

Pass threshold: **70** (configurable)

## Pricing

| Feature | Free | Pro ($19/mo) | Team ($39/mo) | Enterprise |
|---------|:----:|:------------:|:-------------:|:----------:|
| Auth patterns | 30 | 60 | 90 | 90 |
| 6 check categories | Partial | Extended | Full | Full |
| Security score + grade | Yes | Yes | Yes | Yes |
| Remediation advice | Yes | Yes | Yes | Yes |
| JSON output | Yes | Yes | Yes | Yes |
| Pre-commit hooks | | Yes | Yes | Yes |
| Security audit report | | Yes | Yes | Yes |
| HTML reports | | | Yes | Yes |
| All 90 patterns | | | Yes | Yes |

## Commands

### Free Tier (no license required)

| Command | Description |
|---------|-------------|
| `authaudit scan [target]` | Auth audit (30 patterns) |
| `authaudit scan --category AC` | Scan specific category |
| `authaudit scan --format json` | JSON output for CI/CD |
| `authaudit --help` | Show help |
| `authaudit --version` | Show version |

### Pro Tier ($19/user/month)

| Command | Description |
|---------|-------------|
| `authaudit scan [target]` | Extended audit (60 patterns) |
| `authaudit hooks install` | Install pre-commit hooks |
| `authaudit hooks uninstall` | Remove AuthAudit hooks |
| `authaudit report [dir]` | Generate markdown report |

### Team Tier ($39/user/month)

| Command | Description |
|---------|-------------|
| `authaudit scan [target]` | Complete audit (all 90 patterns) |
| `authaudit scan --format html` | HTML report with filtering |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "authaudit": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
        "config": {
          "severityThreshold": "medium",
          "excludePatterns": ["**/node_modules/**", "**/dist/**"],
          "reportFormat": "text",
          "categories": ["AC", "SM", "AZ", "TK", "CS", "PW"]
        }
      }
    }
  }
}
```

Or set the environment variable:

```bash
export AUTHAUDIT_LICENSE_KEY="your-key-here"
```

## CLI Options

| Flag | Description | Default |
|------|-------------|---------|
| `--path <dir>` | Target directory or file | `.` (current directory) |
| `--format <fmt>` | Output format: text, json, html | `text` |
| `--tier <tier>` | Override tier detection | auto-detect from license |
| `--license-key <key>` | Provide license key inline | env/config |
| `--verbose` | Show detailed scan progress | `false` |
| `--category <cat>` | Scan specific category only | all categories |

## Exit Codes

- `0` -- Pass (score >= 70)
- `1` -- Fail (score < 70)

Designed for CI/CD integration. Combine with `--format json` for machine-readable output.

## Privacy

- 100% local -- no code or scan data sent externally
- Zero telemetry
- Offline license validation (JWT-based)
- Pattern matching only -- no AST parsing or code execution

## How It Compares

| Feature | AuthAudit | Semgrep Pro ($40/dev) | SonarQube ($150/yr) | Bearer ($0) |
|---------|:---------:|:---------------------:|:-------------------:|:-----------:|
| Auth-focused patterns | 90 | ~30 auth rules | ~20 auth rules | ~15 auth |
| Offline/local only | Yes | Cloud required | Self-host option | Yes |
| Zero config setup | Yes | Config required | Complex setup | Config required |
| Pre-commit hooks | Yes | Yes | No | Yes |
| CSRF detection | 15 patterns | ~5 rules | ~3 rules | ~2 rules |
| Token security | 15 patterns | ~8 rules | ~5 rules | ~3 rules |
| Session audit | 15 patterns | ~5 rules | ~8 rules | ~2 rules |
| Auth-specific scoring | Yes | No | No | No |
| Setup time | 30 seconds | 15+ minutes | 60+ minutes | 10+ minutes |
| Price (individual) | Free/$19/mo | $40/dev/mo | $150/yr | Free (limited) |

## Part of the ClawHub Ecosystem

AuthAudit is built for [ClawHub](https://openclaw.dev), the marketplace for developer tools that plug into your CLI. Other skills in the ecosystem:

- **[APIShield](https://apishield.pages.dev)** -- API endpoint security auditor
- **[SecretScan](https://secretscan.dev)** -- Pre-commit secret detection
- **[SQLGuard](https://sqlguard.dev)** -- SQL injection and query safety
- **[DepGuard](https://depguard.pages.dev)** -- Dependency audit and vulnerability scanning
- **[EnvGuard](https://envguard.pages.dev)** -- Environment variable safety

## Contributing

AuthAudit is a commercial product. To report bugs or suggest new patterns:

1. Open an issue at [github.com/clawhub/authaudit](https://github.com/clawhub/authaudit)
2. Include the pattern category, a code sample that should trigger, and expected severity
3. For false positive reports, include the file contents and the pattern ID

## License

Commercial -- see [LICENSE](LICENSE) for terms.

Free tier available with no license key required (30 patterns).
Pro/Team/Enterprise tiers require a valid license key from [authaudit.dev](https://authaudit.dev).
