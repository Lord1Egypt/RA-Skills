# Antenna for OpenClaw plugin — 1.6.9

Inbound signed v2 delivery with Off / Dumb / Smart / Both Malicious Content Scanning (MCS).
Default: Dumb. Both runs Dumb first and only calls Smart after a pass.
Authentication, replay checks and receiver-selected existing destinations apply
in every mode. Ordinary approval and MCS holds remain independent.

This package provides signed ingress and direct local dispatch without a messaging
relay model. Manual migration, direct/list transport and contact exchange are
covered in [the companion guide](https://github.com/ClawReefAntenna/antenna-openclaw/blob/v1.6.9/references/USER-GUIDE.md). Peers can run OpenClaw or Hermes, with Antenna installed on both sides
using their own runtime-specific setup. For Public Groups, use the features advertised by your Registry. Delivery is
best-effort; check uncertain outcomes before resending.

## Install in your selected OpenClaw instance

Requires OpenClaw **2026.9.5 or newer**, a Node version supported by OpenClaw,
Bash, jq and flock. Tested platform: Linux x64, with Node 26.8.2 and 24.19.0
and OpenClaw 2026.9.5.
Install `antenna-native-1.6.9.tgz` from the
[v1.6.9 release](https://github.com/ClawReefAntenna/antenna-openclaw/releases/tag/v1.6.9) with
`openclaw plugins install /absolute/path/to/antenna-native-1.6.9.tgz`, using the
intended OpenClaw state/config environment and the matching companion. The OpenClaw peer dependency supplies the public gateway SDK.

Prepare a JSON policy with:
- `schemaVersion: 2`, `receiver`, a private random `bearer` (at least 32 characters);
- `peers`: map of authenticated peer names to Ed25519 PEM `publicKey`,
  allowed `destinations` array and optional `mcs` override;
- `destinations`: receiver-approved name to existing `agent:...` session key;
- absolute, distinct `inboxFile` and `replayFile`;
- optional `mcs` (default dumb), `inbox` (default on), `maxBodyChars` (65536).

For a new absent entry, `node /absolute/antenna/plugin/cli.mjs /path/openclaw.json init policy.json`
writes it **disabled**. If the native installer has already added an entry,
merge the policy into its config explicitly; init refuses to overwrite it.
Set the plugin enabled and allowlisted only in the intended config,
then apply through that gateway’s reload policy. Mode/selection edits require
plugin reload; restart only when hot reload is unavailable or disabled.
Configuration-file edits preserve unrelated settings and activation, validate the
new Antenna policy, and keep a private `HOST.antenna-backup-*/before.json` preimage.
No-op edits do not request a reload or restart. `restartRequired: null` means
the offline editor has not determined the running host’s reload capability.
The file CLI requires resolved JSON and does not accept includes, symlinks or
hard links. Keep other configuration writers stopped while editing. For normal
host administration, prefer supported OpenClaw configuration commands. The file
CLI does not restart services.

The local adapter uses the gateway's configured port and token or password authentication,
matching the host's selected mode without changing its login configuration. The selected
credential must be resolved to a nonempty string and differ from the Antenna peer bearer.
When the mode is explicit and that credential is absent from config, the matching
`OPENCLAW_GATEWAY_TOKEN` or `OPENCLAW_GATEWAY_PASSWORD` environment variable is
accepted. Config values take precedence; the other mode is never used as fallback.
Non-string secret references must be resolved by OpenClaw before registration; standalone
operator commands likewise require a resolved local credential. Unsupported auth modes
and missing credentials fail without falling back to another mode.

## Operator commands

In these examples, `/absolute/antenna` is the companion root and
`/path/openclaw.json` is the resolved configuration for your selected host.

All output is JSON, including escaped message bodies; never render decoded
message bodies as terminal commands, HTML or model instructions.

```text
node /absolute/antenna/plugin/cli.mjs /path/openclaw.json status
node /absolute/antenna/plugin/cli.mjs /path/openclaw.json mode off|dumb|smart|both [peer]
node /absolute/antenna/plugin/cli.mjs /path/openclaw.json mode default peer
node /absolute/antenna/plugin/cli.mjs /path/openclaw.json check registered-model-or-alias
node /absolute/antenna/plugin/cli.mjs /path/openclaw.json select registered-model-or-alias
node /absolute/antenna/plugin/cli.mjs /path/openclaw.json inbox list
node /absolute/antenna/plugin/cli.mjs /path/openclaw.json inbox show ITEM_ID
node /absolute/antenna/plugin/cli.mjs /path/openclaw.json inbox release ITEM_ID '["Awaiting approval","MCS flagged"]'
node /absolute/antenna/plugin/cli.mjs /path/openclaw.json inbox discard ITEM_ID
node /absolute/antenna/plugin/cli.mjs /path/openclaw.json inbox approve-ordinary
```

Status is offline. `check` makes one synthetic request without saving a selection;
`select` checks and saves one registered model/alias shared by Smart and Both.
Neither changes mode or enables the plugin. Reload Antenna after selection/mode
changes; restart when hot reload is unavailable or disabled.
Detection evaluation is optional and does not impose a passing-score gate.

## Registered-model Smart scanning

Configure models and credentials in OpenClaw, including models used only for
scanning. Antenna stores only `scannerModel` and a configuration-binding identity;
it has no custom endpoint, credential-reference or parallel profile interface.
The loaded plugin uses `api.runtime.llm.complete` with
`execution.mode: isolated-agent-runtime`: one fresh user message, fixed scanner
rubric, no tools, unrelated history, session creation or destination delivery.
Unsupported runtime paths fail incomplete; no direct-provider fallback.

OpenClaw requires host plugin LLM permission for an explicit model selection:

```json
{
  "plugins": {
    "entries": {
      "antenna": {
        "llm": {
          "allowModelOverride": true,
          "allowedModels": ["your-provider/your-model"],
          "allowedCompletionModels": ["your-provider/your-model"]
        }
      }
    }
  }
}
```

Merge this into existing host configuration, not the Antenna `config` object;
do not overwrite other settings. This grants model-use authority, not new
credentials. Use your registered canonical model ID in the permission lists.
Start/restart the gateway with the plugin enabled in Off or Dumb mode, check/select
the model, then enable Smart/Both and reload Antenna. Restart when hot reload is unavailable
or disabled. Check/select and Smart diagnostics require the running local
gateway and operator-admin access to `antenna.scan`; the peer bearer cannot call it.
The RPC only scans literal bodies: no endpoint overrides, sessions or inbox writes.

The host resolves authentication and rotation; subscription support depends on the
selected runtime's isolated-completion capability and is not universally promised.
The SDK's `maxTokens` is advisory for some runtimes. Antenna requests 1,024 tokens,
limits input and accepted response bytes, and enforces a deadline; it cannot promise
a provider-side generation cap on a backend that ignores the hint. Oversized,
malformed or unsupported responses hold incomplete. Failed requests are not
automatically retried or sent to another model.

Old `scannerProfile` selections do not authorize Smart in the native plugin. Run
`select` with a registered model; success removes that obsolete field. Existing
held messages remain held. No automatic credential/profile migration is attempted.

## Editable Dumb rulesets

See [ruleset format and agent-friendly editing guide](RULESETS.md). The bundled
`rules/default.json` is selected by default. Optional `rulesetFile` selects one
absolute local file, loaded at startup. Custom copies belong outside the plugin
install directory. `rules validate FILE` checks structure and regex compilation;
`rules select FILE` saves the selection and requires plugin reload (or restart
when the host cannot hot reload). Missing or invalid
selected files fail visibly, never silently disable scanning.

## Explicit upgrade

Schema conversion and legacy migration belong to the separate
[migration app](OPTIONAL-KITS.md#migration). The native runtime never converts
configuration or inbox payloads on startup.

## Optional diagnostics

Evaluation tools and attack corpora are separate. See [optional kits](OPTIONAL-KITS.md)
for version-matched acquisition and standalone commands. Runtime scanning, rules
validation and check/select remain available without a kit.

## Shared resource limits and retention

`limits.mjs` is the versioned hard-ceiling contract. Scan input is 64 KiB; derived
inspection text is bounded to min(4× bytes, 256 KiB) and two decoding levels.
Dumb has a 250 ms wall-time deadline, bounded 64/16 MiB old/young worker heaps,
and at most two process-local workers; idle workers expire after one second.
Timeout or worker failure terminates that worker and yields incomplete.

Gateway and CLI share two kernel-owned `flock` slots per engine beneath the
configured inbox directory (`antenna-scan-slots/`). They use the existing Bash/flock
dependencies; no daemon, owner database, polling queue or automatic stale-lock
stealing. Parent EOF/exit releases leases, with bounded lease lifetime. Default
Smart concurrency is two; `maxActiveSmart: 1` can lower a runtime/command's local
limit. The cross-process hard ceiling remains two; separate inbox installations
are separate capacity domains. Busy scans become incomplete, with no delayed
surprise request. Production durable inbox capacity still governs acceptance.

Smart's 30-second total includes scheduling; connect cap is five seconds, response
64 KiB, serialized request 16 KiB, requested output 1,024 tokens, at most 16 findings
and 512 characters per reason. Oversize context/requests hold incomplete, never crop.
Slow/cold providers time out rather than receiving an automatic retry. HTTP ingress
also has a five-second total body-read deadline and the existing two-request cap.

Pending scans are bounded by the durable inbox, capped at 100 items / 16 MiB,
including terminal items. Capacity is not renewed by silently deleting old records:
**no automatic retention purge, held-payload eviction or pressure-driven release**.
At capacity, further durable admission fails closed. Archive/retire state only by
an explicit stopped-writer operator procedure; no automatic cleanup command is
introduced. Read-only status includes state counts and hard limits. Per-message
scan metadata and diagnostic reports provide timing/outcome/usage counters without
ordinary raw-body logging. Evaluation/custom batches are serial, at most 500 cases
and five repetitions.

## Companion packaging

This npm archive includes the plugin and its own operators, not the companion
`antenna` shell CLI or Python helpers. Keep companion `bin/`, `scripts/`, `lib/`
and `plugin/` together at the same release version. The repository's
[release notes](https://github.com/ClawReefAntenna/antenna-openclaw/blob/v1.6.9/RELEASE-NOTES.md) describe the matching artifacts. They are included with the companion,
not the native archive. Legacy setup is not plugin initialization.

## Recovery and retained hooks

Use the version-matched companion recovery command and its `references/BACKUP-AND-READINESS.md` guide. Recovery is not a plugin-only CLI feature. General-hook rotation is recommended, not mandatory; operator credentials must remain separate. See [migration app](OPTIONAL-KITS.md#migration).
