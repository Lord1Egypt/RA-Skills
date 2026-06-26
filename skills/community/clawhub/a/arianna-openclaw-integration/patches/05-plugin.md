# Step 4: Create OpenClaw Playfilo Plugin

**Prerequisite:** Steps 2–3 — patch applied, dependencies installed.

## Why a Plugin

OpenClaw **fully overrides** Pi's system prompt via `applySystemPromptOverrideToSession()`. Pi's native extension system (`~/.pi/agent/extensions/playfilo-seed.ts`) fires during `before_agent_start`, but its output is discarded when OpenClaw sets the system prompt.

OpenClaw's idiomatic injection point is the `before_prompt_build` plugin hook. Its `prependSystemContext` field is composed into the system prompt and applied via `applySystemPromptOverrideToSession()` — surviving the override chain.

## Action

### Create the plugin directory

```bash
mkdir -p ~/openclaw/extensions/playfilo
```

### `extensions/playfilo/openclaw.plugin.json`

```json
{
  "id": "playfilo",
  "name": "Playfilo",
  "description": "Shared-memory DAG integration with temporal tools (life, recall, trace, tobe)."
}
```

### `extensions/playfilo/package.json`

```json
{
  "name": "@openclaw/playfilo",
  "version": "0.0.1",
  "private": true,
  "type": "module",
  "openclaw": {
    "extensions": ["./index.ts"]
  }
}
```

### `extensions/playfilo/api.ts`

```typescript
export { definePluginEntry, type OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-entry";
```

### `extensions/playfilo/index.ts`

```typescript
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import { definePluginEntry, type OpenClawPluginApi } from "./api.js";

const SEED_PATH = join(homedir(), ".playfilo", "INCUBATION_SEED.md");

export default definePluginEntry({
	id: "playfilo",
	name: "Playfilo",
	description: "Shared-memory DAG with temporal tools.",
	register(api: OpenClawPluginApi) {
		let seedContent: string | null = null;
		try {
			seedContent = readFileSync(SEED_PATH, "utf-8").trim();
		} catch {
			api.logger.warn(`Could not read ${SEED_PATH}`);
		}

		api.on("before_prompt_build", async () => ({
			prependSystemContext: seedContent ?? undefined,
		}));
	},
});
```

### Ensure workspace discovery

Verify `extensions/*` is in `~/openclaw/pnpm-workspace.yaml`:

```yaml
packages:
  - extensions/*
```

Then install:

```bash
cd ~/openclaw
pnpm install
```

## What the Plugin Does

1. **At load time:** Reads `~/.playfilo/INCUBATION_SEED.md` (the Filo identity primer + temporal tool descriptions)
2. **Per agent run:** Returns `{ prependSystemContext: seedContent }` from the `before_prompt_build` hook
3. OpenClaw's `composeSystemPromptWithHookContext()` prepends the seed to the system prompt
4. The final composed prompt is applied via `applySystemPromptOverrideToSession()`

The INCUBATION_SEED already contains descriptions of all four temporal tools (life, trace, recall, tobe) in its "Temporal Senses" section. The tools are also in the API tool declarations (registered by the patched `createAgentSession()`). No separate tool guidance section is needed.

## Plugin Auto-Discovery

OpenClaw auto-discovers plugins in the `extensions/` workspace directory. No explicit config enablement is needed. To verify discovery:

```bash
cd ~/openclaw
pnpm tsgo  # type-check should pass
```

## Verify

```bash
# Plugin files exist
ls ~/openclaw/extensions/playfilo/index.ts

# Type-check passes
cd ~/openclaw && pnpm tsgo

# Full build passes
cd ~/openclaw && pnpm build
```
