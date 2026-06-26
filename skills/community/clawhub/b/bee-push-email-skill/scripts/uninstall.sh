#!/usr/bin/env bash
# Uninstall bee-push-email: stop service, remove files, clean systemd unit.
# Usage: uninstall.sh [--yes|-y]  (skip confirmation)
set -uo pipefail

INSTALL_DIR="/opt/imap-watcher"
SERVICE_NAME="imap-watcher"
SERVICE_UNIT="/etc/systemd/system/${SERVICE_NAME}.service"
LOG_FILE="/var/log/imap-watcher.log"
WATCHER_USER="imap-watcher"

FORCE=false
[[ "${1:-}" == "--yes" || "${1:-}" == "-y" ]] && FORCE=true

echo "🗑️  Bee Push Email Uninstaller"
echo ""

# Confirm (skip if --yes)
if [[ "$FORCE" != true ]]; then
    if ! tty -s; then
        echo "  Non-interactive mode. Use --yes to skip confirmation."
        echo "  Usage: uninstall.sh [--yes|-y]"
        exit 1
    fi
    read -rp "  Stop and remove the IMAP watcher service? [y/N]: " confirm
    if [[ "$confirm" != [yY] ]]; then
        echo "Aborted."
        exit 0
    fi
fi

# Stop and disable service
echo "  Stopping ${SERVICE_NAME}…"
if systemctl is-active --quiet "$SERVICE_NAME" 2>/dev/null; then
    systemctl stop "$SERVICE_NAME" && echo "  ✓ Stopped" || echo "  ⚠ Failed to stop"
fi

if systemctl is-enabled --quiet "$SERVICE_NAME" 2>/dev/null; then
    systemctl disable "$SERVICE_NAME" && echo "  ✓ Disabled" || echo "  ⚠ Failed to disable"
fi

# Remove systemd unit
if [[ -f "$SERVICE_UNIT" ]]; then
    rm -f "$SERVICE_UNIT"
    systemctl daemon-reload 2>/dev/null || true
    echo "  ✓ Removed systemd unit"
fi

# Remove install directory
if [[ -d "$INSTALL_DIR" ]]; then
    rm -rf "$INSTALL_DIR" && echo "  ✓ Removed ${INSTALL_DIR}" || echo "  ⚠ Failed to remove ${INSTALL_DIR}"
fi

# Remove log file
if [[ -f "$LOG_FILE" ]]; then
    rm -f "$LOG_FILE" && echo "  ✓ Removed log file" || echo "  ⚠ Failed to remove log file"
fi

# Remove system user (non-critical)
if id "$WATCHER_USER" &>/dev/null; then
    userdel "$WATCHER_USER" 2>/dev/null && echo "  ✓ Removed system user '${WATCHER_USER}'" || echo "  ⚠ Could not remove system user"
fi

# Unregister beemail bot commands from Telegram (non-critical)
echo "  Unregistering bot commands…"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UNREGISTER_SCRIPT=""
# Search: next to this script first, then known OpenClaw install paths
for candidate in     "${SCRIPT_DIR}/unregister_commands.py"     "/root/.openclaw/workspace/skills/bee-push-email/scripts/unregister_commands.py"     "/root/.openclaw/skills/bee-push-email/scripts/unregister_commands.py"; do
    if [[ -f "$candidate" ]]; then
        UNREGISTER_SCRIPT="$candidate"
        break
    fi
done

if [[ -n "$UNREGISTER_SCRIPT" ]]; then
    python3 "$UNREGISTER_SCRIPT" 2>/dev/null || echo "  ⚠ Could not unregister bot commands — remove via @BotFather"
else
    echo "  ⚠ unregister_commands.py not found — remove beemail commands manually via @BotFather"
fi

echo ""
echo "✅ Bee Push Email uninstalled completely."
