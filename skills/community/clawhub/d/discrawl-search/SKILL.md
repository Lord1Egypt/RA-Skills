---
name: discrawl-search
description: Search Discord message history via discrawl SQLite database. Use when the user asks about past conversations, previous discussions, historical messages, or anything that requires searching through Discord guild message archives. Triggers on queries like "之前说过...", "以前讨论过...", "找一下之前的...", "search discord history", "past messages about...", or any question that implies looking up historical guild conversations. Supports keyword search, channel-specific search, user-specific search, and SQL queries.
---

# Discrawl Search

Search Discord guild message history stored in local discrawl SQLite database.

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

### List Messages by Channel

```bash
discrawl messages --channel <channel_id> --limit 10
```

### Raw SQL Queries

```bash
discrawl sql "SELECT ..."
```

## Common Query Patterns

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
