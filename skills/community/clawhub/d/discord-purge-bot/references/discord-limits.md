# Discord Cleanup Limits

## Required Permissions

- `VIEW_CHANNEL`
- `READ_MESSAGE_HISTORY`
- `MANAGE_MESSAGES` for deleting others' messages
- `MANAGE_CHANNELS` for channel recreation (`purge-nuke.mjs`)

## Core Endpoints

- List messages: `GET /channels/{channel.id}/messages`
- Delete one message: `DELETE /channels/{channel.id}/messages/{message.id}`
- Bulk delete: `POST /channels/{channel.id}/messages/bulk-delete`
- Get channel: `GET /channels/{channel.id}`
- Create guild channel: `POST /guilds/{guild.id}/channels`
- Delete channel: `DELETE /channels/{channel.id}`

## Bulk Delete Rules

- Works only in guild channels.
- Message count per request: 2 to 100 IDs.
- Rejects messages older than 2 weeks.
- Rejects duplicate IDs in the same request.

## Rate Limit Rules

- Never hard-code limits.
- Respect `429` and use `Retry-After` or `retry_after`.
- Use `X-RateLimit-*` headers to avoid bursts.
- Expect global and per-route buckets.

## Operational Guidance

- Always run preview before destructive execution.
- Split delete plan into recent (bulk) and old (single).
- Persist results and errors in JSON artifacts.
- Use bounded scans (`max-scan`) for large channels.
