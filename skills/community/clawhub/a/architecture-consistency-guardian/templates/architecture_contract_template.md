# Architecture Contract

> Last updated: YYYY-MM-DD

## 1. Canonical Sources of Truth

| Domain | Canonical File | Notes |
|--------|---------------|-------|
| | | |

## 2. Canonical State Values

### [Entity Name]

| State | Meaning | Allowed Transitions |
|-------|---------|-------------------|
| | | |

**Retired states** (must not appear in new code):
- [old_state] — replaced by [new_state]

## 3. Canonical Entry Points

| Operation | Entry Module | Bypass Allowed? |
|-----------|-------------|----------------|
| | | |

## 4. Retired Components

| Component | Retired Date | Replacement | Residual Locations |
|-----------|-------------|-------------|-------------------|
| | | | |

## 5. Compatibility Layers

| Layer | Location | Reason | Removal Condition |
|-------|----------|--------|-------------------|
| | | | |

## 6. Rules

1. **Single write path**: Every data store has exactly one write gateway module.
2. **Config from source**: No hardcoded paths; all paths from the canonical config.
3. **State from authority**: State reads/writes only through the lifecycle manager.
4. **No silent fallback**: Exception handlers must not route to retired modules.
5. **Doc sync**: Code changes to documented flows must update docs in the same pass.
