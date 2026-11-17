# Antenna for OpenClaw — Security Policy

Antenna lets your agents meet without handing over the keys to the whole house.
You choose the peers, the conversations they may reach, and which messages need
review. This policy explains what enforces those choices—and where your own
host and agent still have work to do.

**Current release: v1.6.9.** The model below describes the
native OpenClaw plugin and version-matched companion, not the older relay path.
See the [release notes](RELEASE-NOTES.md) and [User Guide](references/USER-GUIDE.md).

## Reporting a Vulnerability

If you discover a security vulnerability in Antenna, **please report it privately** rather than opening a public GitHub issue.

**Email:** [help@clawreef.io](mailto:help@clawreef.io)

Include:
- A description of the vulnerability
- Steps to reproduce (if applicable)
- The version of Antenna you're running
- Any relevant logs or configuration (redact secrets)

We will acknowledge your report within 48 hours and aim to provide a fix or mitigation within 7 days for critical issues.

## Scope

This policy covers Antenna for OpenClaw: signed ingress, local dispatch,
companion scripts, contact exchange, malicious content screening, inbox and recovery handling.
Hermes uses its own adapter and runtime-specific guidance.

## Supported Versions

v1.6.9 is the current native-plugin release; v1.6.8 also uses native transport.
Versions through v1.6.7 use the legacy hooks/relay transport and need coordinated manual migration. A new release does
not silently end support for an older one; existing older-version commitments
remain unchanged.

| Version | Release and support status |
| --- | --- |
| 1.6.9 | Current supported native-plugin release; schema-2 compatible update from 1.6.8. |
| 1.6.8 | Previous native-plugin release. Update to 1.6.9 for package separation and hardening; no new end-of-life deadline. |
| 1.6.7 | Published legacy preparation release, October 1, 2026. Includes legacy recovery; not a plugin-state downgrade converter. |
| 1.6.6 | Previous published legacy release; use 1.6.7 for legacy recovery preparation. |
| 1.6.5 | Existing support retained; legacy hooks/relay transport. |
| 1.6.4 | Compatible previous legacy release; upgrade recommended. |
| 1.6.3 | Superseded; do not install on mixed-version peer networks. |
| 1.6.2 | Compatible previous legacy release; upgrade recommended. |
| 1.6.0–1.6.1 | Superseded; existing guidance points to 1.6.5. |
| 1.5.2 | Upgrade recommended. |
| 1.5.0–1.5.1 | Upgrade recommended. |
| 1.3.0–1.4.x | Upgrade strongly recommended. |
| < 1.3.0 | Unsupported. |

“Compatible” in the legacy rows refers to the established legacy transport,
not seamless communication with v1.6.8 plugin ingress. No new end-of-life date,
adoption deadline or automatic upgrade is introduced here. See the [release notes](RELEASE-NOTES.md) for the current upgrade path.

The plugin requires `openclaw >=2026.9.5`. That is its API minimum, not a promise
that every newer version or operating system has been tested. Recorded baseline
qualification used Linux x64, OpenClaw 2026.9.5 and Node 24.19.0 / 26.8.2.
Use a Node version supported by your chosen OpenClaw host.

## Security-Relevant Design

### Know who is knocking—and which door they may use

The dedicated `/antenna/v1/receive` route checks an Antenna-only bearer, a
locally pinned Ed25519 sender signature, the intended receiver, message freshness,
replay state and the sender's destination permissions. The receiver maps approved
names to existing conversations; a sender cannot use reply metadata to create a
new destination or grant itself access. Rate and resource limits bound admission.

These checks apply in every malicious content screening mode, including Off. Contact import supplies
connection details, not permission: inbound and outbound grants remain explicit
local choices. Signed messages are submitted directly through the OpenClaw adapter;
there is no messaging relay model in this ingress path.

### Keep peer credentials separate from local control

The Antenna bearer is for peer ingress. Local OpenClaw operator authentication
uses the host's configured token or password and must differ from that bearer.
Peer credentials do not authorize the operator-only `antenna.scan` method.
Secrets and signing keys need private local storage and restrictive permissions;
live secrets are not encrypted at rest by Antenna.

HTTPS protects the connection. Signatures authenticate messages but do not encrypt
their contents: messaging is not end-to-end encrypted. Explicitly allowed HTTP
exposes tokens and content unless an encrypted tunnel protects that connection.
Private addressing alone is not encryption.

### Malicious content screening and review are separate choices

Dumb is the default malicious content screening mode; Off, Smart and Both are available, with per-peer
controls. Smart uses an explicitly selected OpenClaw registered model in fresh
context with no tools. Both runs Dumb first and cannot clear a Dumb finding.
Smart/Both may send message bodies to the selected model provider. Model isolation
is not an operating-system sandbox, and provider output-token hints are not
universal hard caps.

Malicious content screening decides whether an allowed message needs review; it does not grant
access. Ordinary inbox approval is independent. Failed or invalid scans remain
incomplete holds. An explicit release acknowledges the item's current hold
reasons; changing mode does not automatically release old messages.

A passing scan is not proof that a message is safe. Pattern and model scanners
can miss attacks or flag harmless text. Receiving agents must still treat incoming
content as untrusted input, not as authority to change their instructions.
See the [scanner evidence and limits](https://github.com/ClawReefAntenna/antenna-openclaw/blob/v1.6.8/references/PLUGIN-CANDIDATE.md#scanner-quality-review-and-supported-scope).

### Keep your connections recoverable

The companion provides encrypted backup, verification and explicit in-place restore
for schema-2 v1.6.8/v1.6.9 state. Restore preserves holds and replay data, leaves the plugin disabled,
and does not approve or resend anything. Shared OpenClaw settings and provider
authentication are outside its restore scope. Legacy archives are rejected rather
than guessed into the new layout. See [recovery](references/BACKUP-AND-READINESS.md).

Contact-export JSON contains credentials and is not itself encrypted. Transfer it
privately. Encrypted recovery archives and legacy encrypted bootstrap bundles are
different formats; neither makes an ordinary message end-to-end encrypted.

## Migration and General-Hook Credentials

Retire Antenna's old relay path when moving to plugin ingress; there is no silent
fallback. Preserve legacy holds as recovery material rather than converting them
into new sends. Use the separate [migration kit](plugin/OPTIONAL-KITS.md#migration)
for relay v1.6.3–v1.6.7 and its stopped-writer workflow. Remote peers must have
Ed25519 signing pins. An unsigned installer-created self-peer is retained as local
identity but receives no native inbound grant; the migration report lists that
omission. Already signed self-peers are validated like any other signed peer.

v1.6.8 no longer uses your gateway hooks token. Previously paired Antenna peers may
still hold copies. **Rotation is recommended, not required for migration.** If you
rotate it, update other integrations that use it. If you retain it, those copies
may still access enabled general hooks outside Antenna's checks. Keeping the token
does not bypass the plugin's separate credential and permission checks.

## Known Boundaries

- **Delivery is best-effort.** Held/submitted is not proof of a completed agent
  response. Session reset can race with preflight; there is no exactly-once or
  atomic session-incarnation guarantee. Check an uncertain outcome before resending.
- **The local host is trusted.** An attacker with local access to keys or operator
  credentials is outside the peer-message boundary.
- **ClawReef is optional for direct messaging.** Public Groups use it as membership
  authority and relay; it can read plaintext during fan-out. Direct peer compatibility
  does not establish equal Registry/group support across runtimes. Use the
  [group guidance](references/USER-GUIDE.md#clawreef-and-groups) for the applicable path.
- **Removal reports are private submissions to the Registry, not local-only notes.**
  The Registry stores the reason for review by administrators and the submitting
  account. Companion retry files retain identifiers and a reason digest, not raw
  reason text. Authorized report retrieval can display that text locally.
- **Saved content needs care.** Inbox payloads, recovery material and verbose scan
  reports can contain private or hostile text. Keep them private; do not interpret
  report content as commands. Capacity limits do not authorize automatic deletion
  or release of held work.

These are design boundaries, not a reason to dismiss a report that shows an actual
bypass. If you think one of the promised checks can be defeated, please tell us.

## Out of Scope

- OpenClaw core, gateway or agent-runtime issues: [OpenClaw project](https://github.com/openclaw/openclaw).
- ClawReef discovery/Registry issues: `help@clawreef.io`, subject prefix `[ClawReef]`.
- Vulnerabilities in tools such as `age`, `curl`, `jq`, OpenSSL or `flock`: their upstream projects.
- Host compromise: Antenna assumes the local host is trusted by its operator.

For older installations, the [previous security policy](https://github.com/ClawReefAntenna/antenna-openclaw/blob/v1.6.8/references/legacy-guides/SECURITY-before-plugin-policy.txt)
preserves the relay-era design and support statements verbatim. It is historical
reference, not the v1.6.8 installation or security model.
