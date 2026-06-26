# A2A API Reference

## Overview

A2A (Agent2Agent) is an open standard for AI Agent communication, contributed by Google to the Linux Foundation.

## Endpoints

### Agent Card

**GET** `/.well-known/agent.json`

Returns agent metadata and capabilities.

**Response:**
```json
{
  "name": "Agent Name",
  "description": "Agent description",
  "url": "http://agent-url/a2a",
  "capabilities": {
    "streaming": false,
    "pushNotifications": false
  },
  "skills": [
    {"name": "chat", "description": "Capability description"}
  ],
  "authentication": {
    "schemes": ["Bearer"]
  }
}
```

### JSON-RPC Endpoint

**POST** `/rpc`

All A2A operations use JSON-RPC 2.0 format.

## Methods

### message/send

Send a message to the agent.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "id": "1",
  "params": {
    "message": {
      "role": "user",
      "parts": [
        {"type": "text", "text": "Hello"}
      ]
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "id": "task-xxx",
    "status": "completed",
    "artifacts": [
      {
        "parts": [
          {"type": "text", "text": "Response content"}
        ]
      }
    ]
  },
  "id": "1"
}
```

### task/get

Get task status.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "task/get",
  "id": "2",
  "params": {"id": "task-xxx"}
}
```

### task/list

List tasks.

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "task/list",
  "id": "3",
  "params": {}
}
```

## Task States

| State | Description |
|-------|-------------|
| `pending` | Waiting to be processed |
| `running` | Currently processing |
| `completed` | Finished successfully |
| `failed` | Failed with error |
| `canceled` | Canceled by user |

## Error Codes

| Code | Description |
|------|-------------|
| -32700 | Parse error |
| -32600 | Invalid Request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |

## Authentication

Use Bearer Token in Authorization header:

```http
Authorization: Bearer your-token-here
```

## References

- A2A Specification: https://a2a-protocol.org/latest/specification/
- JSON-RPC 2.0: https://www.jsonrpc.org/specification
- A2A GitHub: https://github.com/a2aproject/A2A