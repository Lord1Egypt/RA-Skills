---
name: any_sync_pull
description: Pull latest workspace files from GitHub sync repo
metadata:
  openclaw:
    requires:
      bins: [gh]
---

# Pull from GitHub

Pull the latest files from the configured GitHub sync repo into the OpenClaw workspace.

## Steps

### 1. Find Config

Look for config at `$HOME/.any-sync.json` first, then `.any-sync.json` in the current directory. If neither exists, tell the user to run the start skill first.

### 2. Run Pull

```bash
npx any-sync pull "<config-path>" ".any-sync.lock"
```

### 3. Report Results

Parse the JSON output and report:
- **Pulled:** List each file that was downloaded
- **Conflicts:** List each file where both local and remote changed
- **Skipped:** Count of unchanged files

### 4. Resolve Conflicts

If there are conflicts, for each conflicted file ask the user:
- **Keep local** — skip this file (local changes preserved)
- **Take remote** — download the remote version (local changes overwritten)
- **Skip** — do nothing for now

If the user chooses "Take remote" for a conflict, download that specific file by running pull again after clearing the lockfile entry for that file.
