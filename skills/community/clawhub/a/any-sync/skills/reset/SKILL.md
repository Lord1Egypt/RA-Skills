---
name: any_sync_reset
description: Clear Any Sync config and delete lockfile
metadata:
  openclaw:
    requires: {}
---

# Reset Any Sync

Clear the Any Sync config and lockfile.

## Steps

### 1. Confirm Reset

Ask the user to confirm they want to reset. Explain that this will:
- Delete the config file (`.any-sync.json`)
- Delete the lockfile (`.any-sync.lock`)
- NOT delete any synced files (skills, memory, workspace config remain on disk)

### 2. Find Config

Look for config at `$HOME/.any-sync.json` first, then `.any-sync.json` in the current directory.

### 3. Run Reset

```bash
npx any-sync reset "<config-path>" ".any-sync.lock"
```

### 4. Report Results

Parse the JSON output and report what was cleared.
