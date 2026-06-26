# Hooks — Intercept and Control Agent Behavior

Use hooks to run custom code at key points during agent execution.

## How Hooks Work

1. **Event triggers** — Something happens during agent execution
2. **SDK collects** — Checks for hooks registered for that event
3. **Matcher filters** — Regex pattern tests the event target
4. **Callback executes** — Receives input (tool name, arguments, session ID)
5. **Callback returns decision** — allow, deny, modify input, or inject context

## Available Hooks

| Hook Event | Python | TypeScript | Trigger | Example Use Case |
|-----------|--------|------------|---------|------------------|
| `PreToolUse` | ✅ | ✅ | Before tool invocation request | Block dangerous shell commands |
| `PostToolUse` | ✅ | ✅ | After tool execution | Log all file changes |
| `PostToolUseFailure` | ✅ | ✅ | Tool execution fails | Handle errors |
| `UserPromptSubmit` | ✅ | ✅ | User prompt submission | Inject additional context |
| `Stop` | ✅ | ✅ | Agent execution stops | Save session state |
| `SubagentStart` | ✅ | ✅ | Subagent initialization | Track parallel tasks |
| `SubagentStop` | ✅ | ✅ | Subagent completes | Aggregate results |
| `PreCompact` | ✅ | ✅ | Compaction requested | Archive complete records |
| `PermissionRequest` | ✅ | ✅ | Permission dialog | Custom permission handling |
| `Notification` | ✅ | ✅ | Agent status message | Send to Slack |
| `SessionStart/End` | ❌ | ✅ | Session lifecycle | Telemetry |
| `PostToolBatch` | ❌ | ✅ | After batch tool resolution | Inject conventions |

## Configuration

```python
options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [HookMatcher(matcher="Bash", hooks=[my_callback])]
    }
)
```

## Matcher

`matcher` is a regular expression string. Built-in tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch, Agent, etc. MCP tools: `mcp__<server>__<action>`.

## Callback Function

**Input:** `input_data` (event details), `tool_use_id`, `context`
**Output:** `hookSpecificOutput` with `permissionDecision` (allow/deny/ask/defer), `permissionDecisionReason`, `updatedInput`

**Permission priority:** deny > defer > ask > allow

## Common Patterns

**Block dangerous operations:**
```python
async def protect_env(input_data, tool_use_id, context):
    if input_data["tool_input"].get("file_path") == ".env":
        return {"hookSpecificOutput": {
            "hookEventName": input_data["hook_event_name"],
            "permissionDecision": "deny",
            "permissionDecisionReason": "Cannot modify .env files"
        }}
    return {}
```

**Modify tool input (sandbox redirection):**
```python
async def redirect(input_data, tool_use_id, context):
    return {"hookSpecificOutput": {
        "hookEventName": input_data["hook_event_name"],
        "permissionDecision": "allow",
        "updatedInput": {**input_data["tool_input"], "file_path": f"/sandbox{original_path}"}
    }}
```

**Auto-approve read-only tools:**
```python
if input_data["tool_name"] in ["Read", "Glob", "Grep"]:
    return {"hookSpecificOutput": {
        "permissionDecision": "allow",
        "permissionDecisionReason": "Read-only tool auto-approved"
    }}
```

## Asynchronous Output

Return `{"async": True, "asyncTimeout": 30000}` to allow the agent to continue without waiting for the hook to complete. Use only for side effects like logging/metrics/notifications.