---
name: ben-mcadams-mcp
description: Connect to Ben McAdams's personal MCP server for his resume, portfolio, and blog notes.
version: 1.0.0
metadata:
  openclaw:
    always: true
    emoji: "🧑‍💻"
    homepage: https://benmcadams.info
---

# Ben McAdams MCP

Ben McAdams's personal site (benmcadams.info) runs a remote MCP server with
structured access to his resume, portfolio, and blog notes. No install or
credentials needed — it's a public HTTP endpoint.

## Setup

Add to your MCP client config:

```json
{
  "mcpServers": {
    "ben-mcadams": {
      "url": "https://benmcadams.info/api/mcp"
    }
  }
}
```

For stdio-only clients:

```bash
npx -y mcp-remote https://benmcadams.info/api/mcp
```

## Tools

- `about` — Quick summary of the site and available tools.
- `get_resume` — Full JSON Resume of Ben McAdams.
- `download_resume` — Get links to download Ben's resume as PDF or markdown.
- `list_notes` — List blog posts (metadata only).
- `get_post` — Get the full markdown of a post by slug.
- `search_notes` — Keyword search over post bodies.
- `get_portfolio` — Portfolio of agent, DX, and product work.
