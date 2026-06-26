# Providing Custom Tools to Claude

> Define custom tools using an in-process MCP server, allowing Claude to call your functions, access APIs, and perform domain operations.

## Quick Reference

| Goal | Method |
|:---|:---|
| Define a tool | `tool()` (TS) / `@tool` (Python) — name, description, schema, handler |
| Register tools with Claude | Wrap in `createSdkMcpServer` / `create_sdk_mcp_server`, pass to `query()`'s `mcpServers` |
| Pre-approve tools | Add to `allowedTools` list |
| Remove built-in tools | Pass a `tools` array listing only the built-ins you want |
| Make tools callable in parallel | Set `readOnlyHint: true` |
| Handle errors without stopping the loop | Return `isError: true` instead of throwing |
| Return images/files | Use `image` or `resource` blocks in the content array |
| Return structured data | Set `structuredContent` |

## Creating a Custom Tool

A tool definition consists of four parts:

1. **Name**: Unique identifier
2. **Description**: Claude reads this to decide when to call it
3. **Input schema**: Zod schema (TypeScript) or type dict/JSON Schema (Python)
4. **Handler**: Async function that receives validated args and returns `{ content, structuredContent?, isError? }`

### TypeScript Example

```typescript
import { tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const getTemperature = tool(
  "get_temperature",
  "Get the current temperature at a location",
  {
    latitude: z.number().describe("Latitude coordinate"),
    longitude: z.number().describe("Longitude coordinate")
  },
  async (args) => {
    // args typed from schema: { latitude: number; longitude: number }
    const response = await fetch(`https://api.open-meteo.com/v1/forecast?...`);
    const data = await response.json();
    return { content: [{ type: "text", text: `Temperature: ${data.current.temperature_2m}°F` }] };
  }
);

const weatherServer = createSdkMcpServer({
  name: "weather", version: "1.0.0", tools: [getTemperature]
});
```

### Python Example

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("get_temperature", "Get the current temperature at a location", {"latitude": float, "longitude": float})
async def get_temperature(args):
    # ... fetch weather API
    return {"content": [{"type": "text", "text": f"Temperature: {temp}°F"}]}

weather_server = create_sdk_mcp_server(name="weather", version="1.0.0", tools=[get_temperature])
```

### Calling Custom Tools

```typescript
for await (const message of query({
  prompt: "What's the temperature in San Francisco?",
  options: {
    mcpServers: { weather: weatherServer },
    allowedTools: ["mcp__weather__get_temperature"]
  }
})) { /* ... */ }
```

Tool name format: `mcp__{server_name}__{tool_name}`, wildcard: `mcp__weather__*`

## Tool Annotations

As the fifth argument to `tool()` (TS) or the `annotations` keyword argument to `@tool` (Python):

| Field | Default | Meaning |
|:---|:---|:---|
| `readOnlyHint` | `false` | Tool doesn't modify environment, can be called in parallel with other read-only tools |
| `destructiveHint` | `true` | May perform destructive updates |
| `idempotentHint` | `false` | Repeated calls have no extra effect |
| `openWorldHint` | `true` | Tool reaches outside the process |

Annotations are metadata, not enforced.

## Controlling Tool Access

| Option | Layer | Effect |
|:---|:---|:---|
| `tools: ["Read", "Grep"]` | Availability | Only listed built-in tools appear in context |
| `tools: []` | Availability | All built-in tools are removed, only MCP tools are available |
| `allowedTools` | Permission | Listed tools run without permission prompts |
| `disallowedTools` | Permission | Listed tools are rejected each time they are called (but tools still appear in context) |

Prefer `tools` over `disallowedTools` for restricting built-in tools.

## Handling Errors

- Return `isError: true`: Agent loop continues, Claude sees the error and can react
- Throw an exception: Agent loop stops, treated as unexpected failure

```typescript
return { content: [{ type: "text", text: "Database connection failed" }], isError: true };
```

```python
return {"content": [{"type": "text", "text": "Database connection failed"}], "isError": True}
```

## Returning Images and Resources

```typescript
return {
  content: [
    { type: "image", data: base64String, mimeType: "image/png" },
    { type: "resource", uri: "file:///path/to/report.pdf", mimeType: "application/pdf" }
  ]
};
```

## Returning Structured Data

```typescript
return {
  content: [{ type: "text", text: "Analysis complete" }],
  structuredContent: { score: 95, category: "performance", recommendations: ["..."] }
};
```

## Optional Parameters

- TypeScript: Add `.default()` to Zod fields
- Python: Omit parameters from the schema, mention in description, read with `args.get()`