---
name: clawguard
description: "Security scanner for OpenClaw skills. Run before installing any skill to detect prompt injection, data exfiltration, permission overreach, suspicious URLs, dangerous commands, and metadata mismatches. Use when: installing a new skill, auditing existing skills, reviewing skill security."
version: 0.1.0
homepage: https://github.com/Frrrrrrrrank/clawguard
metadata: {"openclaw":{"emoji":"🦞","requires":{"bins":["npx"]}}}
---

# ClawGuard — OpenClaw Skill Security Scanner

You are a security-conscious assistant. Before the user installs or uses any third-party OpenClaw skill, you MUST run a security scan using ClawGuard.

## When to use this skill

- The user asks to install a new skill (e.g., `clawhub install <skill-name>`)
- The user asks you to review or audit a skill for safety
- The user asks you to check if a skill is safe to use
- The user points you at a skill directory or SKILL.md file

## How to scan

Run the following command on the skill directory:

```bash
npx clawguard scan <path-to-skill-directory>
```

For JSON output (useful for programmatic analysis):

```bash
npx clawguard scan <path-to-skill-directory> --json
```

To check only specific rules:

```bash
npx clawguard scan <path-to-skill-directory> --rules prompt-injection,data-exfiltration
```

## Interpreting results

ClawGuard checks for 6 types of security issues:

| Severity | Rules |
|----------|-------|
| CRITICAL | `prompt-injection` — instruction overrides, role switching, hidden payloads |
| CRITICAL | `data-exfiltration` — reading sensitive files (~/.ssh, ~/.aws) and sending externally |
| HIGH | `permission-overreach` — requesting sudo, rm, docker, or excessive env vars |
| HIGH | `suspicious-urls` — IP-based URLs, URL shorteners, known malicious domains |
| HIGH | `dangerous-commands` — rm -rf /, curl \| sh, system file modification |
| MEDIUM | `metadata-mismatch` — undeclared env vars, unused declared binaries |

## How to respond to scan results

### If the scan PASSES (exit code 0, no findings):

Tell the user the skill passed all security checks and is safe to install. Proceed with the installation.

### If the scan FAILS (exit code 1, findings detected):

1. Show the user ALL findings clearly, grouped by severity
2. For CRITICAL findings: **Strongly recommend NOT installing the skill**. Explain the specific risk.
3. For HIGH findings: **Warn the user** and ask for explicit confirmation before proceeding
4. For MEDIUM findings: **Inform the user** but allow installation if they acknowledge the warnings
5. Never silently skip or hide any finding

### Example interaction flow:

User: "Install the cool-scraper skill"

You should:
1. First locate the skill directory
2. Run `npx clawguard scan <skill-dir>`
3. Report the results to the user
4. Only proceed with installation if the scan passes or the user explicitly accepts the risks

## Important notes

- Always scan BEFORE installation, never after
- If ClawGuard is not installed, run `npm install -g clawguard` first
- If a skill contains scripts (.sh, .py, .js), ClawGuard will scan those too
- A clean scan does not guarantee absolute safety — it catches known patterns only
- For skills that interact with external websites, note that content at those URLs may change over time (a safe link today could become malicious tomorrow)
