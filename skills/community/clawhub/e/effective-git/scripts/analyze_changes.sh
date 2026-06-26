#!/bin/bash
# Analyze recent git changes and provide summary

set -e

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not a git repository"
    exit 1
fi

# Get current branch or HEAD state
BRANCH=$(git branch --show-current)
if [ -z "$BRANCH" ]; then
    # Detached HEAD state
    BRANCH="(detached HEAD at $(git rev-parse --short HEAD))"
    echo "⚠️  Warning: In detached HEAD state"
fi
echo "Current branch: $BRANCH"
echo ""

# Check for uncommitted changes
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "=== Uncommitted Changes ==="
    git status --short
    echo ""
    echo "=== Detailed Diff ==="
    git diff --stat
    echo ""
fi

# Show recent commits (last 5)
echo "=== Recent Commits ==="
git log --oneline -5
echo ""

# Show last commit details
echo "=== Last Commit Details ==="
git log -1 --stat
