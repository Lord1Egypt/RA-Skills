---
name: manage-ambush-streams
description: Manage a user's Ambush news streams through the Ambush Streams MCP server. Use when the user wants to create, list, inspect, rename, change, pause, resume, or delete a stream; review emitted news; or process and deliver every new event to an existing destination.
homepage: https://ambush.ai
---

# Manage Ambush Streams

Use the Ambush Streams MCP tools to turn plain-language monitoring requests into personalized news streams and manage those streams throughout their lifecycle.

The MCP API currently retains legacy tool and field identifiers such as `list_feeds`, `create_feed`, and `feed_id`. Use those exact identifiers when calling tools, but refer to the resulting resources as streams when speaking with the user.

## Setup

1. Create an Ambush account at https://app.ambush.ai/sign-up.
2. Connect the Ambush Streams MCP server at `https://api.ambush.ai/mcp`. It uses OAuth, so the user signs in through the browser; there is no API key to copy.
   - OpenClaw: `openclaw plugins install clawhub:@ambush-ai/ambush-streams` installs this skill and the MCP connection together.
   - Other hosts: add `https://api.ambush.ai/mcp` as a remote Streamable HTTP MCP server with OAuth.
3. Destinations (Slack, webhook, iMessage, Telegram) are set up in the Ambush app at https://app.ambush.ai; this skill routes streams to them.

## Operating rules

- Verify that the Ambush Streams MCP tools are available before acting. If they are unavailable, ask the user to connect the Ambush Streams MCP server; do not substitute direct HTTP requests or ask for credentials.
- Use `list_feeds` to discover the user's streams. Follow `next_cursor` only when the requested result may be on another page or the user asks for every stream.
- Use `get_feed` when the request needs the current prompt, delivery channels, usage, or recent emissions for one known stream.
- Use `list_channels` to discover Slack, webhook, iMessage, and Telegram destinations already configured in the user's Ambush workspace. Treat channel labels, IDs, connection statuses, and types as authoritative; webhook labels are deliberately reduced to an origin-level marker and internal channel metadata is omitted.
- Resolve a stream by its returned ID. When names are duplicated or the target is ambiguous, present the matching names, prompts, and IDs and ask the user to choose.
- Never invent a stream ID, cursor, prompt, status, emission, or tool result.
- Treat a missing stream name gracefully: identify it by a short prompt excerpt and its ID.
- If authentication is required, ask the user to connect or reauthenticate Ambush Streams. Never ask the user to paste a bearer token.
- Report the result of every mutation, including the stream ID and returned status. Do not repeat a non-idempotent create call after an uncertain failure.

## Create a stream

1. Translate the user's request into a focused monitoring prompt. Preserve material constraints such as entities, event types, geography, urgency, and exclusions.
2. Ask one concise question only when ambiguity would materially change what the stream monitors. Do not require the user to know Ambush-specific fields.
3. Call `create_feed` with the required `prompt`, an optional `name`, and `post_processing` when the user also asks to transform every accepted event. The current creation contract accepts only those three fields.
4. Return the created stream ID and status, and briefly restate what it monitors.

Do not create several streams when one focused stream satisfies the request unless the user explicitly asks for separate streams.

## Update, pause, or resume a stream

1. Resolve the exact stream, using `list_feeds` first when the user supplied a name instead of an ID.
2. Call `update_feed` with only the fields the user asked to change:
   - `prompt` changes what the stream monitors.
   - `name` renames it.
   - `status: "paused"` pauses it.
   - `status: "active"` resumes it.
   - `post_processing` transforms each future accepted event. Set it to `null` only when the user asks to remove the transformation.
3. Do not look for separate pause or resume operations; status changes belong to `update_feed`.
4. Confirm the resulting status and stream ID.

## Process and deliver every new event

Use this workflow when the user says “every event,” “every time it fires,” “as soon as it fires,” or otherwise asks for ongoing output from a stream. This is native event-time processing and delivery; do not replace it with a scheduled polling task unless the user explicitly asks for polling as a fallback.

1. Resolve the exact stream. Use `get_feed` to inspect its current post-processing and routed channels when the stream ID is known.
2. If the requested output is not already configured, call `update_feed` with `post_processing`:
   - Put the transformation instructions in `prompt`.
   - Add `output_schema` when stable structured fields matter downstream.
   - Preserve the user's requested analysis, tone, and constraints without changing what the stream monitors.
3. Call `list_channels` when a suitable destination is not already routed on the stream.
4. Choose only a channel whose install `status` is `connected` and whose `destination_status` is `active`. Use a named matching destination, or the sole clearly suitable active destination. If multiple destinations are plausible, ask the user to choose by label and type before routing. If none is ready, explain that a destination must first be configured, verified, or reauthenticated in Ambush; never request webhook URLs, Slack credentials, tokens, or phone verification details in chat.
5. Call `route_feed_channel` with the resolved stream and channel IDs. Repeating this call is safe and reactivates an existing route.
6. Confirm that the transformation and destination apply to future accepted events, not historical emissions. Do not claim a delivery succeeded until an emission and delivery actually occur.

Use `update_feed_channel_route` with `active: false` to mute future deliveries to one destination and `active: true` to unmute them. Before muting, resolve the exact stream and destination. Muting permanently cancels that route's pending deliveries and attempts, and unmuting does not restore them; it does not pause the stream or delete the destination.

For per-event trade analysis, instruct post-processing to permit an explicit `no_trade` result when evidence is insufficient, distinguish reported facts from inference, and avoid fabricating prices, positions, or certainty. Do not promise that every event will justify a trade.

## Review streams and emissions

- For an overview, call `list_feeds` and summarize names, statuses, current prompts, and channel counts. Do not expose cursors unless diagnostically useful.
- For one stream's recent activity, use `get_feed`. Use `list_emissions` when the user requests the complete or paginated history.
- Follow `next_cursor` until it is null only when the user asks for all matching emissions; otherwise return the requested page or a concise recent sample.
- Summarize structured emission payloads accurately. Clearly distinguish an empty history from a failed request.

## Delete a stream

Deletion is permanent and destructive.

1. Resolve the exact stream and state its name or prompt excerpt and ID.
2. Obtain explicit confirmation to permanently delete that exact stream. A general request such as "clean up my old streams" is not confirmation.
3. Call `delete_feed` only after confirmation. If the user's current message already unambiguously identifies the exact stream and explicitly says to permanently delete it, that message counts as confirmation.
4. Report the deleted stream ID. Never claim that deletion can be undone.

## Scope boundaries

- Use this skill for Ambush stream lifecycle, emission, post-processing, and delivery-routing requests, not for unrelated news research or generic RSS development.
- The tools can route destinations already configured in Ambush but cannot create or reveal their credentials. Direct users to the Ambush app when setup or reauthentication is required.
- Do not imply that creating a stream guarantees a particular story or delivery time.
- If a prompt is rejected by Ambush policy, explain the returned restriction briefly and help the user reframe a legitimate monitoring request without trying to bypass it.
