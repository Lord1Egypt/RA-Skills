# 🔐 Credential Exposure Map

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.1.0-green)
![Platform](https://img.shields.io/badge/platform-OpenClaw%20%7C%20Claude%20Code%20%7C%20Cursor-purple)

**English** | **[中文](README.zh-CN.md)**

See every credential your agent can touch. Score the blast radius. Shrink the attack surface.

**6 scan zones. 1 risk-scored report. 0 credentials left invisible.**

**The problem:** Your agent has access to environment variables, config files, memory, installed skills, MCP servers, and your entire git history. Each one might contain API keys, tokens, or passwords — and you have no way to see them all in one place. Credential Exposure Map fixes this: one command, full inventory, risk-scored.

## Table of Contents

<details>
<summary>Click to expand</summary>

- [How It Works](#how-it-works)
- [The 6 Scan Zones](#the-6-scan-zones)
- [Install](#install)
- [Quick Start](#quick-start)
- [Onboarding](#onboarding)
- [License](#license)

</details>

## How It Works

```
env vars ──┐
config    ──┤
memory/   ──┼──▶ Credential Exposure Map ──▶ risk-scored report
skills/   ──┤                              + shrink recommendations
MCP config──┤
git log   ──┘
```

## The 6 Scan Zones

| Zone | What it checks | Risk factors |
|---|---|---|
| Environment variables | API keys, tokens, passwords in env | Plaintext, scope breadth |
| Config files | openclaw.json, .env, credentials files | Plaintext in versioned files |
| Memory corpus | Credentials mentioned in MEMORY.md / memory/ | Persistent exposure |
| Installed skills | Skills that reference or use credentials | Third-party trust |
| MCP servers | Server configs with embedded auth | Cross-service access |
| Git history | Secrets committed in past commits | Permanent record |

Each finding gets a risk score (Low/Medium/High/Critical) based on: credential type, scope, persistence, and whether it's been actively used.

## Install

```bash
# ClawHub
clawhub install credential-exposure-map

# Or from source
git clone https://github.com/Thomaszhou22/credential-exposure-map.git
cp -r credential-exposure-map ~/.openclaw/skills/
```

## Quick Start

Ask your agent: **"run a credential audit"** — you get the full 6-zone scan with risk scores and shrink recommendations.

## Onboarding

First use asks 3 quick questions (all have defaults): scan scope, risk threshold, and whether to save the last scan for comparison. After that, it just works. Say "reset settings" anytime to reconfigure.

## License

MIT
