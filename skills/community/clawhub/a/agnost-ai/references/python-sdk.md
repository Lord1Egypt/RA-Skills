# Python SDK Reference

Complete reference for Agnost Python SDKs.

## Packages

| Package | Purpose | Install | Import |
|---------|---------|---------|--------|
| `agnost` | AI conversation tracking | `pip install agnost` | `import agnost` |
| `agnost-mcp` | MCP/FastMCP server analytics | `pip install agnost-mcp` | `from agnost_mcp import track, config` |

---

## Conversation SDK (`agnost`)

### Installation

```bash
pip install agnost
# or
uv add agnost
```

### Module Import

```python
import agnost
```

---

### Global Functions

#### `init(write_key: str, **kwargs) -> bool`

Initialize the SDK. Must be called before any other methods.

**Parameters:**
- `write_key`: Your organization ID from the Agnost dashboard
- `endpoint` (str, optional): API endpoint URL, default `"https://api.agnost.ai"`
- `debug` (bool, optional): Enable debug logging, default `False`

**Returns:** `True` if initialization succeeded

```python
# Basic
agnost.init("your-org-id")

# With options
agnost.init("your-org-id", debug=True, endpoint="https://api.agnost.ai")
```

---

#### `begin(user_id, agent_name, input, conversation_id, properties) -> Interaction`

Start tracking an interaction for deferred completion.

**Parameters:**
- `user_id` (str, optional): User identifier, default `""`
- `agent_name` (str, optional): Agent name, default `"default"`
- `input` (str, optional): Input text (can set later with `set_input()`)
- `conversation_id` (str, optional): Group related events
- `properties` (dict, optional): Custom metadata

**Returns:** `Interaction` object

```python
interaction = agnost.begin(
    user_id="user_123",
    agent_name="weather-agent",
    input="What's the weather?",
    conversation_id="conv_456",
    properties={"model": "gpt-4", "temperature": 0.7}
)

# Process...
result = call_ai()

# Complete
interaction.end(output=result)
```

---

#### `track(user_id, input, output, agent_name, conversation_id, properties, timestamp, success, latency) -> str`

Track a complete AI interaction in a single call.

**Parameters:**
- `user_id` (str, optional): User identifier, default `""`
- `input` (str, optional): Input text/prompt
- `output` (str, optional): Output/response text (error message if `success=False`)
- `agent_name` (str, optional): Agent name, default `"default"`
- `conversation_id` (str, optional): Group related events
- `properties` (dict, optional): Custom metadata
- `timestamp` (datetime, optional): Event timestamp, default now
- `success` (bool, optional): Whether successful, default `True`
- `latency` (int, optional): Execution time in milliseconds

**Returns:** Event ID string or `None`

```python
agnost.track(
    user_id="user_123",
    input="What's the weather?",
    output="It's sunny, 72°F",
    agent_name="weather-agent",
    success=True,
    latency=150,
    properties={"tokens": 42}
)
```

---

#### `identify(user_id: str, traits: dict) -> bool`

Associate user metadata with a user ID.

**Parameters:**
- `user_id`: User identifier
- `traits`: Dictionary of user traits

**Returns:** `True` if successful

```python
agnost.identify("user_123", {
    "name": "John Doe",
    "email": "john@example.com",
    "plan": "premium",
    "company": "Acme Inc"
})
```

---

#### `flush() -> None`

Manually flush all queued events.

```python
agnost.flush()
```

---

#### `shutdown() -> None`

Shutdown the SDK and flush remaining events.

```python
agnost.shutdown()

# Or register for cleanup
import atexit
atexit.register(agnost.shutdown)
```

---

### Class: `Interaction`

Represents an in-progress interaction created by `begin()`.

#### Methods

##### `set_input(text: str) -> Interaction`

Set or update the input text. Chainable.

```python
interaction.set_input("Updated query")
```

##### `set_property(key: str, value: Any) -> Interaction`

Set a single property. Chainable.

```python
interaction.set_property("model", "gpt-4")
```

##### `set_properties(properties: dict) -> Interaction`

Set multiple properties. Chainable.

```python
interaction.set_properties({
    "model": "gpt-4",
    "tokens": 42,
    "version": "v2"
})
```

##### `end(output, success, latency, **extra) -> str`

Complete the interaction and send the event.

**Parameters:**
- `output` (str, optional): Output/result text (error message if `success=False`)
- `success` (bool, optional): Success status, default `True`
- `latency` (int, optional): Override auto-calculated latency (ms)
- `**extra`: Additional properties to merge

**Returns:** Event ID string

```python
# Basic
event_id = interaction.end(output="The weather is sunny")

# With error
event_id = interaction.end(output="Error occurred", success=False)

# With custom latency
event_id = interaction.end(output="Result", latency=200)

# With extra properties
event_id = interaction.end(output="Result", tokens=42, cached=True)
```

---

## MCP SDK (`agnost-mcp`)

### Installation

```bash
pip install agnost-mcp
# or
uv add agnost-mcp
```

### Module Import

```python
from agnost_mcp import track, config
```

---

#### `track(server, org_id, cfg) -> server`

Enable analytics for a FastMCP server.

**Parameters:**
- `server`: FastMCP server instance
- `org_id`: Organization ID
- `cfg`: Config object from `config()`

**Returns:** The server with tracking enabled

```python
from mcp.server.fastmcp import FastMCP
from agnost_mcp import track, config

mcp = FastMCP("my-server")

@mcp.tool()
def my_tool(param: str) -> str:
    return f"Result: {param}"

track(mcp, "your-org-id", config(
    endpoint="https://api.agnost.ai",
    disable_input=False,
    disable_output=False
))

mcp.run()
```

---

#### `config(endpoint, disable_input, disable_output) -> Config`

Create a configuration object (mandatory for `track()`).

**Parameters:**
- `endpoint` (str): API endpoint URL
- `disable_input` (bool): Don't track input arguments
- `disable_output` (bool): Don't track output results

```python
cfg = config(
    endpoint="https://api.agnost.ai",
    disable_input=False,
    disable_output=False
)
```

---

## Complete Examples

### FastAPI Integration

```python
from fastapi import FastAPI, Request
import agnost

app = FastAPI()
agnost.init("your-org-id")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_id = data.get("user_id", "anonymous")
    message = data.get("message")

    interaction = agnost.begin(
        user_id=user_id,
        agent_name="chat-api",
        input=message,
        conversation_id=data.get("conversation_id")
    )

    try:
        response = await call_ai_model(message)
        interaction.end(output=response, success=True)
        return {"response": response}
    except Exception as e:
        interaction.end(output=str(e), success=False)
        raise

@app.on_event("shutdown")
def shutdown():
    agnost.shutdown()
```

### LangChain Integration

```python
from langchain.llms import OpenAI
from langchain.callbacks.base import BaseCallbackHandler
import agnost

agnost.init("your-org-id")

class AgnostCallback(BaseCallbackHandler):
    def __init__(self, user_id: str, conversation_id: str = None):
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.interaction = None

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.interaction = agnost.begin(
            user_id=self.user_id,
            agent_name="langchain",
            input=prompts[0] if prompts else "",
            conversation_id=self.conversation_id
        )

    def on_llm_end(self, response, **kwargs):
        if self.interaction:
            output = response.generations[0][0].text
            self.interaction.end(output=output)

# Usage
llm = OpenAI(callbacks=[AgnostCallback("user_123", "conv_456")])
result = llm("What is the capital of France?")
```

### FastMCP Server

```python
from mcp.server.fastmcp import FastMCP
from agnost_mcp import track, config

# Create server
mcp = FastMCP("analytics-server")

@mcp.tool()
async def analyze_text(text: str) -> str:
    """Analyze text and return statistics"""
    words = text.split()
    return f"Word count: {len(words)}, Characters: {len(text)}"

@mcp.tool()
async def generate_report(data_type: str, time_range: str) -> str:
    """Generate a report based on data type and time range"""
    return f"Report for {data_type} over {time_range}: Success"

# Enable tracking
track(mcp, "your-org-id", config(
    endpoint="https://api.agnost.ai",
    disable_input=False,
    disable_output=False
))

if __name__ == "__main__":
    mcp.run()
```

### Error Handling Pattern

```python
import agnost

agnost.init("your-org-id")

def process_user_request(user_id: str, query: str):
    interaction = agnost.begin(
        user_id=user_id,
        agent_name="request-processor",
        input=query
    )

    try:
        # Validate input
        if not query.strip():
            raise ValueError("Empty query")

        # Process
        result = expensive_ai_operation(query)

        # Success
        interaction.set_property("tokens_used", result.tokens)
        interaction.end(output=result.text, success=True)
        return result.text

    except ValueError as e:
        # Validation error
        interaction.end(output=f"Validation error: {e}", success=False)
        raise

    except Exception as e:
        # Unexpected error
        interaction.end(output=f"Internal error: {e}", success=False)
        raise
```

### Conversation Grouping

```python
import agnost
import uuid

agnost.init("your-org-id")

# Start a conversation
conversation_id = f"conv_{uuid.uuid4()}"

# First turn
agnost.track(
    user_id="user_123",
    input="Hello!",
    output="Hi! How can I help?",
    agent_name="chatbot",
    conversation_id=conversation_id
)

# Second turn
agnost.track(
    user_id="user_123",
    input="What's the weather?",
    output="It's sunny today.",
    agent_name="chatbot",
    conversation_id=conversation_id
)

# Third turn
agnost.track(
    user_id="user_123",
    input="Thanks!",
    output="You're welcome!",
    agent_name="chatbot",
    conversation_id=conversation_id
)

agnost.shutdown()
```
