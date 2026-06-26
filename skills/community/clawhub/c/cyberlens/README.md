---
name: cyberlens-security-scanner
description: Scan websites, GitHub repositories, and Claw Hub skills for security vulnerabilities before you ship, install, or trust them. Supports live web targets (headers, HTTPS, exposed tech, insecure forms), GitHub repos (dependencies, secrets, malicious code), and Claw Hub skill packages (trust posture, behavioural analysis). Returns a 0-100 security score, letter grade (A-F), AI-powered analysis, and plain-English remediation. Export results as formatted markdown or PDF. Use when the user wants to audit a URL, check a skill before installing, scan a repo for vulnerabilities, or generate a security report.
---

# CyberLens Security Scanner

[![Open CLAW](https://img.shields.io/badge/Open%20CLAW-Native%20Skill-blue)](https://openclaw.ai)
[![Claw Hub](https://img.shields.io/badge/Claw%20Hub-Available-brightgreen)](https://clawhub.ai)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB)](https://www.python.org/downloads/)
[![CyberLens](https://img.shields.io/badge/CyberLens-Powered-orange)](https://cyberlensai.com)

Stop guessing whether that website, repo, or skill is safe. CyberLens gives you a security score, a letter grade, and clear remediation steps in seconds.

## What You Get

**Website scanning** has two honest modes: a **local quick scan** without an account and a **full cloud scan** when connected. The local quick scan covers ~15 core checks; the cloud scan runs 70+ checks with richer analysis.

**Repository scanning** analyses GitHub repos for dependency vulnerabilities, leaked secrets, malicious code patterns, and trust posture issues.

**Claw Hub skill scanning** downloads the skill package, extracts it, and analyses the actual source code for dangerous patterns, hardcoded secrets, permission issues, and dependency risks. Paste a Claw Hub URL or a direct download link and CyberLens handles the rest. No account required for skill scanning.

Every scan returns a **0-100 security score**, an **A-F letter grade**, and **plain-English remediation advice**. Results can be viewed as formatted markdown in chat or exported as a professional PDF.

## Quick Start

```
clawhub install cyberlens-security-scanner
```

### 1. Scan something

Just tell your agent what to scan:

- "Check this skill before I install it: https://clawhub.ai/author/skill-name"
- "Scan https://example.com for security issues"
- "Audit https://github.com/owner/repo for vulnerabilities"
- "Give me a quick security score for https://example.com"

CyberLens auto-detects the target type and selects the right scan method. Website quick scans and Claw Hub skill scans work immediately with no account. Repository scans require a connected account.

### 2. Connect your account (for cloud scans)

Without an account, website scans use the local quick scanner and repository scans stay unavailable. Connect your account to upgrade website scans to the full cloud path and unlock repository scanning. The `connect_account` tool opens a browser, completes authentication, and stores your API key locally. Free accounts get 5 cloud scans/month (3 website + 2 repository). No credit card required. If you exhaust website cloud quota, the skill opens the CyberLens pricing page and falls back to the local quick scan automatically.

Don't have an account? Sign up at [cyberlensai.com](https://cyberlensai.com).

### 3. Get your report

After any scan, choose how you want results delivered:

- **In chat** via `generate_report` (formatted markdown)
- **As a PDF** via `export_report_pdf` (colour-coded, professional layout)

---

## Tools

### scan_skill

Scan a Claw Hub skill before installing it. This is the primary tool for vetting OpenClaw skills from the Claw Hub marketplace.

The skill package is downloaded, extracted, and analysed locally -- no CyberLens account required. Accepts Claw Hub URLs (the download link is resolved automatically) or direct download URLs.

**Parameters:**
- `skill_url` (required) -- Claw Hub skill URL (e.g. `https://clawhub.ai/skills/skill-name`) or direct download URL
- `timeout` -- Request timeout in seconds (default: 60)

**Example prompts:**
- "Scan https://clawhub.ai/skills/ontology before I install it"
- "Is this Claw Hub skill safe? https://clawhub.ai/author/skill-name"
- "Check this skill for malicious code before I install it"

**Returns:** Security score, grade (A-F), assessment, and detailed findings with file locations (dangerous code patterns, hardcoded secrets, manifest issues, dependency problems, external URLs).

### scan_target

Scan a live website, GitHub repository, or Claw Hub skill URL. CyberLens auto-detects the target type.

**Parameters:**
- `target` (required) -- Website URL, GitHub repository URL, or Claw Hub skill URL
- `scan_depth` -- Requested depth: `"quick"`, `"standard"` (default), or `"deep"`. Local website mode always uses the quick scan and warns when a deeper mode was requested.
- `timeout` -- Request timeout in seconds (default: 30)
- `use_cloud` -- Force cloud (`true`) or local (`false`). Repository scans require cloud.

**Example prompts:**
- "Scan https://clawhub.ai/author/skill-name for security issues"
- "Scan https://example.com for security issues"
- "Scan https://github.com/shadoprizm/cyberlens-skill before I install it"

### connect_account

Connect or reconnect your CyberLens account for cloud-powered scanning.

**Example prompt:** "Connect my CyberLens account"

### scan_website

Scan a website for security vulnerabilities. Uses the local quick engine without an account and the full cloud API when connected.

**Parameters:**
- `url` (required) -- The URL to scan (must include `https://` or `http://`)
- `scan_depth` -- Requested depth: `"quick"`, `"standard"` (default), or `"deep"`. Local website mode always uses the quick scan and warns when a deeper mode was requested.
- `timeout` -- Request timeout in seconds (default: 30)
- `use_cloud` -- Force cloud (`true`) or local (`false`). Auto-detects by default.

**Example prompts:**
- "Scan https://example.com for security issues"
- "Run the full cloud website scan for https://mysite.com"
- "Check if https://example.com is secure"

**Returns:** Score (0-100), grade (A-F), findings with severity/description/remediation, scan source (cloud or local), and explicit mode metadata showing whether this was a local quick scan or the full cloud scan.

### scan_repository

Scan a GitHub repository for security issues. Requires a connected CyberLens account.

**Parameters:**
- `repository_url` (required) -- GitHub repository URL (e.g. `https://github.com/owner/repo`)
- `timeout` -- Request timeout in seconds (default: 60)
- `use_cloud` -- Force cloud (`true`) or local (`false`). Repository scans require cloud access.

**Example prompts:**
- "Scan https://github.com/shadoprizm/cyberlens-skill for repo vulnerabilities"
- "Audit this OpenClaw skill before I install it"
- "Check my GitHub repo for security issues"

**Returns:** Repository security score, trust score, aggregated findings, and the underlying repository assessment sections from CyberLens cloud analysis.

### generate_report

Generate a formatted markdown report from any scan result. Suitable for sharing in Telegram, Discord, Signal, the web UI, or any channel that renders markdown.

**Parameters:**
- `scan_result` (required) -- The result returned by any CyberLens scan tool

**Example prompts:**
- "Show me the report in chat"
- "Give me a summary of the scan results"
- "Share the findings here"

**Returns:** A clean markdown report with score cards, AI analysis, summary, and severity-sorted findings.

### export_report_pdf

Export scan results as a professionally formatted PDF file with colour-coded severity indicators and full findings detail.

**Parameters:**
- `scan_result` (required) -- The result returned by any CyberLens scan tool
- `output_path` (optional) -- Where to save the PDF. Defaults to `~/cyberlens-report-<timestamp>.pdf`

**Example prompts:**
- "Export that scan as a PDF"
- "Give me a downloadable report"
- "Save the results as a PDF file"

**Returns:** Absolute path to the generated PDF file.

### get_security_score

Quick score check -- faster when you only need the grade. Supports websites, GitHub repositories, and Claw Hub skill URLs.

**Parameters:**
- `url` (required) -- The URL to check
- `timeout` -- Request timeout in seconds (default: 30)

**Example prompt:** "What's the security grade for https://clawhub.ai/author/skill-name?"

### explain_finding

Get a plain-English explanation of a security finding.

**Parameters:**
- `finding_type` (required) -- e.g., `"missing-csp"`, `"no-https"`, `"missing-hsts"`
- `context` (optional) -- Additional context about where the finding was detected

**Known finding types:** `missing-csp`, `missing-hsts`, `missing-x-frame-options`, `missing-x-content-type-options`, `missing-referrer-policy`, `missing-permissions-policy`, `no-https`, `information-disclosure`, `server-version-exposed`, `insecure-form-action`, `missing-csrf-protection`

### list_scan_rules

List all available detection rules organized by category (headers, HTTPS, disclosure, forms, repository).

---

## Cloud vs Local Scanning

| | Local | Cloud |
|---|---|---|
| Checks | ~15 core rules | 70+ rules |
| Account required | No | Yes |
| Results match website | No | Yes |
| Scan history | No | Yes |
| Claw Hub skill scanning | Yes (local analysis) | Yes (cloud analysis) |
| Repository scanning | No | Yes |
| AI-powered analysis | No | Yes |
| PDF report export | Yes (from any result) | Yes (from any result) |

When connected, cloud scanning is used by default for websites and repositories. If website cloud quota is exhausted, the skill opens the CyberLens pricing page and still falls back to a local quick website scan automatically. Claw Hub skill scanning downloads and analyses the skill package locally and does not require a cloud account.

## Account Tiers

| Tier | Website Scans | Repo/Skill Scans | Combined | Price |
|------|:---:|:---:|:---:|-------|
| **Free** | **3** | **2** | **5/month** | **Free** |
| Starter | 20 | 10 | 30/month | $12/mo |
| Advanced | 65 | 35 | 100/month | $25/mo |
| Premium | 175 | 75 | 250/month | $49/mo |
| Agency | 500 | 250 | 750/month | $149/mo |

**Get started free** -- 5 scans/month with no credit card required. Sign up at [cyberlensai.com](https://cyberlensai.com).

---

## Connecting Your Account

The first time you want the full cloud scan, tell your agent to "connect my CyberLens account" (or it will prompt you for cloud-only features). This runs the `connect_account` tool, which:

1. Opens your browser to [cyberlensai.com/connect](https://cyberlensai.com/connect)
2. You sign in or create a free account
3. A local callback server receives a short-lived connect code
4. The skill exchanges that code for your account key over HTTPS
5. The key is stored at `~/.openclaw/skills/cyberlens/config.yaml`

No copy-pasting required. The raw account key never appears in the browser callback URL. The skill only accepts HTTPS exchange URLs on official CyberLens hosts.

If you run out of cloud scans later, CyberLens opens the pricing page automatically and the tool response includes a direct upgrade URL.

You can also set the key via environment variable: `CYBERLENS_API_KEY`.

### Remote or Server Installs

If OpenClaw is running on a different machine than your browser, set a browser-reachable callback URL before running `connect_account`:

```bash
# Direct LAN or VPN callback
export CYBERLENS_CONNECT_CALLBACK_URL="http://10.0.0.5:54321/callback"

# Hosted HTTPS callback behind a reverse proxy
export CYBERLENS_CONNECT_CALLBACK_URL="https://openclaw.example.com/cyberlens/callback"
export CYBERLENS_CONNECT_BIND_HOST="127.0.0.1"
export CYBERLENS_CONNECT_BIND_PORT="54321"
```

If you do not want to expose a callback at all, set `CYBERLENS_API_KEY` manually instead.

---

## Installation

### Via Claw Hub

```
clawhub install cyberlens-security-scanner
```

### Manual

Copy or symlink into your OpenClaw skills folder:

```bash
# Symlink (recommended for development)
ln -s /path/to/cyberlens-skill ~/.openclaw/skills/cyberlens

# Or copy
cp -r /path/to/cyberlens-skill ~/.openclaw/skills/cyberlens
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

For reproducible installs with pinned versions:

```bash
pip install -r requirements.lock
```

OpenClaw auto-discovers the skill from the `SKILL.md` file on the next session.

### Prerequisites

- Python 3.9+
- PDF export requires `reportlab` (included in requirements.txt)

---

## Project Structure

```
cyberlens-skill/
  SKILL.md              # OpenClaw skill manifest (YAML frontmatter + instructions)
  skill.yaml            # Skill metadata and config schema
  requirements.txt      # Python dependencies
  requirements.lock     # Pinned direct dependencies for reproducible installs
  SECURITY.md           # Vulnerability reporting policy
  CONTRIBUTING.md       # Contribution workflow and expectations
  LICENSE               # Apache 2.0 license
  src/
    tools.py            # Tool implementations
    skill_scanner.py    # Local skill analyser (download, extract, scan, cleanup)
    scanner.py          # Local SecurityScanner (async, httpx + BeautifulSoup)
    api_client.py       # CyberLens cloud API client (async, exponential backoff)
    auth.py             # Browser-based connect flow with secure code exchange
    models.py           # Pydantic data models
```

## Dependencies

- `httpx` -- Async HTTP client
- `beautifulsoup4` -- HTML parsing (for local scanning)
- `pydantic` -- Data validation
- `pyyaml` -- Config file handling
- `reportlab` -- PDF report generation

## Security

Please review [SECURITY.md](SECURITY.md) before reporting vulnerabilities. Sensitive reports should not be filed as public issues.

## Related

| Repository | Description |
|------------|-------------|
| [cyberlens-mcp-server](https://github.com/shadoprizm/cyberlens-mcp-server) | MCP server for Claude Desktop, VS Code, and other AI assistants |
| [cyberlens-extension](https://github.com/shadoprizm/cyberlens-extension) | Chrome extension |
| [CyberLens](https://cyberlensai.com) | Full platform with browser-based scanning and dashboards |

## License

Apache 2.0 -- see [LICENSE](LICENSE).

---

Part of the [CyberLens](https://cyberlensai.com) open-source security platform.
