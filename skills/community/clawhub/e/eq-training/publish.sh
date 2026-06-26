#!/bin/bash
# publish.sh — One-command publish to both GitHub and ClawHub
# Usage: ./publish.sh "1.0.1" "changelog message"

set -e

VERSION="${1:?Usage: ./publish.sh <version> [changelog]}"
CHANGELOG="${2:-Update to v$VERSION}"
DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$DIR"

# 1. Git commit & push
echo "📦 Committing and pushing to GitHub..."
git add -A
git commit -m "release: v$VERSION — $CHANGELOG" || echo "Nothing to commit"
git push

# 2. Publish to ClawHub
echo "🚀 Publishing to ClawHub..."
npx clawhub publish "$DIR" --slug replyher --version "$VERSION" --changelog "$CHANGELOG"

echo ""
echo "✅ Done! Published v$VERSION to GitHub + ClawHub"
echo "   GitHub:  https://github.com/replyher/replyher-skill"
echo "   ClawHub: https://clawhub.ai/skills/replyher"
