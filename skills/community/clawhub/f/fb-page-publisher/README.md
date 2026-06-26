# Facebook Page Publisher - OpenClaw MCP Skill

Manage your Facebook Page directly from an AI agent. Create posts, upload photos, schedule content, view analytics, and moderate comments -- all through natural language.

## Features

| Tool | Description |
|------|-------------|
| `create_post` | Publish a text post immediately |
| `upload_photo_post` | Upload a photo with optional caption |
| `schedule_post` | Schedule a post for future publication |
| `get_page_insights` | View page engagement metrics |
| `get_recent_posts` | List recent posts with engagement stats |
| `delete_post` | Remove a post from the page |
| `get_post_comments` | Read comments on a post |
| `reply_to_comment` | Reply to a comment as the Page |

## Quick Start

### 1. Install dependencies

```bash
cd fb-page-publisher
uv sync
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your FB_PAGE_ID and FB_ACCESS_TOKEN
```

### 3. Get your Facebook credentials

1. Go to [developers.facebook.com](https://developers.facebook.com) and create a Business app
2. Open [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
3. Select your app, generate a token with permissions:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_manage_engagement`
4. Call `GET /me/accounts` to get your Page ID and Page Access Token
5. Extend to a long-lived token (see blueprint docs for details)

### 4. Run the server

```bash
uv run src/server.py
```

### 5. Test with MCP Inspector

```bash
npx @modelcontextprotocol/inspector uv run src/server.py
```

## Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fb-page-publisher": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/fb-page-publisher",
        "run",
        "src/server.py"
      ],
      "env": {
        "FB_PAGE_ID": "your_page_id",
        "FB_ACCESS_TOKEN": "your_access_token"
      }
    }
  }
}
```

## Example Prompts

- "Post 'Happy Monday!' to my Facebook page"
- "Upload this image to my FB page with caption 'New product launch'"
- "Schedule a post for tomorrow at 9 AM"
- "Show me my page insights for the last week"
- "Show my last 5 Facebook posts"
- "Reply 'Thank you!' to the latest comment on my recent post"

## Publishing to ClawHub

```bash
clawhub login
clawhub validate .
npx clawhub publish "D:\My_Work\Open-Claw\fb-page-publisher" --slug "fb-page-publisher" --version "1.0.0"
```

## License

MIT
