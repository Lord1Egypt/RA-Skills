---
name: Claude Dev Setup
slug: claude-dev-setup
version: 1.1.0
homepage: https://clawhub.ai/DhruvArvindSingh/claude-dev-setup
description: Complete Claude Code CLI integration with session management and APEX cognitive framework. One skill to set up coding agents with persistent task tracking.
metadata:
  clawdbot:
    emoji: "🤖"
    requires:
      bins: ["claude"]
    os: ["linux", "darwin"]
---

# Claude Dev Setup

Complete package for coding agents: Claude Code CLI integration, session management, and APEX cognitive framework.

## What This Skill Does

Installs and configures:
1. **Session Tracking** — `memory/claude-code-sessions.md` for background task management
2. **AGENTS.md Section** — Workflow documentation for all coding agents
3. **APEX Stack Reference** — How to add cognitive framework to project CLAUDE.md files
4. **OAuth Token Handling** — Automatic token extraction and usage

## Prerequisites

- Node.js 18+
- Claude Pro/Max subscription (for OAuth token)
- OpenClaw agent workspace

## OAuth Token (CRITICAL)

### Where the Token Lives

Claude Code stores its OAuth token in:
```
~/.claude/.credentials.json
```

### Token Format
```
sk-ant-oat01-xxxxx...
```

### How to Get the Token

**Option 1: Extract from credentials file (RECOMMENDED)**
```bash
# Extract the accessToken from credentials
cat ~/.claude/.credentials.json | grep -o '"accessToken":"[^"]*"' | cut -d'"' -f4
```

**Option 2: Authenticate via browser (first-time setup)**
```bash
claude setup-token
# Opens browser for OAuth flow
# Paste authorization code when prompted
```

### ALWAYS Use the Token When Calling Claude Code

Every Claude Code CLI call MUST include the token:

```bash
# ✅ CORRECT - Token set explicitly
export CLAUDE_CODE_OAUTH_TOKEN="sk-ant-oat01-xxxxx..."
claude --print --dangerously-skip-permissions "your task"

# ❌ WRONG - Token not set, will fail in non-interactive mode
claude --print "your task"
```

### Automatic Token Extraction

Add to your shell profile for automatic token loading:
```bash
# Add to ~/.bashrc or ~/.zshrc
export CLAUDE_CODE_OAUTH_TOKEN=$(cat ~/.claude/.credentials.json 2>/dev/null | grep -o '"accessToken":"[^"]*"' | cut -d'"' -f4)
```

### For Agent Executors

When using the `exec` tool, always extract and set the token:

```json
exec({
  command: "export CLAUDE_CODE_OAUTH_TOKEN=$(cat ~/.claude/.credentials.json | grep -o '\"accessToken\":\"[^\"]*\"' | cut -d'\"' -f4) && claude --print --dangerously-skip-permissions 'Task description'",
  background: true,
  yieldMs: 10000
})
```

**Or pre-extract and use:**
```json
// First, extract token
exec({
  command: "cat ~/.claude/.credentials.json | grep -o '\"accessToken\":\"[^\"]*\"' | cut -d'\"' -f4"
})

// Then use in all subsequent calls
exec({
  command: "CLAUDE_CODE_OAUTH_TOKEN=sk-ant-oat01-xxx claude --print --dangerously-skip-permissions 'Task'"
})
```

## Architecture

```
Agent Workspace
├── AGENTS.md                          # + Session management section
├── memory/
│   └── claude-code-sessions.md         # NEW: Session registry
└── skills/
    ├── claude-code-cli-openclaw/       # CLI integration
    ├── apex-stack-claude-code/         # Cognitive framework
    └── claude-dev-setup/               # THIS SKILL

System Level
└── ~/.claude/.credentials.json         # OAuth token (DO NOT COMMIT)
```

## Session Management

### Registry Format

Sessions are tracked in `memory/claude-code-sessions.md`:

```markdown
| Session ID | Label | Task | Started | Status |
|------------|-------|------|---------|--------|
| tender-nexus | build-auth | Build auth module | 2026-03-24 08:50 UTC | running |
```

### Starting a Background Task (CORRECT WAY)

```json
// Step 1: Extract token from credentials
// Step 2: Use in Claude Code call
exec({
  command: "CLAUDE_CODE_OAUTH_TOKEN=$(cat ~/.claude/.credentials.json | grep -o '\"accessToken\":\"[^\"]*\"' | cut -d'\"' -f4) claude --print --dangerously-skip-permissions 'Task description'",
  background: true,
  yieldMs: 10000
})
```

**After starting, log the session:**
1. Note `sessionId` from response
2. Append to `memory/claude-code-sessions.md`
3. Report to user: "Started X (session: label)"

### Checking Status

When user asks "what's the status?":
```json
process({ action: "log", sessionId: "session-id" })
```

### Label Naming Convention

- `build-feature-X` — Building a new feature
- `refactor-Y-module` — Refactoring code
- `fix-bug-Z` — Bug fix
- `test-coverage-A` — Adding tests
- `cleanup-legacy-B` — Removing old code

### Quick Tasks (< 30 seconds)

For simple tasks, use direct exec without tracking:
```json
exec({
  command: "CLAUDE_CODE_OAUTH_TOKEN=$(cat ~/.claude/.credentials.json | grep -o '\"accessToken\":\"[^\"]*\"' | cut -d'\"' -f4) claude --print --dangerously-skip-permissions 'Quick fix'",
  timeout: 60
})
```

## AGENTS.md Integration

After installing this skill, your AGENTS.md gets a new section:

```markdown
## 🤖 Claude Code CLI Sessions

You have access to Claude Code CLI for coding tasks.

### OAuth Token (Required)

**Token location:** `~/.claude/.credentials.json`

**ALWAYS extract and use the token:**
```bash
CLAUDE_CODE_OAUTH_TOKEN=$(cat ~/.claude/.credentials.json | grep -o '"accessToken":"[^"]*"' | cut -d'"' -f4) claude --print --dangerously-skip-permissions 'task'
```

### Session Tracking

All background sessions tracked in `memory/claude-code-sessions.md`.

**Before starting:** Check for running sessions
**After starting:** Log session ID + label
**On completion:** Update status column

### When User Asks Status

1. Read sessions file
2. Find session by label
3. Poll for output
4. Summarize progress
```

## APEX Stack for Projects

The cognitive framework (`apex-stack-claude-code`) should be added to project CLAUDE.md files, not agent memory.

### Adding to a Project

```bash
cd /path/to/your/project

# If CLAUDE.md doesn't exist:
cat ~/.openclaw/workspace-YOURS/skills/apex-stack-claude-code/SKILL.md > CLAUDE.md

# If CLAUDE.md exists, append:
cat ~/.openclaw/workspace-YOURS/skills/apex-stack-claude-code/SKILL.md >> CLAUDE.md
```

### What APEX Stack Does

| Layer | Purpose |
|-------|---------|
| APEX | Cognitive modes (precision, execution, architecture, creative) |
| MEMORIA | Persistent memory for project context |
| ARCHITECT | Autonomous execution loop |

### Project CLAUDE.md Structure

```markdown
# Project: [Name]

## Overview
[1-2 sentences]

## Tech Stack
- Language: ...
- Framework: ...

[APEX Stack content appended here]
```

## Complete Workflow

```
User gives task
    ↓
Agent reads memory/claude-code-sessions.md (check for conflicts)
    ↓
Agent extracts token: cat ~/.claude/.credentials.json | grep accessToken
    ↓
Agent starts: exec({ command: "CLAUDE_CODE_OAUTH_TOKEN=xxx claude ...", background: true })
    ↓
Agent logs session to claude-code-sessions.md
    ↓
Agent reports: "Started X (session: build-feature-X)"
    ↓
User: "What's the status?"
    ↓
Agent reads sessions file → polls process → summarizes
```

## Installation Checklist

Run this after installing the skill:

- [ ] Claude Code CLI installed: `which claude`
- [ ] Authenticated: check `~/.claude/.credentials.json` exists
- [ ] Token extractable: `cat ~/.claude/.credentials.json | grep accessToken`
- [ ] Session file created: `memory/claude-code-sessions.md`
- [ ] AGENTS.md updated with session section
- [ ] APEX Stack added to project CLAUDE.md (if applicable)

## Security Notes

- OAuth token stored in `~/.claude/.credentials.json` (valid 1 year)
- **NEVER commit `CLAUDE_CODE_OAUTH_TOKEN` to git**
- **ALWAYS extract token from credentials file, never hardcode**
- Add `.claude/` to `.gitignore`
- Sessions are local to each agent workspace
- MEMORIA explicitly forbids storing credentials

## Troubleshooting

### "Authentication failed" or "No token"

```bash
# Check if credentials exist
ls -la ~/.claude/.credentials.json

# If missing, run setup
claude setup-token
```

### "command not found: claude"

```bash
# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Verify installation
which claude
claude --version
```

### Token works in terminal but not in exec

The token must be exported in the same shell session:
```bash
# ✅ CORRECT - Same session
CLAUDE_CODE_OAUTH_TOKEN=xxx claude --print "task"

# ❌ WRONG - Separate commands
export CLAUDE_CODE_OAUTH_TOKEN=xxx
claude --print "task"  # Token not available
```

## Token Efficiency

| Method | Tokens/Task | Cost |
|--------|-------------|------|
| Raw API (full context) | 10,000-50,000 | Per-token |
| Claude Code (tool-based) | ~500 | Flat-rate (Max sub) |

Savings: 80-90% reduction in token usage.

## Related Skills

Install these alongside for full capability:

- `self-improving` — Learn from corrections
- `claude-code-cli-openclaw` — CLI integration details
- `apex-stack-claude-code` — Cognitive framework

## Files in This Skill

```
claude-dev-setup/
├── SKILL.md              # This file
├── sessions-template.md  # Template for claude-code-sessions.md
├── agents-section.md     # AGENTS.md section template
└── setup.sh              # Installation script
```

## Publishing

To publish to ClawHub:

```bash
clawhub publish ./skills/claude-dev-setup \
  --slug claude-dev-setup \
  --name "Claude Dev Setup" \
  --version 1.1.0 \
  --changelog "Added explicit OAuth token extraction guide"
```

## Feedback

- If useful: `clawhub star claude-dev-setup`
- Issues: Open issue on ClawHub
- Stay updated: `clawhub sync`