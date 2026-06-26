# Dashform MCP Tools Reference

Technical reference for Dashform MCP (Model Context Protocol) tools.

## MCP Server

**Endpoint:** `https://getaiform.com/api/mcp`
**Protocol:** HTTP-based MCP
**Server Name:** Dashform MCP API
**Version:** 1.0.0

## Prerequisites

- Development server running (`pnpm dev`)
- User session token from https://getaiform.com (for credential caching)

**Note:** Organization ID and User ID are automatically retrieved using the `get_user_info` tool with your session token.

## Available Tools

### get_user_info

Retrieves user information from a session token for credential caching.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sessionToken` | string | Yes | The `better-auth.session_token` cookie value from browser |

**Returns:**

```json
{
  "userId": "string",
  "organizationId": "string",
  "userName": "string",
  "userEmail": "string"
}
```

**Errors:**

- `"Unauthorized: Invalid or expired session token"` - Invalid session
- `"Error getting user info: <message>"` - Specific error

**Usage:**

This tool is used by the credential caching system to automatically retrieve user credentials. Users provide their session token from the browser, and this tool returns their userId and organizationId for subsequent form operations.

---

### create_form

Creates a new form with full configuration support.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organizationId` | string | Yes | Organization ID |
| `userId` | string | Yes | User ID |
| `name` | string | Yes | Form name (1-255 chars) |
| `type` | enum | No | `"structured"` (default) or `"dynamic"` |
| `description` | string | No | Form description |
| `tone` | string | No | Form tone |
| `welcomeScreen` | object | No | Welcome screen config |
| `endScreen` | object | No | End screen config |
| `endScreenEnabled` | boolean | No | Enable end screen |
| `endings` | array | No | Quiz endings |
| `questions` | array | No | Question list |
| `snippets` | array | No | AI reference snippets |
| `maxFollowUpQuestions` | number | No | Max follow-ups (0-10) |
| `theme` | object | No | Visual theme |
| `branding` | object | No | Branding settings |
| `backgrounds` | array | No | Backgrounds (max 10) |

**Returns:**

```json
{
  "success": true,
  "formId": "string",
  "name": "string",
  "type": "structured" | "dynamic",
  "description": "string | null",
  "tone": "string | null",
  "questionsCount": number,
  "createdAt": "ISO8601",
  "shareUrl": "string",
  "editUrl": "string"
}
```

**Errors:**

- `"Failed to create form."` - Database error
- `"Error creating form: <message>"` - Specific error

---

### create_reply

Creates a reply/response for a form.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `formId` | string | Yes | Form ID |
| `organizationId` | string | Yes | Organization ID |
| `respondentName` | string | No | Respondent name |
| `respondentEmail` | string | No | Respondent email |
| `respondentEmotion` | enum | No | `"neutral"` (default), `"positive"`, `"negative"` |
| `data` | object | No | Form data (key-value pairs) |

**Returns:**

```json
{
  "success": true,
  "replyId": "string",
  "formVersionId": "string",
  "status": "partial",
  "respondentName": "string | null",
  "respondentEmail": "string | null",
  "respondentEmotion": "neutral" | "positive" | "negative",
  "data": {},
  "createdAt": "ISO8601"
}
```

**Errors:**

- `"Form not found or does not belong to the specified organization."` - Invalid form/org
- `"No version found for this form."` - No published version
- `"Failed to create reply."` - Database error
- `"Error creating reply: <message>"` - Specific error

---

## Form Types

| Type | Description |
|------|-------------|
| `structured` | Traditional form with fixed questions (default) |
| `dynamic` | AI-powered conversational form |

## Schema Details

For complete schema documentation including question types, screens, themes, and branching logic, see [SCHEMA.md](./SCHEMA.md).

## Testing

Test MCP server directly:

```bash
curl -X POST https://getaiform.com/api/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "create_form",
      "arguments": {
        "organizationId": "org_123",
        "userId": "user_123",
        "name": "Test Form",
        "type": "structured"
      }
    },
    "id": 1
  }'
```

**Required Headers:**
- `Content-Type: application/json` - Request content type
- `Accept: application/json, text/event-stream` - Accept both JSON and SSE responses

## Additional Resources

- **Complete Examples**: See `examples/` directory
- **Schema Reference**: See `SCHEMA.md`
- **MCP Specification**: https://modelcontextprotocol.io
