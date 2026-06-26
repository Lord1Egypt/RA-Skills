#!/bin/bash
# Kill existing and restart tunnel

pkill -9 -f "python3.*http.server" 2>/dev/null
pkill -9 cloudflared 2>/dev/null
sleep 3

cd /root/.openclaw/workspace/skills/epo-patent-intelligence/reports
nohup python3 -m http.server 8080 > /tmp/http_server_fresh.log 2>&1 &
sleep 3

export TUNNEL_TOKEN="eyJhIjoiNmRiMjNkNDYxZjU5YjkyZjdmM2UyM2RkZjYwNjZkYzAiLCJ0IjoiZmE1M2NmZGEtOTYzMy00NDQ0LWJiMzItZDI4ZjllMTI3NTkyIiwicyI6IllUWmlaalk0Tm1NdFptRTNNQzAwTmpoaExUbGhaREF0WkRrNU1XWTFPRFExWW1VNCJ9"
nohup cloudflared tunnel --no-autoupdate run --token "$TUNNEL_TOKEN" --url http://localhost:8080 > /tmp/tunnel.log 2>&1 &
sleep 5

# Verify processes are running
HTTP_PID=$(pgrep -f "python3 -m http.server 8080" || echo "")
TUNNEL_PID=$(pgrep cloudflared || echo "")

echo ""
echo "═══════════════════════════════════════════════════"
if [ -n "$HTTP_PID" ] && [ -n "$TUNNEL_PID" ]; then
    echo "  ✅ PATENT REPORT DEPLOYMENT COMPLETE"
    echo "═══════════════════════════════════════════════════"
    echo ""
    echo "📊 Local Server:  http://localhost:8080 (PID: $HTTP_PID)"
    echo "🌐 Public URL:   https://hermes.sqncr.ai/Patent_report_kw14"
    echo "🔒 Tunnel PID:   $TUNNEL_PID"
    echo ""
    echo "📈 Modern Dashboard Features:"
    echo "   • Tailwind CSS enterprise styling"
    echo "   • Chart.js interactive visualizations"
    echo "   • 37 real patents from EPO API"
    echo "   • Mobile-responsive design"
    echo ""
    echo "⚠️  Tunnel may take 30-60 seconds to fully propagate"
else
    echo "  ❌ DEPLOYMENT FAILED"
    echo "═══════════════════════════════════════════════════"
    echo ""
    [ -z "$HTTP_PID" ] && echo "❌ HTTP server failed to start"
    [ -z "$TUNNEL_PID" ] && echo "❌ Cloudflare tunnel failed to start"
    echo ""
    echo "Check logs:"
    echo "  HTTP: /tmp/http_server.log"
    echo "  Tunnel: /tmp/tunnel.log"
fi
echo "═══════════════════════════════════════════════════"