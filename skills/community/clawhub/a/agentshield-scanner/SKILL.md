---
name: agent-shield
description: >
  Scan AI agent skills, MCP servers, and plugins for security vulnerabilities.
  Use when: user asks to check a skill/plugin for safety, audit security,
  scan for backdoors/data exfiltration/credential leaks, or evaluate
  trust of a third-party skill. Triggers: "is this skill safe", "scan for
  security issues", "audit this plugin", "check for backdoors",
  "安全扫描", "扫一下安不安全".
---

# AgentShield — Security Scanner

Scan any directory for security issues in AI agent skills, MCP servers, and plugins.

## Usage

```bash
# Basic scan
npx @elliotllliu/agent-shield scan ./path/to/skill/

# Pre-install check (GitHub URL, npm package, or local path)
npx @elliotllliu/agent-shield install-check https://github.com/user/repo

# JSON output for programmatic use
npx @elliotllliu/agent-shield scan ./path/to/skill/ --json

# Fail if score is below threshold
npx @elliotllliu/agent-shield scan ./path/to/skill/ --fail-under 70

# Scan .difypkg plugin archives
npx @elliotllliu/agent-shield scan ./plugin.difypkg
```

## What It Detects (30 rules)

**High Risk:**
- `data-exfil` — reads sensitive files + sends HTTP requests
- `backdoor` — eval(), exec(), dynamic code execution
- `reverse-shell` — outbound socket to shell
- `crypto-mining` — mining pool connections
- `credential-hardcode` — hardcoded API keys/tokens
- `obfuscation` — base64+eval, hex strings
- `prompt-injection` — 55+ patterns, 12 categories, 8 languages
- `tool-shadowing` — tool name/description manipulation
- `attack-chain` — multi-step kill chain (5 stages)
- `cross-file` — cross-file data flow and code injection
- `ast-*` — Python AST taint tracking (eval, pickle, SQL injection, SSTI)
- `multilang-injection` — 8-language prompt injection
- `description-integrity` — semantic mismatch between description and code
- `mcp-runtime` — MCP server runtime security issues

**Medium Risk:**
- `env-leak` — process.env exfiltration
- `network-ssrf` — user-controlled URLs, SSRF
- `privilege` — SKILL.md permission vs code mismatch
- `supply-chain` — known CVEs in dependencies
- `sensitive-read` — SSH keys, AWS creds access
- `phone-home` — periodic beacon/heartbeat pattern
- `python-security` — 35 Python-specific patterns

**Low Risk:**
- `excessive-perms` — too many permissions declared
- `hidden-files` — .env with secrets committed
- `typosquatting` — suspicious npm package names

## Interpreting Results

- **Score 90-100**: Low risk ✅
- **Score 70-89**: Moderate risk — review warnings
- **Score 40-69**: High risk — investigate before using
- **Score 0-39**: Critical risk — do not install

## When to Use

1. Before installing a third-party skill: `npx @elliotllliu/agent-shield install-check <url>`
2. Auditing your own skills before publishing
3. CI/CD pipeline gate: `--fail-under 70`
4. Reviewing skills from untrusted sources
