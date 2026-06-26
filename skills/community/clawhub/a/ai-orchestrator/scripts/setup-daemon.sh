#!/usr/bin/env bash
# setup-daemon.sh — One-command setup for ai-orchestrator daemon
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "🧩 Running isolation check..."
node "$SCRIPT_DIR/isolation-check.js"

echo "📦 Installing dependencies..."
npm install --silent

echo "🚀 Starting daemon..."
pm2 start deepseek-daemon.js --name deepseek-daemon --no-autorestart 2>/dev/null || pm2 restart deepseek-daemon

echo "💾 Saving PM2 state..."
pm2 save

echo "🔧 Setting up startup..."
pm2 startup 2>/dev/null || echo "  (run 'pm2 startup' manually if needed)"

echo ""
echo "✅ ai-orchestrator daemon is running!"
echo "   Test: ask-deepseek.sh --daemon 'Say OK'"
