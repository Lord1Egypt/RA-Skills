#!/usr/bin/env bash

# Helper script to install ghostclaw.service replacing placeholders with current user and paths
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
SERVICE_FILE="ghostclaw.service"
TARGET="/etc/systemd/system/$SERVICE_FILE"

# Detect current user
CURRENT_USER=$(whoami)

# Detect path to ghostclaw-mcp (check pipx first, then generic paths, fallback to Python -m)
if command -v ghostclaw-mcp >/dev/null 2>&1; then
    EXEC_START="$(command -v ghostclaw-mcp)"
else
    # Fallback to python module directly
    PYTHON_CMD=$(command -v python3)
    EXEC_START="$PYTHON_CMD -m ghostclaw_mcp.server"
fi

echo "Installing Ghostclaw systemd service..."
echo "User: $CURRENT_USER"
echo "ExecStart: $EXEC_START"
echo "WorkingDirectory: $REPO_ROOT"

# Create a temporary file
TEMP_FILE=$(mktemp)

# Replace placeholders
cat "$SCRIPT_DIR/$SERVICE_FILE" \
    | sed "s|User=ghostclaw|User=$CURRENT_USER|g" \
    | sed "s|ExecStart=/usr/local/bin/ghostclaw-mcp|ExecStart=$EXEC_START|g" \
    | sed "s|WorkingDirectory=/opt/ghostclaw|WorkingDirectory=$REPO_ROOT|g" \
    > "$TEMP_FILE"

echo "Copying to $TARGET (requires sudo)..."
sudo cp "$TEMP_FILE" "$TARGET"
sudo chmod 644 "$TARGET"
rm "$TEMP_FILE"

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload
echo "Enabling service to start on boot..."
sudo systemctl enable "$SERVICE_FILE"
echo "Starting service..."
sudo systemctl start "$SERVICE_FILE"

echo ""
echo "✅ Ghostclaw MCP Server is now running in the background!"
echo "You can check its status with: sudo systemctl status $SERVICE_FILE"
