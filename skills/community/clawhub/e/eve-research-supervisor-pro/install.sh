#!/bin/bash
# EVE Research Supervisor Pro — Installer
# Installs to ~/.openclaw/workspace/research-supervisor-pro/

set -e

BASE=~/.openclaw/workspace/research-supervisor-pro
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   🔴 EVE Research Supervisor Pro v5.0    ║"
echo "║   Installing...                          ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Create directories
mkdir -p "$BASE"/{scripts,templates,memory,research,figures}

# Copy scripts and templates
cp -r scripts/* "$BASE/scripts/"
cp -r templates/* "$BASE/templates/"
chmod +x "$BASE/scripts/"*.py

# Python dependencies
echo "🔍 Checking Python dependencies..."
python3 -c "import requests"   2>/dev/null || pip3 install requests   -q
python3 -c "import pypdf"      2>/dev/null || pip3 install pypdf       -q
python3 -c "import matplotlib" 2>/dev/null || pip3 install matplotlib  -q
python3 -c "import numpy"      2>/dev/null || pip3 install numpy       -q
echo "✅ Python dependencies OK"

# Optional: Graphviz for citation graph visualization
if ! command -v dot &>/dev/null; then
  echo "ℹ️  Optional: install Graphviz to visualize citation graphs:"
  echo "   macOS:  brew install graphviz"
  echo "   Linux:  sudo apt install graphviz"
fi

echo ""
echo "✅ EVE installed to: $BASE"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " QUICK START"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Just say to your AI agent:"
echo "   \"EVE, start research mode\""
echo ""
echo " Or run manually:"
echo "   python3 $BASE/scripts/thesis_context.py init"
echo "   python3 $BASE/scripts/arxiv_downloader.py \"your topic\" 30"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
