#!/bin/bash
# Auto-sync script for Easy-xiaohongshu skill
# Commits any changes to the local git repository

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if there are any changes
if git diff --quiet && git diff --cached --quiet; then
    echo "✅ No changes to sync"
    exit 0
fi

# Add all changes
git add -A

# Create commit with timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "Auto-sync: Changes at $TIMESTAMP"

echo "✅ Synced changes at $TIMESTAMP"
