#!/bin/bash
# emoTwin Installation Script v1.3.3
# Built-in emoPAD service - no external dependency

echo "🌊 Installing emoTwin v1.3.3..."

# Create config directory
mkdir -p ~/.emotwin/diary

# Copy default config if not exists
if [ ! -f ~/.emotwin/config.yaml ]; then
    cp config_defaults.yaml ~/.emotwin/config.yaml
    echo "✅ Created default config at ~/.emotwin/config.yaml"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -q -r requirements.txt

# Check for Chinese fonts (optional but recommended)
echo "🔤 Checking fonts..."
if fc-list :lang=zh | grep -q "Noto\|WQY"; then
    echo "✅ Chinese fonts found"
else
    echo "⚠️  Chinese fonts not found. For Chinese diary cards, install:"
    echo "   sudo apt install fonts-noto-cjk  # Debian/Ubuntu"
    echo "   sudo pacman -S noto-fonts-cjk    # Arch"
fi

# Check for image viewer
echo "🖼️  Checking image viewer..."
if command -v eog &> /dev/null; then
    echo "✅ eog (Eye of GNOME) found - will use for diary popups"
elif command -v xdg-open &> /dev/null; then
    echo "✅ xdg-open found - will use as fallback"
else
    echo "⚠️  No image viewer found. Install eog for best experience:"
    echo "   sudo apt install eog  # Debian/Ubuntu"
fi

echo ""
echo "✨ emoTwin v1.3.3 installed successfully!"
echo ""
echo "Features:"
echo "  ✅ Built-in emoPAD service (auto-starts)"
echo "  ✅ Multi-platform support (Moltcn/Moltbook)"
echo "  ✅ Auto language detection (Chinese/English)"
echo "  ✅ Visual diary cards with popup display"
echo ""
echo "Next steps:"
echo "1. (Optional) Set Moltcn token: export MOLTCN_TOKEN='your_token_here'"
echo "2. (Optional) Connect EEG/PPG/GSR sensors for real emotion detection"
echo "3. Start emoTwin: python3 scripts/emotwin.py start"
echo ""
echo "Or use OpenClaw commands:"
echo "  openclaw emotwin start    # Start with auto emoPAD"
echo "  openclaw emotwin status   # Check emotion status"
echo "  openclaw emotwin stop     # Stop and get diary"
echo ""
echo "Say '带着情绪去 moltcn' or 'go to moltcn' to start!"
