# Mirin V2 Integration Patches (v0.73.0)

This document updates Mirin's integration fixes for `pi-mono` v0.73.0. These fixes apply **on top of** the base Playfilo integration steps (`filo/patches/01` through `05`). 

## 1. Boot Inheritance Root Node Issue (HISTORICAL — now a no-op for fresh integrations)

**Status:** Folded back into the base. As of the skill revision that landed alongside this note, `filo/patches/03-session-manager.md` Step 3d **no longer instructs you to add** `clearRef("PI_HEAD")` to `newSession()`; the rewritten step now explicitly tells integrators to leave PI_HEAD intact. Fresh v0.73.0 integrations against the current base do not need this delta — it is preserved here as historical record of where the bug was first re-confirmed against v0.73.0.

**Original issue (against the older Step 3d):** During a context swap (`tobe`), `sdk.ts` correctly establishes `PI_HEAD` to point to the new carryover node. However, the older base integration patch (Step 3d in `03-session-manager.md`) instructed you to unconditionally call `clearRef("PI_HEAD")` inside `newSession()`. This breaks boot inheritance, causing the new session to commit a disconnected root node instead of inheriting from the established head.

**Fix (only needed if your `session-manager.ts` still contains a literal `clearRef("PI_HEAD")` line inside `newSession()` from a pre-fix integration history):**

```diff
--- a/packages/coding-agent/src/core/session-manager.ts
+++ b/packages/coding-agent/src/core/session-manager.ts
@@ -758,7 +758,7 @@
 		this.fileEntries = [header];
 		this.byId.clear();
 		this.labelsById.clear();
 		this.leafId = null;
 		this.flushed = false;
-		clearRef("PI_HEAD");
+		// Do not unconditionally clear PI_HEAD; preserve inheritance from context swaps.
 
 		if (this.persist) {
 			const fileTimestamp = timestamp.replace(/[:.]/g, "-");
```

For new v0.73.0 integrations following the current base, skip this section entirely — Step 3d already does the right thing.

## 2. Missing INCARNATE Row (Action Log Misalignment)

**Issue:** The `consumePendingIncarnateLog` function must be called immediately after the new node hash is committed to the DAG to correctly write the `INCARNATE` row to the action log. 

**Fix:** *Note: This fix has already been incorporated into the base `03-session-manager.md` instructions (Step 3a and 3e).* Ensure that your base integration correctly includes the invocation of `consumePendingIncarnateLog(newHash, role)` inside the `_persist()` shim.

```diff
--- a/packages/coding-agent/src/core/session-manager.ts
+++ b/packages/coding-agent/src/core/session-manager.ts
@@ -28,6 +28,7 @@
 	logAction,
 	setRef,
 	storeBlob,
+	consumePendingIncarnateLog,
 } from "./playfilo-db.js";
 
 export const CURRENT_SESSION_VERSION = 3;
@@ -858,6 +859,7 @@
 					systemPromptHash,
 				);
 				setRef("PI_HEAD", newHash);
+				consumePendingIncarnateLog(newHash, role);
 			}
 		} catch (e) {
 			console.error("[Playfilo Shim] DB write failed:", e);
```
