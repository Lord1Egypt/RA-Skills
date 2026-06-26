#!/usr/bin/env bash
set -e

# genor-comfy-gate install script
# Installs dependencies and sets up PM2

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔══════════════════════════════════════════╗"
echo "║   Genor-Comfy-Gate — Installer           ║"
echo "╚══════════════════════════════════════════╝"

# 1. Install Node.js dependencies
echo ""
echo "→ Installing Node.js dependencies..."
npm install --production

# 2. Create necessary dirs
echo "→ Creating directories..."
mkdir -p workflows

# 3. Set up PM2
echo "→ Setting up PM2..."
if ! command -v pm2 &>/dev/null; then
    echo "  Installing PM2..."
    npm install -g pm2
fi

# 4. Register with PM2
echo "→ Registering with PM2..."
pm2 start pm2-ecosystem.config.cjs 2>/dev/null || pm2 restart genor-comfy-gate 2>/dev/null || true
pm2 save

echo ""
echo "✅ Genor-Comfy-Gate installed and running!"
echo "   Port: ${PORT:-8188}"
echo "   Add workflows: put .json files in workflows/"
echo ""
echo "   Configure via env vars:"
echo "     MEDIA_DIR          — output directory"
echo "     GATEWAY_PUBLIC_URL — public URL for media links"
echo "     GCG_API_KEY        — API key for remote access"
echo "     COMFY_SERVERS      — JSON array of ComfyUI backends"
