#!/bin/bash
# Install acpx (ACP harness for multiple coding agents)
# Includes: Claude Code, Codex, Gemini CLI, Cursor, etc.

set -e

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt-get install -y nodejs
fi

# Install acpx globally
echo "Installing acpx..."
npm install -g @anthropic-ai/acpx

# Create config directory
mkdir -p ~/.acpx

# Create default config
cat > ~/.acpx/config.json << 'EOF'
{
  "defaultAgent": "claude-code",
  "agents": {
    "claude-code": {
      "command": "claude",
      "args": []
    },
    "codex": {
      "command": "codex",
      "args": []
    }
  }
}
EOF

echo "✅ acpx installed successfully"
echo "Usage: acpx <agent> <task>"
echo "Example: acpx claude-code 'fix the bug in app.ts'"
