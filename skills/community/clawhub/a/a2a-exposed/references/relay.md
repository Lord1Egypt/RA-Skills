# Relay operations

## ACP stdio targets

For an owner-approved local ACP agent, use `relay a2a run --acp` with JSON argv,
`--acp-cwd` and a protected `--acp-peers-file`. To address one existing session,
require both `--acp-session ID` and `--acp-session-peer NAME`; unsupported or failed
`session/load` must not create a replacement. Never let peer content select a
local session, executable or working directory. Independent application bearer
credentials are required; the shared relay ingress token and Worker pairing are
not peer authentication for this target. Permission requests are canceled and
reported `input-required`; peers cannot approve tools. File/terminal client
capabilities are disabled, but cwd is not a sandbox. See the
[ACP/session contract](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/http-relay.md#local-acp-agent-and-session-targeting)
for caps, cleanup and hosted HTTP-relay prerequisites.

Require explicit owner `--acp-mode MODE`, selected from advertised adapter modes,
not provider names/defaults. New and exact loaded sessions must acknowledge
`session/set_mode` before a prompt; later prompts reapply it. Missing/unavailable
mode or uncertain setting fails closed. Conflicting current-mode or mode config
updates stop the binding. Peers cannot select modes or run native slash commands.
This does not change native sandbox/approval defaults globally; real-agent
retesting is required before exposure. Canceled/stopped bindings need connector
restart, not recreation. Phase diagnostics are fixed and sanitized. Optional
`--acp-diagnostics-file NEWFILE` exclusively creates a mode-600 private raw stderr
file, no overwrite/symlink, 1 MiB total cap. Raw data may contain credentials:
inspect locally, never paste into chat/GitHub or send to peers. Environment is
inherited, including `CLAUDECODE`; do not silently strip it. Distinct actual ACP
message IDs get newline boundaries; ID-less chunks remain exact because their
message boundaries cannot be inferred safely.

## Wake relay operations

Offer the relay first when the host is local-only or has no public address the inbox can call. `hosted capabilities --json` reports `relay: true`, or `relay status --json` reports `enabled: true` and `protocolVersion` 1. `enrolled: false` means no connector yet. A 404 means unsupported or disabled. A tunnel is for a self-hosted inbox with a zone. Polling is for a missing relay, no local receiver, or a declined foreground `relay run`. Do not assume a hosted service runs the latest OSS version.

A reachable card proves the inbox answers. `connected: true` proves the connector is up. HTTP 2xx proves the local receiver accepted the signed POST. None of those prove the handler ran or the owner was notified. See the [setup checklist](../../a2a-exposed-setup/references/checklist.md).

A `catchup` hint asks for unfiltered `inbox`. The inbox remains authoritative;
duplicate hints can follow uncertain delivery. Never resend a message merely
because a wake timed out. A 2xx acknowledgment means only local webhook acceptance,
not that an agent handled the inbox.

Enrollment, rotation and revocation require the human's approval. Use the setup
skill and [relay contract](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/wake-relay.md). Credentials stay in a
mode-600 file or named environment variable, never argv, URLs, chat or logs.
The relay carries wakes only, not A2A façade traffic.

The foreground connector stops on replacement/revocation (4001) or a protocol
violation (1008/4008), rather than reconnecting. Invalid relay frames are rejected
before local delivery; check the relay endpoint/configuration before restarting.
`run` emits no stdout/JSON stream. Intentional SIGINT/SIGTERM exits 0; setup,
protocol/policy/revocation failures exit 1 with secret-free stderr guidance.
Reconnect waits 500ms–30s, never zero. Three consecutive failed upgrades or
10-second hello timeouts stop with exit 1; a healthy hello resets the budget.
Each attempt sends one upgrade request, without redirects or automatic HTTP
authentication retries on Node 22.18+, 24 and 26. Handshake failures report
the Node version; check endpoint reachability and enrollment with `relay status`.
Native WebSocket hides handshake HTTP status, so check endpoint, capability and
enrollment rather than assuming every failure is authentication. Expired/skewed
frames and temporary concurrency saturation fail that delivery, not the socket.
Owner draft tests expose canonical `error` codes: `offline`, `timeout`, `revoked`,
`stale_enrollment`, `invalid`, `local_http`, `busy`, `uncertain`, `unavailable`; success omits `error`.
`busy` means temporary backpressure; `uncertain` means a POST may have executed.
Check the connector, receiver and authoritative inbox before explicitly retesting;
never automatically replay an unconfirmed execution.
Keep the numeric local HTTP `status` (including 401/500); never parse `info`.

The owner API can test an unsaved relay draft before saving: `POST
/owner/wake/test` accepts explicit `transport:"relay"`, `connectorId:"default"`,
current enrollment `generation`, `credentialsMode:"resolved"`, preset and optional
application credentials/options. Only supplied credentials are used; omitted or
empty secrets never inherit saved values. Trusted hosted callers resolve any
permitted retained secrets before this call. No URLs or raw request frames are
accepted, and no settings or pending wakes are consumed. A no-body call still
tests applied settings. See the relay contract for the exact allowlist. Do not
send draft credentials through chat or print them in test evidence.


Hosted services advertising `relay: true` in `hosted capabilities --json` support
`relay wake status --agent NAME --json`, then `test` with explicit `--config-version`,
`--connector-id`, `--generation`, `--preset`, protected application inputs and a new
`--receipt-file`. `relay wake save` takes that protected file, the same config version
and explicit `--confirm`. A receipt expires after five minutes and is single-use;
failed retests invalidate old passes. Test does not save; save sends no new test.
Use `relay wake remove --config-version N --confirm` to remove settings separately
from connector `relay revoke`. For MCP, only a scoped CLI receipt can be passed as
`secretReference` with `confirmed:true` (and `clear:true` for a prepared removal).
Never send application/connector secrets or draft overrides through MCP. See the
[protected-file workflow](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/wake-relay.md#hosted-relay-wake-setup-with-protected-files).
