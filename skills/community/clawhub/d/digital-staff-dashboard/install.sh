#!/bin/bash
#
# Agent Dashboard V2 Installation Script
# Compatible with OpenClaw / ClawHub
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_NAME="agent-dashboard"
PORT=${DASHBOARD_PORT:-5181}
PYTHON_CMD=${PYTHON_CMD:-python3}

echo -e "${BLUE}📊 Agent Dashboard V2 Installer${NC}"
echo "================================"
echo ""

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python version: $PYTHON_VERSION${NC}"

# Check if we're in the right directory
if [ ! -f "$SCRIPT_DIR/dashboard_server.py" ]; then
    echo -e "${RED}Error: dashboard_server.py not found.${NC}"
    echo "Please run this script from the agent-dashboard directory."
    exit 1
fi

echo -e "${GREEN}✓ Found dashboard_server.py${NC}"

# Check for OpenClaw
echo ""
echo -e "${BLUE}Checking OpenClaw installation...${NC}"
OPENCLAW_HOME=${OPENCLAW_HOME:-$HOME/.openclaw}

if [ ! -d "$OPENCLAW_HOME" ]; then
    echo -e "${YELLOW}⚠ OpenClaw home not found at $OPENCLAW_HOME${NC}"
    echo -e "${YELLOW}  The dashboard will work but some features may be limited.${NC}"
else
    echo -e "${GREEN}✓ OpenClaw found at: $OPENCLAW_HOME${NC}"
fi

# Install Python dependencies
echo ""
echo -e "${BLUE}Installing Python dependencies...${NC}"
$PYTHON_CMD -m pip install --user flask flask-cors 2>/dev/null || true

# Check if port is available
echo ""
echo -e "${BLUE}Checking port $PORT...${NC}"
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Port $PORT is already in use.${NC}"
    echo -e "${YELLOW}  The dashboard may already be running.${NC}"
else
    echo -e "${GREEN}✓ Port $PORT is available${NC}"
fi

# Create systemd user service (optional)
echo ""
echo -e "${BLUE}Setup options:${NC}"
read -p "Create systemd service for auto-start? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Creating systemd user service...${NC}"
    
    # Create systemd user directory if needed
    mkdir -p "$HOME/.config/systemd/user"
    
    # Create service file
    cat > "$HOME/.config/systemd/user/${SERVICE_NAME}.service" << EOF
[Unit]
Description=Agent Dashboard V2
After=network.target

[Service]
Type=simple
WorkingDirectory=$SCRIPT_DIR
Environment="OPENCLAW_HOME=$OPENCLAW_HOME"
Environment="DASHBOARD_PORT=$PORT"
ExecStart=$PYTHON_CMD $SCRIPT_DIR/dashboard_server.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

    echo -e "${GREEN}✓ Service file created${NC}"
    
    # Reload systemd
    systemctl --user daemon-reload
    
    # Enable and start service
    systemctl --user enable ${SERVICE_NAME}.service
    
    echo ""
    echo -e "${GREEN}Service commands:${NC}"
    echo "  Start:   systemctl --user start ${SERVICE_NAME}"
    echo "  Stop:    systemctl --user stop ${SERVICE_NAME}"
    echo "  Status:  systemctl --user status ${SERVICE_NAME}"
    echo "  Logs:    journalctl --user -u ${SERVICE_NAME} -f"
    
    # Start the service
    echo ""
    read -p "Start the dashboard now? (Y/n): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        systemctl --user start ${SERVICE_NAME}
        echo -e "${GREEN}✓ Service started${NC}"
        
        # Wait a moment for server to start
        sleep 2
        
        # Check if running
        if systemctl --user is-active --quiet ${SERVICE_NAME}; then
            echo ""
            echo -e "${GREEN}🎉 Agent Dashboard is running!${NC}"
            echo ""
            echo -e "${BLUE}Access URL:${NC} http://localhost:$PORT"
            echo ""
        else
            echo -e "${RED}✗ Service failed to start${NC}"
            echo "Check logs with: journalctl --user -u ${SERVICE_NAME} -f"
        fi
    fi
else
    echo -e "${YELLOW}Skipping systemd service creation${NC}"
    echo ""
    echo -e "${BLUE}To run manually:${NC}"
    echo "  cd $SCRIPT_DIR"
    echo "  python3 dashboard_server.py"
fi

# Create desktop entry (optional)
echo ""
read -p "Create desktop shortcut? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p "$HOME/.local/share/applications"
    
    cat > "$HOME/.local/share/applications/agent-dashboard.desktop" << EOF
[Desktop Entry]
Name=Agent Dashboard
Comment=OpenClaw Agent Management Dashboard
Exec=xdg-open http://localhost:$PORT
Icon=applications-system
Type=Application
Categories=Development;System;
StartupNotify=true
EOF

    echo -e "${GREEN}✓ Desktop shortcut created${NC}"
fi

# Final message
echo ""
echo "================================"
echo -e "${GREEN}📊 Installation Complete!${NC}"
echo "================================"
echo ""
echo -e "${BLUE}Dashboard URL:${NC} http://localhost:$PORT"
echo ""
echo "${BLUE}Quick Commands:${NC}"
if [[ $REPLY =~ ^[Yy]$ ]] && systemctl --user is-active --quiet ${SERVICE_NAME} 2>/dev/null; then
    echo "  Dashboard is running as a service"
    echo "  Stop:    systemctl --user stop ${SERVICE_NAME}"
else
    echo "  Start:   cd $SCRIPT_DIR && python3 dashboard_server.py"
fi
echo "  Config:  ~/.openclaw/openclaw.json"
echo ""
echo -e "${GREEN}Enjoy your Agent Dashboard! 🚀${NC}"
