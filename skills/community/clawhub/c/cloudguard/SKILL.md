---
name: CloudGuard
version: 1.0.0
description: "Cloud infrastructure & IaC security scanner -- detects insecure Terraform, open S3 buckets, permissive IAM, missing encryption, exposed ports, and cloud misconfigurations"
homepage: https://cloudguard.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\u2601\ufe0f",
      "primaryEnv": "CLOUDGUARD_LICENSE_KEY",
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

# CloudGuard -- Cloud Infrastructure & IaC Security Scanner

CloudGuard scans codebases for insecure cloud infrastructure patterns including Terraform misconfigurations, open S3 buckets, overly permissive IAM policies, missing encryption at rest, exposed ports, absent logging and monitoring, and general cloud compliance gaps. It uses 90 regex-based patterns across 6 security categories, produces severity-graded reports with actionable remediation, and integrates with git hooks via lefthook. 100% local. Zero telemetry.

## Commands

### Free Tier (No license required)

#### `cloudguard scan [file|directory]`
One-shot cloud security scan of infrastructure-as-code files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all IaC and configuration files (Terraform .tf, CloudFormation .yml/.yaml/.json, Dockerfiles, Kubernetes manifests, cloud config files)
3. Runs 30 cloud security patterns against each file (free tier limit)
4. Skips .git, node_modules, .terraform, vendor, and other non-IaC directories
5. Respects .gitignore and allowlist files
6. Calculates a cloud security score (0-100) per file and overall
7. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
8. Outputs findings with: file, line number, check ID, severity, category, description, recommendation
9. Exit code 0 if score >= 70, exit code 1 if score < 70 (too many misconfigurations)
10. Free tier limited to first 30 of 90 patterns

**Example usage scenarios:**
- "Scan my Terraform for security issues" -> runs `cloudguard scan .`
- "Check my cloud config for misconfigurations" -> runs `cloudguard scan infra/`
- "Audit my AWS infrastructure code" -> runs `cloudguard scan terraform/`
- "Find open S3 buckets in my IaC" -> runs `cloudguard scan .`

### Pro Tier ($19/user/month -- requires CLOUDGUARD_LICENSE_KEY)

#### `cloudguard scan [file|directory]` (Pro -- 60 patterns)
Full scan with 60 of 90 patterns unlocked covering all 6 categories in depth.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier pro
```

#### `cloudguard hooks install`
Install git pre-commit hooks that scan staged IaC files for cloud security issues before every commit.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" hooks install
```

**What it does:**
1. Validates Pro+ license
2. Copies lefthook config to project root
3. Installs lefthook pre-commit and pre-push hooks
4. On every commit: scans all staged IaC files for cloud misconfigurations, blocks commit if critical/high findings, shows remediation advice

#### `cloudguard hooks uninstall`
Remove CloudGuard git hooks.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" hooks uninstall
```

#### `cloudguard report [directory]`
Generate a markdown cloud security report with findings, severity breakdown, category analysis, and remediation steps.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format text report
```

**What it does:**
1. Validates Pro+ license
2. Runs full scan of the directory with 60 patterns
3. Generates a formatted markdown report from template
4. Includes per-category breakdowns, cloud security score, remediation priority
5. Output suitable for security reviews and compliance audits

#### `cloudguard audit [directory]`
Deep cloud security audit across all categories.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] audit
```

**What it does:**
1. Validates Pro+ license
2. Runs comprehensive scan with extended pattern set
3. Provides per-category severity analysis
4. Reports compliance gaps across S3, IAM, networking, encryption, logging, and configuration

### Team Tier ($39/user/month -- requires CLOUDGUARD_LICENSE_KEY with team tier)

#### `cloudguard scan [file|directory]` (Team -- all 90 patterns)
Full scan with all 90 patterns unlocked.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier team
```

#### `cloudguard scan --format json [directory]`
JSON output for CI/CD pipeline integration.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format json
```

**What it does:**
1. Validates Team+ license
2. Runs full scan with all 90 patterns
3. Outputs findings in structured JSON format
4. Compatible with CI/CD pipelines, dashboards, and automated tooling
5. Includes rule definitions, severity mappings, and category breakdowns

#### `cloudguard scan --format html [directory]`
HTML report output for stakeholder sharing.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format html
```

#### `cloudguard scan --category [category] [directory]`
Category-filtered scan for focused audits.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --category S3
```

**What it does:**
1. Validates Team+ license
2. Runs only the patterns for the specified category
3. Available categories: S3, IM, NW, EN, LG, CF
4. Useful for targeted compliance checks

#### `cloudguard status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" status
```

## Check Categories

CloudGuard detects 90 cloud security patterns across 6 categories:

| Category | Code | Patterns | Examples | Severity Range |
|----------|------|----------|----------|----------------|
| **Storage Security** | S3 | 15 | Public S3 buckets, missing encryption, no versioning, overly permissive bucket policies, missing access logging, no lifecycle rules | Critical/High/Medium |
| **IAM & Permissions** | IM | 15 | Wildcard IAM policies, AdministratorAccess, overly broad assume role, missing MFA, root account usage, no least privilege | Critical/High/Medium |
| **Network Security** | NW | 15 | Open security groups (0.0.0.0/0), exposed ports (22, 3389, 3306), missing VPC, no network ACLs, public subnets without NAT, SSH open to world | Critical/High/Medium |
| **Encryption** | EN | 15 | Missing encryption at rest, no KMS key rotation, unencrypted EBS volumes, missing SSL/TLS, no transit encryption, weak cipher suites | Critical/High/Medium/Low |
| **Logging & Monitoring** | LG | 15 | Missing CloudTrail, no VPC flow logs, disabled GuardDuty, missing alarm configurations, no SNS notifications, absent audit logs | High/Medium/Low |
| **Configuration & Compliance** | CF | 15 | Missing tags, no resource naming convention, hardcoded regions, missing backups, no disaster recovery, drift detection gaps | Medium/Low |

## Severity Levels

| Level | Points Deducted | Meaning | Action Required |
|-------|----------------|---------|-----------------|
| **Critical** | 25 | Immediate infrastructure compromise risk (open to internet, no auth, wildcard admin) | Fix immediately; block deployment |
| **High** | 15 | Significant security gap that could be exploited (missing encryption, overly permissive policies) | Fix within current sprint |
| **Medium** | 8 | Security best practice violation that increases attack surface | Plan remediation within 30 days |
| **Low** | 3 | Informational finding, minor hygiene issue, or hardening recommendation | Address when convenient |

## Scoring System

CloudGuard uses a 0-100 scoring system:

- **Starting score:** 100 (perfect, no findings)
- **Deductions:** Each finding deducts points based on severity
- **Floor:** Score cannot go below 0
- **Pass threshold:** 70 (exit code 0)
- **Fail threshold:** Below 70 (exit code 1)

### Grade Scale

| Grade | Score Range | Meaning |
|-------|------------|---------|
| **A** | 90-100 | Excellent -- minimal or no cloud security issues |
| **B** | 80-89 | Good -- minor issues that should be addressed |
| **C** | 70-79 | Acceptable -- passing but needs improvement |
| **D** | 60-69 | Poor -- significant security gaps requiring attention |
| **F** | Below 60 | Failing -- critical misconfigurations must be fixed immediately |

## Tier-Based Pattern Access

| Tier | Patterns Available | Categories |
|------|-------------------|------------|
| **Free** | 30 patterns | First 5 patterns per category |
| **Pro** | 60 patterns | First 10 patterns per category |
| **Team** | 90 patterns (all) | All 15 patterns per category |
| **Enterprise** | 90 patterns (all) | All 15 patterns per category + priority support |

## Configuration

Users can configure CloudGuard in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "cloudguard": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY_HERE",
        "config": {
          "severityThreshold": "high",
          "ignorePatterns": ["**/test/**", "**/examples/**", "**/fixtures/**"],
          "ignoreChecks": [],
          "reportFormat": "text",
          "categories": ["S3", "IM", "NW", "EN", "LG", "CF"]
        }
      }
    }
  }
}
```

## Supported File Types

CloudGuard scans the following file types for cloud security patterns:

| File Type | Extensions | Use Case |
|-----------|------------|----------|
| Terraform | `.tf`, `.tfvars` | HashiCorp Terraform IaC definitions |
| CloudFormation | `.yml`, `.yaml`, `.json`, `.template` | AWS CloudFormation templates |
| Kubernetes | `.yml`, `.yaml` | Kubernetes manifests and Helm charts |
| Docker | `Dockerfile`, `docker-compose.yml` | Container configurations |
| Ansible | `.yml`, `.yaml` | Ansible playbooks and roles |
| General Config | `.conf`, `.cfg`, `.ini`, `.toml`, `.hcl` | Infrastructure configuration files |
| Scripts | `.sh`, `.bash`, `.ps1`, `.py` | Deployment and provisioning scripts |
| Policy | `.json`, `.rego` | IAM policies, OPA Rego rules |

## Important Notes

- **Free tier** works immediately with no configuration
- **All scanning happens locally** -- no code is sent to external servers
- **License validation is offline** -- no phone-home or network calls
- Pattern matching only -- no AST parsing, no external dependencies beyond bash and grep
- Supports scanning all IaC file types in a single pass
- Git hooks use **lefthook** which must be installed (see install metadata above)
- Exit codes: 0 = pass (score >= 70), 1 = fail (score < 70, for CI/CD integration)
- Category-level breakdown shows exactly where security gaps exist

## Error Handling

- If lefthook is not installed and user tries `hooks install`, prompt to install it
- If license key is invalid or expired, show clear message with link to https://cloudguard.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable IaC files found in target, report clean scan with info message
- If invalid category specified with --category, show available categories
- If grep does not support -E flag (rare), fall back gracefully with error message

## When to Use CloudGuard

The user might say things like:
- "Scan my Terraform for security issues"
- "Check my cloud infrastructure code"
- "Find open S3 buckets in my IaC"
- "Audit my AWS configuration"
- "Check for missing encryption in my infrastructure"
- "Find overly permissive IAM policies"
- "Scan for exposed ports in my security groups"
- "Are my CloudFormation templates secure?"
- "Check my Kubernetes manifests for security"
- "Run a cloud security audit"
- "Find missing CloudTrail in my Terraform"
- "Detect VPC misconfigurations"
- "Scan for hardcoded regions in my IaC"
- "Check if my EBS volumes are encrypted"
- "Find missing tags in my cloud resources"
- "Set up pre-commit hooks for cloud security"
- "Generate a cloud security report for my team"
