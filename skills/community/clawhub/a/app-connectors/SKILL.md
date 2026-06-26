---
name: app-connectors
description: Connect your AI agent to 1000+ apps — discover tools, manage OAuth connections, execute actions, and provide a self-service connector dashboard.
version: 5.0.1
---

# App Connectors — Connect Your Agent to 1000+ Apps

Connect your AI agent to Gmail, Slack, GitHub, Notion, Google Calendar, LinkedIn, HubSpot, Stripe, and 1000+ more apps via Composio OAuth.

## Setup

On first use, check credentials:

```bash
# Check environment variables
[ -n "$COMPOSIO_API_KEY" ] && echo "✅ API key" || echo "⏳ Not set"
```

**Required:**
- `COMPOSIO_API_KEY` — Project-scoped API key from Composio

If not in env, check the framework's secrets provider (vault, secrets.json, .env). If missing, stop and report to the operator.

## API Reference

Base URL: `https://backend.composio.dev/api`
Auth header: `x-api-key: $COMPOSIO_API_KEY`

### List Connected Apps

Use the v1 REST API to get all active connections for the current entity:

```bash
curl -s "https://backend.composio.dev/api/v1/connectedAccounts?user_uuid=default&showActiveOnly=true" \
  -H "x-api-key: $COMPOSIO_API_KEY"
```

Returns `{ "items": [...] }` — each item has `appName`, `status`, `id`.

### Discover Tools (COMPOSIO_SEARCH_TOOLS)

Find the right tool for a task. Returns matching tools, schemas, connection status, and execution plan.

```bash
curl -s -X POST "https://backend.composio.dev/api/v3/tools/execute/COMPOSIO_SEARCH_TOOLS" \
  -H "x-api-key: $COMPOSIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "queries": [
        {
          "use_case": "send an email via gmail",
          "known_fields": "recipient_name: John"
        }
      ],
      "session": { "generate_id": true }
    }
  }'
```

**Key fields in response:**
- `primary_tool_slugs` — best matching tools
- `tool_schemas` — input schemas for each tool
- `toolkit_connection_statuses` — whether there's an active connection
- `known_pitfalls` — common mistakes to avoid

**Rules:**
- 1 query = 1 tool action (max 7 queries per call)
- Include the app name in the query when the user specifies one
- Reuse `session.id` from the first response in subsequent calls

### Connect an App (COMPOSIO_MANAGE_CONNECTIONS)

If `has_active_connection` is `false`, or the user wants to connect a new app:

```bash
curl -s -X POST "https://backend.composio.dev/api/v3/tools/execute/COMPOSIO_MANAGE_CONNECTIONS" \
  -H "x-api-key: $COMPOSIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "toolkits": ["gmail"]
    }
  }'
```

**Response statuses:**
- `active` — ready to use, no action needed
- `initiated` — returns `redirect_url` → send to user to complete OAuth
- `failed` — error (often: wrong toolkit slug)

**Common toolkit slugs:** `gmail`, `outlook`, `slack`, `github`, `notion`, `clickup`, `linkedin`, `googlecalendar`, `googledrive`, `googlesheets`, `jira`, `trello`, `hubspot`, `figma`, `discord`, `airtable`, `stripe`, `youtube`, `calendly`, `supabase`, `asana`, `dropbox`, `twitter`

Note: slugs are lowercase, no underscores (e.g. `googlecalendar` not `google_calendar`).

### Execute Tools (COMPOSIO_MULTI_EXECUTE_TOOL)

Only after connection is active:

```bash
curl -s -X POST "https://backend.composio.dev/api/v3/tools/execute/COMPOSIO_MULTI_EXECUTE_TOOL" \
  -H "x-api-key: $COMPOSIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "tools": [
        {
          "tool_slug": "GMAIL_SEND_EMAIL",
          "arguments": {
            "to": "john@example.com",
            "subject": "Hello",
            "body": "Welcome!"
          }
        }
      ],
      "sync_response_to_workbench": false
    }
  }'
```

**Rules:**
- Never invent tool slugs or argument fields — only use what `SEARCH_TOOLS` returned
- Batch independent tools in a single call (max 50)
- Verify connection is active before executing

### Get Full Schemas (COMPOSIO_GET_TOOL_SCHEMAS)

When `SEARCH_TOOLS` returns a `schemaRef` instead of full `input_schema`:

```bash
curl -s -X POST "https://backend.composio.dev/api/v3/tools/execute/COMPOSIO_GET_TOOL_SCHEMAS" \
  -H "x-api-key: $COMPOSIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "tool_slugs": ["GMAIL_SEND_EMAIL"]
    }
  }'
```

## /apps Command

When the user types `/apps`:

1. **List connected apps** using the v1 REST API (`/v1/connectedAccounts?user_uuid=default&showActiveOnly=true`)
2. **Display as a clean list** — one line per app, `🟢` prefix, human-readable name:
   ```
   🟢 Gmail
   🟢 LinkedIn
   🟢 ClickUp
   🟢 Notion
   ```
   If none connected: "No apps connected yet."
3. **End with a prompt**: "To connect a new app, type its name."
4. When the user types an app name, call `COMPOSIO_MANAGE_CONNECTIONS` with the matching slug, get the `redirect_url`, and send it as a clickable link.

**Display name mapping** (slug → display):
`gmail` → Gmail, `outlook` → Outlook, `googlecalendar` → Google Calendar, `googledrive` → Google Drive, `googlesheets` → Google Sheets, `linkedin` → LinkedIn, `notion` → Notion, `clickup` → ClickUp, `slack` → Slack, `github` → GitHub, `jira` → Jira, `trello` → Trello, `hubspot` → HubSpot, `figma` → Figma, `discord` → Discord, `airtable` → Airtable, `stripe` → Stripe, `youtube` → YouTube, `calendly` → Calendly, `supabase` → Supabase, `asana` → Asana, `dropbox` → Dropbox, `twitter` → Twitter/X, `shopify` → Shopify

For unknown slugs, capitalize the first letter.

## Agent Commands

| User says | What to do |
|-----------|------------|
| `/apps` | List connected apps → prompt to connect |
| "Connect Slack" | `MANAGE_CONNECTIONS` with `["slack"]` → send OAuth link |
| "Send an email to X" | `SEARCH_TOOLS` → check connection → `MULTI_EXECUTE_TOOL` |
| "Disconnect Slack" | Use `MANAGE_CONNECTIONS` |

## References

- [Composio Docs](https://docs.composio.dev)
