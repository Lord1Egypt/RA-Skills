#!/bin/bash
# Daily Intelligence Briefing - Publish Script
# Run this after configuring your ClawHub account

set -e

echo "🚀 Publishing Daily Intelligence Briefing to ClawHub..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if logged in
if ! clawhub whoami &>/dev/null; then
    echo "❌ Not logged in!"
    echo ""
    echo "Please login first:"
    echo "  clawhub login --token YOUR_TOKEN"
    echo ""
    echo "Or use the browser flow:"
    echo "  clawhub login"
    echo ""
    exit 1
fi

# Verify package contents
echo "📦 Verifying package..."
PACKAGE_DIR="/home/admin/.openclaw/workspace/skills/daily-briefing"

REQUIRED_FILES=(
    "SKILL.md"
    "README.md"
    "package.json"
    "scripts/briefing.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$PACKAGE_DIR/$file" ]; then
        echo "❌ Missing required file: $file"
        exit 1
    fi
done

echo "✅ All files present"
echo ""

# Get version from package.json
VERSION=$(jq -r '.version' "$PACKAGE_DIR/package.json")
echo "📝 Version: $VERSION"

# Get name
NAME=$(jq -r '.description | split(":")[0]' "$PACKAGE_DIR/package.json")
echo "📝 Package Name: $NAME"
echo ""

# Publish!
echo "🔴 Starting publish..."
echo ""

cd "$PACKAGE_DIR"

clawhub publish . \
  --slug "daily-intelligence-briefing" \
  --name "Daily Intelligence Briefing" \
  --version "$VERSION" \
  --changelog "Initial release: AI/Tech news briefing with SearXNG integration" \
  --workdir . \
  --no-input 2>&1 || {
    echo ""
    echo "⚠️  Publish failed. Common issues:"
    echo "  - API rate limit exceeded"
    echo "  - Invalid package format"
    echo "  - Network connectivity issues"
    echo ""
    echo "Try again later or check the error message above."
    exit 1
}

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 SUCCESS! Published to ClawHub!"
echo ""
echo "Package URL: https://clawhub.com/search?q=daily-intelligence-briefing"
echo ""
echo "Next steps:"
echo "  1. Share the link in your community"
echo "  2. Add a GitHub repository for issues"
echo "  3. Monitor downloads and feedback"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
