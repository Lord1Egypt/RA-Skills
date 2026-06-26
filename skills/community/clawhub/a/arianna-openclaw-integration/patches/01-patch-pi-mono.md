# Step 1: Apply pi-integration-skill to Pi-mono

**Prerequisite:** Step 0 — exact pi-mono version checked out.

## Action

Apply the [pi-integration-skill](../../pi-integration-skill/SKILL.md) to the pi-mono checkout. This modifies:

- `packages/coding-agent/src/core/playfilo-db.ts` (new — DAG storage module)
- `packages/coding-agent/src/core/sdk.ts` (tool registration)
- `packages/coding-agent/src/core/session-manager.ts` (persist shim, DAG read hook)
- `packages/coding-agent/src/core/agent-session.ts` (metadata provider, auto-continue, null checks)
- `packages/coding-agent/package.json` (dependencies)

If the pi-mono version differs from the one the pi-integration-skill was written for, read the [v0.61.1-adaptations.md](../../pi-integration-skill/patches/v0.61.1-adaptations.md) for guidance on adapting to structural changes.

## Build

```bash
cd <pi-mono>/packages/coding-agent
pnpm install  # from repo root if needed
pnpm run build
```

## Verify

```bash
# All four compiled files must exist
ls dist/core/playfilo-db.js dist/core/sdk.js dist/core/session-manager.js dist/core/agent-session.js
```

The compiled output in `dist/core/` is what gets copied into the pnpm patch in step 2.
