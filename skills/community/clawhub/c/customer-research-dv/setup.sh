#!/bin/bash
# Customer Research Skill Setup Script

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔍 Customer Research & Validation Skill Setup"
echo "=============================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    echo "   Install from: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"

# Check pip
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is required but not installed"
    exit 1
fi

echo "✅ Found pip"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r "$SKILL_DIR/requirements.txt" || {
    echo "❌ Failed to install dependencies"
    exit 1
}

echo "✅ Dependencies installed"
echo ""

# Download TextBlob corpora
echo "📚 Downloading TextBlob corpora (for sentiment analysis)..."
python3 -m textblob.download_corpora 2>/dev/null || {
    echo "⚠️  TextBlob corpora download may have failed"
    echo "   Try manually: python3 -m textblob.download_corpora"
}

echo "✅ TextBlob ready"
echo ""

# Create data directory
mkdir -p "$SKILL_DIR/data"
echo "✅ Created data directory"
echo ""

# Test installation
echo "🧪 Testing installation..."

# Test reddit-miner
if python3 "$SKILL_DIR/scripts/reddit-miner.py" --help &> /dev/null; then
    echo "✅ reddit-miner.py works"
else
    echo "❌ reddit-miner.py failed"
fi

# Test survey-gen
if python3 "$SKILL_DIR/scripts/survey-gen.py" --help &> /dev/null; then
    echo "✅ survey-gen.py works"
else
    echo "❌ survey-gen.py failed"
fi

# Test interview-script
if python3 "$SKILL_DIR/scripts/interview-script.py" --help &> /dev/null; then
    echo "✅ interview-script.py works"
else
    echo "❌ interview-script.py failed"
fi

# Test persona-validator
if python3 "$SKILL_DIR/scripts/persona-validator.py" --help &> /dev/null; then
    echo "✅ persona-validator.py works"
else
    echo "❌ persona-validator.py failed"
fi

# Test competitor-scraper
if python3 "$SKILL_DIR/scripts/competitor-scraper.py" --help &> /dev/null; then
    echo "✅ competitor-scraper.py works"
else
    echo "❌ competitor-scraper.py failed"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Quick start:"
echo "  1. Read SKILL.md for full documentation"
echo "  2. Check examples/ for sample outputs"
echo "  3. Run your first command:"
echo ""
echo "     ./customer-research.sh mine \\"
echo "       --category \"your product category\" \\"
echo "       --subreddits subreddit1,subreddit2 \\"
echo "       --output data/insights.json"
echo ""
echo "For help: ./customer-research.sh help"
echo ""
