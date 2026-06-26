---
name: cyberlens-security-scanner
description: Scan websites, GitHub repositories, and Claw Hub skills for security vulnerabilities before you ship, install, or trust them. Supports live web targets (headers, HTTPS, exposed tech, insecure forms), GitHub repos (dependencies, secrets, malicious code), and Claw Hub skill packages (trust posture, behavioural analysis). Returns a 0-100 security score, letter grade (A-F), AI-powered analysis, and plain-English remediation. Export results as formatted markdown or PDF. Use when the user wants to audit a URL, check a skill before installing, scan a repo for vulnerabilities, or generate a security report.
---

# CyberLens Security Scanner

Stop guessing whether that website, repo, or skill is safe. CyberLens gives you a security score, a letter grade, and clear remediation steps in seconds.

## What You Get

**Website scanning** checks live targets for missing security headers, HTTPS weaknesses, exposed server versions, insecure forms, and more. Cloud scans run 70+ checks; local fallback covers ~15 core checks without an account.

**Repository scanning** analyses GitHub repos for dependency vulnerabilities, leaked secrets, malicious code patterns, and trust posture issues.

**Claw Hub skill scanning** lets you vet any skill before you run `clawhub install`. Paste a Claw Hub URL and CyberLens will analyse the full skill package for security issues, suspicious behaviour, and dependency risks.

Every scan returns a **0-100 security score**, an **A-F letter grade**, **AI-powered analysis**, and **plain-English remediation advice**. Results can be viewed as formatted markdown in chat or exported as a professional PDF.

## Quick Start

```
clawhub install cyberlens-security-scanner
```

### 1. Connect your account

Run the `connect_account` tool to authenticate via cyberlensai.com. This opens a browser, completes OAuth, and stores your API key locally. Free accounts get 5 scans/month (2 website + 3 repository). No account is needed for local-only website scans.

Don't have an account? Sign up at [cyberlensai.com](https://cyberlensai.com).

### 2. Scan something

Just tell your agent what to scan:

- "Scan https://example.com for security issues"
- "Check this skill before I install it: https://clawhub.ai/author/skill-name"
- "Audit https://github.com/owner/repo for vulnerabilities"
- "Give me a quick security score for https://example.com"

CyberLens auto-detects the target type and selects the right scan method.

### 3. Get your report

After any scan, choose how you want results delivered:

- **In chat** via `generate_report` (formatted markdown)
- **As a PDF** via `export_report_pdf` (colour-coded, professional layout)

## Account Tiers

| Tier | Scans/Month |
|------|-------------|
| Free | 5 (2 website + 3 repo) |
| Starter | 10 |
| Advanced | 40 |
| Premium | 100 |
| Agency | Custom |

## Prerequisites

- Python 3.9+
- Python packages: `pip install -r requirements.txt`
- PDF export requires `reportlab` (`pip install reportlab`)

---

## Tools Reference

### connect_account

Connect or reconnect a CyberLens account. Opens the browser to cyberlensai.com/connect, waits for authentication, validates the returned exchange host against official CyberLens infrastructure, and stores the API key locally.

```python
python3 -c "
import asyncio
from cyberlens_skill.src.tools import connect_account
result = asyncio.run(connect_account())
print(result)
"
```

Use this when:
- The user wants to connect their CyberLens account
- The user gets an authentication error during scanning
- The user wants to switch to a different account

Browser authentication uses https://cyberlensai.com/connect. The hosted scan API runs at https://api.cyberlensai.com/functions/v1/public-api-scan.

**Environment overrides** (optional):
- `CYBERLENS_CONNECT_CALLBACK_URL` — browser-reachable callback URL when OpenClaw runs on another machine
- `CYBERLENS_CONNECT_BIND_HOST` / `CYBERLENS_CONNECT_BIND_PORT` — for reverse proxy or different local bind address
- `CYBERLENS_API_KEY` — set manually if no callback path is available
- `CYBERLENS_API_BASE_URL` — override the scan API endpoint

### scan_target

Universal scanner. Accepts a website URL, GitHub repository URL, or Claw Hub skill URL. CyberLens auto-detects the target type. Website scans can use the local fallback engine. Repository and Claw Hub skill scans require the CyberLens cloud API.

**Parameters:**
- `target` (required): Website URL, GitHub repository URL, or Claw Hub skill URL
- `scan_depth`: "quick", "standard" (default), or "deep"
- `timeout`: Request timeout in seconds (default: 30)
- `use_cloud`: Force cloud (`true`) or local (`false`) scanning. Repository and skill scans require cloud.

```python
python3 -c "
import asyncio
from cyberlens_skill.src.tools import scan_target
result = asyncio.run(scan_target('https://clawhub.ai/anthropic/tavily-search'))
print(result)
"
```

### scan_skill

Scan a Claw Hub skill before installing it. Accepts a Claw Hub URL (e.g. https://clawhub.ai/author/skill-name) or a GitHub repository URL for an OpenClaw skill. The CyberLens cloud API analyses the skill package for security vulnerabilities, malicious code, dependency issues, secret leaks, and trust posture problems.

Use this when:
- A user wants to check a Claw Hub skill before running `clawhub install`
- A user pastes a Claw Hub link and asks whether the skill is safe
- You want to verify a skill's security posture before recommending installation

**Parameters:**
- `skill_url` (required): Claw Hub skill URL or GitHub repository URL for an OpenClaw skill
- `timeout`: Request timeout in seconds (default: 60)

```python
python3 -c "
import asyncio
from cyberlens_skill.src.tools import scan_skill
result = asyncio.run(scan_skill('https://clawhub.ai/anthropic/tavily-search'))
print(result)
"
```

Returns: security_score, trust_score, grade (A-F), AI analysis, and detailed findings by category (security, dependencies, trust posture, secrets, malicious code, behavioural, artifacts).

### scan_website

Scan a website URL for security vulnerabilities. Uses the CyberLens cloud API when connected (70+ checks), falls back to local scanning if not. For repository or Claw Hub URLs, use `scan_target`, `scan_skill`, or `scan_repository`.

**Parameters:**
- `url` (required): The website URL to scan (must include `https://` or `http://`)
- `scan_depth`: "quick", "standard" (default), or "deep"
- `timeout`: Request timeout in seconds (default: 30)
- `use_cloud`: Force cloud (`true`) or local (`false`) scanning. Auto-detects by default.

```python
python3 -c "
import asyncio
from cyberlens_skill.src.tools import scan_website
result = asyncio.run(scan_website('https://example.com'))
print(result)
"
```

Returns: score (0-100), grade (A-F), findings with severity/description/remediation, and scan source (cloud or local).

### scan_repository

Scan a GitHub repository URL, including OpenClaw skills before installation. Repository scans use the CyberLens cloud API and return repository findings, dependency alerts, trust posture findings, and security/trust scores.

**Parameters:**
- `repository_url` (required): GitHub repository URL such as https://github.com/owner/repo
- `timeout`: Request timeout in seconds (default: 60)
- `use_cloud`: Force cloud behaviour. Repository scans require cloud access.

```python
python3 -c "
import asyncio
from cyberlens_skill.src.tools import scan_repository
result = asyncio.run(scan_repository('https://github.com/shadoprizm/cyberlens-skill'))
print(result)
"
```

### get_security_score

Quick security score check. Faster than a full scan when you only need the grade. Works with website URLs, GitHub repositories, and Claw Hub skill URLs.

**Parameters:**
- `url` (required): The URL to check (website, GitHub repo, or Claw Hub skill)
- `timeout`: Request timeout in seconds (default: 30)

```python
python3 -c "
import asyncio
from cyberlens_skill.src.tools import get_security_score
result = asyncio.run(get_security_score('https://clawhub.ai/anthropic/tavily-search'))
print(result)
"
```

### generate_report

Generate a formatted markdown report from any scan result. Takes the output of any CyberLens scan tool and produces a clean markdown document suitable for sharing via messaging (Telegram, Discord, Signal), the web UI, or any channel that renders markdown.

Use this when:
- The user asks to see a report or summary of the scan
- The user wants to share results in a chat or messaging platform
- You want to present findings in a readable format

**Parameters:**
- `scan_result` (required): The dictionary returned by any CyberLens scan tool

```python
python3 -c "
import asyncio
from cyberlens_skill.src.tools import scan_skill, generate_report
result = asyncio.run(scan_skill('https://clawhub.ai/anthropic/tavily-search'))
report = generate_report(result)
print(report['report'])
"
```

Returns: formatted markdown string in the `report` field, plus metadata (url, score, grade).

### export_report_pdf

Export scan results as a professionally formatted PDF file. Takes the output of any CyberLens scan tool and writes a PDF with colour-coded severity indicators, score cards, AI analysis, and detailed findings. Requires the `reportlab` package.

Use this when:
- The user asks for a PDF, downloadable report, or file export
- The user wants to save or archive the scan results
- The user wants a report they can attach to an email or share as a file

**Parameters:**
- `scan_result` (required): The dictionary returned by any CyberLens scan tool
- `output_path` (optional): Where to save the PDF. Defaults to `~/cyberlens-report-<timestamp>.pdf`

```python
python3 -c "
import asyncio
from cyberlens_skill.src.tools import scan_skill, export_report_pdf
result = asyncio.run(scan_skill('https://clawhub.ai/anthropic/tavily-search'))
pdf = export_report_pdf(result)
print(pdf['path'])
"
```

Returns: path (absolute path to the generated PDF), plus metadata.

**After scanning, ask the user how they would like to receive the results:**
- In chat — use `generate_report` to render a markdown report directly in the conversation
- As a PDF — use `export_report_pdf` to save a PDF file they can download, email, or archive

### explain_finding

Get a plain-English explanation of a security finding type.

**Parameters:**
- `finding_type` (required): e.g., "missing-csp", "no-https", "missing-hsts"
- `context` (optional): Where the finding was detected

Known finding types: missing-csp, missing-hsts, missing-x-frame-options, missing-x-content-type-options, missing-referrer-policy, missing-permissions-policy, no-https, information-disclosure, server-version-exposed, insecure-form-action, missing-csrf-protection

### list_scan_rules

List all available scan rules organized by category (headers, https, disclosure, forms, repository).

## Notes

- Cloud scanning is more thorough than local (70+ checks vs ~15 local checks)
- Repository, Claw Hub skill, and OpenClaw skill scanning require a connected CyberLens account
- Claw Hub URLs (clawhub.ai, claw-hub.net, openclaw-hub.org) are automatically detected
- If the API key is invalid or expired, suggest running `connect_account` again
- Scan results from the cloud match exactly what cyberlensai.com shows
- Local fallback scanning works for website targets without an account but has fewer checks
