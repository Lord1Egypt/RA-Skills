# Runtime Notes

## Controller Discovery

The script does not depend on one machine's fixed group names. It discovers the current Clash controller in this order:

- explicit `--unix-socket` or `--controller-url`
- environment variables `CLASH_API_UNIX_SOCKET`, `CLASH_API_URL`, `CLASH_API_SECRET`
- local Clash config values such as `external-controller-unix`, `external-controller`, and `secret`

The bundled script treats `set-your-secret` as an unset placeholder and avoids sending it.

## Group Discovery Rules

When `--group` is not provided, the script discovers target groups from the live `/proxies` response:

- `current`: follow the currently selected chain and optimize selector groups that are actively selected
- `top-level`: optimize selector groups that are not nested under another selector or load-balance helper group
- `all`: optimize every selector group except `GLOBAL`

This keeps the skill generic across different subscriptions and naming schemes.

## Scheduling

The bundled `launchd` installer requires `--interval-minutes N`, so the user chooses the execution interval at install time instead of inheriting a fixed 30-minute schedule.
