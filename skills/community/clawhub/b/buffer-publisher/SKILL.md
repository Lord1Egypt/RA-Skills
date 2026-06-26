---
name: buffer-publisher
version: 1.0.1
description: Publish social media posts to LinkedIn and Twitter/X via Buffer GraphQL API. PRIMARY and ONLY tool for social publishing (Typefully cancelled 2026-03-25). Use when publishing posts to Nissan's social channels.
author: nissan
tags:
  - social-media
  - publishing
  - buffer
  - linkedin
  - twitter
metadata:
  openclaw:
    emoji: "📢"
    network:
      outbound: true
      reason: "Posts to Buffer GraphQL API (api.buffer.com/graphql) for social publishing"
    security_notes: "All API calls are made to api.buffer.com on behalf of the authenticated account owner. No user data is intercepted or forwarded to third parties. The Buffer API key is the owner's own credential, stored in 1Password."
    subprocess:
      note: "Uses curl commands as examples in skill docs; no shell exec required at runtime"
---
**Last used:** 2026-03-25
**Status:** Active — PRIMARY for LinkedIn

# Buffer Publisher

## When to Use This / When NOT to Use This

**Use Buffer when:**
- Publishing a post to LinkedIn (`nissandookeran`) or Twitter/X (`redditech`) — immediately or scheduled
- Queuing a post for Buffer's automatic optimal-time slot
- Any social publishing task from Liv or the content pipeline

**Do NOT use Buffer for:**
- Bluesky — not connected, no tool available yet
- Drafting content — Buffer publishes, it doesn't draft. Write content first, then call this skill.
- Reading/analytics — Buffer GraphQL can query posts but that's out of scope here; check Buffer dashboard directly
- Any platform other than LinkedIn and Twitter/X

> **Only tool available:** Typefully was cancelled 2026-03-25. Buffer is the single social publishing surface. There is no fallback.

---

## Credentials
- API key: `op://OpenClaw/Buffer API Credentials/credential`
- API base: `https://api.buffer.com/graphql`
- Auth header: `Authorization: Bearer <key>`

## Connected Channels
| Channel | ID | Service |
|---|---|---|
| nissandookeran | `69c29382af47dacb694d24b4` | LinkedIn |
| redditech | `69c29939af47dacb694d3d1f` | Twitter/X |

---

## Publish Immediately (shareNow)

```python
import json, subprocess

BUFFER_KEY = "<key from 1Password>"
CHANNEL_ID = "69c29382af47dacb694d24b4"  # LinkedIn
# or  "69c29939af47dacb694d3d1f"  # Twitter/X

payload = {
    "query": """mutation CreatePost($input: CreatePostInput!) { 
        createPost(input: $input) { 
            ... on PostActionSuccess { post { id status } } 
        } 
    }""",
    "variables": {
        "input": {
            "channelId": CHANNEL_ID,
            "text": "Your post text here",
            "schedulingType": "automatic",
            "mode": "shareNow"
        }
    }
}

result = subprocess.run(
    ["curl", "-s", "-X", "POST",
     "-H", f"Authorization: Bearer {BUFFER_KEY}",
     "-H", "Content-Type: application/json",
     "-d", json.dumps(payload),
     "https://api.buffer.com/graphql"],
    capture_output=True, text=True
)
d = json.loads(result.stdout)
post_id = d["data"]["createPost"]["post"]["id"]
status = d["data"]["createPost"]["post"]["status"]
print(f"Post ID: {post_id}, Status: {status}")
# status "sent" = published immediately
```

---

## Schedule a Post for a Specific Time

Use `mode: "customScheduled"` + a `dueAt` ISO8601 UTC timestamp. **Do NOT use `scheduledAt`** — that field does not exist on the Post type.

```python
import json, subprocess
from datetime import datetime, timezone

BUFFER_KEY = "<key from 1Password>"
CHANNEL_ID = "69c29382af47dacb694d24b4"  # LinkedIn

# Schedule for 9am Sydney time (UTC+11 in AEDT) = 22:00 UTC prior day
# Always convert to UTC before passing to Buffer
scheduled_utc = "2026-03-27T22:00:00Z"  # ISO8601 UTC — the Z suffix is required

payload = {
    "query": """mutation CreatePost($input: CreatePostInput!) { 
        createPost(input: $input) { 
            ... on PostActionSuccess { post { id status dueAt } } 
        } 
    }""",
    "variables": {
        "input": {
            "channelId": CHANNEL_ID,
            "text": "Your scheduled post text here",
            "schedulingType": "automatic",
            "mode": "customScheduled",
            "dueAt": scheduled_utc
        }
    }
}

result = subprocess.run(
    ["curl", "-s", "-X", "POST",
     "-H", f"Authorization: Bearer {BUFFER_KEY}",
     "-H", "Content-Type: application/json",
     "-d", json.dumps(payload),
     "https://api.buffer.com/graphql"],
    capture_output=True, text=True
)
d = json.loads(result.stdout)
post = d["data"]["createPost"]["post"]
print(f"Post ID: {post['id']}, Status: {post['status']}, Due: {post['dueAt']}")
# status "buffer" = queued/scheduled (not yet sent)
```

---

## What Success Looks Like

A successful `createPost` response body looks like this:

```json
{
  "data": {
    "createPost": {
      "post": {
        "id": "67e3a1b2c4d5e6f7a8b9c0d1",
        "status": "sent"
      }
    }
  }
}
```

- `status: "sent"` → published immediately (shareNow)
- `status: "buffer"` → queued or scheduled (will publish at `dueAt`)
- If `data.createPost` is `null` or missing `post`, the mutation failed silently — check for a top-level `errors` array

**Failure response example:**
```json
{
  "errors": [
    {
      "message": "Value \"shareNOW\" does not exist in \"SchedulingType\" enum.",
      "locations": [{"line": 1, "column": 42}]
    }
  ],
  "data": null
}
```

---

## Key Schema Notes
- `schedulingType` enum: `automatic` | `notification` (NOT "now", NOT "shareNow")
- `mode` enum: `addToQueue` | `shareNow` | `shareNext` | `customScheduled` | `recommendedTime`
- Use `automatic` + `shareNow` for immediate publish
- Use `automatic` + `customScheduled` + `dueAt` for scheduled posts
- `dueAt` field takes ISO8601 UTC datetime string (NOT `scheduledAt` — that field doesn't exist on Post type)
- Response type is a union — always use `... on PostActionSuccess` fragment
- `CoreApiError` does NOT exist in schema — omit error fragment or use other error types
- No `draft` field in `CreatePostInput` — omit it

## Get Connected Channels
```bash
curl -s -X POST \
  -H "Authorization: Bearer $BUFFER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ account { id name email channels { id name service } } }"}' \
  https://api.buffer.com/graphql
```

## Twitter/X Threads via Buffer
Buffer does not support native thread composition. Post as a single update with tweets separated by `\n\n---\n\n`. If true threading is ever needed, evaluate alternative tools at that point.

## Routing Rules
| Platform | Tool |
|---|---|
| LinkedIn | **Buffer** ✅ |
| Twitter/X | **Buffer** ✅ |
| Bluesky | Not connected — skip unless new tool added |

> Typefully cancelled 2026-03-25. No backup — Buffer is the only social publishing tool.

---

## Common Mistakes

1. **Wrong enum value for `schedulingType`**
   - ❌ `"schedulingType": "now"` → enum error
   - ❌ `"schedulingType": "shareNow"` → enum error (`shareNow` is a `mode` value, not a `schedulingType`)
   - ✅ `"schedulingType": "automatic"` (almost always what you want)

2. **Using `scheduledAt` instead of `dueAt`**
   - ❌ `"scheduledAt": "2026-03-27T22:00:00Z"` → field does not exist, silently ignored or errors
   - ✅ `"dueAt": "2026-03-27T22:00:00Z"`

3. **Forgetting `Content-Type: application/json`**
   - Returns `"Unsupported Content-Type"` error
   - Always include `-H "Content-Type: application/json"` in curl calls

4. **Using the legacy v1 API base URL**
   - ❌ `https://api.bufferapp.com/1/` → returns 500, dead endpoint
   - ✅ `https://api.buffer.com/graphql`

5. **Including `CoreApiError` in the error fragment**
   - This type does not exist in the schema. Omit it or you'll get a schema validation error.

6. **Including `"draft": true` in CreatePostInput**
   - This field doesn't exist. Buffer has no draft state via API — posts are either queued or live.

7. **Timezone confusion with `dueAt`**
   - Buffer expects UTC. Nissan is AEDT (UTC+11). Always convert: 9am Sydney = 10pm UTC prior day.

---

## Troubleshooting
- `"Unsupported Content-Type"` → must use `Content-Type: application/json`
- `500 from bufferapp.com` → legacy v1 API is dead, use `api.buffer.com/graphql`
- `"Value X does not exist in enum"` → check enum values via introspection: `{ __type(name: "SchedulingType") { enumValues { name } } }`
