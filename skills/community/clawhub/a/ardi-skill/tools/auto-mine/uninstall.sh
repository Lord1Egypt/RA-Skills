#!/usr/bin/env bash
# uninstall.sh — remove auto-mine completely. Does NOT delete:
#   - your local commit/inscription state in ~/.ardi-agent/state/
#   - the env file at ~/.ardi-agent/auto-mine.env (in case you reinstall)
#   - the symlink at ~/.local/share/ardi-auto-mine (re-created on reinstall)
set -euo pipefail
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"
systemctl --user disable --now ardi-mine.timer 2>/dev/null || true
systemctl --user disable ardi-mine.service 2>/dev/null || true
rm -f "$SYSTEMD_USER_DIR/ardi-mine.timer" "$SYSTEMD_USER_DIR/ardi-mine.service"
systemctl --user daemon-reload
echo "auto-mine uninstalled. Env + state preserved."
