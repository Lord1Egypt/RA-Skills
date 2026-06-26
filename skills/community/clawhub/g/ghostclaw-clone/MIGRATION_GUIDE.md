# Migrating to Ghostclaw v0.2.0

This guide helps users upgrade from v0.1.x to v0.2.0.

v0.2.0 introduces **storage reorganization**, **JSON5 config support**, **delta enhancements**, and **QMD backend**. All changes are designed to be backward compatible with automatic migration where possible.

---

## Quick Summary

| Aspect | v0.1.x | v0.2.0 | Action Required |
|--------|--------|--------|----------------|
| Storage layout | `.ghostclaw/reports/`, `.ghostclaw/cache/`, `.ghostclaw.db` (root) | `.ghostclaw/storage/reports/`, `.ghostclaw/storage/cache/` (optional), `.ghostclaw/storage/ghostclaw.db` | **None** — automatic migration on first run |
| Config file | `.ghostclaw/ghostclaw.json` (JSON only) | `.ghostclaw/ghostclaw.json` (JSON5 supported) | Optional: add comments/trailing commas; keep existing JSON |
| Delta mode | `--delta --base HEAD~1` | Same + `--delta-summary` flag, exact commit matching | Optional: use `--delta-summary` for CI logs |
| QMD backend | Not available | `--use-qmd` or `use_qmd: true` | Optional install: `pip install ghostclaw[qmd]` |
| Cache location | `.ghostclaw/cache/` | `.ghostclaw/cache/` (unchanged) | None |

---

## Storage Layout Changes

### What Changed

In v0.2.0, all persistent data has been consolidated under `.ghostclaw/storage/` for better organization and easier `.gitignore` management.

**Old layout (v0.1.x):**

```
.ghostclaw/
├── reports/          ← analysis reports (JSON + Markdown)
├── cache/            ← analysis cache (.json.gz)
├── ghostclaw.db      ← SQLite memory database (v0.1.9+)
└── ghostclaw.json    ← local project config
```

**New layout (v0.2.0):**

```
.ghostclaw/
├── cache/                    ← analysis cache (unchanged location)
├── storage/
│   ├── reports/             ← analysis reports (moved from reports/)
│   ├── qmd/                 ← QMD databases (if used)
│   └── ghostclaw.db         ← SQLite DB (moved from root)
└── ghostclaw.json            ← local project config (JSON5 supported)
```

### Automatic Migration

On first run of v0.2.0, the following happens automatically:

1. If `.ghostclaw/reports/` exists → all files moved to `.ghostclaw/storage/reports/`
2. If `.ghostclaw/cache/` exists → all files moved to `.ghostclaw/storage/cache/`
3. If `.ghostclaw/ghostclaw.db` exists → moved to `.ghostclaw/storage/ghostclaw.db`
4. Empty old directories are removed

**No data loss.** The migration is atomic per-file and continues even if some files are locked.

**No configuration needed.** Ghostclaw detects the old layout and migrates silently (a message is printed to stderr).

---

## JSON5 Configuration

### What Changed

Ghostclaw now supports **JSON5** format for configuration files when the `json5` package is installed. JSON5 allows:

- Comments (`//` or `/* */`)
- Trailing commas
- Unquoted keys (technically allowed but we keep quotes for clarity)
- Multi-line strings

**Example `~/.ghostclaw/ghostclaw.json` (JSON5):**

```json5
{
  // AI settings
  use_ai: false,
  ai_provider: "openrouter",
  ai_model: "anthropic/claude-3.5-sonnet",  // trailing comma OK

  // Delta mode for PR reviews
  delta_mode: false,
  delta_base_ref: "HEAD~1",
}
```

### Backward Compatibility

- Plain JSON files continue to work without any changes.
- If `json5` is not installed, Ghostclaw falls back to stdlib `json` automatically.
- `ghostclaw init` will write JSON5 if `json5` is available, else plain JSON.

**No action required.** Your existing `.ghostclaw/ghostclaw.json` (plain JSON) will still be read correctly.

---

## Delta-Context Enhancements

### Exact Commit Matching

When using `--delta --base <ref>`, Ghostclaw now tries to find a report that exactly matches the commit SHA of the base reference, instead of just picking the latest report.

**Behavior:**

- If you run `ghostclaw . --delta --base origin/main`:
  1. Ghostclaw runs `git rev-parse origin/main` to get the SHA (e.g., `a1b2c3d`)
  2. Scans `.ghostclaw/storage/reports/*.json` for one with `metadata.vcs.commit == "a1b2c3d"`
  3. If found → uses that report as baseline (exact match)
  4. If not found → falls back to the latest report and prints a warning to stderr

This ensures accurate architectural drift detection even when you have multiple baseline reports.

**No special configuration needed.** The feature works automatically as long as your baseline reports include VCS metadata (v0.2.0+ includes it by default).

### `--delta-summary` Flag

Print diff statistics (files changed, insertions, deletions) to stderr after analysis completes.

Useful for CI logs and quick metrics:

```bash
ghostclaw . --delta --base HEAD~3 --delta-summary
```

Output example:

```
=== Delta Summary ===
Files changed: 5
Insertions: +42
Deletions: -17
```

---

## QMD Backend (Experimental)

### What is QMD?

QMD (Quantum Memory Database) is an experimental high-performance alternative to SQLite for storing and searching architectural history. It provides faster search and hybrid (keyword + semantic) capabilities.

### Enabling QMD

**Option 1: CLI flag**

```bash
ghostclaw . --use-qmd
```

**Option 2: Config file**

```json5
{
  use_qmd: true
}
```

**Option 3: MCP environment variable**

```bash
export GHOSTCLAW_USE_QMD=1
ghostclaw-mcp
```

### Installation

QMD support requires the optional dependency:

```bash
pip install ghostclaw[qmd]
```

If you try to use `--use-qmd` without the `qmd` package, Ghostclaw will fall back to SQLite and print a warning.

### How It Works

- When `use_qmd=True`, Ghostclaw enables **both** the `sqlite` and `qmd` storage adapters (dual-write).
- All analysis results are written to both backends, ensuring you can switch back at any time.
- MCP tools (`ghostclaw_memory_search`, etc.) will automatically use QMD if enabled.
- QMD database is stored at `.ghostclaw/storage/qmd/ghostclaw.db` (separate from SQLite).

### Performance

Current implementation uses SQLite for QMD adapter (same as default), so no performance gain yet. Future versions will integrate a true vector-capable backend. The infrastructure is in place for a drop-in replacement.

**Status:** Experimental. SQLite remains the production default.

---

## What Should I Do?

### Before upgrading

1. **Backup your `.ghostclaw/` directory** (optional but recommended):

   ```bash
   cp -r .ghostclaw .ghostclaw.backup
   ```

2. **Ensure you have a recent full analysis report** if you rely on delta mode:

   ```bash
   git checkout main  # or your baseline branch
   ghostclaw . --use-ai
   git add .ghostclaw/storage/reports/
   git commit -m "Baseline report for delta mode"
   ```

### After upgrading

1. Run a full analysis to trigger migration (if using legacy layout):

   ```bash
   ghostclaw . --use-ai
   ```

   You'll see a message if migration occurs: `🔧 Migrated storage to new layout under .ghostclaw/storage/`

2. Verify your reports are accessible:

   ```bash
   ls .ghostclaw/storage/reports/
   ```

3. (Optional) Try delta mode with exact commit matching:

   ```bash
   # Compare current branch against main's last commit
   ghostclaw . --delta --base main
   ```

4. (Optional) Enable QMD if you want to experiment:

   ```bash
   pip install ghostclaw[qmd]
   ghostclaw . --use-qmd
   ```

---

## Troubleshooting

### "No base report found" warning in delta mode

This means Ghostclaw couldn't find a report matching the exact `--base` commit. It falls back to the latest report.

**Fix:** Ensure you have a baseline report from the commit you're comparing against. Run a full analysis on that commit and keep the report in `.ghostclaw/storage/reports/`.

### Old reports not showing up after upgrade

Check if migration happened:

```bash
ls .ghostclaw/reports/  # should be empty or moved
ls .ghostclaw/storage/reports/  # should contain your JSON reports
```

If migration didn't run automatically, you can trigger it by running any analysis command. Or manually move the files:

```bash
mkdir -p .ghostclaw/storage/reports
mv .ghostclaw/reports/* .ghostclaw/storage/reports/
```

### Config file not parsed (JSON5 errors)

If you added JSON5 features (comments, trailing commas) and get parse errors, you likely have an older version of the `json5` package.

Update:

```bash
pip install --upgrade json5
```

Or remove JSON5 features to revert to plain JSON.

### QMD not working despite `--use-qmd`

Check if `qmd` package is installed:

```bash
pip list | grep qmd
```

If not, install with `pip install ghostclaw[qmd]`.

Ghostclaw will fall back to SQLite if QMD is unavailable. The log will show a warning.

---

## Rollback to v0.1.x

If you encounter issues with v0.2.0, you can:

1. **Restore from backup**: Copy `.ghostclaw.backup/` back to `.ghostclaw/`
2. **Reinstall previous version**:

   ```bash
   git checkout <previous-commit>
   pip install -e .  # or use your package manager
   ```

3. **Disable QMD** by removing `use_qmd` from config or omitting `--use-qmd`

The storage migration is **one-way** (files are moved, not copied). Your backup ensures no data loss.

---

## Need Help?

- **Issues**: <https://github.com/Ev3lynx727/ghostclaw/issues>
- **Docs**: `README.md`, `docs/` folder

---

**v0.2.0** — March 12, 2026
