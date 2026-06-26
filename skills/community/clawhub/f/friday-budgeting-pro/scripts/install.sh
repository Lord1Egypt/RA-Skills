#!/bin/sh
# DEPRECATED: This script has been superseded by server/installer.py (see issue #94).
# It is kept as a reference only. SKILL.md now calls:
#   python3 -m server.installer install
# Do NOT add new logic here.
#
# install.sh — Friday Budgeting Pro installer
# Called by ClawHub as the post-install hook (SKILL.md metadata.openclaw.install).
# Safe to run multiple times — all steps are idempotent.
set -e

LABEL="ai.openclaw.friday-budgeting-pro"
PLIST_DEST="$HOME/Library/LaunchAgents/${LABEL}.plist"
TEMPLATE_DIR="$(cd "$(dirname "$0")" && pwd)"
TEMPLATE="${TEMPLATE_DIR}/launchd-template.plist"

# 1. Ensure the app data directory exists.
mkdir -p "$HOME/.friday-bp"

# 2. Initialise the SQLite database (IF NOT EXISTS — fully idempotent).
python3 -c "from server.db import init_db; from server.paths import DB_PATH; init_db(DB_PATH)"

# 3. Render the launchd plist from the template (substitute @HOME@ and @PYTHON@).
PYTHON_BIN="$(command -v python3)"
sed \
    -e "s|@HOME@|${HOME}|g" \
    -e "s|@PYTHON@|${PYTHON_BIN}|g" \
    "$TEMPLATE" > "$PLIST_DEST"
chmod 0644 "$PLIST_DEST"

# 4. Register (or re-register) the service with launchd.
# "already loaded" errors are harmless — ignore them.
launchctl bootstrap "gui/$(id -u)" "$PLIST_DEST" || true

# 5. Done.
echo "✓ Friday Budgeting Pro installed. Open http://127.0.0.1:6789 to finish setup."
