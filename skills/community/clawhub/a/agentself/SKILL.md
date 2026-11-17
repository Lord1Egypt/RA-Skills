---
name: agentself
description: Local agent identity — wallet, secrets, optional email. Use when asked to initialize or hand off an identity, use its wallet or secrets, connect email, or process mail. Prefer --json and open the matching reference for multi-step work.
allowed-tools: Bash(agentself:*)
---

# agentself

CLI identity for an agent. No MCP server.

Requires the `agentself` CLI. If unavailable, install it with `uv tool install agentself` or `pipx install agentself`, then run the version check below.

## Start safely

Do not guess flags or expose values in logs, arguments, or chat.

```bash
agentself --json --version
agentself --help
agentself <command> --help
agentself backends
agentself diagnose
```

Prefer `--json`. Success and failure are one JSON object on stdout with `"ok"`, and failures include `"error"`, `"reason"`, and `"next"`. Human errors may include a `next:` line on stderr. `agentself --json --version` includes `cli` (machine schema id, currently 1). Ignore unknown keys.

Start by checking `agentself --json --version`. This skill requires `cli: 1`. A different schema or an unexpected `package` / `executable` path means the installation is stale: stop, install the intended CLI, reinstall its packaged skill, and check again. Never mix instructions from one schema with an executable from another.

Identity directory is `AGENTSELF_IDENTITY_DIR` (default `~/.agentself`).

## Common path

```bash
agentself install --tools
agentself init
agentself --json show
```

`init` and `diagnose` do not fetch binaries. Missing host tools: `next: agentself install --tools`. `AGENTSELF_FETCH_TOOLS=0` refuses a fetch even for `--tools`. Repeating init is safe; identity or backend changes need `--force`.

`--json show` includes the age recipient and email readiness. For wallet work, inspect `agentself backends wallet`; the default Base wallet is live and can move real funds. Use `wallet authorize` for signing.

For secrets, prefer files: `secret create NAME --file PATH` and `secret get NAME --file PATH`. Plaintext stdout requires explicit `--print`.

For printable cross-agent context, use `note set NAME --file PATH` and
`note get NAME`. Notes are non-secret: never put credentials, OTPs, private
keys, secret values, or mail bodies in them.

## Open the relevant workflow

- Connecting or recovering email setup: [references/email-connect.md](references/email-connect.md)
- Identity sharing, isolation, continuity, interruption, backup, or restore: [references/handoff.md](references/handoff.md)
- Listing, fetching, filtering, and completing mail work: [references/mail.md](references/mail.md)

## Skills

```bash
agentself install --skills
agentself install --skills -g
agentself install --skills=agents
```

Skills install this complete skill tree into the current directory unless `-g`.
