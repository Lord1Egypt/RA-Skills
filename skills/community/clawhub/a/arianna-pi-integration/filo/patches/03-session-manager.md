# Step 3: Persistence Shim in `session-manager.ts`

**File:** `packages/coding-agent/src/core/session-manager.ts`
**Six injection points** (3a–3f)

## 3a. Imports

Add after existing imports:

```typescript
import {
  checkTobeAbortState, commitNodeWithExternalId, consumePendingIncarnateLog,
  getHashByExternalId, getRef, loadEntriesFromDAG, logAction, setRef, storeBlob,
} from "./playfilo-db.js";
```

(`clearRef` is **not** imported here — see Step 3d for why `newSession()` must not clear PI_HEAD. The tobe handler in `sdk.ts` (Step 2, Tool 1) is the only place that calls `clearRef("PI_HEAD")`, and it imports it directly.)

## 3b. PlayfiloMetadata Interface + Provider

Add **before** the `SessionManager` class definition:

```typescript
/** Metadata captured at persist-time for Playfilo DAG storage. */
export interface PlayfiloMetadata {
  systemPrompt: string | null;
  model: { provider: string; modelId: string } | null;
  thinkingLevel: string;
  tools: { name: string; description: string }[];
}
```

Inside the class, add as **private field** alongside other fields:

```typescript
private _metadataProvider: (() => PlayfiloMetadata) | null = null;
```

Add as **public method**:

```typescript
/** Set a callback that provides current agent metadata for Playfilo DAG storage. */
setMetadataProvider(provider: () => PlayfiloMetadata): void {
  this._metadataProvider = provider;
}
```

## 3c. DAG Read Hook in `setSessionFile()`

Find `setSessionFile()`. It currently has a line like:

```typescript
this.fileEntries = loadEntriesFromFile(this.sessionFile);
```

**Replace** it with the DAG read hook:

```typescript
// --- PLAYFILO READ HOOK ---
const rawEntries = loadEntriesFromFile(this.sessionFile);
const fileHeader = rawEntries.find((e) => e.type === "session");
const lastEntry = rawEntries.length > 0 ? rawEntries[rawEntries.length - 1] : null;
let targetHash: string | null = null;
if (lastEntry && lastEntry.type !== "session") {
  targetHash = getHashByExternalId(lastEntry.id);
}
if (targetHash) {
  const dagEntries = loadEntriesFromDAG(targetHash);
  this.fileEntries = fileHeader ? [fileHeader, ...dagEntries] : dagEntries;
  setRef("PI_HEAD", targetHash);
  logAction("BOOT", null, targetHash);
} else {
  this.fileEntries = rawEntries;
}
// --- END READ HOOK ---
```

**Why:** On resume, Pi loads history from the DAG instead of raw JSONL. This preserves cross-agent branches and tobe jump history.

## 3d. PI_HEAD in `newSession()` — intentionally NOT cleared

**Do not** add `clearRef("PI_HEAD")` to `newSession()`. Leave the existing reset block as-is:

```typescript
this.leafId = null;
this.flushed = false;
// (no clearRef("PI_HEAD") here — see rationale below)
```

**Why:** PI_HEAD is the cross-session anchor that the tobe handler in `sdk.ts` (Step 2, Tool 1) deliberately sets to a chosen parent hash *before* the agent loop tears down and rebuilds. The carryover follow-up message and any tail messages must commit as children of that hash. Clearing PI_HEAD inside `newSession()` would unconditionally wipe that anchor — the next `_persist()` would commit a disconnected root node, breaking boot inheritance and severing the lineage that `life()`/`trace()`/`tobe`-replay all depend on.

The "trace shows stale data until first persist" cosmetic is acceptable: the first `_persist()` call advances PI_HEAD, and the stale view collapses to a single intermediate node — far cheaper than losing DAG continuity across context swaps.

If you have an integration history that already applied a `clearRef("PI_HEAD")` here, remove it. (See Mirin's v0.61.1 / v0.73.0 historical patches under `mirin/patches/` for the diff against an older revision of this step.)

## 3e. Persistence Shim in `_persist()`

Find `_persist(entry: SessionEntry)`. Add the shim **at the very top**, before the existing file-append logic:

```typescript
_persist(entry: SessionEntry): void {
  // --- PLAYFILO SHIM INJECTION (V3 LINGUA FRANCA) ---
  try {
    if (checkTobeAbortState()) {
      // Fall through to native JSONL persist below — only skip the DAG commit
    } else {
      const parentHash: string | null = getRef("PI_HEAD");
      const blobHashes: string[] = [];
      let role = "pi_internal";

      if (entry.type === "message") {
        role = entry.message.role;
        if (role === "toolResult") {
          const msg = entry.message as any;
          blobHashes.push(
            storeBlob("tool_result", {
              toolCallId: msg.toolCallId, toolName: msg.toolName,
              content: msg.content, isError: msg.isError,
            }),
          );
        } else if ("content" in entry.message && Array.isArray(entry.message.content)) {
          for (const part of entry.message.content) {
            if (part.type === "text") blobHashes.push(storeBlob("text", part.text));
            else if (part.type === "thinking") blobHashes.push(storeBlob("thinking", part.thinking));
            else if (part.type === "toolCall")
              blobHashes.push(storeBlob("tool_call", { id: part.id, name: part.name, arguments: part.arguments }));
            else blobHashes.push(storeBlob("pi_meta", part));
          }
        } else {
          blobHashes.push(storeBlob("pi_meta", entry.message));
        }
      } else {
        blobHashes.push(storeBlob("pi_meta", entry));
      }

      let configJson: string | undefined;
      let systemPromptHash: string | undefined;
      if (this._metadataProvider) {
        const meta = this._metadataProvider();
        if (meta.systemPrompt) {
          systemPromptHash = storeBlob("system_prompt", meta.systemPrompt);
        }
        configJson = JSON.stringify({
          agent: "pi",
          model: meta.model ? { provider: meta.model.provider, id: meta.model.modelId } : null,
          thinkingLevel: meta.thinkingLevel,
          tools: meta.tools,
        });
      }

      const newHash = commitNodeWithExternalId(
        parentHash, role, blobHashes, entry.id, configJson, systemPromptHash,
      );
      setRef("PI_HEAD", newHash);
      consumePendingIncarnateLog(newHash, role);
    }
  } catch (e) {
    console.error("[Playfilo Shim] DB write failed:", e);
  }
  // --- END SHIM ---

  // ... existing file-append logic follows ...
```

**Blob type mapping:**

| Pi content part | Blob type | Content stored |
|---|---|---|
| `{ type: "text", text }` | `"text"` | The text string |
| `{ type: "thinking", thinking }` | `"thinking"` | The thinking string |
| `{ type: "toolCall", id, name, arguments }` | `"tool_call"` | `{ id, name, arguments }` |
| ToolResultMessage | `"tool_result"` | `{ toolCallId, toolName, content, isError }` |
| Image, custom parts | `"pi_meta"` | The raw part object |
| Non-message entries | `"pi_meta"` | The raw entry object |
| System prompt (via metadata) | `"system_prompt"` | The full prompt string |

## 3f. Defensive Null Checks for DAG-Loaded Entries

DAG-loaded entries (via `loadEntriesFromDAG`) may lack fields Pi's native code expects.

**In `buildSessionContext()` (same file):** Find where `model` is extracted from assistant messages. The original code does:

```typescript
model = { provider: entry.message.provider, modelId: entry.message.modelId };
```

Replace with a null-safe version:

```typescript
const msg = entry.message as any;
if (msg.provider && msg.model) {
  model = { provider: msg.provider, modelId: msg.model };
}
```

## Verify

```bash
cd packages/coding-agent && npm run build
```

At this point, sending a message to Pi should create nodes in `~/.playfilo/playfilo.db`. Verify:

```bash
sqlite3 ~/.playfilo/playfilo.db "SELECT id, role, timestamp FROM nodes ORDER BY timestamp DESC LIMIT 3;"
```
