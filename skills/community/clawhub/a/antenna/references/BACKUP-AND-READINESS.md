# Plugin-native backup and restore — v1.6.9

Keep your Antenna identity, connections and saved state in an encrypted backup.
This guide covers schema-2 backups from v1.6.8 and v1.6.9.

## Commands

Stop the local OpenClaw gateway and all Antenna writers before capture or restore.
This interrupts other agents on a shared gateway; plan that interruption. The
utility checks local processes and locks but never stops or starts a service.

```bash
antenna backup create --host /absolute/openclaw.json --output /private/backups/antenna.age
antenna backup inspect /private/backups/antenna.age --json
antenna backup verify /private/backups/antenna.age
antenna backup restore /private/backups/antenna.age --host /absolute/openclaw.json
antenna backup restore /private/backups/antenna.age --host /absolute/openclaw.json --apply
```

`--host` defaults to `OPENCLAW_CONFIG_PATH`, otherwise `~/.openclaw/openclaw.json`.
Create uses the invoked companion installation; restore defaults to that installation
and accepts `--to /absolute/compatible-antenna`. Target metadata and recovery validators
must match. A readable migrated companion config/peer inventory and resolved local
JSON host config are required. Damaged reference/config files need explicit operator
repair first; this tool does not guess ownership or resolve includes/secret providers.
Inspect/verify need no active host configuration and make no operational changes.

Enter the passphrase directly at age's protected terminal prompt, never in chat.
**If you lose the passphrase, the backup cannot be recovered.** Creation prompts
for confirmation and opens the encrypted result again to verify it before saving.
An existing output is never overwritten. `--yes` skips only the restore replacement
confirmation, never passphrase entry or validation. `--json` does not expose bodies,
credentials or passphrases. No unattended unlock is supplied.

Restore without `--apply` verifies and previews changes. `--apply` asks:

> This will replace Antenna’s configuration and saved state with this backup. Changes made since the backup—including newer inbox records—will be lost. Installed program files and OpenClaw conversation history will not be changed. Continue?

## Covered state and exclusions

Covered: companion configuration, contacts, signing/exchange keys and tokens,
lists, Public Group routes/registration records, rate/replay state, retained legacy
recovery queue, Antenna plugin configuration (including policy and scanner selection),
plugin inbox/replay files, and the selected custom ruleset. Exact plugin payloads,
hold reasons, approval status and replay entries are retained; no conversion or
automatic release occurs. Bundled rules are supplied by the matching program package.

Only the Antenna plugin **config** is archived from OpenClaw. Provider credentials,
operator/hooks tokens, unrelated plugins/settings, installer paths/allowlists,
conversation history, agent memories, logs and program files are excluded. On restore,
only Antenna config and its enabled flag are changed in the current host JSON;
unrelated settings are preserved. Operator credentials must remain separate from
peer-known credentials. The plugin is left **disabled**, never auto-activated.

External referenced files are captured individually. Restored credentials are remapped
into the companion's private `secrets/` or `keys/`; plugin state and custom rules into
`state/plugin-*.json`. Original external files are not deleted or overwritten. The
preview lists mappings. Unrecognized operational files, unsafe links, invalid state
or unsupported layouts fail visibly rather than producing a partial backup.
Limits: 10,000 members, 128 MiB per file, 512 MiB total; runtime-specific inbox/rules
limits are also validated. Kernel scan slots and operation locks are not state payloads.

Replacement is verified, with temporary private displaced-state copies. Failed writes
roll back; interruption may leave `.antenna-restore-*` with `rollback.json` (absolute
local target paths) and recovery instructions. Keep services stopped and retain that
folder until recovered. It is not a permanent backup history or recovery service.

## After restore

Review restored policy, contacts, scanner selection and inbox. Use the native
Doctor and validate destinations/scanner readiness before explicitly re-enabling and
restarting. Provider configuration is not restored. Old snapshots may reintroduce
revoked permissions or forget later replay entries; there is no exactly-once guarantee.
No credential rotation, service start, message send, approval or resend is performed.

## Version compatibility and update recovery

v1.6.9 reads v1.6.8 and v1.6.9 schema-2 archives. The old v1.6.8 recovery
command does not read v1.6.9-produced archives: for rollback with the old command,
retain your pre-upgrade v1.6.8 backup. Unknown future versions are refused.
Legacy archives are rejected before any replacement. Legacy backup/restore belongs
to v1.6.7; one-way migration uses the separate
[migration kit](../plugin/OPTIONAL-KITS.md#migration).

If an update fails, leave Antenna disabled. Use compatible state and matched
packages for recovery, review Doctor and policy, then explicitly re-enable.
Never reactivate the retired relay.

The current `antenna readiness` runs native read-only Doctor checks; it does not
qualify remote peers or live ingress. Backup remains optional.
