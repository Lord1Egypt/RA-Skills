#!/bin/bash
# Quick git operations with short commands
# Usage: git_quick.sh <command>

set -e

# Configuration: terminal for diff display
# Set GIT_QUICK_DIFF_TERMINAL to open diff in new terminal window
# Examples: export GIT_QUICK_DIFF_TERMINAL="konsole"
#           export GIT_QUICK_DIFF_TERMINAL="gnome-terminal --"
#           export GIT_QUICK_DIFF_TERMINAL="alacritty -e"
: "${GIT_QUICK_DIFF_PAGER:=${PAGER:-less}}"

# Helper function to show diff including untracked files
show_diff_with_untracked() {
    # Show modified tracked files
    git diff
    # Show untracked new files
    local untracked_files
    untracked_files=$(git ls-files --others --exclude-standard)
    if [ -n "$untracked_files" ]; then
        echo ""
        echo "=== Untracked New Files ==="
        echo "$untracked_files" | while read -r file; do
            echo ""
            echo "+++ New file: $file +++"
            cat "$file" 2>/dev/null || echo "(binary or empty file)"
        done
    fi
}

if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not a git repository"
    exit 1
fi

CMD="$1"
ARG="$2"

case "$CMD" in
    # Branch operations
    "b:l"|"bl")
        # List branches
        echo "=== Local Branches ==="
        git branch -vv
        echo ""
        echo "=== Remote Branches ==="
        git branch -r
        ;;
    
    "b:c"|"bc")
        # Current branch
        BRANCH=$(git branch --show-current)
        if [ -z "$BRANCH" ]; then
            echo "Detached HEAD at $(git rev-parse --short HEAD)"
        else
            echo "Current branch: $BRANCH"
        fi
        ;;
    
    "b->")
        # Switch to branch
        if [ -z "$ARG" ]; then
            echo "Error: Branch name required"
            echo "Usage: git_quick.sh b-> <branch-name>"
            exit 1
        fi
        git checkout "$ARG"
        ;;
    
    "b:n")
        # Create new branch from current
        if [ -z "$ARG" ]; then
            echo "Error: Branch name required"
            echo "Usage: git_quick.sh b:n <new-branch-name>"
            exit 1
        fi
        git checkout -b "$ARG"
        echo "Created and switched to new branch: $ARG"
        ;;
    
    "b:d")
        # Delete branch (safe)
        if [ -z "$ARG" ]; then
            echo "Error: Branch name required"
            echo "Usage: git_quick.sh b:d <branch-name>"
            exit 1
        fi
        git branch -d "$ARG"
        ;;
    
    # Status operations
    "s"|"st")
        # Short status
        git status --short --branch
        ;;
    
    "s:f"|"sf")
        # Full status
        git status
        ;;
    
    # Log operations
    "l"|"log")
        # Recent commits (10)
        git log --oneline --graph --decorate -10
        ;;
    
    "l:a"|"la")
        # All commits with graph
        git log --oneline --graph --decorate --all -20
        ;;
    
    "l:f"|"lf")
        # Last commit full details
        git log -1 --stat
        ;;
    
    # Diff operations
    "d"|"diff")
        # Unstaged changes + untracked new files
        if [ -n "$DISPLAY" ] && [ -n "$GIT_QUICK_DIFF_TERMINAL" ]; then
            $GIT_QUICK_DIFF_TERMINAL bash -c "$(declare -f show_diff_with_untracked); show_diff_with_untracked; echo ''; echo 'Press Enter to close...'; read"
        else
            show_diff_with_untracked | $GIT_QUICK_DIFF_PAGER
        fi
        ;;
    
    "d:s"|"ds")
        # Staged changes - open in terminal if configured, else use pager
        if [ -n "$DISPLAY" ] && [ -n "$GIT_QUICK_DIFF_TERMINAL" ]; then
            $GIT_QUICK_DIFF_TERMINAL bash -c 'git diff --cached; echo ""; echo "Press Enter to close..."; read'
        else
            git diff --cached | $GIT_QUICK_DIFF_PAGER
        fi
        ;;
    
    "d:st"|"dst")
        # Diff stat (summary)
        git diff --stat
        ;;
    
    # Stash operations
    "st:s"|"sts")
        # Stash save
        git stash push -m "${ARG:-Quick stash}"
        ;;
    
    "st:l"|"stl")
        # Stash list
        git stash list
        ;;
    
    "st:p"|"stp")
        # Stash pop
        git stash pop
        ;;
    
    "st:a"|"sta")
        # Stash apply (keep in stash)
        git stash apply "${ARG:-stash@{0}}"
        ;;
    
    # Remote operations
    "r:l"|"rl")
        # List remotes
        git remote -v
        ;;
    
    "r:f"|"rf")
        # Fetch all
        git fetch --all --prune
        ;;
    
    # Quick commit
    "c"|"commit")
        # Quick commit with message
        if [ -z "$ARG" ]; then
            echo "Error: Commit message required"
            echo "Usage: git_quick.sh c <message>"
            exit 1
        fi
        git add -A
        git commit -m "$ARG"
        ;;
    
    "c:a"|"ca")
        # Amend last commit
        git commit --amend --no-edit
        ;;
    
    # Help
    "h"|"help"|"")
        cat << 'HELP'
Git Quick Commands
==================

Branch Operations:
  b:l, bl          List all branches
  b:c, bc          Show current branch
  b-> <name>       Switch to branch
  b:n <name>       Create new branch from current
  b:d <name>       Delete branch (safe)

Status & Info:
  s, st            Short status
  s:f, sf          Full status
  l, log           Recent commits (graph)
  l:a, la          All branches commits (graph)
  l:f, lf          Last commit details

Diff:
  d, diff          Show unstaged changes
  d:s, ds          Show staged changes
  d:st, dst        Diff summary (stat)

Stash:
  st:s, sts        Stash changes
  st:l, stl        List stashes
  st:p, stp        Pop stash
  st:a, sta        Apply stash (keep)

Remote:
  r:l, rl          List remotes
  r:f, rf          Fetch all

Quick Commit:
  c <msg>          Add all & commit
  c:a, ca          Amend last commit

Help:
  h, help          Show this help

Examples:
  git_quick.sh b:l              # List branches
  git_quick.sh b-> feature      # Switch to feature branch
  git_quick.sh b:n fix-bug      # Create new branch fix-bug
  git_quick.sh s                # Quick status
  git_quick.sh l                # Recent commits
HELP
        ;;
    
    *)
        echo "Unknown command: $CMD"
        echo "Run 'git_quick.sh help' for usage"
        exit 1
        ;;
esac
