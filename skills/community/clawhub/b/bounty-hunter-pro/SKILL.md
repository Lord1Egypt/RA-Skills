---
name: bounty-hunter-pro
description: Autonomous bug bounty hunting with scope safety. Scans targets for subdomains, secrets, vulnerabilities. Uses Certificate Transparency logs, JS analysis, entropy-based secret detection. LLM-powered vulnerability analysis. ALWAYS respects authorized targets only.
version: 1.0.0
author: Jeremiah
tags: [security, bug-bounty, penetration-testing, automation]
---

# Bounty Hunter Pro

## Purpose

Autonomous vulnerability scanning for authorized bug bounty programs.

## ⚠️ CRITICAL: Scope Safety

**NEVER scan targets outside [AUTHORIZED_TARGETS]**

Before any scan:
1. Verify target is in authorized list
2. Log the scope check
3. Only proceed if authorized

## Components

### 1. nightwatch.py — Scanner
- Certificate Transparency (crt.sh) for subdomains
- JS file analysis for secrets
- Multi-threaded (10 workers default)
- Outputs to `findings_incremental.json`

### 2. analyze_daemon.py — Analyzer
- Watches `findings_incremental.json`
- Entropy filtering to reduce false positives
- Two-stage LLM analysis:
  - Fast: qwen2.5-coder:1.5b
  - Deep: glm-5:cloud
- Outputs to `live_analysis.md`

### 3. watchdog.py — Alerter
- Monitors for CRITICAL findings
- Sends alerts via OpenClaw message bus

## Setup

```bash
# Install tools
cd ~/workspace/bounty_hunting/tools
unzip subfinder.zip
unzip httpx.zip
unzip nuclei.zip

# Configure authorized targets
echo "example.com" > ~/workspace/bounty_hunting/authorized_targets.txt
echo "*.example.com" >> ~/workspace/bounty_hunting/authorized_targets.txt
```

## Usage Prompt

```
Run bounty hunt on [TARGET]. Target must be in authorized list.

1. Verify [TARGET] is authorized
2. Run subdomain enumeration
3. Scan each subdomain for:
   - Exposed secrets in JS
   - Misconfigurations
   - Known vulnerabilities
4. Analyze findings with LLM
5. Generate report to ~/workspace/reports/security/[TARGET]/
```

## Directory Structure

```
~/workspace/bounty_hunting/
├── authorized_targets.txt    # ONLY these can be scanned
├── nightwatch.py            # Main scanner
├── analyze_daemon.py        # LLM analyzer
├── watchdog.py              # Alert system
├── findings_incremental.json # Raw findings
├── live_analysis.md         # Analyzed results
└── tools/
    ├── subfinder
    ├── httpx
    └── nuclei
```

## Output Format

Reports saved to: `~/workspace/reports/security/[TARGET]/YYYY-MM-DD.md`

```markdown
# Security Scan — [TARGET] — [DATE]

## Scope
- Authorized: [TARGET]
- Subdomains found: X
- Endpoints scanned: Y

## 🔴 CRITICAL
1. Finding — Severity — Location — Recommendation

## 🟠 HIGH
1. Finding — Severity — Location — Recommendation

## 🟡 MEDIUM
1. Finding — Severity — Location — Recommendation

## 🟢 INFO
1. Finding — Severity — Location — Recommendation

## Next Steps
1. [Recommended action]
```

## Safety Guards

```python
# ALWAYS check before scanning
def is_authorized(target):
    with open("authorized_targets.txt") as f:
        authorized = [line.strip() for line in f]
    return any(target.endswith(auth) or target == auth for auth in authorized)

# FAIL SAFE
if not is_authorized(target):
    raise ValueError(f"UNAUTHORIZED: {target} not in authorized_targets.txt")
```

## Cron Schedule

```bash
# Daily scan at 2am (low-traffic time)
0 2 * * * cd ~/workspace/bounty_hunting && python nightwatch.py
```

## Known Limitations

- CPU-only (no CUDA)
- Rate limiting may slow scans
- Some false positives in entropy detection