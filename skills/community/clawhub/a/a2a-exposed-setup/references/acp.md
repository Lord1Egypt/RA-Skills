# ACP session relay setup

When the owner wants a local ACP v1 stdio agent rather than a wake receiver, use
[the ACP setup/session contract](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/http-relay.md#local-acp-agent-and-session-targeting).
Obtain approval for relay enrollment and the exact local executable/cwd first.
Use `relay a2a run --acp` with JSON argv, `--acp-cwd` and a mode-600
`--acp-peers-file` of independent application token hashes; forward `authorization`
at enrollment. Worker pairing and shared ingress are not application peer auth.
Prefer `--acp-session ID --acp-session-peer NAME` when exposing an existing
conversation. Require advertised `loadSession` and fail rather than creating a
replacement; never accept session selection from peer text. Keep native tool
permissions enabled; cwd is not a sandbox, and canceled permission requests need
local owner resolution. Hosted wake-relay support does not imply HTTP-relay
support; verify the separate runtime feature before enrollment. No deployment,
credential changes or real provider inference is authorized by this guidance.

Require owner-selected `--acp-mode MODE`: inspect the adapter's advertised IDs
locally, never guess a safe mode from its provider name or defaults. Both new and
exact loaded sessions must advertise the mode and acknowledge `session/set_mode`
before prompts; each later prompt reapplies it. Conflicting current-mode or mode
config updates stop the binding. Native slash prompts are refused. This is not a
sandbox and does not modify global native approval settings. Real-adapter safety
retesting remains necessary; protocol fixtures cannot establish it.

Failures identify a fixed phase, never raw adapter errors. Canceled/stopped
bindings require connector restart, never automatic recreation. Optional
`--acp-diagnostics-file NEWFILE` captures private raw stderr only: exclusive new
mode-600 regular file, no symlink/overwrite, 1 MiB aggregate cap. Keep it in a
private directory, inspect locally and never paste it into chat or GitHub; it may
contain credentials. Child environment is inherited, including `CLAUDECODE`; use
an appropriate launch shell rather than silently stripping it. Actual message IDs
separate assistant messages; ID-less chunks have ambiguous boundaries and stay
unchanged, not newline-per-chunk.
