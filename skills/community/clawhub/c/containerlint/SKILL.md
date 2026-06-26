---
name: ContainerLint
version: 1.0.0
description: "Docker & container security anti-pattern analyzer -- detects Dockerfile issues, missing health checks, resource limit gaps, privileged containers, insecure networking, and orchestration anti-patterns"
homepage: https://containerlint.pages.dev
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udc33",
      "primaryEnv": "CONTAINERLINT_LICENSE_KEY",
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

# ContainerLint -- Docker & Container Security Anti-Pattern Analyzer

ContainerLint scans codebases for Docker and container security anti-patterns, Dockerfile issues, missing health checks, resource limit gaps, privileged containers, insecure networking, and orchestration misconfigurations. It uses regex-based pattern matching against 90 container-specific patterns across 6 categories, lefthook for git hook integration, and produces markdown reports with actionable remediation guidance. 100% local. Zero telemetry.

## Commands

### Free Tier (No license required)

#### `containerlint scan [file|directory]`
One-shot container security scan of files or directories.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target]
```

**What it does:**
1. Accepts a file path or directory (defaults to current directory)
2. Discovers all source files (skips .git, node_modules, binaries, images, .min.js)
3. Runs 30 container security patterns against each file (free tier limit)
4. Calculates a container security score (0-100) per file and overall
5. Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
6. Outputs findings with: file, line number, check ID, severity, description, recommendation
7. Exit code 0 if score >= 70, exit code 1 if container security is poor
8. Free tier limited to first 30 patterns (DF + SC categories)

**Example usage scenarios:**
- "Scan my code for Dockerfile issues" -> runs `containerlint scan .`
- "Check this file for container anti-patterns" -> runs `containerlint scan docker-compose.yml`
- "Find privileged containers" -> runs `containerlint scan .`
- "Audit container security in my project" -> runs `containerlint scan .`
- "Check for missing health checks" -> runs `containerlint scan .`

### Pro Tier ($19/user/month -- requires CONTAINERLINT_LICENSE_KEY)

#### `containerlint scan --tier pro [file|directory]`
Extended scan with 60 patterns covering Dockerfile, security context, health checks, and resource management.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [target] --tier pro
```

**What it does:**
1. Validates Pro+ license
2. Runs 60 container security patterns (DF, SC, HC, RS categories)
3. Detects missing health checks and readiness probes
4. Identifies resource limit gaps and unbounded containers
5. Full category breakdown reporting

#### `containerlint scan --format json [directory]`
Generate JSON output for CI/CD integration.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format json
```

#### `containerlint scan --format html [directory]`
Generate HTML report for browser viewing.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --format html
```

#### `containerlint scan --category HC [directory]`
Filter scan to a specific check category (DF, SC, HC, RS, NW, OR).

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --category HC
```

### Team Tier ($39/user/month -- requires CONTAINERLINT_LICENSE_KEY with team tier)

#### `containerlint scan --tier team [directory]`
Full scan with all 90 patterns across all 6 categories including networking and orchestration.

**How to execute:**
```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --tier team
```

**What it does:**
1. Validates Team+ license
2. Runs all 90 patterns across 6 categories
3. Includes networking checks (host networking, exposed ports, insecure registries)
4. Includes orchestration checks (compose anti-patterns, missing restart policies)
5. Full category breakdown with per-file results

#### `containerlint scan --verbose [directory]`
Verbose output showing every matched line and pattern details.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" --path [directory] --verbose
```

#### `containerlint status`
Show license and configuration information.

```bash
bash "<SKILL_DIR>/scripts/dispatcher.sh" status
```

## Check Categories

ContainerLint detects 90 container security anti-patterns across 6 categories:

| Category | Code | Patterns | Description | Severity Range |
|----------|------|----------|-------------|----------------|
| **Dockerfile Best Practices** | DF | 15 | Missing USER directive, ADD instead of COPY, latest tag, missing .dockerignore patterns, multiple FROM without alias | medium -- high |
| **Security Context** | SC | 15 | Privileged mode, running as root, exposed secrets, capability escalation, no seccomp profile | high -- critical |
| **Health & Readiness** | HC | 15 | No HEALTHCHECK, missing readiness probes, no liveness checks, no startup probes | medium -- high |
| **Resource Management** | RS | 15 | No resource limits, no memory limits, no CPU limits, unbounded storage, no ephemeral storage limits | medium -- high |
| **Networking & Exposure** | NW | 15 | Exposing all ports, host networking, no network policy, publishing on 0.0.0.0, insecure registries | medium -- critical |
| **Orchestration & Compose** | OR | 15 | No restart policy, no replicas, hardcoded IPs in compose, no volume mounts for secrets, latest tag in compose | low -- high |

## Tier-Based Pattern Access

| Tier | Patterns | Categories |
|------|----------|------------|
| **Free** | 30 | DF, SC |
| **Pro** | 60 | DF, SC, HC, RS |
| **Team** | 90 | DF, SC, HC, RS, NW, OR |
| **Enterprise** | 90 | DF, SC, HC, RS, NW, OR + priority support |

## Scoring

ContainerLint uses a deductive scoring system starting at 100 (perfect):

| Severity | Point Deduction | Description |
|----------|-----------------|-------------|
| **Critical** | -25 per finding | Severe security vulnerability (privileged mode, exposed secrets) |
| **High** | -15 per finding | Significant security problem (running as root, no resource limits) |
| **Medium** | -8 per finding | Moderate concern (latest tag, missing health check) |
| **Low** | -3 per finding | Informational / best practice suggestion |

### Grading Scale

| Grade | Score Range | Meaning |
|-------|-------------|---------|
| **A** | 90-100 | Excellent container security |
| **B** | 80-89 | Good security with minor issues |
| **C** | 70-79 | Acceptable but needs improvement |
| **D** | 60-69 | Poor container security |
| **F** | Below 60 | Critical security problems |

- **Pass threshold:** 70 (Grade C or better)
- Exit code 0 = pass (score >= 70)
- Exit code 1 = fail (score < 70)

## Configuration

Users can configure ContainerLint in `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "containerlint": {
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
- If license key is invalid or expired, show clear message with link to https://containerlint.pages.dev/renew
- If a file is binary, skip it automatically with no warning
- If no scannable files found in target, report clean scan with info message
- If an invalid category is specified with --category, show available categories

## When to Use ContainerLint

The user might say things like:
- "Scan my code for Dockerfile issues"
- "Check my container security"
- "Find privileged containers"
- "Detect missing health checks"
- "Are there any hardcoded secrets in my Docker files?"
- "Check for missing resource limits"
- "Audit my container security practices"
- "Find insecure Docker configurations"
- "Check for missing network policies"
- "Scan for container anti-patterns"
- "Run a container security audit"
- "Generate a container security report"
- "Check if my containers have proper resource limits"
- "Find containers running as root"
- "Check my docker-compose for anti-patterns"
