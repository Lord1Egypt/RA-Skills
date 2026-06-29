#!/usr/bin/env bash
# log-decision.sh — Log an architecture decision to the project's ADR
# Usage: bash scripts/log-decision.sh <project-path> <title> <context> <decision> [alternatives] [consequences]
#
# Example:
#   bash scripts/log-decision.sh ~/projects/<name> "<Title>" "<Context>" "<Decision>" "<Alternatives>" "<Consequences>"

set -euo pipefail

PROJECT_PATH="${1:-}"
TITLE="${2:-}"
CONTEXT="${3:-}"
DECISION="${4:-}"
ALTERNATIVES="${5:-}"
CONSEQUENCES="${6:-}"

if [ -z "$PROJECT_PATH" ] || [ -z "$TITLE" ]; then
    echo "Usage: bash scripts/log-decision.sh <project-path> <title> <context> <decision> [alternatives] [consequences]"
    exit 1
fi

ADRS_DIR="$PROJECT_PATH/.planning/ADRs"
mkdir -p "$ADRS_DIR"

# Create a slug from the title
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
DATE=$(date '+%Y-%m-%d')
FILENAME="$ADRS_DIR/${DATE}-${SLUG}.md"

cat > "$FILENAME" << ADREOF
# ADR: $TITLE

**Date:** $DATE
**Status:** Accepted

## Context
$CONTEXT

## Decision
$DECISION

## Alternatives Considered
$ALTERNATIVES

## Consequences
$CONSEQUENCES

## Related
- (link to related ADRs or discussions)
ADREOF

echo "✅ Decision logged: $TITLE"
echo "   File: $FILENAME"