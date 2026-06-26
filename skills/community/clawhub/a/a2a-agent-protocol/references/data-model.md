# A2A Data Model Reference

> Reference: https://a2a-protocol.org/latest/specification/ Section 4

## Core Objects

### Task

```json
{
  "taskId": "string (required)",
  "sessionId": "string (optional, for multi-turn threading)",
  "contextId": "string (optional, for conversation threading)",
  "status": "TaskStatus (required)",
  "metadata": "object (optional, arbitrary metadata)",
  "artifacts": [
    "Artifact[] (optional, produced during or after task)"
  ],
  "messages": [
    "Message[] (optional, history if retained)"
  ]
}
```

### TaskStatus

```json
{
  "state": "TaskState (required)",
  "message": "string (optional, human-readable status message)",
  "timestamp": "ISO-8601 datetime (required)"
}
```

### TaskState

| State | Meaning |
|-------|---------|
| `submitted` | Task received, not yet processing |
| `working` | Task is actively processing |
| `completed` | Task finished successfully |
| `failed` | Task encountered an error |
| `canceled` | Task was cancelled by client |

### Message

```json
{
  "role": "Role (required) — 'user' or 'agent'",
  "parts": [
    "Part[] (required, content blocks)"
  ],
  "messageId": "string (optional)"
}
```

### Role

| Value | Who |
|-------|-----|
| `user` | The initiating human or client agent |
| `agent` | The responding server agent |

### Part

A `Part` is a discriminated union with a `kind` field:

```json
// TextPart
{ "kind": "text", "text": "string" }

// DataPart
{ "kind": "data", "data": object }

// FilePart
{ "kind": "file", "file": { "name": "string", "mimeType": "string", "bytes": "base64", "url": "https://..." } }
```

### Artifact

```json
{
  "artifactId": "string",
  "name": "string (optional)",
  "description": "string (optional)",
  "parts": [
    "Part[] (required, content blocks)"
  ],
  "metadata": "object (optional)"
}
```

### AgentCard

> Full schema with all optional fields — see `references/agent-card-template.md` for a complete annotated example.

Minimal AgentCard:

```json
{
  "name": "string (required)",
  "description": "string (required)",
  "version": "string (required)",
  "capabilities": {
    "streaming": "SUPPORTED | NOT_SUPPORTED",
    "pushNotifications": "SUPPORTED | NOT_SUPPORTED",
    "agentPrivilege": "boolean",
    "signedAgentCard": "boolean"
  },
  "authentication": {
    "schemes": ["string"],
    "credentials": "required | optional"
  }
}
```

### AgentCapabilities

```json
{
  "streaming": "SUPPORTED | NOT_SUPPORTED | STREAMABLE",
  "pushNotifications": "SUPPORTED | NOT_SUPPORTED",
  "agentPrivilege": "boolean",
  "signedAgentCard": "boolean",
  "dataStreamingSupported": "boolean",
  "supportsAuthenticatedExtendedAgentCard": "boolean"
}
```

### AgentSkill

```json
{
  "id": "string (required)",
  "name": "string (required)",
  "description": "string (required)",
  "tags": ["string[] (optional)"],
  "examples": ["string[] (optional)"]
}
```

## Streaming Events

### TaskStatusUpdateEvent

```json
{
  "kind": "TaskStatusUpdateEvent",
  "taskId": "string",
  "status": "TaskStatus",
  "final": "boolean (true when task reaches terminal state)"
}
```

### TaskArtifactUpdateEvent

```json
{
  "kind": "TaskArtifactUpdateEvent",
  "taskId": "string",
  "artifact": "Artifact",
  "final": "boolean"
}
```

## Push Notification Objects

### PushNotificationConfig

```json
{
  "id": "string",
  "taskId": "string",
  "pushProviderName": "string",
  "pushProviderUrl": "string",
  "authentication": "AuthenticationInfo",
  "payload": {
    "secret": "string (optional)"
  }
}
```

### AuthenticationInfo

```json
{
  "kind": "APIKeyAuthenticationInfo | HTTPBearerAuthenticationInfo | OAuth2AuthenticationInfo",
  "credentials": "string or object"
}
```

## Security Objects

### SecurityScheme ( discriminated union)

| Kind | Auth Type |
|------|-----------|
| `apiKey` | X-API-Key header |
| `httpBearer` | Authorization: Bearer <token> |
| `oauth2` | OAuth 2.0 flow |
| `mutualTLS` | Mutual TLS certificate |
| `openIdConnect` | OIDC token |