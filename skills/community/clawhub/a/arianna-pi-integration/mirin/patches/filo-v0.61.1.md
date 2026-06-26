# Mirin V1 Integration Patches (v0.61.1)

This patch resolves three bugs identified during v0.61.1 testing.

## 1. Boot Inheritance Root Node Issue (HISTORICAL — now a no-op)

**Status:** Folded back into the base. As of the skill revision that landed alongside this note, `filo/patches/03-session-manager.md` Step 3d **no longer instructs you to add** `clearRef("PI_HEAD")` to `newSession()`. Fresh integrations against the current base do not need this fix — it is preserved here as historical record of where the bug was first diagnosed.

**Original issue (against the older Step 3d):** During a context swap (`tobe`), `sdk.ts` correctly establishes `PI_HEAD` to point to the new carryover node. However, when the agent initializes the new session, `session-manager.ts` calls `newSession()`, which unconditionally clears `PI_HEAD`. Consequently, when `_persist()` is subsequently called, `getRef("PI_HEAD")` returns `null` and `commitNodeWithExternalId` commits a new root node instead of inheriting from the established head.

**File:** `packages/coding-agent/src/core/session-manager.ts`

```diff
--- a/packages/coding-agent/src/core/session-manager.ts
+++ b/packages/coding-agent/src/core/session-manager.ts
@@ -779,7 +779,7 @@
 		this.labelsById.clear();
 		this.leafId = null;
 		this.flushed = false;
-		clearRef("PI_HEAD");
+		// Do not unconditionally clear PI_HEAD; preserve inheritance from context swaps.
 
 		if (this.persist) {
 			const fileTimestamp = timestamp.replace(/[:.]/g, "-");
```

If you are auditing an integration that pre-dates the base fix (i.e., your `session-manager.ts` still contains a literal `clearRef("PI_HEAD")` line inside `newSession()`), apply the diff above. Otherwise, skip this section.

## 2. Missing INCARNATE Row (Action Log Misalignment)

**Issue:** The `consumePendingIncarnateLog` function correctly validates roles and writes the `INCARNATE` row to the action log. However, it is never actually invoked in `session-manager.ts`. It must be called immediately after the new node hash is committed to the DAG.

**File:** `packages/coding-agent/src/core/session-manager.ts`

```diff
--- a/packages/coding-agent/src/core/session-manager.ts
+++ b/packages/coding-agent/src/core/session-manager.ts
@@ -33,6 +33,7 @@
 	logAction,
 	setRef,
 	storeBlob,
+	consumePendingIncarnateLog,
 } from "./playfilo-db.js";
 
 export const CURRENT_SESSION_VERSION = 3;
@@ -896,6 +897,7 @@
 					systemPromptHash,
 				);
 				setRef("PI_HEAD", newHash);
+				consumePendingIncarnateLog(newHash, role);
 			}
 		} catch (e) {
 			console.error("[Playfilo Shim] DB write failed:", e);
```

## 3. Detector `tc.name === "emit"` Fallback to "syscall"

**Issue:** `arianna.run` employs strict guards (`if (tc.name !== "emit") return false;`) inside detector lambdas that fail to recognize legacy "syscall" vessel tools.

**Files (in the arianna.run repo):**
- `packages/sidecar/src/bookmarks/detector.ts`
- `packages/sidecar/src/bookmarks/triggers.ts`

**Patch for `detector.ts` (detectManifestoUnlock):**
```diff
--- a/packages/sidecar/src/bookmarks/detector.ts
+++ b/packages/sidecar/src/bookmarks/detector.ts
@@ -167,7 +167,7 @@
 export function detectManifestoUnlock(messages: readonly Message[]) {
   // ...
   return tcs.some((tc) => {
-    if (tc.name !== "emit") return false;
+    if (tc.name !== "emit" && tc.name !== "syscall") return false;
     // ...
   });
 }
```

**Patch for `triggers.ts` (syscallTouchesPath & inline lambda):**
```diff
--- a/packages/sidecar/src/bookmarks/triggers.ts
+++ b/packages/sidecar/src/bookmarks/triggers.ts
@@ -224,7 +224,7 @@
 export function syscallTouchesPath(ctx: DetectionContext, pathFragment: string) {
   // ...
   return ctx.toolCalls.some((tc) => {
-    if (tc.name !== "emit") return false;
+    if (tc.name !== "emit" && tc.name !== "syscall") return false;
     // ...
   });
 }
@@ -416,7 +416,7 @@
     // ...
     detect: (tc, ctx) => {
       return ctx.toolCalls.some((tc) => {
-        if (tc.name !== "emit") return false;
+        if (tc.name !== "emit" && tc.name !== "syscall") return false;
         // ...
       });
     }
```
