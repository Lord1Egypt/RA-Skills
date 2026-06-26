#!/usr/bin/env bash
set -euo pipefail

# Bootstrap script for installing darkhunt-observability as an OpenClaw plugin.
#
# What it does:
#   1. Installs npm dependencies (if not already present)
#   2. Adds plugins.load.paths and a minimal plugin entry to ~/.openclaw/openclaw.json
#      so OpenClaw loads it as a plugin (not just a skill)
#   3. Prints next steps
#
# Usage:
#   cd ~/.openclaw/workspace/skills/darkhunt-observability
#   bash setup-plugin.sh
#
# After running this script, restart the gateway and run the setup wizard:
#   openclaw gateway restart
#   openclaw tracehub setup

PLUGIN_ID="darkhunt-observability"
CONFIG_FILE="${HOME}/.openclaw/openclaw.json"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

bold() { printf '\033[1m%s\033[0m' "$1"; }
green() { printf '\033[32m%s\033[0m' "$1"; }
red() { printf '\033[31m%s\033[0m' "$1"; }
dim() { printf '\033[2m%s\033[0m' "$1"; }

echo ""
echo "$(bold 'Darkhunt Observability — Plugin Setup')"
echo ""

# ── 1. Install dependencies ──────────────────────────────────────
if [ ! -d "$SCRIPT_DIR/node_modules" ]; then
  echo "==> Installing dependencies..."
  (cd "$SCRIPT_DIR" && npm install --omit=dev --silent 2>&1)
  echo "    $(green 'Done')"
else
  echo "==> Dependencies already installed"
fi

# ── 2. Patch openclaw.json ───────────────────────────────────────
if [ ! -f "$CONFIG_FILE" ]; then
  echo "$(red "Error: $CONFIG_FILE not found")"
  echo "Make sure OpenClaw is installed and has been run at least once."
  exit 1
fi

echo "==> Updating $CONFIG_FILE..."

# Use node to safely merge JSON (no jq dependency)
node -e "
const fs = require('fs');
const path = require('path');

const configPath = '${CONFIG_FILE}';
const skillsDir = '${SKILLS_DIR}';
const pluginId = '${PLUGIN_ID}';

const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

// Backup
fs.copyFileSync(configPath, configPath + '.bak');

// Ensure plugins.load.paths includes the skills directory
if (!config.plugins) config.plugins = {};
if (!config.plugins.load) config.plugins.load = {};
if (!config.plugins.load.paths) config.plugins.load.paths = [];

if (!config.plugins.load.paths.includes(skillsDir)) {
  config.plugins.load.paths.push(skillsDir);
  console.log('    Added ' + skillsDir + ' to plugins.load.paths');
} else {
  console.log('    plugins.load.paths already includes ' + skillsDir);
}

// Ensure plugin entry exists with enabled: true
if (!config.plugins.entries) config.plugins.entries = {};
if (!config.plugins.entries[pluginId]) {
  config.plugins.entries[pluginId] = { enabled: true, config: {} };
  console.log('    Created plugin entry: ' + pluginId);
} else if (!config.plugins.entries[pluginId].enabled) {
  config.plugins.entries[pluginId].enabled = true;
  console.log('    Enabled plugin entry: ' + pluginId);
} else {
  console.log('    Plugin entry already exists and is enabled');
}

fs.writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n', 'utf-8');
console.log('    Saved (backup at ' + configPath + '.bak)');
"

# ── 3. Next steps ────────────────────────────────────────────────
echo ""
echo "$(green '  Setup complete!')"
echo ""
echo "  Next steps:"
echo ""
echo "    $(bold '1.') Restart the gateway:"
echo "       $(dim 'openclaw gateway restart')"
echo ""
echo "    $(bold '2.') Run the setup wizard to configure endpoints and auth:"
echo "       $(dim 'openclaw tracehub setup')"
echo ""
echo "    Or configure manually with:"
echo "       $(dim 'openclaw tracehub set traces_endpoint https://api.darkhunt.ai/trace-hub/otlp/t/YOUR_TENANT/v1/traces')"
echo "       $(dim 'openclaw tracehub set authorization \"Bearer dh-YOUR-TOKEN\"')"
echo "       $(dim 'openclaw tracehub set workspace_id YOUR_WORKSPACE_ID')"
echo "       $(dim 'openclaw tracehub set application_id YOUR_APP_ID')"
echo "       $(dim 'openclaw tracehub set payload_mode full')"
echo ""
