---
name: cyberlens
description: Scan websites, GitHub repositories, and Claw Hub skills for practical security issues using a local quick website scan and CyberLens cloud analysis when connected.
metadata: {"openclaw": {"requires": {"bins": ["python3"]}, "primaryEnv": "CYBERLENS_API_KEY", "emoji": "\ud83d\udd12", "homepage": "https://cyberlensai.com"}}
---

# CyberLens Security Scanner

Scan websites, GitHub repositories, and Claw Hub skills for practical security issues before you ship, install, or trust them. CyberLens can audit live web targets for missing headers, HTTPS weaknesses, exposed technologies, and insecure forms. It can scan GitHub repositories for dependency vulnerabilities, secret leaks, and malicious code. And it can scan Claw Hub skills directly from their Claw Hub URL — just paste a link like `https://clawhub.ai/author/skill-name` and CyberLens will analyse the skill package before you install it. Results include a 0-100 security score, letter grade (A-F), AI-powered analysis, and plain-English remediation advice. Reports can be shared as formatted markdown in chat or exported as a PDF.

## Prerequisites

- **Python 3.9+**: Required for script execution
- **Python Packages**:
  ```bash
  pip install -r requirements.txt
  ```

## First-Time Setup

Website quick scans and Claw Hub skill package scans work without an account. Connect a CyberLens account when the user wants the full cloud website scan or any repository scan. Run the `connect_account` tool. This opens a browser to cyberlensai.com where they sign in or create an account. A short-lived connect code is delivered through the callback, the skill exchanges that code for the real account key over HTTPS on official CyberLens hosts, and the key is stored at `~/.openclaw/skills/cyberlens/config.yaml`.

Browser authentication uses `https://cyberlensai.com/connect`. The hosted scan API runs at `https://api.cyberlensai.com/functions/v1/public-api-scan`. If the user needs to override the scan API endpoint explicitly, set `CYBERLENS_API_BASE_URL`.

If the user doesn't have a CyberLens account, direct them to https://cyberlensai.com to sign up. Free tier includes 5 scans/month (3 website + 2 repository). Repository scanning requires a connected account. If the user exhausts quota, the skill opens the pricing page and returns an upgrade URL in the tool result.

## Tools

### connect_account

Connect or reconnect a CyberLens account. Opens the browser to cyberlensai.com/connect, waits for authentication, validates the returned exchange host against official CyberLens infrastructure, and stores the API key locally.

```bash
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

If OpenClaw is running on another machine, set `CYBERLENS_CONNECT_CALLBACK_URL` to a browser-reachable callback URL before running `connect_account`. Use `CYBERLENS_CONNECT_BIND_HOST` and `CYBERLENS_CONNECT_BIND_PORT` when a reverse proxy or different local bind address is involved. If no callback path is available, the user can still set `CYBERLENS_API_KEY` manually. If the user prefers not to persist the key on disk, they can keep `CYBERLENS_API_KEY` only in the process environment.

### scan_target

Scan a live website, GitHub repository, or Claw Hub skill URL. CyberLens auto-detects the target type. Website scans use the local quick engine without an account and the full cloud path when connected. Repository scans require the CyberLens cloud API.

Parameters:
- `target` (required): Website URL, GitHub repository URL, or Claw Hub skill URL
- `scan_depth`: requested depth: "quick", "standard" (default), or "deep". Local website mode always uses the quick scan and warns when a deeper mode was requested.
- `timeout`: Request timeout in seconds (default: 30)
- `use_cloud`: Force cloud (true) or local (false) scanning. Repository and skill scans require cloud.

```bash
python3 -c "
import asyncio
from cyberlens_skill.src.tools import scan_target
result = asyncio.run(scan_target('https://clawhub.ai/anthropic/tavily-search'))
print(result)
"
```

### scan_skill

Scan a Claw Hub skill before installing it. Accepts a Claw Hub URL (e.g. `https://clawhub.ai/author/skill-name`) or a direct skill download URL. The skill package is downloaded and analysed locally for security vulnerabilities, malicious code, dependency issues, secret leaks, and trust posture problems.

Use this when:
- A user wants to check a Claw Hub skill before running `clawhub install`
- A user pastes a Claw Hub link and asks whether the skill is safe
- You want to verify a skill's security posture before recommending installation

Parameters:
- `skill_url` (required): Claw Hub skill URL or direct skill download URL
- `timeout`: Request timeout in seconds (default: 60)

```bash
python3 -c "
import asyncio
from cyberlens_skill.src.tools import scan_skill
result = asyncio.run(scan_skill('https://clawhub.ai/anthropic/tavily-search'))
print(result)
"
```

Returns: security_score, grade (A-F), local assessment, and detailed findings with file paths and recommendations.

### scan_website

Scan a website URL for security vulnerabilities. Uses the local quick scan without an account and the CyberLens cloud API when connected (70+ checks). For repository or Claw Hub URLs, use `scan_target`, `scan_skill`, or `scan_repository`.

Parameters:
- `url` (required): The website URL to scan (must include https:// or http://)
- `scan_depth`: requested depth: "quick", "standard" (default), or "deep". Local website mode always uses the quick scan and warns when a deeper mode was requested.
- `timeout`: Request timeout in seconds (default: 30)
- `use_cloud`: Force cloud (true) or local (false) scanning. Auto-detects by default.

```bash
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

Parameters:
- `repository_url` (required): GitHub repository URL such as `https://github.com/owner/repo`
- `timeout`: Request timeout in seconds (default: 60)
- `use_cloud`: Force cloud behaviour. Repository scans require cloud access.

```bash
python3 -c "
import asyncio
from cyberlens_skill.src.tools import scan_repository
result = asyncio.run(scan_repository('https://github.com/shadoprizm/cyberlens-skill'))
print(result)
"
```

### get_security_score

Quick security score check. Faster than a full scan when you only need the grade. Works with website URLs, GitHub repositories, and Claw Hub skill URLs.

Parameters:
- `url` (required): The URL to check (website, GitHub repo, or Claw Hub skill)
- `timeout`: Request timeout in seconds (default: 30)

```bash
python3 -c "
import asyncio
from cyberlens_skill.src.tools import get_security_score
result = asyncio.run(get_security_score('https://clawhub.ai/anthropic/tavily-search'))
print(result)
"
```

### generate_report

Generate a formatted markdown report from any scan result. Takes the output of `scan_target`, `scan_skill`, `scan_website`, or `scan_repository` and produces a clean markdown document suitable for sharing via messaging (Telegram, Discord, Signal), the web UI, or any channel that renders markdown.

Use this when:
- The user asks to see a report or summary of the scan
- The user wants to share results in a chat or messaging platform
- You want to present findings in a readable format

Parameters:
- `scan_result` (required): The dictionary returned by any CyberLens scan tool

```bash
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

Parameters:
- `scan_result` (required): The dictionary returned by any CyberLens scan tool
- `output_path` (optional): Where to save the PDF. Defaults to `~/cyberlens-report-<timestamp>.pdf`

```bash
python3 -c "
import asyncio
from cyberlens_skill.src.tools import scan_skill, export_report_pdf
result = asyncio.run(scan_skill('https://clawhub.ai/anthropic/tavily-search'))
pdf = export_report_pdf(result)
print(pdf['path'])
"
```

Returns: `path` (absolute path to the generated PDF), plus metadata.

After scanning, ask the user how they would like to receive the results:
1. **In chat** — use `generate_report` to render a markdown report directly in the conversation
2. **As a PDF** — use `export_report_pdf` to save a PDF file they can download, email, or archive

### explain_finding

Get a plain-English explanation of a security finding type.

Parameters:
- `finding_type` (required): e.g., "missing-csp", "no-https", "missing-hsts"
- `context` (optional): Where the finding was detected

Known finding types: missing-csp, missing-hsts, missing-x-frame-options, missing-x-content-type-options, missing-referrer-policy, missing-permissions-policy, no-https, information-disclosure, server-version-exposed, insecure-form-action, missing-csrf-protection

### list_scan_rules

List all available scan rules organized by category (headers, https, disclosure, forms, repository).

## Account Tiers

| Tier | Scans/Month |
|------|-------------|
| Free | 5 (3 website + 2 repo) |
| Starter | 10 |
| Advanced | 40 |
| Premium | 100 |
| Agency | Custom |

## Notes

- Cloud scanning is more thorough than local (70+ checks vs ~15 local checks)
- The local website engine is always a quick scan, even if the caller requested "standard" or "deep"
- Repository scanning requires a connected CyberLens account
- Claw Hub URLs (clawhub.ai, claw-hub.net, openclaw-hub.org) are automatically detected
- If the API key is invalid or expired, suggest running `connect_account` again
- Scan results from the cloud match exactly what cyberlensai.com shows
- Local fallback scanning works for website targets without an account and after website quota exhaustion, but it has fewer checks
- After any scan completes, ask the user whether they want results in chat (markdown) or as a PDF file
- PDF export requires the `reportlab` package — install with `pip install reportlab`
