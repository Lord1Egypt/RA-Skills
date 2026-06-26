#!/bin/bash
# Start Cloudflare tunnel for patent reports
# Usage: ./start_cloudflare_tunnel.sh

# Kill existing processes
pkill -f "python3 -m http.server" 2>/dev/null
pkill cloudflared 2>/dev/null
sleep 2

# Start HTTP server on port 8080
echo "🚀 Starting HTTP server on port 8080..."
cd /root/.openclaw/workspace/skills/epo-patent-intelligence/reports
python3 -m http.server 8080 > /tmp/http_server.log 2>&1 &
SERVER_PID=$!

sleep 3

# Test if server is working
if curl -s http://localhost:8080 > /dev/null; then
    echo "✅ HTTP server running on http://localhost:8080"
else
    echo "❌ HTTP server failed to start"
    exit 1
fi

# Start Cloudflare tunnel
echo "🌐 Starting Cloudflare tunnel..."
export TUNNEL_TOKEN="eyJhIjoiNmRiMjNkNDYxZjU5YjkyZjdmM2UyM2RkZjYwNjZkYzAiLCJ0IjoiZmE1M2NmZGEtOTYzMy00NDQ0LWJiMzItZDI4ZjllMTI3NTkyIiwicyI6IllUWmlaalk0Tm1NdFptRTNNQzAwTmpoaExUbGhaREF0WkRrNU1XWTFPRFExWW1VNCJ9"

# Try to start the tunnel
cloudflared tunnel --no-autoupdate run --token "$TUNNEL_TOKEN" --url http://localhost:8080 2>&1 &
TUNNEL_PID=$!

echo ""
echo "═══════════════════════════════════════════════════"
echo "  PATENT REPORT SERVER STARTED"
echo "═══════════════════════════════════════════════════"
echo ""
echo "📊 Local URL:     http://localhost:8080"
echo "🌐 Subdomain:     https://hermes.sqncr.ai/Patent_report_kw14"
echo ""
echo "📁 Reports directory:"
echo "   /root/.openclaw/workspace/skills/epo-patent-intelligence/reports/"
echo ""
echo "⚠️  Note: Cloudflare tunnel may take 30-60 seconds to establish"
echo ""
echo "📝 To stop: kill $SERVER_PID $TUNNEL_PID"
echo "═══════════════════════════════════════════════════"

# Save PIDs
echo $SERVER_PID > /tmp/patent_report.pid
echo $TUNNEL_PID >> /tmp/patent_report.pid
