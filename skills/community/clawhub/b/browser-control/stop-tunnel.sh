#!/bin/bash
echo "🛑 Stopping Browser Control services..."

pkill -f "ngrok.*http" 2>/dev/null && echo "   ✓ ngrok stopped" || echo "   - ngrok not running"
pkill -f "websockify.*6080" 2>/dev/null && echo "   ✓ noVNC stopped" || echo "   - noVNC not running"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    vncserver -kill :1 2>/dev/null && echo "   ✓ VNC stopped" || echo "   - VNC not running"
fi

echo ""
echo "✅ All services stopped"
