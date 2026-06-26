#!/bin/bash
# Save git diff before merge/rebase for conflict resolution tracking

set -e

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not a git repository"
    exit 1
fi

# Create diffs directory if it doesn't exist
DIFF_DIR=".git/merge-diffs"
mkdir -p "$DIFF_DIR"

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Get current branch or HEAD
BRANCH=$(git branch --show-current)
if [ -z "$BRANCH" ]; then
    # Detached HEAD state
    BRANCH="detached_$(git rev-parse --short HEAD)"
    echo "⚠️  In detached HEAD state"
fi

# Save current state diff
DIFF_FILE="$DIFF_DIR/${TIMESTAMP}_${BRANCH}.diff"
git diff HEAD > "$DIFF_FILE"

# Save staged changes if any
if ! git diff --cached --quiet; then
    STAGED_FILE="$DIFF_DIR/${TIMESTAMP}_${BRANCH}_staged.diff"
    git diff --cached > "$STAGED_FILE"
    echo "Saved staged changes to: $STAGED_FILE"
fi

echo "Saved current diff to: $DIFF_FILE"
echo ""
echo "To view later: cat $DIFF_FILE"
echo "To apply: git apply $DIFF_FILE"
