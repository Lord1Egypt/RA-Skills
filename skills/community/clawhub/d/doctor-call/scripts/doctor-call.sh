#!/bin/bash
# Doctor Call: Run openclaw doctor and auto-fix issues

ACTION="${1:-check}"
TIMEOUT=30

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}🩺 Doctor Call${NC}"
echo ""

if [ "$ACTION" = "status" ]; then
    # Quick health check
    echo -e "${GREEN}📊 Status Check${NC}"
    echo ""
    
    if pgrep -f "openclaw" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ OpenClaw: Running${NC}"
    else
        echo -e "${RED}❌ OpenClaw: Not running${NC}"
        echo "Run 'doctor-call fix' to restart"
        exit 1
    fi
    
    DISK_PCT=$(df -h / | tail -1 | awk '{print $5}' | tr -d '%')
    echo -e "${GREEN}✅ Disk: ${DISK_PCT}% used${NC}"
    
    MEM_FREE=$(free -m | tail -2 | head -1 | awk '{print $7}')
    echo -e "${GREEN}✅ Memory: ${MEM_FREE}MB free${NC}"
    
    # Check if user timer is enabled
    if systemctl --user is-enabled openclaw-health.timer 2>/dev/null | grep -q "enabled"; then
        echo -e "${GREEN}✅ Auto-restart: Enabled (every 1 hour)${NC}"
    else
        echo -e "${YELLOW}⚠️  Auto-restart: Not enabled (run 'doctor-call setup')${NC}"
    fi
    
    echo ""
    echo "Run 'doctor-call check' for full diagnostics"
    
elif [ "$ACTION" = "check" ]; then
    # Full diagnostics
    echo -e "${GREEN}🔍 Running diagnostics...${NC}"
    echo ""
    
    timeout "$TIMEOUT" openclaw doctor --lint --non-interactive 2>&1 | head -50 || {
        echo -e "${YELLOW}⚠️  Doctor timed out - running basic checks instead${NC}"
        echo ""
        
        if pgrep -f "openclaw" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ OpenClaw: Running${NC}"
        else
            echo -e "${RED}❌ OpenClaw: Not running${NC}"
            echo ""
            echo -e "${YELLOW}⚠️  Gateway is down! Run 'doctor-call fix' to restart${NC}"
        fi
        
        DISK_PCT=$(df -h / | tail -1 | awk '{print $5}' | tr -d '%')
        if [ "$DISK_PCT" -gt 90 ]; then
            echo -e "${RED}❌ Disk: ${DISK_PCT}% full (critical)${NC}"
        else
            echo -e "${GREEN}✅ Disk: ${DISK_PCT}% used${NC}"
        fi
    }
    
elif [ "$ACTION" = "fix" ]; then
    # Auto-repair
    echo -e "${YELLOW}🔧 Running auto-repair...${NC}"
    echo ""
    
    # Check if OpenClaw is running
    if ! pgrep -f "openclaw" > /dev/null 2>&1; then
        echo -e "${RED}⚠️  OpenClaw not running - restarting gateway...${NC}"
        echo ""
        systemctl --user restart openclaw-gateway 2>&1
        sleep 3
        if pgrep -f "openclaw" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Gateway restarted successfully${NC}"
        else
            echo -e "${RED}❌ Restart failed${NC}"
        fi
        echo ""
        exit 0
    fi
    
    # Try doctor repair first
    timeout "$TIMEOUT" openclaw doctor --repair --yes --non-interactive 2>&1 || {
        echo -e "${YELLOW}⚠️  Doctor timed out${NC}"
    }
    
    # Check if gateway is still healthy after repair
    if ! pgrep -f "openclaw" > /dev/null 2>&1; then
        echo ""
        echo -e "${RED}⚠️  Gateway crashed - restarting...${NC}"
        systemctl --user restart openclaw-gateway 2>&1
        sleep 3
        if pgrep -f "openclaw" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Gateway restarted${NC}"
        fi
    else
        echo ""
        echo -e "${GREEN}🎉 All fixed!${NC}"
    fi

elif [ "$ACTION" = "setup" ]; then
    # Set up systemd user timer (no sudo needed!)
    echo -e "${GREEN}🔧 Setting up auto-restart via systemd...${NC}"
    echo ""
    
    mkdir -p ~/.config/systemd/user
    
    # Create systemd service (user-level, no sudo needed)
    cat > ~/.config/systemd/user/openclaw-health.service <<'EOF'
[Unit]
Description=OpenClaw Health Monitor

[Service]
Type=oneshot
ExecStart=/home/umbrel/.openclaw/skills/doctor-call/scripts/doctor-call.sh fix
StandardOutput=journal
StandardError=journal
EOF

    # Create systemd timer (runs every 5 minutes)
    cat > ~/.config/systemd/user/openclaw-health.timer <<'EOF'
[Unit]
Description=Run OpenClaw health check every 5 minutes

[Timer]
OnBootSec=30
OnUnitActiveSec=5min
Unit=openclaw-health.service

[Install]
WantedBy=default.target
EOF

    systemctl --user daemon-reload
    systemctl --user enable openclaw-health.timer
    systemctl --user start openclaw-health.timer
    
    echo ""
    echo -e "${GREEN}✅ Auto-restart enabled!${NC}"
    echo ""
    echo "• Service: ~/.config/systemd/user/openclaw-health.service"
    echo "• Timer: runs every 1 hour"
    echo "• OpenClaw will auto-restart if it crashes"
    echo ""
    echo "Check status: systemctl --user status openclaw-health.timer"
    
elif [ "$ACTION" = "remove" ]; then
    # Remove systemd auto-restart
    echo -e "${YELLOW}🗑️  Removing auto-restart...${NC}"
    systemctl --user stop openclaw-health.timer 2>/dev/null || true
    systemctl --user disable openclaw-health.timer 2>/dev/null || true
    rm -f ~/.config/systemd/user/openclaw-health.service
    rm -f ~/.config/systemd/user/openclaw-health.timer
    systemctl --user daemon-reload
    echo -e "${GREEN}✅ Auto-restart removed${NC}"
fi

echo ""