#!/bin/bash
# claw-presenter dependency installer
set -e

echo "🎤 Installing claw-presenter dependencies..."

# 1. Python packages
echo "📦 Installing Python packages..."
pip3 install --quiet python-pptx Pillow pdf2image pdfplumber

# 2. System dependencies (poppler for PDF→image)
if command -v brew &>/dev/null; then
    echo "📦 Installing poppler via Homebrew (macOS)..."
    brew install poppler 2>/dev/null || echo "  poppler already installed"
elif command -v apt-get &>/dev/null; then
    echo "📦 Installing poppler via apt (Debian/Ubuntu)..."
    sudo apt-get install -y poppler-utils
elif command -v dnf &>/dev/null; then
    echo "📦 Installing poppler via dnf (Fedora/RHEL)..."
    sudo dnf install -y poppler-utils
elif command -v pacman &>/dev/null; then
    echo "📦 Installing poppler via pacman (Arch)..."
    sudo pacman -S --noconfirm poppler
else
    echo "⚠️  Please install poppler-utils manually for PDF→image conversion"
fi

# 3. LibreOffice (optional, for high-fidelity PPTX→image)
if command -v soffice &>/dev/null || command -v libreoffice &>/dev/null; then
    echo "✅ LibreOffice found"
else
    echo ""
    echo "💡 Optional: Install LibreOffice for high-fidelity PPTX→image conversion:"
    if command -v brew &>/dev/null; then
        echo "   brew install --cask libreoffice"
    elif command -v apt-get &>/dev/null; then
        echo "   sudo apt-get install -y libreoffice"
    else
        echo "   https://www.libreoffice.org/download/"
    fi
    echo "   Without LibreOffice, PPTX slides will use simple text rendering (lower quality)."
fi

echo ""
echo "✅ claw-presenter dependencies installed!"
echo "   Run: python3 scripts/parse-presentation.py <your-file.pptx>"
