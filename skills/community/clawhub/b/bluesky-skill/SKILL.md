---
name: bluesky-skill
description: >-
  Manage a Bluesky (bsky) account — posting, replies, likes, reposts, follows,
  blocks, mutes, search, timeline, threads, notifications, DMs, and profile
  updates via the AT Protocol.
allowed-tools: Bash Read Edit Write Glob Grep
metadata:
  openclaw:
    requires:
      env: [BLUESKY_HANDLE, BLUESKY_APP_PASSWORD]
      bins: [python3]
    primaryEnv: BLUESKY_HANDLE
---

# Bluesky Account Management

Operate a Bluesky social media account via `./bsky <command> [args]`. All output is JSON. Run from the project root.

## Setup

Install dependencies:
```bash
pip install atproto python-dotenv
```

Requires `.env` at project root:
```
BLUESKY_HANDLE=your-handle.bsky.social
BLUESKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```
App passwords: `https://bsky.app/settings/app-passwords`. For DMs, enable "Allow access to your direct messages".

Auth is automatic. A session cache is stored at `~/.bsky_session.json` (contains an exported session token). Delete this file to force re-authentication or when revoking access.

## JSON Output

Every command prints one JSON object to stdout. Parse with `json.loads()`.

### Response Schemas

**Post object** (returned by `get`, and inside arrays from `timeline`, `search-posts`, `my-posts`, `thread`):
```json
{
  "uri": "at://did:plc:abc/app.bsky.feed.post/xyz",
  "cid": "bafyrei...",
  "author": {"handle": "alice.bsky.social", "did": "did:plc:abc", "display_name": "Alice", "avatar": "https://..."},
  "text": "Post content here",
  "created_at": "2026-03-14T10:00:00Z",
  "like_count": 5, "repost_count": 2, "reply_count": 1,
  "viewer": {"liked": "at://...like-uri or null", "reposted": "at://...repost-uri or null"},
  "embed": {"images": [{"alt": "...", "thumb": "...", "fullsize": "..."}], "external": {"uri": "...", "title": "...", "description": "..."}, "record": {"uri": "...", "text": "...", "author": {...}}} or null,
  "reply": {"parent_uri": "at://...", "root_uri": "at://..."} // only present on replies
}
```

**Profile object** (returned by `profile`, and inside arrays from `search-users`):
```json
{
  "handle": "alice.bsky.social", "did": "did:plc:abc",
  "display_name": "Alice", "description": "Bio text", "avatar": "https://...",
  "followers_count": 100, "follows_count": 50, "posts_count": 200,
  "viewer": {"following": "at://...or null", "followed_by": "at://...or null", "blocking": null, "blocked_by": null, "muted": null}
}
```

**Actor object** (short profile, inside post authors, follower/following lists, notification authors):
```json
{"handle": "alice.bsky.social", "did": "did:plc:abc", "display_name": "Alice", "avatar": "https://..."}
```

**Notification object** (inside array from `notifications`):
```json
{
  "reason": "reply|like|repost|follow|mention|quote",
  "uri": "at://...", "cid": "bafyrei...", "is_read": false,
  "indexed_at": "2026-03-14T10:00:00Z",
  "author": {"handle": "...", "did": "...", "display_name": "...", "avatar": "..."},
  "record_text": "Their reply/post text (if applicable)",
  "reason_subject": "at://...the post they liked/reposted/replied-to (if applicable)",
  "subject_text": "Text of the subject post (if reason_subject exists)"
}
```

**Conversation object** (inside array from `dm-list`):
```json
{
  "id": "convo-id", "unread_count": 2,
  "members": [{"handle": "...", "did": "...", "display_name": "...", "avatar": "..."}],
  "last_message": {"id": "msg-id", "text": "...", "sent_at": "...", "sender_did": "did:plc:..."} or null
}
```

**DM message object** (inside array from `dm-read`):
```json
{"id": "msg-id", "text": "Message text", "sent_at": "2026-03-14T10:00:00Z", "sender_did": "did:plc:..."}
```

**Feed object** (inside array from `feeds`):
```json
{
  "uri": "at://did:plc:abc/app.bsky.feed.generator/whats-hot",
  "cid": "bafyrei...", "did": "did:web:...",
  "creator": {"handle": "...", "did": "...", "display_name": "...", "avatar": "..."},
  "display_name": "What's Hot", "description": "Trending posts across Bluesky",
  "avatar": "https://...", "like_count": 12345, "indexed_at": "2026-03-14T10:00:00Z"
}
```

### Command Response Keys

Each command returns these top-level keys:

| Command | Response keys |
|---------|--------------|
| `post` | `{"uri", "cid"}` |
| `delete` | `{"deleted"}` (the URI) |
| `like` | `{"liked", "uri"}` (post URI + like record URI) |
| `unlike` | `{"unliked"}` |
| `repost` | `{"reposted", "uri"}` (post URI + repost record URI) |
| `unrepost` | `{"unreposted"}` |
| `timeline` | `{"feed": [{"post": <post>, "reason": {"type": "repost", "by": <actor>} or null}], "cursor"}` |
| `thread` | `{"thread": <post with nested "replies": [...]>}` |
| `search-posts` | `{"posts": [<post>], "cursor"}` |
| `search-users` | `{"actors": [<profile>], "cursor"}` |
| `follow` | `{"followed", "uri"}` |
| `unfollow` | `{"unfollowed"}` |
| `followers` | `{"followers": [<actor>], "cursor"}` |
| `following` | `{"following": [<actor>], "cursor"}` |
| `mute` | `{"muted"}` |
| `unmute` | `{"unmuted"}` |
| `block` | `{"blocked", "uri"}` |
| `unblock` | `{"unblocked"}` |
| `profile` | `<profile>` (top-level, no wrapper) |
| `get` | `<post>` (top-level, no wrapper) |
| `my-posts` | `{"posts": [<post>], "cursor"}` |
| `user-posts` | `{"posts": [<post>], "cursor"}` |
| `likes` | `{"likes": [{"actor": <actor>, "created_at": "..."}], "cursor"}` |
| `reposts` | `{"reposted_by": [<actor>], "cursor"}` |
| `notifications` | `{"notifications": [<notification>], "cursor"}` |
| `notif-read` | `{"success": true}` |
| `dm-list` | `{"conversations": [<convo>], "cursor"}` |
| `dm-read` | `{"convo_id", "messages": [<dm>], "cursor"}` |
| `dm-send` | `{"sent": true, "convo_id", "message_id"}` |
| `dm-mark-read` | `{"success": true}` |
| `update-profile` | `<profile>` (top-level, no wrapper) |
| `post-thread` | `{"posts": [{"uri", "cid"}, ...]}` |
| `feeds` | `{"feeds": [<feed>], "cursor"}` |

**Important:** Note that `timeline` wraps posts in `feed[].post` (with an optional `reason`), while `search-posts` and `my-posts` use `posts[]` directly.

### Pagination

List commands support `--cursor TOKEN`. The response includes `"cursor"` (null = no more results).
1. First call: omit `--cursor`
2. Next page: pass the returned cursor as `--cursor`
3. Stop when cursor is null

### Errors

Errors return JSON with exit code 1:
```json
{"error": "ERROR_TYPE", "message": "Human-readable description", "type": "SUBTYPE (for AUTH_ERROR)"}
```

Error types: `NOT_FOUND`, `NOT_LIKED`, `NOT_REPOSTED`, `NOT_FOLLOWING`, `NOT_BLOCKING`, `FILE_NOT_FOUND`, `INVALID_ARGS`, `AUTH_ERROR`.

## Command Quick Reference

### Posting
| Command | Description |
|---------|-------------|
| `post "text"` | Create a text post (max 300 graphemes) |
| `post "text" --image photo.jpg --alt "description"` | Post with image (repeat `--image`/`--alt` for up to 4) |
| `post "text" --reply-to <uri>` | Reply to a post |
| `post "text" --quote <uri>` | Quote a post |
| `post "text" --quote <uri> --image photo.jpg --alt "desc"` | Quote with image |
| `post-thread "text1" "text2" "text3"` | Create a multi-post thread |
| `delete <uri>` | Delete a post |

### Engagement
| Command | Description |
|---------|-------------|
| `like <uri>` | Like a post |
| `unlike <uri>` | Unlike (pass the post URI, not the like URI) |
| `repost <uri>` | Repost a post |
| `unrepost <uri>` | Undo repost (pass the post URI) |

### Reading & Discovery
| Command | Description |
|---------|-------------|
| `timeline [--limit N] [--cursor TOKEN]` | Home timeline (default 20) |
| `thread <uri> [--depth N]` | Post thread with replies (default depth 6) |
| `search-posts "query" [--limit N] [--cursor TOKEN]` | Search posts |
| `search-users "query" [--limit N] [--cursor TOKEN]` | Search users |
| `feeds [--query "keyword"] [--limit N] [--cursor TOKEN]` | Browse suggested feed generators (note: `--query` filters client-side, so results may be fewer than `--limit`) |

### Social Graph
| Command | Description |
|---------|-------------|
| `follow <handle>` | Follow |
| `unfollow <handle>` | Unfollow |
| `followers <handle> [--limit N] [--cursor TOKEN]` | List followers |
| `following <handle> [--limit N] [--cursor TOKEN]` | List following |
| `mute <handle>` / `unmute <handle>` | Mute/unmute |
| `block <handle>` / `unblock <handle>` | Block/unblock |

### Profile & Info
| Command | Description |
|---------|-------------|
| `profile [handle]` | View profile (own if omitted) |
| `update-profile [--name "Name"] [--bio "Bio"] [--avatar image.jpg]` | Update your profile |
| `my-posts [--limit N] [--cursor TOKEN]` | Own recent posts |
| `user-posts <handle> [--limit N] [--cursor TOKEN]` | A user's recent posts |
| `get <uri>` | Fetch a single post |
| `likes <uri> [--limit N] [--cursor TOKEN]` | Who liked a post |
| `reposts <uri> [--limit N] [--cursor TOKEN]` | Who reposted a post |

### Notifications
| Command | Description |
|---------|-------------|
| `notifications [--limit N] [--unread-only] [--filter TYPE] [--cursor TOKEN]` | List notifications (filter: like, repost, follow, mention, reply, quote) |
| `notif-read` | Mark all as read |

### Direct Messages
| Command | Description |
|---------|-------------|
| `dm-list [--limit N] [--cursor TOKEN]` | List conversations |
| `dm-read --handle <handle> [--limit N] [--cursor TOKEN]` | Read messages with a user |
| `dm-read --convo-id <id> [--limit N] [--cursor TOKEN]` | Read messages by convo ID |
| `dm-send <handle> "text"` | Send a DM |
| `dm-mark-read --convo-id <id>` | Mark convo as read |
| `dm-mark-read --all` | Mark all as read |

Only text DMs are supported (no images).

## Common Workflows

### Check and respond to mentions
```bash
./bsky notifications --unread-only --filter mention
# Parse → for each notification, extract reason_subject (the post they mentioned you in)
./bsky get <reason_subject_uri>
# Read context, then reply:
./bsky post "Your reply" --reply-to <uri>
./bsky notif-read
```

### Engage with timeline
```bash
./bsky timeline --limit 30
# Parse → extract feed[].post objects
# Like interesting posts:
./bsky like <uri>
# Reply to engage:
./bsky post "Your reply" --reply-to <uri>
```

### Search and engage with a topic
```bash
./bsky search-posts "topic keywords" --limit 20
# Parse → like/repost/reply to relevant posts[]
./bsky like <uri>
./bsky repost <uri>
```

### Join a conversation (read thread before replying)
```bash
./bsky thread <uri> --depth 6
# Parse → read thread.text and thread.replies[] to understand context
./bsky post "Informed reply" --reply-to <uri>
```

### Grow the network
```bash
./bsky search-users "topic or niche" --limit 20
# Parse → review actors[] profiles for relevance
./bsky profile <handle>
# Check their posts before following:
./bsky user-posts <handle> --limit 10
# Avoid re-following — check viewer.following is null, then:
./bsky follow <handle>
```

### Check engagement on own posts
```bash
./bsky my-posts --limit 10
# Parse → find posts with high reply_count
./bsky thread <uri>
# Respond to replies, like engaged followers
./bsky likes <uri>
```

### Check and respond to DMs
```bash
./bsky dm-list
# Parse → find conversations[] with unread_count > 0
./bsky dm-read --convo-id <id>
# Parse → read messages[], reply:
./bsky dm-send <handle> "Your reply"
./bsky dm-mark-read --convo-id <id>
```

### Post a thread
```bash
./bsky post-thread "First, let me explain the context..." "Second, here's the main point..." "Finally, the conclusion."
# Returns: {"posts": [{"uri": "...", "cid": "..."}, ...]}
```

### Update your profile
```bash
./bsky update-profile --name "New Display Name" --bio "Updated bio text"
./bsky update-profile --avatar new-avatar.jpg
```

### Discover feeds
```bash
./bsky feeds --limit 10
# Filter by keyword:
./bsky feeds --query "news"
```

### Check before posting (avoid duplicates)
```bash
./bsky my-posts --limit 5
# Parse → check posts[].text for similar content
./bsky post "New post text"
```

## Key Concepts

- **Handles**: Always pass handles **without** the `@` prefix — use `user.bsky.social`, not `@user.bsky.social`.
- **URIs**: Every post has an AT Protocol URI (`at://did:plc:abc/app.bsky.feed.post/xyz`). Extract from the `uri` field in JSON. Used as arguments for like, reply, repost, thread, get, delete.
- **Rich text**: @mentions, #hashtags, URLs in post text are auto-converted to links. Write naturally.
- **Character limit**: 300 graphemes per post.
- **Unlike/unrepost**: Pass the **post URI**, not the like/repost record URI. Auto-resolved internally.
- **Reply threading**: `--reply-to <uri>` auto-resolves the thread root.

## Auth Troubleshooting

Auth errors: `{"error": "AUTH_ERROR", "type": "<TYPE>", "message": "..."}` with exit code 1.

1. **SESSION_CORRUPT** → `rm ~/.bsky_session.json` and retry
2. **MISSING_ENV** → Ensure `.env` has `BLUESKY_HANDLE` and `BLUESKY_APP_PASSWORD`
3. **INVALID_CREDENTIALS** → Handle: `user.bsky.social`, App password: `xxxx-xxxx-xxxx-xxxx` (19 chars)
4. **NETWORK** → Retry up to 3 times with 10s delay
5. **ACCOUNT_SUSPENDED** → Inform user, cannot fix programmatically
