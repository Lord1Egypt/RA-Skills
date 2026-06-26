# BookStack Skill for Claude Code

Manage your [BookStack](https://www.bookstackapp.com/) wiki directly from Claude Code. Create, read, update, and delete books, chapters, pages, and shelves — with full-text search across all content.

## Installation

```bash
claude skill install f-liva/skill-bookstack
```

## Configuration

Create an API token in BookStack: **Profile > API Tokens > Create Token** (the user's role must have "Access System API" permission).

Add credentials to `~/.clawdbot/clawdbot.json`:

```json
{
  "skills": {
    "entries": {
      "bookstack": {
        "env": {
          "BOOKSTACK_URL": "https://your-bookstack.example.com",
          "BOOKSTACK_TOKEN_ID": "your-token-id",
          "BOOKSTACK_TOKEN_SECRET": "your-token-secret"
        }
      }
    }
  }
}
```

## What it does

Once installed, Claude Code can:

- **Search** your knowledge base — "find the page about deployment"
- **Read** page content in HTML or Markdown
- **Create** new pages, chapters, and books
- **Update** existing documentation
- **Organize** content across books, chapters, and shelves

Just ask naturally — "update the wiki page about server setup", "search the docs for nginx config", "create a new page in the DevOps book".

## Cloudflare note

The script includes a `User-Agent` header to work with BookStack instances behind Cloudflare. Without it, requests get blocked with HTTP 403.

## License

MIT
