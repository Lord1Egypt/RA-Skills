---
name: brix-signage
description: Control Brix digital signage screens from an agent — list screens and check which are offline, put an image, video or playlist on screens for a set time, import media from a URL, set what a screen plays, reboot or refresh a screen, fire an emergency message, and pull proof-of-play reports.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📺"
    homepage: https://brixsignage.com/developers/
    requires:
      env:
        - BRIX_API_KEY
      bins:
        - curl
    primaryEnv: BRIX_API_KEY
    envVars:
      - name: BRIX_API_KEY
        required: true
        description: Brix API key (starts with ak_). Create it in the Brix CMS under Settings → AI, API & MCP.
---

# Brix digital signage

[Brix](https://brixsignage.com/?utm_source=clawhub&utm_medium=skill) is cloud digital signage software. It runs screens on the Amazon Signage Stick, Fire TV, Android, Windows and web players, and manages them from one console. This skill calls the Brix REST API.

## Setup

1. Sign up for a free 7-day trial (no card needed): https://brixsignage.com/start?utm_source=clawhub&utm_medium=skill
2. In the Brix CMS open **Settings → AI, API & MCP** and create an API key. Only give it the permissions the agent needs, such as `screen.view`, `screen.cast` or `media.create`. You can also limit the key to one location.
3. Set `BRIX_API_KEY` to the key (`ak_…`).

Pricing is $6 per screen per month billed yearly, or $8 month to month.

## Calling the API

- Base URL: `https://api.brixsignage.com`
- Auth header: `Authorization: Bearer $BRIX_API_KEY`
- Successful responses are `{ "data": … }`. Errors are `{ "error": "<code>", "message": "…" }`.
- A `429` or a `503 database_busy` comes with `Retry-After`. Wait that long and retry.
- Paged lists take `?limit=`. Follow `nextCursor` with `?cursor=` until it is null.
- Full OpenAPI spec: https://api.brixsignage.com/v1/openapi.json

```bash
curl -s https://api.brixsignage.com/v1/screens -H "Authorization: Bearer $BRIX_API_KEY"
```

Always look up real ids with a list call first. Never guess an id.

## Tasks

### See screens and which are offline
`GET /v1/screens` returns each screen's location, assigned content, online status and player settings. `GET /v1/screens/{id}` returns one screen. `GET /v1/screens/{id}/diagnose` explains why a screen is having trouble.

### Find content
- `GET /v1/media`: images, videos and web links
- `GET /v1/playlists`
- `GET /v1/schedules`
- `GET /v1/screen-groups`

### Add media from a URL
`POST /v1/media/import-url` with `{"url": "https://…/file.jpg", "name": "Lunch special"}`. Brix fetches the file on its own servers and returns the new media item.

### Put something on screens for a while (a cast)
`POST /v1/casts`:
```json
{ "contentKind": "media", "contentId": "<media id>", "scopeKind": "screens",
  "screenIds": ["<screen id>"], "expiresAt": "2026-10-20T18:00:00Z" }
```
- `contentKind` is one of `media`, `playlist`, `app`, `creative` or `schedule`.
- `scopeKind` is `all`, `node` (with `scopeNodeId` set to a location id) or `screens` (with `screenIds`).
- The screens go back to their normal content when `expiresAt` passes. End a cast early with `POST /v1/casts/{id}/clear`.

### Change what a screen normally plays
`POST /v1/screens/{id}/assign` with `{"contentKind": "playlist", "contentId": "<playlist id>"}`. This is a lasting change. Confirm with the user before you make it.

### Device commands
`POST /v1/screens/{id}/commands` with `{"kind": "reboot"}`. Other kinds include `refresh`, `screenshot`, `clear-cache`, `cec-on`/`cec-off` (turn the TV on or off), and `set-volume` with `{"payload": {"level": 0-100}}`. The device runs the command the next time it checks in.

### Emergency message on every screen
`GET /v1/emergency-templates` lists the stored templates. `POST /v1/emergencies/from-template/{templateId}` with `{}` fires one as stored, or send `scopeKind` and `expiresAt` to override its scope and end time. Clear it with `POST /v1/emergencies/{id}/clear`. Emergencies take over real screens, so always confirm with the user first.

### Proof of play
`GET /v1/proof?from=2026-10-01T00:00:00Z&to=2026-10-19T00:00:00Z` returns what played, where and for how long, broken down by content and by screen. Add `screenId=` to look at one screen.

## Rules

- Reading is safe. Before any call that changes real screens (assign, cast, emergency, reboot), tell the user what will change and on which screens.
- A key never has more permissions than the person who created it. A `403` means the key lacks the permission named in the error, so ask the user to add it rather than retry.
- Something in another workspace returns `404`, not `403`.

## Prefer MCP?

Brix also runs a hosted MCP server at `https://api.brixsignage.com/v1/mcp` with OAuth sign-in. It works in Claude, ChatGPT and other MCP clients. Setup: https://brixsignage.com/developers/mcp/
