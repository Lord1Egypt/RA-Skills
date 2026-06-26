#!/bin/bash
set -e

echo "--- Installing Diagram Rendering Skill (Local-First) ---"

# Detect OS
OS="$(uname)"
case "$OS" in
    Linux*)     PLATFORM=Linux;;
    Darwin*)    PLATFORM=Mac;;
    *)          PLATFORM="UNKNOWN"
esac

echo "Detected Platform: $PLATFORM"

# 1. Install System Dependencies (Graphviz)
if [[ "$PLATFORM" == "Linux" ]]; then
    if command -v apt-get &> /dev/null; then
        echo "Installing graphviz via apt..."
        sudo apt-get update && sudo apt-get install -y graphviz plantuml default-jre
    fi
elif [[ "$PLATFORM" == "Mac" ]]; then
    if command -v brew &> /dev/null; then
        echo "Installing graphviz via brew..."
        brew install graphviz
    fi
fi

# 2. Install D2 CLI
if ! command -v d2 &> /dev/null; then
    echo "Installing D2..."
    curl -fsSL https://d2lang.com/install.sh | sh
else
    echo "D2 already installed."
fi

# 3. Install Mermaid CLI (requires Node)
if command -v npm &> /dev/null; then
    if ! command -v mmdc &> /dev/null; then
        echo "Installing mermaid-cli..."
        sudo npm install -g @mermaid-js/mermaid-cli
    else
        echo "Mermaid CLI already installed."
    fi
else
    echo "Warning: Node/NPM not found. Mermaid rendering will fallback to Cloud API."
fi

# 4. Install Python Dependencies
echo "Setting up Python virtual environment..."
if [[ ! -d ".venv" ]]; then
    python3 -m venv .venv
    echo "Virtual environment created."
fi

# Use the local venv's pip
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

echo "--- Local-First Skill Environment Ready ---"
echo "Note: Always run rendering scripts using './.venv/bin/python3 scripts/local_render.py'"
