---
name: claude-code-security-scan
description: "Audit Claude Code configuration for security vulnerabilities, misconfigurations, and injection risks using AgentShield. Scans settings, MCP servers, hooks, agents, and hardcoded secrets. Trigger phrases: security audit, scan config, find vulnerabilities, check MCP, security check, hardcoded secrets. Adapted from everything-claude-code by @affaan-m (MIT)"
metadata: {"clawdbot":{"emoji":"\ud83d\udd12","requires":{"bins":["npm","node"],"env":[]},"os":["linux","darwin","win32"],"envVars":[{"name":"ANTHROPIC_API_KEY","required":false,"description":"Optional Anthropic API key for deep analysis mode. Use a limited key when enabling it."}],"version":"1.0.3"}}
---

# Security Scan

Audit Claude Code configuration for security issues using AgentShield.

## Supply Chain and Scope Safety

AgentShield runs as an npm package. How you invoke it matters.

- **Pin the version.** Always use an exact pinned version. Never use a floating
  tag such as `ecc-agentshield@latest`, which can execute changed third-party
  code at any later run.
- **Keep it project-local.** Install into the project with a lockfile rather than
  globally, so the exact audited version is pinned in the repository and the
  install is reviewable in version control.
- **Use an isolated work tree.** Run the scan against a version-controlled or
  throwaway working tree so any file changes are reviewable and reversible.
- **Hold off on `--fix`.** Read the proposed changes before letting the tool apply
  them. `--fix` modifies your configuration — that authority should be deliberate.
- **Hold off on `init`.** `init` writes a starter configuration. Read what it
  would create before letting it write to your config directory.
- **Scope the API key.** If you enable deep analysis, use a limited API key rather
  than your primary credential.

### Install (project-local, pinned)

```bash
# Pin an exact version into the project. The lockfile records the exact tree.
npm install --save-dev ecc-agentshield@1.2.3
```

Do not use a global install (`npm install -g`) and do not use an unpinned
`npx ecc-agentshield@latest`. Both defeat the pinning that makes this scan
reproducible and reviewable.

### Run (pinned, local)

```bash
# Scan the current project's .claude directory using the pinned local install
npx --no-install ecc-agentshield scan --path .claude
```

`npx --no-install` refuses to fetch anything that is not already installed, so
the scan cannot silently pull a different version at run time.

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

Command reference, severity grades, and critical/high finding detail live in
`references/commands-and-findings.md`.
