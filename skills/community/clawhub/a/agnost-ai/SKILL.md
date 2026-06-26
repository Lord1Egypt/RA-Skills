---
name: agnost-ingestion
description: USE when implementing data ingestion for Agnost AI analytics. Contains API reference, SDK guides for Python and TypeScript, and code examples for tracking AI conversations, MCP server events, and user interactions.
license: MIT
metadata:
  author: Agnost AI
  version: "1.0.0"
---

# Agnost Data Ingestion

Comprehensive guide for ingesting data into Agnost AI for analytics, monitoring, and insights. Covers the Conversation SDK for tracking AI interactions and the MCP SDK for Model Context Protocol server analytics.

> **Official docs:** [https://docs.agnost.ai](https://docs.agnost.ai)
> **API Endpoint:** `https://api.agnost.ai`
> **Dashboard:** [https://app.agnost.ai](https://app.agnost.ai)

## IMPORTANT: How to Apply This Skill

**Before implementing Agnost ingestion, follow this priority order:**

1. **Identify the use case**: Conversation tracking (AI chatbots, agents) or MCP server analytics
2. **Check SDK references** in the `references/` directory for detailed API
3. **Use provided code examples** as starting points
4. **Cite references** when explaining implementation details

---

## Quick Reference

### SDK Packages

| Use Case | Python | TypeScript/Node.js | Go |
|----------|--------|-------------------|-----|
| **Conversation/AI Tracking** | `pip install agnost` | `npm install agnostai` | N/A |
| **MCP Server Analytics** | `pip install agnost-mcp` | `npm install agnost` | `go get github.com/agnostai/agnost-go` |

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/capture-session` | POST | Create a new conversation/session |
| `/api/v1/capture-event` | POST | Record an event within a session |

---

## Conversation SDK (Recommended for AI Applications)

Use the Conversation SDK when building AI applications, chatbots, or agents that need to track user interactions, inputs, outputs, and performance metrics.

### Python Installation & Setup

```python
# Installation
pip install agnost
# or
uv add agnost

# Basic Setup
import agnost

# Initialize with your org ID (from dashboard)
agnost.init("your-org-id")
```

### TypeScript/Node.js Installation & Setup

```typescript
// Installation
npm install agnostai
// or
pnpm add agnostai

// Basic Setup
import * as agnost from "agnostai";

// Initialize with your org ID (from dashboard)
agnost.init("your-org-id");
```

---

## Core Methods

### 1. `init(org_id, config?)` - Initialize SDK

**Must be called before any tracking methods.**

#### Python
```python
import agnost

# Basic initialization
agnost.init("your-org-id")

# With configuration
agnost.init(
    "your-org-id",
    endpoint="https://api.agnost.ai",  # Custom endpoint (optional)
    debug=True                          # Enable debug logging
)
```

#### TypeScript
```typescript
import * as agnost from "agnostai";

// Basic initialization
agnost.init("your-org-id");

// With configuration
agnost.init("your-org-id", {
  endpoint: "https://api.agnost.ai",  // Custom endpoint (optional)
  debug: true                          // Enable debug logging
});
```

---

### 2. `begin()` + `end()` - Track Interactions (Recommended)

Use the begin/end pattern for **automatic latency calculation** and cleaner code.

#### Python
```python
import agnost

agnost.init("your-org-id")

# Start tracking an interaction
interaction = agnost.begin(
    user_id="user_123",
    agent_name="weather-agent",
    input="What's the weather in NYC?",
    conversation_id="conv_456",  # Optional: group related events
    properties={"model": "gpt-4"}  # Optional: custom metadata
)

# ... Your AI processing happens here ...
response = call_your_ai_model(interaction.input)

# Complete the interaction (latency auto-calculated)
interaction.end(
    output=response,
    success=True  # Set False if the call failed
)
```

#### TypeScript
```typescript
import * as agnost from "agnostai";

agnost.init("your-org-id");

// Start tracking an interaction
const interaction = agnost.begin({
  userId: "user_123",
  agentName: "weather-agent",
  input: "What's the weather in NYC?",
  conversationId: "conv_456",  // Optional: group related events
  properties: { model: "gpt-4" }  // Optional: custom metadata
});

// ... Your AI processing happens here ...
const response = await callYourAIModel(interaction.input);

// Complete the interaction (latency auto-calculated)
interaction.end(response);  // or interaction.end(response, true) for success
```

---

### 3. `track()` - Single-Call Tracking

Use when you have all data available at once (no need for begin/end).

#### Python
```python
import agnost

agnost.init("your-org-id")

agnost.track(
    user_id="user_123",
    input="What's the weather?",
    output="The weather is sunny with 72°F.",
    agent_name="weather-agent",
    conversation_id="conv_456",  # Optional
    success=True,
    latency=150,  # milliseconds
    properties={"model": "gpt-4", "tokens": 42}
)
```

---

### 4. `identify()` - User Enrichment

Associate user metadata with a user ID for richer analytics.

#### Python
```python
import agnost

agnost.init("your-org-id")

agnost.identify("user_123", {
    "name": "John Doe",
    "email": "john@example.com",
    "plan": "premium",
    "company": "Acme Inc"
})
```

#### TypeScript
```typescript
import * as agnost from "agnostai";

agnost.init("your-org-id");

agnost.identify("user_123", {
  name: "John Doe",
  email: "john@example.com",
  plan: "premium",
  company: "Acme Inc"
});
```

---

### 5. `flush()` & `shutdown()` - Resource Management

#### Python
```python
import agnost

# Manually flush pending events
agnost.flush()

# Clean shutdown (flushes and closes connections)
agnost.shutdown()
```

#### TypeScript
```typescript
import * as agnost from "agnostai";

// Manually flush pending events
await agnost.flush();

// Clean shutdown (flushes and closes connections)
await agnost.shutdown();
```

---

## Interaction Object Methods

When using `begin()`, you get an `Interaction` object with these methods:

| Method | Description |
|--------|-------------|
| `set_input(text)` / `setInput(text)` | Set/update the input text |
| `set_property(key, value)` / `setProperty(key, value)` | Add a single custom property |
| `set_properties(dict)` / `setProperties(obj)` | Add multiple custom properties |
| `end(output, success?, latency?)` | Complete and send the event |

#### Example: Building Input Dynamically (Python)

```python
interaction = agnost.begin(
    user_id="user_123",
    agent_name="my-agent"
)

# Build input from multiple sources
interaction.set_input("Combined user query: " + user_input)
interaction.set_property("source", "chat-widget")
interaction.set_properties({"model": "gpt-4", "version": "v2"})

# Process and complete
response = process_query(interaction.input)
interaction.end(output=response)
```

---

## MCP Server Analytics

For tracking Model Context Protocol (MCP) servers, use the MCP SDK.

### Python (FastMCP)

```python
from mcp.server.fastmcp import FastMCP
from agnost_mcp import track, config

# Create FastMCP server
mcp = FastMCP("my-mcp-server")

# Add your tools
@mcp.tool()
def my_tool(param: str) -> str:
    return f"Result: {param}"

# Enable tracking
track(mcp, "your-org-id", config(
    endpoint="https://api.agnost.ai",
    disable_input=False,   # Track input arguments
    disable_output=False   # Track output results
))

# Run server
mcp.run()
```

### TypeScript (MCP SDK)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { trackMCP } from "agnost";

// Create MCP server
const server = new Server({
  name: "my-mcp-server",
  version: "1.0.0"
}, {
  capabilities: { tools: {} }
});

// Enable tracking
trackMCP(server, "your-org-id", {
  endpoint: "https://api.agnost.ai",
  disableInput: false,
  disableOutput: false
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Go (mcp-go)

```go
package main

import (
    "github.com/agnostai/agnost-go/agnost"
    "github.com/mark3labs/mcp-go/server"
)

func main() {
    s := server.NewMCPServer("my-server", "1.0.0")

    // Add tools...

    // Enable tracking
    agnost.Track(s, "your-org-id", &agnost.Config{
        DisableInput:  false,
        DisableOutput: false,
        BatchSize:     10,
        LogLevel:      "info",
    })

    server.ServeStdio(s)
}
```

---

## API Reference (Direct HTTP)

For cases where you need direct API access without an SDK.

### Create Session

```bash
curl -X POST https://api.agnost.ai/api/v1/capture-session \
  -H "Content-Type: application/json" \
  -H "X-Org-Id: your-org-id" \
  -d '{
    "session_id": "unique-session-id",
    "client_config": "my-app",
    "connection_type": "http",
    "ip": "",
    "user_data": {
      "user_id": "user_123",
      "email": "user@example.com"
    },
    "tools": ["tool1", "tool2"]
  }'
```

### Capture Event

```bash
curl -X POST https://api.agnost.ai/api/v1/capture-event \
  -H "Content-Type: application/json" \
  -H "X-Org-Id: your-org-id" \
  -d '{
    "session_id": "unique-session-id",
    "primitive_type": "tool",
    "primitive_name": "weather_lookup",
    "latency": 150,
    "success": true,
    "args": "{\"city\": \"NYC\"}",
    "result": "{\"temp\": 72}",
    "metadata": {
      "model": "gpt-4",
      "tokens": "42"
    }
  }'
```

---

## Data Structures

### Session Request

```json
{
  "session_id": "string (UUID or custom ID)",
  "client_config": "string (app identifier)",
  "connection_type": "string (http/stdio/sse)",
  "ip": "string (optional)",
  "user_data": {
    "user_id": "string",
    "...": "any additional user fields"
  },
  "tools": ["array", "of", "tool", "names"]
}
```

### Event Request

```json
{
  "session_id": "string (must match existing session)",
  "primitive_type": "string (tool/resource/prompt)",
  "primitive_name": "string (name of the primitive)",
  "latency": "integer (milliseconds)",
  "success": "boolean",
  "args": "string (JSON-encoded input)",
  "result": "string (JSON-encoded output)",
  "checkpoints": [
    {
      "name": "string",
      "timestamp": "integer (ms since start)",
      "metadata": {}
    }
  ],
  "metadata": {
    "key": "value pairs"
  }
}
```

---

## Configuration Options

### Python Conversation SDK

```python
agnost.init(
    "your-org-id",
    endpoint="https://api.agnost.ai",  # API endpoint
    debug=False                         # Enable debug logging
)
```

### TypeScript Conversation SDK

```typescript
interface ConversationConfig {
  endpoint?: string;  // API endpoint (default: https://api.agnost.ai)
  debug?: boolean;    // Enable debug logging (default: false)
}

agnost.init("your-org-id", { endpoint: "...", debug: true });
```

### Python MCP SDK (FastMCP)

```python
from agnost_mcp import track, config

track(server, "your-org-id", config(
    endpoint="https://api.agnost.ai",
    disable_input=False,   # Don't track input arguments
    disable_output=False   # Don't track output results
))
```

### TypeScript MCP SDK

```typescript
import { trackMCP, createConfig } from "agnost";

const cfg = createConfig({
  endpoint: "https://api.agnost.ai",
  disableInput: false,
  disableOutput: false
});

trackMCP(server, "your-org-id", cfg);
```

### Go MCP SDK

```go
type Config struct {
    Endpoint         string        // default: "https://api.agnost.ai"
    DisableInput     bool          // default: false
    DisableOutput    bool          // default: false
    BatchSize        int           // default: 5
    MaxRetries       int           // default: 3
    RetryDelay       time.Duration // default: 1s
    RequestTimeout   time.Duration // default: 5s
    LogLevel         string        // "debug", "info", "warning", "error"
    Identify         IdentifyFunc  // optional user identification
}
```

---

## Best Practices

### 1. Always Initialize Early
```python
# At application startup
import agnost
agnost.init("your-org-id")
```

### 2. Use begin/end for Accurate Latency
```python
# Automatically calculates processing time
interaction = agnost.begin(user_id="u1", agent_name="agent")
# ... processing ...
interaction.end(output=result)
```

### 3. Group Related Events with conversation_id
```python
# All events for a single chat session
conversation_id = f"chat_{session_id}"
interaction = agnost.begin(
    user_id="u1",
    conversation_id=conversation_id,
    agent_name="chatbot"
)
```

### 4. Handle Errors Gracefully
```python
interaction = agnost.begin(user_id="u1", agent_name="agent")
try:
    result = process_request()
    interaction.end(output=result, success=True)
except Exception as e:
    interaction.end(output=str(e), success=False)
```

### 5. Shutdown Cleanly
```python
import atexit
import agnost

atexit.register(agnost.shutdown)
```

---

## When to Apply

This skill activates when you encounter:

- Data ingestion implementation for Agnost
- AI conversation tracking setup
- MCP server analytics integration
- Event/session capture API usage
- SDK initialization questions
- Latency tracking requirements
- User identification/enrichment

---

## Additional Resources

- **Python SDK Reference**: `references/python-sdk.md`
- **TypeScript SDK Reference**: `references/typescript-sdk.md`
- **API Reference**: `references/api-reference.md`
- **Dashboard**: [https://app.agnost.ai](https://app.agnost.ai)
- **Discord Community**: [https://discord.gg/agnost](https://discord.gg/agnost)
