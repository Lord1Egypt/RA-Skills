#!/usr/bin/env bash
# Auto-setup: clone/update meme repo + install CLI
set -e

MEME_DIR="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}/memes"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 1. Clone or update meme repo
if [ -d "$MEME_DIR/.git" ]; then
  echo "📦 Updating memes..."
  cd "$MEME_DIR" && git pull --ff-only
else
  echo "📦 Cloning meme repo..."
  git lfs install 2>/dev/null || true
  git clone https://github.com/kagura-agent/memes "$MEME_DIR"
fi

# 2. Git LFS pull (critical! without this, images are 132-byte pointers)
cd "$MEME_DIR"
if command -v git-lfs &>/dev/null || git lfs version &>/dev/null 2>&1; then
  echo "📦 Pulling LFS files..."
  git lfs pull
else
  echo "⚠️  git-lfs not installed! Images will be broken pointer files."
  echo "   Install: https://git-lfs.com then run: cd $MEME_DIR && git lfs pull"
fi

FILE_COUNT=$(find "$MEME_DIR" -type f \( -name '*.gif' -o -name '*.jpg' -o -name '*.png' -o -name '*.webp' \) -size +1k | wc -l)
echo "✅ Memes ready at $MEME_DIR ($FILE_COUNT image files)"

# 3. Install CLI (memes command)
chmod +x "$SCRIPT_DIR/memes.sh"
chmod +x "$SCRIPT_DIR"/*-send-image.sh 2>/dev/null || true
if [ -d "$HOME/.local/bin" ]; then
  cp "$SCRIPT_DIR/memes.sh" "$HOME/.local/bin/memes"
  chmod +x "$HOME/.local/bin/memes"
  echo "✅ CLI installed at ~/.local/bin/memes"
elif [ -w /usr/local/bin ]; then
  cp "$SCRIPT_DIR/memes.sh" /usr/local/bin/memes
  chmod +x /usr/local/bin/memes
  echo "✅ CLI installed at /usr/local/bin/memes"
else
  mkdir -p "$HOME/.local/bin"
  cp "$SCRIPT_DIR/memes.sh" "$HOME/.local/bin/memes"
  chmod +x "$HOME/.local/bin/memes"
  echo "✅ CLI installed at ~/.local/bin/memes (add to PATH if needed)"
fi

# 4. Install platform-specific helpers
TARGET_DIR="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}/scripts"
mkdir -p "$TARGET_DIR"
if [ -f "$SCRIPT_DIR/feishu-send-image.mjs" ]; then
  cp "$SCRIPT_DIR/feishu-send-image.mjs" "$TARGET_DIR/feishu-send-image.mjs"
  echo "✅ Feishu quick-send script installed"
fi

echo ""
echo "🎉 Setup complete! Try: memes categories"
