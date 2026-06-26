# Session Destroy

Safely deletes the currently active Claude Code session and restarts the IDE Extension Host.

## Quick Start

```bash
scripts/destroy-session.sh
```

## How It Works

1. Moves the current session file to `~/.claude/projects/.bak/` as a backup
2. Backup filename: `{project-folder-name}_{session-id}.jsonl`
3. Restarts the Extension Host if in a VSCode/Cursor environment

## Scripts

### destroy-session.sh

Extracts the project folder name from the current working directory and moves the most recently modified session file to the backup folder.

### restart-extension-host.sh

Restarts the Extension Host:
1. VSCode CLI: `code --command "workbench.action.restartExtensionHost"`
2. Cursor CLI: `cursor --command "workbench.action.restartExtensionHost"`
3. macOS AppleScript fallback
4. Manual guidance: `Cmd+Shift+P > 'Developer: Restart Extension Host'`

## Notes

- The current conversation will end after this skill runs
- Backup files are kept in `~/.claude/projects/.bak/`
- All extensions will be reloaded when the Extension Host restarts

## Recovery

To restore a deleted session:

```bash
# Check backup folder
ls ~/.claude/projects/.bak/

# Restore (move back to original location)
mv ~/.claude/projects/.bak/{backup_file}.jsonl ~/.claude/projects/{project_name}/{session_id}.jsonl
```

## Check Current Session ID

To check the current session ID before running the script:

```bash
# Search by unique text from the current conversation (first message recommended)
grep -l "{unique text from current conversation}" ~/.claude/projects/{project_name}/*.jsonl
```
