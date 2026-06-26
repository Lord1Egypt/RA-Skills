---
name: apm_session_start
description: "Inject APM (Agent Progressive Memory) bootstrap context per chat type — DM uses memory/main/*, group chat uses memory/groups/{name}.md. Channel-agnostic (Matrix / Telegram / Slack / Discord)."
metadata: |
  {
    "openclaw": {
      "export": "handler",
      "events": ["agent:bootstrap"]
    }
  }
---

# apm_session_start Hook (chat-type aware, channel-agnostic)

Auto-loads the right APM memory context per chat type and injects a synthetic
bootstrap file. Solves two problems:

1. **DRY** — Agent never has to remember to load memory on the first turn.
2. **Privacy** — Group chats **MUST NOT** receive DM-only memory
   (`MEMORY.md`, `memory/main/*`, `memory/YYYY-MM-DD.md`).

## Supported Channels

The hook is channel-agnostic for chat-type detection. The sessionKey patterns
below are handled uniformly:

| Channel  | DM pattern                            | Group pattern                          |
|----------|---------------------------------------|----------------------------------------|
| Matrix   | `agent:<id>:matrix:direct:<room>`     | `agent:<id>:matrix:channel:<room>`     |
| Telegram | `agent:<id>:telegram:<direct\|group>:<chat_id>` | (Telegram only has `group` for groups) |
| Slack    | `agent:<id>:slack:direct:<user_id>`   | `agent:<id>:slack:channel:<channel_id>` |
| Discord  | `agent:<id>:discord:direct:<user_id>` | `agent:<id>:discord:channel:<guild_id>` |

**Matrix is the primary supported channel.** Other channels are handled by
the same chat-type detection logic but require operators to populate
`memory/groups/group_names.json` with channel-appropriate keys (see
[Group-Name Resolution](#group-name-resolution) below).

## Chat-Type Detection

`agent:bootstrap` event context does **not** include `chatType`. The hook
parses `event.sessionKey` to derive it:

| Token in sessionKey | Detected  | Action                |
|---------------------|-----------|-----------------------|
| `:direct:`          | `direct`  | DM protocol           |
| `:channel:`         | `channel` | Group protocol        |
| `:group:`           | `channel` | Group protocol (Telegram alias) |
| `:subagent:`        | `subagent`| Skip (renderer filters anyway)   |
| `cron:` / `:cron-*` | `cron`    | Skip                  |
| anything else       | `unknown` | DM protocol + warn    |

## Behavior (7 steps)

On every `agent:bootstrap` event:

1. **Type detection** — parse `event.sessionKey` → `chatType`
2. **Scope guard** — return early if `subagent` / `cron`
3. **Empty-list guard** — skip if `context.bootstrapFiles` is empty
   (lightweight non-heartbeat runs — nothing to attach to)
4. **Chat-type branching**:
   - `channel` → resolve friendly name via `memory/groups/group_names.json`,
     then read `memory/groups/{name}.md` (L0) + `memory/groups/flush-state.json`
   - `direct` / `unknown` → read APM DM files (`memory/main/index.md` +
     attention/longterm/daily-synced + today/yesterday daily notes +
     `memory/flush-state.json`)
5. **Privacy gate (group)** — group sessions **MUST NOT** receive DM-only
   memory. The injected entry includes an explicit DO-NOT-READ block listing
   `memory/main/*`, `MEMORY.md`, and `memory/YYYY-MM-DD.md`. If group index
   is missing (first-join), inject nothing and log; AGENTS.md "First-join"
   flow handles it.
6. **Idempotency** — skip if our synthetic entry name is already in
   `bootstrapFiles` (cached per session)
7. **Push** a synthetic entry to `context.bootstrapFiles`

## Injected Entry Names

| Chat Type | Entry Name                   | Path                                          |
|-----------|------------------------------|-----------------------------------------------|
| DM        | `APM_SESSION_START.md`       | `memory/APM_SESSION_START.md`                 |
| Group     | `APM_GROUP_SESSION_START.md` | `memory/groups/APM_GROUP_SESSION_START.md`    |

Both names are intentionally distinct from recognized workspace basenames
(`MEMORY.md`, `AGENTS.md`, etc.) to avoid collisions with workspace templates.

## Group-Name Resolution

Group-chat sessions require `memory/groups/group_names.json` to map
**channel-specific id** → friendly name. The hook tries:

1. **Full key match** (channel-agnostic) — the raw channel id as extracted
   from `sessionKey`:
   - Matrix: `!roomId:domain.example`
   - Telegram: `<chat_id>` (e.g. `-1001234567890`)
   - Slack: `<channel_id>` (snowflake, e.g. `C0123ABCDEF`)
   - Discord: `<channel_id>` (snowflake, e.g. `123456789012345678`)
2. **Matrix-only fallback** — strip `:domain` suffix and try `!roomId`.
   (Other channels' ids don't contain `:`, so this is a no-op for them.)

If neither matches → **log warning + fall back to DM protocol** (NOT
RECOMMENDED — private memory may leak). Operators should add the missing
mapping before relying on this fallback.

### Expected `group_names.json` shape

```json
{
  "<channel_id_key>": {
    "name": "<friendly_name>",
    "channel": "matrix|telegram|slack|discord"
  }
}
```

Example for a multi-channel workspace:

```json
{
  "!roomId1:matrix.example.com": { "name": "team-alpha", "channel": "matrix" },
  "-1001234567890":              { "name": "team-alpha-tg", "channel": "telegram" },
  "C0123ABCDEF":                 { "name": "team-alpha-slack", "channel": "slack" }
}
```

## Token Caps

| Constant | Value | Reason |
|----------|-------|--------|
| `APM_MAX_TOTAL_CHARS` | 12000 | Stay well under bootstrap total limit |
| `DAILY_NOTE_MAX_CHARS` | 6000 | Per-day cap for today/yesterday daily notes |
| `FILE_READ_MAX_CHARS` | 30000 | Per-file read cap for non-daily files |

If exceeded, the relevant section is truncated with an explicit
`[... truncated at N chars; original M chars at PATH]` marker.

## Configuration

| Item | Value |
|------|-------|
| Hook event | `agent:bootstrap` |
| Hook path | `~/.openclaw/hooks/apm_session_start/` |
| Trigger | Every agent run (one shot per session) |

## Installation

```bash
# From skill directory:
cp -r hooks/apm_session_start/ ~/.openclaw/hooks/apm_session_start/
```

### Post-install Structure

```
~/.openclaw/hooks/apm_session_start/
├── HOOK.md
└── handler.js
```

## Why

AGENTS.md mandates:

- **DM**: APM 1.6.0 protocol — load `memory/main/index.md` first, then up
  to 2 P-files on-demand
- **Group**: Progressive Disclosure Protocol — only `memory/groups/{name}.md`
  is the legal entry; everything else loads on-demand per the L0 routing
  table; **never** read `MEMORY.md` or `memory/YYYY-MM-DD.md` in group chat

Without chat-type awareness the hook would inject DM context into group
sessions — a privacy violation. This hook respects the group protocol by
default.

## Idempotency Notes

- `applyBootstrapHookOverrides` fires the hook on every agent turn, but
  `bootstrapFiles` is cached per session. Once the synthetic entry is
  pushed, subsequent turns see it and skip.
- For `lightweight + heartbeat` runs the renderer strips non-`HEARTBEAT.md`
  entries later in the pipeline, so injecting APM context there wastes
  tokens. We skip those runs up-front via the empty-list guard.

## Known Limitations

1. **`MEMORY.md` is still injected by OpenClaw as a workspace bootstrap file**
   in group sessions (the hook cannot filter it out — that requires a
   separate change in OpenClaw's `loadWorkspaceBootstrapFiles`). The
   injected entry includes an explicit DO-NOT-READ warning; rely on agent
   discipline until OpenClaw-level filtering lands.
2. **`chatType === 'unknown'` falls back to DM.** If OpenClaw adds new
   sessionKey formats in the future, update `detectChatTypeFromSessionKey`.
   The handler logs a warning for unrecognized patterns.
3. **Group-name resolution depends on operator-configured
   `group_names.json`.** New channels must add their key format to
   `resolveGroupName` and document it above.

## Related

- `AGENTS.md` — "Every Session" → APM DM Progressive Loading + Progressive Disclosure Protocol
- `memory/main/index.md` — DM APM routing table (L0)
- `memory/groups/group_names.json` — channel id → friendly name map
- `memory/groups/{name}.md` — per-group L0 entry (only legal entry for groups)
- `memory/groups/flush-state.json` — group-only flush state (NOT memory/flush-state.json)
- OpenClaw docs: `/automation/hooks`, `/plugins/hooks`
