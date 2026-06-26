# openclaw v2026.5.7 + pi-mono v0.73.0 integration

Porting the Playfilo shared-memory DAG integration forward from v2026.3.x.

## Changes

### 1. Playfilo Extension (`extensions/playfilo/`)

Re-introduced the Playfilo extension to handle system context injection (PAX identity and incubation seed). In v2026.5.7, a plugin manifest (`openclaw.plugin.json`) is required for proper discovery and activation.

- `extensions/playfilo/package.json`: NPM package metadata.
- `extensions/playfilo/openclaw.plugin.json`: OpenClaw plugin manifest (New in v2026.5.7).
- `extensions/playfilo/index.ts`: Implementation of `before_prompt_build` hook for context injection.

### 2. Tool Allowlist (`src/agents/pi-embedded-runner/tool-name-allowlist.ts`)

Updated the tool allowlist mechanism to include temporal tools (`life`, `recall`, `trace`, `tobe`). 

- Isolated `PLAYFILO_TOOL_NAMES` to avoid side effects on standard built-in conflict checks.
- Updated `collectAllowedToolNames` to auto-inject these tools. This ensures that even when OpenClaw applies strict tool policies (e.g. in group chats or restricted agents), the temporal navigation tools remain available.

### 3. Unit Tests (`src/agents/pi-embedded-runner/tool-name-allowlist.test.ts`)

Updated unit tests to reflect the auto-inclusion of temporal tools.

## Implementation Details

### `extensions/playfilo/openclaw.plugin.json` (New)

```json
{
  "id": "playfilo",
  "name": "Playfilo",
  "description": "Shared-memory DAG with temporal tools.",
  "activation": {
    "onStartup": true
  },
  "enabledByDefault": true,
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

### `extensions/playfilo/index.ts`

```typescript
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

const SEED_PATH = join(homedir(), ".playfilo", "INCUBATION_SEED.md");

const PAX_IDENTITY = `# IDENTITY: PAX
// ... (Identity Content) ...
`;

const plugin = {
	id: "playfilo",
	name: "Playfilo",
	// ...
	api.on("before_prompt_build", async () => ({
		prependSystemContext: (seedContent ? seedContent + "\n\n" : "") + PAX_IDENTITY,
	}));
	// ...
};
```

## Patches

### `src/agents/pi-embedded-runner/tool-name-allowlist.ts`

```patch
--- a/src/agents/pi-embedded-runner/tool-name-allowlist.ts
+++ b/src/agents/pi-embedded-runner/tool-name-allowlist.ts
@@ -6,6 +6,11 @@
  */
 export const PI_RESERVED_TOOL_NAMES = ["bash", "edit", "find", "grep", "ls", "read", "write"];
 
+/**
+ * Tools required for Playfilo shared-memory DAG and temporal navigation.
+ */
+export const PLAYFILO_TOOL_NAMES = ["life", "recall", "trace", "tobe"];
+
 function addName(names: Set<string>, value: unknown): void {
   if (typeof value !== "string") {
     return;
@@ -21,7 +26,10 @@
   tools: AgentTool[];
   clientTools?: ClientToolDefinition[];
 }): Set<string> {
   const names = new Set<string>();
+  for (const name of PLAYFILO_TOOL_NAMES) {
+    names.add(name);
+  }
   for (const tool of params.tools) {
     addName(names, tool.name);
   }
```

### `src/agents/pi-embedded-runner/tool-name-allowlist.test.ts`

```patch
--- a/src/agents/pi-embedded-runner/tool-name-allowlist.test.ts
+++ b/src/agents/pi-embedded-runner/tool-name-allowlist.test.ts
@@ -23,7 +23,9 @@
       ],
     });
 
-    expect([...names]).toEqual(["read", "memory_search", "image_generate"]);
+    expect([...names].toSorted()).toEqual(
+      ["read", "memory_search", "image_generate", "life", "recall", "trace", "tobe"].toSorted(),
+    );
   });
 
   it("builds a stable Pi session allowlist from custom tool names", () => {
@@ -65,6 +67,8 @@
       }),
     );
 
-    expect(allowlist).toEqual(["exec", "image_generate", "read"]);
+    expect(allowlist).toEqual(
+      ["exec", "image_generate", "read", "life", "recall", "trace", "tobe"].toSorted(),
+    );
   });
 });
```
