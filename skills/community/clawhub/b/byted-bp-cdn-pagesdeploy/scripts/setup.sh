#!/usr/bin/env bash
# Quick setup script - Install nest CLI and configure authentication
set -euo pipefail

echo "=== Pages Deploy - Quick Setup ==="
echo ""

# Install nest CLI
echo "[1/2] Installing @byteplus/nest CLI..."
INSTALL_DIR="${HOME}/.nest-cli"

if command -v nest &>/dev/null; then
    echo "[OK] nest CLI already installed globally"
elif [[ -x "$INSTALL_DIR/node_modules/.bin/nest" ]]; then
    echo "[OK] nest CLI already installed at $INSTALL_DIR"
else
    npm install @byteplus/nest --prefix "$INSTALL_DIR" 2>/dev/null
    echo "[OK] Installed to $INSTALL_DIR"
fi

NEST="${INSTALL_DIR}/node_modules/.bin/nest"
command -v nest &>/dev/null && NEST="nest"

echo ""
echo "[2/2] Configure authentication"
echo ""

if $NEST pages list &>/dev/null 2>&1; then
    echo "[OK] Authentication already configured"
else
    echo "Please enter your BytePlus / VolcEngine credentials:"
    echo ""
    read -p "Access Key: " AK
    read -p "Secret Key: " SK
    $NEST config set -g cloud.access_key "$AK"
    $NEST config set -g cloud.secret_key "$SK"
    echo "[OK] Credentials saved"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Usage:"
echo "  # Deploy a site"
echo "  bash scripts/deploy.sh --name my-site --dir ./dist"
echo ""
echo "  # Manage projects"
echo "  bash scripts/manage.sh list"
echo ""
echo "  # Add alias for convenience"
echo "  alias nest='$NEST'"
