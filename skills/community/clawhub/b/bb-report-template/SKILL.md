---
name: bb-report-template
description: Generate professional bug bounty reports for HackerOne, Bugcrowd, and other platforms. Pre-filled templates with CWE mapping, reproduction steps, and severity assessment.
metadata: {"openclaw":{"emoji":"🐛","requires":{"bins":["python3"]}}}
---

# Bug Bounty Report Template Generator

Generate professional, platform-ready bug bounty reports. Supports HackerOne, Bugcrowd, and generic formats with automatic CWE mapping and severity assessment.

## Quick Start

```bash
python3 {baseDir}/scripts/generate-report.py --platform hackerone --title "XSS in Profile Page" --severity medium
python3 {baseDir}/scripts/generate-report.py --platform bugcrowd --type idor --target example.com
```

## Options

- `--platform PLATFORM` — Target platform: `hackerone`, `bugcrowd`, `generic` (default: generic)
- `--type TYPE` — Vulnerability type: `xss`, `idor`, `sqli`, `ssrf`, `rce`, `auth-bypass`, `info-disclosure`, `csrf`, `redirect`, `custom`
- `--title TITLE` — Report title
- `--severity LEVEL` — `critical`, `high`, `medium`, `low`, `info`
- `--target DOMAIN` — Target domain/application
- `--output FILE` — Output file path (default: stdout)
- `--template TEMPLATE` — Custom template file

## Features

- Automatic CWE mapping for common vulnerability types
- CVSS score calculation helper
- Pre-formatted reproduction steps sections
- Impact assessment templates
- Mitigation suggestions
- Scope validation reminders

## Example Output Structure

```
# [Title]

## Summary
[Brief description]

## Steps to Reproduce
1. Navigate to...
2. Intercept request...
3. Modify parameter...

## Impact
[Business impact description]

## Remediation
[Suggested fix]

## References
- CWE-XXX: [Description]
- CVSS: [Score]
```
