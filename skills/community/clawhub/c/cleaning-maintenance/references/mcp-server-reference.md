# MCP Server Reference

TIDY's public API is an [MCP](https://modelcontextprotocol.io/) server, compatible with Claude Desktop, Claude Code, Cursor, and any MCP client.

**Endpoint:** `POST https://public-api.tidy.com/mcp` (Streamable HTTP)

## Setup

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "tidy": {
      "url": "https://public-api.tidy.com/mcp"
    }
  }
}
```

### Claude Code

```bash
claude mcp add tidy --transport http https://public-api.tidy.com/mcp
```

### Any MCP Client

Connect to `https://public-api.tidy.com/mcp` using Streamable HTTP transport. The server supports `initialize`, `tools/list`, and `tools/call` methods.

## Available Tools

### `login`

Authenticate with an existing TIDY account.

```json
{
  "name": "login",
  "description": "Authenticate with an existing TIDY account and get an API token.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "email": { "type": "string", "description": "The account email address" },
      "password": { "type": "string", "description": "The account password" }
    },
    "required": ["email", "password"]
  }
}
```

**Returns:** `{ "token": "...", "customer_id": 12345, "message": "Authenticated successfully..." }`

### `signup`

Create a new TIDY account.

```json
{
  "name": "signup",
  "description": "Create a new TIDY account and get an API token.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "email": { "type": "string", "description": "Email address for the new account" },
      "password": { "type": "string", "description": "Password (min 8 characters)" },
      "first_name": { "type": "string", "description": "First name" },
      "last_name": { "type": "string", "description": "Last name" }
    },
    "required": ["email", "password", "first_name", "last_name"]
  }
}
```

**Returns:** `{ "token": "...", "customer_id": 12345, "message": "Account created successfully..." }`

### `message_tidy`

Send a natural-language request. **This is the primary tool — use it for everything.**

```json
{
  "name": "message_tidy",
  "description": "Send a freeform natural language message to TIDY for ALL property management requests.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "message": { "type": "string", "description": "Your request in natural language" },
      "context": {
        "type": "object",
        "description": "Optional context to scope the request",
        "properties": {
          "address_id": { "type": "integer", "description": "Relevant address ID" },
          "booking_id": { "type": "integer", "description": "Relevant booking ID" },
          "issue_id": { "type": "integer", "description": "Relevant task/issue ID" },
          "guest_reservation_id": { "type": "integer", "description": "Relevant guest reservation ID" }
        }
      },
      "response_schema": {
        "type": "object",
        "description": "Optional JSON Schema for structured responses"
      }
    },
    "required": ["message"]
  }
}
```

**Returns:**
```json
{
  "object": "message_tidy",
  "id": 12345,
  "message": "Schedule a turnover clean...",
  "status": "processing",
  "is_complete": false,
  "response_message": null,
  "next_step": "Poll get_message_tidy with this id until is_complete is true"
}
```

### `get_message_tidy`

Poll for the result of a `message_tidy` request.

```json
{
  "name": "get_message_tidy",
  "description": "Poll the status of a previously submitted message_tidy request.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "message_tidy_id": { "type": "integer", "description": "The ID of the message to retrieve" }
    },
    "required": ["message_tidy_id"]
  }
}
```

**Returns** (when complete):
```json
{
  "object": "message_tidy",
  "id": 12345,
  "status": "completed",
  "is_complete": true,
  "response_message": "Done! I've scheduled a turnover clean..."
}
```

### `list_messages_tidy`

List all previously submitted messages.

```json
{
  "name": "list_messages_tidy",
  "description": "List all previously submitted freeform messages. Optionally filter by status.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "status": { "type": "array", "items": { "type": "string" }, "description": "Filter by status" }
    },
    "required": []
  }
}
```

## Async Pattern

`message_tidy` is **asynchronous**. Always follow this pattern:

1. Call `message_tidy` with your request
2. Note the returned `id`
3. Poll `get_message_tidy` with that ID every 3-5 seconds
4. When `is_complete` is `true`, read `response_message`
5. If TIDY needs more info, `response_message` will ask — relay to the user, then call `message_tidy` again with their answer

**Status values:** `received` → `processing` → `completed` or `failed`

**Never return a pending response to the user.** Always poll until complete.
