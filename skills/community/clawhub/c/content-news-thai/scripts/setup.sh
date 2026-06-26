#!/bin/bash
# Content News Thai — Setup Script
# Installs dependencies for generating news images with Thai text overlay
# Works on: Ubuntu/Debian (Docker), macOS

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "🔧 Setting up Content News Thai..."
echo "   Skill dir: $SKILL_DIR"

# === 1. Detect OS ===
if [[ "$OSTYPE" == "darwin"* ]]; then
  OS="macos"
elif [[ -f /etc/debian_version ]]; then
  OS="debian"
else
  OS="linux"
fi
echo "   OS: $OS"

# === 2. Install system dependencies ===
if [[ "$OS" == "debian" ]]; then
  echo "📦 Installing system dependencies..."
  apt-get update -qq
  apt-get install -y -qq build-essential libcairo2-dev libjpeg-dev libpango1.0-dev libgif-dev librsvg2-dev pkg-config 2>/dev/null || {
    echo "⚠️  apt-get failed — trying without sudo"
    sudo apt-get update -qq
    sudo apt-get install -y -qq build-essential libcairo2-dev libjpeg-dev libpango1.0-dev libgif-dev librsvg2-dev pkg-config
  }
elif [[ "$OS" == "macos" ]]; then
  if ! command -v brew &>/dev/null; then
    echo "⚠️  Homebrew not found. Install from https://brew.sh"
  else
    echo "📦 Installing system dependencies (macOS)..."
    brew list cairo &>/dev/null || brew install cairo
    brew list pango &>/dev/null || brew install pango
    brew list pkg-config &>/dev/null || brew install pkg-config
  fi
fi

# === 3. Install Node.js dependencies ===
echo "📦 Installing canvas npm package..."
cd "$SKILL_DIR/scripts"
if [[ ! -f package.json ]]; then
  cat > package.json << 'EOF'
{
  "name": "content-news-thai",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "canvas": "^3.1.0"
  }
}
EOF
fi
npm install --production 2>&1 | tail -3

# === 4. Download Thai fonts ===
FONTS_DIR="$SKILL_DIR/assets/fonts"
mkdir -p "$FONTS_DIR"

download_font() {
  local url="$1"
  local name="$2"
  if [[ ! -f "$FONTS_DIR/$name" ]]; then
    echo "   Downloading $name..."
    curl -sL "$url" -o "$FONTS_DIR/$name"
  fi
}

echo "📝 Downloading Thai fonts..."
# Kanit Bold
download_font "https://github.com/google/fonts/raw/main/ofl/kanit/Kanit-Bold.ttf" "Kanit-Bold.ttf"
# Kanit Light  
download_font "https://github.com/google/fonts/raw/main/ofl/kanit/Kanit-Light.ttf" "Kanit-Light.ttf"
# Sarabun SemiBold
download_font "https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-SemiBold.ttf" "Sarabun-SemiBold.ttf"
# Prompt Bold
download_font "https://github.com/google/fonts/raw/main/ofl/prompt/Prompt-Bold.ttf" "Prompt-Bold.ttf"

# === 5. Install fonts system-wide (Linux) ===
if [[ "$OS" == "debian" || "$OS" == "linux" ]]; then
  SYSFONT_DIR="/usr/local/share/fonts/thai"
  mkdir -p "$SYSFONT_DIR" 2>/dev/null || sudo mkdir -p "$SYSFONT_DIR"
  cp "$FONTS_DIR"/*.ttf "$SYSFONT_DIR/" 2>/dev/null || sudo cp "$FONTS_DIR"/*.ttf "$SYSFONT_DIR/"
  fc-cache -f 2>/dev/null || true
  echo "   Fonts installed to $SYSFONT_DIR"
fi

# === 6. Verify ===
echo ""
echo "🔍 Verifying setup..."
node -e "import('canvas').then(c => { console.log('   ✅ canvas:', c.default ? 'OK' : 'OK'); }).catch(e => { console.log('   ❌ canvas:', e.message); process.exit(1); })" 2>/dev/null && echo "" || {
  cd "$SKILL_DIR/scripts" && node -e "import('canvas').then(() => console.log('   ✅ canvas: OK')).catch(e => { console.log('   ❌ canvas:', e.message); process.exit(1); })"
}

echo "✅ Content News Thai setup complete!"
echo ""
echo "Usage: node $SKILL_DIR/scripts/gen-news.mjs '{\"headline\":\"ข่าวทดสอบ\",\"sub\":\"sub headline\",\"bgColor\":\"#1a1a2e\"}'"
