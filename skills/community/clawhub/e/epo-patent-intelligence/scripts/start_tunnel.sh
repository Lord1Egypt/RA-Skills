#!/bin/bash
# Start report server and tunnel

# Kill existing processes
pkill -f "report_server.py" 2>/dev/null
pkill cloudflared 2>/dev/null

# Start report server on port 8080
cd /root/.openclaw/workspace/skills/epo-patent-intelligence
python3 scripts/report_server.py &
SERVER_PID=$!
echo "Report server started on PID $SERVER_PID"

# Wait for server to be ready
sleep 3

# Check if server is running
if curl -s http://localhost:8080 > /dev/null; then
    echo "✅ Report server responding on :8080"
else
    echo "❌ Report server not responding"
    exit 1
fi

# Start Cloudflare tunnel
export TUNNEL_TOKEN="eyJhIjoiNmRiMjNkNDYxZjU5YjkyZjdmM2UyM2RkZjYwNjZkYzAiLCJ0IjoiZmE1M2NmZGEtOTYzMy00NDQ0LWJiMzItZDI4ZjllMTI3NTkyIiwicyI6IllUWmlaalk0Tm1NdFptRTNNQzAwTmpoaExUbGhaREF0WkRrNU1XWTFPRFExWW1VNCJ9"
cloudflared tunnel --no-autoupdate run --token "$TUNNEL_TOKEN" --url http://localhost:8080 &
TUNNEL_PID=$!
echo "Cloudflare tunnel started on PID $TUNNEL_PID"

# Save PIDs for later cleanup
echo $SERVER_PID > /tmp/patent_report_server.pid
echo $TUNNEL_PID > /tmp/patent_report_tunnel.pid

echo ""
echo "✅ Patent report server and tunnel started!"
echo "📊 Local: http://localhost:8080"
echo "🌐 Tunnel: Check https://hermes.sqncr.ai/Patent_report_kw14"