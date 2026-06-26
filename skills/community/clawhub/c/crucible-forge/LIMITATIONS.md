# Forge — Limitations

## What Forge Does NOT Do

### No Auto-Execution
Forge generates plans. It does not execute them. You read the plan, you move the files. This is a deliberate safety choice, not a missing feature.

### No Platform-Specific Integration
Forge works with files and directories. It does not integrate with:
- Cron job management (you update cron jobs manually based on the plan)
- Git operations (commit/push after reorg is your responsibility)
- Cloud storage sync
- Database state files
- Container or VM management

### No Content Understanding
Forge classifies files by name, extension, and location — not by reading and understanding their contents. It won't know that a file named `notes.md` contains trading strategies that belong in a `trading/` directory unless you configure a classification rule for it.

### No Conflict Resolution
If two files have the same name and both need to move to the same directory, Forge flags the conflict. It does not resolve it. You decide which file wins.

### No Incremental Mode
Each scan is a full workspace scan. There is no "only scan files changed since last run." For large workspaces (10,000+ files), scans may take several minutes.

### No Undo Button
Forge creates manifests and rollback commands, but there is no single "undo" command. Rolling back requires restoring from the pre-move backup. Always verify your backup before executing a plan.

## When NOT to Use Forge

- **During active incidents.** If your agent is mid-task or a live system is unstable, don't reorganize.
- **Without a backup.** Forge enforces this, but if you override it, you're on your own.
- **On workspaces you don't own.** Forge moves files. Make sure you have permission.
- **As a substitute for understanding your workspace.** Forge is a tool, not a consultant. If you don't know what your files do, scanning them won't tell you. Read them first.

## Known Edge Cases

1. **Symlinks:** Forge follows symlinks during scanning but does not create or preserve them during moves. If your workspace relies on symlinks, verify them manually after reorganization.

2. **Binary files:** Reference scanning only works on text files. Binary files are inventoried but not scanned for cross-references.

3. **Very long paths:** Some operating systems have path length limits. Forge does not check for this. Deep directory nesting may cause issues on Windows.

4. **Concurrent access:** If another process modifies files during a scan, the scan results may be inconsistent. Run scans during quiet periods.

5. **Unicode filenames:** Forge handles UTF-8 filenames. Other encodings may cause issues on some platforms.

## Assumptions

- Python 3.8+ is available
- The workspace is on a local filesystem (not a network mount with high latency)
- You have read/write permissions to the workspace
- Files are small enough to read into memory for reference scanning (configurable limit, default 10MB)
