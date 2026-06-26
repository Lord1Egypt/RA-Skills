---
name: engagelab-webpush
description: >
  Call EngageLab Web Push REST APIs to send push notifications and in-app messages
  to web browsers (Chrome, Firefox, Safari, Edge, etc.); manage tags and aliases;
  create scheduled tasks; batch push by registration_id or alias; group push;
  delete users; query statistics; and configure callbacks. Use this skill when the
  user wants to send web push via EngageLab, manage web device tags/aliases,
  schedule web pushes, use batch single push, group push, delete web users, query
  web push statistics, or integrate with EngageLab Web Push. Also trigger for
  "engagelab web push", "web push api", "browser push", "registration_id",
  "tag alias web", "scheduled web push", "batch web push", "web push callback", or
  "MTPush web".
---

# EngageLab Web Push API Skill

This skill enables interaction with the EngageLab Web Push REST API (MTPush Web). The service supports push notifications and in-app messages to web platforms only, with support for EngageLab channel and system channels (Chrome, Firefox, Safari, Edge, Opera).

It covers these areas:

1. **Create Push** — Send notification or message to single/multiple web devices (broadcast, tag, alias, registration_id)
2. **Batch Single Push** — Batch push by registration_id or alias (up to 500 per request)
3. **Group Push** — Push to all apps in a group
4. **Scheduled Tasks** — Create, get, update, delete scheduled web push tasks (single, periodical, intelligent)
5. **Tag & Alias** — Query/set/delete device tags and aliases; query tag count
6. **Delete User** — Delete a user (registration_id) and all associated data
7. **Statistics** — Message lifecycle stats (targets, sent, delivered, impressions, clicks by channel)
8. **Callback** — Webhook setup and signature verification

## Resources

### scripts/

- **`webpush_client.py`** — Python client class (`EngageLabWebPush`) wrapping create push, batch push (regid/alias), device get/set/delete, tag count, scheduled tasks CRUD, and message details. Handles Basic auth and typed error handling.

### references/

- **`error-codes.md`** — Web Push API error codes and descriptions
- **`http-status-code.md`** — HTTP status code specification
- **`callback-api.md`** — Callback address, validation, security (X-CALLBACK-ID, HMAC-SHA256)

Source API docs: `doc/webpush/REST API/` (REST API Overview, Create Push API, Batch Single Push API, Group Push API, Scheduled Tasks API, Tag Alias API, Delete User API, Statistics API, Callback API, HTTP Status Code).

## Authentication

All EngageLab Web Push API calls use **HTTP Basic Authentication**.

- **Base URL** (choose by data center):
  - Singapore: `https://webpushapi-sgp.engagelab.com`
  - Hong Kong: `https://webpushapi-hk.engagelab.com`
- **Header**: `Authorization: Basic base64(appKey:masterSecret)`
- **Content-Type**: `application/json`

Obtain **AppKey** and **Master Secret** from Console → Application Settings → Application Info.

**Group Push** uses different auth: `username` = `group-` + GroupKey, `password` = Group Master Secret (from Group management).

**Example** (curl):

```bash
curl -X POST https://webpushapi-sgp.engagelab.com/v4/push \
  -H "Content-Type: application/json" \
  -u "YOUR_APP_KEY:YOUR_MASTER_SECRET" \
  -d '{ "from": "push", "to": "all", "body": { "platform": "web", "notification": { "web": { "alert": "Hello!", "title": "Web Push", "url": "https://example.com" } } } }'
```

If the user hasn't provided credentials, ask for **AppKey** and **Master Secret** before generating API calls.

## Request Rate Limits

- **Standard**: 500 requests per second per AppKey.
- Batch Single Push shares the same QPS quota as the Push API (1 target = 1 QPS).

## Quick Reference — Main Endpoints

| Operation | Method | Path |
|-----------|--------|------|
| Create push | `POST` | `/v4/push` |
| Batch push by registration_id | `POST` | `/v4/batch/push/regid` |
| Batch push by alias | `POST` | `/v4/batch/push/alias` |
| Group push | `POST` | `/v4/grouppush` |
| Create scheduled task | `POST` | `/v4/schedules` |
| Get scheduled task | `GET` | `/v4/schedules/{schedule_id}` |
| Update scheduled task | `PUT` | `/v4/schedules/{schedule_id}` |
| Delete scheduled task | `DELETE` | `/v4/schedules/{schedule_id}` |
| Tag count | `GET` | `/v4/tags_count` |
| Get device (tags/alias) | `GET` | `/v4/devices/{registration_id}` |
| Set device tags/alias | `POST` | `/v4/devices/{registration_id}` |
| Delete device (user) | `DELETE` | `/v4/devices/{registration_id}` |
| Message statistics | `GET` | `/v4/messages/details` (message_ids) |

## Create Push (`POST /v4/push`)

Push a notification or message to web devices. Platform is **web** only.

### Request structure (summary)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `from` | string | No | Sender, e.g. `"push"` |
| `to` | string or object | Yes | Target: `"all"` (broadcast, devices active within 30 days), or object with `tag`, `tag_and`, `tag_not`, `alias`, `registration_id` |
| `body` | object | Yes | See below |
| `request_id` | string | No | Client-defined request ID returned in response |
| `custom_args` | object | No | Returned on callback |

### body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `platform` | string | Yes | Must be `"web"` |
| `notification` | object | Optional* | Notification content (web: alert, title, url, icon, image, extras) |
| `message` | object | Optional* | In-app/custom message (msg_content, title, content_type, extras) |
| `options` | object | No | time_to_live, override_msg_id, big_push_duration, web_buttons, multi_language, third_party_channel (w3push.distribution), plan_id, cid |

*One of notification or message must exist; they cannot coexist.

### notification.web

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `alert` | string | Yes | Message content |
| `url` | string | Yes | Click jump URL |
| `title` | string | No | Message title |
| `icon` | string | No | Notification icon (recommended 192×192px; ≤1MB; JPG/PNG/GIF; Chrome, Firefox) |
| `image` | string | No | Big image (recommended 360×180px; ≤1MB; Chrome, Edge) |
| `extras` | object | No | Custom key-value for business |

### options (highlights)

- **time_to_live**: Offline retention in seconds (default 86400, max 15 days); 0 = online only.
- **override_msg_id**: Override a previous message (effective 1 day).
- **big_push_duration**: Throttled push over n minutes (max 1440); max 20 throttled pushes at once.
- **web_buttons**: Array of up to 2 buttons (id, text, icon, url); Chrome 48+.
- **multi_language**: Per-language content/title (e.g. en, zh-Hans).
- **third_party_channel.w3push.distribution**: `first_ospush` | `mtpush` | `secondary_push` | `ospush` for system channel priority.
- **plan_id**, **cid**: Push plan ID and duplicate-prevention ID (max 64 chars, unique per AppKey).

### Push target `to` examples

- Broadcast: `"to": "all"`
- Tags (OR): `"to": { "tag": ["tag1","tag2"] }`
- Tags (AND): `"to": { "tag_and": ["tag3","tag4"] }`
- Tag NOT: `"to": { "tag_not": ["tag5"] }`
- Alias: `"to": { "alias": ["user1","user2"] }` (up to 1000)
- Registration IDs: `"to": { "registration_id": ["id1","id2"] }` (up to 1000)

### Response (success)

```json
{ "request_id": "12345678", "msg_id": "1828256757" }
```

Notification body length limit: 2048 bytes (doc); total message limit 4000 bytes. See `doc/webpush/REST API/Create Push API.md`. Error codes: `references/error-codes.md`.

## Batch Single Push

- **By registration_id**: `POST /v4/batch/push/regid`
- **By alias**: `POST /v4/batch/push/alias`

Request body: `{ "requests": [ { "target": "reg_id_or_alias", "platform": "web", "notification": { "web": { "alert", "title", "url", ... } }, "message": {...}, "options": {...}, "custom_args": {...} } ] }`. Max **500** items per request; `target` must be unique. See `doc/webpush/REST API/Batch Single Push API.md`.

## Group Push

`POST /v4/grouppush` — Same body structure as Create Push (platform `web`, notification.web). Auth: Basic with `group-{GroupKey}` and Group Master Secret. override_msg_id and Schedule API not supported for group push.

## Scheduled Tasks

- Create: `POST /v4/schedules` — Body: `name`, `enabled`, `trigger` (single / periodical / intelligent), `push` (same as Create Push body with platform web).
- Get: `GET /v4/schedules/{schedule_id}`.
- Update: `PUT /v4/schedules/{schedule_id}`.
- Delete: `DELETE /v4/schedules/{schedule_id}`.

Trigger types: **single** (time, zone_type), **periodical** (start, end, time, time_unit, point, zone_type), **intelligent** (backup_time: `"now"` or `"yyyy-MM-dd HH:mm:ss"`). Max 1000 valid scheduled tasks. See `doc/webpush/REST API/Scheduled Tasks API.md`.

## Tag & Alias

- **Tag count**: `GET /v4/tags_count?tags=tag1&tags=tag2&platform=web` (up to 1000 tags; platform for Web Push is typically `web` — confirm in doc).
- **Get device**: `GET /v4/devices/{registration_id}` — Returns `tags`, `alias`.
- **Set device**: `POST /v4/devices/{registration_id}` — Body: `{ "tags": { "add": ["t1"], "remove": ["t2"] }, "alias": "alias1" }`.

Limits: 100,000 tags per app; 40 bytes per tag; 100 tags per device; 100,000 devices per tag; one alias per device (40 bytes); 100,000 aliases per app. See `doc/webpush/REST API/Tag Alias API.md`.

## Delete User

`DELETE /v4/devices/{registration_id}` — Asynchronously deletes user and all related data. Cannot be restored. Batch deletion not supported.

## Statistics

- **Message details**: `GET /v4/messages/details?message_ids=id1,id2` (up to 100 message_ids). Returns targets, sent, delivered, impressions, clicks, and sub-stats by channel (sub_web: engageLab_web, chrome, safari, firefox, edge, opera). Data retained up to one month. See `doc/webpush/REST API/Statistics API.md`.

## Callback

Configure callback URL (via Engagelab support). Validation: server sends POST with `echostr` in body; respond with body = `echostr` value. Security: use `X-CALLBACK-ID` header; `signature = HMAC-SHA256(secret, timestamp+nonce+username)`. Respond with 200/204 within 3 seconds for success. See `references/callback-api.md` and `doc/webpush/REST API/Callback API.md`.

## Generating Code

When the user asks to send web push or use other Web Push APIs, generate working code. Default to **curl** unless the user specifies a language. Supported: **curl**, **Python** (requests), **Node.js** (fetch/axios), **Java** (HttpClient), **Go** (net/http). Always include the Authorization header and error handling. Use placeholders `YOUR_APP_KEY` and `YOUR_MASTER_SECRET` if credentials are not provided.

### Python Example — Create Web Push

```python
import requests

APP_KEY = "YOUR_APP_KEY"
MASTER_SECRET = "YOUR_MASTER_SECRET"
BASE_URL = "https://webpushapi-sgp.engagelab.com"

resp = requests.post(
    f"{BASE_URL}/v4/push",
    auth=(APP_KEY, MASTER_SECRET),
    headers={"Content-Type": "application/json"},
    json={
        "from": "push",
        "to": "all",
        "body": {
            "platform": "web",
            "notification": {
                "web": {
                    "alert": "Hello, Web Push!",
                    "title": "Web Push Title",
                    "url": "https://example.com",
                    "extras": {"key": "value"},
                }
            },
            "options": {"time_to_live": 86400},
        },
        "request_id": "req_001",
    },
)
result = resp.json()
if resp.status_code == 200:
    print("msg_id:", result.get("msg_id"))
else:
    print("Error:", result.get("error"))
```
