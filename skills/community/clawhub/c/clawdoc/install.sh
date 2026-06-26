#!/usr/bin/env bash
set -euo pipefail

# install.sh
# Installs clawdoc to ~/.openclaw/skills/clawdoc
# Run from the clawdoc repo root.

INSTALL_DIR="${OPENCLAW_SKILLS_DIR:-$HOME/.openclaw/skills}/clawdoc"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🩻 clawdoc installer"
echo ""

# Check deps first
if ! bash "$SCRIPT_DIR/scripts/check-deps.sh"; then
  echo ""
  echo "Please install missing dependencies and retry."
  exit 1
fi

echo ""
echo "Installing to: $INSTALL_DIR"

if [ -d "$INSTALL_DIR" ]; then
  echo "Existing installation found. Updating..."
  # Backup existing, then overwrite
  cp -r "$INSTALL_DIR" "${INSTALL_DIR}.bak.$(date +%Y%m%d%H%M%S)" 2>/dev/null || true
fi

mkdir -p "$INSTALL_DIR"

# Copy all project files
cp -r "$SCRIPT_DIR/scripts"   "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/templates" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/tests"     "$INSTALL_DIR/"
cp    "$SCRIPT_DIR/SKILL.md"  "$INSTALL_DIR/"
cp    "$SCRIPT_DIR/README.md" "$INSTALL_DIR/"
cp    "$SCRIPT_DIR/LICENSE"   "$INSTALL_DIR/"
cp    "$SCRIPT_DIR/VERSION"   "$INSTALL_DIR/"
cp    "$SCRIPT_DIR/Makefile"  "$INSTALL_DIR/" 2>/dev/null || true
cp    "$SCRIPT_DIR/CHANGELOG.md" "$INSTALL_DIR/" 2>/dev/null || true

# Ensure scripts are executable
chmod +x "$INSTALL_DIR"/scripts/*.sh
chmod +x "$INSTALL_DIR"/tests/test-detection.sh

echo ""
echo "✓ Installed clawdoc $(cat "$SCRIPT_DIR/VERSION") to $INSTALL_DIR"
echo ""
echo "Run a health check:"
echo "  bash $INSTALL_DIR/scripts/headline.sh ~/.openclaw/agents/main/sessions/"
echo ""
echo "Or from any OpenClaw channel: /clawdoc"
