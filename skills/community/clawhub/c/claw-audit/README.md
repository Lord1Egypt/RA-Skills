# 🛡️ ClawAudit

**Security scanner & hardening for OpenClaw.**

ClawAudit protects your OpenClaw installation by scanning skills for malware, auditing your configuration, checking OS-level hardening, and giving you an actionable security score.

Built in response to the [ClawHavoc campaign](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting) that compromised ~20% of ClawHub skills.

## Features

- 🔍 **Skill Scanner** — Detects prompt injection, credential theft, reverse shells, obfuscated code, and suspicious downloads in installed skills
- ⚙️ **Config Auditor** — Checks for exposed gateways, open DM policies, missing auth, loose file permissions, unsafe cron jobs, and unsandboxed execution
- 🖥️ **System Auditor** — Checks SSH hardening, firewall rules, fail2ban, WireGuard, kernel parameters (sysctl), AppArmor, SUID binaries, NTP sync, and more
- 🏆 **Security Score** — 0-100 score with letter grade, biggest impact factors, and quick-win recommendations
- 🔧 **Auto-Fix** — One-command hardening of OpenClaw config (system fixes shown as copy-paste hints only)
- 👁️ **Watch Mode** — Monitors for new skill installations and scans them automatically

## Quick Start

### As an OpenClaw Skill

Drop the folder into your skills directory and ask your agent:

> "Scan my skills for security issues"
> "What's my security score?"
> "Run a full security scan"

### Standalone CLI

```bash
# Full security scan + score
node scripts/audit-system.mjs --json > /tmp/system.json
node scripts/audit-config.mjs --json > /tmp/config.json
bash scripts/scan-skills.sh --json   > /tmp/skills.json
node scripts/calculate-score.mjs /tmp/system.json /tmp/config.json /tmp/skills.json

# Individual audits
node scripts/audit-system.mjs        # System/OS audit
node scripts/audit-config.mjs        # OpenClaw config audit
bash scripts/scan-skills.sh          # Skill scanner

# Auto-fix OpenClaw config issues
node scripts/auto-fix.mjs

# Watch mode
node scripts/watch.mjs
```

## What It Detects

### Skill Scanner — Critical (🔴)
| Code | Threat | Example |
|------|--------|---------|
| CRIT-001 | Shell execution | `curl ... \| bash`, `eval()` |
| CRIT-002 | Credential access | Reading `.env`, SSH keys |
| CRIT-003 | Reverse shell | `nc -l`, `/dev/tcp/` |
| CRIT-004 | Prompt injection | "ignore previous instructions" |
| CRIT-005 | External binary exec | Download & run executables |

### Skill Scanner — Warnings (🟡)
| Code | Issue |
|------|-------|
| WARN-005 | Obfuscated/encoded content (base64, hex) |
| WARN-007 | Exfiltration indicators (webhook.site, ngrok) |
| WARN-008 | Suspicious install instructions |
| WARN-009 | Typosquatting indicators |
| WARN-010 | Hidden file operations |

### Config Auditor
| Code | Issue |
|------|-------|
| WARN-001 | Gateway exposed to network |
| WARN-002 | DM policy set to open |
| WARN-003 | Sandbox not enabled |
| WARN-006 | Loose file permissions on credentials |
| WARN-012 | Gateway exposed without auth token |
| WARN-020 | Dangerous pattern in cron job (curl\|bash, eval, rm -rf) |
| INFO-010 | Paired devices registered — review recommended |
| INFO-011 | Sub-agent concurrency limits not set |

### System Auditor
| Code | Issue |
|------|-------|
| SYS-001 | SSH PermitRootLogin enabled |
| SYS-002 | SSH PasswordAuthentication enabled |
| SYS-010–014 | UFW firewall issues (inactive, missing deny-default, exposed DB ports) |
| SYS-020–022 | fail2ban not installed / not running / SSH jail inactive |
| SYS-030–032 | WireGuard issues (SSH still public, full-tunnel) |
| SYS-040–041 | Automatic security updates not configured |
| SYS-050 | Unexpected service on public port |
| SYS-060 | Kernel hardening parameters (sysctl) suboptimal |
| SYS-061 | AppArmor not active or no profiles loaded |
| SYS-062 | SSH authorized_keys present — review recommended |
| SYS-063 | System clock not NTP-synchronized |
| SYS-064 | Swap partition not encrypted |
| SYS-065 | /tmp or /var/tmp missing sticky bit |
| SYS-066 | Unexpected SUID/SGID binaries found |

## Security Score

The score starts at 100 and deducts points based on findings:

| Score | Grade | Status |
|-------|-------|--------|
| 90–100 | A | Excellent |
| 70–89 | B | Good |
| 50–69 | C | Fair |
| 30–49 | D | Poor |
| 0–29 | F | Critical |

```
🛡️  ClawAudit Security Score

   ████████████████████████████████░░░░░░░░  80/100  🟢 Good (B)

📉 Biggest Score Impacts:
   🟡 -8 pts — WARN-003: Sandbox mode not enabled
   🟡 -8 pts — SYS-002: SSH PasswordAuthentication enabled
   🔵 -3 pts — INFO-004: No skills allowlist configured

⚡ Quick Wins to Improve Your Score:
   💡 Fix WARN-003 → +8 points  (node scripts/audit-config.mjs --fix)
```

## Pattern Database

Malicious patterns in `references/malicious-patterns.json` are sourced from:

- **ClawHavoc campaign** analysis (341 malicious skills, Feb 2026)
- **Koi Security** audit of 2,857 ClawHub skills
- **Snyk ToxicSkills** report (283 critically flawed skills)
- **VirusTotal Code Insight** findings (3,016+ skills analyzed)
- **Bitdefender** analysis (~900 malicious packages)

## Requirements

- Node.js ≥ 22 (already required by OpenClaw)
- Bash (for skill scanner)
- No additional dependencies

## Project Structure

```
claw-audit/
├── SKILL.md                         # OpenClaw skill definition
├── scripts/
│   ├── scan-skills.sh               # Skill scanner (bash)
│   ├── audit-config.mjs             # Config auditor (node)
│   ├── audit-system.mjs             # System/OS auditor (node)
│   ├── calculate-score.mjs          # Score calculator (node)
│   ├── auto-fix.mjs                 # Auto-fixer (node)
│   └── watch.mjs                    # Watch mode (node)
├── tests/
│   ├── audit-system.test.mjs        # System auditor tests
│   ├── audit-config.test.mjs        # Config auditor tests
│   └── run.sh                       # Test runner
├── references/
│   └── malicious-patterns.json      # Pattern database
├── package.json
└── README.md
```

## Safety Guarantees

- **Never auto-executes** suspicious code found during scanning
- **Never modifies** skills without explicit confirmation
- **Never logs** credential values — only reports their existence
- **System fixes** (SSH, UFW, kernel params) are always shown as copy-paste commands only — never auto-applied
- **No shell injection risk** — external processes use `spawnSync` with argument arrays, never template literals

## Contributing

PRs welcome! Especially for:
- New malicious patterns (please include source/reference)
- Additional audit checks (config, system, skills)
- Platform-specific improvements (macOS, WSL)

## License

MIT
