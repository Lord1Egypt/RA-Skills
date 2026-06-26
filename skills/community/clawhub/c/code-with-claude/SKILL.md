---
name: code-with-claude
description: >-
  Comprehensive Claude Code CLI reference covering interactive mode, CLI flags,
  commands, environment variables, hooks, channels, checkpointing, plugins,
  and tools. Use when asked about Claude Code features, configuration, workflows,
  keyboard shortcuts, session management, permission modes, environment setup,
  or best practices for using Claude Code effectively.
---

# Code with Claude

Use this skill when the user asks about Claude Code CLI features, configuration, workflows, or best practices.

## Claude Code Feature Map

| Feature | What It Does | Reference |
|---------|-------------|-----------|
| CLI flags | Launch-time options for sessions, models, permissions, prompts | `./references/cli-reference.md` |
| Commands | In-session `/` commands for model switching, permissions, context, workflows | `./references/commands.md` |
| Interactive mode | Keyboard shortcuts, Vim mode, multiline input, voice, task list | `./references/interactive-mode.md` |
| Hooks | Shell commands, HTTP endpoints, or LLM prompts at lifecycle events | `./references/hooks.md` |
| Plugins | Extend Claude Code with skills, agents, hooks, MCP/LSP servers | `./references/plugins.md` |
| Channels | MCP servers that push external events into a session | `./references/channels.md` |
| Checkpointing | Automatic file edit tracking with rewind and summarize | `./references/checkpointing.md` |
| Tools | Built-in tools: Bash, Edit, Read, Write, Agent, WebFetch, etc. | `./references/tools.md` |
| Environment variables | Control behavior via env vars or `settings.json` | `./references/env-vars.md` |

## Quick Reference: Essential CLI Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--model` | Set model (alias or full name) | `claude --model opus` |
| `--continue`, `-c` | Resume most recent conversation | `claude -c` |
| `--resume`, `-r` | Resume by session ID or name | `claude -r "auth-refactor"` |
| `--print`, `-p` | Non-interactive print mode (SDK) | `claude -p "query"` |
| `--permission-mode` | Start in a specific permission mode | `claude --permission-mode plan` |
| `--worktree`, `-w` | Isolated git worktree session | `claude -w feature-auth` |
| `--bare` | Minimal mode, skip auto-discovery | `claude --bare -p "query"` |
| `--append-system-prompt` | Add to default system prompt | `claude --append-system-prompt "Use TS"` |
| `--effort` | Set effort level for session | `claude --effort high` |

## Quick Reference: Essential Commands

| Command | Purpose |
|---------|---------|
| `/model [model]` | Switch model mid-session |
| `/compact [instructions]` | Compact conversation, free context |
| `/clear` | Clear conversation history |
| `/rewind` | Rewind to a checkpoint (Esc+Esc) |
| `/permissions` | Manage tool allow/deny rules |
| `/plan [description]` | Enter plan mode |
| `/batch <instruction>` | Parallel large-scale changes |
| `/hooks` | View hook configurations |
| `/memory` | Edit CLAUDE.md memory files |
| `/diff` | Interactive diff viewer |
| `/cost` | Show token usage statistics |
| `/effort [level]` | Set effort (low/medium/high/max) |

## Quick Reference: Key Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel current generation |
| `Esc+Esc` | Rewind / checkpoint menu |
| `Shift+Tab` | Cycle permission modes |
| `Ctrl+O` | Toggle transcript viewer |
| `Ctrl+B` | Background running tasks |
| `Ctrl+T` | Toggle task list |
| `Alt+P` | Switch model |
| `Alt+T` | Toggle extended thinking |
| `!command` | Run bash directly in session |
| `@path` | File path autocomplete |

## Quick Reference: Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Ask for each tool use |
| `acceptEdits` | Auto-approve file edits, ask for bash |
| `plan` | Read-only exploration, no writes |
| `auto` | AI classifier approves safe operations |
| `bypassPermissions` | Skip all permission prompts |

Cycle modes with `Shift+Tab`. Start in a specific mode: `claude --permission-mode plan`.

## Quick Reference: Core Tools

| Tool | Description | Permission |
|------|-------------|------------|
| `Bash` | Execute shell commands | Yes |
| `Read` | Read file contents | No |
| `Edit` | Targeted file edits | Yes |
| `Write` | Create or overwrite files | Yes |
| `Agent` | Spawn subagent with own context | No |
| `Glob` | Find files by pattern | No |
| `Grep` | Search file contents | No |
| `WebFetch` | Fetch URL content | Yes |
| `WebSearch` | Web search | Yes |
| `Monitor` | Background watch + react | Yes |

## Gotchas

- **Env vars don't persist** across Bash tool commands. Use `CLAUDE_ENV_FILE` or a SessionStart hook.
- **Checkpoints don't track bash changes** — only direct file edits via Edit/Write tools are tracked.
- **`applyTo: "**"` burns context** — always-on instructions load on every interaction. Use specific globs.
- **macOS Alt shortcuts** require Option-as-Meta in your terminal (iTerm2: Profiles → Keys → "Esc+").
- **`--bare` disables everything** — hooks, skills, plugins, MCP, auto-memory, CLAUDE.md. Use for fast scripted calls.
- **Hook `if` patterns** use tool permission syntax: `Bash(rm *)` matches bash commands starting with `rm`.
- **Plugin agents can't use** `hooks`, `mcpServers`, or `permissionMode` frontmatter for security reasons.

## When to Load References

Load the appropriate reference when the user needs detailed information:

- **CLI flags, system prompt customization, launch options** → Read `./references/cli-reference.md`
- **In-session commands, slash commands, skills list** → Read `./references/commands.md`
- **Keyboard shortcuts, Vim mode, multiline, voice, task list** → Read `./references/interactive-mode.md`
- **Hooks lifecycle, events, matchers, configuration** → Read `./references/hooks.md`
- **Plugins structure, manifest, MCP/LSP, distribution** → Read `./references/plugins.md`
- **Channels, webhook receivers, two-way chat bridges** → Read `./references/channels.md`
- **Checkpointing, rewind, restore, summarize** → Read `./references/checkpointing.md`
- **Built-in tools, Bash behavior, LSP, Monitor, PowerShell** → Read `./references/tools.md`
- **Environment variables, timeouts, model config, proxy** → Read `./references/env-vars.md`
