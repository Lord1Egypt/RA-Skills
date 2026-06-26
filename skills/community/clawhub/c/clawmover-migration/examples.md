# Examples

## Installation Check

User:

`Check whether ClawMover is installed on this machine`

Expected behavior:

- run `clawmover --version`
- if missing, explain that `@clawmover/cli` can be installed after confirmation

## Backup

User:

`Back up this OpenClaw machine`

Expected behavior:

- ask for `instanceId` if missing
- ask for confirmation before installing the CLI if needed
- prefer the two-step non-interactive verification flow

## Simulated Restore

User:

`Restore this migration to /tmp/restore-check first`

Expected behavior:

- treat this as simulated restore
- use `--dest-path`
- explain that real restore can be done later

## Real Restore

User:

`Restore this migration onto this machine now`

Expected behavior:

- warn that this can modify the live OpenClaw environment
- request explicit confirmation
- only then proceed without `--dest-path`
