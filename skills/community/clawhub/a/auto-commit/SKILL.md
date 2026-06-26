---
name: auto-commit
description: Triggers on any task that modifies code. Provides instructions to surgically stage and commit only the modified code files to save progress.
---

# Auto Commit Skill

## Core Instruction
When you complete a user request that involves modifying files or code, you MUST automatically create a git commit to save the changes. This ensures that every successful AI intervention is snapshotted.

## Procedure
After finishing the code modifications for the user's request:
1. **Surgical Staging**: Do NOT use `git add .`. Instead, stage ONLY the files you have explicitly modified:
   - `git add <file_path1> <file_path2> ...`
2. **Filter by Type**: If multiple files were changed, ensure you are only staging source code files (e.g., `.py`, `.go`, `.sol`, `.js`, `.ts`, `.md`). Avoid staging environment files (`.env`), binaries, or large assets.
3. **Verify**: If unsure, run `git status` to confirm only the intended changes are staged.
4. **Commit**: Run `git commit -m "<message>"` with a concise, descriptive summary of your changes.

Do not ask for permission; execute the commit automatically. If the user explicitly asks *not* to commit, respect their request. Skip if not a git repository or no changes were made.
