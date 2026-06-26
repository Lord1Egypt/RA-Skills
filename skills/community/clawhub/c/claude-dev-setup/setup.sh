#!/bin/bash
# Claude Dev Setup - Installation Script
# Run this after installing the skill via clawhub

set -e

echo "🤖 Claude Dev Setup"
echo "==================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check if claude CLI is installed
if ! command -v claude &> /dev/null; then
    echo "⚠️  Claude Code CLI not found. Installing..."
    npm install -g @anthropic-ai/claude-code
else
    echo "✓ Claude Code CLI installed: $(claude --version)"
fi

# Check if authenticated
if [ ! -f "$HOME/.claude/.credentials.json" ]; then
    echo ""
    echo "⚠️  Not authenticated. Run: claude setup-token"
    echo "   You'll need a Claude Pro/Max subscription."
    echo ""
else
    echo "✓ Already authenticated with Claude"
fi

# Determine workspace
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace-gsoc}"
echo ""
echo "Workspace: $WORKSPACE"
echo ""

# Create memory directory if needed
mkdir -p "$WORKSPACE/memory"

# Create sessions file if it doesn't exist
SESSIONS_FILE="$WORKSPACE/memory/claude-code-sessions.md"
if [ ! -f "$SESSIONS_FILE" ]; then
    echo "Creating session tracking file..."
    cat > "$SESSIONS_FILE" << 'EOF'
# Claude Code CLI Sessions

## Purpose
Track background Claude Code CLI sessions for status queries.

## Session Registry

| Session ID | Label | Task | Started | Status |
|------------|-------|------|---------|--------|
| (populated at runtime) | (human-readable name) | (what it's doing) | (timestamp) | (running/completed/failed) |

EOF
    echo "✓ Created $SESSIONS_FILE"
else
    echo "✓ Session file already exists"
fi

# Check if AGENTS.md exists and needs updating
AGENTS_FILE="$WORKSPACE/AGENTS.md"
if [ -f "$AGENTS_FILE" ]; then
    if grep -q "Claude Code CLI Sessions" "$AGENTS_FILE"; then
        echo "✓ AGENTS.md already has session section"
    else
        echo ""
        echo "⚠️  AGENTS.md exists but missing session section."
        echo "   Add the following to AGENTS.md:"
        echo ""
        cat "$(dirname "$0")/agents-section.md"
        echo ""
    fi
else
    echo "⚠️  No AGENTS.md found at $AGENTS_FILE"
fi

# Check for dependent skills
echo ""
echo "Checking dependent skills..."
SKILLS_DIR="$WORKSPACE/skills"

for skill in claude-code-cli-openclaw apex-stack-claude-code; do
    if [ -d "$SKILLS_DIR/$skill" ]; then
        echo "✓ $skill installed"
    else
        echo "⚠️  $skill not found. Install with: clawhub install $skill"
    fi
done

echo ""
echo "=========================="
echo "Setup complete! ✅"
echo ""
echo "Next steps:"
echo "1. Authenticate if not done: claude setup-token"
echo "2. Add APEX Stack to project CLAUDE.md files"
echo "3. Start coding: claude --print 'your task'"
echo ""