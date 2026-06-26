#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <target-skills-dir>"
  echo "Example: $0 ~/.openclaw/skills"
  exit 1
fi

TARGET_DIR="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_NAME="claw-go"

mkdir -p "$TARGET_DIR"
rm -rf "$TARGET_DIR/$SKILL_NAME"
cp -R "$SKILL_DIR" "$TARGET_DIR/$SKILL_NAME"

echo "Installed $SKILL_NAME to: $TARGET_DIR/$SKILL_NAME"
