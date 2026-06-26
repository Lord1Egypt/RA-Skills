#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="amath-socthink"
SOURCE_DIR="$SCRIPT_DIR/openclaw_skills/$SKILL_NAME"
DEFAULT_TARGET_DIR="${HOME}/.openclaw/skills"
TARGET_ROOT="${1:-$DEFAULT_TARGET_DIR}"
TARGET_DIR="$TARGET_ROOT/$SKILL_NAME"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Source skill directory not found: $SOURCE_DIR" >&2
  exit 1
fi

mkdir -p "$TARGET_ROOT"
rm -rf "$TARGET_DIR"
cp -R "$SOURCE_DIR" "$TARGET_DIR"

cat <<EOF
Installed OpenClaw skill:
- Source: $SOURCE_DIR
- Target: $TARGET_DIR

Next steps:
1. Ensure OpenClaw gateway is running.
2. Ensure this repository remains available at:
   $SCRIPT_DIR
3. Open OpenClaw and start a new session.
4. Ask it to use the '$SKILL_NAME' skill.

Reference docs:
- $SCRIPT_DIR/OPENCLAW_SETUP.md
EOF
