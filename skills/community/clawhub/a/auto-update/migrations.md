# Migration Queue Contract - Auto-Update

This document defines how migration review is tracked for skills.

## What Counts as Migration Risk

- folder or file structure changes
- setup or state-storage path changes
- AGENTS, TOOLS, SOUL, or workspace-hook changes
- renamed ledgers, templates, or memory folders
- instructions that assume new state without migrating old state

## Pending Entry Must Include

- skill slug
- from version
- to version
- what might break or move
- whether the user already approved the migration

## Behavior

If migration risk exists:
- pause auto-apply or pause first use of the new version
- show the user what changed
- ask before moving or deleting anything
