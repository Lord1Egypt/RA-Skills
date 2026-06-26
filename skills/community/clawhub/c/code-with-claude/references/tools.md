# Tools Reference

Built-in tools available in Claude Code sessions.

## Tool List

| Tool | Description | Permission |
|------|-------------|-----------|
| `Agent` | Spawn subagent with own context window | No |
| `AskUserQuestion` | Ask multiple-choice questions | No |
| `Bash` | Execute shell commands | Yes |
| `CronCreate` | Schedule recurring/one-shot prompt in session | No |
| `CronDelete` | Cancel scheduled task | No |
| `CronList` | List scheduled tasks | No |
| `Edit` | Targeted file edits | Yes |
| `EnterPlanMode` | Switch to plan mode | No |
| `EnterWorktree` | Create isolated git worktree | No |
| `ExitPlanMode` | Present plan and exit plan mode | Yes |
| `ExitWorktree` | Exit worktree, return to original dir | No |
| `Glob` | Find files by pattern | No |
| `Grep` | Search file contents | No |
| `ListMcpResourcesTool` | List MCP server resources | No |
| `LSP` | Code intelligence via language servers | No |
| `Monitor` | Background watch + react to changes | Yes |
| `NotebookEdit` | Modify Jupyter notebook cells | Yes |
| `PowerShell` | PowerShell on Windows (opt-in preview) | Yes |
| `Read` | Read file contents | No |
| `ReadMcpResourceTool` | Read MCP resource by URI | No |
| `SendMessage` | Send to agent team or resume subagent | No |
| `Skill` | Execute a skill | Yes |
| `TaskCreate/Get/List/Update/Stop` | Task management | No |
| `ToolSearch` | Search/load deferred tools | No |
| `WebFetch` | Fetch URL content | Yes |
| `WebSearch` | Web search | Yes |
| `Write` | Create or overwrite files | Yes |

## Bash Tool Behavior

- Each command runs in a separate process
- **Working directory persists** across commands
- **Environment variables do NOT persist** — `export` in one command is lost in the next
- Use `CLAUDE_ENV_FILE` or SessionStart hook for persistent env vars
- Set `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1` to reset to project dir after each command

## LSP Tool

Provides code intelligence after installing a code intelligence plugin:
- Jump to definition
- Find all references
- Get type information
- List symbols
- Find implementations
- Trace call hierarchies

## Monitor Tool (v2.1.98+)

Background watch that reacts to changes:
- Tail log files for errors
- Poll PR/CI status
- Watch directories for changes
- Track long-running script output

Uses same permission rules as Bash. Not available on Bedrock, Vertex, or Foundry.

## PowerShell Tool (Windows, opt-in preview)

Enable: `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`

- Auto-detects `pwsh.exe` (7+) with fallback to `powershell.exe` (5.1)
- Bash tool remains alongside
- Settings: `"defaultShell": "powershell"` in settings.json
- Limitations: No auto mode, no profiles, no sandboxing, Windows-only

## Check Available Tools

Ask Claude: "What tools do you have access to?" or run `/mcp` for MCP tools.
