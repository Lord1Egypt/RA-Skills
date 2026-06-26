# Agora Sentinel

**Security scanner for OpenClaw skills.** Checks any ClawHub skill for malware,
prompt injection, data theft, and dangerous permissions before you install it.

## Why?

In early 2026, over 2,300 malicious skills were found on ClawHub — including
wallet-stealing malware downloaded 14,000+ times. VirusTotal catches known
malware, but misses prompt injection, permission abuse, and novel attacks.

Agora Sentinel continuously scans **every skill on ClawHub** (30,000+) using
8 specialized scanners: static analysis, permission auditing, prompt injection
detection, ClickFix social engineering, two-stage loader detection, credential
theft patterns, infrastructure IOCs, and typosquat detection.

## How It Works

1. Install this skill
2. Before installing any other skill, your agent automatically checks
   its trust score against Sentinel's database
3. Dangerous skills get flagged before they can do harm

No API key needed. No account needed. Free forever.

## Commands

- **Auto-check**: Happens automatically before any `clawhub install`
- **Manual check**: "Is [skill-name] safe?" or "Check [skill-name] security"
- **Audit installed**: "Scan all my installed skills for security issues"
- **Browse dashboard**: https://checksafe.dev/dashboard/

## Trust Scores

| Badge | Score | Meaning |
|-------|-------|---------|
| TRUSTED | 90-100 | Strong safety record, well-established |
| CLEAN | 70-89 | No significant issues |
| CAUTION | 50-69 | Some concerns, review recommended |
| WARNING | 30-49 | Significant risks detected |
| DANGER | 0-29 | Malicious patterns detected, do not install |

## API

Free public API, no authentication:

```bash
# Quick badge check
curl https://checksafe.dev/api/v1/skills/{slug}/badge.json

# Full report
curl https://checksafe.dev/api/v1/skills/{slug}/report

# Search safe skills
curl https://checksafe.dev/api/v1/search?q=weather&min_tier=2
```

## About

Built by [Agora](https://checksafe.dev) — trust infrastructure for AI agents.
