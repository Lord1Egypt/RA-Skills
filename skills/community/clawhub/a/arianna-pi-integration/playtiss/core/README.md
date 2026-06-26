# `playtiss/core/playfilo-db.ts`

Playtiss-backed equivalent of `filo/playfilo-db.ts`. Drop-in replacement: same public API, same on-disk schema, same hash format for legacy rows. Patches written against `filo/playfilo-db.ts` (Mirin's, Pax's, future graduates') apply unchanged because every export keeps its signature and observable behavior.

## Design choice: hybrid (same schema, playtiss `StorageProvider` for blobs)

Three options were on the table during Dispatch 1:

1. **Pure same-schema wrapper.** Keep raw `better-sqlite3` for everything. Don't import `@playtiss/core` at all. Trivially backward-compatible but doesn't actually use playtiss.
2. **Different-schema clean cut.** New schema where every node IS a CID-keyed blob. Use `computeStorageBlock` for everything. Different DB file. Loses backward compat with `~/.playfilo/playfilo.db`.
3. **Hybrid.** Same Filo schema, same Filo hash for `nodes` / `refs` / `action_log`, but expose a `StorageProvider` over the `blobs` table and add async `storeAsset` / `loadAsset` helpers for callers who want true playtiss content addressing.

We picked option 3.

**Why:**

- **Retcon does it this way.** `retcon/src/storage.ts` (`SqliteStorageProvider`) implements `StorageProvider` for retcon's `blobs` table. Retcon's `events`, `revisions`, `branch_views`, and `sessions` tables are plain columnar SQL — they don't go through playtiss at all. The "use playtiss the way the canonical consumer uses it" pattern lands here.
- **Filo's hash is incompatible with playtiss's CID format.** Filo uses sorted-keys `JSON.stringify` + SHA-256 hex (e.g. `a3f5e2c1...`). Playtiss uses `dag-json` + multiformats CID (e.g. `bafkrei...`). They produce different hashes for the same logical content. Switching everything to playtiss CIDs would orphan every existing on-disk DB, every recorded `action_log.from_node` / `to_node`, and every `external_id` ↔ hash mapping. The 100%-reversibility constraint forbids that breakage.
- **Mirin/Pax patches must apply unchanged.** Mirin's three v0.61.1 fixes touch `consumePendingIncarnateLog`, `clearRef("PI_HEAD")`, and detector lambdas. Pax's fix swaps resolution priority in `handleLife` / `handleRecall`. Neither cares about hash format — both just need the same exports with the same signatures.

## What's added on top of the Filo API

The Filo public surface is preserved 1:1. Additions:

| Symbol | Purpose |
|---|---|
| `SqliteBlobStorageProvider` | `@playtiss/core` `StorageProvider` implementation backed by the `blobs` table. Reads/writes byte buffers keyed by `AssetId` (CID string). |
| `getStorageProvider()` | Module-singleton accessor. Pass into `@playtiss/core`'s `load` / `resolve` / `store` from external callers. |
| `storeAsset(value)` | Persist any `AssetValue` via `@playtiss/core`'s content-addressed store. Returns the playtiss CID. Idempotent. |
| `loadAsset(id)` | Load a previously-stored `AssetValue` by its playtiss CID. |
| `hashContentPlaytiss(value)` | Compute the playtiss CID of a value without persisting (dedup checks, pre-write hashing). |
| `computeAssetBlock(value)` | Pre-compute the `{cid, bytes}` pair without going through the provider. Useful for embedding CIDs in parent blobs before saving. |

These additions are **opt-in**. Filo-shape callers (the Mirin patches, the Pax patches, every existing call site in `pi-mono/packages/coding-agent`) ignore them and continue working with `storeBlob`, `commitNodeWithExternalId`, `getRef`, `setRef`, `loadEntriesFromDAG`, etc.

## Coexistence in the `blobs` table

Filo blobs use `type IN ('text', 'thinking', 'tool_call', 'tool_result', 'pi_meta', 'pi_entry', 'inline_data')` and `hash` is a 64-char SHA-256 hex string.

Playtiss blobs use `type = 'playtiss'` and `hash` is a multiformats CID (typically starts `bafkrei...`). The `content` column stores the byte buffer base64-encoded so the existing `TEXT NOT NULL` schema accommodates it without a migration. (A future schema bump could add a native `BLOB` column for byte storage; out of scope for Dispatch 1.)

The two row formats can't collide on `hash` because their alphabets and lengths differ. Both kinds of rows sit in the same table, looked up by their respective callers.

## What stays as raw better-sqlite3

Every domain-semantics function:

- `nodes` writes (`commitNodeWithExternalId`, `commitTobeDeparture`)
- `nodes` reads (`getNodeParent`, `getHashByExternalId`, `getExternalIdByHash`, `nodeExists`, `resolveNodeId`, `loadEntriesFromDAG`)
- `refs` operations (`getRef`, `setRef`, `clearRef`)
- `action_log` operations (`logAction`, `consumePendingIncarnateLog`, `setPendingIncarnateLog`)
- `tobeAbortState` machinery (`setTobeAbortState`, `checkTobeAbortState`, `consumePendingTobeContext`)
- Tool handlers (`handleLife`, `handleRecall`, `handleTrace`)

All of these depend on Filo's specific hash algorithm + schema + column shapes. Wrapping them in `@playtiss/core` primitives would either change observable behavior (different hashes) or add zero value (just paraphrasing SQL through a generic interface).

## Importing the module

Same as the Filo file:

```typescript
import {
  // Filo-shape API (unchanged)
  storeBlob,
  hashContent,
  commitNodeWithExternalId,
  loadEntriesFromDAG,
  getRef, setRef, clearRef,
  getHashByExternalId, getExternalIdByHash,
  resolveNodeId, nodeExists,
  setTobeAbortState, checkTobeAbortState, consumePendingTobeContext,
  commitTobeDeparture,
  setPendingIncarnateLog, consumePendingIncarnateLog,
  logAction,
  handleLife, handleRecall, handleTrace,

  // Playtiss-shape additions
  SqliteBlobStorageProvider,
  getStorageProvider,
  storeAsset, loadAsset,
  hashContentPlaytiss,
  computeAssetBlock,
} from "./playfilo-db.js";
```

## Required dependency

This module imports `@playtiss/core`. Add to `packages/coding-agent/package.json`:

```bash
cd packages/coding-agent
pnpm add @playtiss/core
# (better-sqlite3 should already be present from the Filo step)
```

## When to use which

- **Filo-shape (`storeBlob` / `hashContent`)**: anywhere existing code expects the legacy 64-char hex hash. All current pi-mono integration paths.
- **Playtiss-shape (`storeAsset` / `hashContentPlaytiss`)**: new code that wants Merkle-DAG semantics across nested objects, or that needs to interoperate with other `@playtiss/core` consumers (retcon, future SDK tooling). Returns a CID string, which is NOT interchangeable with the Filo hex hash even for the same logical content.

Don't mix them in a single `parts_list` array unless the caller knows which lookup path each blob belongs to — `loadEntriesFromDAG` only knows how to interpret Filo-shape blob types.

## Future work

- **Blob column type.** Add a `bytes BLOB` column in a v5 schema migration so playtiss blobs can store native binary instead of base64-encoded TEXT. Saves ~33% disk on playtiss-shape blobs.
- **Reference tracking.** `SqliteBlobStorageProvider.saveBuffer` accepts `references` (per `@playtiss/core`'s `AssetReferences`) but doesn't persist them. v1.1+ GC would wire these up via a separate join table.
- **Migration helper.** A function that walks the existing Filo nodes/blobs and produces a playtiss-CID mirror for any caller that wants to exchange Pi DAGs with retcon-shape consumers.
