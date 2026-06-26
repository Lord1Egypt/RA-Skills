#!/usr/bin/env bash
set -euo pipefail

# Usage: ./tmp/publish.sh "<changelog message>"
# Example: ./tmp/publish.sh "Initial clawhub release"

CHANGELOG="${1:-}"
if [[ -z "$CHANGELOG" ]]; then
  echo "Usage: $0 \"<changelog message>\""
  exit 1
fi

# Read version and slug from _meta.json using Python
VERSION=$(python3 -c "import json; print(json.load(open('_meta.json'))['version'])")
SLUG=$(python3 -c "import json; print(json.load(open('_meta.json'))['slug'])")
NAME="FRITZ!Box"
TAG="v${VERSION}"

echo "Publishing ${SLUG}@${VERSION} (tag: ${TAG})"

# Ensure working tree is clean
if [[ -n "$(git status --porcelain)" ]]; then
  echo "❌ Working tree is dirty. Commit or stash changes before publishing."
  exit 1
fi

# Tag and push
if git tag "$TAG" 2>/dev/null; then
  echo "✅ Created tag ${TAG}"
else
  echo "⚠️  Tag ${TAG} already exists, skipping"
fi

git push
git push --tags

# Publish to clawhub
npx clawhub@latest publish . \
  --slug "$SLUG" \
  --name "$NAME" \
  --version "$VERSION" \
  --changelog "$CHANGELOG"
