# 🦞 Antenna for OpenClaw v1.6.9 — A Lighter Kit

Your everyday messaging kit now carries just what it needs. Diagnostics and legacy
migration tools are separate from the native plugin and companion.

**Packaging and documentation update — October 9, 2026:** Migration and diagnostics
now have their own repositories and release downloads. Guides and examples follow
those new homes; messaging runtime code is unchanged.

## What changed

- A smaller everyday install, with diagnostics available as an optional download.
- Configuration changes now keep private recovery copies.
- Tighter checks for Smart responses, metadata files and gateway connections.
- Restore schema-2 backups from v1.6.8 or v1.6.9. New backups are marked v1.6.9.
- Clearer guidance on signed messaging, model-based malicious content screening and Registry report privacy.

## Install or update

Install `antenna-native-1.6.9.tgz` with the matching
`antenna-companion-1.6.9.tgz`. Add the optional
[diagnostics kit](https://github.com/ClawReefAntenna/antenna-diagnostics/releases/download/v1.6.9/antenna-diagnostics-1.6.9.tgz) to try malicious content screening rules and sample messages.
Verify the selected release's [SHA-256 manifest](https://github.com/ClawReefAntenna/antenna-openclaw/releases/download/v1.6.9/SHA256SUMS).
Start with the [User Guide](references/USER-GUIDE.md#install-and-configure).

Updating from native v1.6.8? Your existing connections and permissions carry
forward; no relay migration is needed. Requires OpenClaw **2026.9.5 or newer**.
Tested platform: Linux.

Moving from relay v1.6.3–v1.6.7? Download the separate [migration kit](https://github.com/ClawReefAntenna/antenna-migration/releases/download/v1.6.9/antenna-migration-1.6.9.tgz)
and follow the [migration guide](https://github.com/ClawReefAntenna/antenna-migration/blob/v1.6.9/migration/README.md). The kit is separate from the messaging
and diagnostics downloads; see [optional kits](plugin/OPTIONAL-KITS.md#migration)
for checksums and setup.

## Recovery and security

Before replacing packages, stop the gateway and preserve your Antenna state.
A backup is recommended; keep the previous matched packages if you may need to
roll back. Follow the [recovery guide](references/BACKUP-AND-READINESS.md) for
restore steps and version compatibility.

Your existing permissions and malicious content screening choices stay yours. See the
[Security Policy](SECURITY.md) for privacy details and how these controls work.
