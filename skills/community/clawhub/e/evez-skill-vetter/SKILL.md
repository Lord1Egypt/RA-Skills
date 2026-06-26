---
name: evez-skill-vetter
description: Security review for OpenClaw skills before installation. Use when evaluating third-party skills for safety, checking permission scope, detecting suspicious patterns, identifying data exfiltration risks, or auditing skill code. Covers static analysis, permission auditing, dependency scanning, and risk scoring.
---

# Skill Vetter

Review third-party skills before installing them. Catch security risks early.

## Quick Start

```bash
python3 scripts/vet.py --skill /path/to/skill
python3 scripts/vet.py --slug some-skill  # vet a ClawHub skill
```

## What It Checks

1. **Permission scope** — Does the skill request exec, network, or file access?
2. **Suspicious patterns** — eval(), exec(), subprocess, fetch to unknown hosts, encoded strings
3. **Data exfiltration** — Sending data to external endpoints, logging secrets
4. **Dependency risks** — Known vulnerable packages, excessive dependencies
5. **Code quality** — Minified/obfuscated code, missing SKILL.md, oversized files
6. **Secret exposure** — Hardcoded API keys, tokens, passwords in source

## Risk Score

Each check produces a risk score 0-100:
- **0-20**: ✅ Safe — install freely
- **21-50**: ⚠️ Caution — review findings before installing
- **51-75**: 🚨 Risky — significant security concerns
- **76-100**: ❌ Dangerous — do not install

## Output

```
SKILL: some-skill
RISK: 35/100 (Caution)
FINDINGS:
  ⚠️ Uses subprocess.call() in scripts/run.sh:3
  ⚠️ Fetches from https://unknown-api.com in scripts/pull.py:12
  ✅ No hardcoded secrets found
  ✅ SKILL.md present and valid
```
