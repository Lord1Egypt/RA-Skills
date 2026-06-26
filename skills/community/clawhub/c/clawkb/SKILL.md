---
name: clawkb
description: Use this skill when an agent needs to work with a ClawKB server over HTTP: register itself, obtain or use a Bearer token, upload images, create or update entries, search entries, read entry detail, or inspect plugin-backed API flows.
---

# ClawKB

## Overview

This skill is for operating ClawKB as an API client. Use it when the task is to register an agent account, authenticate with a Bearer token, upload images to MinIO through ClawKB, create or edit entries, or search and read stored knowledge.

Assume the server base URL is provided by the user. If not, ask for it. Prefer `curl` examples unless the user requests another client.

## Quick Start

1. Get a base URL, for example `http://localhost:3500`.
2. If you do not already have a token, register an agent with `POST /api/auth/register-agent`.
3. Store the returned `apiToken`.
4. Send authenticated requests with `Authorization: Bearer <token>`.

Example:

```bash
BASE_URL="http://localhost:3500"

curl -sS "$BASE_URL/api/auth/register-agent" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "OpenClaw Recon Agent",
    "avatarUrl": "https://example.com/agent-avatar.png"
  }'
```

Successful response fields to retain:

- `user.id`
- `user.username`
- `apiToken`
- `token.prefix`
- `token.type`

## Authentication

Use Bearer token auth for API automation.

```bash
TOKEN="clawkb_..."

curl -sS "$BASE_URL/api/me" \
  -H "Authorization: Bearer $TOKEN"
```

If the response is `401`, the token is invalid or revoked. If the response is `403`, the token exists but the user does not have enough permission for that route.

## Create Entries

Use `POST /api/entries`.

Required fields:

- `type`
- `source`
- `title`

Common optional fields:

- `summary`
- `content`
- `status`
- `url`
- `tags`
- `metadata`
- `images`

Example:

```bash
curl -sS "$BASE_URL/api/entries" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "report",
    "source": "nightly-recon",
    "title": "GPU cluster pricing moved lower this week",
    "summary": "Spot market pricing softened across three vendors.",
    "content": "## Notes\nObserved lower prices in APAC and US regions.",
    "status": "new",
    "tags": ["gpu", "cloud-pricing"],
    "metadata": {
      "region": ["us", "apac"],
      "confidence": "medium"
    }
  }'
```

The response includes:

- entry core fields
- `author`
- `tags`
- `images`

## Edit Entries

Use `PATCH /api/entries/:id`.

Editors can update their own entries. Admins can update any entry.

```bash
ENTRY_ID=123

curl -sS -X PATCH "$BASE_URL/api/entries/$ENTRY_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "summary": "Updated summary after analyst review.",
    "status": "interested",
    "tags": ["gpu", "cloud-pricing", "capacity"]
  }'
```

Delete uses `DELETE /api/entries/:id` and is typically admin-only.

## Upload Images

Use `POST /api/upload` with `multipart/form-data`.

For entry images:

```bash
curl -sS "$BASE_URL/api/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "kind=entry" \
  -F "file=@/path/to/image.png"
```

For avatar images:

```bash
curl -sS "$BASE_URL/api/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "kind=avatar" \
  -F "file=@/path/to/avatar.png"
```

Upload response fields:

- `url`
- `key`
- `filename`
- `mimeType`
- `size`

To attach uploaded images when creating or editing an entry, include:

```json
{
  "images": [
    {
      "url": "https://minio.example/entries/user-7/...",
      "key": "entries/user-7/...",
      "filename": "image.png",
      "mimeType": "image/png",
      "size": 12345,
      "caption": "Optional caption"
    }
  ]
}
```

## Search And Read

List or search entries with `GET /api/entries`.

Useful query params:

- `search`
- `type`
- `status`
- `source`
- `tag`
- `page`
- `limit`
- `sort`

Examples:

```bash
curl -sS "$BASE_URL/api/entries?search=gpu&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

```bash
curl -sS "$BASE_URL/api/entries?tag=cloud-pricing&status=interested" \
  -H "Authorization: Bearer $TOKEN"
```

Read one entry:

```bash
curl -sS "$BASE_URL/api/entries/$ENTRY_ID" \
  -H "Authorization: Bearer $TOKEN"
```

Entry detail may include `pluginRender`, which indicates plugin-provided UI or related blocks.

## Comments

To comment on another user's entry, use:

```bash
curl -sS "$BASE_URL/api/entries/$ENTRY_ID/comments" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"content":"Flagging this for follow-up next week."}'
```

List comments:

```bash
curl -sS "$BASE_URL/api/entries/$ENTRY_ID/comments" \
  -H "Authorization: Bearer $TOKEN"
```

## API Reference

- `POST /api/auth/register-agent`
  Registers an agent user and returns a new API token.
- `GET /api/me`
  Returns the authenticated principal.
- `POST /api/upload`
  Uploads an entry image or avatar.
- `GET /api/entries`
  Lists and searches entries.
- `POST /api/entries`
  Creates an entry.
- `GET /api/entries/:id`
  Reads one entry.
- `PATCH /api/entries/:id`
  Updates one entry.
- `DELETE /api/entries/:id`
  Deletes one entry.
- `GET /api/entries/:id/comments`
  Lists comments for an entry.
- `POST /api/entries/:id/comments`
  Creates a comment.
- `GET /api/search`
  Uses ClawKB search endpoints if the deployment exposes them.

## Working Rules

- Prefer Bearer token auth for agent automation.
- Preserve returned `key` values from image upload responses; they are needed for image references.
- When updating entries, send only the fields that should change.
- If the server returns plugin-related data, keep it intact unless the user explicitly wants to strip or replace it.
- If a request fails, surface the HTTP status and the JSON `error` field.

## Auto-Recall Plugin (Optional)

By default this skill provides **manual** ClawKB access — the agent must explicitly call the API to search. For **automatic** knowledge recall on every conversation, install the companion OpenClaw gateway plugin:

```bash
openclaw plugins install @hata1234/clawkb-openclaw
```

**What it does:**
- Hooks into `before_prompt_build` — automatically searches ClawKB before the agent sees each message
- Injects relevant knowledge entries into the agent's system context
- Supports multiple ClawKB instances in parallel (e.g. personal KB + company KB + public KB)
- Per-sender token mapping — different users get different access levels, controlled entirely by ClawKB server-side ACL

**After installing, configure in OpenClaw settings:**
1. Add your ClawKB instance URL
2. Create API tokens in ClawKB (Settings → API Tokens)
3. Map sender IDs to tokens in the plugin config

**Don't want it?** This is completely optional. The skill works fine without the plugin — you just search manually via the API.

## Internal Links (Entry Mentions)

ClawKB supports internal links between entries using a wiki-style syntax:

```
[[entry:ID|Display Title]]
```

**Examples:**

```markdown
See point 3 in [[entry:134|Gap Analysis]]
This issue is discussed in [[entry:143|Root Cause Report]] and [[entry:145|Mitigation Plan]]
```

**Rules:**

- The syntax is `[[entry:<numeric_id>|<display_text>]]`
- `display_text` is typically the entry title at time of writing
- When rendered, these become clickable links to `/entries/<id>` with a distinctive pill-badge style
- The search API supports numeric ID lookup: `?search=142` will match entry #142 directly
- **Do NOT use plain `#123` for entry references** — that syntax is not recognized and may conflict with other uses (e.g. order numbers)
- When creating entries that reference other entries, always use the `[[entry:ID|title]]` format
- In the web UI, users can type `[[` in the content editor to trigger an autocomplete popup for selecting entries

**Agent usage example (creating an entry with internal links):**

```bash
curl -sS "$BASE_URL/api/entries" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "knowledge",
    "source": "agent",
    "title": "Unified Root Cause Analysis",
    "content": "## Analysis\n\nBased on [[entry:143|Root Cause Report]], insufficient moisture retention was the primary factor.\n\nSee [[entry:147|Mitigation Summary]] for action items.",
    "tags": ["quality", "analysis"]
  }'
```
