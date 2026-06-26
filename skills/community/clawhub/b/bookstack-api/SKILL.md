---
name: bookstack
description: "BookStack Wiki & Documentation API integration. Manage your knowledge base programmatically: create, read, update, and delete books, chapters, pages, and shelves. Full-text search across all content. Use this skill whenever the user mentions BookStack, wiki pages, knowledge base, documentation pages, or wants to publish, update, or search content on a BookStack instance -- even if they just say 'update the docs' or 'check the wiki' without naming BookStack explicitly. Also use when syncing or automating documentation workflows between systems."
metadata: {"requiredEnv": ["BOOKSTACK_URL", "BOOKSTACK_TOKEN_ID", "BOOKSTACK_TOKEN_SECRET"]}
---

# BookStack API Skill

Interact with a BookStack wiki through its REST API using the bundled Python script. No external dependencies beyond Python 3 standard library.

## Configuration

Credentials live in `~/.clawdbot/clawdbot.json` under the `bookstack` skill entry:

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

Generate a token from BookStack: Profile > API Tokens > Create Token. The user's role needs the **"Access System API"** permission enabled.

## Usage

All commands follow the pattern:

```
python3 scripts/bookstack.py <command> [args] [options]
```

Pass the env vars from the config above when executing.

### Quick Reference

| Action | Command |
|--------|---------|
| Search | `search "query" [--type page\|book\|chapter]` |
| List pages | `list_pages [--count N]` |
| Read page | `get_page <id> [--content\|--markdown]` |
| Create page | `create_page --book-id <id> --name "Title" --html "<p>content</p>"` |
| Update page | `update_page <id> --html "<p>new content</p>"` |
| Delete page | `delete_page <id>` |

The same CRUD pattern applies to `books`, `chapters`, and `shelves`. For the full command list with all flags and options, see [references/api-commands.md](references/api-commands.md).

## Important Notes

- **Cloudflare protection**: The script sends a `User-Agent` header because BookStack instances behind Cloudflare reject requests without one (HTTP 403). If you get a 403, this is likely why.
- **Content formats**: Pages accept HTML by default. Use `--markdown` for Markdown input. When reading, `get_page --content` returns HTML, `--markdown` returns Markdown.
- **Large HTML updates**: For big page updates, prepare the HTML in a temp file and read it into the API call programmatically, rather than passing it inline on the command line.
