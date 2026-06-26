#!/bin/bash
# Quick Local Production Deployment

set -e

echo "🦪 SHIB Payment Agent - Local Production Deployment"
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ Don't run as root. Run as regular user (will use sudo when needed)."
   exit 1
fi

# Check if .env.local exists
if [ ! -f .env.local ]; then
    echo "❌ .env.local not found!"
    echo "   Create it from .env.example and add your wallet details."
    exit 1
fi

echo "✅ Environment configured"

# Install systemd service
echo "📦 Installing systemd service..."
sudo cp shib-payment-agent.service /etc/systemd/system/
sudo systemctl daemon-reload

echo "✅ Service installed"

# Enable auto-start
echo "🔄 Enabling auto-start on boot..."
sudo systemctl enable shib-payment-agent

# Stop if already running
if sudo systemctl is-active --quiet shib-payment-agent; then
    echo "⏸️  Stopping existing instance..."
    sudo systemctl stop shib-payment-agent
fi

# Start service
echo "🚀 Starting agent..."
sudo systemctl start shib-payment-agent

# Wait a moment
sleep 2

# Check status
if sudo systemctl is-active --quiet shib-payment-agent; then
    echo ""
    echo "✅ Deployment complete!"
    echo ""
    echo "Agent Status:"
    sudo systemctl status shib-payment-agent --no-pager | head -10
    echo ""
    echo "📍 Running on: http://localhost:8003"
    echo "🔗 Agent Card: http://localhost:8003/.well-known/agent-card.json"
    echo ""
    echo "Useful commands:"
    echo "  sudo systemctl status shib-payment-agent   # Check status"
    echo "  sudo systemctl stop shib-payment-agent     # Stop agent"
    echo "  sudo systemctl restart shib-payment-agent  # Restart agent"
    echo "  sudo journalctl -u shib-payment-agent -f   # View logs"
    echo ""
    echo "🎉 Agent is now running and will auto-start on boot!"
else
    echo ""
    echo "❌ Failed to start agent"
    echo "Check logs with: sudo journalctl -u shib-payment-agent -n 50"
    exit 1
fi
