#!/bin/bash
set -eo pipefail

echo "🧠 Installing Agent Memory Continuity Skill..."
echo "Solving the 'agent forgot everything' problem"

# Get workspace directory
WORKSPACE="${1:-$(pwd)}"
if [[ ! -d "$WORKSPACE" ]]; then
    echo "❌ Workspace directory not found: $WORKSPACE"
    exit 1
fi

echo "📁 Installing to: $WORKSPACE"

# Create memory directory structure
echo "🏗️  Creating memory structure..."
mkdir -p "$WORKSPACE/memory"
mkdir -p "$WORKSPACE/reports"

# Copy memory protocol template
echo "📋 Installing memory protocol..."
cp templates/AGENT_MEMORY_PROTOCOL.md "$WORKSPACE/AGENT_MEMORY_PROTOCOL.md"

# Create today's memory file if it doesn't exist
TODAY_MEMORY="$WORKSPACE/memory/$(date +%Y-%m-%d).md"
if [[ ! -f "$TODAY_MEMORY" ]]; then
    echo "📝 Creating today's memory file..."
    cp templates/daily-memory-template.md "$TODAY_MEMORY"
    sed -i "s/YYYY-MM-DD/$(date +%Y-%m-%d)/g" "$TODAY_MEMORY"
fi

# Copy config files
echo "⚙️  Installing configuration..."
cp config/memory-config.json "$WORKSPACE/.memory-config.json" 2>/dev/null || echo '{"memory_continuity": {"enabled": true}}' > "$WORKSPACE/.memory-config.json"
cp config/search-patterns.txt "$WORKSPACE/.memory-search-patterns.txt" 2>/dev/null || echo "project decisions ongoing tasks" > "$WORKSPACE/.memory-search-patterns.txt"

# Make scripts executable
chmod +x scripts/*.sh

echo "✅ Agent Memory Continuity installed successfully!"
echo ""
echo "🚀 Quick Start:"
echo "  1. bash scripts/init-memory-protocol.sh"
echo "  2. bash scripts/activate-memory-sync.sh"
echo "  3. Test with: bash scripts/test-memory-continuity.sh"
echo ""
echo "📖 Documentation: docs/troubleshooting.md"
echo "🏢 Enterprise support: support@sapconet.co.za"