#!/bin/sh
# DEPRECATED: This script has been superseded by server/installer.py (see issue #94).
# It is kept as a reference only. SKILL.md now calls:
#   python3 -m server.installer uninstall
# Do NOT add new logic here.
#
# uninstall.sh — Friday Budgeting Pro uninstaller
# Called by ClawHub as the uninstall hook (SKILL.md metadata.openclaw.uninstall).
# Data in ~/.friday-bp/ is intentionally preserved.
set -e

LABEL="ai.openclaw.friday-budgeting-pro"
PLIST_DEST="$HOME/Library/LaunchAgents/${LABEL}.plist"

# 1. Unload the daemon from launchd (ignore errors if not loaded).
launchctl bootout "gui/$(id -u)/${LABEL}" || true

# 2. Remove the plist file.
rm -f "$PLIST_DEST"

# 3. Done. Data directory is intentionally preserved.
echo "✓ Friday Budgeting Pro daemon removed. Your data in ~/.friday-bp/ is preserved (delete manually to wipe)."
