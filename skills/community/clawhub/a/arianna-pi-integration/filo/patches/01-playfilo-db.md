# Step 1: Copy `playfilo-db.ts` + Add Dependency

**File:** `packages/coding-agent/src/core/playfilo-db.ts` (new file)
**Source:** `playfilo-db.ts` in this skill's directory

## 1a. Build Environment (pnpm)

If using pnpm instead of npm, the repo needs additional setup because pi-mono was developed with npm's flat `node_modules` hoisting. pnpm uses strict isolation — each package can only resolve its own declared dependencies.

**Create `pnpm-workspace.yaml`** at repo root (mirrors the `"workspaces"` array from `package.json`):

```yaml
packages:
  - "packages/*"
```

**Approve native module builds** — add to root `package.json`:

```json
"pnpm": {
  "onlyBuiltDependencies": ["better-sqlite3", "esbuild", "@parcel/watcher", "protobufjs", "koffi"]
}
```

Without this, pnpm blocks compilation of `better-sqlite3` and other native modules, requiring interactive `pnpm approve-builds` prompts.

**Fix missing transitive dependencies** — these are pre-existing gaps in pi-mono's `package.json` files (not caused by Playfilo). They only surface under pnpm's strict resolution:

| Package | Missing dependency | Why |
|---|---|---|
| `packages/coding-agent` | `ajv` | `model-registry.ts` imports it; resolved transitively under npm |
| `packages/ai` | `@smithy/node-http-handler` | `amazon-bedrock.ts` dynamic import; transitive via `@aws-sdk/client-bedrock-runtime` |
| `packages/agent` | `@sinclair/typebox` | `types.ts` imports it; transitive via `@mariozechner/pi-ai` |
| `packages/web-ui` | `@mariozechner/pi-agent-core` | Multiple source files import Agent/AgentEvent |
| `packages/web-ui` | `@sinclair/typebox` | Tool files import `Type` |
| `packages/web-ui` | `highlight.js` | Artifact tool files use it for syntax highlighting |
| `packages/web-ui` (dev) | `tailwindcss` | CSS import needs core package, not just `@tailwindcss/cli` |

Add each with `pnpm add <package>` in the respective package directory. Skip this section if using npm (flat hoisting resolves these automatically).

## 1b. Copy Source File

```bash
cp playfilo-db.ts /path/to/pi-mono/packages/coding-agent/src/core/playfilo-db.ts
```

## 1c. Add `better-sqlite3` Dependency

If `better-sqlite3` is not already a dependency of `packages/coding-agent`:

```bash
cd /path/to/pi-mono/packages/coding-agent
pnpm add better-sqlite3
pnpm add -D @types/better-sqlite3
```

## What this file does

Self-contained DAG storage module. All SQLite operations, blob storage, node commits, and tool handlers live here. No other file needs to know about SQLite.

- Module-level `db` singleton opened at import time (`~/.playfilo/playfilo.db`, WAL mode)
- Schema V4 created via `CREATE TABLE IF NOT EXISTS` (safe for concurrent access)
- All exports are pure functions operating on the module-level `db`

## Verify

```bash
# Build should succeed with the new file present
cd packages/coding-agent && npm run build
```

The file is inert until imported — no side effects until step 2+ import it.
