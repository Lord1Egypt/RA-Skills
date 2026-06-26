# Handling Approvals and User Input

Claude requests user input in two scenarios: **tool permission approvals** and **AskUserQuestion clarification questions**. Handle these via the `canUseTool` callback.

## Detecting Input Requests

```python
async def handle_tool_request(tool_name, input_data, context):
    # Check tool_name == "AskUserQuestion" to distinguish clarification questions
    ...
options = ClaudeAgentOptions(can_use_tool=handle_tool_request)
```

## Response Types

| Response | Python | TypeScript |
|----------|--------|------------|
| **Allow** | `PermissionResultAllow(updated_input=...)` | `{ behavior: "allow", updatedInput }` |
| **Deny** | `PermissionResultDeny(message=...)` | `{ behavior: "deny", message }` |

## Strategy Patterns

**Approve:** Pass input through as-is
**Approve and modify:** Modify input before execution (e.g., sandbox path rewriting)
**Approve and remember:** Echo permission rule in `context.suggestions`, skip prompt next time
**Deny:** Block tool, Claude sees denial message
**Suggest alternatives:** Provide guidance in denial message
**Redirect:** Send entirely new instructions using streaming input

## AskUserQuestion

When `tool_name == "AskUserQuestion"`, Claude has clarification questions. `input_data` contains a `questions` array, each with `question`, `header`, `options` (multi-select list). Return user answers:

```python
return PermissionResultAllow(updated_input={
    "answers": [{"question": "Which database?", "answer": "PostgreSQL"}]
})
```

## Key Considerations

- Callback can remain pending indefinitely
- Python requires `PreToolUse` hook + streaming mode to keep stream open
- TypeScript's `options` parameter includes `signal: AbortSignal` and `suggestions`