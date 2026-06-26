# Effective Git

Intelligent Git workflow assistant that helps you commit, push, and manage code changes following best practices.

## Introduction

Effective Git is an intelligent Git workflow assistant that can:
- Analyze code changes and provide commit suggestions
- Automatically detect project commit conventions
- Provide safe push operations with confirmation mechanisms
- Intelligently resolve merge conflicts
- Quickly execute common Git commands

## Quick Start

### Getting Help

```bash
# Display usage guide
./scripts/show_help.sh

# View best practices
cat ./references/best-practices.md

# View conflict resolution guide
cat ./references/conflict-resolution.md

# View quick commands list
cat ./references/quick-commands.md
```

## Core Features

### 1. Quick Operations Mode

Use the `gq` prefix for quick, read-only Git operations:

```bash
# Branch operations
gq b:l          # List all branches
gq b-> main     # Switch to main branch
gq b:n feature  # Create new branch
gq b:d old      # Delete branch

# Status & info
gq s            # Short status
gq l            # Recent commits
gq d            # Show changes

# Stash operations
gq st:s         # Stash changes
gq st:p         # Pop stash

# Remote operations
gq r:f          # Fetch remote updates

# Quick commit
gq c "message"  # Add all and commit
gq c:a          # Amend last commit
```

See [quick-commands.md](references/quick-commands.md) for the full command list.

**Important**: Quick commands require explicit `gq` prefix to avoid accidental triggering. Use only for read-only or low-risk operations; dangerous operations still require the full workflow.

### 2. Full Workflow Mode

For commits, pushes, merges, and other operations, use natural language:

```bash
# Commit code (automatically analyzes changes and provides suggestions)
"help me commit code"

# Push code (with safety checks)
"push code to remote"

# Resolve conflicts
"resolve merge conflicts"

# Rebase operation
"rebase onto main"
```

#### Full Workflow Steps

1. **Analyze Changes**
   ```bash
   ./scripts/analyze_changes.sh
   ```
   Understand current branch, uncommitted changes, recent commit history, and last commit details.

2. **Determine Commit Strategy**
   
   The system automatically decides whether to use `git commit --amend` or create a new commit:
   
   - **Use amend**: Fixing small issues in last commit, adding forgotten files, last commit not pushed, changes logically belong to last commit
   - **Use new commit**: New logical unit, last commit already pushed, changes unrelated to last commit

3. **Check Project Conventions**
   
   Automatically analyze recent commit history to detect:
   - Commit prefixes (feat:, fix:, chore:, etc.)
   - Ticket references (#123, JIRA-456)
   - Emoji usage (✨, 🐛, 📝)
   - Capitalization style
   
   If unclear, asks user about project conventions.

4. **Write Commit Message**
   
   Follow best practices:
   - Use imperative mood ("Add feature" not "Added feature")
   - Keep subject line under 50 characters
   - Be specific and descriptive
   - Match project conventions

5. **Safe Push**
   
   **Critical constraint**: Only push to current branch.
   
   Before pushing:
   1. Confirm current branch
   2. Show what will be pushed
   3. Ask user for confirmation
   4. Execute push

## Best Practices

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type definitions:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test related
- `chore`: Maintenance tasks

**Rules:**
1. **Subject line**: Under 50 characters, imperative mood
2. **Body**: Wrap at 72 characters, explain what and why (not how)
3. **Atomic commits**: One logical change per commit
4. **Present tense**: "Fix bug" not "Fixed bug"

**Example:**
```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow with Google and GitHub providers.
Users can now sign in using their existing accounts.

Closes #123
```

### Dangerous Operations

The following operations require user confirmation and risk explanation:
- `git push --force` / `git push -f`
- `git reset --hard`
- `git clean -fd`
- `git rebase` on shared branches
- `git branch -D` (force delete)
- Any history rewriting operations

## Conflict Resolution

### Core Principle: Never Lose Code

**Critical principle**: The absolute priority when resolving conflicts is preserving all code. If unable to resolve confidently, you must:
1. Clearly summarize the conflict
2. Show both versions to the user
3. Request guidance
4. **Never** automatically choose one side

### Conflict Resolution Workflow

1. **Save Pre-merge State**
   ```bash
   ./scripts/save_diff.sh
   # Also create backup branch
   git branch <current-branch>-backup
   ```

2. **Detect and Analyze Conflicts**
   ```bash
   ./scripts/analyze_conflicts.sh
   ./scripts/visualize_conflicts.sh
   ```

3. **Deep Conflict Analysis**
   
   For complex conflicts, analyze:
   - **Intent**: What problem does each version solve? What functionality is added/removed/modified? Is it a bug fix, feature, refactor, or optimization?
   - **Approach comparison**: Different algorithms? Different API or interface changes? Different dependencies added/removed? Different side effects?
   - **Trade-offs**: Performance vs readability? Simple vs robust?

4. **Determine Resolution Strategy**
   - **Keep Both (Merge)**: Both changes are valuable and compatible
   - **Keep Ours (HEAD)**: Our changes are newer/more complete
   - **Keep Theirs (Incoming)**: Their changes are more correct/complete
   - **Rewrite**: Both have issues, create a better solution
   - **Ask User**: Cannot decide confidently

5. **Post-Resolution Verification**
   ```bash
   # Generate resolution diff
   git diff --cached > .git/merge-diffs/resolution_$(date +%Y%m%d_%H%M%S).diff
   
   # Compare with backup branch
   git diff <branch>-backup <branch>
   ```

### Special Cases

- **Detached HEAD**: Scripts detect and warn; recommend creating a branch before operations
- **Submodules**: Detected and flagged; require special handling
- **Large files**: Output automatically limited to prevent overwhelming context
- **Rebase to less code**: Default to preserving current branch's work

See [conflict-resolution.md](references/conflict-resolution.md) for detailed guide.

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

## Script Tools

| Script | Function | Purpose |
|--------|----------|---------|
| `analyze_changes.sh` | Analyze current Git state | Understand branch, uncommitted changes, recent commits |
| `analyze_conflicts.sh` | Analyze merge conflicts | Provide three-way diff view, show only conflict sections |
| `git_quick.sh` | Execute quick Git commands | Backend implementation for gq commands |
| `save_diff.sh` | Save change snapshot | Backup before conflict resolution |
| `show_help.sh` | Display usage help | Quick guide and examples |
| `visualize_conflicts.sh` | Visualize conflicts | Show conflict files and markers |

## Common Workflows

### Feature Branch Workflow

```bash
# 1. Create feature branch from main
gq b:n feature/new-feature

# 2. Develop and commit
# ... write code ...
./scripts/analyze_changes.sh
# Commit based on suggestions

# 3. Stay in sync with main
git fetch origin
git rebase origin/main

# 4. Push and create PR
git push origin HEAD
```

### Hotfix Workflow

```bash
# 1. Switch to main and create fix branch
gq b-> main
gq b:n fix/critical-bug

# 2. Fix and commit
# ... fix code ...
gq c "fix: resolve critical bug in auth"

# 3. Push
git push origin HEAD
```

### Clean Up History

```bash
# Interactive rebase to clean up last 3 commits
git rebase -i HEAD~3

# Or use amend to fix last commit
git commit --amend
```

## Notes

1. **Never** use `git push --force` on shared branches
2. **Always** create backup branches before dangerous operations
3. **Carefully review** `git diff` output before committing
4. **Keep commits atomic**: One logical change = One commit
5. **Delete merged branches** promptly

## Resources

- **Help script**: `scripts/show_help.sh` - Usage guide and examples
- **Best practices reference**: `references/best-practices.md` - Commit conventions and workflows
- **Conflict resolution guide**: `references/conflict-resolution.md` - Detailed analysis framework and templates
- **Quick commands reference**: `references/quick-commands.md` - Shorthand for common operations

## License

MIT License
