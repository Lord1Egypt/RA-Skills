---
name: effective-git
description: Intelligent Git workflow assistant following best practices. Use when user needs help with git commits, analyzing changes, writing commit messages, pushing code, rebasing, merging, or any git operations. Also triggers on quick command prefix 'gq' or 'gq:' for rapid operations like 'gq b:l' (list branches), 'gq b:n name' (create branch), 'gq:s' (status). Automatically analyzes changes, suggests appropriate commit strategies (amend vs new commit), follows project conventions, and ensures safe operations with confirmation for dangerous commands.
---

# Effective Git

Smart Git workflow assistant that helps you commit, push, and manage code changes following best practices.

## Getting Help

**Quick help**: When user asks "gq help", "gq:h", or "git help", run `scripts/show_help.sh` to display usage guide

**Detailed help**: When user asks about specific topics:
- "show me git best practices" → Read `references/best-practices.md`
- "how to resolve conflicts" → Read `references/conflict-resolution.md`
- "quick commands list" → Read `references/quick-commands.md`

**Usage examples**:
- Use `gq <command>` for quick operations (status, branch switching, etc.)
- Use natural language for commits, pushes, merges (full workflow with analysis and safety checks)
- Examples:
  - "gq b:l" → Quick branch list
  - "help me commit code" → Full commit workflow with analysis
  - "gq:s" → Quick status
  - "resolve conflicts" → Full conflict resolution with guidance

## Core Workflow

When helping with git operations, follow this sequence:

### Quick Operations Mode

For simple, read-only operations or quick checks, use `scripts/git_quick.sh`:

**When user asks for:**
- "list branches" → `git_quick.sh b:l`
- "switch to xxx" → `git_quick.sh "b->" xxx`
- "create branch xxx" → `git_quick.sh b:n xxx`
- "check status" → `git_quick.sh s`
- "recent commits" → `git_quick.sh l`
- "show changes" → `git_quick.sh "d"`
  - If `GIT_QUICK_DIFF_TERMINAL` is set, opens in new terminal window
  - Otherwise uses `$PAGER` (default: less)
  - Staged changes: `git_quick.sh "d:s"`

See `references/quick-commands.md` for full command list.

### Full Workflow Mode

For commits, pushes, merges, and conflict resolution, follow the detailed workflow below:

### 1. Analyze Recent Changes

Run `scripts/analyze_changes.sh` to understand:
- Current branch
- Uncommitted changes
- Recent commit history
- Last commit details

### 2. Determine Commit Strategy

Check if changes should amend the last commit or create a new one:

**Use `git commit --amend` when:**
- Fixing typos or small issues in the last commit
- Adding forgotten files to the last commit
- Last commit hasn't been pushed yet
- Changes are logically part of the last commit

**Use `git commit -m "message"` when:**
- Changes represent a new logical unit of work
- Last commit has been pushed
- Changes are unrelated to the last commit

### 3. Check Project Conventions

Before writing commit message:
1. Review recent commit messages: `git log --oneline -10`
2. Look for patterns:
   - Prefixes (feat:, fix:, chore:, etc.)
   - Ticket references (#123, JIRA-456)
   - Emoji usage (✨, 🐛, 📝)
   - Capitalization style
3. If unclear, ask user about project conventions

### 4. Write Commit Message

Follow conventions from references/best-practices.md:
- Use imperative mood ("Add feature" not "Added feature")
- Keep subject line under 50 chars
- Be specific and descriptive
- Match project conventions discovered above

### 5. Safe Push Operations

**Critical constraint**: Only push to current branch.

Before pushing:
1. Confirm current branch: `git branch --show-current`
2. Show what will be pushed: `git log origin/$(git branch --show-current)..HEAD --oneline`
3. Ask user to confirm
4. Push: `git push origin HEAD`

Never use `git push --force` without explicit user confirmation.

## Dangerous Operations

These require user confirmation before execution:
- `git push --force` or `git push -f`
- `git reset --hard`
- `git clean -fd`
- `git rebase` on shared/public branches
- `git branch -D` (force delete)
- Any history rewriting on pushed commits

Always explain the risk before asking for confirmation.

## Conflict Resolution

**Critical Principle:** When resolving conflicts, the absolute priority is preserving all code. If unable to confidently resolve, you must summarize the issue and feedback to the user. **DO NOT perform automatic merges.**

### Conflict Handling Workflow:

1.  **Pre-merge/Rebase Snapshot:** Before attempting a merge or rebase, save a snapshot of the current state for documentation and safety.
    ```bash
    scripts/save_diff.sh
    # Also create backup branch
    git branch <current-branch>-backup
    ```
    This creates a `git diff` document before the merge.

2.  **Detect and Analyze Conflicts:** If conflicts arise during a merge or rebase:
    ```bash
    scripts/analyze_conflicts.sh
    ```
    This provides detailed three-way diff analysis for each conflicted file.

3.  **Deep Conflict Analysis:** For complex conflicts where both sides modified the same code:
    
    **Analyze the intent:**
    - What problem does each version solve?
    - What functionality does each add/remove/modify?
    - Is it a bug fix, feature, refactor, or optimization?
    
    **Compare approaches:**
    - Do they implement different algorithms?
    - Do they change APIs or interfaces differently?
    - What are the trade-offs (performance vs readability, simplicity vs robustness)?
    
    **Determine resolution strategy:**
    - **Keep Both (Merge)**: Both changes are valuable and can be combined
    - **Keep Ours**: Our change is more complete/correct
    - **Keep Theirs**: Their change is more complete/correct
    - **Rewrite**: Neither is ideal, create better solution combining insights
    - **Ask User**: Cannot decide confidently, need user guidance

4.  **Present Analysis to User:** When conflicts cannot be resolved automatically, create a structured summary:
    - Show both versions of conflicting code
    - Explain the intent and trade-offs of each
    - Provide your recommendation with reasoning
    - Ask for user's decision
    - See `references/conflict-resolution.md` for detailed template

5.  **Post-Resolution Documentation:** After conflicts are resolved:
    ```bash
    # Generate diff of resolution
    git diff --cached > .git/merge-diffs/resolution_$(date +%Y%m%d_%H%M%S).diff
    
    # Show summary
    git diff --cached --stat
    ```

6.  **Verify No Code Loss:** After completing merge/rebase:
    ```bash
    # Compare with backup branch
    git diff <branch>-backup <branch>
    
    # Review carefully for unexpected deletions
    ```

**Special attention for edge cases:**
- **Detached HEAD**: Scripts will detect and warn; recommend creating a branch before operations
- **Submodules**: Detected and flagged; require special handling (see `references/conflict-resolution.md`)
- **Large files**: Output automatically limited to prevent overwhelming context
- **Rebase to less code**: Default to preserving current branch's work (see `references/conflict-resolution.md`)

## Rebase & Merge

### Interactive Rebase
```bash
# Clean up last N commits
git rebase -i HEAD~N

# Rebase feature branch onto main
git checkout feature-branch
git fetch origin
git rebase origin/main
```

### Merge Strategies
```bash
# Standard merge (preserves history)
git merge feature-branch

# Squash merge (single commit)
git merge --squash feature-branch
```

## Common Tasks

### Stash Changes
```bash
git stash                    # Stash current changes
git stash list              # List stashes
git stash pop               # Apply and remove last stash
git stash apply stash@{0}   # Apply specific stash
```

### Cherry-pick
```bash
git cherry-pick <commit-hash>
```

### Undo Changes
```bash
git restore <file>          # Discard working changes
git restore --staged <file> # Unstage file
git reset HEAD~1            # Undo last commit (keep changes)
```

## Resources

- **Help script**: scripts/show_help.sh (usage guide and examples)
- **Best practices reference**: references/best-practices.md
- **Conflict resolution guide**: references/conflict-resolution.md (includes detailed analysis framework and templates)
- **Quick commands reference**: references/quick-commands.md (shorthand for common operations)
- **Change analysis script**: scripts/analyze_changes.sh
- **Conflict analysis script**: scripts/analyze_conflicts.sh (deep three-way diff analysis)
- **Save diff script**: scripts/save_diff.sh
- **Visualize conflicts script**: scripts/visualize_conflicts.sh
- **Quick operations script**: scripts/git_quick.sh (fast branch switching, status checks, etc.)

## Quick Commands

For rapid git operations, use `scripts/git_quick.sh` with the `gq` prefix pattern:

**Trigger pattern**: When user message starts with `gq:` or uses git quick command syntax

**Common commands:**
- `gq b:l` or `gq:b:l` - List branches
- `gq b-> <name>` - Switch to branch
- `gq b:n <name>` - Create new branch from current
- `gq s` - Quick status
- `gq l` - Recent commits
- `gq d` - Show diff

**Usage in conversation:**
- User: "gq b:l" → Run `scripts/git_quick.sh b:l`
- User: "gq b-> feature" → Run `scripts/git_quick.sh "b->" feature`
- User: "gq:s" → Run `scripts/git_quick.sh s`

**⚠️ Shell quoting rule**: Always quote the command argument when calling `git_quick.sh` to prevent shell misinterpreting special characters. Use `git_quick.sh "b->" <branch>`, never `git_quick.sh b-> <branch>` (shell will treat `>` as redirection).

See `references/quick-commands.md` for full command list and usage patterns.

**Important**: Only trigger quick commands when user explicitly uses `gq` prefix or quick command syntax. Do not auto-trigger for general git questions.
