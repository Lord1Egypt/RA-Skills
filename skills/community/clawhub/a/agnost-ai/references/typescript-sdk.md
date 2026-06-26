# TypeScript SDK Reference

Complete reference for Agnost TypeScript/Node.js SDKs.

## Packages

| Package | Purpose | Install | Import |
|---------|---------|---------|--------|
| `agnostai` | AI conversation tracking | `npm install agnostai` | `import * as agnost from "agnostai"` |
| `agnost` | MCP server analytics | `npm install agnost` | `import { trackMCP } from "agnost"` |

---

## Conversation SDK (`agnostai`)

### Installation

```bash
npm install agnostai
# or
yarn add agnostai
# or
pnpm add agnostai
```

### Module Import

```typescript
import * as agnost from "agnostai";

// Or individual imports
import { ConversationClient, Interaction } from "agnostai";
```

---

### Global Client Methods

#### `init(writeKey: string, config?: ConversationConfig): boolean`

Initialize the SDK. Must be called before any other methods.

**Parameters:**
- `writeKey`: Your organization ID from the Agnost dashboard
- `config`: Optional configuration object

**Returns:** `true` if initialization succeeded

```typescript
// Basic
agnost.init("your-org-id");

// With config
agnost.init("your-org-id", {
  endpoint: "https://api.agnost.ai",
  debug: true
});
```

---

#### `begin(options: BeginOptions): Interaction | null`

Start tracking an interaction for deferred completion.

**Parameters:**
```typescript
interface BeginOptions {
  userId: string;              // Required: User identifier
  agentName: string;           // Required: Agent/primitive name
  input?: string;              // Optional: Input text
  conversationId?: string;     // Optional: Group related events
  properties?: EventProperties; // Optional: Custom metadata
  event?: string;              // Optional: Event name
  interactionId?: string;      // Optional: Custom interaction ID
}
```

**Returns:** `Interaction` object or `null` if not initialized

```typescript
const interaction = agnost.begin({
  userId: "user_123",
  agentName: "weather-agent",
  input: "What's the weather?",
  conversationId: "conv_456",
  properties: { model: "gpt-4", temperature: 0.7 }
});

// Process...
const result = await callAI();

// Complete
interaction?.end(result);
```

---

#### `identify(userId: string, traits: UserTraits): boolean`

Associate user metadata with a user ID.

**Parameters:**
- `userId`: User identifier
- `traits`: Object with user traits

**Returns:** `true` if successful

```typescript
agnost.identify("user_123", {
  name: "John Doe",
  email: "john@example.com",
  plan: "premium",
  company: "Acme Inc"
});
```

---

#### `getInteraction(interactionId: string): Interaction | null`

Retrieve an active interaction by ID. Useful for completing interactions from callbacks.

```typescript
// Start with custom ID
agnost.begin({
  userId: "user_123",
  agentName: "agent",
  interactionId: "my-custom-id"
});

// Later, retrieve and complete
const interaction = agnost.getInteraction("my-custom-id");
interaction?.end("Response");
```

---

#### `flush(): Promise<void>`

Manually flush all queued events.

```typescript
await agnost.flush();
```

---

#### `shutdown(): Promise<void>`

Shutdown the SDK and flush remaining events.

```typescript
await agnost.shutdown();
```

---

#### `setDebugLogs(enabled: boolean): void`

Enable or disable debug logging.

```typescript
agnost.setDebugLogs(true);   // Enable
agnost.setDebugLogs(false);  // Disable
```

---

### Properties

#### `isInitialized: boolean`

Check if SDK is initialized.

```typescript
if (agnost.isInitialized) {
  // Safe to track events
}
```

#### `queueSize: number`

Get current event queue size.

```typescript
console.log(`Pending events: ${agnost.queueSize}`);
```

---

### Class: `Interaction`

Represents an in-progress interaction created by `begin()`.

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `eventId` | string | Unique event identifier |
| `userId` | string | User identifier |
| `event` | string | Event name |
| `conversationId` | string | Conversation identifier |
| `agentName` | string | Agent name |
| `input` | string | Current input text |
| `properties` | EventProperties | Current properties |
| `isFinished` | boolean | Whether interaction is completed |

#### Methods

##### `setInput(text: string): this`

Set or update the input text. Chainable.

```typescript
interaction.setInput("Updated query");
```

##### `setProperty(key: string, value: any): this`

Set a single property. Chainable.

```typescript
interaction.setProperty("model", "gpt-4");
```

##### `setProperties(properties: EventProperties): this`

Set multiple properties. Chainable.

```typescript
interaction.setProperties({
  model: "gpt-4",
  tokens: 42,
  version: "v2"
});
```

##### `end(output: string, success?: boolean, latency?: number, extra?: Record<string, any>): string`

Complete the interaction and send the event.

**Parameters:**
- `output`: Output/result text (error message if `success=false`)
- `success`: Success status (default: `true`)
- `latency`: Override auto-calculated latency in ms (optional)
- `extra`: Additional properties to merge (optional)

**Returns:** Event ID string

```typescript
// Basic
const eventId = interaction.end("The weather is sunny");

// With error
const eventId = interaction.end("Error occurred", false);

// With custom latency
const eventId = interaction.end("Result", true, 200);

// With extra properties
const eventId = interaction.end("Result", true, undefined, {
  tokens: 42,
  cached: true
});
```

---

### Interfaces

#### `ConversationConfig`

```typescript
interface ConversationConfig {
  endpoint?: string;  // API endpoint (default: "https://api.agnost.ai")
  debug?: boolean;    // Enable debug logging (default: false)
}
```

#### `EventProperties`

```typescript
type EventProperties = Record<string, any>;
```

#### `UserTraits`

```typescript
type UserTraits = Record<string, any>;
```

---

## MCP SDK (`agnost`)

### Installation

```bash
npm install agnost @modelcontextprotocol/sdk
# or
pnpm add agnost @modelcontextprotocol/sdk
```

### Module Import

```typescript
import { trackMCP, createConfig, checkpoint } from "agnost";
```

---

#### `trackMCP(server, orgId, config?): void`

Enable analytics for an MCP server.

**Parameters:**
- `server`: MCP Server instance
- `orgId`: Organization ID
- `config`: Optional configuration object or result of `createConfig()`

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { trackMCP } from "agnost";

const server = new Server({
  name: "my-mcp-server",
  version: "1.0.0"
}, {
  capabilities: { tools: {} }
});

// Basic
trackMCP(server, "your-org-id");

// With config
trackMCP(server, "your-org-id", {
  endpoint: "https://api.agnost.ai",
  disableInput: false,
  disableOutput: false
});
```

---

#### `createConfig(options): Config`

Create a configuration object.

```typescript
import { trackMCP, createConfig } from "agnost";

const config = createConfig({
  endpoint: "https://api.agnost.ai",
  disableInput: false,
  disableOutput: false
});

trackMCP(server, "your-org-id", config);
```

---

#### `checkpoint(name: string, metadata?: any): void`

Add a performance checkpoint within a tool handler.

```typescript
import { trackMCP, checkpoint } from "agnost";

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  checkpoint("validation_start");
  // ... validate input
  checkpoint("validation_complete");

  checkpoint("database_query_start");
  const results = await db.query(/* ... */);
  checkpoint("database_query_complete", { rowCount: results.length });

  return { /* results */ };
});
```

---

### Configuration Options

```typescript
interface MCPConfig {
  endpoint?: string;       // API endpoint (default: "https://api.agnost.ai")
  disableInput?: boolean;  // Don't track input arguments (default: false)
  disableOutput?: boolean; // Don't track output results (default: false)
  identify?: IdentifyFunction; // Optional user identification function
}

type IdentifyFunction = (
  request: Request | undefined,
  env: Record<string, string>
) => { userId: string; email?: string; role?: string } | null;
```

---

## Complete Examples

### Express.js Integration

```typescript
import express, { Request, Response } from "express";
import * as agnost from "agnostai";

const app = express();
app.use(express.json());

agnost.init("your-org-id", { debug: true });

app.post("/chat", async (req: Request, res: Response) => {
  const { user_id, message, conversation_id } = req.body;

  const interaction = agnost.begin({
    userId: user_id || "anonymous",
    agentName: "chat-api",
    input: message,
    conversationId: conversation_id
  });

  if (!interaction) {
    return res.status(500).json({ error: "Analytics not initialized" });
  }

  try {
    const response = await callAIModel(message);
    interaction.end(response, true);
    res.json({ response });
  } catch (error) {
    interaction.end(String(error), false);
    res.status(500).json({ error: "AI call failed" });
  }
});

// Graceful shutdown
process.on("SIGTERM", async () => {
  await agnost.shutdown();
  process.exit(0);
});

app.listen(3000);
```

### Next.js API Route

```typescript
// app/api/chat/route.ts
import * as agnost from "agnostai";
import { NextRequest, NextResponse } from "next/server";

// Initialize once
if (!agnost.isInitialized) {
  agnost.init(process.env.AGNOST_ORG_ID!);
}

export async function POST(req: NextRequest) {
  const { userId, message, conversationId } = await req.json();

  const interaction = agnost.begin({
    userId,
    agentName: "nextjs-chat",
    input: message,
    conversationId
  });

  try {
    const response = await generateAIResponse(message);
    interaction?.end(response);
    return NextResponse.json({ response });
  } catch (error) {
    interaction?.end(String(error), false);
    return NextResponse.json(
      { error: "Failed to generate response" },
      { status: 500 }
    );
  }
}
```

### Vercel AI SDK Integration

```typescript
import * as agnost from "agnostai";
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";

agnost.init("your-org-id");

export async function chat(userId: string, prompt: string) {
  const interaction = agnost.begin({
    userId,
    agentName: "vercel-ai",
    input: prompt,
    properties: { model: "gpt-4" }
  });

  try {
    const { text } = await generateText({
      model: openai("gpt-4"),
      prompt
    });

    interaction?.setProperty("tokensUsed", text.length / 4);
    interaction?.end(text);
    return text;
  } catch (error) {
    interaction?.end(String(error), false);
    throw error;
  }
}
```

### MCP Server with Tools

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema
} from "@modelcontextprotocol/sdk/types.js";
import { trackMCP, checkpoint } from "agnost";

const server = new Server({
  name: "weather-server",
  version: "1.0.0"
}, {
  capabilities: { tools: {} }
});

// List tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "get_weather",
    description: "Get weather for a city",
    inputSchema: {
      type: "object",
      properties: {
        city: { type: "string", description: "City name" }
      },
      required: ["city"]
    }
  }]
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "get_weather") {
    checkpoint("fetch_start");
    const weather = await fetchWeather(args.city);
    checkpoint("fetch_complete", { city: args.city });

    return {
      content: [{ type: "text", text: JSON.stringify(weather) }]
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// Enable tracking with user identification
trackMCP(server, "your-org-id", {
  endpoint: "https://api.agnost.ai",
  disableInput: false,
  disableOutput: false,
  identify: (request, env) => ({
    userId: request?.headers?.["x-user-id"] || env?.USER_ID || "anonymous",
    email: request?.headers?.["x-user-email"] || env?.USER_EMAIL
  })
});

// Start server
const transport = new StdioServerTransport();
server.connect(transport);
```

### Custom Client Usage

```typescript
import { ConversationClient } from "agnostai";

const client = new ConversationClient();
client.init("your-org-id");

const interaction = client.begin({
  userId: "user_123",
  agentName: "greeting-bot",
  input: "Hello!"
});

interaction.end("Hello! How can I help you today?");

await client.shutdown();
```
