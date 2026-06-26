#!/bin/bash
# Email Bridge Installation Script
# Usage: ./install.sh

set -e

echo "📧 Email Bridge Installer"
echo "========================"

# Check Python version
PYTHON_VERSION=$(python3 --version 2>/dev/null | awk '{print $2}' | cut -d. -f1,2)
if [ -z "$PYTHON_VERSION" ]; then
    echo "❌ Python 3 not found. Please install Python 3.10+ first."
    exit 1
fi

echo "✓ Python $PYTHON_VERSION detected"

# Check if uv is available (preferred)
if command -v uv &> /dev/null; then
    echo "✓ Using uv for installation"
    uv sync
    source .venv/bin/activate
elif command -v pip &> /dev/null; then
    echo "✓ Using pip for installation"
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e .
else
    echo "❌ Neither uv nor pip found. Please install one of them."
    exit 1
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "Quick Start:"
echo "-----------"
echo ""
echo "1. Add your email account:"
echo "   # QQ Mail (with authorization code)"
echo "   email-bridge accounts add your@qq.com -p qq --config '{\"password\": \"YOUR_AUTH_CODE\"}'"
echo ""
echo "2. Sync emails:"
echo "   email-bridge sync"
echo ""
echo "3. Start daemon for real-time notifications:"
echo "   email-bridge daemon start -d"
echo ""
echo "For Gmail setup, see README.md → Gmail 配置指南"
echo ""
echo "Documentation: https://github.com/ryanchan720/email-bridge"