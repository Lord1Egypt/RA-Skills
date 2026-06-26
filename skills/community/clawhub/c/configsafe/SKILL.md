---
name: configsafe
description: Infrastructure configuration auditor — scans Dockerfiles, K8s manifests, Terraform, and CI/CD pipelines for security misconfigurations
homepage: https://configsafe.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udc33",
      "primaryEnv": "CONFIGSAFE_LICENSE_KEY",
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

# ConfigSafe — Infrastructure Configuration Auditor

ConfigSafe scans infrastructure configuration files for security misconfigurations across Dockerfiles, docker-compose, Kubernetes manifests, Terraform, CI/CD pipelines, and web server configs. It uses regex-based pattern matching against 80+ misconfiguration patterns, lefthook for git hook integration, and produces markdown security reports with CIS benchmark mapping.

## Commands

### Free Tier (No license required)

#### `configsafe scan [file|directory]`
One-shot configuration security scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/configsafe.sh" scan [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Auto-detects configuration types (Dockerfile, docker-compose, Kubernetes, Terraform, CI/CD, Nginx/Apache)
3. Finds all config files matching known patterns
4. Runs 80+ misconfiguration patterns against each file
5. Calculates a security score (0-100) per file and overall
6. Outputs findings with: file, line number, check ID, severity, description, recommendation
7. Exit code 0 if secure (score >= 70), exit code 1 if issues found
8. Free tier limited to 5 config files per scan

**Example usage scenarios:**
- "Scan my infrastructure configs for security issues" -> runs `configsafe scan .`
- "Check this Dockerfile for misconfigurations" -> runs `configsafe scan Dockerfile`
- "Audit my Kubernetes manifests" -> runs `configsafe scan k8s/`
- "Is my Terraform config secure?" -> runs `configsafe scan terraform/`

### Pro Tier ($19/user/month -- requires CONFIGSAFE_LICENSE_KEY)

#### `configsafe hooks install`
Install git pre-commit hooks that scan staged config files before every commit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/configsafe.sh" hooks install
```

**What it does:**
1. Validates Pro+ license
2. Copies lefthook config to project root
3. Installs lefthook pre-commit hook
4. On every commit: scans all staged config files for misconfigurations, blocks commit if critical/high findings, shows remediation advice

#### `configsafe hooks uninstall`
Remove ConfigSafe git hooks.

```bash
bash "<SKILL_DIR>/scripts/configsafe.sh" hooks uninstall
```

#### `configsafe report [directory]`
Generate a markdown security report with findings, severity breakdown, and remediation steps.

```bash
bash "<SKILL_DIR>/scripts/configsafe.sh" report [directory]
```

**What it does:**
1. Validates Pro+ license
2. Runs full scan of the directory
3. Generates a formatted markdown report from template
4. Includes per-file breakdowns, security scores, CIS benchmark references
5. Output suitable for security reviews and compliance audits

#### `configsafe benchmark [directory]`
Run CIS benchmark checks against infrastructure configurations.

```bash
bash "<SKILL_DIR>/scripts/configsafe.sh" benchmark [directory]
```

**What it does:**
1. Validates Pro+ license
2. Maps findings to CIS Docker Benchmark, CIS Kubernetes Benchmark, and CIS AWS Foundations
3. Reports pass/fail status for each benchmark check
4. Outputs overall compliance percentage

### Team Tier ($39/user/month -- requires CONFIGSAFE_LICENSE_KEY with team tier)

#### `configsafe policy [directory]`
Enforce organization-specific security policies on infrastructure configurations.

```bash
bash "<SKILL_DIR>/scripts/configsafe.sh" policy [directory]
```

**What it does:**
1. Validates Team+ license
2. Loads custom policies from ~/.openclaw/openclaw.json (configsafe.config.customPolicies)
3. Enforces organization-specific rules (e.g., required labels, forbidden images, mandatory resource limits)
4. Combines custom policies with built-in patterns for comprehensive scanning
5. Outputs SARIF-compatible results

#### `configsafe compliance [directory]`
Generate a full compliance report covering CIS and NIST frameworks.

```bash
bash "<SKILL_DIR>/scripts/configsafe.sh" compliance [directory]
```

**What it does:**
1. Validates Team+ license
2. Runs full scan with all patterns
3. Maps findings to CIS Docker Benchmark, CIS Kubernetes Benchmark, CIS AWS Foundations, and NIST 800-190
4. Generates comprehensive compliance report with pass/fail per control
5. Includes executive summary, detailed findings, and remediation roadmap

#### `configsafe status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/configsafe.sh" status
```

## Detected Misconfigurations

ConfigSafe detects 80+ misconfiguration patterns across 6 config types:

| Category | Examples | Severity |
|----------|----------|----------|
| **Dockerfile** | Running as root, `latest` tag, ADD vs COPY, exposed sensitive ports, missing health checks, secrets in ENV, curl pipe bash, chmod 777, missing multi-stage builds | Critical/High |
| **docker-compose** | privileged: true, host network, Docker socket mount, missing resource limits, plaintext secrets, unbound ports, missing restart policy | Critical/High |
| **Kubernetes** | Running as root, privileged containers, missing security context, missing resource limits, hostPath volumes, default namespace, missing probes, allowPrivilegeEscalation | Critical/High |
| **Terraform** | Hardcoded credentials, missing encryption, public S3 buckets, open security groups (0.0.0.0/0), missing logging, overly permissive IAM, default VPC | Critical/High |
| **CI/CD Pipelines** | Plaintext secrets, PR trigger with write perms, unpinned actions, missing timeout, unrestricted self-hosted runners, artifact upload without expiry | High/Medium |
| **Nginx/Apache** | Missing security headers, server tokens enabled, SSL/TLS misconfig, open proxy, missing rate limiting, directory listing enabled | Medium/High |

## Configuration

Users can configure ConfigSafe in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "configsafe": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "high",
          "customPolicies": [],
          "excludePatterns": ["**/test/**", "**/examples/**"],
          "reportFormat": "markdown"
        }
      }
    }
  }
}
```

## Important Notes

- **Free tier** works immediately with no configuration
- **All scanning happens locally** -- no code or configs are sent to external servers
- **License validation is offline** -- no phone-home or network calls
- Pattern matching only -- no AST parsing, no external dependencies
- Supports scanning multiple config types in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = secure (score >= 70), 1 = issues found (for CI/CD integration)

## Error Handling

- If lefthook is not installed and user tries `hooks install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://configsafe.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no config files found in target, report clean scan with info message
- If config type cannot be determined, skip the file gracefully

## When to Use ConfigSafe

The user might say things like:
- "Scan my Dockerfile for security issues"
- "Check my Kubernetes manifests for misconfigurations"
- "Audit my Terraform configs"
- "Is my docker-compose file secure?"
- "Check my CI/CD pipeline for security problems"
- "Generate a security report for my infrastructure"
- "Run CIS benchmark checks"
- "Set up pre-commit hooks for config scanning"
- "Check if my containers are running as root"
- "Scan for open security groups in Terraform"
- "Are there any hardcoded secrets in my configs?"
- "Check my nginx config for security headers"
