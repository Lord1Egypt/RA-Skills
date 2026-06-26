#!/bin/bash
# =============================================================================
# OpenClaw Security Audit - Interactive Fix Script
# =============================================================================
# Description: Interactive fix with user confirmation for each action
# Author: Winnie.C
# Version: 1.0.0
# Created: 2026-03-10
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[32m'
YELLOW='\033[33m'
BLUE='\033[34m'
CYAN='\033[36m'
NC='\033[0m'

# Configuration
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"
BACKUP_DIR="$HOME/.openclaw/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# =============================================================================
# Helper Functions
# =============================================================================

print_header() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✅]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠️]${NC} $1"
}

print_error() {
    echo -e "${RED}[❌]${NC} $1"
}

ask_confirmation() {
    local prompt="$1"
    local default="${2:-n}"

    echo ""
    echo -e "${YELLOW}$prompt${NC}"
    echo -n "Continue? [y/N]: "

    read -r response

    case "$response" in
        [yY][eE][sS]|[yY])
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

show_menu() {
    print_header "OpenClaw Security Fix Menu"

    echo "Available fixes:"
    echo ""
    echo "  1. 🔒 Fix Gateway Binding (change to localhost only)"
    echo "  2. 🔑 Generate New Token (40+ characters)"
    echo "  3. 🚫 Add Deny Commands (block dangerous commands)"
    echo "  4. 🔄 Restart Gateway Service"
    echo "  5. 🔐 Fix Firewall Settings"
    echo "  6. 📋 Run All Fixes (interactive)"
    echo ""
    echo "  0. Exit"
    echo ""
}

# =============================================================================
# Fix Functions
# =============================================================================

fix_gateway_binding() {
    print_header "Fix Gateway Binding"

    print_info "Current Gateway configuration:"
    python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
        g = cfg.get('gateway', {})
        print(f\"  Mode: {g.get('mode', 'unknown')}\")
        print(f\"  Bind: {g.get('bind', 'unknown')}\")
        print(f\"  Port: {g.get('port', 'unknown')}\")
except:
    print('  Error reading config')
" 2>/dev/null

    echo ""

    if ! ask_confirmation "This will change Gateway bind to 'loopback' (127.0.0.1 only)"; then
        print_info "Skipped"
        return 1
    fi

    # Backup
    cp "$OPENCLAW_CONFIG" "$BACKUP_DIR/openclaw.json.$TIMESTAMP"
    print_info "Backup created: $BACKUP_DIR/openclaw.json.$TIMESTAMP"

    # Apply fix
    python3 -c "
import json
with open('$OPENCLAW_CONFIG') as f:
    cfg = json.load(f)

if 'gateway' not in cfg:
    cfg['gateway'] = {}

cfg['gateway']['bind'] = 'loopback'
cfg['gateway']['mode'] = 'local'

with open('$OPENCLAW_CONFIG', 'w') as f:
    json.dump(cfg, f, indent=2)

print('✅ Gateway binding updated to loopback')
" 2>/dev/null

    if [ $? -eq 0 ]; then
        print_success "Gateway binding fixed"
        return 0
    else
        print_error "Failed to update Gateway binding"
        return 1
    fi
}

fix_token() {
    print_header "Generate New Token"

    print_info "Current token info:"
    python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
        token = cfg.get('gateway', {}).get('auth', {}).get('token', '')
        print(f\"  Token length: {len(token)} characters\")
        print(f\"  Token preview: {token[:8]}...{token[-4:] if len(token) > 12 else token}\")
except:
    print('  Error reading config')
" 2>/dev/null

    echo ""

    if ! ask_confirmation "This will generate a new secure token (64 characters)"; then
        print_info "Skipped"
        return 1
    fi

    # Generate new token
    local new_token=$(openssl rand -hex 32 2>/dev/null)

    if [ -z "$new_token" ]; then
        # Fallback to Python
        new_token=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    fi

    # Backup
    cp "$OPENCLAW_CONFIG" "$BACKUP_DIR/openclaw.json.$TIMESTAMP"
    print_info "Backup created: $BACKUP_DIR/openclaw.json.$TIMESTAMP"

    # Apply fix
    python3 -c "
import json
with open('$OPENCLAW_CONFIG') as f:
    cfg = json.load(f)

if 'gateway' not in cfg:
    cfg['gateway'] = {}
if 'auth' not in cfg['gateway']:
    cfg['gateway']['auth'] = {}

cfg['gateway']['auth']['token'] = '$new_token'

with open('$OPENCLAW_CONFIG', 'w') as f:
    json.dump(cfg, f, indent=2)

print(f'✅ New token generated: {len(\"$new_token\")} characters')
" 2>/dev/null

    if [ $? -eq 0 ]; then
        print_success "Token updated"
        print_info "New token: ${new_token:0:8}...${new_token: -4}"
        return 0
    else
        print_error "Failed to update token"
        return 1
    fi
}

fix_deny_commands() {
    print_header "Add Deny Commands"

    print_info "Current deny list:"
    python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
        deny = cfg.get('gateway', {}).get('nodes', {}).get('denyCommands', [])
        print(f\"  Commands blocked: {len(deny)}\")
        for cmd in deny[:5]:
            print(f\"    - {cmd}\")
        if len(deny) > 5:
            print(f\"    ... and {len(deny)-5} more\")
except:
    print('  Error reading config')
" 2>/dev/null

    echo ""

    print_info "Critical commands to deny:"
    echo "  - camera.snap"
    echo "  - camera.clip"
    echo "  - screen.record"
    echo "  - contacts.add"
    echo "  - reminders.add"
    echo "  - files.read (sensitive paths)"
    echo ""

    if ! ask_confirmation "Add these commands to deny list?"; then
        print_info "Skipped"
        return 1
    fi

    # Backup
    cp "$OPENCLAW_CONFIG" "$BACKUP_DIR/openclaw.json.$TIMESTAMP"
    print_info "Backup created: $BACKUP_DIR/openclaw.json.$TIMESTAMP"

    # Apply fix
    python3 -c "
import json
with open('$OPENCLAW_CONFIG') as f:
    cfg = json.load(f)

if 'gateway' not in cfg:
    cfg['gateway'] = {}
if 'nodes' not in cfg['gateway']:
    cfg['gateway']['nodes'] = {}

existing = cfg['gateway']['nodes'].get('denyCommands', [])
critical = ['camera.snap', 'camera.clip', 'screen.record', 'contacts.add', 'reminders.add']

all_deny = list(set(existing + critical))
cfg['gateway']['nodes']['denyCommands'] = all_deny

with open('$OPENCLAW_CONFIG', 'w') as f:
    json.dump(cfg, f, indent=2)

print(f'✅ Deny list updated: {len(all_deny)} commands blocked')
" 2>/dev/null

    if [ $? -eq 0 ]; then
        print_success "Deny commands updated"
        return 0
    else
        print_error "Failed to update deny commands"
        return 1
    fi
}

restart_gateway() {
    print_header "Restart Gateway Service"

    print_info "Current Gateway status:"
    ps aux | grep -i openclaw-gateway | grep -v grep || echo "  Not running"

    echo ""

    if ! ask_confirmation "This will restart the OpenClaw Gateway service"; then
        print_info "Skipped"
        return 1
    fi

    # Stop existing
    if pgrep -f "openclaw-gateway" > /dev/null 2>&1; then
        print_info "Stopping current Gateway..."
        pkill -f "openclaw-gateway"
        sleep 2
    fi

    # Start new
    print_info "Starting Gateway..."
    nohup openclaw-gateway > /dev/null 2>&1 &
    sleep 3

    # Verify
    if pgrep -f "openclaw-gateway" > /dev/null 2>&1; then
        print_success "Gateway restarted successfully"
        return 0
    else
        print_error "Failed to start Gateway"
        return 1
    fi
}

fix_firewall() {
    print_header "Fix Firewall Settings"

    print_info "Current firewall status:"
    /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null

    echo ""

    if ! ask_confirmation "Enable firewall and stealth mode? (requires sudo)"; then
        print_info "Skipped"
        return 1
    fi

    print_info "Enabling firewall..."
    sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on 2>/dev/null

    print_info "Enabling stealth mode..."
    sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode on 2>/dev/null

    print_success "Firewall configured"
    return 0
}

run_all_fixes() {
    print_header "Run All Fixes (Interactive)"

    print_warning "This will run all fixes with confirmation for each."
    echo ""

    if ! ask_confirmation "Continue with interactive fixes?"; then
        print_info "Cancelled"
        return 1
    fi

    local fixes_applied=0
    local fixes_skipped=0

    # Run each fix
    fix_gateway_binding
    if [ $? -eq 0 ]; then ((fixes_applied++)); else ((fixes_skipped++)); fi

    fix_token
    if [ $? -eq 0 ]; then ((fixes_applied++)); else ((fixes_skipped++)); fi

    fix_deny_commands
    if [ $? -eq 0 ]; then ((fixes_applied++)); else ((fixes_skipped++)); fi

    # Summary
    print_header "Fix Summary"

    echo "Fixes applied: $fixes_applied"
    echo "Fixes skipped: $fixes_skipped"
    echo ""

    if [ $fixes_applied -gt 0 ]; then
        print_warning "Consider restarting Gateway to apply changes"
        if ask_confirmation "Restart Gateway now?"; then
            restart_gateway
        fi
    fi
}

# =============================================================================
# Main
# =============================================================================

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

# Main menu loop
while true; do
    show_menu

    echo -n "Select option [0-6]: "
    read -r choice

    case $choice in
        1)
            fix_gateway_binding
            ;;
        2)
            fix_token
            ;;
        3)
            fix_deny_commands
            ;;
        4)
            restart_gateway
            ;;
        5)
            fix_firewall
            ;;
        6)
            run_all_fixes
            ;;
        0)
            print_info "Goodbye!"
            exit 0
            ;;
        *)
            print_error "Invalid option"
            ;;
    esac

    echo ""
    echo -n "Press Enter to continue..."
    read -r
done
