# E2B Notes

## MCPorter-native design

This skill is now structured around a local MCP server:

```text
scripts/e2b-mcp-server.mjs
```

Registration helper:

```text
scripts/register-mcporter.mjs
```

After registration, mcporter should expose the following tool surface:

- `create_sandbox`
- `list_sandboxes`
- `get_info`
- `exec`
- `host`
- `set_timeout`
- `snapshot`
- `kill`

## What the MCP server wraps

The server uses the E2B JavaScript SDK and covers the common OpenClaw-agent actions:

- create a sandbox
- reconnect to a sandbox by id or saved label
- run one-shot commands inside the sandbox
- derive public host URLs for exposed ports
- extend timeout
- snapshot
- kill

## State file

The script stores known sandboxes in:

```text
~/.openclaw/workspace/.state/e2b-sandboxes.json
```

Use labels to make follow-up actions easier:

```bash
mcporter call e2b-sandbox.create_sandbox --args '{"label":"codex-lab"}'
mcporter call e2b-sandbox.exec --args '{"sandbox":"codex-lab","cmd":"uname -a"}'
```

## Credential requirement

Set `E2B_API_KEY` in the OpenClaw vault / environment before using the skill.

## Operational notes

- Default timeout is 1 hour unless overridden with `timeoutMs`.
- `exec` is for one-shot commands; use a custom agent flow if you need a long interactive PTY session.
- `host` returns the externally reachable URL for services listening on a port.
- `snapshot` is useful when you want a reusable prewarmed environment.
- `kill` also removes the sandbox from the local state file.
- The legacy shell wrapper remains available as a fallback/debug path.
