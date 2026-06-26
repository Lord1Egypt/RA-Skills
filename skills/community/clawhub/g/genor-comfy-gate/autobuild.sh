#!/usr/bin/env bash
set -e

# Auto-build and restart genor-comfy-gate
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Fetching latest changes..."
git pull || echo "No git repo or already up to date"

echo "Installing dependencies..."
npm install --production

# Restart via PM2 (if already running) or start if not
if pm2 list | grep -q genor-comfy-gate; then
    echo "Restarting genor-comfy-gate via PM2..."
    pm2 restart genor-comfy-gate
else
    echo "Starting genor-comfy-gate via PM2..."
    pm2 start pm2-ecosystem.config.cjs
fi

pm2 save

echo "✅ Auto-build complete."
