# Release review - Baton v1.8.2

## Security audit remediation

Resolved the ClawHub audit finding about config parsing by deleting the `Function(...)` fallback. Baton now parses strict JSON, JSONC, and a small safe JSON5 subset without evaluating `openclaw.json` contents.


Status: release candidate.

## Checks performed

- `SKILL.md` exists and includes valid-looking frontmatter with name, description, version, homepage, and metadata.
- `SKILL.md` avoids non-standard `requires.tools` metadata and keeps tool requirements in instructions.
- Runtime kernel is below the validator budget of 6500 characters.
- Referenced files exist.
- Node scripts pass syntax checks.
- Setup, discovery, status, routing, leasing, and per-agent routing were smoke-tested with a JSON5-like OpenClaw config.

## OpenClaw alignment

- Uses `sessions_spawn`/`subagents` for always-spawn orchestration.
- Treats `sessions_spawn` as non-blocking and prefers `sessions_yield` over polling.
- Keeps `runTimeoutSeconds` in OpenClaw subagent config guidance, not spawn arguments.
- Uses `provider/model` model refs and keeps Baton-specific state under `.openclaw/baton/` rather than modifying `openclaw.json`.

## Release note

Run `node scripts/baton-setup.mjs --config openclaw.json --all` or use the model manager before enabling explicit model routing in a real workspace.
