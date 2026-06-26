# MemOS Cloud Sync API Reference

## API Endpoints

### GET /api/memo — Pull Memory

Fetch paginated memory entries from cloud.

**Request**:

```
POST /api/memo
Content-Type: application/json
Authorization: Bearer <token>
```

**Body** (optional filter):

```json
{
  "and": [
    {"create_time": {"gte": "2026-04-29 10:00:00"}}
  ]
}
```

**Response**:

```json
{
  "memo": [
    {
      "id": 1234,
      "content": "memory content...",
      "create_time": "2026-04-29T10:30:00+08:00"
    }
  ]
}
```

**Pagination**: Not returned explicitly — use `filter` with `create_time.gte` cursor to paginate.

### POST /api/memo — Push Memory

Add new memory entries to cloud.

**Request**:

```
POST /api/memo
Content-Type: application/json
Authorization: Bearer <token>
```

**Push Multiple**:

```json
[
  {
    "content": "# memory content\nkey facts...",
    "created_ts": 1714350000
  }
]
```

**Response**: Returns created memo objects.

## Sync State Files

### `.sync-cloud-state.json` (Pull State)

Tracks last successful pull timestamp.

```json
{
  "last_pull": "2026-04-30 10:00:00"
}
```

### `.sync-push-state.json` (Push State)

Tracks SHA256 hashes per file for incremental push.

```json
{
  "memory/2026-04-29.md": "sha256hash...",
  "memory/2026-04-30.md": "sha256hash..."
}
```

## Sync Flow Details

### Pull (Cloud → MD)

1. Read `last_pull` from state file
2. Request `create_time >= last_pull` from cloud
3. Append new entries to `memory/memos-cloud-*.md`
4. Update `last_pull` to current time

### Push (MD → Cloud)

1. Calculate SHA256 for each `memory/*.md` file
2. Compare with stored hash in state file
3. Only push files with changed hashes
4. Update state file with new hashes

### Excluded Files

Never pushed to cloud:
- `memos-cloud-*.md` (already in cloud)
- `MEMORY_INDEX.md` (generated locally)
- `DREAMS.md` (transient analysis)
- `.sync-*.json` (internal state)

## Error Handling

- HTTP 401: Token expired — renew and retry
- HTTP 429: Rate limited — backoff and retry
- Network error: Log and skip, retry next cycle
- Partial failure: Continue with remaining items

## Security

- Token stored in `openclaw.json` or `.env`, never in memory files
- SHA256 content verification before push
- No sensitive data (hashed values) pushed to cloud
