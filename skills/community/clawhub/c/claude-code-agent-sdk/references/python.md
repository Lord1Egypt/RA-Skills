# Python SDK API Reference

## Installation
```bash
pip install claude-agent-sdk
```

## query() Function

```python
async def query(
    *, prompt: str | AsyncIterable[dict],
    options: ClaudeAgentOptions | None = None,
    transport: Transport | None = None
) -> AsyncIterator[Message]
```

Each call creates a new session, returns `AsyncIterator[Message]`.

## ClaudeSDKClient

Client that maintains a conversation session (supports multi-turn, interruption):

```python
class ClaudeSDKClient:
    def __init__(self, options=None, transport=None)
    async def connect(self, prompt=None) -> None
    async def query(self, prompt, session_id="default") -> None
    async def receive_response(self) -> AsyncIterator[Message]
    async def interrupt(self) -> None
    async def set_permission_mode(self, mode: str) -> None
    async def set_model(self, model: str | None = None) -> None
    async def disconnect(self) -> None
```

**query() vs ClaudeSDKClient:**
- `query()`: One-off tasks, new session each time, no interrupt support
- `ClaudeSDKClient`: Ongoing conversation, multi-turn context, supports interrupt

## tool() Decorator

```python
@tool("greet", "Greet a user", {"name": str})
async def greet(args: dict) -> dict:
    return {"content": [{"type": "text", "text": f"Hello, {args['name']}!"}]}
```

`input_schema` supports simple type mapping or JSON Schema. Annotations set via `ToolAnnotations`.

## create_sdk_mcp_server()

```python
calculator = create_sdk_mcp_server(name="calc", version="2.0.0", tools=[add, multiply])
options = ClaudeAgentOptions(mcp_servers={"calc": calculator})
```

## Session Management Functions

- `list_sessions(directory, limit, include_worktrees)` → `list[SDKSessionInfo]`
- `get_session_messages(session_id, directory, limit, offset)` → `list[SessionMessage]`
- `get_session_info(session_id, directory)` → `SDKSessionInfo | None`
- `rename_session(session_id, title, directory)` → `None`
- `tag_session(session_id, tag, directory)` → `None`

## ClaudeAgentOptions Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `allowed_tools` | `list[str]` | Auto-approved tools |
| `disallowed_tools` | `list[str]` | Blocked tools |
| `permission_mode` | `str` | default/acceptEdits/plan/dontAsk/bypassPermissions |
| `system_prompt` | `str` | Custom system prompt |
| `max_turns` | `int` | Maximum turns |
| `max_budget_usd` | `float` | Maximum budget |
| `mcp_servers` | `dict` | MCP server configuration |
| `hooks` | `dict` | Hook configuration |
| `agents` | `dict[str, AgentDefinition]` | Sub-agent definitions |
| `can_use_tool` | `Callable` | Tool approval callback |
| `include_partial_messages` | `bool` | Enable streaming output |
| `setting_sources` | `list[str]` | Setting sources |
| `cwd` | `str` | Working directory |
| `env` | `dict` | Environment variables |
| `model` | `str` | Model selection |

## Message Types

- `SystemMessage` — Session events (subtype: init, compact_boundary)
- `AssistantMessage` — Claude response (list of content blocks)
- `UserMessage` — Tool results
- `ResultMessage` — Final result (subtype, result, total_cost_usd, session_id)
- `StreamEvent` — Stream events (event field)

## AgentDefinition

```python
AgentDefinition(
    description="...",  # When to use
    prompt="...",       # System prompt
    tools=["Read", ...],  # Allowed tools
    model="sonnet",     # Model override
    skills=[...],       # Pre-loaded skills
    max_turns=None,     # Maximum turns
    effort="high",      # Reasoning level
    background=False,   # Run in background
)