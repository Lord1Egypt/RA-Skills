## 🤖 Claude Code CLI Sessions

You have access to Claude Code CLI for coding tasks. Use it for file operations, refactoring, debugging, and code generation.

### OAuth Token (REQUIRED)

**Token location:** `~/.claude/.credentials.json`

**ALWAYS extract and use the token when calling Claude Code:**

```bash
# Extract token and use in one command
CLAUDE_CODE_OAUTH_TOKEN=$(cat ~/.claude/.credentials.json | grep -o '"accessToken":"[^"]*"' | cut -d'"' -f4) claude --print --dangerously-skip-permissions 'task'
```

**For exec tool:**
```json
exec({
  command: "CLAUDE_CODE_OAUTH_TOKEN=$(cat ~/.claude/.credentials.json | grep -o '\"accessToken\":\"[^\"]*\"' | cut -d'\"' -f4) claude --print --dangerously-skip-permissions 'Task description'",
  background: true,
  yieldMs: 10000
})
```

**If token not found**, user needs to run: `claude setup-token`

### Session Tracking

All background Claude Code sessions are tracked in `memory/claude-code-sessions.md`.

**Before starting a task:**
1. Read `memory/claude-code-sessions.md` to check for running sessions
2. If a similar task is running, report status instead of starting duplicate

**Starting a session:**
```json
exec({
  command: "CLAUDE_CODE_OAUTH_TOKEN=$(cat ~/.claude/.credentials.json | grep -o '\"accessToken\":\"[^\"]*\"' | cut -d'\"' -f4) claude --print --dangerously-skip-permissions 'Task description'",
  background: true,
  yieldMs: 10000
})
```

**After starting:**
1. Note the `sessionId` from the response
2. Append to `memory/claude-code-sessions.md`:
   ```
   | session-id | task-label | Description | 2026-03-24 08:50 UTC | running |
   ```

**Checking status:**
```json
process({ action: "log", sessionId: "session-id" })
```

**On completion:**
Update status column to `completed` or `failed`.

**Label naming:** Use descriptive labels like `build-feature-X`, `refactor-Y-module`, `fix-bug-Z`

### Quick Tasks (< 30 seconds)

For simple tasks, use non-background exec:
```json
exec({
  command: "CLAUDE_CODE_OAUTH_TOKEN=$(cat ~/.claude/.credentials.json | grep -o '\"accessToken\":\"[^\"]*\"' | cut -d'\"' -f4) claude --print --dangerously-skip-permissions 'Quick fix'",
  timeout: 60
})
```

No session tracking needed for quick tasks.

### When User Asks Status

1. Read `memory/claude-code-sessions.md`
2. Find the relevant session by label
3. Poll for output: `process({ action: "log", sessionId: "..." })`
4. Summarize progress for user

### APEX Stack for Projects

For enhanced cognition, add APEX Stack to your project's CLAUDE.md:
```bash
cd /path/to/project
cat ~/.openclaw/workspace-YOURS/skills/apex-stack-claude-code/SKILL.md >> CLAUDE.md
```

This enables:
- **APEX**: Cognitive modes (precision, execution, architecture, creative)
- **MEMORIA**: Persistent project memory
- **ARCHITECT**: Autonomous execution loop