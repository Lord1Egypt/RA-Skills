#!/bin/bash
set -euo pipefail

echo "🧠 Initializing Agent Memory Protocol..."

# Get workspace directory
WORKSPACE="${1:-$(pwd)}"
cd "$WORKSPACE"

# Ensure AGENT_MEMORY_PROTOCOL.md exists
if [[ ! -f "AGENT_MEMORY_PROTOCOL.md" ]]; then
    echo "❌ AGENT_MEMORY_PROTOCOL.md not found. Run install.sh first."
    exit 1
fi

echo "✅ Memory protocol found"

# Create memory directory
mkdir -p memory
echo "📁 Memory directory created"

# Create today's memory file
TODAY_FILE="memory/$(date +%Y-%m-%d).md"
if [[ ! -f "$TODAY_FILE" ]]; then
    cat > "$TODAY_FILE" << EOF
# $(date +%Y-%m-%d) Daily Memory

## Key Conversations
- [Add significant discussion topics here]

## Decisions Made
- [Log important decisions here]

## Ongoing Projects
- [Track project status here]

## Context Notes
- [Add context that should be preserved here]

## Tomorrow's Priorities
- [Note items for next session here]
EOF
    echo "📝 Today's memory file created: $TODAY_FILE"
else
    echo "📝 Today's memory file already exists: $TODAY_FILE"
fi

# Update main MEMORY.md if it exists
if [[ -f "MEMORY.md" ]]; then
    echo "" >> MEMORY.md
    echo "## Agent Memory Protocol Initialized ($(date +%Y-%m-%d))" >> MEMORY.md
    echo "- Search-first protocol: Active" >> MEMORY.md
    echo "- Daily memory logging: Enabled" >> MEMORY.md
    echo "- Context preservation: Operational" >> MEMORY.md
    echo "📋 MEMORY.md updated with protocol status"
fi

echo ""
echo "🎯 Memory Protocol Initialized Successfully!"
echo ""
echo "Next steps:"
echo "  1. Configure search-first behavior: bash scripts/configure-search-first.sh"
echo "  2. Activate memory sync: bash scripts/activate-memory-sync.sh"
echo "  3. Test the system: bash scripts/test-memory-continuity.sh"