#!/bin/bash
# ClawBox CLI setup script
# Installs the clawbox CLI tool and initializes with a token

set -e

# Check if clawbox is already installed
if command -v clawbox &> /dev/null; then
    echo "clawbox CLI is already installed."
    clawbox status 2>/dev/null || true
    exit 0
fi

# Find the repo root (look for pyproject.toml)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

if [ ! -f "$REPO_ROOT/pyproject.toml" ]; then
    echo "Error: Cannot find pyproject.toml. Run this from the clawbox repo."
    exit 1
fi

echo "Installing clawbox CLI..."
pip install "$REPO_ROOT"

echo ""
echo "Initializing clawbox..."
clawbox init

echo ""
echo "Setup complete! Try: clawbox status"
