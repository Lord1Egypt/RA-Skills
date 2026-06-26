---
name: agent-audit-scanner
description: "Security scanner for OpenClaw skills. Detects prompt injection, credential leaks, unsafe code execution, MCP misconfigurations, privilege escalation, obfuscated shell commands, and social engineering patterns. Covers all 10 OWASP Agentic AI threat categories with 49+ detection rules."
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: []
      optional_env: []
    emoji: "🛡️"
    homepage: https://github.com/HeadyZhang/agent-audit
    source: https://github.com/HeadyZhang/agent-audit
    license: MIT
    os:
      - darwin
      - linux
      - windows
    file_reads:
      - "~/.openclaw/workspace/skills/**"
      - "~/.openclaw/skills/**"
      - "~/.openclaw/openclaw.json"
    file_writes: []
    network_endpoints: []
    telemetry: false
    persistence: false
    privilege_escalation: false
    always: false
    autonomous_invocation: restricted
---

# Agent Audit Scanner — Security Scanning for OpenClaw Skills

You are a security auditor. Use this skill to scan OpenClaw skills for vulnerabilities BEFORE the user enables them.

## When to Trigger

1. **New skill installed** — scan before confirming it's ready.
2. **User asks about safety** — "is this skill safe?", "audit this skill", etc.
3. **`/audit` command** — `/audit` (all) or `/audit <skill-name>`.
4. **Bulk audit** — "audit all skills", "check my skills".

## Setup (first-time only)

```bash
pip install agent-audit && agent-audit --version
```

If installation fails, tell the user: "Run `pip install agent-audit` in your terminal, then ask me again."

## How to Scan a Single Skill

Run the scan script bundled with this skill:

```bash
python3 {baseDir}/scripts/scan-skill.py "<path-to-skill-directory>"
```

Or use agent-audit directly:

```bash
agent-audit scan "<path-to-skill-directory>" --format json
```

Common skill locations:
- Workspace skills: `~/.openclaw/workspace/skills/<skill-name>/`
- Managed skills: `~/.openclaw/skills/<skill-name>/`

## How to Scan All Skills

```bash
python3 {baseDir}/scripts/scan-all-skills.py
```

This discovers and scans every skill in `~/.openclaw/workspace/skills/` and `~/.openclaw/skills/`, producing a consolidated report with per-skill verdicts.

## How to Audit OpenClaw Config

```bash
python3 {baseDir}/scripts/check-config.py
```

Checks `~/.openclaw/openclaw.json` and `.mcp.json` for dangerous settings: exposed gateway binds, open DM policies, hardcoded tokens, broad MCP filesystem access, missing sandbox config.

## Interpreting Results

Findings have three severity tiers:

- **BLOCK** (confidence >= 0.92): DO NOT enable. Warn the user. Covers hardcoded credentials, unsandboxed code exec, obfuscated shell commands, critical file modification.
- **WARN** (0.60-0.91): Inform the user and let them decide. Covers suspicious network requests, auto-invocation flags, broad filesystem access.
- **INFO** (0.30-0.59): Mention briefly. Low-confidence, usually safe patterns.
- **CLEAN** (0 findings): Confirm safe to enable.

## What Gets Scanned

Scripts (py/sh/js/ts), all text files for credentials, `*.mcp.json` for MCP misconfigs, `SKILL.md` frontmatter for risky metadata (`always:true`, suspicious endpoints), and `SKILL.md` body for obfuscated shell commands and social engineering. See `references/owasp-asi-mapping.md` for the full 56-rule mapping across all 10 OWASP ASI categories.

## Important Notes

- Always scan BEFORE enabling a skill, never after.
- If the scan fails, recommend manual review.
- Never skip scanning because a skill is popular. The #1 ClawHub skill was found to be malware.
- Any skill that modifies SOUL.md, AGENTS.md, MEMORY.md, or IDENTITY.md is BLOCK-level regardless of confidence.
