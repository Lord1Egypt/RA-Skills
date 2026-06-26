---
name: any_sync_start
description: Initialize Any Sync config for OpenClaw workspace and run first pull — guided setup wizard
metadata:
  openclaw:
    requires:
      bins: [gh]
---

# Any Sync Setup Wizard

Guide the user through setting up Any Sync for cross-device workspace sync.

## Steps

### 1. Check Authentication

Run the auth check:
```bash
npx any-sync auth
```

If it fails (exit code 1), help the user set up authentication:
- Option A: Set `GITHUB_TOKEN` environment variable
- Option B: Run `gh auth login` to authenticate with GitHub CLI

Do not proceed until auth succeeds.

### 2. Get Sync Repo

Ask the user for their sync repo in `owner/repo` format. This is the GitHub repository where their OpenClaw workspace files will be stored.

If they don't have one yet, suggest they create a new private repo on GitHub first.

### 3. Create Config

Ask the user which items to sync (default: all three):
- Skills (`~/.openclaw/workspace/skills`)
- Memory (`~/.openclaw/workspace/memory`)
- Config files (`AGENTS.md`, `SOUL.md`, `USER.md`, `TOOLS.md`, `IDENTITY.md`)

Then run the init command with the OpenClaw preset:
```bash
npx any-sync init "$HOME/.any-sync.json" "<owner/repo>" "<branch>" --preset openclaw
```

Use `main` as the default branch unless the user specifies otherwise.

The init command respects `OPENCLAW_WORKSPACE` and `OPENCLAW_PROFILE` environment variables for custom workspace paths.

### 4. First Pull

Run the first pull to download existing files:
```bash
npx any-sync pull "$HOME/.any-sync.json" ".any-sync.lock"
```

### 5. Show Summary

Parse the JSON output and display what was synced in a readable format:
- Number of files pulled per mapping
- Any conflicts found
- Config file location
