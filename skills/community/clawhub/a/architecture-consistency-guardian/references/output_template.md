# Consistency Report Template

Use this template for the Phase 8 structured report.

## Report Structure

```markdown
## Consistency Report

### 1. Classification
- **Category**: [naming | state-machine | config-path | entry-point | schema | legacy-cleanup | doc-alignment | cross-module]
- **Sub-categories** (if applicable): [list]
- **Trigger**: [What prompted this task]

### 2. Source of Truth
- **Canonical file/module**: [path]
- **Competing sources found**: [list or "none"]
- **Resolution**: [which survived, which retired]

### 3. Scope
- **Files modified**: [count]
- **Files scanned**: [count]
- **Repos involved**: [list]

| File | Change Type | Description |
|------|------------|-------------|
| path/to/file.py | renamed field | old_name → new_name |
| path/to/other.py | removed fallback | deleted legacy import path |
| ... | ... | ... |

### 4. Changes Made
[Concise description of what was unified/renamed/removed/updated, grouped logically]

### 5. Residual Compatibility
| Item | Location | Reason for Retention | Removal Condition |
|------|----------|---------------------|-------------------|
| old_function() | module.py:42 | External dep X | After X migrates |
| ... | ... | ... | ... |

If none: "No residual compatibility layers remain."

### 6. Verification
| Check | Result |
|-------|--------|
| grep old names | 0 hits / N hits (explained) |
| test suite | passed / N failures (explained) |
| config resolution | verified in real layout |
| ... | ... |

### 7. Follow-up Risks (optional)
- [Risk 1: description and suggested mitigation]
- [Risk 2: description and suggested mitigation]
```

## Compact Format

For smaller changes, use this condensed version:

```markdown
## Consistency Report
- **Category**: naming
- **Source of truth**: runtime_config.py
- **Scope**: 4 files modified, 12 scanned
- **Changes**: Unified `db_path` / `DB_PATH` / `database_path` → `DB_PATH` from runtime_config
- **Residual**: None
- **Verification**: grep old names = 0 hits; test suite passed (13/13)
- **Risks**: None identified
```

## Anti-patterns in Reports

Do NOT write reports like:
- ❌ "Fixed the issue." (no detail)
- ❌ "Refactored the module." (no scope)
- ❌ "Updated all references." (no proof)
- ❌ "Everything should be consistent now." (no verification)

Every claim must be backed by a concrete action or check result.
