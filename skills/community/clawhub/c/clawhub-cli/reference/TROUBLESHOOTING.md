# Troubleshooting (ClawHub CLI)

This guide helps diagnose common failures when using `clawhub` commands from an agent session.

## First Step (Always)

Capture:

- the exact command that was run
- the full CLI output (including the error)
- the OS + shell (PowerShell, bash, etc.)

Then re-run with the smallest possible change.

## Login / Auth Issues

### Symptom: "not logged in" / "unauthorized"

Actions:

- run `clawhub login` (interactive), or
- run `clawhub login --token <api-token>`

If still failing:

- verify the token is valid and not expired
- verify the token has permission to publish/sync (if relevant)

## Publish Conflicts

### Symptom: slug already exists

Actions:

- pick a new slug (recommended), or
- publish under a different namespace if the CLI supports it (check `clawhub publish --help`)

### Symptom: version already exists / version conflict

Actions:

- bump patch/minor/major depending on change magnitude
- re-run publish with the new SemVer

## Install / Update Issues

### Symptom: cannot resolve / network / timeout

Actions:

- retry once (transient network)
- verify corporate proxy/VPN settings
- try a different network

### Symptom: installed version is not what you expected

Actions:

- run `clawhub list` to see what is pinned
- install/update with `--version <semver>` to force a specific version

## Sync Issues

### Symptom: sync would upload too much / unexpected files

Actions:

- use `--dry-run` if supported
- remove secrets and large artifacts from skill folders
- keep skill folders minimal: `SKILL.md`, `reference/`, small `scripts/`, small `assets/`

