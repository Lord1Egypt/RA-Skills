# Mirin OpenClaw Integration Patches (v2026.5.7)

This document contains the required modifications and extensions to integrate Playfilo with OpenClaw v2026.5.7. It mirrors the system updates from our previous integrations, adapted for the latest codebase.

## 1. Tool Allowlist Override

**File:** `src/agents/pi-embedded-runner/run/attempt.ts`

**Issue:** OpenClaw filters allowed tool calls to prevent unintended side effects. We need to explicitly allow the Playfilo temporal tools (`life`, `recall`, `trace`, `tobe`) so the embedded agent can execute DAG operations.

**Fix:** Append the temporal tools to the `allowedToolNames` set immediately after it is collected.

```diff
--- a/src/agents/pi-embedded-runner/run/attempt.ts
+++ b/src/agents/pi-embedded-runner/run/attempt.ts
@@ -1084,6 +1084,7 @@
       tools: effectiveTools,
       clientTools,
     });
+    for (const name of ["life", "recall", "trace", "tobe"]) allowedToolNames.add(name);
     const explicitToolAllowlistSources = collectAttemptExplicitToolAllowlistSources({
       config: params.config,
       sessionKey: params.sessionKey,
```

## 2. The Playfilo OpenClaw Extension

**Directory:** `extensions/playfilo`

**Description:** This extension reads the shared `~/.playfilo/INCUBATION_SEED.md` graph context and prepends it to the system context via the `before_prompt_build` hook. This is how the OpenClaw agent discovers its DAG origins and temporal toolset without direct DB layer modifications in the OpenClaw repository.

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

### `extensions/playfilo/index.ts`

```typescript
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

const SEED_PATH = join(homedir(), ".playfilo", "INCUBATION_SEED.md");

const plugin = {
	id: "playfilo",
	name: "Playfilo",
	description: "Shared-memory DAG with temporal tools.",
	register(api: any) {
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
};

export default plugin;
```

## 3. Legacy Patches Retired & SOUL.md Exclusion

Note that previous versions included a patch into `@mariozechner/pi-coding-agent` to inject `playfilo-db.js` into the `dist` folder. In v2026.5.7, we rely on the `pi-mono` build being externally patched before consumption (see Preconditions below). We no longer need to patch `pi-coding-agent` distributions directly via OpenClaw's `package.json`, nor do we need to add `better-sqlite3` to OpenClaw, as the patched `pi-mono` build handles the Playfilo DB hooks natively.

Additionally, the untracked `SOUL.md` found in older OpenClaw integration references is a Filo-namespace identity note, not a functional component loaded by the system. It has been explicitly excluded from this patch bundle and removed from the worktree.

## 4. Preconditions

For this OpenClaw integration to function correctly, the `pi-mono` build resolved by OpenClaw **must** already be patched with the `pi-adapt` v0.73.0 Playfilo DB hooks. The required patches are located at `pi-integration-skill/filo/patches/` and `pi-integration-skill/mirin/patches/filo-v0.73.0.md`. This integration relies on the strict precondition that those patches have natively injected the graph-anchoring capabilities into `pi-mono` *before* OpenClaw resolves the `@mariozechner/pi-coding-agent` dependency.
