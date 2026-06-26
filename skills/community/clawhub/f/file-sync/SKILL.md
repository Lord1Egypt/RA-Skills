---
name: file-sync
description: Bidirectional file synchronization tool using MD5 hash + version history for conflict detection. Use when the user needs to sync files between two directories (e.g., PC ↔ USB), wants to set up a file sync workflow, or asks to sync/merge two folders with conflict detection. Triggers on keywords: sync files, file sync, bidirectional sync, two-way sync, sync.py, merge folders, sync PC and USB.
version: 1.0.1
changelog:
  "1.0.1": "Fixed bug where shutil.copy2 was called without first creating parent directories, causing failures when syncing into nested subdirectories."
---

# file-sync

`sync.py` is a bidirectional file synchronization tool. It keeps two directories in sync (e.g. PC ↔ USB), detects conflicts using version history, and handles deletions safely via `.trash/`.

## Usage

```bash
python sync.py <local_folder> <remote_folder> <device_name>
```

**Arguments:**
- `local_folder` — First directory to sync
- `remote_folder` — Second directory to sync
- `device_name` — Label for this device (used in conflict file names, e.g. "PC1", "USB")

**Sync direction:** The tool is symmetric — either folder can be local or remote.

## Sync Rules

| Situation | Behavior |
|-----------|----------|
| New file on one side | Copy to the other side |
| Single-side modification | Copy updated file to the other side |
| Concurrent modification (conflict) | Both copies → `.conflict/`, no overwrite |
| File deleted on one side, kept on other | **Conflict** (both kept in `.conflict/`) |
| File deleted on both sides | Remove from both, nothing to trash |
| One side deletes, other side unchanged | Delete propagates to the other side via `.trash/` |

## Special Directories (auto-ignored)

Files and folders matching these names are excluded from sync: `.conflict`, `.trash`, `.sync_logs`

## State & History

State is stored in `.sync_state.json` in each folder. Each file maintains a `history` list of MD5 hashes (up to 10 entries). Conflict detection uses history to find a common ancestor:
- **No common ancestor** → conflict
- **One side unchanged** (matches ancestor) → auto-merge
- **Both sides changed from ancestor** → conflict

## Conflict Resolution

When a conflict is detected, **both versions** are copied into `local_folder/.conflict/` with names like:
```
filename_LOCAL_<device>_<timestamp>
filename_REMOTE_<device>_<timestamp>
```
The original files are left untouched. Manually review and merge, then delete from `.conflict/`.

## Deletion Safety

Deleted files go to `.trash/<relpath>.<timestamp>` rather than being permanently removed.

## Logging

Logs are written to `local_folder/.sync_logs/sync_<timestamp>.log`, including timestamps, action types (INFO/CONFLICT/TRASH/ERROR), and a summary count.

## Workflow Example

```bash
# Sync PC1 with USB drive (USB mounted as E:)
python sync.py C:\Users\PC1 E:\ PC1

# Sync back after working on USB
python sync.py E:\ C:\Users\PC1 USB
```

## Bundled Resources

- `scripts/sync.py` — The sync script (copy to your project or call directly)
- `references/behaviors.md` — Detailed behavior notes, edge cases, and design rationale