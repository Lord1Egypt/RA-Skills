# fourok Retrieval OpenClaw Skill

This directory is the source of truth for the OpenClaw skill-hub artifact.
It is a CLI-first client package: OpenClaw agents use the public `fourok`
CLI and the colocated `SKILL.md` instructions to retrieve source-backed
context from an existing fourok backend.

It intentionally contains only client-facing assets and avoids bundling the
full local runtime stack, connector import pipeline, or operator surfaces.

## Commands exposed to agents

```bash
fourok status
fourok retrieve "<query>" --json
fourok open <source_ref>
fourok onboard
```

## Build artifact

```bash
uv run fourok-dev build-openclaw-skill
uv run fourok-dev validate-openclaw-skill
```
