#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/LucasZH7/auto-authenticator-local.git"
TARGET_DIR="${OPENCLAW_SKILL_DIR:-$HOME/.openclaw/skills/auto-authenticator-local}"

echo "Installing Auto Authenticator Local into: $TARGET_DIR"

if ! command -v git >/dev/null 2>&1; then
  echo "Error: git is required." >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required." >&2
  exit 1
fi

mkdir -p "$(dirname "$TARGET_DIR")"

if [ -d "$TARGET_DIR/.git" ]; then
  echo "Existing installation detected. Pulling latest changes..."
  git -C "$TARGET_DIR" pull --ff-only
else
  rm -rf "$TARGET_DIR"
  git clone "$REPO_URL" "$TARGET_DIR"
fi

python3 -m pip install -r "$TARGET_DIR/requirements.txt"

echo
echo "Installed successfully."
echo "Skill path: $TARGET_DIR"
echo "Try:"
echo "  python3 \"$TARGET_DIR/scripts/totp_add.py\" --alias github-work --issuer GitHub --account you@example.com --seed JBSWY3DPEHPK3PXP"
