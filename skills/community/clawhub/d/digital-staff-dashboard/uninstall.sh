#!/bin/bash
#
# Agent Dashboard V2 Uninstallation Script
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SERVICE_NAME="agent-dashboard"

echo -e "${BLUE}📊 Agent Dashboard V2 Uninstaller${NC}"
echo "==================================="
echo ""

# Check if service exists
if systemctl --user list-unit-files | grep -q "${SERVICE_NAME}.service"; then
    echo -e "${BLUE}Stopping and removing systemd service...${NC}"
    
    # Stop service if running
    if systemctl --user is-active --quiet ${SERVICE_NAME} 2>/dev/null; then
        systemctl --user stop ${SERVICE_NAME}
        echo -e "${GREEN}✓ Service stopped${NC}"
    fi
    
    # Disable service
    systemctl --user disable ${SERVICE_NAME} 2>/dev/null || true
    
    # Remove service file
    rm -f "$HOME/.config/systemd/user/${SERVICE_NAME}.service"
    
    # Reload systemd
    systemctl --user daemon-reload
    
    echo -e "${GREEN}✓ Service removed${NC}"
else
    echo -e "${YELLOW}No systemd service found${NC}"
fi

# Remove desktop entry
if [ -f "$HOME/.local/share/applications/agent-dashboard.desktop" ]; then
    echo -e "${BLUE}Removing desktop shortcut...${NC}"
    rm -f "$HOME/.local/share/applications/agent-dashboard.desktop"
    echo -e "${GREEN}✓ Desktop shortcut removed${NC}"
fi

echo ""
echo -e "${GREEN}✓ Uninstallation complete${NC}"
echo ""
echo "Note: The dashboard files have not been removed."
echo "To completely remove, delete this directory:"
echo "  $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
