# configsafe

<p align="center">
  <img src="https://img.shields.io/badge/patterns-80+-blue" alt="80+ patterns">
  <img src="https://img.shields.io/badge/config_types-6-purple" alt="6 config types">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License">
  <img src="https://img.shields.io/badge/install-clawhub-blue" alt="ClawHub">
  <img src="https://img.shields.io/badge/zero-telemetry-brightgreen" alt="Zero telemetry">
</p>

<h3 align="center">Catch misconfigs before they become CVEs.</h3>

<p align="center">
  <a href="https://configsafe.pages.dev">Website</a> &middot;
  <a href="#quick-start">Quick Start</a> &middot;
  <a href="#supported-config-types">Config Types</a> &middot;
  <a href="https://configsafe.pages.dev/#pricing">Pricing</a>
</p>

---

## Your container is running as root. Again.

It happens to everyone. A Dockerfile with no USER directive. A Kubernetes pod with `privileged: true`. A Terraform security group open to `0.0.0.0/0`. A GitHub Actions workflow with write permissions on pull requests.

The vulnerability scanner catches it in production. After the breach.

**ConfigSafe catches misconfigurations before they leave your machine.** Pre-commit hooks. Local scanning. 80+ patterns across 6 config types. Zero data leaves your laptop.

## Quick Start

```bash
# 1. Install via ClawHub (free)
clawhub install configsafe

# 2. Scan your repo
configsafe scan

# 3. Install pre-commit hooks (Pro)
configsafe hooks install
```

That's it. Every commit is now scanned for infrastructure misconfigurations.

## What It Does

### Scan infrastructure configs for misconfigurations
One command to scan any file, directory, or your entire repo. 80+ regex patterns detect security misconfigurations across Dockerfiles, docker-compose, Kubernetes manifests, Terraform, CI/CD pipelines, and web server configs.

### Block commits with pre-commit hooks
Install a lefthook pre-commit hook that scans every staged config file. If a misconfiguration is detected, the commit is blocked with a clear remediation message.

### Generate security reports
Produce markdown reports with severity breakdowns, CIS benchmark mapping, and remediation steps. Ideal for security reviews and compliance audits.

### Run CIS benchmark checks
Map your infrastructure configurations against CIS Docker Benchmark, CIS Kubernetes Benchmark, and CIS AWS Foundations. Get pass/fail status per control.

### Enforce security policies
Define organization-specific policies (required labels, forbidden images, mandatory resource limits) and enforce them alongside the built-in 80+ patterns.

### Full compliance reports
Generate comprehensive reports covering CIS and NIST 800-190 frameworks with executive summaries, detailed findings, and remediation roadmaps.

## How It Compares

| Feature | ConfigSafe | Checkov ($299/mo) | Trivy ($0) | Hadolint ($0) | Terrascan ($0) |
|---------|:----------:|:------------------:|:----------:|:-------------:|:--------------:|
| Dockerfile scanning | Yes | Yes | Yes | Yes | No |
| docker-compose scanning | Yes | Yes | Yes | No | No |
| Kubernetes scanning | Yes | Yes | Yes | No | Yes |
| Terraform scanning | Yes | Yes | Yes | No | Yes |
| CI/CD pipeline scanning | Yes | Yes | No | No | No |
| Nginx/Apache scanning | Yes | No | No | No | No |
| Pre-commit hooks | Yes | Yes | No | No | No |
| Zero config scan | Yes | Config required | Config required | Yes | Config required |
| CIS benchmark mapping | Yes | Yes | Yes | No | Yes |
| NIST compliance | Yes | Yes | No | No | No |
| Offline license validation | Yes | N/A | N/A | N/A | N/A |
| Local-only (no cloud) | Yes | No | Yes | Yes | Yes |
| Zero telemetry | Yes | No | Yes | Yes | Yes |
| ClawHub integration | Yes | No | No | No | No |
| Price (individual) | Free/$19/mo | $299/mo | Free | Free | Free |

## Supported Config Types

ConfigSafe detects 80+ misconfiguration patterns across 6 config types:

### Dockerfile

| Check | Severity | Description |
|-------|----------|-------------|
| Running as root | Critical | No USER directive -- container runs as root |
| `latest` tag | High | Using `latest` tag -- unpinned, non-reproducible builds |
| ADD vs COPY | Medium | ADD instead of COPY -- ADD has tar extraction and URL side effects |
| Sensitive ports | High | Exposing sensitive ports (22, 3306, 5432, 6379, 27017) |
| Missing health check | Medium | No HEALTHCHECK directive defined |
| Secrets in ENV | Critical | Hardcoded secrets in ENV directives |
| curl pipe bash | Critical | Using `curl \| bash` -- remote code execution risk |
| chmod 777 | High | World-writable file permissions |
| apt-get bloat | Low | Missing `--no-install-recommends` on apt-get install |
| Missing multi-stage | Medium | Single-stage build includes build dependencies in final image |

### docker-compose

| Check | Severity | Description |
|-------|----------|-------------|
| privileged: true | Critical | Container runs with full host privileges |
| Host network mode | High | Container shares host network stack |
| Docker socket mount | Critical | Mounting /var/run/docker.sock gives container control over Docker |
| Missing resource limits | Medium | No memory/CPU limits defined |
| Plaintext secrets | Critical | Secrets in environment variables in plaintext |
| Unbound ports | High | Ports exposed without binding to 127.0.0.1 |
| Missing restart policy | Low | No restart policy defined |
| Missing health check | Medium | No healthcheck defined |

### Kubernetes

| Check | Severity | Description |
|-------|----------|-------------|
| Running as root | Critical | Container runs as root user |
| Privileged containers | Critical | securityContext.privileged: true |
| Missing security context | High | No securityContext defined |
| Missing resource limits | High | No resource requests/limits defined |
| hostPath volumes | Critical | hostPath volumes expose host filesystem |
| Default namespace | Medium | Resources deployed to default namespace |
| Missing probes | Medium | No readiness/liveness probes defined |
| Plaintext secrets | Critical | Secrets in env vars instead of Secret resources |
| allowPrivilegeEscalation | High | allowPrivilegeEscalation: true |
| Missing pod security | Medium | No pod security standards applied |

### Terraform

| Check | Severity | Description |
|-------|----------|-------------|
| Hardcoded credentials | Critical | AWS keys, passwords, or tokens in .tf files |
| Missing encryption | High | S3 buckets, RDS, EBS without encryption at rest |
| Public S3 buckets | Critical | S3 bucket ACL set to public-read or public-read-write |
| Open security groups | Critical | Ingress rule with 0.0.0.0/0 CIDR |
| Missing logging | Medium | CloudTrail, VPC Flow Logs, or S3 access logging not enabled |
| Missing state encryption | High | Terraform state backend without encryption |
| Default VPC | Medium | Using default VPC instead of custom |
| Overly permissive IAM | High | IAM policies with Action: "*" or Resource: "*" |

### CI/CD Pipelines

| Check | Severity | Description |
|-------|----------|-------------|
| Plaintext secrets | Critical | Secrets hardcoded in pipeline files |
| PR write permissions | High | Pull request trigger with write permissions |
| Unpinned actions | Medium | Using actions/checkout without pinned SHA version |
| Missing timeout | Low | No timeout-minutes defined for jobs |
| Unrestricted runners | High | Self-hosted runners without label restrictions |
| Artifact no expiry | Low | Artifact upload without retention/expiry |

### Nginx/Apache

| Check | Severity | Description |
|-------|----------|-------------|
| Missing security headers | High | Missing X-Frame-Options, CSP, HSTS, etc. |
| Server tokens | Medium | Server version information exposed |
| SSL/TLS misconfig | High | Weak SSL protocols or ciphers enabled |
| Open proxy | Critical | Proxy configured to forward arbitrary requests |
| Missing rate limiting | Medium | No rate limiting configuration |
| Directory listing | High | autoindex on / Options +Indexes enabled |

## Pricing

| Feature | Free | Pro ($19/user/mo) | Team ($39/user/mo) |
|---------|:----:|:------------------:|:-------------------:|
| One-shot config scan | 5 files | Unlimited | Unlimited |
| 80+ detection patterns | Yes | Yes | Yes |
| Auto-detect config types | Yes | Yes | Yes |
| Pre-commit hooks | | Yes | Yes |
| Security reports | | Yes | Yes |
| CIS benchmark mapping | | Yes | Yes |
| Policy enforcement | | | Yes |
| Compliance reports (CIS, NIST) | | | Yes |
| SARIF output | | | Yes |
| CI/CD integration | | | Yes |

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "configsafe": {
        "enabled": true,
        "apiKey": "YOUR_LICENSE_KEY",
        "config": {
          "severityThreshold": "high",
          "customPolicies": [
            {
              "regex": "image:.*myregistry\\.io",
              "severity": "high",
              "configType": "kubernetes",
              "description": "Must use approved container registry"
            }
          ],
          "excludePatterns": ["**/test/**", "**/examples/**"]
        }
      }
    }
  }
}
```

## Ecosystem

ConfigSafe is part of the ClawHub security suite:

- **[EnvGuard](https://envguard.pages.dev)** -- Pre-commit secret detection
- **[DepGuard](https://depguard.pages.dev)** -- Dependency vulnerability scanning
- **[ConfigSafe](https://configsafe.pages.dev)** -- Infrastructure configuration auditing
- **[APIShield](https://apishield.pages.dev)** -- API security scanning
- **[MigrateSafe](https://migratesafe.pages.dev)** -- Database migration safety checking

## Privacy

- 100% local -- no code or configs sent externally
- Zero telemetry
- Offline license validation
- Pattern matching only -- no AST parsing, no external dependencies

## License

MIT
