#!/bin/bash
# Quick report server startup

pkill -f "python3 -m http.server" 2>/dev/null
sleep 1

cd /root/.openclaw/workspace/skills/epo-patent-intelligence/reports
python3 -m http.server 8080 > /tmp/simple_server.log 2>&1 &
sleep 2

echo "Server started on port 8080"
curl -s http://localhost:8080 | head -5