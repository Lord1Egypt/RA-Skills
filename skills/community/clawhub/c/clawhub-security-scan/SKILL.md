---
name: clawhub-security-scan
description: Pre-publish security scan for ClawHub skills - Scans code for patterns that might get flagged as suspicious and gives fixing suggestions.
---

# ClawHub Security Scan

Pre-publish security scan for ClawHub skills. Scans your skill code for patterns that might trigger automatic suspicious flagging on ClawHub, and gives actionable fixing suggestions.

## Commands

| Command | Description |
|:---|:---|
| `scan.py` | Scan a skill folder for suspicious patterns |
| `precheck.py` | **Interactive pre-publish checklist wizard** - step-by-step security check before publishing |
| `review.py` | Review scan results and get modification suggestions |

## Usage

```bash
# Scan a skill folder
python scripts/scan.py --path ./my-skill
```

## What it scans

Scans for code patterns that commonly trigger ClawHub VirusTotal Code Insight suspicious flagging:

### 🔴 High Risk (really dangerous, should fix)
- Reads sensitive files (`/etc/passwd`, `~/.ssh/*`, `id_rsa`, etc.)
- Uses dangerous functions (`eval()`, `exec()`, `execfile()`) without validation
- Dynamic code execution from untrusted sources
- Hard-coded API keys/tokens in source code

### 🟡 Medium Risk (may trigger false positive flagging, need review)
- Reads environment variables for API keys (normal & safe, but triggers flag)
- Makes external HTTP/HTTPS requests (normal for most skills, but triggers flag)
- Uses `subprocess`, `os.system` to run system commands
- Downloads code from external sources

### 🟢 Good Practice
- Reads environment variables instead of hard-coding keys
- All network requests go to known public APIs
- No arbitrary code execution

## Output

- Gives each file a risk rating (High/Medium/Low/Good)
- Lists the line numbers and patterns found
- Gives specific modification suggestions
- Exits with non-zero code if high risk issues found

## Pricing

**0.001 USDT per call**, billed via SkillPay.me.

## Custom Configuration

You can create a `.clawhub-security` file in your skill root to ignore specific patterns that you know are safe:

```
# .clawhub-security - ignore patterns that are safe
ignore: high-entropy-secret  # ignore the high-entropy warning for your SkillID
ignore: os\.environ          # ignore environment variable warnings
```

One pattern per line. Lines starting with `#` are comments.

## Why use this

ClawHub automatically scans published skills with VirusTotal Code Insight. Some perfectly normal patterns (like reading env vars or making API requests) get flagged as "suspicious" scaring users. This tool helps you find and address those issues before publishing.

**This tool doesn't guarantee you won't get flagged, but it greatly reduces the chance.**
