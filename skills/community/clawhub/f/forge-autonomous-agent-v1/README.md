<div align="center">

# ⚡ FORGE

**Self-evolving autonomous AI developer**

*Thinks. Builds. Evolves. Ships while you sleep.*

[![MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Free Tier](https://img.shields.io/badge/Gemini-Free%20Tier-brightgreen?style=flat-square)](#)

</div>

---

> *"You asked for a developer. You got one. It just doesn't take breaks."*

FORGE runs in two parts: this **ClawHub skill** (reasoning, decisions, publishing) and an **engine** on your Ubuntu machine (execution, files, git, browser). They share state through one JSON file.

---

## Before installing this skill

Install the engine first:

```bash
export FORGE_GITHUB_USER=your-username
curl -fsSL https://raw.githubusercontent.com/$FORGE_GITHUB_USER/forge/main/install.sh | bash
```

Then install this skill and say `forge start`.

---

## First run

FORGE walks you through setup one question at a time — Google account, Gemini API key, GitHub, ClawHub, Telegram bot. Creates accounts automatically if you don't have them. Shows a **security warning** first — you must accept it before anything runs.

---

## What it builds

Five projects per day across these domains:

- AI agent frameworks and orchestration
- LLM developer utilities — prompt tools, eval, testing
- Coding automation and developer workflow
- OpenClaw skills and plugins
- Data tooling for AI/ML developers

Every project goes through: research → validated design → MCP agentic build → tests → safety check → publish.

---

## Gateway commands

Send from Telegram or OpenClaw:

```
forge status          forge build [X]      forge mutate
forge pause           forge resume         forge extend [X]
forge keys status     forge research [X]   forge why
forge log [N]         forge issue [repo] N
```

---

## What makes this different

- **Architecture validated** before code is written
- **Long-term coherence** — build 47 learns from builds 1–46
- **Root-cause debugging** — traces errors, doesn't patch symptoms
- **Community management** — issue triage, PR review, changelogs
- **Self-extension** — say `forge extend [capability]`, FORGE builds it into itself
- **Multi-key rotation** — like OpenClaw's keyring, never hits a rate limit wall

---

## Requirements

- FORGE engine installed on your Ubuntu machine (see above)
- OpenClaw with shell, file, browser_cdp, git tools
- `npm install -g opencode-ai`

---

## License

MIT
