#!/usr/bin/env bash
# rollback.sh — Rollback a failed release.
#
# Usage:
#   ./scripts/release/rollback.sh <version>
#
# Steps:
#   1. Unpublish from npm (if within 72h window)
#   2. Delete git tag (local + remote)
#   3. Revert the release commit
#   4. Force push

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$ROOT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

ok() { echo -e "  ${GREEN}✓${NC} $1"; }
warn() { echo -e "  ${YELLOW}⚠${NC} $1"; }
die() { echo -e "  ${RED}✗${NC} $1"; exit 1; }

VERSION="${1:-}"
if [ -z "$VERSION" ]; then
  # Auto-detect from last tag
  VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
  VERSION="${VERSION#v}"  # strip leading v
fi

if [ -z "$VERSION" ]; then
  echo "Usage: rollback.sh <version>"
  echo "  version: The version to rollback (e.g., 0.2.0)"
  exit 1
fi

echo "═══════════════════════════════════════════"
echo -e "  ${BOLD}⏪ Rolling back v${VERSION}${NC}"
echo "═══════════════════════════════════════════"
echo ""

# Confirm
read -p "Are you sure you want to rollback v${VERSION}? [y/N] " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Aborted."
  exit 0
fi

# 1. npm unpublish
echo ""
echo "▶ Unpublishing from npm..."
PKG_NAME=$(node -e "console.log(require('./package.json').name)" 2>/dev/null || echo "")
if [ -n "$PKG_NAME" ]; then
  npm unpublish "${PKG_NAME}@${VERSION}" 2>&1 \
    && ok "Unpublished ${PKG_NAME}@${VERSION} from npm" \
    || warn "npm unpublish failed (may be outside 72h window or not published)"
else
  warn "Could not determine package name"
fi

# 2. Delete git tag
echo ""
echo "▶ Deleting git tag v${VERSION}..."
git tag -d "v${VERSION}" 2>&1 && ok "Deleted local tag" || warn "Local tag not found"
git push origin ":refs/tags/v${VERSION}" 2>&1 && ok "Deleted remote tag" || warn "Remote tag not found"

# 3. Revert the release commit
echo ""
echo "▶ Reverting release commit..."
RELEASE_COMMIT=$(git log --oneline --all --grep="chore(release): v${VERSION}" --format="%H" | head -1)
if [ -n "$RELEASE_COMMIT" ]; then
  git revert "$RELEASE_COMMIT" --no-edit 2>&1 && ok "Reverted release commit" || warn "Revert failed (conflicts?)"
else
  warn "Release commit not found — you may need to revert manually"
fi

# 4. Push
echo ""
echo "▶ Pushing rollback..."
BRANCH=$(git branch --show-current)
git push origin "$BRANCH" 2>&1 && ok "Pushed rollback" || warn "Push failed"

echo ""
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ Rollback of v${VERSION} complete${NC}"
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
echo ""
echo "Note: Docker images are NOT automatically removed."
echo "Run manually if needed:"
echo "  docker rmi ${PKG_NAME}:v${VERSION} ${PKG_NAME}:latest"
