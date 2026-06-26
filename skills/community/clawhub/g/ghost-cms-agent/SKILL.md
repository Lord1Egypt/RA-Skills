---
name: ghost-cms
description: Manage Ghost CMS content via the REST API. Create and publish posts, manage tags, and fetch site analytics. Supports both the Content API (public data) and Admin API (authenticated management).
metadata:
  {
    "openclaw":
      {
        "emoji": "👻",
        "requires":
          {
            "env": ["GHOST_URL", "GHOST_ADMIN_API_KEY"],
          },
      },
  }
---

# Ghost CMS

Manage Ghost CMS content via its REST API. Works with self-hosted and Ghost Pro sites.

## Configuration

```bash
# Your Ghost site URL
export GHOST_URL="https://example.com"

# Admin API key (from Ghost Admin > Settings > Integrations)
export GHOST_ADMIN_API_KEY="your-admin-api-key"

# Optional: Content API key (for public data)
export GHOST_CONTENT_API_KEY="your-content-api-key"
```

## Get Posts

```bash
bash skills/ghost-cms/scripts/posts.sh [--limit 10] [--page 1] [--status published]
```

Options:
- `--limit` — Number of posts to return (default: 10)
- `--page` — Page number (default: 1)
- `--status` — Filter by status: `published`, `draft`, `scheduled`, `all` (default: published)
- `--format` — Output format: `json` or `table` (default: json)

## Create a New Post

```bash
bash skills/ghost-cms/scripts/new-post.sh \
  --title "My New Post" \
  --content "## Hello World

This is the post content in Markdown." \
  --tags "news,updates" \
  --publish
```

Options:
- `--title` — Post title (required)
- `--content` — Post content in Markdown (required)
- `--excerpt` — Short excerpt/summary (optional)
- `--tags` — Comma-separated tag names (optional, auto-creates)
- `--publish` — Publish immediately (omit to save as draft)
- `--featured` — Mark as featured (optional)

## Manage Tags

```bash
# List all tags
bash skills/ghost-cms/scripts/tags.sh --list

# Create a tag
bash skills/ghost-cms/scripts/tags.sh --create --name "Tutorials" --description "How-to guides" --slug "tutorials"

# Get a tag by slug
bash skills/ghost-cms/scripts/tags.sh --slug "tutorials"
```

## Get Site Stats

```bash
bash skills/ghost-cms/scripts/stats.sh
```

Returns: total posts, total published posts, total draft posts, total members, total paid members, total pageviews (if stats addon is enabled)

## Notes

- Admin API key format: `[id]:[apiKey]` — split on the colon, use the second part as the bearer token
- Tags are created automatically if they don't exist when creating posts
- Ghost uses a `Content-Type: application/json` header for all API calls
- All scripts output JSON by default; use `--format table` for human-readable output where supported
