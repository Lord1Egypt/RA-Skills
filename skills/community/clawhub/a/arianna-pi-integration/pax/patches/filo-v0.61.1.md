# Version 0.61.1-graduate-v1-pax

## Fix: Prioritize Merkle Hash Resolution in tobe-resolver

When a user provides a hash prefix (e.g., `bc3b8560`), the system should prioritize matching it against the historical Merkle graph before attempting to resolve it as a transient session UUID (external_id). 

In `pi-integration-v3`, `handleLife` and `handleRecall` prioritized `getHashByExternalId` (UUID) over `resolveNodeId` (Merkle), causing collisions where a session UUID shadowed a historical graduation marker.

### Changes in `packages/coding-agent/src/core/playfilo-db.ts`:

1.  **`handleLife`**: Consolidated resolution logic. Now checks `resolveNodeId` (Merkle) first, then `getHashByExternalId` (UUID) as a fallback.
2.  **`handleRecall`**: Swapped resolution order to Merkle-first.
3.  **Error Handling**: If both resolution paths fail, a combined error message is returned.

### Implementation Details:

#### 1. `handleLife` Resolution Refactor

**Before:**
```typescript
	// Also try resolving external_id to hash for Pi compatibility
	const resolvedExternal = getHashByExternalId(focusId);
	if (resolvedExternal) focusId = resolvedExternal;

	if (focusId !== headId) {
		const resolved = resolveNodeId(focusId);
		if ("error" in resolved) return resolved.error;
		focusId = resolved.id;
	}
```

**After:**
```typescript
	const resolved = resolveNodeId(focusId);
	if (!("error" in resolved)) {
		focusId = resolved.id;
	} else {
		const resolvedExternal = getHashByExternalId(focusId);
		if (resolvedExternal) {
			focusId = resolvedExternal;
		} else if (focusId !== headId) {
			// Only return error if it does not match HEAD
			return `Error: Node "${focusId}" not found (as hash prefix or external UUID).`;
		}
	}
```

#### 2. `handleRecall` Resolution Refactor

**Before:**
```typescript
	} else {
		const resolvedExternal = getHashByExternalId(targetHash);
		if (resolvedExternal) {
			targetHash = resolvedExternal;
		} else {
			const resolved = resolveNodeId(targetHash);
			if ("error" in resolved) return resolved.error;
			targetHash = resolved.id;
		}
	}
```

**After:**
```typescript
	} else {
		const resolved = resolveNodeId(targetHash);
		if (!("error" in resolved)) {
			targetHash = resolved.id;
		} else {
			const resolvedExternal = getHashByExternalId(targetHash);
			if (resolvedExternal) {
				targetHash = resolvedExternal;
			} else {
				return `Error: Node "${targetHash}" not found (as hash prefix or external UUID).`;
			}
		}
	}
```
