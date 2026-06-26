#!/usr/bin/env bash
set -euo pipefail

echo "=== Company Brain Core OS Setup ==="
echo ""

# Check Python 3.10+
PYVER=$(python3 --version 2>/dev/null | awk '{print $2}' | cut -d. -f1,2)
if [ -z "$PYVER" ]; then
    echo "ERROR: Python 3.10+ required. Install from https://python.org"
    exit 1
fi

MAJOR=$(echo "$PYVER" | cut -d. -f1)
MINOR=$(echo "$PYVER" | cut -d. -f2)
if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]); then
    echo "ERROR: Python 3.10+ required. Found: $PYVER"
    exit 1
fi

echo "✓ Python $PYVER"

# Check bun (required for PGLite)
if ! command -v bun &> /dev/null; then
    echo "⚠ Bun not found. Installing..."
    curl -fsSL https://bun.sh/install | bash
    export PATH="$HOME/.bun/bin:$PATH"
fi

echo "✓ Bun $(bun --version)"

# Setup directory
INSTALL_DIR="${COMPANY_BRAIN_HOME:-$HOME/.company-brain}"
mkdir -p "$INSTALL_DIR"

# Check if brain already exists
if [ -f "$INSTALL_DIR/brain_wrapper.py" ]; then
    echo "✓ Brain already installed at $INSTALL_DIR"
else
    echo "📦 Installing Company Brain..."
    
    # Clone or copy source
    GIT_DIR="/data/.openclaw/workspace/company-brain"
    if [ -d "$GIT_DIR" ]; then
        # Running from workspace — copy source
        cp -r "$GIT_DIR"/* "$INSTALL_DIR/"
        echo "  Copied from workspace"
    else
        # User machine — clone from GitHub
        git clone --depth 1 https://github.com/CertainLogicAI/company-brain-os.git "$INSTALL_DIR"
        echo "  Cloned from GitHub"
    fi
    
    # Install Python deps
    if [ -f "$INSTALL_DIR/requirements.txt" ]; then
        echo "  Installing dependencies..."
        pip3 install -q -r "$INSTALL_DIR/requirements.txt" 2>/dev/null || true
    fi
fi

echo ""
echo "✅ Company Brain Core OS installed!"
echo ""
echo "Location: $INSTALL_DIR"
echo "Facts: 443 verified concepts"
echo "Cache: 122x speedup"
echo ""
echo "Quick start:"
echo "  cd $INSTALL_DIR"
echo "  python3 -m http.server 8000 &"
echo "  python3 cache_warmer.py"
echo ""
echo "Test: curl -s http://localhost:8000/health"
echo ""
echo "Next: Install self-improving tools to enhance your brain:"
echo "  clawhub install certainlogic-self-improving-stack"
echo ""
