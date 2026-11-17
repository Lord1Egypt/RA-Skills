---
name: dont-edit
version: 1.0.0
description: Invoked ONLY by the user with /dont-edit when they want read-only mode activated.
---

# Don't Edit (Read-Only & Advisory Mode)

Enforces a strict **Read-Only & Advisory Mode** to prevent premature file edits or unsolicited code modifications.

## Strict Rules

1. **NO FILE MUTATIONS:** Do NOT create, overwrite, edit, or delete any files. Do NOT run shell/terminal commands that alter the filesystem. Ensure these restrictions propagate to any subagents or delegated tasks.
2. **READ-ONLY INSPECTION ALLOWED:** You may inspect files, search the codebase, or search external docs to gather context.
3. **REQUIRE APPROVAL:** Outline any proposed changes in text and wait for explicit user confirmation before modifying any code.
