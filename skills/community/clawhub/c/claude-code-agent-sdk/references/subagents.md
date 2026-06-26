# Sub-agents

Sub-agents are independent agent instances that the main agent can spawn to handle focused sub-tasks.

## Defining Sub-agents

```python
from claude_agent_sdk import AgentDefinition

agents={
    "code-reviewer": AgentDefinition(
        description="Expert code review specialist. Use for quality and security reviews.",
        prompt="You are a code review specialist...",
        tools=["Read", "Grep", "Glob"],
        model="sonnet",
    ),
    "test-runner": AgentDefinition(
        description="Runs and analyzes test suites.",
        prompt="You are a test execution specialist...",
        tools=["Bash", "Read", "Grep"],
    ),
}
```

> The `Agent` tool must be in `allowedTools`. Sub-agents cannot spawn their own sub-agents.

## AgentDefinition Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | string | ✅ | Natural language description of when to use this agent |
| `prompt` | string | ✅ | System prompt for the agent |
| `tools` | string[] | ❌ | Allowed tools. Omit to inherit all |
| `disallowedTools` | string[] | ❌ | Tools to remove |
| `model` | string | ❌ | Model override: sonnet/opus/haiku/inherit |
| `skills` | string[] | ❌ | List of pre-loaded skills |
| `maxTurns` | number | ❌ | Maximum turn limit |
| `background` | boolean | ❌ | Run as non-blocking background task |
| `effort` | 'low'\|'medium'\|'high'\|'xhigh'\|'max' | ❌ | Reasoning effort level |
| `permissionMode` | PermissionMode | ❌ | Permission mode |

## Benefits

- **Context isolation** — Intermediate tool calls stay within sub-agent, only final message returns to parent
- **Parallelization** — Multiple sub-agents can run concurrently
- **Specialized instructions** — Each sub-agent has custom system prompt
- **Tool restriction** — Limit to specific tools, reducing risk

## What Sub-agents Inherit

Sub-agents receive: their own system prompt, project CLAUDE.md, tool definitions
Sub-agents do NOT receive: parent conversation history, pre-loaded skills (unless listed in skills)

## Dynamic Agent Configuration

```python
def create_security_agent(security_level: str) -> AgentDefinition:
    return AgentDefinition(
        description="Security code reviewer",
        prompt=f"You are a {'strict' if security_level == 'strict' else 'balanced'} security reviewer...",
        tools=["Read", "Grep", "Glob"],
        model="opus" if security_level == "strict" else "sonnet",
    )
```

## Detecting Sub-agent Invocations

Check `tool_use` blocks with `name` `"Agent"` or `"Task"` (for legacy compatibility). Sub-agent messages include `parent_tool_use_id` field.

## Resuming Sub-agents

1. Capture session ID from `ResultMessage.session_id`
2. Parse `agentId` from message content
3. Pass `resume: session_id` in subsequent query and include agentId in prompt

## Todo Tracking

The SDK automatically creates todos for complex multi-step tasks. Lifecycle: pending → in_progress → completed.

Monitor `TodoWrite` tool calls:

```python
if isinstance(block, ToolUseBlock) and block.name == "TodoWrite":
    todos = block.input["todos"]
    for todo in todos:
        status = "✅" if todo["status"] == "completed" else "🔧" if todo["status"] == "in_progress" else "❌"
        print(f"{status} {todo['content']}")