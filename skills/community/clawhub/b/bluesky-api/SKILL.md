---
name: bluesky
version: "1.0.3"
description: "Read, search, post, and monitor Bluesky (AT Protocol) accounts"
metadata: { "openclaw": { "emoji": "🦋" } }
allowed-tools: ["exec", "web_fetch"]
required-binaries: ["curl", "jq"]
---

# Bluesky Skill

Interact with Bluesky via the AT Protocol API. Supports public reads, search, authenticated posting, and profile monitoring.

## Configuration

Credentials can come from openclaw config or environment variables:

| Source | Handle | App Password |
|--------|--------|--------------|
| Config | `channels.bluesky.handle` | `channels.bluesky.appPassword` |
| Env var | `BSKY_HANDLE` | `BSKY_APP_PASSWORD` |

App passwords are created at: https://bsky.app/settings/app-passwords

**Never use a main account password. Always use an app password.**

---

## 1. Read — Fetch Recent Posts from a Profile

**No auth required.** Uses the public API.

### API Endpoint

```
GET https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=<handle>&limit=<n>
```

- `actor` — Bluesky handle (e.g. `alice.bsky.social`) or DID
- `limit` — number of posts to return (1–100, default 50)

### curl Example

```bash
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=alice.bsky.social&limit=5" | jq '.feed[] | {text: .post.record.text, createdAt: .post.record.createdAt, uri: .post.uri}'
```

### Helper Script

```bash
./scripts/bsky-read.sh alice.bsky.social 5
```

### Response Structure

The response JSON has a `feed` array. Each entry contains:
- `.post.record.text` — the post text
- `.post.record.createdAt` — ISO 8601 timestamp
- `.post.uri` — AT URI of the post
- `.post.author.handle` — author handle
- `.post.author.displayName` — author display name
- `.post.likeCount`, `.post.repostCount`, `.post.replyCount` — engagement counts

---

## 2. Search — Find Posts by Keyword

**No auth required.** Uses the public API.

### API Endpoint

```
GET https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=<query>&limit=<n>
```

- `q` — search query (keywords, hashtags, phrases)
- `limit` — number of results (1–100, default 25)

### curl Example

```bash
curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=openclaw&limit=10" | jq '.posts[] | {text: .record.text, author: .author.handle, createdAt: .record.createdAt}'
```

### Helper Script

```bash
./scripts/bsky-search.sh "openclaw" 10
```

### Response Structure

The response JSON has a `posts` array. Each entry contains:
- `.record.text` — the post text
- `.record.createdAt` — ISO 8601 timestamp
- `.author.handle` — author handle
- `.author.displayName` — author display name
- `.uri` — AT URI of the post

---

## 3. Post — Create a New Post

**Requires auth.** Uses app password authentication.

### Step 1: Authenticate

```
POST https://bsky.social/xrpc/com.atproto.server.createSession
Content-Type: application/json

{"identifier": "<handle>", "password": "<app_password>"}
```

This returns a session with `accessJwt` and `did`.

#### curl Example

```bash
# Always use env vars — never interpolate credentials directly into shell strings
SESSION=$(curl -s -X POST "https://bsky.social/xrpc/com.atproto.server.createSession" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg h "$BSKY_HANDLE" --arg p "$BSKY_APP_PASSWORD" '{identifier: $h, password: $p}')")

ACCESS_TOKEN=$(echo "$SESSION" | jq -r '.accessJwt')
DID=$(echo "$SESSION" | jq -r '.did')
```

### Step 2: Create the Post

```
POST https://bsky.social/xrpc/com.atproto.repo.createRecord
Authorization: Bearer <accessJwt>
Content-Type: application/json

{
  "repo": "<did>",
  "collection": "app.bsky.feed.post",
  "record": {
    "$type": "app.bsky.feed.post",
    "text": "<post text>",
    "createdAt": "<ISO 8601 timestamp>"
  }
}
```

#### curl Example

```bash
curl -s -X POST "https://bsky.social/xrpc/com.atproto.repo.createRecord" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"repo\": \"${DID}\",
    \"collection\": \"app.bsky.feed.post\",
    \"record\": {
      \"\$type\": \"app.bsky.feed.post\",
      \"text\": \"Hello from OpenClaw!\",
      \"createdAt\": \"$(date -u +%Y-%m-%dT%H:%M:%S.000Z)\"
    }
  }"
```

### Helper Script

```bash
# Pass app password via env var — never as a CLI argument (visible in ps/shell history)
BSKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx ./scripts/bsky-post.sh alice.bsky.social "Hello from OpenClaw!"
```

### Post Length Limit

Bluesky posts have a 300-character limit (grapheme count). Check length before posting.

---

## 4. Monitor — Check for New Posts Since Last Check

Use the read endpoint with a timestamp comparison to detect new posts. This is useful for heartbeat monitoring.

### Approach

1. Fetch recent posts from the target profile.
2. Compare `.post.record.createdAt` against the last-known timestamp.
3. Any post with a `createdAt` newer than the stored timestamp is new.

### curl Example

```bash
# Fetch the 10 most recent posts
FEED=$(curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=alice.bsky.social&limit=10")

# Filter posts newer than a given timestamp
SINCE="2026-03-24T00:00:00.000Z"
echo "$FEED" | jq --arg since "$SINCE" '.feed[] | select(.post.record.createdAt > $since) | {text: .post.record.text, createdAt: .post.record.createdAt}'
```

### Monitoring Loop Pattern

For heartbeat use, store the latest seen timestamp and compare on each check:

```bash
# Use a user-owned state dir, not world-readable /tmp
LAST_SEEN_FILE="${XDG_STATE_HOME:-$HOME/.local/state}/bsky-monitor-${HANDLE}.txt"
mkdir -p "$(dirname "$LAST_SEEN_FILE")"
HANDLE="alice.bsky.social"

# Read last seen timestamp (or default to 24h ago)
if [ -f "$LAST_SEEN_FILE" ]; then
  SINCE=$(cat "$LAST_SEEN_FILE")
else
  SINCE=$(date -u -v-24H +%Y-%m-%dT%H:%M:%S.000Z 2>/dev/null || date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%S.000Z)
fi

FEED=$(curl -s "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=${HANDLE}&limit=20")
NEW_POSTS=$(echo "$FEED" | jq --arg since "$SINCE" '[.feed[] | select(.post.record.createdAt > $since)]')
COUNT=$(echo "$NEW_POSTS" | jq 'length')

if [ "$COUNT" -gt 0 ]; then
  echo "Found $COUNT new post(s) from $HANDLE since $SINCE"
  echo "$NEW_POSTS" | jq '.[] | {text: .post.record.text, createdAt: .post.record.createdAt}'
  # Update last seen to the most recent post timestamp
  echo "$NEW_POSTS" | jq -r '.[0].post.record.createdAt' > "$LAST_SEEN_FILE"
else
  echo "No new posts from $HANDLE since $SINCE"
fi
```

---

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 200 | Success | Parse response |
| 400 | Bad request | Check parameters |
| 401 | Unauthorized | Re-authenticate (token may be expired) |
| 404 | Not found | Check handle/DID exists |
| 429 | Rate limited | Back off and retry after delay |

### Auth Token Expiry

Access tokens expire. If you get a 401, re-authenticate by calling `createSession` again. Do not cache tokens for more than a few minutes.

---

## Quick Reference

| Operation | Auth? | Script |
|-----------|-------|--------|
| Read profile feed | No | `./scripts/bsky-read.sh <handle> [limit]` |
| Search posts | No | `./scripts/bsky-search.sh <query> [limit]` |
| Create post | Yes | `./scripts/bsky-post.sh <handle> <app_password> <text>` |
| Monitor new posts | No | Use read + timestamp filter (see section 4) |
