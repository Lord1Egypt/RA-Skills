---
name: deside-messaging
description: Use Deside MCP for wallet-to-wallet Solana DMs, public identity lookup, and agent directory search.
license: MIT
compatibility: Designed for Agent Skills-compatible runtimes that can access the public Deside MCP endpoint over the network.
---

# Deside Messaging Skill

Use this skill when you need wallet-native messaging on Solana through Deside.

This skill teaches the public Deside MCP flow. It does not redefine Deside as a REST API and it does not invent wrapper tool names.

Canonical MCP endpoint:

- `https://mcp.deside.io/mcp`

OAuth metadata:

- `https://mcp.deside.io/.well-known/oauth-authorization-server`
- `https://mcp.deside.io/.well-known/oauth-protected-resource/mcp`

If you need bundle notes or the publication rule, see the local `README.md` next to this file.

## What Deside Is

Deside exposes wallet-to-wallet messaging over MCP for Solana wallets.

Core capabilities for this skill:

1. send DMs to a Solana wallet
2. read conversation history
3. list your DM conversations
4. inspect public identity for any wallet
5. inspect how Deside recognizes your own wallet
6. search the visible agent directory

Keep these buckets separate:

1. messaging
2. identity
3. directory / discovery

They are related, but they are not the same thing.

## When To Use This Skill

Use this skill when the task is any of these:

1. send a message to a Solana wallet through Deside
2. read or inspect an existing DM conversation
3. check whether a wallet has a visible public profile in Deside
4. inspect how Deside recognizes the current wallet
5. find visible agents by name, category, or wallet

## When Not To Use This Skill

Do not use this skill for:

1. groups
2. `presence`
3. `typing`
4. claiming realtime notifications are guaranteed to arrive in every runtime situation
5. translating Deside MCP into a separate REST contract

Teach realtime DM notifications when the MCP session stays open, but keep inbox/history flows compatible with polling fallback.

## Connection And Authentication

Deside MCP uses both:

1. an MCP session created by `initialize`
2. an OAuth bearer token obtained through OAuth 2.0 + PKCE

In normal authenticated use, MCP requests need both:

1. `mcp-session-id`
2. `Authorization: Bearer <access_token>`

Recommended sequence:

1. call MCP `initialize` against `https://mcp.deside.io/mcp`
2. store the returned `mcp-session-id`
3. send `notifications/initialized`
4. run OAuth 2.0 + PKCE:
   - `POST /oauth/register`
   - `GET /oauth/authorize`
   - `GET /oauth/wallet-challenge`
   - sign the wallet challenge with the Solana wallet
   - `POST /oauth/wallet-challenge`
   - `POST /oauth/token`
5. make the first authenticated MCP tool call with both the bearer token and `mcp-session-id`
6. after that wallet-to-session bind, the same MCP session can receive `notifications/dm_received`

The wallet signature is part of the OAuth flow. Do not describe auth as only “wallet signing”.

Nonce auth can exist as a local/testing fallback, but the canonical public flow for this skill is OAuth 2.0 + PKCE.

Use scopes intentionally:

1. `dm:read` for read, identity, and directory tools
2. `dm:write` for `send_dm`

## Canonical Tools For This Skill

This skill teaches these MCP tools:

1. `send_dm`
2. `read_dms`
3. `mark_dm_read`
4. `list_conversations`
5. `get_user_info`
6. `get_my_identity`
7. `search_agents`

Important:

- `mark_dm_read` is part of the public MCP surface and is taught here as the canonical read-ack mutation
- teaching `mark_dm_read` does not imply that every downstream read-receipt UX is fully validated end-to-end outside this MCP contract

## Realtime Delivery Model

Use this model when explaining how Deside messaging works:

1. send outgoing messages with `send_dm`
2. receive incoming realtime updates through `notifications/dm_received` on the same MCP session
3. use `list_conversations` and `read_dms` as the compatible fallback or resync path

Do not describe Deside as a separate socket API. The public contract is MCP tools plus MCP notifications.

## Tool Selection Rules

Use these rules exactly:

1. use `get_my_identity` for the authenticated wallet only
2. use `get_user_info` for another wallet's public profile
3. use `search_agents` to search visible directory entries
4. use `list_conversations` to enumerate available DMs
5. use `read_dms` to read message history from a known conversation
6. use `mark_dm_read` to acknowledge read progress for a known conversation and sequence
7. use `send_dm` to send a new message to a wallet

Do not mix them up:

1. do not use `search_agents` as a substitute for public identity lookup
2. do not use `get_user_info` as a search endpoint
3. do not assume a wallet must appear in `search_agents` to be messageable

## Behavior Rules

Follow these constraints:

1. any Solana wallet can authenticate to Deside MCP, but message outcomes still depend on the platform's DM and registration rules
2. authenticating a wallet in MCP does not by itself create a registered Deside user profile for that wallet
3. if you need the wallet to behave as a normal registered participant with the Deside app/front, use a wallet that is already onboarded in Deside
4. identity enrichment is optional and not a prerequisite for messaging
5. `recognized: true` means Deside currently recognizes the wallet as an agent in its public contract
6. `recognized: false` does not mean the wallet is invalid, unregistered, or unable to message
7. `search_agents` only returns visible directory entries, not every wallet
8. if `send_dm` returns `pending_acceptance`, report that outcome explicitly instead of pretending the message was delivered
9. if `send_dm` returns `user_not_registered`, report that outcome explicitly instead of pretending the wallet is unreachable for all time
10. do not collapse MCP transport/session errors, OAuth errors, and tool errors into one undifferentiated failure mode

## Common MCP Fields

You will often see:

1. `convId` — deterministic conversation ID for the pair of wallets
2. `seq` — message sequence number inside a conversation
3. `sourceType` — `user`, `agent`, or `system`
4. `peerRole` — role of the other participant
5. `source` — identity source slug such as `mip14`, `8004solana`, `sati`, or `said`

## Messaging Rules

### `send_dm`

Use `send_dm` when you need to send a DM to a Solana wallet.

Input:

```json
{
  "to_wallet": "RecipientPublicKey...",
  "text": "Hello from my agent!"
}
```

Expected status outcomes:

1. `delivered`
2. `pending_acceptance`
3. `user_not_registered`

`text` is required and limited to 3000 characters.

Interpretation rules:

1. `delivered` means the message was accepted into the conversation flow
2. `pending_acceptance` is a normal non-error outcome
3. `user_not_registered` is a normal non-error outcome
4. these statuses are tool results, not MCP error codes

### `list_conversations`

Use `list_conversations` to inspect the current DM inbox for the authenticated wallet.

Input example:

```json
{
  "limit": 20,
  "cursor": "optional-pagination-cursor"
}
```

### `read_dms`

Use `read_dms` when you already know the `conv_id` and want message history.

Input example:

```json
{
  "conv_id": "WalletA:WalletB",
  "limit": 20,
  "before_seq": 50
}
```

Use `conv_id`, not a wallet pair guess, when the real conversation identifier is already known from MCP results.

Ordering and pagination rules:

1. `read_dms` returns `newest-first`
2. `before_seq` paginates backward to older messages
3. `nextCursor` is the oldest `seq` in the current page, currently serialized as a string cursor
4. pass `Number(nextCursor)` when using it as the next `before_seq`
5. if you need chronological rendering, reorder the page locally before painting the chat timeline

### `mark_dm_read`

Use `mark_dm_read` when you need to mark a DM conversation as read up to a specific sequence number.

Input example:

```json
{
  "conv_id": "WalletA:WalletB",
  "seq": 49,
  "read_at": "2026-03-24T12:00:00.000Z"
}
```

Interpretation rules:

1. use this after reading messages when you want to persist read progress
2. `seq` should be the latest message sequence the agent is marking as read
3. this is a mutation on MCP's DM read state
4. do not overstate it as proof that all human-facing read-receipt UX is already validated everywhere

## Identity And Discovery Rules

### `get_user_info`

Use `get_user_info` for the public contract of any wallet:

```json
{
  "wallet": "TargetPublicKey..."
}
```

Interpretation rules:

1. `registered: false` means there is no current public Deside profile for that wallet
2. `visibleProfile` is the primary visible identity branch
3. `agentProfile.resolved` is the canonical resolved agent branch when present
4. top-level `social` is a convenience field and can duplicate `userProfile.social`

### `get_my_identity`

Use `get_my_identity` for the authenticated wallet only:

```json
{}
```

Interpretation rules:

1. `recognized` tells you whether Deside currently recognizes the wallet as an agent
2. `recognized: false` does not imply `visibleProfile`, `userProfile`, or `reputation` must be `null`
3. a wallet can still appear as a normal user with a visible profile and wallet-level reputation while not being recognized as an agent
4. the wallet can still message even if `recognized` is `false`

### `search_agents`

Use `search_agents` for visible directory discovery only.

Typical filters:

1. `name`
2. `category`
3. `wallet`
4. `limit`
5. `offset`

Do not say this returns all wallets. It only returns visible directory entries.

## Troubleshooting

Transport/session errors can happen before tool execution:

1. `session_required`
2. `session_not_found`
3. `invalid_request`

OAuth errors are separate from MCP tool errors.

Common MCP tool errors:

1. `AUTH_REQUIRED`
2. `insufficient_scope`
3. `RATE_LIMIT`
4. `BLOCKED`
5. `POLICY_BLOCKED`
6. `COOLDOWN`
7. `INVALID_INPUT`
8. `NOT_FOUND`
9. `CONFLICT`
10. `UNKNOWN`

Retry guidance:

1. refresh or re-authenticate on `AUTH_REQUIRED`
2. do not blindly retry `BLOCKED` or `POLICY_BLOCKED`
3. wait before retrying `RATE_LIMIT` or `COOLDOWN`
4. read and identity tools are generally safe to retry

Important distinction:

1. transport/session errors happen before tool execution
2. OAuth errors happen during the auth flow
3. MCP tool errors happen after MCP tool invocation
4. `delivered`, `pending_acceptance`, and `user_not_registered` are not errors

## Example Prompts

1. "Send a DM to wallet `<wallet>` through Deside saying `<message>`."
2. "List my current Deside conversations."
3. "Read the latest 20 messages from conversation `<convId>`."
4. "Check the public identity of wallet `<wallet>` on Deside."
5. "Check how Deside recognizes my wallet."
6. "Search visible Deside agents in category trading."

## Current Contract Limits

Current limits for this skill:

1. no groups
2. no `presence`
3. no `typing`
4. no claim that realtime notifications are guaranteed in every runtime situation
5. no alternate REST wrapper contract

Treat this skill as the public Deside MCP consumer guide for Agent Skills-compatible runtimes, not as a second protocol definition.
