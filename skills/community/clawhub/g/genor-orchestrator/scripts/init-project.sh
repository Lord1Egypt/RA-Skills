#!/usr/bin/env bash
# init-project.sh — Scaffold a new project's .planning directory
# Usage: bash scripts/init-project.sh <project-path> <project-name> [stack]
#
# Example:
#   bash scripts/init-project.sh ~/projects/myapp "My App" "nextjs+postgres"

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="${ORCHESTRATOR_DATA_DIR:-$(dirname "$(dirname "$SKILL_DIR")")/orchestrator-data}"
PROJECTS_DIR="$DATA_DIR/projects"

PROJECT_PATH="${1:-}"
PROJECT_NAME="${2:-}"
STACK="${3:-unknown}"

if [ -z "$PROJECT_PATH" ] || [ -z "$PROJECT_NAME" ]; then
    echo "Usage: bash scripts/init-project.sh <project-path> <project-name> [stack]"
    echo ""
    echo "Arguments:"
    echo "  project-path  — Absolute path to the project directory"
    echo "  project-name  — Human-readable project name"
    echo "  stack         — Optional stack description (e.g., nextjs+postgres)"
    exit 1
fi

PLANNING_DIR="$PROJECT_PATH/.planning"

if [ -d "$PLANNING_DIR" ]; then
    echo "⚠️  Planning directory already exists at $PLANNING_DIR"
    echo "   Use existing files or remove the directory first."
    exit 0
fi

mkdir -p "$PLANNING_DIR/ADRs"

# CONFIG.md
cat > "$PLANNING_DIR/CONFIG.md" << CONFIGEOF
# $PROJECT_NAME — Configuration

**Stack:** $STACK
**Created:** $(date '+%Y-%m-%d')
**Status:** Initialising

## Ports & Services
- (to be filled)

## Environment Variables
- (to be filled)

## Dependencies
- (to be filled)
CONFIGEOF

# STATE.md
cat > "$PLANNING_DIR/STATE.md" << STATEEOF
# $PROJECT_NAME — State

**Current Phase:** Initialisation
**Status:** Planned

## What's Been Done
- (nothing yet)

## What's Next
- [ ] Project setup

## Known Issues
- (none)
STATEEOF

# ROADMAP.md
cat > "$PLANNING_DIR/ROADMAP.md" << ROADMAPEOF
# $PROJECT_NAME — Roadmap

## Milestone 1: MVP
- [ ] Core functionality
- [ ] Basic UI
- [ ] Initial deploy

## Milestone 2: Polish
- [ ] Error handling
- [ ] Testing
- [ ] Documentation

## Backlog
- (to be filled)
ROADMAPEOF

# REQUIREMENTS.md
cat > "$PLANNING_DIR/REQUIREMENTS.md" << REQEOF
# $PROJECT_NAME — Requirements

## Functional
- (to be filled)

## Non-Functional
- (to be filled)

## Constraints
- (to be filled)
REQEOF

echo "✅ Project scaffolded: $PROJECT_NAME"
echo "   Location: $PLANNING_DIR"
echo ""
echo "   Files created:"
echo "   - CONFIG.md"
echo "   - STATE.md"
echo "   - ROADMAP.md"
echo "   - REQUIREMENTS.md"
echo "   - ADRs/ (empty)"
echo ""

# Register in orchestrator data directory
mkdir -p "$PROJECTS_DIR"
# Build filesystem-safe slugs for the filename
PROJECT_SLUG=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
PATH_SLUG=$(basename "$PROJECT_PATH" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
PROJECT_REF="$PROJECTS_DIR/$PROJECT_SLUG-$PATH_SLUG.md"
if [ ! -f "$PROJECT_REF" ]; then
  cat > "$PROJECT_REF" << REFEOF
# $PROJECT_NAME

**Path:** $PROJECT_PATH
**Stack:** $STACK
**Created:** $(date '+%Y-%m-%d')
**Status:** Scaffolded

## Sessions
(none yet)

## Notes
-
REFEOF
  echo "   Registered in orchestrator: $PROJECT_REF"
  echo ""
fi

echo "   Next: Edit these files with project-specific details."
echo "   Set ORCHESTRATOR_DATA_DIR to override data location (default: $DATA_DIR)"