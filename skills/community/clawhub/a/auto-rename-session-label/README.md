# Auto Rename Session Label

An OpenClaw internal **hook** (packaged for SkillHub / ClawHub) that
automatically titles new chat sessions.

When a message arrives for a session that has no title yet, the hook asks the
**same model that session is currently using** to produce a short title and
stores it as the session `label`. If anything fails (no model, timeout, upstream
error), it falls back to truncating the first user message — so a label is always
written.

## Why a hook (not a skill)?

Auto-titling must run automatically in the background on every inbound message.
That is an event-driven side effect — exactly what OpenClaw **internal hooks**
(`message:received`) are for. A skill would require the model to "decide" to run
it on every message, which is neither reliable nor efficient. This package is an
installable wrapper that drops the hook into place and enables it.

## Portable by design

No hardcoded machine paths, no personal data. At runtime it resolves:

- OpenClaw home: `OPENCLAW_HOME` env, else `~/.openclaw`
- Agent id: event context → `sessionKey` → `OPENCLAW_AGENT_ID` env → `main`
- OpenClaw `dist`: probed from the CLI/node entry and common global install
  roots, verified by the hashed `stream-*.js` bundle

It reuses OpenClaw's internal one-shot completion chain (`resolveModelAsync` →
`prepareModelForSimpleCompletion` → runtime auth → `completeSimple`) and locates
those hashed dist modules by exported-symbol name, so it survives version bumps.
If an internal symbol ever moves, the hook falls back instead of crashing.

## Install

See `SKILL.md`. In short: copy `hook/` into
`~/.openclaw/hooks/auto-rename-session-label/`, run
`openclaw hooks enable auto-rename-session-label`, reload the gateway.

## License

MIT — see `LICENSE`.
