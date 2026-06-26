---
name: cursor-agent-cli
description: Cursor Agent CLI integration - AI-powered coding agent for terminal. Use when user mentions Cursor Agent, agent CLI, AI coding, code generation, refactoring, or interactive programming sessions.
metadata:
  openclaw:
    requires:
      bins: ["agent", "cursor"]
    optional:
      bins: ["git", "gh"]
  version: "1.0.0"
  author: "OpenClaw Community"
  license: "MIT"
  tags: ["cursor", "cursor-agent", "ai-coding", "automation", "developer-tools"]
---

# Cursor CLI Integration Skill

🤖 **Cursor Agent** - AI-powered coding assistant directly in your terminal.

## What is Cursor CLI?

Cursor provides two CLI tools:

1. **`cursor`** - Editor launcher (like `code` for VS Code)
2. **`agent`** ⭐ - Interactive AI coding assistant with full tool access

## Installation

```bash
# macOS, Linux, WSL
curl https://cursor.com/install -fsS | bash

# Windows PowerShell
irm 'https://cursor.com/install?win32=true' | iex

# Verify installation
agent --version
```

## Quick Start

### Interactive Mode

```bash
# Start interactive session
agent

# Start with initial prompt
agent "refactor the auth module to use JWT tokens"

# Resume latest session
agent resume

# Continue previous session
agent --continue

# List all sessions
agent ls
```

### Non-Interactive Mode (Scripts/CI)

```bash
# Run with specific prompt
agent -p "find and fix performance issues" --model "gpt-5.2"

# Code review
agent -p "review these changes for security issues" --output-format text

# JSON output for parsing
agent -p "analyze this codebase structure" --output-format json
```

## Modes

| Mode | Description | Usage |
|------|-------------|-------|
| **Agent** | Full access - can modify code | Default |
| **Plan** | Read-only planning and analysis | `--plan` or `/plan` |
| **Ask** | Q&A without making changes | `--mode=ask` or `/ask` |

### Switch modes mid-conversation

```
/plan        # Switch to plan mode
/ask         # Switch to ask mode
Shift+Tab    # Toggle plan mode
```

## Cloud Agent (Background Execution)

Run tasks in the cloud while you're away:

```bash
# Start in cloud mode
agent -c "refactor the auth module and add comprehensive tests"

# Send to cloud mid-conversation
& refactor the auth module and add comprehensive tests
```

Track at: [cursor.com/agents](https://cursor.com/agents)

## Models

```bash
# List available models
agent --list-models

# Use specific model
agent --model "gpt-5.2"
agent --model "sonnet-4"
agent --model "sonnet-4-thinking"
```

## Advanced Options

### Force Mode (Auto-approve)

```bash
# Auto-approve all commands
agent --force "build the feature"
agent --yolo "build the feature"  # Alias
```

### Sandbox Control

```bash
# Enable/disable sandbox
agent --sandbox enabled
agent --sandbox disabled

# Interactive sandbox menu
/sandbox
```

### Workspace & Worktree

```bash
# Specify workspace
agent --workspace /path/to/project

# Start in isolated git worktree
agent -w feature-branch
agent --worktree feature-branch --worktree-base main
```

### Custom Headers & API Key

```bash
# Set API key
export CURSOR_API_KEY="your-key"
agent --api-key "your-key"

# Add custom headers
agent -H "X-Custom-Header: value"
```

## Output Formats

```bash
# Text output (default)
agent -p "analyze code" --output-format text

# JSON output
agent -p "list functions" --output-format json

# Streaming JSON
agent -p "generate code" --output-format stream-json --stream-partial-output
```

## Authentication

```bash
# Login
agent login

# Check status
agent status
agent whoami

# Logout
agent logout
```

## Session Management

```bash
# Create new empty chat
agent create-chat

# Resume specific chat
agent --resume="chat-id-here"

# Resume latest
agent resume
agent --continue
```

## Cursor Rules Generation

```bash
# Interactive rule generation
agent generate-rule
agent rule
```

## MCP (Model Context Protocol) Management

```bash
# Manage MCP servers
agent mcp

# Auto-approve MCP servers
agent --approve-mcps
```

## Shell Integration

```bash
# Install shell integration
agent install-shell-integration

# Uninstall
agent uninstall-shell-integration
```

## Use Cases

### 1. Code Refactoring

```bash
agent "refactor the authentication module to use modern patterns"
```

### 2. Bug Fixing

```bash
agent -p "find and fix the memory leak in server.js"
```

### 3. Feature Development

```bash
agent "implement user profile editing with validation"
```

### 4. Code Review

```bash
# Review uncommitted changes
git diff | agent -p "review these changes for security issues"

# Review specific file
agent "review api/auth.js for security vulnerabilities"
```

### 5. Documentation

```bash
agent "add comprehensive JSDoc comments to all functions"
```

### 6. Testing

```bash
agent "generate unit tests for the auth module with 90% coverage"
```

### 7. Performance Optimization

```bash
agent "analyze and optimize database queries in user-service.js"
```

### 8. Migration

```bash
agent "migrate from Express to Fastify maintaining all functionality"
```

## CI/CD Integration

```bash
#!/bin/bash
# .github/workflows/code-review.yml

# Automated code review on PR
agent -p "review changed files for security and performance issues" \
  --output-format json \
  --trust \
  > review-report.json
```

## Best Practices

### ✅ Do

- Use `--plan` mode first for complex changes
- Review proposed changes before approving
- Use `--workspace` to specify project directory
- Save important sessions (they auto-save)
- Use `--force` only in trusted environments

### ❌ Don't

- Use `--yolo` on production code without review
- Share your API key
- Run in untrusted workspaces with `--trust`
- Ignore security warnings

## OpenClaw Integration

### Call agent from OpenClaw

```javascript
// Interactive session
exec({ command: "agent 'refactor auth module'", pty: true })

// Non-interactive
exec({ command: "agent -p 'analyze code' --output-format json" })
```

### Use in subagents

When spawning coding agents, you can use Cursor agent as an alternative:

```javascript
sessions_spawn({
  runtime: "acp",
  agentId: "cursor",  // If configured
  task: "Refactor authentication module"
})
```

## Troubleshooting

### Check version

```bash
agent --version
```

### Update to latest

```bash
agent update
```

### View system info

```bash
agent about
```

### Authentication issues

```bash
# Re-authenticate
agent logout
agent login
```

### Workspace trust

If prompted about workspace trust in headless mode:

```bash
agent --trust -p "your prompt"
```

## Configuration

Cursor agent reads from:
- `~/.cursor/` - Configuration and cache
- `~/.cursor/worktrees/` - Git worktrees
- Environment variables: `CURSOR_API_KEY`, `NO_OPEN_BROWSER`

## Keyboard Shortcuts (Interactive Mode)

| Shortcut | Action |
|----------|--------|
| `Shift+Tab` | Toggle plan mode |
| `/plan` | Switch to plan mode |
| `/ask` | Switch to ask mode |
| `/sandbox` | Open sandbox menu |
| `/max-mode on` | Enable max mode |
| `& <prompt>` | Send to Cloud Agent |

## Resources

- 📖 Official Docs: https://cursor.com/docs/cli/overview
- 🌐 Cloud Agent: https://cursor.com/agents
- 💬 Community: https://forum.cursor.com

## Version

**Current Version**: 2026.02.27-e7d2ef6

Check for updates: `agent update`

---

## Examples

### Example 1: Interactive Refactoring

```bash
$ agent "refactor the user authentication system"
```

Agent will:
1. Analyze current auth code
2. Propose refactoring plan
3. Show file changes
4. Ask for approval
5. Execute changes

### Example 2: Automated Testing

```bash
$ agent -p "generate comprehensive tests for src/api/*.js" --force
```

Non-interactive, auto-approved test generation.

### Example 3: Code Review in CI

```yaml
# .github/workflows/review.yml
- name: AI Code Review
  run: |
    agent -p "review changes for security issues" \
      --output-format json \
      --trust \
      > review.json
```

### Example 4: Cloud Background Task

```bash
$ agent -c "implement payment gateway integration with Stripe"
# Go do other work, check back later at cursor.com/agents
```

---

**Pro Tip**: Use `agent ls` frequently to review and resume past sessions. Context is preserved across sessions!
