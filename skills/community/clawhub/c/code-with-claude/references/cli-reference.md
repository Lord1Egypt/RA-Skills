# CLI Reference

## CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `claude` | Start interactive session | `claude` |
| `claude "query"` | Start with initial prompt | `claude "explain this project"` |
| `claude -p "query"` | Query via SDK, then exit | `claude -p "explain this function"` |
| `cat file \| claude -p "query"` | Process piped content | `cat logs.txt \| claude -p "explain"` |
| `claude -c` | Continue most recent conversation | `claude -c` |
| `claude -c -p "query"` | Continue via SDK | `claude -c -p "Check for type errors"` |
| `claude -r "<session>" "query"` | Resume session by ID or name | `claude -r "auth-refactor" "Finish this PR"` |
| `claude update` | Update to latest version | `claude update` |
| `claude auth login` | Sign in. `--email`, `--sso`, `--console` flags available | `claude auth login --console` |
| `claude auth logout` | Log out | `claude auth logout` |
| `claude auth status` | Show auth status as JSON. `--text` for human-readable | `claude auth status` |
| `claude agents` | List configured subagents | `claude agents` |
| `claude auto-mode defaults` | Print auto mode classifier rules as JSON | `claude auto-mode defaults > rules.json` |
| `claude mcp` | Configure MCP servers | See MCP docs |
| `claude plugin` | Manage plugins. Alias: `claude plugins` | `claude plugin install code-review@claude-plugins-official` |
| `claude remote-control` | Start Remote Control server | `claude remote-control --name "My Project"` |
| `claude setup-token` | Generate long-lived OAuth token for CI/scripts | `claude setup-token` |

## CLI Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--add-dir` | Add working directories | `claude --add-dir ../apps ../lib` |
| `--agent` | Specify agent for session | `claude --agent my-custom-agent` |
| `--allowedTools` | Tools that execute without prompting | `"Bash(git log *)" "Read"` |
| `--append-system-prompt` | Append to default system prompt | `claude --append-system-prompt "Always use TypeScript"` |
| `--append-system-prompt-file` | Append from file | `claude --append-system-prompt-file ./extra-rules.txt` |
| `--bare` | Minimal mode, skip auto-discovery | `claude --bare -p "query"` |
| `--channels` | MCP channel notifications to listen for | `claude --channels plugin:my-notifier@my-marketplace` |
| `--chrome` | Enable Chrome browser integration | `claude --chrome` |
| `--continue`, `-c` | Resume most recent conversation | `claude --continue` |
| `--debug` | Enable debug with optional category filter | `claude --debug "api,mcp"` |
| `--disallowedTools` | Tools removed from context | `"Bash(git log *)" "Edit"` |
| `--effort` | Set effort level: low/medium/high/max | `claude --effort high` |
| `--enable-auto-mode` | Unlock auto mode in Shift+Tab cycle | `claude --enable-auto-mode` |
| `--fallback-model` | Fallback model when overloaded (print mode) | `claude -p --fallback-model sonnet "query"` |
| `--fork-session` | Create new session ID when resuming | `claude --resume abc123 --fork-session` |
| `--json-schema` | Validated JSON output matching schema (print mode) | `claude -p --json-schema '...' "query"` |
| `--max-budget-usd` | Max spend before stopping (print mode) | `claude -p --max-budget-usd 5.00 "query"` |
| `--max-turns` | Limit agentic turns (print mode) | `claude -p --max-turns 3 "query"` |
| `--mcp-config` | Load MCP servers from JSON | `claude --mcp-config ./mcp.json` |
| `--model` | Set model (alias or full name) | `claude --model claude-sonnet-4-6` |
| `--name`, `-n` | Session display name | `claude -n "my-feature-work"` |
| `--output-format` | Output format: text/json/stream-json | `claude -p "query" --output-format json` |
| `--permission-mode` | Start in permission mode | `claude --permission-mode plan` |
| `--print`, `-p` | Non-interactive print mode | `claude -p "query"` |
| `--remote` | Create web session on claude.ai | `claude --remote "Fix the login bug"` |
| `--remote-control`, `--rc` | Interactive + Remote Control | `claude --remote-control "My Project"` |
| `--resume`, `-r` | Resume by ID or name | `claude --resume auth-refactor` |
| `--system-prompt` | Replace entire system prompt | `claude --system-prompt "You are a Python expert"` |
| `--system-prompt-file` | Replace with file contents | `claude --system-prompt-file ./custom-prompt.txt` |
| `--tools` | Restrict available tools | `claude --tools "Bash,Edit,Read"` |
| `--worktree`, `-w` | Isolated git worktree | `claude -w feature-auth` |

## System Prompt Flags

| Flag | Behavior |
|------|----------|
| `--system-prompt` | Replaces entire default prompt |
| `--system-prompt-file` | Replaces with file contents |
| `--append-system-prompt` | Appends to default prompt |
| `--append-system-prompt-file` | Appends file contents to default prompt |

`--system-prompt` and `--system-prompt-file` are mutually exclusive. Append flags can combine with either.
For most use cases, use append flags to preserve built-in capabilities.
