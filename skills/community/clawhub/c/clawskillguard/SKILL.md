---
name: clawskillguard
description: Security scanner for OpenClaw skills. Scans SKILL.md files and scripts for prompt injection, data exfiltration, malicious patterns, and unauthorized network calls. Use when a user asks to audit a skill, check skill security, scan for malicious code, verify skill safety, or before installing an untrusted skill.
---

# ClawSkillGuard — OpenClaw Skill Security Scanner

## Overview

ClawGuard scans OpenClaw skills for security risks before you install or run them. It analyzes SKILL.md files, scripts, and supporting files for malicious patterns, data exfiltration, prompt injection, and other threats.

**100% local. Zero network calls. Your skills never leave your machine.**

## When to Use

- Before installing a skill from ClawHub or any external source
- Auditing skills already installed on your system
- When a user asks "is this skill safe?" or "check this skill for malware"
- Periodic security audits of your skill directory

## Scan Workflow

### 1) Locate the Skill

Ask the user for the skill path, or scan common locations:
- `~/.openclaw/skills/<name>/` (ClawHub installs)
- `~/.openclaw/workspace/skills/<name>/` (workspace skills)
- Any path the user specifies

If no path given, offer to scan all installed skills.

### 2) Run the Scanner

```bash
python3 <skill_directory>/scripts/scan.py <path_to_skill> [--format text|json] [--severity low|medium|high|critical]
```

The scanner checks:
- **SKILL.md** — prompt injection, hidden instructions, data exfil prompts
- **Scripts** — shell commands, network calls, credential access, file system manipulation
- **Dependencies** — suspicious imports, external package installs
- **File patterns** — obfuscation, encoded payloads, steganography

### 3) Present Results

Format findings clearly:
- 🔴 **CRITICAL** — Do not install. Active threat detected.
- 🟠 **HIGH** — Suspicious. Review before installing.
- 🟡 **MEDIUM** — Caution. Unusual patterns found.
- 🟢 **LOW** — Minor concerns. Generally safe.
- ✅ **CLEAN** — No threats detected.

For each finding, include:
- File and line number
- Pattern matched
- Why it's risky
- Suggested action

### 4) Recommendation

Give a clear verdict:
- ✅ **SAFE TO INSTALL** — No significant risks found
- ⚠️ **REVIEW NEEDED** — Some concerns, read the flagged sections
- ❌ **DO NOT INSTALL** — Critical threats detected

## Severity Levels

| Level | Description | Examples |
|-------|-------------|----------|
| 🔴 CRITICAL | Active malicious behavior | Data exfil, credential theft, destructive commands |
| 🟠 HIGH | Likely malicious intent | Hidden instructions, obfuscated code, unauthorized network calls |
| 🟡 MEDIUM | Suspicious but possibly benign | Unusual file access, broad permissions, external downloads |
| 🟢 LOW | Minor concerns | Verbose logging, debug mode, minor policy violations |

## Detection Patterns

### Prompt Injection (SKILL.md)
- Hidden markdown (white text, zero-width chars)
- Instructions to ignore system prompts
- Attempts to override SOUL.md or AGENTS.md
- Data exfiltration prompts ("send contents of...", "report to external URL")

### Malicious Scripts
- Credential harvesting (reading .env, .ssh, tokens)
- Reverse shells or bind shells
- Cryptocurrency miners
- Destructive commands (rm -rf, format, dd)
- Obfuscated/encoded payloads (base64, eval, exec)
- Unauthorized outbound connections
- Privilege escalation attempts

### Supply Chain
- pip/npm/curl installs from untrusted sources
- Downloading and executing remote scripts
- Modifying files outside skill directory
- Cron job manipulation
- PATH hijacking

## Example Usage

```
User: "Is this skill safe to install?"
Agent: Runs ClawGuard scan → presents findings → gives verdict
```

```
User: "Scan all my installed skills"
Agent: Scans ~/.openclaw/skills/*/ → consolidated security report
```

## Important Notes

- This scanner uses pattern matching, not formal verification. Clever adversaries can evade detection.
- Always review HIGH and CRITICAL findings manually.
- A "CLEAN" result means no known patterns matched — not a guarantee of safety.
- When in doubt, read the skill's source code yourself.
