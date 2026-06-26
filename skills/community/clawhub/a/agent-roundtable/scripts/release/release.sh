#!/usr/bin/env bash
# release.sh — Main release entry point.
#
# Usage:
#   ./scripts/release/release.sh [--dry-run] [--type=patch|minor|major]
#
# Steps:
#   1. Preflight checks (git clean, tests, lint, build)
#   2. Calculate version bump (conventional commits)
#   3. Generate changelog
#   4. Commit version bump + changelog
#   5. Create git tag & push
#   6. PyPI publish (agent-roundtable)
#   7. ClawHub + Hermes Skill Hub publish
#   8. GitHub Release

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$ROOT_DIR"

# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------

DRY_RUN=false
BUMP_TYPE=""

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --type=*) BUMP_TYPE="${arg#--type=}" ;;
  esac
done

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

step() { echo -e "\n${CYAN}[$1/8]${NC} ${BOLD}$2${NC}"; }
ok() { echo -e "  ${GREEN}✓${NC} $1"; }
warn() { echo -e "  ${YELLOW}⚠${NC} $1"; }
die() { echo -e "  ${RED}✗${NC} $1"; exit 1; }

echo "═══════════════════════════════════════════"
echo "  🚀 Roundtable Release"
if $DRY_RUN; then
  echo -e "  ${YELLOW}DRY RUN — no changes will be published${NC}"
fi
echo "═══════════════════════════════════════════"

# ---------------------------------------------------------------------------
# Step 1: Preflight
# ---------------------------------------------------------------------------

step 1 "Running preflight checks..."
bash "$SCRIPT_DIR/preflight-check.sh" || die "Preflight checks failed"

# ---------------------------------------------------------------------------
# Step 2: Calculate version
# ---------------------------------------------------------------------------

step 2 "Calculating version bump..."
BUMP_ARGS=""
if [ -n "$BUMP_TYPE" ]; then
  BUMP_ARGS="--type=$BUMP_TYPE"
fi

if $DRY_RUN; then
  node "$SCRIPT_DIR/bump-version.js" --dry-run $BUMP_ARGS
  NEW_VERSION=$(node "$SCRIPT_DIR/bump-version.js" $BUMP_ARGS 2>/dev/null | tail -1)
else
  NEW_VERSION=$(node "$SCRIPT_DIR/bump-version.js" $BUMP_ARGS)
  ok "Version bumped to v$NEW_VERSION (package.json updated)"
fi

# Sync version to pyproject.toml and SKILL.md
if [ -f "pyproject.toml" ]; then
  sed -i '' "s/^version = .*/version = \"$NEW_VERSION\"/" pyproject.toml
  ok "Synced version $NEW_VERSION to pyproject.toml"
fi
if [ -f "SKILL.md" ]; then
  sed -i '' "s/^version: .*/version: $NEW_VERSION/" SKILL.md
  ok "Synced version $NEW_VERSION to SKILL.md"
fi

# ---------------------------------------------------------------------------
# Step 3: Generate changelog
# ---------------------------------------------------------------------------

step 3 "Generating changelog..."
if $DRY_RUN; then
  node "$SCRIPT_DIR/changelog.js" --dry-run --version="$NEW_VERSION"
else
  node "$SCRIPT_DIR/changelog.js" --version="$NEW_VERSION"
  ok "CHANGELOG.md updated"
fi

# ---------------------------------------------------------------------------
# Step 4: Commit & tag
# ---------------------------------------------------------------------------

step 4 "Committing and tagging..."
if $DRY_RUN; then
  echo "  Would commit: package.json, CHANGELOG.md"
  echo "  Would create tag: v$NEW_VERSION"
else
  git add package.json pyproject.toml SKILL.md CHANGELOG.md
  git -c user.name="agent-mafei" -c user.email="mafei@izmw.me" \
    commit -m "chore(release): v$NEW_VERSION"
  git tag -a "v$NEW_VERSION" -m "Release v$NEW_VERSION"
  ok "Committed and tagged v$NEW_VERSION"
fi

# ---------------------------------------------------------------------------
# Step 5: Git push & tag
# ---------------------------------------------------------------------------

step 5 "Pushing to origin..."
if $DRY_RUN; then
  echo "  Would push branch to origin"
  echo "  Would push tags"
else
  BRANCH=$(git branch --show-current)
  git push origin "$BRANCH" 2>&1 && ok "Pushed branch" || warn "Branch push failed"
  git push origin --tags 2>&1 && ok "Pushed tags" || warn "Tag push failed"
fi

# ---------------------------------------------------------------------------
# Step 6: PyPI publish
# ---------------------------------------------------------------------------

step 6 "Publishing to PyPI..."
if $DRY_RUN; then
  echo "  Would build sdist + wheel"
  echo "  Would upload to PyPI as agent-roundtable v$NEW_VERSION"
elif [ -f "pyproject.toml" ]; then
  # Build dist
  python3 -m build --sdist --wheel 2>&1 && ok "Built sdist + wheel" || die "python3 -m build failed"

  # Upload
  TWINE_PATH=$(find "$HOME" -path "*/venv/bin/twine" 2>/dev/null | head -1)
  if [ -z "$TWINE_PATH" ]; then
    TWINE_PATH="twine"
  fi
  "$TWINE_PATH" upload dist/* 2>&1 && ok "Published to PyPI as agent-roundtable v$NEW_VERSION" || warn "PyPI upload failed (check .pypirc token)"
else
  warn "No pyproject.toml — skipping PyPI publish"
fi

# ---------------------------------------------------------------------------
# Step 7: ClawHub + Hermes Skill Hub
# ---------------------------------------------------------------------------

step 7 "Publishing to skill hubs..."

if $DRY_RUN; then
  echo "  Would publish to ClawHub as agent-roundtable v$NEW_VERSION"
  echo "  Would sync SKILL.md to $HERMES_SKILL_REPO"
else

# ClawHub
if command -v clawhub &>/dev/null; then
  echo "  Publishing to ClawHub..."
  clawhub publish . --slug agent-roundtable --version "$NEW_VERSION" 2>&1 \
    && ok "Published to ClawHub as agent-roundtable v$NEW_VERSION" \
    || warn "ClawHub publish failed (run 'clawhub whoami' to check auth)"
else
  warn "clawhub CLI not found — skipping ClawHub"
fi

# Hermes Skill Hub (via GitHub pointer repo)
HERMES_SKILL_REPO="MoyuFamily/hermes-skill-agent-roundtable"
if command -v gh &>/dev/null; then
  echo "  Syncing to Hermes Skill Hub ($HERMES_SKILL_REPO)..."
  SKILL_TMPDIR=$(mktemp -d)
  gh repo clone "$HERMES_SKILL_REPO" "$SKILL_TMPDIR" 2>/dev/null || {
    # Create repo if not exists
    gh repo create "$HERMES_SKILL_REPO" --public --description "Hermes Skill Hub pointer: agent-roundtable" 2>&1 && ok "Created $HERMES_SKILL_REPO" || warn "Failed to create pointer repo"
    gh repo clone "$HERMES_SKILL_REPO" "$SKILL_TMPDIR" 2>&1 || { warn "Cannot clone pointer repo"; SKILL_TMPDIR=""; }
  }
  if [ -n "$SKILL_TMPDIR" ] && [ -d "$SKILL_TMPDIR" ]; then
    cp SKILL.md "$SKILL_TMPDIR/SKILL.md"
    cd "$SKILL_TMPDIR"
    git add SKILL.md
    git -c user.name="agent-xiaohe" -c user.email="xiaohe@izmw.me" \
      commit -m "chore: update SKILL.md to v$NEW_VERSION" 2>/dev/null || echo "  No changes to commit"
    git push origin main 2>&1 && ok "Synced SKILL.md to $HERMES_SKILL_REPO" || warn "Push to pointer repo failed"
    cd "$ROOT_DIR"
    rm -rf "$SKILL_TMPDIR"
  fi
else
  warn "gh CLI not found — skipping Hermes Skill Hub"
fi

fi  # end dry-run check for step 7

# ---------------------------------------------------------------------------
# Step 8: GitHub Release
# ---------------------------------------------------------------------------

step 8 "Creating GitHub Release..."
if $DRY_RUN; then
  echo "  Would create GitHub Release v$NEW_VERSION"
elif command -v gh &>/dev/null; then
  CHANGELOG_LATEST=$(awk "/^## \\[$NEW_VERSION/{found=1; next} /^## \\[/{if(found) exit} found{print}" CHANGELOG.md)
  if [ -n "$CHANGELOG_LATEST" ]; then
    echo "$CHANGELOG_LATEST" > /tmp/release-notes-$NEW_VERSION.md
    gh release create "v$NEW_VERSION" \
      --title "v$NEW_VERSION" \
      --notes-file "/tmp/release-notes-$NEW_VERSION.md" \
      2>&1 && ok "GitHub Release created" || warn "GitHub Release failed"
    rm -f "/tmp/release-notes-$NEW_VERSION.md"
  else
    gh release create "v$NEW_VERSION" \
      --title "v$NEW_VERSION" \
      --generate-notes \
      2>&1 && ok "GitHub Release created" || warn "GitHub Release failed"
  fi
else
  warn "gh CLI not found — skipping GitHub Release"
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
if $DRY_RUN; then
  echo -e "${GREEN}  Dry run complete. No changes published.${NC}"
else
  echo -e "${GREEN}  ✅ Release v$NEW_VERSION complete!${NC}"
fi
echo -e "${GREEN}═══════════════════════════════════════════${NC}"
