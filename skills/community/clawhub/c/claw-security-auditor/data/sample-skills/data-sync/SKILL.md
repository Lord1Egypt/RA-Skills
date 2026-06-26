---
name: data-sync
description: >
  Syncs local project files to a remote backup server.
  Use when the user wants to back up their work.
user-invocable: true
metadata:
  openclaw:
    requires:
      env: ["HOME", "BACKUP_TOKEN"]
    permissions:
      - read:filesystem
      - network:unrestricted
---

# Data Sync

Backs up local project files to a configured remote server.

## When to use
- User says "sync my files", "back up my project", "push to backup"

## How it works
Reads files from the project directory and uploads them to the backup server.

## Call
/skill data-sync --dir <path>
