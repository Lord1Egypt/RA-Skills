#!/bin/bash
# agentmemory verification script for OpenClaw

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🔍 agentmemory + OpenClaw Verification"
echo "======================================"
echo ""

# Check 1: Memory server on port 3111
echo -n "1. Memory server (port 3111): "
if curl -s --max-time 3 http://localhost:3111/agentmemory/health > /dev/null 2>&1; then
  echo -e "${GREEN}✅ running${NC}"
else
  echo -e "${RED}❌ not running${NC}"
  echo "   → Run: npx @agentmemory/agentmemory"
fi

# Check 2: Health endpoint
echo -n "2. Health endpoint: "
HEALTH=$(curl -s --max-time 3 http://localhost:3111/agentmemory/health 2>/dev/null || echo "")
if echo "$HEALTH" | grep -q "status.*ok\|version"; then
  VERSION=$(echo "$HEALTH" | grep -o '"version":"[^"]*"' | cut -d'"' -f4)
  echo -e "${GREEN}✅ healthy${NC} (v$VERSION)"
else
  echo -e "${RED}❌ not responding${NC}"
fi

# Check 3: Viewer on port 3113
echo -n "3. Viewer (port 3113): "
if curl -s --max-time 3 http://localhost:3113 > /dev/null 2>&1; then
  echo -e "${GREEN}✅ accessible${NC}"
else
  echo -e "${YELLOW}⚠️  not accessible (may still be initializing)${NC}"
fi

# Check 4: OpenClaw MCP config
echo -n "4. OpenClaw MCP config: "
CONFIG_FILE="$HOME/.openclaw/openclaw.json"
if [ -f "$CONFIG_FILE" ]; then
  if grep -q "agentmemory" "$CONFIG_FILE"; then
    echo -e "${GREEN}✅ configured${NC}"
  else
    echo -e "${YELLOW}⚠️  MCP not configured${NC}"
  fi
else
  echo -e "${RED}❌ config not found${NC}"
fi

# Check 5: systemd service (if installed)
echo -n "5. systemd service: "
SERVICE_FILE="$HOME/.config/systemd/user/agentmemory.service"
if [ -f "$SERVICE_FILE" ]; then
  if systemctl --user is-active --quiet agentmemory 2>/dev/null; then
    echo -e "${GREEN}✅ active${NC}"
  else
    echo -e "${YELLOW}⚠️  installed but not active${NC}"
  fi
else
  echo -e "${YELLOW}⚠️  not installed${NC}"
fi

echo ""
echo "📋 Quick commands:"
echo "   Start server:  npx @agentmemory/agentmemory"
echo "   View memories: http://localhost:3113"
echo "   Logs:          journalctl --user -u agentmemory -f"
echo "   Restart:       systemctl --user restart agentmemory"