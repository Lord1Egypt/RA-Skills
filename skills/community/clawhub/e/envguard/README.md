# envguard

<p align="center">
  <img src="https://img.shields.io/badge/patterns-50+-blue" alt="50+ patterns">
  <img src="https://img.shields.io/badge/services-20+-purple" alt="20+ services">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/install-clawhub-blue" alt="ClawHub">
  <img src="https://img.shields.io/badge/zero-telemetry-brightgreen" alt="Zero telemetry">
</p>

<h3 align="center">Pre-commit secret detection. Block leaked credentials before they hit git.</h3>

<p align="center">
  <a href="https://envguard.pages.dev">Website</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#supported-patterns">Patterns</a> &middot;
  <a href="https://envguard.pages.dev/#pricing">Pricing</a>
</p>

---

## Your .env just got committed. Again.

It happens to everyone. A Stripe key in a config file. An AWS secret in a test fixture. A database URL in a docker-compose checked into a public repo.

GitGuardian emails you 3 hours later. By then, bots have already scraped it.

**EnvGuard catches secrets before they leave your machine.** Pre-commit hooks. Local scanning. 50+ patterns. Zero data leaves your laptop.

## Quick Start

```bash
# 1. Install via ClawHub (free)
clawhub install envguard

# 2. Scan your repo
envguard scan

# 3. Install pre-commit hooks (Pro)
envguard hooks install
```

That's it. Every commit is now scanned for secrets.

## What It Does

### Scan files for secrets
One command to scan any file, directory, or your entire repo. 50+ regex patterns detect API keys, tokens, passwords, private keys, and connection strings from 20+ services.

### Block commits with pre-commit hooks
Install a lefthook pre-commit hook that scans every staged file. If a secret is detected, the commit is blocked with a clear remediation message.

### Manage false positives
Allowlist known-safe patterns (test fixtures, example values) so they don't trigger on every scan.

### Scan staged changes only
For large repos, scan only the diff instead of the entire codebase. Faster, focused, and perfect for CI.

### Full git history scan
Audit your entire git history for secrets that were committed in the past. Even deleted secrets remain in git objects -- find them before an attacker does.

### Generate compliance reports
Produce markdown reports with severity breakdowns and remediation steps. Ideal for security reviews and compliance audits.

### Custom patterns
Define organization-specific secret patterns (internal tokens, proprietary formats) alongside the built-in 50+ patterns.

## How It Compares

| Feature | EnvGuard | GitGuardian | Gitleaks | TruffleHog |
|---------|:--------:|:-----------:|:--------:|:----------:|
| Local-only (no cloud) | Yes | No | Yes | Yes |
| Pre-commit hooks | Yes | Yes | Yes | Yes |
| Zero config scan | Yes | No | Config required | Config required |
| Custom patterns | Yes | Enterprise | Yes | Yes |
| Git history scan | Yes | Yes | Yes | Yes |
| Allowlist management | Yes | Yes | Via config | Via config |
| SARIF-compatible reports | Yes | Yes | Yes | Yes |
| Offline license validation | Yes | N/A | N/A | N/A |
| Zero telemetry | Yes | No | Yes | Yes |
| ClawHub integration | Yes | No | No | No |
| Price (individual) | Free/$19/mo | $0-$380/mo | Free | Free |

## Supported Patterns

EnvGuard detects 50+ secret patterns across 20+ services:

| Service | Patterns | Severity |
|---------|----------|----------|
| **AWS** | Access Key IDs (AKIA), Secret Access Keys, STS tokens | Critical |
| **Stripe** | sk_live, sk_test, rk_live, rk_test, whsec_ | Critical |
| **GitHub** | ghp_, gho_, ghu_, ghs_, ghr_, github_pat_ | Critical |
| **GitLab** | glpat-, gloas-, glrt- | Critical |
| **Private Keys** | RSA, OpenSSH, DSA, EC, PGP, PKCS8 | Critical |
| **Slack** | xoxb-, xoxp-, xoxo-, xapp-, xoxs- | High |
| **Google** | AIza API keys, OAuth client IDs | High |
| **JWT** | eyJ... tokens | High |
| **Database** | postgres://, mysql://, mongodb://, redis://, amqp://, mssql:// | High |
| **Twilio** | SK (API Keys), AC (Account SIDs) | High |
| **SendGrid** | SG.* API keys | High |
| **npm** | npm_ tokens, registry auth | High |
| **Firebase** | API keys, config values | High |
| **Supabase** | Service role keys, JWTs | High |
| **Vercel** | vercel_ tokens | High |
| **Heroku** | API keys (UUID format) | Medium |
| **DigitalOcean** | dop_v1_, doo_v1_ | Medium |
| **Azure** | AccountKey, client secrets, SAS tokens | Medium |
| **Cloudflare** | API tokens, global API keys | Medium |
| **Docker** | dckr_pat_ tokens, password configs | Medium |
| **Mailgun** | key- API keys | Medium |
| **Generic** | api_key=, secret=, password=, token= | Low |
| **.env leaks** | KEY=value patterns in source files | Low |

## Pricing

| Feature | Free | Pro ($19/user/mo) | Team ($39/user/mo) |
|---------|:----:|:------------------:|:-------------------:|
| One-shot secret scan | Yes | Yes | Yes |
| 50+ detection patterns | Yes | Yes | Yes |
| .envguardignore support | Yes | Yes | Yes |
| Pre-commit hooks | | Yes | Yes |
| Allowlist management | | Yes | Yes |
| Staged diff scanning | | Yes | Yes |
| Full git history scan | | | Yes |
| Compliance reports | | | Yes |
| Custom patterns | | | Yes |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "envguard": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
        "config": {
          "severityThreshold": "high",
          "allowlist": ["EXAMPLE_KEY_FOR_TESTS"],
          "customPatterns": [
            {
              "regex": "myco_[0-9a-f]{32}",
              "severity": "critical",
              "service": "MyCorp",
              "description": "MyCorp internal API token"
            }
          ],
          "excludePatterns": ["**/test-fixtures/**"]
        }
      }
    }
  }
}
```

## .envguardignore

Create a `.envguardignore` file in your repo root to exclude paths from scanning. Uses the same syntax as `.gitignore`:

```
# Test fixtures with fake secrets
tests/fixtures/**
test-data/**

# Generated files
*.min.js
dist/**

# Documentation with example keys
docs/examples/**
```

## Privacy

- 100% local -- no code or secrets sent externally
- Zero telemetry
- Offline license validation
- Matches are always redacted in output (first/last 4 chars only)

## License

MIT
