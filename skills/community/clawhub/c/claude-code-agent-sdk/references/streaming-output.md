# Streaming and Output

## Streaming Output

Enable `include_partial_messages` / `includePartialMessages` to receive incremental updates as text and tool calls are generated.

```python
from claude_agent_sdk.types import StreamEvent

options = ClaudeAgentOptions(include_partial_messages=True)
async for message in query(prompt="...", options=options):
    if isinstance(message, StreamEvent):
        event = message.event
        if event.get("type") == "content_block_delta":
            delta = event.get("delta", {})
            if delta.get("type") == "text_delta":
                print(delta.get("text", ""), end="", flush=True)
```

### StreamEvent Structure

| Field | Type | Description |
|-------|------|-------------|
| `event` | dict / BetaRawMessageStreamEvent | Raw Claude API stream event |
| `uuid` | str | Unique identifier |
| `session_id` | str | Session ID |
| `parent_tool_use_id` | str \| None | Parent tool ID for sub-agents |

### Event Types

| Event | Description |
|-------|-------------|
| `message_start` | New message begins |
| `content_block_start` | Content block starts (text or tool_use) |
| `content_block_delta` | Incremental update (text_delta or input_json_delta) |
| `content_block_stop` | Content block ends |
| `message_delta` | Message-level update |
| `message_stop` | Message ends |

### Tool Call Streaming

```python
if event_type == "content_block_start":
    if content_block.get("type") == "tool_use":
        current_tool = content_block.get("name")
elif event_type == "content_block_delta":
    if delta.get("type") == "input_json_delta":
        tool_input += delta.get("partial_json", "")
```

### Limitations
- Extended thinking: StreamEvent not emitted when `max_thinking_tokens` is set
- Structured output: JSON only in final `ResultMessage.structured_output`

## Streaming Input Mode

Two input modes:

### Streaming Input (Default, Recommended)
Supports image attachments, dynamic message queues, real-time interruption, hooks, multi-turn conversations.

```python
async with ClaudeSDKClient(options) as client:
    await client.query(message_generator())
    async for message in client.receive_response():
        print(message)
```

### Single Message Input
Simple one-shot queries. Does not support images, hooks, dynamic message queues. Suitable for stateless environments (lambda).

```python
async for message in query(prompt="Explain the auth flow", options=ClaudeAgentOptions(max_turns=1)):
    if isinstance(message, ResultMessage): print(message.result)
```

## Structured Output

Returns validated JSON. Supports JSON Schema, Zod (TypeScript), Pydantic (Python).

**TypeScript (Zod):**
```typescript
import { z } from "zod";
const schema = z.object({ name: z.string(), age: z.number() });
// Result available in ResultMessage.structured_output
```

**Python (Pydantic):**
```python
from pydantic import BaseModel
class UserInfo(BaseModel): name: str; age: int
options = ClaudeAgentOptions(structured_output={"schema": UserInfo.model_json_schema()})
```

Result appears in `ResultMessage.structured_output`, not in streaming increments.