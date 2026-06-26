#!/usr/bin/env bash
# eor-log.sh v2 — Single executive EOR log per project
#
# Usage: eor-log.sh <project-dir> [summary-text]
#
# Maintains ONE living EOR log per project at:
#   - <project>/docs/EOR.md (codebase, pushed to GitHub)
#   - $OBSIDIAN_BASE/<Project>/EOR.md (Obsidian vault, if OBSIDIAN_BASE is set)
#
# This is NOT a per-agent log. It's an executive summary maintained by the orchestrator.
# Contains: what's been achieved, latest updates, what's next, actionable levers.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
[[ -f "$SCRIPT_DIR/swarm.conf" ]] && source "$SCRIPT_DIR/swarm.conf"

PROJECT_DIR="${1:?Usage: eor-log.sh <project-dir> [summary-text]}"
SUMMARY="${2:-}"

PROJECT_NAME=$(basename "$PROJECT_DIR")
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
DATE=$(date "+%Y-%m-%d")

# Determine paths
CODEBASE_EOR="$PROJECT_DIR/docs/EOR.md"
OBSIDIAN_BASE="${OBSIDIAN_BASE:-}"

# Create codebase docs directory
mkdir -p "$PROJECT_DIR/docs"

# If EOR doesn't exist yet, create template
if [[ ! -f "$CODEBASE_EOR" ]]; then
  cat > "$CODEBASE_EOR" << TEMPLATE
# $PROJECT_NAME — Executive Summary (EOR)
*Last updated: $TIMESTAMP*

## What We've Built
<!-- High-level summary of what exists -->

## Latest Updates
<!-- Most recent session's work -->

## What's Next
<!-- Prioritized next steps -->

## Actionable Levers
<!-- What would it take to make this succeed? Key decisions, resources, blockers -->

## Learnings
<!-- Technical and product lessons learned -->

---
*This is a living document maintained by the orchestrator. Updated after each work session.*
TEMPLATE
fi

# If summary provided, append as an update
if [[ -n "$SUMMARY" ]]; then
  # Update the "Last updated" timestamp
  sed -i "s/\*Last updated:.*\*/*Last updated: $TIMESTAMP*/" "$CODEBASE_EOR"

  # Append update entry
  cat >> "$CODEBASE_EOR" << UPDATE

### Update: $TIMESTAMP
$SUMMARY
UPDATE
fi

echo "[eor] Updated EOR for $PROJECT_NAME at $TIMESTAMP"
echo "  → $CODEBASE_EOR"

# Sync to Obsidian (optional)
if [[ -n "$OBSIDIAN_BASE" ]]; then
  OBSIDIAN_EOR="$OBSIDIAN_BASE/$PROJECT_NAME/EOR.md"
  mkdir -p "$OBSIDIAN_BASE/$PROJECT_NAME"
  cp "$CODEBASE_EOR" "$OBSIDIAN_EOR"
  echo "  → $OBSIDIAN_EOR"
fi
