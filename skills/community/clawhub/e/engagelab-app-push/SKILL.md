---
name: engagelab-apppush
description: >
  Call EngageLab App Push REST APIs to send push notifications and in-app messages
  to Android, iOS, and HarmonyOS devices; manage tags and aliases; create scheduled
  tasks and push plans; batch push; recall messages; query statistics; and
  configure callbacks. Use this skill when the user wants to send push notifications
  via EngageLab, manage device tags/aliases, schedule pushes, use batch single push,
  group push, message recall, delete users, query push statistics, validate push
  requests, upload images for OPPO, use push-to-speech, or integrate with EngageLab
  App Push. Also trigger for "engagelab push", "app push api", "push notification",
  "registration_id", "tag alias", "scheduled push", "push plan", "batch push",
  "message recall", "push statistics", "push callback", or "MTPush".
---

# EngageLab App Push API Skill

This skill enables interaction with the EngageLab App Push REST API (MTPush). The service supports push notifications and in-app messages to Android, iOS, and HarmonyOS, with multi-vendor channel support (FCM, Huawei, Xiaomi, OPPO, vivo, Meizu, Honor, etc.).

It covers these areas:

1. **Create Push** — Send notification or message to single/multiple devices (broadcast, tag, alias, registration_id, segment)
2. **Batch Single Push** — Batch push by registration_id or alias (up to 500 per request)
3. **Group Push** — Push to all apps in a group
4. **Push Plan** — Create/update/list push plans and query msg_ids by plan
5. **Scheduled Tasks** — Create, get, update, delete scheduled push tasks (single, periodical, intelligent)
6. **Tag & Alias** — Query/set/delete device tags and aliases; query tag count
7. **Message Recall** — Recall a pushed message (within one day)
8. **Delete User** — Delete a user (registration_id) and all associated data
9. **Statistics** — Message lifecycle stats, report APIs
10. **Callback** — Webhook setup and signature verification
11. **Test Push** — Validate push request without sending
12. **Image API** — OPPO big/small picture upload
13. **Push-to-Speech** — Create/update voice broadcast files

## Resources

### scripts/

- **`push_client.py`** — Python client class (`EngageLabPush`) wrapping create push, batch push (regid/alias), device get/set/delete, tag count, message recall, validate push, push plan create/list, scheduled tasks CRUD, and message detail stats. Handles Basic auth and typed error handling. Use as a helper or import into the user's project.

### references/

- **`error-codes.md`** — Push API error codes and descriptions
- **`http-status-code.md`** — HTTP status code specification
- **`callback-api.md`** — Callback address, validation, security (X-CALLBACK-ID, HMAC-SHA256)

Source API docs: `doc/apppush/REST API/` (Create Push API, Batch Single Push API, Group Push API, Push Plan API, Scheduled Tasks API, Tag Alias API, Message Recall, Delete User API, Statistics API, Callback API, Test Push API, imageAPI, Push-to-Speech API, REST API OVERVIEW, HTTP Status code).

## Authentication

All EngageLab App Push API calls use **HTTP Basic Authentication**.

- **Base URL** (choose by data center):
  - Singapore: `https://pushapi-sgp.engagelab.com`
  - Virginia, USA: `https://pushapi-usva.engagelab.com`
  - Frankfurt: `https://pushapi-defra.engagelab.com`
  - Hong Kong: `https://pushapi-hk.engagelab.com`
- **Header**: `Authorization: Basic base64(appKey:masterSecret)`
- **Content-Type**: `application/json` (or `multipart/form-data` for Image/Push-to-Speech as specified)

Obtain **AppKey** and **Master Secret** from Console → Application Settings → Application Info.

**Group Push** uses a different auth: `username` = `group-` + GroupKey, `password` = Group Master Secret (from Group management).

**Example** (curl):

```bash
curl -X POST https://pushapi-sgp.engagelab.com/v4/push \
  -H "Content-Type: application/json" \
  -u "YOUR_APP_KEY:YOUR_MASTER_SECRET" \
  -d '{ "from": "push", "to": "all", "body": { "platform": "all", "notification": { "alert": "Hello!" } } }'
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
| Create/update push plan | `POST` | `/v4/push_plan` |
| List push plans | `GET` | `/v4/push_plan/list` |
| Msg IDs by plan | `GET` | `/v4/status/plan/msg/` |
| Create scheduled task | `POST` | `/v4/schedules` |
| Get scheduled task | `GET` | `/v4/schedules/{schedule_id}` |
| Update scheduled task | `PUT` | `/v4/schedules/{schedule_id}` |
| Delete scheduled task | `DELETE` | `/v4/schedules/{schedule_id}` |
| Tag count | `GET` | `/v4/tags_count` |
| Get device (tags/alias) | `GET` | `/v4/devices/{registration_id}` |
| Set device tags/alias | `POST` | `/v4/devices/{registration_id}` |
| Delete device (user) | `DELETE` | `/v4/devices/{registration_id}` |
| Message recall | `DELETE` | `/v4/push/withdraw/{msg_id}` |
| Message statistics | `GET` | `/v4/status/detail` (message_ids) |
| Test push (validate) | `POST` | `/v4/push/validate` |
| OPPO image upload | `POST` | `/v4/image/oppo` |
| Create/update voice | `POST` | `/v4/voices` |
| List/delete voices | `GET` / `DELETE` | `/v4/voices` |

## Create Push (`POST /v4/push`)

Push a notification or message to a single device or list of devices. Body is JSON.

### Request structure (summary)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `from` | string | No | Sender, e.g. `"push"` |
| `to` | string or object | Yes | Target: `"all"` (broadcast), or object with `tag`, `tag_and`, `tag_not`, `alias`, `registration_id`, `live_activity_id`, `seg` |
| `body` | object | Yes | See below |
| `request_id` | string | No | Client-defined request ID returned in response |
| `custom_args` | object | No | Returned on callback, max 128 chars |

### body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `platform` | string or array | Yes | `"all"` or `["android","ios","hmos"]` |
| `notification` | object | Optional* | Notification content (android, ios, hmos; alert, title, extras, etc.) |
| `message` | object | Optional* | In-app/custom message (msg_content, title, content_type, extras) |
| `live_activity` | object | Optional* | iOS Live Activity (ios.event, content-state, attributes, etc.) |
| `voip` | object | Optional* | iOS VoIP (key-value); cannot coexist with notification/message/live_activity |
| `options` | object | No | time_to_live, apns_production, apns_collapse_id, big_push_duration, multi_language, third_party_channel, plan_id, cid, etc. |

*One of notification, message, live_activity, or voip must exist; they cannot coexist (except notification+message in some cases — see doc). For iOS, set `options.apns_production` (true/false) for environment.

### Push target `to` examples

- Broadcast: `"to": "all"`
- Tags (OR): `"to": { "tag": ["Shenzhen","Guangzhou"] }`
- Tags (AND): `"to": { "tag_and": ["female","members"] }`
- Alias: `"to": { "alias": ["user1","user2"] }`
- Registration IDs: `"to": { "registration_id": ["id1","id2"] }`
- Segment: `"to": { "seg": { "id": "segid" } }`
- Live Activity: `"to": { "live_activity_id": "LiveActivity-1" }`

### Response (success)

```json
{ "request_id": "12345678", "msg_id": "1828256757" }
```

For full parameter details (android/ios/hmos notification fields, options, multi_language, third_party_channel, push limits per vendor), see `doc/apppush/REST API/Create Push API.md`. Error codes: `references/error-codes.md`.

## Batch Single Push

- **By registration_id**: `POST /v4/batch/push/regid`
- **By alias**: `POST /v4/batch/push/alias`

Request body: `{ "requests": [ { "target": "reg_id_or_alias", "platform": "android"|"ios"|"all", "notification": {...}, "message": {...}, "options": {...}, "custom_args": {...} } ] }`. Max **500** items per request; `target` must be unique in the batch. Response returns per-target result (msg_id or error). See `doc/apppush/REST API/Batch Single Push API.md`.

## Group Push

`POST /v4/grouppush` — Same body structure as Create Push. Auth: Basic with `group-{GroupKey}` and Group Master Secret. Response includes `group_msgid` and per-app msg_id. override_msg_id and Schedule API are not supported for group push.

## Push Plan

- Create/update: `POST /v4/push_plan` — Body: `{ "plan_id": "xxx", "plan_description": "..." }`.
- List: `GET /v4/push_plan/list?page_index=1&page_size=20&send_source=0|1&search_description=xxx`.
- Msg IDs by plan: `GET /v4/status/plan/msg/?plan_ids=id1,id2&start_date=yyyy-MM-dd&end_date=yyyy-MM-dd` (within 30 days, max 31 days span).

Use `plan_id` in Create Push `body.options` to associate a push with a plan.

## Scheduled Tasks

- Create: `POST /v4/schedules` — Body includes `name`, `enabled`, `trigger` (single / periodical / intelligent), `push` (same as Create Push body).
- Get: `GET /v4/schedules/{schedule_id}`.
- Update: `PUT /v4/schedules/{schedule_id}`.
- Delete: `DELETE /v4/schedules/{schedule_id}`.

Trigger types: **single** (one-time, `time`, `zone_type`), **periodical** (start, end, time, time_unit, point, zone_type), **intelligent** (backup_time: `"now"` or `"yyyy-MM-dd HH:mm:ss"`). See `doc/apppush/REST API/Scheduled Tasks API.md`.

## Tag & Alias

- **Tag count**: `GET /v4/tags_count?tags=tag1&tags=tag2&platform=android|ios|hmos` (up to 1000 tags).
- **Get device**: `GET /v4/devices/{registration_id}` — Returns `tags`, `alias`.
- **Set device**: `POST /v4/devices/{registration_id}` — Body: `{ "tags": { "add": ["t1"], "remove": ["t2"] }, "alias": "alias1" }`.

Limits: 100,000 tags per app; 40 bytes per tag; 100 tags per device; 100,000 devices per tag; one alias per device (40 bytes). See `doc/apppush/REST API/Tag Alias API.md`.

## Message Recall

`DELETE /v4/push/withdraw/{msg_id}` — Recall within one day; no duplicate recall.

## Delete User

`DELETE /v4/devices/{registration_id}` — Asynchronously deletes user and all related data (tags, alias, device info, timezone). Cannot be restored. Batch deletion not supported.

## Statistics

- **Message detail**: `GET /v4/status/detail?message_ids=id1,id2` (up to 100 message_ids). Returns targets, sent, delivered, impressions, clicks, and sub-stats by channel. Data retained up to one month.

Other report endpoints (e.g. report APIs) are documented in `doc/apppush/REST API/Statistics API.md`.

## Callback

Configure callback URL (via Engagelab support). Validation: server sends POST with `echostr` in body; respond with body = `echostr` value. Security: use `X-CALLBACK-ID` header; `signature = HMAC-SHA256(secret, timestamp+nonce+username)`. Respond with 200/204 within 3 seconds for success. See `references/callback-api.md` and `doc/apppush/REST API/Callback API.md`.

## Test Push

`POST /v4/push/validate` — Same body as Create Push. Validates request without sending to users.

## Image API (OPPO)

`POST /v4/image/oppo` — Body: `{ "big_picture_url": "url", "small_picture_url": "url" }`. Returns `big_picture_id`, `small_picture_id` for use in push options (e.g. third_party_channel.oppo). OPPO constraints: big 984×369, ≤1MB; small 144×144, ≤50KB; PNG/JPG/JPEG.

## Push-to-Speech

- Create/update: `POST /v4/voices` — `Content-Type: multipart/form-data`; fields: `language` (en, zh-Hans, zh-Hant), `file` (zip of mp3 files). Returns `file_url`.
- List: `GET /v4/voices`.
- Delete: `DELETE /v4/voices?language=en`.

Use `options.voice_value` in push body to reference voice for TTS. See `doc/apppush/REST API/Push-to-Speech API.md`.

## Generating Code

When the user asks to send push or use other App Push APIs, generate working code. Default to **curl** unless the user specifies a language. Supported patterns:

- **curl** — Shell with `-u "AppKey:MasterSecret"` and correct base URL
- **Python** — `requests` with Basic auth
- **Node.js** — `fetch` or `axios`
- **Java** — `HttpClient`
- **Go** — `net/http`

Always include the Authorization header and error handling. Use placeholders like `YOUR_APP_KEY` and `YOUR_MASTER_SECRET` if credentials are not provided.

### Python Example — Create Push

```python
import requests

APP_KEY = "YOUR_APP_KEY"
MASTER_SECRET = "YOUR_MASTER_SECRET"
BASE_URL = "https://pushapi-sgp.engagelab.com"

resp = requests.post(
    f"{BASE_URL}/v4/push",
    auth=(APP_KEY, MASTER_SECRET),
    headers={"Content-Type": "application/json"},
    json={
        "from": "push",
        "to": "all",
        "body": {
            "platform": "all",
            "notification": {
                "alert": "Hello, Push!",
                "android": {"alert": "Hi, Android!", "title": "Title"},
                "ios": {"alert": "Hi, iOS!", "sound": "default", "badge": "+1"},
            },
            "options": {"time_to_live": 86400, "apns_production": False},
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
