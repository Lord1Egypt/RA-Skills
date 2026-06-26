#!/usr/bin/env bash
# birdx install script
# Installs birdx CLI + required npm deps

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIRDX_JS="$SKILL_DIR/scripts/birdx.js"
MODULES_DIR="$HOME/clawd/node_modules"
BIN_TARGET=""

# Find node
if command -v node &>/dev/null; then
  NODE_BIN="$(command -v node)"
elif [ -x "/opt/homebrew/bin/node" ]; then
  NODE_BIN="/opt/homebrew/bin/node"
else
  echo "❌ node not found. Install via: brew install node"
  exit 1
fi
echo "✅ node: $($NODE_BIN --version) at $NODE_BIN"

# Fix shebang to use found node
sed -i '' "s|#!/usr/bin/env node|#!$NODE_BIN|" "$BIRDX_JS" 2>/dev/null \
  || sed -i "s|#!/usr/bin/env node|#!$NODE_BIN|" "$BIRDX_JS"
chmod +x "$BIRDX_JS"

# Install npm deps
echo "📦 Installing deps (ws, jsdom, x-client-transaction-id)..."
mkdir -p "$MODULES_DIR"
cd "$HOME/clawd"
[ ! -f package.json ] && echo '{"name":"clawd","private":true}' > package.json
npm install --prefix "$HOME/clawd" ws jsdom x-client-transaction-id --save-exact --silent
echo "✅ Deps installed to $MODULES_DIR"

# Symlink birdx to PATH
if [ -d "/opt/homebrew/bin" ]; then
  BIN_TARGET="/opt/homebrew/bin/birdx"
elif [ -d "$HOME/.local/bin" ]; then
  BIN_TARGET="$HOME/.local/bin/birdx"
else
  mkdir -p "$HOME/.local/bin"
  BIN_TARGET="$HOME/.local/bin/birdx"
fi

ln -sf "$BIRDX_JS" "$BIN_TARGET"
echo "✅ Symlinked: $BIN_TARGET -> $BIRDX_JS"

# Run auth
echo ""
echo "🔑 Running birdx auth (reads Chrome cookies from disk)..."
"$BIRDX_JS" auth

echo ""
echo "🎉 birdx installed! Try: birdx search 'OpenAI'"
