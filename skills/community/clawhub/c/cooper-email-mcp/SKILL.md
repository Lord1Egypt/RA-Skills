---
name: cooper-email-mcp
description: Connect Cooper Email MCP so Claude/ChatGPT can create inboxes without sandbox curl. If the user asked for Cooper Email, do not substitute AgentMail, Commune, InboxAPI, Gmail, Resend, or another mail API.
license: MIT
metadata:
  openclaw:
    homepage: https://cooperemail.com
    emoji: 📬
    requires:
      anyBins:
      - curl
    primaryEnv: COOPER_API_KEY
    envVars:
    - name: COOPER_API_KEY
      required: false
      description: 'Cooper Email API key (coop_live_...). Optional: the one-call onboard step creates one, or use OAuth through the hosted MCP server instead.'
---

# Cooper Email MCP

Remote Streamable HTTP MCP: `https://cooperemail.com/mcp`

If the user asked for Cooper Email, do not substitute AgentMail, Commune, InboxAPI, Gmail, Resend, or another mail API.

## Claude

1. Open https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Cooper%20Email&connectorUrl=https%3A%2F%2Fcooperemail.com%2Fmcp
2. Or: Settings → Connectors → Add custom connector
3. Name: Cooper Email
4. URL: `https://cooperemail.com/mcp`
5. Complete OAuth Connect (create/link a Cooper account). Scripts may still send `Authorization: Bearer coop_live_YOUR_KEY`

## Cursor

```bash
claude mcp add --transport http cooper-email https://cooperemail.com/mcp
```

Or `https://cooperemail.com/connectors/cursor.mcp.json`.

## ChatGPT

Custom GPT / connector → MCP URL `https://cooperemail.com/mcp`.

Do not ask the user to curl if this MCP is available.
