#!/bin/bash
# LanceDB Memory System - Enable Script

set -e

echo "🧠 LanceDB Memory System Setup"
echo "=============================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python version: $(python3 --version)"

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# Check API Key
if [ -z "$ZHIPU_API_KEY" ]; then
    echo ""
    echo "⚠️  ZHIPU_API_KEY not set"
    echo ""
    echo "Please get your API key from: https://open.bigmodel.cn/"
    echo "Then add to ~/.bashrc:"
    echo ""
    echo "  export ZHIPU_API_KEY='your-key-here'"
    echo ""
    echo "Or set it now:"
    read -p "Enter ZHIPU_API_KEY: " api_key
    if [ -n "$api_key" ]; then
        export ZHIPU_API_KEY="$api_key"
        echo "export ZHIPU_API_KEY='$api_key'" >> ~/.bashrc
    fi
fi

# Test memory system
echo ""
echo "🧪 Testing memory system..."
if python3 skill.py stats > /dev/null 2>&1; then
    echo "✅ Memory System is ready!"
else
    echo "❌ Memory system test failed"
    exit 1
fi

echo ""
echo "=============================="
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "  1. Set ZHIPU_API_KEY (if not set)"
echo "  2. Run: python3 skill.py profile"
echo "  3. Add memory: python3 skill.py add --content '...' --type preference"
echo ""
