# Changelog - agent-workspace-manager v1.1.0

## New Features

### 1. Code File Classification Rules
- Added classification rules for `.sql`, `.py`, `.sh` files
- SQL files now have dedicated directories:
  - `knowledge/sql/` for core business SQL
  - `templates/sql/` for reusable query templates
  - `archives/sql_versions/` for historical SQL versions
- Python and Shell scripts now belong in `scripts/`

### 2. Duplicate File Detection
- Added methods to detect duplicate files:
  - Name pattern detection (version suffixes like `_v1`, `_最终版`, `_修正版`)
  - Content similarity detection (>80% overlap)
  - Functional similarity detection (multiple files serving same purpose)
- Detection commands provided for `.sql` and `.md` files

### 3. File Naming Best Practices
- Added comprehensive naming guidelines:
  - ✅ DO: Use semantic names (e.g., `神策宽表转JSON.sql`)
  - ❌ DON'T: Use version suffixes (e.g., `file_v1.md`, `file_最终版.sql`)
- Version management guidelines for SQL files
- Merge vs Archive decision flowchart

## Improvements

### Workspace Health Check
- Enhanced to detect version-suffixed files
- Added SQL-specific cleanup workflow
- Added code file duplicate detection

### Classification Rules
- Updated `classification-rules.md` with code file examples
- Added common misclassification examples for SQL files
- Added file naming violation detection

## Structure Updates

### New Directories
- `knowledge/sql/` - Core business SQL queries
- `templates/sql/` - Reusable SQL templates
- `archives/sql_versions/` - Historical SQL versions
- `scripts/` - Utility scripts (Python, Shell)

### Updated Structure Template
```
workspace/
├── knowledge/
│   └── sql/               # NEW
├── templates/
│   └── sql/               # NEW
├── archives/
│   └── sql_versions/      # NEW
└── scripts/               # NEW
```

## Breaking Changes
- None (backward compatible)

## Migration Guide
For existing workspaces with SQL files:
1. Move core SQL files to `knowledge/sql/`
2. Rename files to remove version suffixes
3. Archive historical versions to `archives/sql_versions/`
4. Use `workspace_audit.py` to detect duplicates

## Files Changed
- `SKILL.md` - Added code file classification, duplicate detection, naming rules
- `references/classification-rules.md` - Added code file rules, duplicate detection, naming best practices

## Version
- Previous: 1.0.0
- Current: 1.1.0
- Release Date: 2026-03-25
