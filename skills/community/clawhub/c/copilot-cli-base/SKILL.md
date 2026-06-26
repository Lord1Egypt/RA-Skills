---
name: copilot-cli
description: >
  Reference knowledge base for GitHub Copilot CLI. Use when answering questions about
  Copilot CLI features, commands, configuration, plugins, hooks, skills, MCP servers,
  custom agents, automation, or troubleshooting CLI workflows. Do NOT use for general
  Git/GitHub questions, VS Code Copilot Chat, or IDE-only Copilot features.
license: MIT-0
compatibility: Designed for OpenClaw, Claude Code, GitHub Copilot, and compatible AgentSkills clients
metadata:
  openclaw:
    emoji: "⌨️"
    homepage: "https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-copilot-cli"
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["copilot"]
    install:
      - id: npm
        kind: node
        package: "@github/copilot"
        bins: ["copilot"]
        label: "Install via npm"
---

# Copilot CLI Reference Skill

GitHub Copilot CLI is a terminal-native AI coding agent. This skill provides reference docs for all features, commands, and operational patterns.

## When to Use

✅ **USE this skill when:**
- Answering questions about Copilot CLI features, commands, or configuration
- Setting up CI/CD automation with Copilot CLI or GitHub Actions
- Troubleshooting Copilot CLI errors, auth, or rate limits
- Creating custom agents, plugins, hooks, or MCP server integrations
- Writing prompts for programmatic/autopilot execution
- Comparing Copilot CLI vs Claude Code for a specific use case

❌ **DON'T use this skill when:**
- General Git or GitHub questions unrelated to Copilot CLI (→ use git CLI / GitHub skill)
- VS Code Copilot Chat or Copilot Edits features (→ IDE-specific docs)
- GitHub Actions workflows that don't involve Copilot (→ Actions docs)
- Copilot Workspace or other non-CLI Copilot products

## Setup

Install: `npm install -g @github/copilot` (or via GitHub CLI extension)
Auth: `copilot` → trust directory → `/login`
Config: edit `~/.copilot/config.json` directly (no `copilot config set` command)

See `references/getting-started.md` for full installation, authentication, and configuration details.

## Quick Reference

**Interactive:** `copilot` → trust directory → `/login` → prompt
**Programmatic:** `copilot -p "PROMPT" --yolo --no-ask-user -s`
**With permissions:** `copilot -p "PROMPT" --allow-tool='shell(git:*), write' --no-ask-user`
**Autopilot:** `copilot --autopilot --yolo --max-autopilot-continues 10 -p "PROMPT"`
**Custom agent:** `copilot -p "PROMPT" --agent=my-agent`
**Model override:** `copilot -p "PROMPT" --model claude-opus-4.6`
**Plan mode:** `Shift+Tab` to cycle modes (standard/plan/autopilot)
**Research:** `/research TOPIC` → deep report with citations
**Fleet:** `/fleet PROMPT` → parallel subagent execution
**Chronicle:** `/chronicle standup` · `tips` · `improve` · `reindex`

## Copilot CLI vs Claude Code

| Need | Copilot CLI | Claude Code |
|------|-------------|-------------|
| Rate-limited on Claude Code | ✅ Use as fallback | — |
| CI/CD automation | ✅ Built-in Actions support | Limited |
| Clean stdout (no PTY/ANSI) | — | ✅ Better |
| Long iterative reviews | ✅ Better for many iterations | — |

See `references/patterns-and-best-practices.md` for the full decision matrix.

## Key Gotchas

**Automation:**
- Always use `-p` (not `-i`) for automation — `-i` hangs
- Always set `--max-autopilot-continues=N` in CI/CD to prevent runaway loops
- Size timeouts by complexity: 120s (simple) → 1800s (large)
- Background servers die between exec spawns — restart each time

**OpenClaw Integration (programmatic exec):**
- Copilot requires a real TTY — pipe/stdout redirection causes `EPIPE` crashes
- Use `pty: true` on exec calls to avoid output fragmentation
- Set `timeout: 120` minimum (MCP startup ~3s + inference ~25s+)
- Use `--allow-all` (or `--yolo`) for file write permissions in `--no-ask-user` mode
- Working formula:
  ```bash
  copilot -p "<prompt>" --no-ask-user --allow-all --max-autopilot-continues 3
  # + exec options: pty=true, timeout=120
  ```
- The `--add-dir <path>` flag grants access to specific directories without full `--allow-all`

**Configuration:**
- `--yolo` does NOT skip folder trust — pre-trust in `~/.copilot/config.json`
- No `copilot config set` — edit config JSON manually
- Custom instructions now **combine** (not cascade) — avoid conflicting instructions

**Experimental features:**
- `/chronicle` and history queries require `--experimental` or `/experimental on`
- Premium requests vary by model multiplier — check with `/model`

See `references/troubleshooting.md` for all issues and fixes.

## Quick Responses

| Question | Answer |
|----------|--------|
| How do I start Copilot CLI? | `copilot` (interactive) |
| How do I use it in CI/CD? | `copilot -p "PROMPT" --yolo --no-ask-user -s` |
| How do I create a custom agent? | See `references/automation-and-delegation.md` |
| How do I add an MCP server? | See `references/customization.md` |
| How do I research a topic? | `/research TOPIC` in interactive mode |

## Reference Documents

Full index: `references/index.md`

| File | Contents |
|------|----------|
| `getting-started.md` | Installation, auth, config, permissions, env vars, plan mode overview |
| `usage.md` | Interactive & programmatic modes, 40+ slash commands, shortcuts, model selection, config settings, built-in agents |
| `automation-and-delegation.md` | CI/CD, GitHub Actions, autopilot, delegate, fleet, custom agent creation |
| `customization.md` | Custom instructions (combining), plugins, MCP servers, enterprise governance |
| `hooks.md` | Hook types (command + prompt), config, denial responses, PowerShell support |
| `integrations.md` | VS Code integration (diffs, sessions, selection), ACP server |
| `research.md` | `/research` reports with citations, `/chronicle` session history & insights |
| `troubleshooting.md` | Auth, rate limits, autopilot runaway, enterprise access, diagnostics |
| `patterns-and-best-practices.md` | Decision matrix, prompt engineering, anti-patterns |

All files in `references/` directory.
