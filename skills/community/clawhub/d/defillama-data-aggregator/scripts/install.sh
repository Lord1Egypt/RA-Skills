#!/bin/bash

# DefiLlama Data Aggregator Installation Script

set -e

echo "🚀 Installing DefiLlama Data Aggregator..."
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js >= 16.0.0"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Node.js version must be >= 16.0.0. Current version: $(node -v)"
    exit 1
fi

echo "✓ Node.js version: $(node -v)"
echo ""

# Navigate to skill directory
cd "$(dirname "$0")"

# Install dependencies
echo "📦 Installing dependencies..."
npm install --silent
echo "✓ Dependencies installed"
echo ""

# Create config file if it doesn't exist
if [ ! -f "config/keys.js" ]; then
    echo "🔑 Creating config file..."
    cp config/keys.example.js config/keys.js
    echo "✓ Config file created: config/keys.js"
    echo ""
else
    echo "✓ Config file already exists: config/keys.js"
    echo ""
fi

# Link CLI command
echo "🔗 Linking CLI command..."
npm link
echo "✓ CLI command linked: defillama-data"
echo ""

# Test installation
echo "🧪 Testing installation..."
if command -v defillama-data &> /dev/null; then
    echo "✓ Installation successful!"
    echo ""
    echo "📝 Usage:"
    echo "  defillama-data --help"
    echo "  defillama-data defillama tvl"
    echo "  defillama-data defillama protocols --limit 10 --format table"
    echo "  defillama-data defillama yields --min-apy 10 --limit 20"
    echo "  defillama-data health"
    echo ""
else
    echo "❌ Installation failed. CLI command not available."
    exit 1
fi
