#!/bin/bash
# Visualize merge conflicts in a readable format

set -e

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not a git repository"
    exit 1
fi

# Check if there are conflicts
if ! git diff --name-only --diff-filter=U | grep -q .; then
    echo "No merge conflicts detected"
    exit 0
fi

echo "=== Merge Conflicts Detected ==="
echo ""

# List conflicted files
echo "Conflicted files:"
git diff --name-only --diff-filter=U
echo ""

# Show detailed conflict markers for each file
for file in $(git diff --name-only --diff-filter=U); do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "File: $file"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Show the conflict with context
    cat "$file" | grep -B 3 -A 3 "^<<<<<<< \|^=======$\|^>>>>>>>" || cat "$file"
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Summary: $(git diff --name-only --diff-filter=U | wc -l) file(s) with conflicts"
