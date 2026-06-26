#!/bin/bash
# install-linux.sh — Install Gateway Watchdog Lite as a systemd user service (Linux)
#
# Usage:
#   WORKSPACE_PATH=/your/workspace OC_PORT=18789 TELEGRAM_ID=your_id bash install-linux.sh
#
# Supplied by ConfusedUser.com — OpenClaw tools & skills
# Full version with crash loop detection: https://confuseduser.com

set -euo pipefail

WORKSPACE_PATH="${WORKSPACE_PATH:-}"
OC_PORT="${OC_PORT:-}"
TELEGRAM_ID="${TELEGRAM_ID:-}"

if [ -z "$WORKSPACE_PATH" ] || [ -z "$OC_PORT" ]; then
    echo "ERROR: Missing required parameters."
    echo ""
    echo "Usage:"
    echo "  WORKSPACE_PATH=/your/workspace OC_PORT=18789 TELEGRAM_ID=your_id bash install-linux.sh"
    exit 1
fi

if ! command -v systemctl &>/dev/null; then
    echo "ERROR: systemctl not found. This script requires systemd."
    exit 1
fi

[ -z "${XDG_RUNTIME_DIR:-}" ] && export XDG_RUNTIME_DIR="/run/user/$(id -u)"

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_DIR="$WORKSPACE_PATH/.watchdog"
mkdir -p "$INSTALL_DIR"

cp "$SKILL_DIR/scripts/gateway-watchdog-linux.sh" "$INSTALL_DIR/gateway-watchdog.sh"
chmod +x "$INSTALL_DIR/gateway-watchdog.sh"

sed -i "s|PROBE_URL=\"http://127.0.0.1:YOUR_OC_PORT\"|PROBE_URL=\"http://127.0.0.1:${OC_PORT}\"|g" "$INSTALL_DIR/gateway-watchdog.sh"
sed -i "s|YOUR_TELEGRAM_ID|${TELEGRAM_ID}|g" "$INSTALL_DIR/gateway-watchdog.sh"
echo "[OK] Watchdog script installed to $INSTALL_DIR/gateway-watchdog.sh"

mkdir -p "$HOME/.config/systemd/user"
SERVICE_FILE="$HOME/.config/systemd/user/gateway-watchdog.service"

cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=OpenClaw Gateway Watchdog Lite
After=network.target

[Service]
Type=simple
ExecStart=$INSTALL_DIR/gateway-watchdog.sh
Restart=always
RestartSec=10
Environment="HOME=$HOME"
Environment="PATH=$PATH"
Environment="XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR"

[Install]
WantedBy=default.target
EOF

echo "[OK] systemd service written to $SERVICE_FILE"

systemctl --user daemon-reload
systemctl --user enable gateway-watchdog.service
systemctl --user start gateway-watchdog.service

echo ""
echo "==> Installation complete!"
echo "    Status: systemctl --user status gateway-watchdog"
echo "    Logs:   journalctl --user -u gateway-watchdog -f"
