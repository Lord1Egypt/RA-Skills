# apishield

<p align="center">
  <img src="https://img.shields.io/badge/checks-20+-blue" alt="20+ security checks">
  <img src="https://img.shields.io/badge/frameworks-6-purple" alt="6 frameworks">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/install-clawhub-blue" alt="ClawHub">
  <img src="https://img.shields.io/badge/zero-telemetry-brightgreen" alt="Zero telemetry">
</p>

<h3 align="center">Catch API security vulnerabilities before they reach production.</h3>

<p align="center">
  <a href="https://apishield.pages.dev">Website</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#supported-frameworks">Frameworks</a> &middot;
  <a href="https://apishield.pages.dev/#pricing">Pricing</a>
</p>

---

## Your API routes are exposed. You just don't know it yet.

Missing auth middleware on a single endpoint. A wildcard CORS config copy-pasted from a tutorial. An `/admin` route with no access control. A `req.body` used without validation.

These are the vulnerabilities that static analysis tools miss and penetration testers find. By then it's too late -- the endpoint is live.

**APIShield scans your route definitions for 20+ security issues across 6 frameworks. Locally. Before you commit.**

## Quick Start

```bash
# Install via ClawHub (free)
clawhub install apishield

# Scan your API routes
apishield scan

# Scan a specific directory
apishield scan src/routes/

# Scan a single file
apishield scan app/api/users/route.ts

# Install pre-commit hooks (Pro)
apishield hooks install

# Generate a security report (Pro)
apishield report

# Generate API endpoint inventory (Team)
apishield inventory

# Map findings to OWASP Top 10 (Team)
apishield compliance
```

## What It Catches

APIShield runs 20+ security checks against your route definitions:

| Check | Description | Severity |
|-------|-------------|----------|
| Missing Auth Middleware | Routes without authentication middleware | Critical |
| Debug Endpoints Exposed | /debug, /test, /admin without auth | Critical |
| SQL Injection Risk | String interpolation in SQL queries | Critical |
| SSL Verification Disabled | verify=False, rejectUnauthorized: false | Critical |
| Sensitive Data Exposure | Routes returning passwords/tokens/secrets | High |
| Missing Rate Limiting | Public endpoints without rate limit middleware | High |
| CORS Misconfiguration | Access-Control-Allow-Origin: * or open defaults | High |
| Missing Input Validation | Direct req.body/request.data without validation | High |
| Missing CSRF Protection | State-changing endpoints without CSRF tokens | High |
| Debug Mode Enabled | DEBUG=True in production code | High |
| Overly Permissive Methods | app.all() or wildcard method handlers | Medium |
| Error Handling Leaks | Stack traces sent to clients | Medium |
| Missing Security Headers | No helmet or security headers middleware | Medium |
| Insecure HTTP | HTTP URLs where HTTPS should be used | Medium |
| Hardcoded Tokens | Bearer tokens or API keys in source code | High |

## Supported Frameworks

| Framework | Language | Route Detection | Auth Checks | Rate Limit Checks | Validation Checks |
|-----------|----------|-----------------|-------------|--------------------|--------------------|
| **Express.js** | JavaScript/TypeScript | app.get/post/put/delete, router.* | passport, jwt, auth middleware | express-rate-limit | joi, zod, celebrate, express-validator |
| **FastAPI** | Python | @app.get/post, @router.* | Depends() auth | slowapi | Pydantic models |
| **Flask** | Python | @app.route | @login_required, @auth_required | flask-limiter | WTForms, marshmallow |
| **Django** | Python | urlpatterns, path() | @login_required, permission_classes | throttle_classes | DRF serializers |
| **Rails** | Ruby | resources, get/post | before_action :authenticate | rack-attack | strong_parameters |
| **Next.js** | TypeScript/JavaScript | export function GET/POST | getServerSession, auth() | @upstash/ratelimit | zod validation |

## How It Compares

| Feature | APIShield | StackHawk ($35/dev/mo) | Snyk API ($25/dev/mo) | OWASP ZAP ($0) |
|---------|:---------:|:----------------------:|:---------------------:|:--------------:|
| Local-only (no cloud) | Yes | No | No | Yes |
| Zero config setup | Yes | No | No | No |
| Route-level scanning | Yes | Runtime only | Runtime only | Runtime only |
| Pre-commit hooks | Yes | No | Yes | No |
| OWASP Top 10 mapping | Yes | Yes | Yes | Yes |
| No code upload required | Yes | No | No | Yes |
| API endpoint inventory | Yes | No | No | No |
| Offline license validation | Yes | N/A | N/A | N/A |
| Zero telemetry | Yes | No | No | Yes |
| ClawHub integration | Yes | No | No | No |
| Setup time | 30 seconds | 30+ minutes | 15+ minutes | 60+ minutes |
| Price (individual) | Free/$19/mo | $35/dev/mo | $25/dev/mo | Free (complex) |

## Pricing

| Feature | Free | Pro ($19/user/mo) | Team ($39/user/mo) |
|---------|:----:|:------------------:|:-------------------:|
| Security scan (20+ checks) | 5 files | Unlimited | Unlimited |
| 6 framework support | Yes | Yes | Yes |
| Security score + grade | Yes | Yes | Yes |
| Detailed remediation advice | Yes | Yes | Yes |
| Pre-commit hooks | | Yes | Yes |
| Security audit report | | Yes | Yes |
| API endpoint inventory | | | Yes |
| OWASP Top 10 compliance | | | Yes |

## Commands

### Free Tier (no license required)

| Command | Description |
|---------|-------------|
| `apishield scan [target]` | Security audit (up to 5 route files) |
| `apishield status` | Show license and config info |
| `apishield help` | Show help |

### Pro Tier ($19/user/month)

| Command | Description |
|---------|-------------|
| `apishield scan [target]` | Unlimited route file scanning |
| `apishield hooks install` | Install pre-commit security hooks |
| `apishield hooks uninstall` | Remove APIShield hooks |
| `apishield report [dir]` | Generate markdown security report |

### Team Tier ($39/user/month)

| Command | Description |
|---------|-------------|
| `apishield inventory [dir]` | Generate API endpoint catalog |
| `apishield compliance [dir]` | Map findings to OWASP Top 10 |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "apishield": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
        "config": {
          "severityThreshold": "high",
          "excludePatterns": ["**/node_modules/**", "**/dist/**"],
          "reportFormat": "markdown"
        }
      }
    }
  }
}
```

Or set the environment variable:

```bash
export APISHIELD_LICENSE_KEY="your-key-here"
```

## Exit Codes

- `0` -- Secure (score >= 70, no critical issues)
- `1` -- Issues found (score < 70 or critical issues present)

Perfect for CI/CD integration.

## Privacy

- 100% local -- no code or route data sent externally
- Zero telemetry
- Offline license validation (JWT-based)
- Pattern matching only -- no AST parsing or code execution

## Part of the ClawHub Ecosystem

APIShield is built for [ClawHub](https://openclaw.dev), the marketplace for developer tools that plug into your CLI. Other skills in the ecosystem:

- **[DocSync](https://docsync-1q4.pages.dev)** -- Keep docs in sync with code
- **[DepGuard](https://depguard.pages.dev)** -- Dependency audit and vulnerability scanning
- **[EnvGuard](https://envguard.pages.dev)** -- Pre-commit secret detection
- **[GitPulse](https://gitpulse.pages.dev)** -- Git workflow analytics
- **[MigrateSafe](https://migratesafe.pages.dev)** -- Database migration safety checks

## License

MIT
