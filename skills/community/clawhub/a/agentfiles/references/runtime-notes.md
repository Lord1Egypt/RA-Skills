# AgentFiles Runtime Notes

## Requirements

- Node.js 20+ is expected.
- The `agentfiles` CLI binary must be on `PATH` (installed via `npm i -g agentfiles-cli`).

## Auth and Config

- The CLI config lives at `~/.attach/config.json`.
- Credentials are normally obtained through browser-approved `setup` or `connect` flows, then stored in that config file.
- If the CLI is not configured, `requireConfig()` will fail with `Error: Not configured. Run 'agentfiles setup' or 'agentfiles config' first.`
- Use `agentfiles whoami` to confirm the active principal and namespaces.
- Use `agentfiles config --show` to inspect the current config without changing it.
- The skill reuses local CLI config; it should not ask the user to paste secrets inline into skill prompts.

## Browser-Based Onboarding

- `setup` is the default browser-approved onboarding path.
- `connect <runtime>` is the advanced/manual path for dedicated runtime credentials.
- Use `connect` only when the user explicitly wants runtime-specific credentials, or when the runtime-specific setup path is the point of the task.
- In sandboxed environments, opening the browser may require extra approval.

## Polling Watch Caveats

`watch` is intentionally V1 and best-effort:

- it polls the namespace list endpoint
- it only remembers seen artifact versions in memory for the current process
- it does not persist seen state across restarts
- high churn beyond the fetched window can miss older updates
- `--once --since now` seeds current state, emits nothing, and exits
- `--exec` is executable-path-only in V1; do not pass shell strings or inline args

Use `--json` when another wrapper needs stable machine-readable output.

## Sandbox and Network Notes

- The CLI does not use shell composition.
- Installing `agentfiles-cli` requires network access the first time.
- In sandboxed agent environments, request approval before a command that must cross the network or open a browser.
