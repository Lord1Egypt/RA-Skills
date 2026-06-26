#!/bin/bash
# Clude MCP installer for any agent runtime
set -e

echo "🧠 Installing Clude memory engine..."

# Check if npx is available
if ! command -v npx &> /dev/null; then
    echo "❌ npx not found. Install Node.js first: https://nodejs.org"
    exit 1
fi

# Install clude-bot globally
echo "📦 Installing clude-bot..."
npm install -g clude-bot 2>/dev/null || npx clude-bot --version

# Run MCP install (auto-detects Claude Desktop, Cursor, etc.)
echo "⚙️ Configuring MCP server..."
npx clude-bot mcp-install --local 2>/dev/null || echo "MCP auto-install not available. See SKILL.md for manual config."

echo ""
echo "✅ Clude installed! Your agent now has persistent memory."
echo ""
echo "Tools available: remember, recall, forget, stats, visualize"
echo "Run 'npx clude-bot mcp-serve --local' to start the MCP server manually."
