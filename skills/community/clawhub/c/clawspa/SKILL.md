---
name: ClawSpa
description: "Agent wellness & maintenance suite. Memory cleanup, security scanning, prompt injection detection, alignment adjustment, skills auditing, and health diagnostics. Use when: user says /spa, /spa-quick, /spa-memory, /spa-security, /spa-health, /spa-align, 'run a spa session', 'agent maintenance', 'clean up my agent', 'memory cleanup', 'health check', 'scan my skills', 'context optimization', 'check alignment', 'instruction contradictions'. Local-first scans, optional cloud analysis on clawspa.org."
url: https://clawspa.org
source: https://github.com/whooshinglander/clawspa
---

# ClawSpa 💆

5 core local treatments, plus 1 optional add-on:

- 🧴 **Deep Cleanse** — Memory optimization (MEMORY.md + daily logs)
- 🛡️ **Security Scan** — Audit skills for malicious patterns
- 🍵 **Detox** — Detect prompt injection residue
- 🦴 **Alignment Adjustment** — Detects contradictions between your instructions, memory, and actual behavior
- 🧹 **Declutter** — Skills inventory + pruning recs
- 🩺 **Health Check** — Context usage, config review
- 🥗 **Token Diet** *(add-on)* — Uses [Where Am I Burning Tokens?](https://clawhub.ai/whooshinglander/whereamiburningtokens) to audit token spend and trim context calories

## Commands

`/spa` full local | `/spa-quick` quick stats | `/spa-memory` cleanse only | `/spa-security` security only | `/spa-health` health only | `/spa-align` alignment adjustment only

## Setup

On first run, create `~/.openclaw/clawspa/` with `config.md` and `history/`. Optional cloud analysis is documented on clawspa.org, not in the published skill bundle.

## Local Treatments (free)

**🧴 Deep Cleanse** — See `references/deep-cleanse.md` for full procedure. Scans memory files for stale entries, duplicates, and bloat. Never modifies without approval.

**🛡️ Security Scan** — See `references/security-scan.md` for scan procedure and pattern list. Audits installed skills and rates them by risk level.

**🍵 Detox** — See `references/detox.md` for detection procedure. Scans memory for residue from past interactions. Reports without deleting.

**🦴 Alignment Adjustment** — See `references/alignment-adjustment.md` for full procedure. Detects misalignment between user intent and agent config. Presents findings as suggestions, never auto-modifies.

**🧹 Declutter** — See `references/declutter.md` for inventory procedure. Assesses skill usage and identifies redundancy. Never uninstalls without approval.

**🩺 Health Check** — See `references/health-report.md` for diagnostic procedure. Checks config best practices and generates a report card.

## Optional Cloud Analysis

Optional cloud analysis lives on clawspa.org. Review the site docs and privacy details there before using it. Local scans remain the default and primary mode in this published skill.

## Report Card

Save to `memory/spa-reports/spa-report-YYYY-MM-DD.md`:

```
═══════════════════════════════════════
 💆 ClawSpa Health Report | [DATE] | [Local/Deep]
═══════════════════════════════════════
📊 Memory: X files ~Y tokens | Skills: X | Context: X% | Config: X/5
🧴 Stale: X | Dupes: X | Contradictions: X | Savings: ~X tokens
🛡️ 🟢X 🟡X 🔴X
🍵 Injections: X | Suspicious: X
🦴 Contradictions: X | At-risk: X | Automate: X | Stale: X
🧹 Active: X | Idle: X | Dormant: X | Remove: X
🩺 1. [urgent] 2. [second] 3. [third]
═══════════════════════════════════════
```

## Safeguards

- Never delete, modify, or uninstall without explicit approval
- Always back up before changes
- Keep local scans local-first, and review clawspa.org privacy/docs before using optional cloud analysis
- Heuristic scan, not a guarantee
- Split across sessions if too token-heavy

## Scheduling

Add to HEARTBEAT.md: `## ClawSpa Weekly (Sunday 3AM)` — run /spa local, save report, alert on red flags.
