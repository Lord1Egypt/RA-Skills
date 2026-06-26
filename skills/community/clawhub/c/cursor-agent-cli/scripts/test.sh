#!/bin/bash
# Test script for cursor-agent-cli skill

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "🧪 Testing Cursor Agent CLI Skill"
echo "=========================="
echo ""

# Test 1: Check if agent is installed
echo "Test 1: Check agent installation"
if command -v agent &> /dev/null; then
    echo "✅ agent command found"
    agent --version
else
    echo "❌ agent command not found"
    echo "Install: curl https://cursor.com/install -fsS | bash"
    exit 1
fi
echo ""

# Test 2: Check helper script
echo "Test 2: Check helper script"
if [ -x "$SCRIPT_DIR/cursor-agent.sh" ]; then
    echo "✅ cursor-agent.sh is executable"
else
    echo "❌ cursor-agent.sh not executable"
    chmod +x "$SCRIPT_DIR/cursor-agent.sh"
    echo "✅ Fixed permissions"
fi
echo ""

# Test 3: Test helper script commands
echo "Test 3: Test helper commands"
"$SCRIPT_DIR/cursor-agent.sh" help > /dev/null
echo "✅ Help command works"
echo ""

# Test 4: Check authentication status
echo "Test 4: Check authentication"
if agent status > /dev/null 2>&1; then
    echo "✅ Authenticated"
    agent status
else
    echo "⚠️  Not authenticated"
    echo "Run: agent login"
fi
echo ""

# Test 5: List available models
echo "Test 5: List models"
if agent --list-models > /dev/null 2>&1; then
    echo "✅ Can list models"
else
    echo "⚠️  Cannot list models (authentication required)"
fi
echo ""

# Test 6: Check session list
echo "Test 6: Check sessions"
if agent ls > /dev/null 2>&1; then
    echo "✅ Can list sessions"
    echo "Total sessions:"
    agent ls | wc -l
else
    echo "⚠️  Cannot list sessions"
fi
echo ""

echo "=========================="
echo "✅ Cursor Agent CLI Skill test complete"
echo ""
echo "Next steps:"
echo "1. Run: agent login (if not authenticated)"
echo "2. Try: agent 'hello world'"
echo "3. Read: cat SKILL.md"
