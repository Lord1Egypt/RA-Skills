#!/bin/bash
# ClawOrchestrate — Systemd service installer
# Run this on each remote machine to set up persistent dispatcher

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DISPATCHER_PATH="$SCRIPT_DIR/dispatcher.py"
SERVICE_NAME="agent-dispatcher"
USER=$(whoami)

echo "Installing ClawOrchestrate dispatcher as systemd service..."

# Create service file
cat > ~/.config/systemd/user/${SERVICE_NAME}.service << EOF
[Unit]
Description=ClawOrchestrate Agent Dispatcher
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 ${DISPATCHER_PATH}
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=default.target
EOF

# Reload and enable
systemctl --user daemon-reload
systemctl --user enable ${SERVICE_NAME}
systemctl --user start ${SERVICE_NAME}

echo "✅ Service installed and started."
echo "Status: systemctl --user status ${SERVICE_NAME}"
echo "Logs: journalctl --user -u ${SERVICE_NAME} -f"
