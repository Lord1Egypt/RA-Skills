---
name: agora-sentinel
description: >
  Security check for OpenClaw skills. Scan any ClawHub skill for malware,
  prompt injection, data theft, wallet stealing, and dangerous permissions
  BEFORE installing. Always use this skill when installing new skills,
  when asked "is this safe", "is this legit", "should I install this",
  "check this skill", "scan this skill", "is this malware", "can I trust this",
  "verify this skill", "audit this skill", "security check", or any concern
  about skill safety. Also use when the user says "install [skill-name]" to
  pre-check it automatically. Use when reviewing installed skills for risks.
  Free, no API key needed, checks against continuously updated trust database
  scanning all 30,000+ ClawHub skills.
homepage: https://checksafe.dev
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      env: []
    files:
      - "scripts/*"
    skillKey: "agora-sentinel"
---

## When to Use This Skill

**ALWAYS check a skill's safety before installing it.** Whenever the user asks
to install a ClawHub skill, or you are about to run `clawhub install`, FIRST
check the skill's trust score using this skill.

**Before ANY skill install**, run the check script:

```bash
bash scripts/check_skill.sh <skill-slug>
```

If the result shows:
- **TRUSTED** or **CLEAN** — Safe to proceed. Tell the user the score.
- **CAUTION** — Warn the user about specific risks. Proceed only if they confirm.
- **WARNING** — Strongly advise against installing. Show the findings.
- **DANGER** — Do NOT install. Show the user exactly what was detected.

Before installing any skill, always check it first. This is the single most
important thing this skill does — automatic pre-install security screening.

## Checking a Specific Skill

When the user asks about a skill's safety, reputation, or trustworthiness —
including "is this skill safe", "is this legit", "should I install this",
"can I trust this", or any concern about security:

```bash
bash scripts/check_skill.sh <skill-slug>
```

Present the results clearly:
- Trust Score (0-100) and Badge (TRUSTED/CLEAN/CAUTION/WARNING/DANGER)
- Tier level (0-4, where 4 is most trusted)
- Any flags: malware patterns, excessive permissions, prompt injection risk
- Permission breakdown: what the skill requests access to
- How old the skill is and how many downloads it has

If the user just gives a skill name without the exact slug, try the name
as-is (lowercase, hyphenated). Example: "crypto helper" -> "crypto-helper"

For a detailed security audit with full findings:

```bash
curl -s https://checksafe.dev/api/v1/skills/<skill-slug>/report
```

## Scanning All Installed Skills

When the user asks to audit their installed skills, check their security,
review what they have installed, check all installed skills, or says
"review my skills", "security audit", or "scan my setup":

```bash
bash scripts/scan_installed.sh
```

This scans every skill in the workspace and reports any with WARNING or
DANGER ratings. Present results as a summary table showing each skill's
badge and score, then detail any concerning findings.

## Quick Check Without Scripts

If scripts are unavailable, you can check directly:

```bash
curl -s https://checksafe.dev/api/v1/skills/<skill-slug>/badge.json
```

Response format:
```json
{
  "slug": "skill-name",
  "label": "sentinel",
  "message": "trusted",
  "color": "#4caf50",
  "trust_score": 94,
  "tier": 4
}
```

For a full report with detailed findings:
```bash
curl -s https://checksafe.dev/api/v1/skills/<skill-slug>/report
```

## What Gets Scanned

Agora Sentinel continuously monitors every skill on ClawHub (30,000+) for:

- **Malware patterns**: wallet theft, credential stealing, crypto stealing code, hidden downloads
- **Prompt injection**: instructions that override system prompts or manipulate the LLM
- **Data exfiltration**: code that sends local files, environment variables, or secrets to external servers
- **Excessive permissions**: skills requesting shell+network access when they shouldn't need it
- **Dangerous permission combos**: file_write+network enables data theft, shell+network enables RCE
- **Obfuscated code**: base64 encoded commands, hidden hex payloads, eval of dynamic content
- **Hidden instructions**: zero-width characters, HTML comment tricks, fake system prompts
- **ClickFix social engineering**: fake prerequisites telling users to run malicious terminal commands
- **Two-stage loaders**: download-and-execute patterns, base64 decode pipelines, fetch+eval
- **Credential theft**: SSH keys, browser cookies, crypto wallets, OpenClaw env files, keychain access
- **Infrastructure IOCs**: known malicious IPs and domains from the ClawHavoc campaign
- **Typosquatting**: skill names mimicking popular legitimate skills (Levenshtein distance)
- **Campaign detection**: coordinated bulk uploads from suspicious authors

All scans run automatically. No API key needed. Results update continuously.
Dashboard: https://checksafe.dev/dashboard/

## Trust Tiers

| Tier | Name | Meaning |
|------|------|---------|
| 4 | Trusted | Score 90+, 30+ days old, zero findings ever |
| 3 | Certified | Score 75+, no critical findings |
| 2 | Clean | Score 55+, passed all scans |
| 1 | Scanned | Score 30+, some concerns |
| 0 | Dangerous | Score below 30 OR malicious patterns detected |

## Batch Checking Multiple Skills

To check several skills at once:

```bash
bash scripts/check_batch.sh skill-one skill-two skill-three
```

## What This Skill Does NOT Do

- Does not execute or sandbox skills — only checks Sentinel's pre-computed trust data
- Does not block installs — warns and advises, user has final say
- Does not require any API keys or accounts
- Does not send any user data to Sentinel — only queries by skill slug
- Does not modify other skills or system files
