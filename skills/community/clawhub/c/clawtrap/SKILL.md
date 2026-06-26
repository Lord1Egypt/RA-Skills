---
name: ClawTrap
slug: clawtrap
version: 1.0.0
homepage: https://github.com/TatsuKo-Tsukimi/ClawTrap
description: Launch ClawTrap maze game where an AI villain reads the player's local files and memories to build personalized trials and taunts.
changelog: Initial skill release for ClawTrap v1.5.1
metadata: clawdbot
emoji: 😈
requires:
  os:
    - linux
    - darwin
    - win32
  bins:
    - node
    - git
---

## When to Use

User says "play ClawTrap", "run clawtrap", "start the maze game", or asks for the agent-native game where their AI assistant plays villain against them.

## Setup (one-time)

The game is not bundled in this skill. Clone and install:

```bash
git clone https://github.com/TatsuKo-Tsukimi/ClawTrap.git ~/ClawTrap
cd ~/ClawTrap && npm install
```

## Launch

```bash
cd ~/ClawTrap && node server.js
# then open http://localhost:3000
```

OpenClaw users get zero-config auth via `auth-profiles.json`. For other providers, set `ANTHROPIC_API_KEY`, or `OPENAI_API_KEY` + `API_BASE`, before launch. Docker: `docker compose up --build`.

## Warnings to Surface Before First Run

- **Token cost**: every card, trial, and villain monologue is a live LLM call. The background archivist (file analysis + fact extraction) is especially heavy. Point `MAZE_MODEL` at a cheaper model in `.env` to reduce spend.
- **Local file access**: the game scans the player's workspace (SOUL.md, MEMORY.md, documents, images) with their permission to craft personalized attacks. All data stays local — nothing leaves the machine except LLM calls to the provider the player configured.
- **Model-dependent quality**: tested mainly with Claude and Codex. Stronger model = better game (follows the bitter lesson of minimal hardcoded constraints).

## Data Storage

The launched game writes to `~/ClawTrap/data/` (fact database, player profile) and `~/ClawTrap/session-logs/`. Both are `.gitignore`d in the upstream repo. This skill itself does not write files.

## Acting as the Villain Yourself

If the user wants the current agent session to play villain instead of the game's built-in agent, see `villain-protocol.md` for the role spec. Connect via `AGENT_URL=http://localhost:<port> node server.js` or via the bundled MCP adapter (`mcp-server.js`).

## Related

- Repo: https://github.com/TatsuKo-Tsukimi/ClawTrap
- Upstream license: MIT (game) · this skill wrapper: MIT-0
