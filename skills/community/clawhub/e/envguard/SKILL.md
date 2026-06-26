---
name: envguard
description: Pre-commit secret detection — block leaked credentials, API keys, and .env files before they hit git
homepage: https://envguard.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udd10",
      "primaryEnv": "ENVGUARD_LICENSE_KEY",
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

# EnvGuard — Pre-Commit Secret Detection

EnvGuard scans your code for leaked secrets, credentials, API keys, and .env file contents before they reach git. It uses regex-based pattern matching against 50+ secret formats from 20+ services, lefthook for git hook integration, and produces SARIF-compatible reports for compliance workflows.

## Commands

### Free Tier (No license required)

#### `envguard scan [file|directory]`
One-shot secret scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/envguard.sh" scan [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Finds all text files (excluding .git/, node_modules/, dist/, build/, vendor/, __pycache__)
3. Runs 50+ secret detection patterns against each file
4. Respects .envguardignore exclusions (gitignore syntax)
5. Outputs findings with: file, line number, pattern matched, severity, redacted match
6. Exit code 0 if clean, exit code 1 if critical/high findings detected

**Example usage scenarios:**
- "Scan this repo for leaked secrets" -> runs `envguard scan .`
- "Check this file for API keys" -> runs `envguard scan src/config.ts`
- "Are there any secrets in my source code?" -> runs `envguard scan src/`

### Pro Tier ($19/user/month -- requires ENVGUARD_LICENSE_KEY)

#### `envguard hooks install`
Install git pre-commit hooks that scan staged files for secrets before every commit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/envguard.sh" hooks install
```

**What it does:**
1. Validates Pro+ license
2. Copies lefthook config to project root
3. Installs lefthook pre-commit hook
4. On every commit: scans all staged files for secrets, blocks commit if secrets found, shows remediation advice

#### `envguard hooks uninstall`
Remove EnvGuard git hooks.

```bash
bash "<SKILL_DIR>/scripts/envguard.sh" hooks uninstall
```

#### `envguard allowlist [add|remove|list] [pattern]`
Manage false positive patterns. Allowlisted patterns are skipped during scanning.

```bash
bash "<SKILL_DIR>/scripts/envguard.sh" allowlist add "EXAMPLE_API_KEY_FOR_TESTS"
bash "<SKILL_DIR>/scripts/envguard.sh" allowlist remove "EXAMPLE_API_KEY_FOR_TESTS"
bash "<SKILL_DIR>/scripts/envguard.sh" allowlist list
```

**What it does:**
1. Validates Pro+ license
2. Reads/writes allowlist in ~/.openclaw/openclaw.json (envguard.config.allowlist)
3. Allowlisted patterns are treated as known-safe and skipped during scans

#### `envguard diff`
Scan only staged changes (git diff --cached) for secrets.

```bash
bash "<SKILL_DIR>/scripts/envguard.sh" diff
```

**What it does:**
1. Validates Pro+ license
2. Gets staged changes via `git diff --cached`
3. Scans only added/modified lines for secrets
4. Ideal for pre-commit checks on large repos

### Team Tier ($39/user/month -- requires ENVGUARD_LICENSE_KEY with team tier)

#### `envguard history [directory]`
Full git history scan -- finds secrets in all previous commits.

```bash
bash "<SKILL_DIR>/scripts/envguard.sh" history [directory]
```

**What it does:**
1. Validates Team+ license
2. Walks entire git log using `git log -p`
3. Scans every diff for secrets across all commits
4. Reports: commit hash, author, date, file, line, pattern matched
5. Critical for onboarding repos that may have had secrets committed in the past

#### `envguard report [directory]`
Generate a SARIF-compatible or markdown compliance report.

```bash
bash "<SKILL_DIR>/scripts/envguard.sh" report [directory]
```

**What it does:**
1. Validates Team+ license
2. Runs full scan of the directory
3. Generates a formatted markdown report with severity breakdown
4. Includes remediation steps for each finding category
5. Output suitable for compliance audits and security reviews

#### `envguard policy [directory]`
Custom secret patterns and enforcement rules.

```bash
bash "<SKILL_DIR>/scripts/envguard.sh" policy [directory]
```

**What it does:**
1. Validates Team+ license
2. Loads custom patterns from ~/.openclaw/openclaw.json (envguard.config.customPatterns)
3. Enforces organization-specific secret rules (e.g., internal token formats)
4. Combines custom patterns with built-in patterns for comprehensive scanning

## Detected Secret Types

EnvGuard detects 50+ secret patterns across 20+ services:

| Category | Examples | Severity |
|----------|----------|----------|
| AWS Credentials | AKIA* keys, aws_secret_access_key | Critical |
| Stripe Keys | sk_live_*, sk_test_*, rk_live_*, whsec_* | Critical |
| GitHub Tokens | ghp_*, gho_*, ghu_*, ghs_*, ghr_* | Critical |
| GitLab Tokens | glpat-* | Critical |
| Private Keys | RSA, OPENSSH, DSA, EC, PGP private keys | Critical |
| Slack Tokens | xoxb-*, xoxp-*, xoxo-*, xapp-* | High |
| Google API Keys | AIza* | High |
| JWT Tokens | eyJ* (long base64 tokens) | High |
| Database URIs | postgres://, mysql://, mongodb://, redis:// | High |
| Twilio Keys | SK* account SIDs | High |
| SendGrid Keys | SG.* | High |
| Firebase/Supabase | API keys and service tokens | High |
| npm Tokens | npm_* | High |
| Heroku API Keys | Heroku token patterns | Medium |
| DigitalOcean | dop_v1_*, doo_v1_* | Medium |
| Azure Keys | Azure subscription/account keys | Medium |
| Cloudflare | API tokens and keys | Medium |
| Docker Hub | Docker auth tokens | Medium |
| Mailgun/Postmark | API keys | Medium |
| Generic Secrets | api_key=, password=, secret=, token= | Low |
| .env Leaks | KEY=value patterns in source files | Low |

## Configuration

Users can configure EnvGuard in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "envguard": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "high",
          "allowlist": [],
          "customPatterns": [],
          "excludePatterns": ["**/node_modules/**", "**/dist/**", "**/.git/**"],
          "reportFormat": "markdown"
        }
      }
    }
  }
}
```

## Important Notes

- **Free tier** works immediately with no configuration
- **All scanning happens locally** -- no code or secrets are sent to external servers
- **License validation is offline** -- no phone-home or network calls
- Supports .envguardignore files (gitignore syntax) to exclude paths
- Matches are always **redacted** in output (first/last 4 chars only)
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = clean, 1 = findings detected (for CI/CD integration)

## Error Handling

- If lefthook is not installed and user tries `hooks install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://envguard.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If .envguardignore is malformed, warn and continue with default excludes
- If no files found in target, report clean scan with info message

## When to Use EnvGuard

The user might say things like:
- "Scan for leaked secrets"
- "Check if any API keys are in my code"
- "Set up secret scanning on my commits"
- "Are there any credentials in this repo?"
- "Generate a security report for compliance"
- "Scan git history for leaked passwords"
- "Block secrets from being committed"
- "Check my staged files for secrets"
- "Add a false positive to the allowlist"
