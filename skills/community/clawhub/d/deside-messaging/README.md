# Deside Messaging Skill Bundle

This directory is the canonical source bundle for the Deside Messaging skill.

It is designed as an Agent Skills-compatible bundle that teaches agents how to
use the public Deside MCP server.

## Files

1. `SKILL.md` — primary skill artifact
2. `README.md` — short operator notes for this bundle

This bundle can be distributed through channels such as ClawHub, but the bundle
itself remains the source of truth.

## Current Scope

This first release teaches these public MCP tools:

1. `send_dm`
2. `read_dms`
3. `mark_dm_read`
4. `list_conversations`
5. `get_user_info`
6. `get_my_identity`
7. `search_agents`

`mark_dm_read` is included as the MCP read-ack mutation. Its inclusion here does
not claim that every downstream read-receipt UX is fully validated end-to-end.

## Public Endpoints

1. MCP endpoint: `https://mcp.deside.io/mcp`
2. OAuth metadata: `https://mcp.deside.io/.well-known/oauth-authorization-server`
3. Protected resource metadata: `https://mcp.deside.io/.well-known/oauth-protected-resource/mcp`

## Canonical References

When editing this source bundle in the repository, use these as the source of truth:

1. `../../docs/authentication.md`
2. `../../docs/tools.md`
3. `../../docs/error-handling.md`
4. `../../examples/mini-agent/`

## Contract Boundaries

This bundle is intentionally narrow.

Included:

1. wallet-to-wallet DMs
2. conversation history
3. public identity lookup
4. agent directory search
5. realtime DM notifications via MCP when the session stays open

Not included:

1. groups
2. `presence`
3. `typing`
4. push-only assumptions or guaranteed realtime delivery wording
5. REST wrappers or `openclaw.json`

## Testing Reference

The working public hello-world flow is the mini-agent example:

1. initialize MCP session
2. send `notifications/initialized`
3. complete OAuth 2.0 + PKCE
4. call MCP tools with bearer token + `mcp-session-id`
5. if the session stays open, optionally handle `notifications/dm_received`

Core delivery model for the skill:

1. send with `send_dm`
2. after the first authenticated tool call binds wallet auth to the MCP session, receive realtime updates with `notifications/dm_received`
3. resync with `list_conversations` + `read_dms` when needed

Operational note:

1. MCP OAuth auth does not by itself create a registered Deside user profile
2. if you want the wallet to behave as a normal registered participant with the Deside app/front, use a wallet already onboarded in Deside

History pagination note:

1. `read_dms` is `newest-first`
2. `before_seq` pages backward to older messages
3. `nextCursor` currently comes back as a string cursor carrying the oldest `seq` in the page
4. pass `Number(nextCursor)` into the next `before_seq`
5. chat UIs that want chronological rendering should reorder locally before painting

Relevant files:

1. `../../examples/mini-agent/README.md`
2. `../../examples/mini-agent/mini-agent.js`

## Installation Channels

Validated channels:

1. ClawHub:
   - `clawhub install deside-messaging`
2. Agent Skills CLI from the public GitHub repo:
   - `npx skills add https://github.com/DesideApp/deside-mcp --skill deside-messaging`
3. Agent Skills CLI from a local path:
   - `npx skills add /path/to/deside-mcp --skill deside-messaging`

Portable/manual channel:

1. copy this directory into a compatible skills folder as:
   - `skills/deside-messaging/`

Both the public GitHub repo path and the local path have been smoke-tested for
this bundle.

## Publishing Rule

Do not publish this skill to ClawHub until:

1. `SKILL.md` and `README.md` agree
2. the skill wording matches the public MCP contract
3. a real smoke has passed
4. the public listing text does not overstate the current scope
