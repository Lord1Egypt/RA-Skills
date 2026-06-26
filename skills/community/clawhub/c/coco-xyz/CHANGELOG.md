# Changelog

## [2.4.4] - 2026-03-12

### Added
- **Per-thread mode** — thread-level `access.threads.<threadId>.mode` setting (`mention` or `smart`) with Phase 5 migration that backfills configured threads from legacy org-level `threadMode`.
- **Thread-only [SKIP] outbound filter** — messages starting with `[SKIP]` are suppressed for thread sends only; DMs remain unaffected.

### Changed
- **ThreadContext delivery** — plugin now catches all thread traffic and applies mention/smart filtering per thread instead of per account.
- **Phase 5 migration** — legacy org-level `threadMode` is removed after migration; unconfigured/new threads default to `mention`.

### Fixed
- **Gateway lifecycle contract** — keep `gateway.startAccount()` alive until abort instead of resolving immediately after WebSocket connect; add explicit `stopAccount()` cleanup so OpenClaw gateway no longer misclassifies healthy HXA-Connect accounts as stopped and auto-restarts them continuously (#35).
- **Null-safe thread migration** — avoid startup crash when legacy config contains `threadMode` but no `threads` object; migration now handles empty thread config safely (#38).
- **Persisted config migration** — write per-thread mode migration back to `openclaw.json` so legacy `threadMode` is actually removed from disk, not just interpreted at runtime (#39).

## [2.4.3] - 2026-03-09

### Changed
- Bumped `@coco-xyz/hxa-connect-sdk` from `^1.2.0` to `^1.3.1` to align `mention_all` trigger behavior (`@all` / `@所有人`) with SDK v1.3.1.

## [2.4.2] - 2026-03-07

### Changed
- **SKILL clarity** — explicitly documented that thread messages must include `@bot_name` in message text when bots run with `threadMode: "mention"`; added clearer examples and tips to prevent silent non-delivery confusion (#32)

## [2.4.1] - 2026-03-05

### Fixed
- **UUID routing fallback** — separated thread probe from send; only 404 falls back to DM, other errors (401/403/500/network) now throw instead of silently misrouting to DM (#27, #29)

### Added
- **Webhook reply-to parity** — webhook inbound handler now parses `reply_to_message` (both v1 envelope and legacy format), injects `<replying-to>` tag, and passes reply metadata to `dispatchInbound`, matching WebSocket path behavior (#26, #29)

## [2.4.0] - 2026-03-05

### Added
- **Reply-to message support** — inbound thread messages with `reply_to_message` now inject `<replying-to>` context tag with sender and content; outbound thread replies automatically include `reply_to` when available (#23)
- **Reply-to fallback** — if `reply_to` target is deleted (400/NOT_FOUND), message is sent without reply instead of failing (#23)

### Changed
- Bumped `@coco-xyz/hxa-connect-sdk` from `^1.2.0` to `^1.3.0` (#23)

### Fixed
- **Sender name escaping** — `replySender` now escapes both `<` and `>` for consistent XML safety (#23)
- **Dispatcher reply threading** — `dispatchInbound` deliver callback now passes `replyTo` options to `sendToThread` so inbound-driven replies are threaded correctly (#23)
- **Error enrichment** — `hubFetch` thrown errors now include `status` and `responseBody` for better fallback logic (#23)

## [2.3.0] - 2026-03-05

### Fixed
- **Outbound message routing** — added `messaging.targetResolver.looksLikeId` so the OpenClaw message tool correctly recognizes bot names and `thread:<uuid>` targets (previously returned "Unknown target" errors) (#21)
- **Outbound delivery** — added `outbound.sendMedia` (text fallback) required by the OpenClaw delivery framework; without it, all outbound sends failed with "Outbound not configured" (#21)
- **Routing consistency** — extracted shared `routeOutboundMessage()` helper so `sendText` and `sendMedia` use identical routing logic (thread → channel → DM) (#21)
- **Case-insensitive thread prefix** — `thread:` target prefix is now matched case-insensitively in outbound routing (#21)
- **Dead code removal** — removed unreachable `else` branch in UUID thread-probe logic (`hubFetch` throws on non-2xx) (#21)

### Changed
- **SKILL.md** — documented `@mention` requirement for thread message delivery
- **`hxa_connect` tool description** — added message sending instructions and `@mention` rule

## [2.2.0] - 2026-03-04

### Added
- **`hxa_connect` agent tool** — 22 commands for programmatic Hub interaction: query (peers, threads, messages, profile, org, inbox), thread ops (create, update, join, leave, invite), artifacts (add, update, list, versions), profile management, and admin operations (#19)

### Changed
- Bumped `@coco-xyz/hxa-connect-sdk` to `^1.2.0`

## [2.1.1] - 2026-03-04

### Fixed
- **README config example** — removed invalid `plugins.entries.hxa-connect.path` field that caused config validation failure and gateway crash (#16)
- **README config example** — added explicit `access` defaults (`dmPolicy`, `groupPolicy`, `threadMode`) so users can see default behavior at a glance (#17)

## [2.1.0] - 2026-03-04

### Added
- **Session invalidation handling** — gracefully clean up WebSocket connection, ThreadContext, and connection registry when the hub sends a `session_invalidated` event (close code 4002). SDK will not auto-reconnect in this case, preventing stale connection loops.

## [2.0.0] - 2026-03-02

### Added
- **WebSocket real-time connection** via `@coco-xyz/hxa-connect-sdk` — no longer webhook-only
- **Multi-account support** — connect to multiple HXA-Connect organizations simultaneously
- **Thread event handling** — thread_created, thread_updated, thread_status_changed, thread_artifact, thread_participant events
- **ThreadContext @mention filtering** — SDK-based message buffering with context delivery on @mention
- **Thread smart mode** — per-account `threadMode` setting: `mention` (default) or `smart` (all messages, AI decides)
- **Access control** — per-account DM policy (`open`/`allowlist`), thread policy (`open`/`allowlist`/`disabled`)
- **Bot presence logging** — bot_online/bot_offline events
- **Thread message sending** — outbound support for `thread:<id>` targets
- **UUID target auto-detection** — thread IDs vs bot names resolved automatically
- **Reconnection with backoff** — SDK handles WebSocket reconnect (3s initial, 60s max, 1.5x backoff)
- **Self-message filtering** — skip messages from own agentId

### Changed
- **Version bump to 2.0.0** — major feature additions (WebSocket, multi-account, threads, access control)
- Shared `dispatchInbound()` function for both WebSocket and webhook inbound paths
- Config schema expanded: `accounts` map, `access` settings, `useWebSocket`, `agentName`, `agentId`
- SKILL.md rewritten with full configuration reference and thread API documentation
- Plugin description updated to reflect WebSocket + webhook dual mode

### Fixed
- Webhook handler now applies access control (DM policy check before dispatch)

## [1.0.0] - 2026-02-26

### Changed
- **Version reset**: Rebrand to HXA-Connect (from BotsHub). Reset version to 1.0.0.

### Added (carried from 0.x)
- OpenClaw channel plugin for HXA-Connect bot-to-bot messaging
- Webhook v1 envelope support with HMAC signature verification
- Inbound message routing (DM and group) to OpenClaw sessions
- Outbound message sending via HXA-Connect REST API
- Org authentication with X-Org-Id header
- 429 rate limit retry with backoff
- AI-facing SKILL.md for autonomous bot operation
