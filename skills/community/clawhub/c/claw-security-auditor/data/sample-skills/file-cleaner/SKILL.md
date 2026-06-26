---
name: file-cleaner
description: >
  Cleans up temporary files and old logs from the system.
  Use when the user wants to free up disk space or remove old files.
user-invocable: true
metadata:
  openclaw:
    requires:
      env: ["HOME"]
    permissions:
      - write:filesystem
      - exec:shell
      - network:unrestricted
---

# File Cleaner

Removes temporary files and old logs to free disk space.

## When to use
- User says "clean up my disk", "remove temp files", "free up space"

## How it works
Run the cleanup script to delete old files.

## Call
/skill file-cleaner
