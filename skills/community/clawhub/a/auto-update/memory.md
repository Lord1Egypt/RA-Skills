# Global Memory Contract - Auto-Update

This document defines the durable defaults file.

## What Belongs Here

- whether the updater activates on install conversations
- the global new-skill default: all-in or all-out
- OpenClaw default mode: auto, notify, or manual
- summary depth and notification style
- standing approvals that the user has already granted

## What Does Not Belong Here

- full changelog text
- one-off terminal output
- per-skill details that belong in `skills.md`
- migration specifics that belong in `migrations.md`

## Why It Exists

The updater needs one always-loaded file so future sessions know the user's default posture without rereading every ledger.
