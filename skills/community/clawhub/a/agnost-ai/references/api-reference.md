# Agnost API Reference

Direct HTTP API for data ingestion when not using an SDK.

## Base URL

```
https://api.agnost.ai/api/v1
```

## Authentication

All requests require the `X-Org-Id` header with your organization ID.

```http
X-Org-Id: your-organization-id
```

---

## Endpoints

### POST `/capture-session`

Create a new conversation/session. Call this before capturing events.

#### Request Headers

```http
Content-Type: application/json
X-Org-Id: <your-org-id>
```

#### Request Body

```json
{
  "session_id": "string (required)",
  "client_config": "string",
  "connection_type": "string",
  "ip": "string",
  "user_data": {
    "user_id": "string",
    "...": "any additional fields"
  },
  "tools": ["string"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | string | Yes | Unique session identifier (UUID or custom string) |
| `client_config` | string | No | Client/app identifier |
| `connection_type` | string | No | Connection type (http, stdio, sse) |
| `ip` | string | No | Client IP address |
| `user_data` | object | No | User metadata (must include `user_id` if present) |
| `tools` | string[] | No | List of available tool names |

#### Example

```bash
curl -X POST https://api.agnost.ai/api/v1/capture-session \
  -H "Content-Type: application/json" \
  -H "X-Org-Id: your-org-id" \
  -d '{
    "session_id": "sess_12345",
    "client_config": "my-chatbot-v2",
    "connection_type": "http",
    "user_data": {
      "user_id": "user_123",
      "name": "John Doe",
      "email": "john@example.com",
      "plan": "premium"
    },
    "tools": ["weather_lookup", "search", "calculator"]
  }'
```

---

### POST `/capture-event`

Record an event within an existing session.

#### Request Headers

```http
Content-Type: application/json
X-Org-Id: <your-org-id>
```

#### Request Body

```json
{
  "session_id": "string (required)",
  "primitive_type": "string (required)",
  "primitive_name": "string (required)",
  "latency": 0,
  "success": true,
  "args": "string (JSON-encoded)",
  "result": "string (JSON-encoded)",
  "checkpoints": [],
  "metadata": {}
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | string | Yes | Session ID from capture-session |
| `primitive_type` | string | Yes | Type: "tool", "resource", "prompt" |
| `primitive_name` | string | Yes | Name of the primitive/agent |
| `latency` | integer | No | Execution time in milliseconds |
| `success` | boolean | No | Whether call succeeded (default: true) |
| `args` | string | No | JSON-encoded input arguments |
| `result` | string | No | JSON-encoded output/result |
| `checkpoints` | array | No | Timing checkpoints within execution |
| `metadata` | object | No | Additional key-value metadata |

#### Checkpoints

Track granular timing within an execution:

```json
{
  "checkpoints": [
    {
      "name": "parse_input",
      "timestamp": 10,
      "metadata": { "tokens": "50" }
    },
    {
      "name": "call_api",
      "timestamp": 100,
      "metadata": { "endpoint": "/weather" }
    },
    {
      "name": "format_response",
      "timestamp": 145,
      "metadata": { "format": "json" }
    }
  ]
}
```

#### Example

```bash
curl -X POST https://api.agnost.ai/api/v1/capture-event \
  -H "Content-Type: application/json" \
  -H "X-Org-Id: your-org-id" \
  -d '{
    "session_id": "sess_12345",
    "primitive_type": "tool",
    "primitive_name": "weather_lookup",
    "latency": 150,
    "success": true,
    "args": "{\"city\": \"New York\", \"units\": \"fahrenheit\"}",
    "result": "{\"temperature\": 72, \"conditions\": \"sunny\"}",
    "metadata": {
      "model": "gpt-4",
      "tokens_used": "42",
      "cache_hit": "false"
    }
  }'
```

---

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid request body or missing required fields |
| 401 | Unauthorized - Missing or invalid X-Org-Id header |
| 500 | Internal Server Error |

### Error Response

```json
{
  "error": "Error message description"
}
```

---

## Code Examples

### Python (requests)

```python
import requests
import json

BASE_URL = "https://api.agnost.ai/api/v1"
ORG_ID = "your-org-id"

headers = {
    "Content-Type": "application/json",
    "X-Org-Id": ORG_ID
}

# Create session
requests.post(
    f"{BASE_URL}/capture-session",
    headers=headers,
    json={
        "session_id": "sess_123",
        "client_config": "my-app",
        "user_data": {"user_id": "user_456"}
    }
)

# Capture event
response = requests.post(
    f"{BASE_URL}/capture-event",
    headers=headers,
    json={
        "session_id": "sess_123",
        "primitive_type": "tool",
        "primitive_name": "search",
        "latency": 200,
        "success": True,
        "args": json.dumps({"query": "weather NYC"}),
        "result": json.dumps({"answer": "72°F and sunny"})
    }
)
```

### TypeScript (fetch)

```typescript
const BASE_URL = "https://api.agnost.ai/api/v1";
const ORG_ID = "your-org-id";

const headers = {
  "Content-Type": "application/json",
  "X-Org-Id": ORG_ID
};

// Create session
await fetch(`${BASE_URL}/capture-session`, {
  method: "POST",
  headers,
  body: JSON.stringify({
    session_id: "sess_123",
    client_config: "my-app",
    user_data: { user_id: "user_456" }
  })
});

// Capture event
await fetch(`${BASE_URL}/capture-event`, {
  method: "POST",
  headers,
  body: JSON.stringify({
    session_id: "sess_123",
    primitive_type: "tool",
    primitive_name: "search",
    latency: 200,
    success: true,
    args: JSON.stringify({ query: "weather NYC" }),
    result: JSON.stringify({ answer: "72°F and sunny" })
  })
});
```

---

## Best Practices

1. **Create session first** - Always call `/capture-session` before `/capture-event`
2. **Use consistent session IDs** - Group related events with the same session ID
3. **JSON-encode args/result** - The `args` and `result` fields must be JSON strings
4. **Include metadata** - Add context like model name, token counts, etc.
5. **Handle retries** - Implement exponential backoff for transient failures
