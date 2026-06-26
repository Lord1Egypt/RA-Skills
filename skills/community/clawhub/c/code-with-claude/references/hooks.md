# Hooks Reference

Hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at lifecycle events.

## Hook Lifecycle

Events fire at three cadences:
- **Once per session**: `SessionStart`, `SessionEnd`
- **Once per turn**: `UserPromptSubmit`, `Stop`, `StopFailure`
- **Every tool call**: `PreToolUse`, `PostToolUse`

## Hook Events

| Event | When It Fires |
|-------|---------------|
| `SessionStart` | Session begins or resumes |
| `UserPromptSubmit` | Prompt submitted, before Claude processes |
| `PreToolUse` | Before tool call. Can block it |
| `PermissionRequest` | Permission dialog appears |
| `PermissionDenied` | Tool denied by auto mode. Return `{retry: true}` to allow retry |
| `PostToolUse` | After tool succeeds |
| `PostToolUseFailure` | After tool fails |
| `Notification` | Claude sends a notification |
| `SubagentStart` | Subagent spawned |
| `SubagentStop` | Subagent finishes |
| `TaskCreated` | Task created via TaskCreate |
| `TaskCompleted` | Task marked completed |
| `Stop` | Claude finishes responding |
| `StopFailure` | Turn ends due to API error |
| `TeammateIdle` | Agent team teammate going idle |
| `InstructionsLoaded` | CLAUDE.md or rules file loaded |
| `ConfigChange` | Config file changes during session |
| `CwdChanged` | Working directory changes |
| `FileChanged` | Watched file changes on disk |
| `WorktreeCreate` | Worktree being created |
| `WorktreeRemove` | Worktree being removed |
| `PreCompact` | Before context compaction |
| `PostCompact` | After compaction completes |
| `Elicitation` | MCP server requests user input |
| `ElicitationResult` | User responds to MCP elicitation |
| `SessionEnd` | Session terminates |

## Configuration

### Hook Locations

Hooks can be defined in:
- `settings.json` (user, project, or local scope)
- `hooks/hooks.json` (in plugin root)
- Inline in `plugin.json`

### Matcher Patterns

Matchers narrow which tool calls trigger a hook:
- Tool name: `"Bash"`, `"Write|Edit"`, `"mcp__server__tool"`
- `if` condition: `"Bash(rm *)"` matches commands starting with `rm`

### Hook Handler Types

| Type | Description |
|------|-------------|
| `command` | Execute shell command/script |
| `http` | POST event JSON to URL |
| `prompt` | Evaluate with LLM (`$ARGUMENTS` placeholder) |
| `agent` | Run agentic verifier with tools |

### Example: Block Destructive Commands

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

## Exit Code Behavior

| Exit Code | Effect |
|-----------|--------|
| 0 | Success, continue |
| 1 | Error, but continue |
| 2 | Block the operation (PreToolUse blocks tool, UserPromptSubmit blocks prompt) |

## Environment Variables in Hooks

- `CLAUDE_PROJECT_DIR` — project root directory
- `CLAUDE_PLUGIN_ROOT` — plugin root (for plugin hooks)

## Async Hooks

Configure with `"async": true` to run in background without blocking the lifecycle.

## Prompt-Based Hooks

Use `"type": "prompt"` with a response schema for LLM-evaluated hooks. Useful for multi-criteria Stop hooks.

## Agent-Based Hooks

Use `"type": "agent"` for complex verification tasks with full tool access.
