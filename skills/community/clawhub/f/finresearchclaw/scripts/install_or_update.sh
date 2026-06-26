#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${1:-$HOME/.openclaw/workspace/AutoResearchClaw}"
REPO_URL="https://github.com/ChipmunkRPA/FinResearchClaw.git"

mkdir -p "$(dirname "$REPO_DIR")"

if [ -d "$REPO_DIR/.git" ]; then
  echo "Updating existing repo metadata at $REPO_DIR"
  git -C "$REPO_DIR" remote get-url origin >/dev/null 2>&1 || true
  git -C "$REPO_DIR" fetch --all --prune
  CURRENT_BRANCH="$(git -C "$REPO_DIR" branch --show-current || true)"
  echo "Current branch: ${CURRENT_BRANCH:-unknown}"
  echo "Fetched latest refs. Review/merge manually if you do not want automatic fast-forwards."
else
  echo "Cloning FinResearchClaw into $REPO_DIR"
  git clone "$REPO_URL" "$REPO_DIR"
fi

echo "Repo ready: $REPO_DIR"
