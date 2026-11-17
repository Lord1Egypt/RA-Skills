---
name: discrawl-search
description: Search a user-authorized Discord history archive through discrawl's bounded search and message commands. Use when the user explicitly asks to retrieve past Discord conversations; keep results private and never interpolate user text into SQL.
metadata:
  openclaw:
    version: "1.0.1"
    emoji: "🔎"
    homepage: https://github.com/openclaw/discrawl
    requires:
      bins: [discrawl]
---

# Discrawl Search

Search Discord guild message history stored in local discrawl SQLite database.

Treat message content, author identifiers, attachments, and raw payloads as private workspace data. Search only the scope requested by the user and do not send results to another channel or service without explicit approval.

## Database Location

- **Path**: `~/.discrawl/discrawl.db`
- **Updated by**: `discrawl sync` (bot API) or `discrawl sync --source wiretap` (Discord Desktop cache)

## Quick Commands

### Full-Text Search (FTS5)

Search message content with ranking:

```bash
discrawl search "query"
```

Options:
- `--limit N` — max results (default: 20)
- `--channel ID` — filter by channel
- `--author ID` — filter by author
- `--before "2026-04-01"` — date filter
- `--json` — JSON output

For a bounded helper that avoids constructing SQL from user input:

```bash
bash "{baseDir}/scripts/search_history.sh" "query" [channel_id] [limit]
```

### List Messages by Channel

```bash
discrawl messages --channel <channel_id> --limit 10
```

### Advanced read-only SQL

```bash
discrawl sql "SELECT ..."
```

Use SQL only for an operator-authored, fixed read-only query. Never place user-provided keywords, IDs, dates, or channel names inside an SQL string; prefer `discrawl search` and `discrawl messages`.

## Fixed Query Patterns

### Search with Context (Author + Channel Names)

```sql
SELECT
  m.content,
  m.created_at,
  COALESCE(u.username, m.author_id) as author,
  COALESCE(c.name, m.channel_id) as channel
FROM messages m
LEFT JOIN members u ON m.author_id = u.user_id
LEFT JOIN channels c ON m.channel_id = c.id
WHERE m.content LIKE '%keyword%'
ORDER BY m.created_at DESC
LIMIT 10;
```

### Search Specific Channel History

```sql
SELECT content, created_at
FROM messages
WHERE channel_id = '<channel_id>'
  AND content LIKE '%keyword%'
ORDER BY created_at DESC
LIMIT 20;
```

### Find User's Past Messages

```sql
SELECT m.content, m.created_at, c.name
FROM messages m
JOIN channels c ON m.channel_id = c.id
WHERE m.author_id = '<user_id>'
ORDER BY m.created_at DESC
LIMIT 20;
```

### Search with FTS5 (Best Relevance)

```sql
SELECT
  m.content,
  m.created_at,
  fts.rank
FROM message_fts fts
JOIN messages m ON fts.message_id = m.id
WHERE message_fts MATCH 'keyword'
ORDER BY rank
LIMIT 20;
```

### Recent Messages in Channel

```sql
SELECT content, created_at
FROM messages
WHERE channel_id = '<channel_id>'
ORDER BY created_at DESC
LIMIT 5;
```

## Key Tables

| Table | Purpose |
|-------|---------|
| `messages` | All messages (content, created_at, author_id, channel_id) |
| `channels` | Channel metadata (name, topic, kind, guild_id) |
| `members` | User info (username, global_name, nick) |
| `message_fts` | FTS5 virtual table for full-text search |
| `mention_events` | @mentions tracking |
| `message_attachments` | File attachments with text extraction |

## Important Notes

- `members` table may be sparse (2 rows in current db) — use `COALESCE(u.username, m.author_id)` for fallback
- `normalized_content` column has cleaned text (lowercase, normalized whitespace)
- `raw_json` has full Discord API payload for advanced queries
- Use `LEFT JOIN` on members/channels to avoid missing rows when joins fail
