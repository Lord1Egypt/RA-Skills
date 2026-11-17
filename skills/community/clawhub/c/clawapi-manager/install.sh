#!/bin/bash
#
# API Cockpit - Install Script
# Sets up the cockpit skill, permissions, and cron jobs
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Installing API Cockpit in ${SCRIPT_DIR}..."

# Set correct permissions
echo "Setting permissions..."
chmod 700 "${SCRIPT_DIR}"
chmod 600 "${SCRIPT_DIR}/config" 2>/dev/null || true
chmod 600 "${SCRIPT_DIR}/config/.env" 2>/dev/null || true
chmod 700 "${SCRIPT_DIR}/"*.sh 2>/dev/null || true
chmod 700 "${SCRIPT_DIR}/lib/"*.py 2>/dev/null || true

# Create required directories
echo "Creating directories..."
mkdir -p "${SCRIPT_DIR}/logs"
mkdir -p "${SCRIPT_DIR}/data"
mkdir -p "${SCRIPT_DIR}/locks"
chmod 700 "${SCRIPT_DIR}/logs" "${SCRIPT_DIR}/data" "${SCRIPT_DIR}/locks"

# Install logrotate config
echo "Installing logrotate..."
if [ -d "/etc/logrotate.d" ]; then
    if [ -f "${SCRIPT_DIR}/logrotate.d/api-cockpit" ]; then
        cp "${SCRIPT_DIR}/logrotate.d/api-cockpit" "/etc/logrotate.d/api-cockpit"
        chmod 644 "/etc/logrotate.d/api-cockpit"
        echo "✓ logrotate config installed"
    fi
fi

# Copy config template if not exists
if [ ! -f "${SCRIPT_DIR}/config/.env" ] && [ -f "${SCRIPT_DIR}/config/.env.example" ]; then
    echo "Creating config from template..."
    cp "${SCRIPT_DIR}/config/.env.example" "${SCRIPT_DIR}/config/.env"
    chmod 600 "${SCRIPT_DIR}/config/.env"
    echo "⚠️  Please edit ${SCRIPT_DIR}/config/.env and fill in your credentials!"
fi

echo ""
echo "✅ API Cockpit installed!"
echo ""
echo "Next steps:"
echo "1. Edit config: ${SCRIPT_DIR}/config/.env"
echo "2. Test health check: ${SCRIPT_DIR}/cockpit-admin.sh health"
echo "3. (Optional) Install cron: cp ${SCRIPT_DIR}/cron.example /etc/cron.d/api-cockpit"
echo ""
