# Connect Aftercard

Production remote Streamable HTTP endpoint: https://mcp.aftercard.ai/mcp.
Use the host's supported MCP connection manager and host-managed OAuth.
An installed skill does not create or authenticate that connection. A native
plugin is optional. Do not install a local server, payment CLI or proxy.

Inspect the exact endpoint and selected agent. Reuse an existing matching
connection and valid sign-in; other services are not aliases. If the name is
already used for a different endpoint, report the conflict without replacing
or disconnecting it. Installation, OAuth completion, tool activation and rail
readiness are separate facts. Missing tools alone prove none of them.

When sign-in is required, use one supported native authentication action for
that connection. Email and OTP belong only in its secure browser flow. Keep
tokens, authorization codes and access-bearing URLs out of chat, shell
arguments, logs and evidence. Reuse pending sign-in. A canceled or denied
attempt stops; another client or method must not bypass it.

If a supported existing CLI is the user's host configuration surface, Codex
can add an absent server with `codex mcp add aftercard --url
https://mcp.aftercard.ai/mcp` and authenticate with `codex mcp login aftercard`.
Claude Code can add it with `claude mcp add --transport http aftercard
https://mcp.aftercard.ai/mcp`; use its interactive `/mcp` Authenticate action
when the agent cannot initiate login. Do not install another CLI to bridge a
missing host feature. Other hosts use their native remote MCP settings.

After authorization, discover deferred tools in this conversation and call
`get_magicpay_capabilities`, then `get_magicpay_status`. Reuse the current task
when callable. Follow observed authentication, service and activation errors
separately. Use only the host's supported refresh or documented user handoff;
do not automate its settings or invent private RPC. A new chat cannot prove
sign-in or retain a payment approval/context that the host did not preserve.

Check the selected environment, owned agent, current setup state, execution
mode and rail-specific availability. Respect each rail's compatibility floor;
do not require the newest release merely because it exists. Offer only ready
rails. Silently read `get_payment_balance` without an asset selector after
authenticated readiness. Unknown balance is unknown, not zero. Report the
verified connection, exact formatted balance and actual available capabilities.
Connection verification creates no payment, top-up or test charge.

Inside Aftercard's own hosted agent, the host already binds the authenticated
connection and selected identity. Reuse that binding. If the user selected an
external agent credential through the app, preserve that exact identity and
its private host configuration; do not replace it with user OAuth or expose
the credential. A host without required private-header support reports the
limitation instead of switching agents.
