---
name: any_sync_push
description: Push local workspace changes directly to configured branch on GitHub
metadata:
  openclaw:
    requires:
      bins: [gh]
---

# Push to GitHub

Push local workspace changes directly to the configured branch on GitHub.

## Steps

### 1. Find Config

Look for config at `$HOME/.any-sync.json` first, then `.any-sync.json` in the current directory. If neither exists, tell the user to run the start skill first.

### 2. Check for Changes

Run the status command to see what has changed:
```bash
npx any-sync status "<config-path>" ".any-sync.lock"
```

Show the user which files have changed (modified or new) across all mappings.

### 3. Confirm Push

Ask the user to confirm before pushing. Show:
- Which files will be pushed
- Which branch they will be pushed to
- Which repo they will be pushed to

### 4. Run Push

If confirmed:
```bash
npx any-sync push "<config-path>" ".any-sync.lock"
```

### 5. Report Results

Parse the JSON output and report:
- Files pushed
- Branch updated
- Any errors encountered
