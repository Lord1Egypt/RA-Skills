#!/bin/bash

# Cavepony hook installer for Claude Code
# Installs auto-activation hooks for cavepony mode

set -e

echo "🏍️ Installing Cavepony hooks for Claude Code..."

# Determine Claude Code config directory
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS
  CONFIG_DIR="$HOME/Library/Application Support/Claude Code"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
  # Linux
  CONFIG_DIR="$HOME/.config/claude-code"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
  echo "Windows not yet supported. Please install manually."
  exit 1
else
  echo "Unsupported OS: $OSTYPE"
  exit 1
fi

HOOKS_DIR="$CONFIG_DIR/hooks"
CAVEPONY_HOOK="$HOOKS_DIR/cavepony.js"

# Create hooks directory if it doesn't exist
mkdir -p "$HOOKS_DIR"

# Check if cavepony hook already exists
if [[ -f "$CAVEPONY_HOOK" ]]; then
  echo "⚠️  Cavepony hook already exists at: $CAVEPONY_HOOK"
  echo "   Overwrite? (y/N)"
  read -r response
  if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "❌ Aborting."
    exit 1
  fi
fi

# Create the hook file
cat > "$CAVEPONY_HOOK" << 'EOF'
// Cavepony hook for Claude Code
// Auto-activates cavepony mode on session start

module.exports = {
  name: 'Cavepony',
  description: 'Auto-activate cavepony mode on session start',
  
  onSessionStart: async (context) => {
    // Add cavepony rules to the session
    await context.addSystemPrompt(`
Terse like cavepony. Technical substance exact. Only fluff die.
Drop: articles, filler (just/really/basically), pleasantries, hedging.
Fragments OK. Short synonyms. Code unchanged.
Pattern: [thing] [action] [reason]. [next step].
Pony substitutions: human/people -> pony/ponies, man/woman -> stallion/mare, boy/girl -> colt/filly, child/children -> foal/foals, hand/foot -> hoof/hooves, hey -> hay, hell/heck -> hay, Christmas -> Heartswarming, New York -> Manehattan, Philadelphia -> Fillydelphia, etc.
ACTIVE EVERY RESPONSE. No revert after many turns. No filler drift.
Code/commits/PRs: normal. Off: "stop cavepony" / "normal mode".
    `);
    
    // Set status line indicator
    context.setStatusLine('[CAVEPONY]');
    
    console.log('🏍️ Cavepony mode activated!');
  }
};
EOF

echo "✅ Cavepony hook installed at: $CAVEPONY_HOOK"
echo ""
echo "To enable cavepony in Claude Code:"
echo "1. Restart Claude Code"
echo "2. Check status line shows [CAVEPONY]"
echo ""
echo "Commands:"
echo "  /cavepony pony    - Activate pony mode (with substitutions)"
echo "  /cavepony full    - Standard compression"
echo "  /cavepony lite    - Light compression"
echo "  /cavepony ultra   - Maximum compression"
echo "  /normal           - Return to normal mode"
echo ""
echo "🐴 Happy hoofing!"