#!/bin/bash
# uninstall.sh — Uninstall correlation-memory plugin from OpenClaw
# Usage: ./uninstall.sh [--force]

set -euo pipefail

PLUGIN_ID="correlation-memory"
OPENCLAW_CONFIG="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
BACKUP_DIR="${OPENCLAW_CONFIG}.bak-$(date +%Y%m%d-%H%M%S)"
FORCE="${1:-}"

echo "=== correlation-memory Plugin Uninstaller ==="
echo "Plugin ID: $PLUGIN_ID"
echo "Config: $OPENCLAW_CONFIG"
echo ""

# Check if config exists
if [[ ! -f "$OPENCLAW_CONFIG" ]]; then
  echo "❌ Error: OpenClaw config not found at $OPENCLAW_CONFIG"
  echo "Is OpenClaw installed?"
  exit 1
fi

# Check if plugin is installed
if ! jq -e ".plugins.entries[\"$PLUGIN_ID\"]" "$OPENCLAW_CONFIG" > /dev/null 2>&1; then
  echo "⚠️  Plugin '$PLUGIN_ID' not found in config"
  echo "It may not be installed, or installed under a different ID"
  echo ""
  echo "Installed plugins:"
  jq -r '.plugins.entries | keys[]' "$OPENCLAW_CONFIG" 2>/dev/null || echo "(none or plugins.entries not found)"
  echo ""
  read -p "Continue anyway? [y/N] " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
  fi
fi

# Backup config before modification
echo "📦 Backing up config to $BACKUP_DIR"
cp "$OPENCLAW_CONFIG" "$BACKUP_DIR"
echo "✓ Backup created"
echo ""

# Confirm uninstall
if [[ "$FORCE" != "--force" ]]; then
  echo "This will remove the $PLUGIN_ID plugin from your OpenClaw config."
  echo "Backup: $BACKUP_DIR"
  read -p "Confirm uninstall? [y/N] " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
  fi
else
  echo "⚠️  --force flag set — skipping confirmation"
fi

# Remove plugin entry
echo "🗑️  Removing plugin from openclaw.json..."
if jq --arg id "$PLUGIN_ID" 'del(.plugins.entries[$id])' "$OPENCLAW_CONFIG" > "${OPENCLAW_CONFIG}.tmp"; then
  mv "${OPENCLAW_CONFIG}.tmp" "$OPENCLAW_CONFIG"
  echo "✓ Plugin removed from config"
else
  echo "❌ Error: Failed to remove plugin from config"
  echo "Backup restored from $BACKUP_DIR"
  cp "$BACKUP_DIR" "$OPENCLAW_CONFIG"
  exit 1
fi

# Verify removal
if jq -e ".plugins.entries[\"$PLUGIN_ID\"]" "$OPENCLAW_CONFIG" > /dev/null 2>&1; then
  echo "❌ Error: Plugin still exists in config after removal"
  echo "Backup restored from $BACKUP_DIR"
  cp "$BACKUP_DIR" "$OPENCLAW_CONFIG"
  exit 1
fi

echo "✓ Verification passed — plugin not in config"
echo ""

# Clean up temporary files
rm -f "${OPENCLAW_CONFIG}.tmp"

echo "=== Uninstall Complete ==="
echo ""
echo "Plugin '$PLUGIN_ID' has been uninstalled."
echo ""
echo "Backup location:"
echo "  - Config backup: $BACKUP_DIR"
echo ""
echo "Next steps:"
echo "  1. Restart OpenClaw gateway (if running):"
echo "     openclaw gateway restart"
echo "  2. Verify plugin is gone:"
echo "     openclaw plugins list"
