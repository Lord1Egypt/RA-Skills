# APM — Hooks Overview

This skill ships **three OpenClaw hooks** that automate the APM memory
lifecycle. Each hook has its own `HOOK.md` with full details; this file is
the entry point and contains only the overview, shared conventions, and
installation instructions.

## Hook Index

| Hook | Event | Purpose | Full docs |
|------|-------|---------|-----------|
| `apm_session_start` | `agent:bootstrap` | Auto-inject APM context per chat type (DM vs group, channel-agnostic) | [`hooks/apm_session_start/HOOK.md`](hooks/apm_session_start/HOOK.md) |
| `remem-flush` | `message:received`, `system:event` | Manual flush on `/remem` (user or cron) | [`hooks/remem-flush/HOOK.md`](hooks/remem-flush/HOOK.md) |
| `precompact-remem` | `session:compact:before` | Auto-flush before context is lost | [`hooks/precompact-remem/HOOK.md`](hooks/precompact-remem/HOOK.md) |

## Shipped Files

```
hooks/
├── apm_session_start/
│   ├── HOOK.md
│   └── handler.js
├── remem-flush/
│   ├── HOOK.md
│   └── handler.js
└── precompact-remem/
    ├── HOOK.md
    └── handler.js
```

## Channel Compatibility

All three hooks are **channel-agnostic at the chat-type level** (DM vs
group). `apm_session_start` additionally detects multiple channel
sessionKey patterns:

| Channel  | DM | Group | Notes |
|----------|----|----|-------|
| Matrix   | ✅ | ✅ | First-class; full + room-only key matching |
| Telegram | ✅ | ✅ | chat_id as key (negative for groups) |
| Slack    | ✅ | ✅ | channel_id snowflake as key |
| Discord  | ✅ | ✅ | channel_id snowflake as key |

To add a new channel, update `detectChatTypeFromSessionKey` in
`hooks/apm_session_start/handler.js` and document the key format in
`hooks/apm_session_start/HOOK.md`.

## Installation

Install all three hooks in one go:

```bash
SKILL_DIR=~/.openclaw/workspace/skills/apm-agent-progressive-memory
HOOKS_DIR=~/.openclaw/hooks

cp -r "$SKILL_DIR/hooks/apm_session_start/"   "$HOOKS_DIR/"
cp -r "$SKILL_DIR/hooks/remem-flush/"          "$HOOKS_DIR/"
cp -r "$SKILL_DIR/hooks/precompact-remem/"     "$HOOKS_DIR/"

# Avoid double-flush with the built-in memory-flush hook
openclaw hooks disable memory-flush

# Enable precompact (apm_session_start and remem-flush are auto-loaded)
openclaw hooks enable precompact-remem
```

## Verification

After installation, verify all three handlers load:

```bash
# Each handler should parse and export { handler } without error
for hook in apm_session_start remem-flush precompact-remem; do
  node -e "require('./hooks/$hook/handler.js'); console.log('$hook OK')"
done
```

## Hook Interaction

```
agent run start
   │
   ▼
agent:bootstrap event
   │
   ├─► apm_session_start  ──► injects APM_SESSION_START.md (DM)
   │                       or APM_GROUP_SESSION_START.md (group)
   │
   ▼
agent responds to user
   │
   ▼
user sends /remem (or cron fires /remem)
   │
   ├─► remem-flush        ──► records mtime deltas in
   │                          memory/flush-state.json (DM) OR
   │                          memory/groups/flush-state.json (group)
   │
   ▼
... session continues ...
   │
   ▼
context near limit OR session idle
   │
   ├─► precompact-remem   ──► records mtime deltas in
   │                          memory/flush-state.json (DM) OR
   │                          memory/groups/flush-state.json (group)
   │
   ▼
session:compact fires
```

## Shared Conventions

### flush-state.json Shape

All three hooks read/write `memory/flush-state.json` (DM) and may
also read `memory/groups/flush-state.json` (group). See
[`ADDENDUM.md`](ADDENDUM.md) for the full schema.

### mtime-based Deltas

`remem-flush` and `precompact-remem` use file mtime to detect
changes since last flush. They preserve prior `_mtime` keys in
`flush-state.json` so unchanged files don't trigger re-flushes.

### Idempotency

`apm_session_start` is idempotent per session (cached in
`bootstrapFiles`). `remem-flush` and `precompact-remem` write to
`flush-state.json` but use mtime gating to avoid re-stamping
unchanged files.

## OpenClaw Built-ins to Disable

| Built-in hook | Why disable |
|---------------|-------------|
| `memory-flush` | Listens to `/new` (not `/remem`); fires too late (after context is lost) |

```bash
openclaw hooks disable memory-flush
```

## See Also

- [`SKILL.md`](SKILL.md) — core APM protocol (loading, write-back, flush triggers)
- [`ADDENDUM.md`](ADDENDUM.md) — file templates, audit rules, flush-state schema
- `hooks/<name>/HOOK.md` — full per-hook documentation
