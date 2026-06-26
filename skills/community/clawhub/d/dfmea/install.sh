#!/bin/bash

# DFMEA Skill Installer
set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.openclaw/skills"

echo "Installing DFMEA skill..."

# Create skills directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Copy all skill files
cp "$SKILL_DIR/SKILL.md" "$INSTALL_DIR/dfmea.SKILL.md"
cp "$SKILL_DIR/dfmea.js" "$INSTALL_DIR/dfmea.js"
cp "$SKILL_DIR/package.json" "$INSTALL_DIR/dfmea.package.json"
cp "$SKILL_DIR/README.md" "$INSTALL_DIR/dfmea.README.md"

# Create templates directory
mkdir -p "$INSTALL_DIR/templates"
cp "$SKILL_DIR/templates/smart_hardware_template.json" "$INSTALL_DIR/templates/smart_hardware_template.json"

# Create examples directory  
mkdir -p "$INSTALL_DIR/examples"
cp "$SKILL_DIR/examples/smart_home_hub_example.json" "$INSTALL_DIR/examples/smart_home_hub_example.json"

# Make the CLI executable
chmod +x "$INSTALL_DIR/dfmea.js"

# Create symlink for easy access
ln -sf "$INSTALL_DIR/dfmea.js" "$HOME/.npm-global/bin/dfmea" 2>/dev/null || true

echo "DFMEA skill installed successfully!"
echo "Usage: dfmea --help"
echo "Smart hardware templates available in $INSTALL_DIR/templates/"