#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
SLUG="${SLUG:-forge-skill}"
NAME="${NAME:-Forge AI Skill}"
VERSION="${VERSION:-1.0.0}"

if ! command -v clawhub &>/dev/null; then
  echo "Installing clawhub CLI..."
  npm install -g clawhub
fi

if ! clawhub whoami &>/dev/null 2>&1; then
  echo "Please log in to ClawHub:"
  clawhub login
fi

echo "Publishing $NAME ($SLUG) v$VERSION to ClawHub..."
clawhub skill publish "$SKILL_DIR" \
  --slug "$SLUG" \
  --name "$NAME" \
  --version "$VERSION" \
  "$@"
