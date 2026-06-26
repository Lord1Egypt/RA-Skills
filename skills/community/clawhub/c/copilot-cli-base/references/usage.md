---
title: "Usage Guide"
source:
  - https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli-agents/overview
  - https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-programmatic-reference
category: reference
---

Interactive mode, programmatic mode, commands, shortcuts, and all usage patterns for Copilot CLI.

## Starting a Session

```bash
copilot                   # interactive session
copilot -i "PROMPT"       # interactive with initial prompt
copilot --continue        # resume most recent session
copilot --resume          # pick from session list
```

On first launch: trust directory → `/login` for OAuth.

## Two Modes

**Interactive:** `copilot` — starts terminal session with tool approval prompts.
**Programmatic:** `copilot -p "PROMPT"` — execute and exit. Use `-s` for clean output. Pipe: `echo "..." | copilot`.

## Keyboard Shortcuts

### Global

| Shortcut | Action |
|----------|--------|
| `Esc` | Cancel current operation |
| `Ctrl+C` | Cancel / clear / exit (press twice) |
| `Ctrl+D` | Shutdown |
| `Ctrl+L` | Clear screen |
| `@FILE` | Include file in context |
| `!COMMAND` | Run shell command directly |
| `/` | Show slash commands |
| `Ctrl+X` then `/` | Run slash command mid-prompt (without retyping) |
| `Shift+Tab` | Cycle modes (standard/plan/autopilot) |

### Timeline

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Expand recent timeline items (when prompt empty) |
| `Ctrl+E` | Expand all timeline items (when prompt empty) |
| `Ctrl+T` | Toggle reasoning visibility (persists across sessions) |

### Navigation

| Shortcut | Action |
|----------|--------|
| `Ctrl+A` / `Home` | Beginning of line |
| `Ctrl+E` / `End` | End of line (when typing) |
| `Ctrl+B` / `Ctrl+F` | Previous / next character |
| `Meta+←` / `Meta+→` | Move by word |
| `Ctrl+Home` / `Ctrl+End` | Start / end of text |
| `Ctrl+G` | Edit prompt in external editor |
| `Ctrl+H` | Delete previous character |
| `Ctrl+K` | Delete to end of line |
| `Ctrl+U` | Delete to beginning of line |
| `Ctrl+W` | Delete previous word |
| `↑` / `↓` | Navigate command history |

## Slash Commands

**Session:** `/clear` `/new` `/resume` `/rename NAME` `/session` `/share file|gist` `/usage` `/exit` `/quit` `/restart` `/copy`
**History:** `/undo` `/rewind` — revert last turn and file changes
**Navigation:** `/add-dir PATH` `/cwd PATH` `/cd PATH` `/list-dirs`
**Auth:** `/login` `/logout` `/user`
**Config:** `/model` `/theme` `/experimental` `/terminal-setup` `/allow-all` `/yolo` `/reset-allowed-tools` `/on-air` `/streamer-mode`
**Features:** `/plan PROMPT` `/review PROMPT` `/delegate PROMPT` `/fleet PROMPT` `/research TOPIC` `/diff` `/compact` `/context` `/pr [view|create|fix|auto]` `/changelog`
**Customization:** `/agent` `/skills` `/plugin` `/mcp` `/lsp` `/init` `/instructions`
**Help:** `/help` `/feedback`

`/on-air` / `/streamer-mode` hides preview model names and quota details (useful for demos).

## Key CLI Options

| Option | Purpose |
|--------|---------|
| `-p PROMPT` | Programmatic prompt (exit after) |
| `-s` / `--silent` | Output only response |
| `-i PROMPT` | Interactive with initial prompt |
| `--model=MODEL` | Set AI model |
| `--agent=AGENT` | Use custom agent |
| `--resume=ID` / `--continue` | Resume session |
| `--allow-all` / `--yolo` | All permissions |
| `--allow-all-tools` | Skip tool approval |
| `--allow-tool=TOOL` / `--deny-tool=TOOL` | Tool permission control |
| `--autopilot` | Autonomous continuation |
| `--max-autopilot-continues=N` | Limit autopilot iterations |
| `--no-ask-user` | Disable user questions |
| `--no-custom-instructions` | Skip loading AGENTS.md etc. |
| `--output-format=FORMAT` | `text` (default) or `json` (JSONL) |
| `--share=PATH` / `--share-gist` | Export session transcript |
| `--secret-env-vars=VAR` | Redact env var values |
| `--additional-mcp-config=JSON` | Add MCP server for session |
| `--effort=LEVEL` | Reasoning effort: `low`, `medium`, `high` |
| `--acp` | Start Agent Client Protocol server |
| `--config-dir=PATH` | Override config directory |
| `--disable-builtin-mcps` | Disable built-in MCP servers (e.g., `github-mcp-server`) |
| `--disable-mcp-server=NAME` | Disable specific MCP server |
| `--add-github-mcp-tool=TOOL` | Enable specific GitHub MCP tool (`*` for all) |
| `--excluded-tools=TOOL` | Exclude tools from model availability |
| `--plugin-dir=DIR` | Load plugin from local directory |
| `--screen-reader` | Screen reader optimizations |
| `--plain-diff` | Disable rich diff rendering |
| `--mouse[=on|off]` | Mouse support in alt screen mode |

## File Context (@)

```
Explain @config/ci/ci-required-checks.yml
Fix the bug in @src/app.js
```

Tab-completion works. Drag-and-drop images for visual references.

## Session Management

| Command | Purpose |
|---------|---------|
| `/clear`, `/new` | Reset context |
| `/resume` | Resume previous session |
| `/session` | Show session info |
| `/session checkpoints` | List compaction checkpoints |
| `/rename NAME` | Rename session |
| `/share file [PATH]` | Export to Markdown |
| `/compact` | Compress history manually |
| `/context` | Visualize token usage |

Auto-compaction triggers at 95% token limit. Session data at `~/.copilot/session-state/{session-id}/`.

## Plan Mode

Press `Shift+Tab` to cycle into plan mode, or `/plan PROMPT`.

1. Copilot analyzes request and codebase
2. Asks clarifying questions
3. Creates structured plan with checkboxes
4. Waits for approval before implementing

**Use for:** complex multi-file changes, refactoring, new features. **Skip for:** quick fixes, single file changes.

## Model Selection

| Model | Best for |
|-------|----------|
| Claude Opus 4.5 | Complex architecture, deep debugging |
| Claude Sonnet 4.5 (default) | Day-to-day coding |
| Claude Haiku 4.5 | Lightweight/fast tasks (explain, summarize) |
| GPT-5.2 / 5.3 Codex | Code generation, code review |

Switch: `/model` (interactive, persists to config.json) or `--model=MODEL` (CLI).

**Precedence:** custom agent def > `--model` > `COPILOT_MODEL` env > `config.json` > default.

**Reasoning effort:** Some models support effort levels. Set via `--effort=LEVEL` or `effortLevel` in config (`low`, `medium`, `high`, `xhigh`).

**Availability:** Only GitHub-routed models work (e.g., `claude-opus-4.6`, `claude-sonnet-4`). For others, use BYOK env vars.

## Code Review

```
/review                                    # review all changes
/review Focus on security issues in @src/  # scoped
/review Use Opus 4.5 and Codex 5.2 to review changes against main  # multi-model
```

## Steering Agents

- **Queue messages** while Copilot is thinking to redirect
- **Inline feedback on rejection** — explain why so Copilot adapts
- Press `Esc` to stop a running operation

## Tool Availability Values

For use with `--available-tools` and `--excluded-tools`.

**Shell:** `bash`/`powershell`, `read_bash`/`read_powershell`, `write_bash`/`write_powershell`, `stop_bash`/`stop_powershell`, `list_bash`/`list_powershell`
**File:** `view`, `create`, `edit`, `apply_patch`
**Agent:** `task`, `read_agent`, `list_agents`
**Other:** `grep`/`rg`, `glob`, `web_fetch`, `skill`, `ask_user`, `report_intent`, `show_file`, `fetch_copilot_cli_documentation`, `update_todo`, `store_memory`, `task_complete`, `exit_plan_mode`, `sql` (experimental), `lsp` (experimental)

## Permission Approval Keys

| Key | Effect |
|-----|--------|
| `y` | Allow once |
| `n` | Deny once |
| `!` | Allow all similar for session |
| `#` | Deny all similar for session |
| `?` | Show details |

## Built-in Agents

| Agent | Description |
|-------|-------------|
| Explore | Quick codebase analysis without adding to main context |
| Task | Executes tests/builds with brief summaries (full output on failure) |
| General-purpose | Complex multi-step tasks in separate context window |
| Code-review | Reviews changes, surfaces only genuine issues |

The model can auto-delegate to these agents or you can invoke them via `/agent` or `--agent`.

## Configuration Settings Reference

Settings cascade: user (`~/.copilot/config.json`) < repository (`.github/copilot/settings.json`) < local (`.github/copilot/settings.local.json`). CLI flags and env vars have highest precedence.

### Key User Settings

| Key | Default | Description |
|-----|---------|-------------|
| `model` | varies | AI model |
| `effortLevel` | `"medium"` | Reasoning effort (`low`, `medium`, `high`, `xhigh`) |
| `theme` | `"auto"` | `"auto"`, `"dark"`, `"light"` |
| `trusted_folders` | `[]` | Pre-trusted directories |
| `allowed_urls` / `denied_urls` | `[]` | URL allow/deny lists |
| `hooks` | — | Inline hook definitions |
| `disableAllHooks` | `false` | Disable all hooks |
| `streamerMode` | `false` | Hide model names and quota details |
| `includeCoAuthoredBy` | `true` | Add `Co-authored-by` to git commits |
| `companyAnnouncements` | `[]` | Custom messages on startup |
| `banner` | `"once"` | Banner display: `"always"`, `"once"`, `"never"` |
| `autoUpdate` | `true` | Automatic CLI updates |
| `screenReader` | `false` | Screen reader optimizations |
| `mouse` | `true` | Mouse support in alt screen mode |
| `respectGitignore` | `true` | Exclude gitignored files from `@` picker |

### Repository Settings

| Key | Merge Behavior | Description |
|-----|---------------|-------------|
| `companyAnnouncements` | Replaced (repo wins) | Startup messages |
| `enabledPlugins` | Merged (repo overrides user) | Declarative plugin auto-install |
| `extraKnownMarketplaces` | Merged (repo overrides user) | Plugin marketplaces |
