# Claude Code Skill for OpenClaw

> Call Claude Code CLI from OpenClaw to read codebase, edit files, run commands, and automate coding tasks.

## Overview

This skill provides integration with Claude Code CLI, allowing OpenClaw to leverage Claude Code's powerful coding capabilities including:
- Reading and understanding codebases
- Editing files with AI assistance
- Running terminal commands
- Creating commits and PRs
- Code review and debugging
- Running sub-agents for parallel tasks

## Prerequisites

1. **Install Claude Code CLI**:
   ```bash
   curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **Authenticate**:
   ```bash
   claude auth login
   ```

3. **Verify installation**:
   ```bash
   claude --version
   ```

## Usage

### Basic Query

Ask Claude Code a question about your codebase:

```
/claude-code What does the auth module do?
```

### Run a Task

Execute a coding task:

```
/claude-code write tests for the login function
```

### Continue Previous Session

Resume the most recent conversation:

```
/claude-code --continue
```

### Resume Specific Session

Resume a session by name or ID:

```
/claude-code --resume auth-fix
```

### Code Review

Review code changes:

```
/claude-code review the recent changes
```

### Create Commit

Commit changes with a descriptive message:

```
/claude-code commit my changes
```

### Run with Custom Model

Use a specific model:

```
/claude-code --model opus explain this code
```

### JSON Output

Get structured JSON output for scripting:

```
/claude-code --output-format json --print "list all functions"
```

## CLI Reference

### Common Commands

| Command | Description |
|:---|:---|
| `claude -p "query"` | Query via SDK, then exit |
| `claude -c` | Continue most recent conversation |
| `claude -r "session" "query"` | Resume session by ID or name |
| `claude --print "query"` | Print response without interactive mode |
| `claude update` | Update to latest version |
| `claude auth status` | Show authentication status |

### Useful Flags

| Flag | Description | Example |
|:---|:---|:---|
| `--print`, `-p` | Non-interactive mode | `claude -p "query"` |
| `--continue`, `-c` | Continue session | `claude -c` |
| `--resume`, `-r` | Resume specific session | `claude -r session-id "task"` |
| `--model` | Specify model | `claude --model opus "task"` |
| `--output-format` | Output format (text/json/stream-json) | `claude -p --output-format json "task"` |
| `--max-turns` | Limit agentic turns | `claude -p --max-turns 3 "task"` |
| `--max-budget-usd` | Max API spend | `claude -p --max-budget-usd 5 "task"` |
| `--add-dir` | Additional directories | `claude --add-dir ../lib "task"` |
| `--mcp-config` | Load MCP servers | `claude --mcp-config ./mcp.json` |

### Environment Variables

| Variable | Description |
|:---|:---|
| `ANTHROPIC_API_KEY` | API key for authentication |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | Enable CLAUDE.md from additional dirs |

## Integration with OpenClaw

This skill is designed to work with OpenClaw's exec tool. Here's how it integrates:

### Method 1: Direct CLI Execution

Use OpenClaw's exec tool to run Claude Code commands:

```bash
claude -p "What files were changed in the last commit?"
```

### Method 2: Session Management

Manage Claude Code sessions through OpenClaw:

```bash
# Continue last session
claude -c

# Resume specific session
claude -r my-session "Continue working on the feature"
```

### Method 3: MCP Integration

For advanced integration, configure MCP servers:

```bash
claude mcp add <server-name> <config>
```

## Examples

### Example 1: Explore a New Codebase

```
/claude-code Explore the project structure and tell me what the main components are
```

### Example 2: Fix a Bug

```
/claude-code Find and fix the login bug - users can't log in with correct credentials
```

### Example 3: Write Tests

```
/claude-code Write unit tests for the payment module
```

### Example 4: Refactor Code

```
/claude-code Refactor the auth middleware to use async/await
```

### Example 5: Code Review

```
/claude-code Review this PR for security issues
```

### Example 6: Batch Operations

```
/claude-code /batch migrate all API endpoints to use the new error handler
```

## Troubleshooting

### Authentication Issues

```bash
# Check auth status
claude auth status

# Re-authenticate
claude auth login
```

### Permission Issues

```bash
# Run with specific permission mode
claude --permission-mode plan "task"
```

### Session Issues

```bash
# List available sessions
claude --resume

# Fork a session (create new)
claude -r old-session --fork-session "new task"
```

## Advanced Features

### Sub-agents

Run multiple Claude Code instances in parallel:

```bash
claude --agents '{
  "reviewer": {
    "description": "Code reviewer",
    "prompt": "You are a senior code reviewer",
    "tools": ["Read", "Grep", "Bash"]
  }
}'
```

### Hooks

Automate actions before/after Claude Code runs:

See [Hooks documentation](https://code.claude.com/docs/en/hooks.md)

### MCP Servers

Connect Claude Code to external tools:

```bash
claude mcp add github '{"github_token": "..."}'
```

## Resources

- [Official Docs](https://code.claude.com/docs/)
- [CLI Reference](https://code.claude.com/docs/en/cli-reference.md)
- [Skills Guide](https://code.claude.com/docs/en/skills.md)
- [MCP Documentation](https://code.claude.com/docs/en/mcp.md)
- [Common Workflows](https://code.claude.com/docs/en/common-workflows.md)

---

**Note**: Claude Code requires authentication. Run `claude auth login` before first use.
