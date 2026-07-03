#!/bin/bash
# load-context.sh — Load project context for Geordi builds
# Usage: load-context.sh <project-path>
# Outputs structured context block to stdout for injection into task prompts
# Exits 1 if no context file found (build should not proceed without context)

set -euo pipefail

PROJECT_PATH="${1:?Usage: load-context.sh <project-path>}"
PROJECT_PATH="${PROJECT_PATH/#\~/$HOME}"

if [ ! -d "$PROJECT_PATH" ]; then
  echo "❌ ERROR: Project path does not exist: $PROJECT_PATH" >&2
  exit 1
fi

PROJECT_NAME=$(basename "$PROJECT_PATH")
MEMORY_DIR="$HOME/clawd/memory"
CONTEXT_FILE=""

# --- Context file discovery (priority order) ---

# 1. CONTEXT.md at repo root (standard per PROJECT CONTEXT FILE RULE)
if [ -f "$PROJECT_PATH/CONTEXT.md" ]; then
  CONTEXT_FILE="$PROJECT_PATH/CONTEXT.md"

# 2. Known project mappings
elif [ "$PROJECT_NAME" = "entity" ] && [ -f "$MEMORY_DIR/entity-project-context.md" ]; then
  CONTEXT_FILE="$MEMORY_DIR/entity-project-context.md"

# 3. memory/<project-name>-context.md
elif [ -f "$MEMORY_DIR/${PROJECT_NAME}-context.md" ]; then
  CONTEXT_FILE="$MEMORY_DIR/${PROJECT_NAME}-context.md"

# 4. memory/<project-name>-project-context.md
elif [ -f "$MEMORY_DIR/${PROJECT_NAME}-project-context.md" ]; then
  CONTEXT_FILE="$MEMORY_DIR/${PROJECT_NAME}-project-context.md"

# 5. memory/projects/<project-name>/context.md
elif [ -f "$MEMORY_DIR/projects/${PROJECT_NAME}/context.md" ]; then
  CONTEXT_FILE="$MEMORY_DIR/projects/${PROJECT_NAME}/context.md"
fi

if [ -z "$CONTEXT_FILE" ]; then
  echo "❌ ERROR: No context file found for project '$PROJECT_NAME'" >&2
  echo "  Searched:" >&2
  echo "    - $PROJECT_PATH/CONTEXT.md" >&2
  echo "    - $MEMORY_DIR/${PROJECT_NAME}-context.md" >&2
  echo "    - $MEMORY_DIR/${PROJECT_NAME}-project-context.md" >&2
  echo "    - $MEMORY_DIR/projects/${PROJECT_NAME}/context.md" >&2
  echo "" >&2
  echo "  Create one first: update-context.sh $PROJECT_PATH --init" >&2
  exit 1
fi

# --- Output structured context block ---

echo "=== PROJECT CONTEXT (from $CONTEXT_FILE) ==="
echo ""
cat "$CONTEXT_FILE"
echo ""

# --- Supplement with key project files ---

echo "=== SUPPLEMENTARY PROJECT INFO ==="
echo ""

# package.json summary
if [ -f "$PROJECT_PATH/package.json" ]; then
  echo "## package.json"
  python3 -c "
import json, sys
try:
    pkg = json.load(open('$PROJECT_PATH/package.json'))
    print(f\"Name: {pkg.get('name', '?')}\")
    print(f\"Version: {pkg.get('version', '?')}\")
    deps = list(pkg.get('dependencies', {}).keys())[:15]
    if deps: print(f\"Key deps: {', '.join(deps)}\")
    scripts = list(pkg.get('scripts', {}).keys())
    if scripts: print(f\"Scripts: {', '.join(scripts)}\")
except: pass
" 2>/dev/null
  echo ""
fi

# TESTING.md
if [ -f "$PROJECT_PATH/TESTING.md" ]; then
  echo "## TESTING.md (first 20 lines)"
  head -20 "$PROJECT_PATH/TESTING.md"
  echo ""
fi

# PRD.md (first 30 lines)
if [ -f "$PROJECT_PATH/PRD.md" ]; then
  echo "## PRD.md (first 30 lines)"
  head -30 "$PROJECT_PATH/PRD.md"
  echo ""
fi

# Recent git log
if [ -d "$PROJECT_PATH/.git" ]; then
  echo "## Recent commits"
  git -C "$PROJECT_PATH" log --oneline -10 2>/dev/null || true
  echo ""
fi

echo "=== END PROJECT CONTEXT ==="
