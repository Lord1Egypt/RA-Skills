# AgentPearl Exporter

AgentPearl Exporter packages the agent-defining source files from supported repositories into a small zip that AI systems can inspect and migrate across frameworks.

It focuses on agent core only:

- identity and instruction files
- bootstrap and memory context files
- runtime config and config schemas
- capability boundaries
- built-in roles or agent manifests
- prompt composition sources

Supported framework signatures:

- `nanoclaw-ts-bootstrap`
- `nanobot-py-templates`
- `nullclaw-zig-bootstrap`
- `zeroclaw-rs-config-prompt`
- `openfang-rs-manifests`
- `codex-rs-builtins`

Example:

```bash
./scripts/export-agent-core-pack.sh --repos codex,openfang --output-dir ./out
```

The generated archive includes `README.txt` and `MANIFEST.txt` so the exported pack can be consumed directly by humans or AI migration workflows.
