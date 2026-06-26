---
name: claude-code-security-scan
description: "Audit Claude Code configuration for security vulnerabilities, misconfigurations, and injection risks using AgentShield. Scans settings, MCP servers, hooks, agents, and hardcoded secrets. Trigger phrases: security audit, scan config, find vulnerabilities, check MCP, security check, hardcoded secrets. Adapted from everything-claude-code by @affaan-m (MIT)"
metadata: {"clawdbot":{"emoji":"🔒","requires":{"bins":["npm","node"],"env":[],"optional_env":["ANTHROPIC_API_KEY"]},"os":["linux","darwin","win32"]}}
---

# Security Scan

Audit Claude Code configuration for security issues using AgentShield.

## When to Activate

- Setting up a new Claude Code project
- After modifying settings.json, CLAUDE.md, or MCP configs
- Before committing configuration changes
- Onboarding to repo with existing configs
- Periodic security hygiene checks

## What It Scans

- `CLAUDE.md` — Hardcoded secrets, auto-run instructions, injection patterns
- `settings.json` — Overly permissive allow lists, missing deny lists
- `mcp.json` — Risky MCP servers, hardcoded env secrets
- `hooks/` — Command injection via interpolation, data exfiltration
- `agents/` — Unrestricted tool access, missing model specs

## Setup & Usage

```bash
# Install globally (recommended)
npm install -g ecc-agentshield

# Or run via npx (no install needed)
npx ecc-agentshield scan
```

### Commands

```bash
# Basic scan
npx ecc-agentshield scan

# Scan specific path
npx ecc-agentshield scan --path /path/to/.claude

# Filter by severity
npx ecc-agentshield scan --min-severity medium

# Output formats
npx ecc-agentshield scan --format json
npx ecc-agentshield scan --format markdown
npx ecc-agentshield scan --format html > report.html

# Auto-fix safe issues
npx ecc-agentshield scan --fix

# Deep analysis (requires ANTHROPIC_API_KEY)
npx ecc-agentshield scan --opus --stream

# Initialize secure config
npx ecc-agentshield init
```

## Severity Grades

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 90-100 | Secure |
| B | 75-89 | Minor issues |
| C | 60-74 | Needs attention |
| D | 40-59 | Significant risks |
| F | 0-39 | Critical |

## Critical Findings (Fix Immediately)

- Hardcoded API keys in config
- `Bash(*)` unrestricted shell access
- Command injection via `${file}` interpolation
- Shell-running MCP servers

## High Findings (Fix Before Production)

- Auto-run instructions in CLAUDE.md
- Missing deny lists
- Unnecessary Bash access in agents
