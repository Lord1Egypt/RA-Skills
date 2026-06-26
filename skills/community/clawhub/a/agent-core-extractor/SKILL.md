---
name: agentpearl-exporter
version: 1.0.0
description: Export the agent core from supported framework repositories into a small source-only zip for AI migration or cross-framework analysis. Use when the user wants to detect supported agent repos, extract only agent-defining files, produce a portability pack, or study identity, instruction, runtime, capability, multi-agent, and prompt-composition layers.
metadata:
  license: MIT
  author: moshiwei
  homepage: https://github.com/moshiwei/AgentPearl
  tags:
    - agents
    - portability
    - migration
    - export
    - prompt-engineering
  openclaw:
    emoji: shell
    bins:
      zip: Optional but recommended for building export archives.
---

# AgentPearl Exporter

Use this skill to build a pure agent-core export from one or more supported repositories.

## When To Use It

Use this skill when the user wants to:

- extract only the files that define an agent
- package agent-core files into a clean zip
- detect which supported framework a repo uses
- prepare source material for AI-driven migration into another agent framework
- study the identity, instruction, runtime, capability, multi-agent, or composition layers of an agent repo

## Supported Frameworks

The bundled exporter detects these framework signatures:

- `nanoclaw-ts-bootstrap`
- `nanobot-py-templates`
- `nullclaw-zig-bootstrap`
- `zeroclaw-rs-config-prompt`
- `openfang-rs-manifests`
- `codex-rs-builtins`

## Workflow

1. Confirm the target repositories exist under a common base directory.
2. Run `scripts/export-agent-core-pack.sh`.
3. Inspect the resulting zip, `README.txt`, and `MANIFEST.txt`.
4. If the user needs migration guidance, read `references/AGENT_CORE.md` to map the exported files into agent-core layers.

## Commands

Export the default supported repositories under `~/Documents/GitHub`:

```bash
./scripts/export-agent-core-pack.sh
```

Export a subset of repositories:

```bash
./scripts/export-agent-core-pack.sh --repos nanobot,openfang
```

Choose a base directory, output directory, and archive name:

```bash
./scripts/export-agent-core-pack.sh \
  --base-dir ~/Documents/GitHub \
  --output-dir ./out \
  --name agent-core-snapshot \
  --repos codex,nullclaw
```

## Rules

- Keep the archive source-only.
- Include only files that directly define agent behavior.
- Exclude tests, build artifacts, dependency folders, unrelated app code, and target-framework metadata.
- If a repository does not match a supported signature, stop and report it instead of guessing.

## References

- Read `references/AGENT_CORE.md` when you need the layer model for interpreting exported files.
