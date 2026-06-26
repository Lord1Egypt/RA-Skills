#!/bin/bash
# Gbrow — One-command setup for OpenClaw
# Usage: curl -fsSL https://raw.githubusercontent.com/ashish797/Gbrow/main/setup.sh | bash

set -e

echo "🌐 Gbrow — Setting up your AI browser..."

# Check/install Bun
if ! command -v bun &> /dev/null; then
    echo "📦 Installing Bun..."
    # Install unzip if missing
    if ! command -v unzip &> /dev/null; then
        if command -v brew &> /dev/null; then
            brew install unzip -q
        elif command -v apt-get &> /dev/null; then
            sudo apt-get install -y unzip -qq
        elif command -v yum &> /dev/null; then
            sudo yum install -y unzip -q
        else
            echo "❌ Please install unzip first, then re-run."
            exit 1
        fi
    fi
    curl -fsSL https://bun.sh/install | bash
    export BUN_INSTALL="$HOME/.bun"
    export PATH="$BUN_INSTALL/bin:$PATH"
else
    echo "✅ Bun $(bun --version) found"
fi

# Ensure Bun is in PATH
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

# Install dependencies
echo "📦 Installing dependencies..."
bun install --frozen-lockfile 2>/dev/null || bun install

# Install Playwright Chromium
echo "🌐 Installing Chromium..."
npx playwright install chromium 2>/dev/null || true

# Create state directory
mkdir -p .gstack

echo ""
echo "✅ Gbrow installed successfully!"
echo ""
echo "Start the server:"
echo "  bun run src/server.ts"
echo ""
echo "Or use from OpenClaw:"
echo "  Read SKILL.md for usage instructions"
echo ""
echo "🌐 Happy browsing!"
