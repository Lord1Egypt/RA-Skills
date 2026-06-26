---
name: bangumi-tracker
description: Manage Bangumi collections and track watch progress via OAuth. Use when user wants to track anime/book/game/music progress, manage wish/doing/collect lists, or access personal Bangumi data.
compatibility: Requires Python 3.9+, Bangumi account, and browser for OAuth flow.
metadata:
  author: MountLynx
  version: "1.1"
  api_version: v0
---

# Bangumi Tracker

Manage your Bangumi collections and track watch/read progress.

## First Time Setup

### Step 1: Create OAuth App

1. Visit https://bgm.tv/dev/app/create
2. Fill in:
   - App Name: `bangumi-tracker`
   - Homepage URL: `http://localhost:17321`
   - Callback URL: `http://localhost:17321/callback`
3. Get your **Client ID** and **Client Secret**

### Step 2: Configure

```bash
python bangumi_tracker.py config --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
```

### Step 3: Authenticate

```bash
python bangumi_tracker.py auth
```

Opens browser for OAuth authorization.

## Quick Commands

```bash
# Check status
python bangumi_tracker.py status

# List collections
python bangumi_tracker.py collections
python bangumi_tracker.py collections --type anime --status doing

# Add/update
python bangumi_tracker.py collect 428477 doing

# Remove from collection
python bangumi_tracker.py uncollect 428477

# Get progress
python bangumi_tracker.py progress 428477

# User info
python bangumi_tracker.py me

# === Character Collection ===
# Collect/uncollect character
python bangumi_tracker.py collect-character 42084 collect
python bangumi_tracker.py collect-character 42084 uncollect

# List collected characters
python bangumi_tracker.py my-characters

# === Person Collection ===
# Collect/uncollect person
python bangumi_tracker.py collect-person 12345 collect
python bangumi_tracker.py collect-person 12345 uncollect

# List collected persons
python bangumi_tracker.py my-persons

# === Episode Progress ===
# Get episode collection status
python bangumi_tracker.py episodes 428477

# Mark episode as watched/unwatched
python bangumi_tracker.py watch 123456 watched
python bangumi_tracker.py watch 123456 unwatched
```

## Security

- Windows: Credentials stored in Windows Credential Manager
- Other platforms: Credentials stored in `~/.bangumi/`
- Tokens auto-refresh when expired

## More Info

- [Command Reference](references/COMMANDS.md)
- [API Documentation](references/API.md)