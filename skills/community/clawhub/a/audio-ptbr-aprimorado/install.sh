#!/bin/bash
# Audio PT Auto-Reply - Automatic Installation Script
# Detects architecture, downloads Piper, voice models, and dependencies

set -e

echo "🎙️  Audio PT Auto-Reply - Smart Installation"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detect architecture
ARCH=$(uname -m)
OS=$(uname -s)

echo -e "${BLUE}[1/6] Detecting system...${NC}"
echo "  Architecture: $ARCH"
echo "  OS: $OS"
echo ""

# Set Piper download URL based on architecture
case $ARCH in
  arm64|aarch64)
    PIPER_URL="https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz"
    PIPER_FILE="piper_arm64.tar.gz"
    echo -e "${GREEN}✓ ARM64 detected (Raspberry Pi, Apple Silicon)${NC}"
    ;;
  x86_64|amd64)
    PIPER_URL="https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_x86_64.tar.gz"
    PIPER_FILE="piper_x86_64.tar.gz"
    echo -e "${GREEN}✓ x86_64 detected (Intel/AMD)${NC}"
    ;;
  *)
    echo -e "${RED}✗ Unsupported architecture: $ARCH${NC}"
    exit 1
    ;;
esac

# Setup paths
WORKSPACE="${HOME}/.openclaw/workspace"
PIPER_DIR="${WORKSPACE}/piper"
VOICES_DIR="${PIPER_DIR}"
SKILL_DIR="${WORKSPACE}/skills/audio-ptbr-autoreply"
VENV="${WORKSPACE}/venv"

echo ""
echo -e "${BLUE}[2/6] Creating directories...${NC}"
mkdir -p "$PIPER_DIR"
mkdir -p "$VOICES_DIR"
mkdir -p "$(dirname $SKILL_DIR)"
echo -e "${GREEN}✓ Directories created${NC}"

echo ""
echo -e "${BLUE}[3/6] Installing Python dependencies...${NC}"

# Check for required system tools
for cmd in python3 pip ffmpeg; do
  if ! command -v $cmd &> /dev/null; then
    echo -e "${YELLOW}⚠ $cmd not found. Installing...${NC}"
    if [[ "$OS" == "Linux" ]]; then
      sudo apt-get update && sudo apt-get install -y $cmd
    elif [[ "$OS" == "Darwin" ]]; then
      brew install $cmd
    fi
  fi
done

# Install Python dependencies
python3 -m pip install --upgrade pip setuptools wheel > /dev/null 2>&1
python3 -m pip install -q transformers torch torchaudio anthropic

if [ -d "$VENV" ]; then
  source "$VENV/bin/activate"
  python -m pip install -q transformers torch torchaudio anthropic
  deactivate
fi

echo -e "${GREEN}✓ Python dependencies installed${NC}"

echo ""
echo -e "${BLUE}[4/6] Downloading Piper TTS...${NC}"

if [ -f "$PIPER_DIR/piper/piper" ]; then
  echo -e "${GREEN}✓ Piper already installed${NC}"
else
  echo "  Downloading from: $PIPER_URL"
  cd "$PIPER_DIR"
  wget -q "$PIPER_URL" -O "$PIPER_FILE"
  tar xzf "$PIPER_FILE"
  rm "$PIPER_FILE"
  chmod +x "$PIPER_DIR/piper/piper"
  echo -e "${GREEN}✓ Piper installed successfully${NC}"
fi

echo ""
echo -e "${BLUE}[5/6] Downloading voice models (this may take a while)...${NC}"

# Voice models with their URLs
declare -A VOICES=(
  ["pt_BR-jeff-medium.onnx"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/jeff/medium/pt_BR-jeff-medium.onnx"
  ["pt_BR-jeff-medium.onnx.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/jeff/medium/pt_BR-jeff-medium.onnx.json"
  ["pt_BR-cadu-medium.onnx"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/cadu/medium/pt_BR-cadu-medium.onnx"
  ["pt_BR-cadu-medium.onnx.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/cadu/medium/pt_BR-cadu-medium.onnx.json"
  ["pt_BR-faber-medium.onnx"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx"
  ["pt_BR-faber-medium.onnx.json"]="https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json"
  ["pt_BR-miro-high.onnx"]="https://huggingface.co/TarcisoAmorim/piper-pt_BR-miro-high/resolve/main/model.onnx"
  ["pt_BR-miro-high.onnx.json"]="https://huggingface.co/TarcisoAmorim/piper-pt_BR-miro-high/resolve/main/config.json"
)

cd "$VOICES_DIR"
for voice_file in "${!VOICES[@]}"; do
  if [ ! -f "$voice_file" ]; then
    echo "  Downloading $voice_file..."
    wget -q "${VOICES[$voice_file]}" -O "$voice_file" || echo -e "${YELLOW}⚠ Failed to download $voice_file${NC}"
  fi
done

echo -e "${GREEN}✓ Voice models ready${NC}"

echo ""
echo -e "${BLUE}[6/6] Finalizing setup...${NC}"

# Make scripts executable
chmod +x "$SKILL_DIR/scripts/"*.py 2>/dev/null || true
chmod +x "$SKILL_DIR/scripts/"*.sh 2>/dev/null || true

# Create config directory if needed
mkdir -p "$(dirname $WORKSPACE/.audio_pt_voice_config)"

echo -e "${GREEN}✓ Setup complete!${NC}"

echo ""
echo "=============================================="
echo -e "${GREEN}✅ Installation successful!${NC}"
echo "=============================================="
echo ""
echo "📝 Next steps:"
echo "  1. Restart OpenClaw: openclaw gateway restart"
echo "  2. Try voice commands:"
echo "     /voz list        - Show available voices"
echo "     /voz jeff        - Use Jeff voice"
echo "     /voz miro        - Use Miro (feminine)"
echo ""
echo "💡 Tips:"
echo "  • Send audio message → Receive voice reply"
echo "  • Say 'texto' for text mode"
echo "  • Use /voz command to change voices"
echo ""
echo "📊 Installation Summary:"
echo "  Piper: $PIPER_DIR"
echo "  Voices: $VOICES_DIR"
echo "  Config: $WORKSPACE/.audio_pt_voice_config"
echo ""
