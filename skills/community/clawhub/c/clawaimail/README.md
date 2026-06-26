# ClawAIMail MCP Server

MCP Server for ClawAIMail, letting AI tools (OpenClaw, Claude Code, Cursor) manage email.

## Setup

### Claude Code / Cursor

Add to your MCP config (`~/.claude/mcp.json` or Cursor settings):

```json
{
  "mcpServers": {
    "clawaimail": {
      "command": "node",
      "args": ["/path/to/agent-mail/mcp/index.js"],
      "env": {
        "CLAWAIMAIL_API_KEY": "pb_your_api_key",
        "CLAWAIMAIL_BASE_URL": "https://api.clawaimail.com"
      }
    }
  }
}
```

### OpenClaw

Add to `openclaw.json` tools section or install as a plugin.

## Available Tools

| Tool | Description |
|------|-------------|
| `list_inboxes` | List all email inboxes |
| `create_inbox` | Create a new inbox |
| `send_email` | Send an email |
| `list_messages` | List messages in an inbox |
| `read_email` | Read a specific email |
| `search_emails` | Search emails by keyword |
| `delete_inbox` | Delete an inbox |
| `account_info` | Get account info and usage |
