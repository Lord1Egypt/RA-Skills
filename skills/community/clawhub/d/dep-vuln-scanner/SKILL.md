---
name: dep-vuln-scanner
description: Scan project dependencies for known security vulnerabilities using the OSV.dev API. Supports npm (package.json), Python/pip (requirements.txt), and Go (go.mod). Use when checking a project for vulnerable packages, auditing dependencies before deployment, or investigating CVEs in third-party libraries. No API key required.
---

# Dependency Vulnerability Scanner

Scan project dependencies against the OSV.dev vulnerability database. Zero config, no API keys.

## Quick Start

```bash
# Scan current directory (auto-detects project type)
python3 scripts/dep_vuln_scan.py .

# Scan a specific project
python3 scripts/dep_vuln_scan.py /path/to/project

# JSON output for CI/CD
python3 scripts/dep_vuln_scan.py . --json

# Scan only npm dependencies
python3 scripts/dep_vuln_scan.py . --ecosystem npm
```

## Supported Ecosystems

| File | Ecosystem |
|------|-----------|
| `package.json` | npm |
| `requirements.txt` | PyPI |
| `go.mod` | Go |

Multiple files in the same directory are scanned together.

## Output

- Color-coded severity: CRITICAL/HIGH (red), MEDIUM (yellow), LOW (green)
- Includes CVE aliases, vulnerability IDs, and descriptions
- Summary with total count and critical/high breakdown
- Exit code 1 if any vulnerabilities found (useful for CI gates)

## Flags

- `--json` — Machine-readable JSON output
- `--ecosystem <name>` — Filter by ecosystem (repeatable)
