#!/bin/bash
# FlowForge — Initialize a new forge workspace
# Usage: init_forge.sh "<task_description>" "<repo_path>"

set -e

TASK="${1:-}"
REPO="${2:-$(pwd)}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
WORKSPACE="$HOME/.forge/$TIMESTAMP"

mkdir -p "$WORKSPACE"

cat > "$WORKSPACE/task.md" << TASK
# Task

$TASK

## Repository
$REPO

## Started
$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TASK

cat > "$WORKSPACE/forge.env" << ENV
REPO_PATH="$REPO"
WORKSPACE="$WORKSPACE"
TIMESTAMP="$TIMESTAMP"
ENV

echo "✅ Workspace: $WORKSPACE"
echo "📝 Edit $WORKSPACE/task.md if needed, then run:"
echo "   bash $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/run_forge.sh $WORKSPACE"
