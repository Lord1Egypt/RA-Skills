# Quick Git Commands Reference

This reference provides a shorthand command system for common git operations.

## Trigger Pattern

**Important**: Quick commands require explicit `gq` prefix to avoid accidental triggering.

**Valid triggers:**
- `gq <command>` - Standard format
- `gq:<command>` - Alternative format
- `gq <command> <arg>` - With arguments

**Examples:**
- ✅ "gq b:l" → Triggers quick command
- ✅ "gq:s" → Triggers quick command
- ✅ "gq b-> feature" → Triggers quick command (runs as `git_quick.sh "b->" feature`)
- ❌ "list branches" → Does NOT trigger (use full workflow)
- ❌ "b:l" → Does NOT trigger (missing gq prefix)

## Usage

```bash
scripts/git_quick.sh "<command>" [argument]
```

When user says "gq <command>", run:
```bash
scripts/git_quick.sh "<command>"
```

## Command Categories

### 🌿 Branch Operations

| Command | Alias | Description | Example |
|---------|-------|-------------|---------|
| `b:l` | `bl` | List all branches (local + remote) | `gq b:l` |
| `b:c` | `bc` | Show current branch | `gq b:c` |
| `b->` | - | Switch to branch | `gq "b->" feature` |
| `b:n` | - | Create new branch from current | `gq b:n fix-bug` |
| `b:d` | - | Delete branch (safe) | `gq b:d old-feature` |

### 📊 Status & Info

| Command | Alias | Description | Example |
|---------|-------|-------------|---------|
| `s` | `st` | Short status | `gq s` |
| `s:f` | `sf` | Full status | `gq s:f` |
| `l` | `log` | Recent commits (10, with graph) | `gq l` |
| `l:a` | `la` | All branches commits (20, graph) | `gq l:a` |
| `l:f` | `lf` | Last commit full details | `gq l:f` |

### 📝 Diff Operations

| Command | Alias | Description | Example |
|---------|-------|-------------|---------|
| `d` | `diff` | Show unstaged changes (terminal/pager) | `gq d` |
| `d:s` | `ds` | Show staged changes (terminal/pager) | `gq d:s` |
| `d:st` | `dst` | Diff summary (stat) | `gq d:st` |

### 💾 Stash Operations

| Command | Alias | Description | Example |
|---------|-------|-------------|---------|
| `st:s` | `sts` | Stash changes | `gq st:s` |
| `st:l` | `stl` | List stashes | `gq st:l` |
| `st:p` | `stp` | Pop stash (apply + remove) | `gq st:p` |
| `st:a` | `sta` | Apply stash (keep in list) | `gq st:a` |

### 🌐 Remote Operations

| Command | Alias | Description | Example |
|---------|-------|-------------|---------|
| `r:l` | `rl` | List remotes | `gq r:l` |
| `r:f` | `rf` | Fetch all remotes | `gq r:f` |

### ⚡ Quick Commit

| Command | Alias | Description | Example |
|---------|-------|-------------|---------|
| `c` | `commit` | Add all & commit | `gq c "fix: bug"` |
| `c:a` | `ca` | Amend last commit | `gq c:a` |

## Common Workflows

### Quick Status Check
```bash
gq s          # What's changed?
gq l          # Recent commits
```

### Branch Switching
```bash
gq b:l        # See all branches
gq "b->" main   # Switch to main
```

### Create Feature Branch
```bash
gq b:c        # Confirm current branch
gq b:n feature-x  # Create new branch
```

### Quick Save Work
```bash
gq st:s       # Stash current work
gq "b->" main   # Switch branch
# ... do something ...
gq "b->" feature-x  # Back to feature
gq st:p       # Restore work
```

### Review Changes
```bash
gq d:st       # Summary of changes
gq d          # Full diff
gq d:s        # What's staged?
```

## Design Philosophy

Commands follow patterns:
- **Category prefix**: `b:` (branch), `s:` (status), `l:` (log), `d:` (diff), `st:` (stash), `r:` (remote), `c:` (commit)
- **Action suffix**: `l` (list), `c` (current), `f` (full/fetch), `s` (save/staged), `a` (apply/all), `n` (new)
- **Navigation**: `->` for switching/moving

Single letter commands for most common operations: `s`, `l`, `d`, `c`

## Integration with Main Workflow

These quick commands complement the main effective-git workflow:
- Use quick commands for exploration and status checks
- Use main workflow (SKILL.md) for commits, pushes, and conflict resolution
- Quick commands are read-only or low-risk operations
- Dangerous operations still go through main workflow with confirmations

## Configuration

### Diff Display (d, d:s commands)

Set `GIT_QUICK_DIFF_TERMINAL` to open diff in a new terminal window:

```bash
# ~/.bashrc or ~/.zshrc
export GIT_QUICK_DIFF_TERMINAL="konsole"           # KDE
export GIT_QUICK_DIFF_TERMINAL="gnome-terminal --" # GNOME
export GIT_QUICK_DIFF_TERMINAL="alacritty -e"      # Alacritty
export GIT_QUICK_DIFF_TERMINAL="kitty"             # Kitty
```

Without this variable, diff uses `$PAGER` (default: `less`).
