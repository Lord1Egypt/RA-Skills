#!/usr/bin/env bash
# Cognition — Install script
# Creates the memory directory structure and template files.
# Usage: bash scripts/install.sh [workspace_path]
# Default: ~/.openclaw/workspace

set -euo pipefail

WORKSPACE="${1:-$HOME/.openclaw/workspace}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES="$SKILL_DIR/templates"

echo "🧠 Cognition — Installing practical memory architecture"
echo "   Workspace: $WORKSPACE"
echo ""

# Create directories
for dir in \
  "memory/procedures" \
  "memory/consolidation" \
  "memory/summaries" \
  "memory/meta" \
  "memory/bank"
do
  if [[ ! -d "$WORKSPACE/$dir" ]]; then
    mkdir -p "$WORKSPACE/$dir"
    echo "  ✅ Created $dir/"
  else
    echo "  ⏭️  $dir/ already exists"
  fi
done

# Copy templates (non-destructive)
copy_template() {
  local src="$1"
  local dest="$2"
  if [[ ! -f "$dest" ]]; then
    cp "$src" "$dest"
    echo "  ✅ Created $(basename "$dest")"
  else
    echo "  ⏭️  $(basename "$dest") already exists (skipped)"
  fi
}

copy_template "$TEMPLATES/FUTURE_INTENTS.md" "$WORKSPACE/memory/FUTURE_INTENTS.md"
copy_template "$TEMPLATES/KNOWLEDGE_MAP.md" "$WORKSPACE/memory/KNOWLEDGE_MAP.md"
copy_template "$TEMPLATES/cross-references.md" "$WORKSPACE/memory/bank/cross-references.md"
copy_template "$TEMPLATES/procedures-index.yaml" "$WORKSPACE/memory/procedures/index.yaml"
copy_template "$TEMPLATES/gap_tracker.json" "$WORKSPACE/memory/meta/gap_tracker.json"
copy_template "$TEMPLATES/retrieval_log.json" "$WORKSPACE/memory/meta/retrieval_log.json"

echo ""
echo "🧠 Cognition installed!"
echo ""
echo "Next steps:"
echo "  1. Read SKILL.md for the 3-tier adoption guide"
echo "  2. Add the Memory Protocol from references/protocols.md to AGENTS.md"
echo "  3. Set up nightly consolidation with references/consolidation-prompt.md"
echo "  4. Treat memory/KNOWLEDGE_MAP.md and cross-references as optional Advanced overlays"
echo ""
