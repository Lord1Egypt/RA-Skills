# Optional tools for v1.6.9

Your everyday kit is ready for messaging. Add diagnostics when you want to try
malicious content screening rules or test a collection of messages.

## Diagnostics

Download [antenna-diagnostics-1.6.9.tgz](https://github.com/ClawReefAntenna/antenna-diagnostics/releases/download/v1.6.9/antenna-diagnostics-1.6.9.tgz),
verify its SHA-256 against [SHA256SUMS](https://github.com/ClawReefAntenna/antenna-diagnostics/releases/download/v1.6.9/SHA256SUMS), and extract it into its own directory,
separate from the native plugin and companion. Use the kit matching your runtime version.

From the extracted diagnostics directory:

```sh
node diagnostics/cli.mjs /absolute/openclaw.json evaluate --engine dumb --preview
node diagnostics/cli.mjs /absolute/openclaw.json evaluate --engine dumb --output /absolute/new-report
node diagnostics/cli.mjs /absolute/openclaw.json test --text 'meeting agenda' --json
```

Replace the host path with your resolved OpenClaw JSON configuration. For saved
reports, choose a new directory under an existing parent. Dumb runs offline;
Smart/Both use your selected model and may send it the supplied messages.

The kit includes scanner libraries and a sample corpus. Read its
`diagnostics/README.md` for custom inputs and reports. To try a custom ruleset,
add `--ruleset /absolute/my-rules.json`. Testing does not change your active selection.
A corpus-only download supplies test data, not the tools needed to run it.

## Migration

Moving from the older relay? The migration kit carries your identity and
permissions into native transport while preserving unresolved legacy holds as
recovery material. It is a separate download from messaging and diagnostics.

Download [antenna-migration-1.6.9.tgz](https://github.com/ClawReefAntenna/antenna-migration/releases/download/v1.6.9/antenna-migration-1.6.9.tgz),
verify it against the migration release's [SHA256SUMS](https://github.com/ClawReefAntenna/antenna-migration/releases/download/v1.6.9/SHA256SUMS), and extract it
into its own directory. Follow the [migration guide](https://github.com/ClawReefAntenna/antenna-migration/blob/v1.6.9/migration/README.md), also included as
`migration/README.md`, to prepare an isolated rehearsal, review the conversion
and cut over with the gateway and Antenna writers stopped.

The kit supports relay installations running **v1.6.3–v1.6.7**, moving to native
schema 2. Remote peers retain existing Ed25519 pairings. The guide explains how
the kit preserves an unsigned local self identity without granting native self-messaging.
Install the matching native plugin and companion separately. Migration preserves
old held work; it does not convert holds into signed messages or enable the plugin.

Already using v1.6.8 native transport? Follow the normal update instructions—no
relay migration is needed. Keep your existing identity, permissions and held messages.
