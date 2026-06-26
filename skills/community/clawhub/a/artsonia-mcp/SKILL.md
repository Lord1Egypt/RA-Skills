---
name: artsonia-mcp
description: Access Artsonia student-art portfolios, comments, and fans via MCP. Use when the user asks about a child's artwork, wants to post an art comment, check fans, view portfolios, or manage Artsonia notifications. Triggers on phrases like "show me Emma's latest artwork", "post a comment on that painting", "who are the fans for this student", "invite grandma as a fan", or any request involving student art portfolios on Artsonia. Requires artsonia-mcp installed and the artsonia server registered (see Setup below).
---

# artsonia-mcp

MCP server for Artsonia — natural-language access to student-art portfolios, comments, and fans.

- **npm:** [npmjs.com/package/artsonia-mcp](https://www.npmjs.com/package/artsonia-mcp)
- **Source:** [github.com/chrischall/artsonia-mcp](https://github.com/chrischall/artsonia-mcp)

## Setup

### Option A — npx (recommended)

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "artsonia": {
      "command": "npx",
      "args": ["-y", "artsonia-mcp"],
      "env": {
        "ARTSONIA_USERNAME": "your-email@example.com",
        "ARTSONIA_PASSWORD": "your-password"
      }
    }
  }
}
```

### Option B — from source

```bash
git clone https://github.com/chrischall/artsonia-mcp
cd artsonia-mcp
npm install && npm run build
```

Then add to `.mcp.json`:

```json
{
  "mcpServers": {
    "artsonia": {
      "command": "node",
      "args": ["/path/to/artsonia-mcp/dist/index.js"],
      "env": {
        "ARTSONIA_USERNAME": "your-email@example.com",
        "ARTSONIA_PASSWORD": "your-password"
      }
    }
  }
}
```

Or use a `.env` file in the project directory with `ARTSONIA_USERNAME=<value>` and `ARTSONIA_PASSWORD=<value>`.

## Authentication

Username/password auth using your Artsonia parent/fan account credentials. The server logs in and maintains a session cookie.

## Tools

### Core
| Tool | Description |
|------|-------------|
| `artsonia_healthcheck` | Check connectivity and authentication status |
| `artsonia_list_students` | List all students linked to the account |

### Portfolio & Artwork
| Tool | Description |
|------|-------------|
| `artsonia_get_activity` | Get recent activity feed for a student |
| `artsonia_get_portfolio` | Get a student's art portfolio. Optional `include_details: boolean` (default `false`) fetches each artwork's full detail (title/project/grade/views/…) concurrently and merges it into the rows; omit it for the fast, lean tiles. |
| `artsonia_get_artwork` | Get details for a single artwork |
| `artsonia_download_artwork` | Download a student's artwork images to a local folder. Optional `write_index: boolean` (default `false`) writes an `index.json` manifest into the destination listing the downloaded items (`artwork_id`, `title`, `file`, `grade`, `project`, `date`); the manifest path is returned as `index_file`. |

### Social
| Tool | Description |
|------|-------------|
| `artsonia_list_comments` | List comments on an artwork |
| `artsonia_get_fans` | Get the fan list for a student |
| `artsonia_post_comment` | Post a comment on an artwork |
| `artsonia_invite_fan` | Invite someone to become a fan of a student |
| `artsonia_set_notifications` | Update notification preferences for a student |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ARTSONIA_USERNAME` | Yes | Your Artsonia login email address |
| `ARTSONIA_PASSWORD` | Yes | Your Artsonia account password |
| `ARTSONIA_TRANSPORT` | No | Override transport: `stdio` (default), `sse`, or `fetchproxy` |
| `ARTSONIA_WS_PORT` | No | WebSocket port when using `sse` transport |
