# Discrawl Database Schema Reference

## Core Tables

### messages
| Column | Type | Description |
|--------|------|-------------|
| id | TEXT PK | Discord message ID |
| guild_id | TEXT | Guild ID |
| channel_id | TEXT | Channel ID |
| author_id | TEXT | Author user ID |
| message_type | INTEGER | Discord message type |
| created_at | TEXT | ISO timestamp |
| edited_at | TEXT | Edit timestamp |
| deleted_at | TEXT | Deletion timestamp |
| content | TEXT | Raw message content |
| normalized_content | TEXT | Lowercase, normalized whitespace |
| reply_to_message_id | TEXT | Reply reference |
| pinned | INTEGER | Pinned flag |
| has_attachments | INTEGER | Has attachments flag |
| raw_json | TEXT | Full Discord API payload |
| updated_at | TEXT | Last sync timestamp |

### channels
| Column | Type | Description |
|--------|------|-------------|
| id | TEXT PK | Channel ID |
| guild_id | TEXT | Guild ID |
| parent_id | TEXT | Parent category ID |
| kind | TEXT | Channel type (text, voice, etc) |
| name | TEXT | Channel name |
| topic | TEXT | Channel topic |
| position | INTEGER | Sort position |
| is_nsfw | INTEGER | NSFW flag |
| is_archived | INTEGER | Archived flag |
| is_locked | INTEGER | Locked flag |
| is_private_thread | INTEGER | Private thread flag |

### members
| Column | Type | Description |
|--------|------|-------------|
| guild_id | TEXT | Guild ID |
| user_id | TEXT PK | User ID |
| username | TEXT | Username |
| global_name | TEXT | Global display name |
| display_name | TEXT | Display name |
| nick | TEXT | Guild nickname |
| bot | INTEGER | Bot flag |
| role_ids_json | TEXT | JSON array of role IDs |

## FTS5 Virtual Tables

### message_fts
Columns: message_id, guild_id, channel_id, author_id, author_name, channel_name, content

### member_fts
Columns: member_key, guild_id, user_id, username, display_name, profile_text

## Useful SQL Patterns

### Count messages per channel
```sql
SELECT c.name, COUNT(*) as count
FROM messages m
JOIN channels c ON m.channel_id = c.id
GROUP BY c.id
ORDER BY count DESC;
```

### Messages in date range
```sql
SELECT content, created_at
FROM messages
WHERE created_at >= '2026-04-01'
  AND created_at < '2026-04-02'
ORDER BY created_at;
```

### Search with FTS ranking
```sql
SELECT m.content, m.created_at, rank
FROM message_fts fts
JOIN messages m ON fts.message_id = m.id
WHERE message_fts MATCH 'OpenClaw MCP'
ORDER BY rank
LIMIT 20;
```
