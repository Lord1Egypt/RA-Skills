# API Reference

## Base URL

Use `http://localhost:3010` on the same machine or `http://<lan-ip>:3010` from
another device on the same LAN. The bundled CLI reads `CORKBOARD_API`.

If the dashboard operator has put corkie behind a reverse proxy to expose only
`/api/*` externally (see the "Exposing only the API" section of the main README),
`CORKBOARD_API` can also be set to a public HTTPS hostname like
`https://corkie-api.example.com`. The bearer-token header is still required, and
the frontend is not reachable through that hostname — only the API routes are.

Responses are JSON unless noted otherwise. Validation failures return `400` with `{"error":"..."}`. Missing rows return `404`.

## Authentication

Every request to `/api/*` requires an `Authorization: Bearer <token>` header. The
token lives in the dashboard's `.env` as `CORKBOARD_TOKEN` and is auto-generated
on first run. The bundled `corkboard.sh` helper loads it for you; for raw curl,
export it explicitly:

```bash
export CORKBOARD_TOKEN="$(grep '^CORKBOARD_TOKEN=' /path/to/dashboard/.env | cut -d= -f2-)"
```

Missing/invalid tokens return `401` with `WWW-Authenticate: Bearer realm="corkboard"`.

Socket.IO clients must pass `{ auth: { token: '<value>' } }` in the connect options;
the handshake is hard-rejected with a `connect_error` event when the token is wrong.

If your dashboard sits behind a reverse-proxy auth layer, the server admin can set
`CORKBOARD_AUTH=disabled` in `.env` to bypass these checks. Don't do this on a
public-facing instance without another auth layer in front of it.

## Pins

| Method | Endpoint | Notes |
|--------|----------|-------|
| `GET` | `/api/pins` | All non-deleted pins, ordered active first, then priority, then newest |
| `GET` | `/api/pins/:id` | Single non-deleted pin |
| `POST` | `/api/pins` | Create a pin, returns `201` |
| `PATCH` | `/api/pins/:id` | Update a pin, including `status` |
| `DELETE` | `/api/pins/:id` | Soft delete, returns `204 No Content` |
| `GET` | `/api/pins/history/deleted` | Deleted pin history, newest first, capped to 50 |
| `POST` | `/api/pins/:id/restore` | Restore a deleted pin and rebroadcast it as `pin:created` |

Example:
```bash
curl -X POST "$CORKBOARD_API/api/pins" \
  -H "Authorization: Bearer $CORKBOARD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"task","title":"Review PR","content":"Auth refactor complete","priority":1}'
```

Important request fields:
- Required on create: `type`, `title`
- On update (PATCH): all fields are optional; `title` and `content` are commonly updated for Task and Note pins (the dashboard supports inline editing of these via double-click on the title)
- Common optional fields: `content`, `url`, `dueAt`, `priority`, `status`
- Valid `status` values: `active | completed | snoozed | dismissed`
- Valid `priority` values: `1 | 2 | 3`; create defaults to `2`
- URL fields must be absolute `http(s)` URLs
- Specialized optional fields: `emailFrom`, `emailDate`, `emailId`, `repo`, `stars`, `forks`, `ideaVerdict`, `ideaScores`, `trackingNumber`, `trackingCarrier`, `trackingStatus`, `trackingEta`, `trackingUrl`, `articleData`, `youtubeData`

Validation notes:
- Bad enums, invalid priorities, malformed nested objects, and invalid `http(s)` URL fields return `400`.
- `articleData` must include `url`, `source`, `tldr`, and a `bullets` string array.
- `ideaScores.*` values must be finite numbers between `0` and `10`.
- `youtubeData` must include `videoId` (non-empty string) and `thumbnailUrl` (absolute http(s) URL). Optional: `channelTitle`, `description`, `publishedAt`, `duration`, `embedUrl`, `sourceUrl`.

## Projects

Projects are for sustained work with tracks and per-track task lists. `GET /api/projects` returns all non-deleted projects, including `active`, `on-hold`, `archived`, and `cellar`.

Project enums:
- `phase`: `concept | build | polish | publish | shipped`
- `projectStatus`: `active | on-hold | archived | cellar`
- `track.owner`: `claude | you | shared`
- `track.status`: `active | waiting | done | locked`

### Project routes

| Method | Endpoint | Notes |
|--------|----------|-------|
| `GET` | `/api/projects` | All non-deleted projects across every project status |
| `GET` | `/api/projects/:id` | Single non-deleted project |
| `POST` | `/api/projects` | Create project, returns `201` |
| `PATCH` | `/api/projects/:id` | Update name, emoji, color, or phase |
| `DELETE` | `/api/projects/:id` | Soft delete, returns `204 No Content` |
| `POST` | `/api/projects/:id/restore` | Restore deleted project and rebroadcast it as `project:created` |
| `POST` | `/api/projects/:id/hold` | Body: `{"reason":"..."}` |
| `POST` | `/api/projects/:id/resume` | Resume held, archived, or cellar project back to `active` |
| `POST` | `/api/projects/:id/archive` | Archive project |
| `POST` | `/api/projects/:id/cellar` | Move project into the future-ideas cellar |

Create-project body notes:
- Required: `name`
- Optional: `emoji`, `color`, `phase`, `tracks`, `initialStatus`
- `initialStatus` accepts `active | on-hold | archived | cellar`
- If you create tracks up front, the first track starts `active`; later tracks start `waiting`

### Track routes

| Method | Endpoint | Notes |
|--------|----------|-------|
| `POST` | `/api/projects/:id/tracks` | Body: `{"name":"...","owner":"claude|you|shared"}` |
| `PATCH` | `/api/projects/:id/tracks/:trackId` | Update track metadata, tasks, or attachment |
| `DELETE` | `/api/projects/:id/tracks/:trackId` | Delete track |
| `POST` | `/api/projects/:id/tracks/reorder` | Body: `{"order":["track-id", ...]}` with every track id exactly once |
| `POST` | `/api/projects/:id/tracks/:trackId/tasks/:taskId/toggle` | Toggle a task |

Track update notes:
- `tasks` must be an array of `{ id, text, done }`
- `attachment` may be `null` or:

```json
{
  "type": "code | image | file | link",
  "label": "firmware.ino",
  "note": "ready for bench test",
  "url": "https://example.com/optional"
}
```

- When a track changes to `done`, the server may auto-create a bridge `task` pin for the next handoff.
- Completing the final active track may also trigger a success lamp state.

Project example:
```bash
curl -X POST "$CORKBOARD_API/api/projects" \
  -H "Authorization: Bearer $CORKBOARD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Launch blog",
    "emoji":"✍️",
    "color":"#4ecdc4",
    "phase":"build",
    "tracks":[
      {"name":"Write posts","owner":"claude"},
      {"name":"Review","owner":"you"}
    ]
  }'
```

Cellar example:
```bash
curl -X POST "$CORKBOARD_API/api/projects" \
  -H "Authorization: Bearer $CORKBOARD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Retail display concept",
    "emoji":"🍷",
    "color":"#7a2f3a",
    "initialStatus":"cellar",
    "tracks":[
      {"name":"Rough concept","owner":"claude"},
      {"name":"Prototype feasibility","owner":"you"}
    ]
  }'
```

## Lamp Endpoints

| Method | Endpoint | Notes |
|--------|----------|-------|
| `GET` | `/api/lamp/status` | Returns current state plus HA connection info when HA is enabled |
| `POST` | `/api/lamp/:state` | Allowed states: `waiting`, `idle`, `attention`, `urgent`, `success`, `off` |

## WebSocket Events

The dashboard uses Socket.IO. REST mutations also broadcast over the socket.

### Server → client

| Event | Payload |
|-------|---------|
| `pin:created` | `Pin` |
| `pin:updated` | `Pin` |
| `pin:deleted` | `string` pin id |
| `pins:sync` | `Pin[]` |
| `project:created` | `Project` |
| `project:updated` | `Project` |
| `project:deleted` | `{ id: string }` |
| `projects:sync` | `Project[]` |

Notes:
- Restoring a pin emits `pin:created`.
- Restoring a project emits `project:created`.
- Track completion can emit both `project:updated` and an additional `pin:created` auto-pin.

### Client → server

| Event | Payload |
|-------|---------|
| `pin:complete` | `string` pin id |
| `pin:dismiss` | `string` pin id |
| `pins:request` | none |
| `projects:request` | none |
| `project:task:toggle` | `{ projectId, trackId, taskId }` |
