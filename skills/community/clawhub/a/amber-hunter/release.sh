#!/bin/bash
# release.sh — Publish to GitHub Release + ClawHub
# Usage: bash release.sh [version] [github_token]
# Example: bash release.sh v0.9.1 ghp_xxx...

set -e

# 确保脚本自身目录为工作目录（无论从哪里执行）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VERSION=${1:?Usage: bash release.sh v0.9.1 [github_token]}
TOKEN=${2:-${GITHUB_TOKEN:?Requires GITHUB_TOKEN env or second argument}}
REPO="ankechenlab-node/amber_hunter"
TAG="v${VERSION#v}"

echo "🌙 Releasing $TAG for $REPO"

# Extract changelog section for this version
SECTION=$(awk "/## \[$TAG\]/,/^## /" CHANGELOG.md 2>/dev/null | sed '1d;$d' | head -30)
if [ -z "$SECTION" ]; then
  echo "⚠️  No CHANGELOG entry found for $TAG, using generic body"
  BODY="Release $TAG of amber-hunter."
else
  BODY="$SECTION"
fi

# ── 1. GitHub Release ─────────────────────────────────────
if ! git rev-parse "$TAG" >/dev/null 2>&1; then
  git tag -a "$TAG" -m "Release $TAG"
  git push origin "$TAG"
  echo "  → Tag $TAG created and pushed"
else
  echo "  → Tag $TAG already exists"
fi

# Check if release already exists
EXISTING=$(curl -s -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/$REPO/releases/tags/$TAG" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('id',''))" 2>/dev/null)

if [ -n "$EXISTING" ]; then
  # Update existing release
  RESPONSE=$(curl -s -X PATCH \
    "https://api.github.com/repos/$REPO/releases/$EXISTING" \
    -H "Authorization: token $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg body "$BODY" '{body: $body}')")
  echo "  → GitHub Release updated: $(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin).get('html_url','?'))")"
else
  # Create new release
  RESPONSE=$(curl -s -X POST \
    "https://api.github.com/repos/$REPO/releases" \
    -H "Authorization: token $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$(jq -n \
      --arg tag "$TAG" \
      --arg name "amber-hunter $TAG" \
      --arg body "$BODY" \
      '{tag_name: $tag, name: $name, body: $body, draft: false}')")
  echo "  → GitHub Release created: $(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin).get('html_url','?'))")"
fi

# ── 2. ClawHub ────────────────────────────────────────────
echo ""
echo "🔶 Publishing to ClawHub..."
CLEAN_VERSION="${VERSION#v}"
CHANGELOG_LINE=$(echo "$SECTION" | head -5 | tr '\n' ' ' | sed 's/  */ /g')

if npx clawhub whoami >/dev/null 2>&1; then
  npx clawhub publish . \
    --slug amber-hunter \
    --version "$CLEAN_VERSION" \
    --changelog "${CHANGELOG_LINE:-Release $CLEAN_VERSION}"
  echo "  → ClawHub: amber-hunter@$CLEAN_VERSION published ✅"
else
  echo "  ⚠️  Not logged in to ClawHub. Run: npx clawhub login"
  echo "     Then re-run this script."
fi

echo ""
echo "✅ Done: amber-hunter $TAG released on GitHub + ClawHub"
