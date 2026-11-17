---
name: manage-channels
description: List connected social media channels and check their health via BulkPublish. Use when the user asks about their connected accounts.
---

# BulkPublish — Channels Reference

## Tools

| Tool | Use for | Key params |
|---|---|---|
| `list_channels` | All connected accounts with IDs and status | none |
| `get_channel_health` | Token validity and connection issues | `channelId` |
| `get_channel_options` | Platform-specific options | `channelId` |
| `search_mentions` | Find @mention usernames | `channelId`, `query` |

## list_channels response shape

Each channel: `id`, `platform`, `accountName`, `accountId`, `accountType`, `isActive`, `tokenStatus` ("valid"/"expiring_soon"/"expired"), `tokenExpiresAt`.

## Platform names (used in channels and create_post)

`facebook`, `instagram`, `x`, `linkedin`, `tiktok`, `youtube`, `pinterest`, `threads`, `bluesky`, `gmb`, `mastodon`, `discord`, `telegram`, `tumblr`, `snapchat`

## Channel options by platform

| Platform | get_channel_options returns |
|---|---|
| Pinterest | Available boards |
| YouTube | Playlists, categories |
| Instagram | Eligible collaborators |

## Channel Sets (REST API)

Saved channel groups for one-click targeting. MCP tools: `list_channel_sets`, `create_channel_set`, `update_channel_set`, `delete_channel_set`. The REST API uses `Authorization: Bearer bp_your_key`, base `https://app.bulkpublish.com`:

| Endpoint | Use for |
|---|---|
| `GET /api/channel-sets` | List sets (ordered by name) |
| `POST /api/channel-sets` | Create — body `{name, channelIds}` |
| `PUT /api/channel-sets/{id}` | Rename or change channels — body `{name?, channelIds?}` (send at least one) |
| `DELETE /api/channel-sets/{id}` | Delete → `{success: true}` |

- Set object: `id`, `name`, `channelIds` (number[]), `createdAt`, `updatedAt`
- `name` is trimmed, max 100 chars, unique per organization — a duplicate name returns **409** with `error.code: "DUPLICATE_NAME"`
- `channelIds` needs at least 1 id; every id must belong to your org (get them from `list_channels`)
- Max **50 sets per org** — creating beyond that returns 400
- To target a set when creating a post, fetch it and pass its `channelIds` — sets are expanded client-side; `create_post` still takes `channels` pairs

## Notes

- Channels can only be connected/reconnected via the web UI (OAuth) — not via API
- LinkedIn channels are either a personal profile or a company page (`accountType`: `personal` / `organization`); both are connected in the dashboard and posted to like any other channel. They run on separate LinkedIn apps and are gated separately — `list_platforms` reports pages under `variants.organization`, so check that (not the platform-level state) before telling a user they can connect a company page
- `search_mentions` works on X/Twitter, Bluesky, Mastodon and LinkedIn (on LinkedIn the query is a Page's URL slug, exact match; on Mastodon each handle is `@username` for the same server or `@username@domain` for another, and a full `username@domain` query finds accounts the server has not seen yet)
- Token "expired" means the user needs to reconnect at app.bulkpublish.com/channels
