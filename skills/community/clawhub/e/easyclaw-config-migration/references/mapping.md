# Migration Mapping

## Auto-migrated fields

These fields in `~/.openclaw/easyclaw.json` have clear OpenClaw equivalents and are safe to merge selectively:

- `commands.native` -> `openclaw.json.commands.native`
- `commands.nativeSkills` -> `openclaw.json.commands.nativeSkills`
- `commands.restart` -> `openclaw.json.commands.restart`
- `gateway.mode` -> `openclaw.json.gateway.mode`
- `gateway.auth.mode` -> `openclaw.json.gateway.auth.mode`
- `gateway.auth.token` -> `openclaw.json.gateway.auth.token`

## Report-only fields

These are useful to surface but should not be auto-merged by default:

- `gateway.remote.token`
  - Relevant for bridge/remote workflows but not always present in active OpenClaw config.
- `meta.*`
  - Historical bookkeeping, not functional runtime config.

## Desktop-only / no direct equivalent

These usually come from `~/Library/Application Support/@cfmind/easyclaw/easyclaw.json` and should be reported, not migrated:

- `app.language`
- `app.autoStart`
- `app.minimizeToTray`
- `app.theme`
- `window.*`
- `analytics.*`
- `update.*`
- `firstLaunch`

## Strategy

1. Prefer copying from `~/.openclaw/easyclaw.json`, not from the desktop app file.
2. Preserve existing richer OpenClaw config in `~/.openclaw/openclaw.json`.
3. Do not delete unrelated OpenClaw sections.
4. Back up before writing.
