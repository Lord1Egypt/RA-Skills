#!/bin/bash
# Restart tunnel for KW16
# Usage: ./restart_tunnel_kw16.sh

pkill -9 -f "python3.*http.server" 2>/dev/null
pkill -9 cloudflared 2>/dev/null
sleep 3

cd "/root/.openclaw/workspace/skills/epo-patent-intelligence/scripts/../reports"
nohup python3 -m http.server 8080 > /tmp/http_server_kw16.log 2>&1 &
sleep 3

export TUNNEL_TOKEN="eyJhIjoiNmRiMjNkNDYxZjU5YjkyZjdmM2UyM2RkZjYwNjZkYzAiLCJ0IjoiZmE1M2NmZGEtOTYzMy00NDQ0LWJiMzItZDI4ZjllMTI3NTkyIiwicyI6IllUWmlaalk0Tm1NdFptRTNNQzAwTmpoaExUbGhaREF0WkRrNU1XWTFPRFExWW1VNCJ9"
nohup cloudflared tunnel --no-autoupdate run --token "$TUNNEL_TOKEN" --url http://localhost:8080 > /tmp/tunnel_kw16.log 2>&1 &
sleep 5

echo ""
echo "═══════════════════════════════════════════════════"
echo "  ✅ PATENT REPORT KW16 DEPLOYMENT COMPLETE"
echo "═══════════════════════════════════════════════════"
echo ""
echo "📊 Local Server:  http://localhost:8080"
echo "🌐 Public URL:   https://hermes.sqncr.ai/Patent_report_kw16"
echo ""
echo "📈 Modern Dashboard Features:"
echo "   • Tailwind CSS enterprise styling"
echo "   • Chart.js interactive visualizations"
echo "   • Mobile-responsive design"
echo ""
echo "⚠️  Tunnel may take 30-60 seconds to fully propagate"
echo "═══════════════════════════════════════════════════"
