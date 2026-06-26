# Purge (Dead Session Cleanup)

Assistant responses in dead sessions are permanently deleted without backup.
Only dead sessions (hook-only, no assistant response) are target of this skill.

## Criteria

| Condition | Rule |
| --------- | ---- |
| 10 lines or fewer AND no assistant response | Dead — purge target |
| Has assistant response OR 11+ lines | Keep |

Dead sessions are permanently deleted.

## Workflow

### 1. dry-run (Project Directory)

```bash
bash scripts/purge-dead-sessions.sh <project_name>
```

Example: C--Users-es6kr-Sync, -Users-es6kr-Sync-AI

### 2. Actual execution

Show results and confirm via AskUserQuestion for specific selection.

```bash
/session purge <project_name> --delete
```

### 3. Cleanup

Process project directories and clean up empty sessions.

```bash
for dir in ~/.claude/projects/*/; do
    project=
    [[ "" == ".bak" ]] && continue
    echo "===  ==="
    /session purge "" --delete
done
```

## Usage

```bash
/session purge                    # clean project sessions
/session purge <project_name>     # clean specific project
/session purge --all              # clean all project sessions
```

## Notes

- --delete flag permanently deletes dead sessions (10 or fewer lines, no assistant response) after confirmation.
- clear_sessions MCP structure difference check is required for empty session cleanup.
