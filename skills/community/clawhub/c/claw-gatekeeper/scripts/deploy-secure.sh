#!/bin/bash
#
# Claw Gatekeeper - Secure Deployment Script
# Deploys Guardian in maximum security mode (human-in-the-loop)
#
# Usage: ./deploy-secure.sh [--check | --apply | --restore]
#   --check   : Verify current security settings
#   --apply   : Apply hardened configuration (default)
#   --restore : Restore from backup

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.claw-gatekeeper"
BACKUP_DIR="$CONFIG_DIR/backups"
HARDENED_CONFIG="$SCRIPT_DIR/../config/config.hardened.json"
CURRENT_CONFIG="$CONFIG_DIR/config.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_banner() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║     🛡️  OpenClaw Guardian - Secure Deployment Tool          ║"
    echo "║           Human-in-the-Loop Security Mode                    ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
}

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if [ ! -d "$CONFIG_DIR" ]; then
        print_error "OpenClaw Guardian config directory not found: $CONFIG_DIR"
        print_status "Please install Guardian first before running this script"
        exit 1
    fi
    
    if [ ! -f "$HARDENED_CONFIG" ]; then
        print_error "Hardened config not found: $HARDENED_CONFIG"
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 is required but not installed"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

create_backup() {
    local backup_timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$BACKUP_DIR/config.json.bak.$backup_timestamp"
    
    mkdir -p "$BACKUP_DIR"
    
    if [ -f "$CURRENT_CONFIG" ]; then
        cp "$CURRENT_CONFIG" "$backup_file"
        print_success "Current config backed up to: $backup_file"
        echo "$backup_file" > "$BACKUP_DIR/latest.txt"
    else
        print_warning "No existing config to backup"
    fi
}

apply_hardened_config() {
    print_status "Applying hardened security configuration..."
    
    # Copy hardened config
    cp "$HARDENED_CONFIG" "$CURRENT_CONFIG"
    
    # Set secure permissions
    chmod 600 "$CURRENT_CONFIG"
    
    print_success "Hardened configuration applied"
}

setup_audit_logging() {
    print_status "Setting up secure audit logging..."
    
    local session_dir="$CONFIG_DIR/sessions"
    local audit_log="$session_dir/Operate_Audit.log"
    
    mkdir -p "$session_dir"
    touch "$audit_log"
    chmod 600 "$audit_log"
    
    # Secure the sessions directory
    chmod 700 "$session_dir"
    
    print_success "Audit logging configured"
}

setup_log_rotation() {
    print_status "Setting up log rotation (30-day retention)..."
    
    # Check if cron is available
    if ! command -v crontab &> /dev/null; then
        print_warning "Cron not available - skipping automatic log rotation setup"
        print_status "Please manually configure log rotation for: $CONFIG_DIR/sessions/*.log"
        return
    fi
    
    # Check if rotation job already exists
    if crontab -l 2>/dev/null | grep -q "claw-gatekeeper.*find.*sessions.*delete"; then
        print_success "Log rotation already configured"
        return
    fi
    
    # Add rotation job
    (crontab -l 2>/dev/null || echo "") | {
        cat
        echo "# OpenClaw Guardian - Audit log rotation (30-day retention)"
        echo "0 0 * * * find $CONFIG_DIR/sessions -name '*.log' -type f -mtime +30 -delete 2>/dev/null"
    } | crontab -
    
    print_success "Log rotation cron job added (30-day retention)"
}

verify_configuration() {
    print_status "Verifying configuration..."
    
    if [ -f "$CURRENT_CONFIG" ]; then
        # Check key security settings
        local strict_mode=$(python3 -c "import json; print(json.load(open('$CURRENT_CONFIG')).get('strict_mode', False))" 2>/dev/null || echo "False")
        local auto_allow_low=$(python3 -c "import json; print(json.load(open('$CURRENT_CONFIG')).get('auto_allow_low', True))" 2>/dev/null || echo "True")
        local medium_approval=$(python3 -c "import json; print(json.load(open('$CURRENT_CONFIG')).get('medium_requires_approval', False))" 2>/dev/null || echo "False")
        
        echo ""
        echo "Current Security Settings:"
        echo "  Strict Mode: $strict_mode"
        echo "  Auto-allow LOW: $auto_allow_low"
        echo "  MEDIUM requires approval: $medium_approval"
        echo ""
        
        if [ "$strict_mode" = "True" ] && [ "$auto_allow_low" = "False" ] && [ "$medium_approval" = "True" ]; then
            print_success "Configuration verified: Hardened mode active"
            return 0
        else
            print_warning "Configuration may not be fully hardened"
            return 1
        fi
    else
        print_error "Configuration file not found"
        return 1
    fi
}

print_security_report() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                 🔒 Security Deployment Report                ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║                                                              ║"
    echo "║  ✅ Hardened Configuration:        APPLIED                   ║"
    echo "║  ✅ Human-in-the-Loop Mode:        ENABLED                   ║"
    echo "║  ✅ All Operations Require:        CONFIRMATION              ║"
    echo "║  ✅ Strict Mode:                   ENABLED                   ║"
    echo "║  ✅ Audit Logging:                 CONFIGURED                ║"
    echo "║  ✅ Log Rotation (30 days):        CONFIGURED                ║"
    echo "║  ✅ File Permissions:              SECURED (600)             ║"
    echo "║                                                              ║"
    echo "║  🛡️  Risk Level Behaviors:                                   ║"
    echo "║     🔴 CRITICAL (80-100):          Always Confirm            ║"
    echo "║     🟠 HIGH (60-79):               Always Confirm            ║"
    echo "║     🟡 MEDIUM (30-59):             Always Confirm            ║"
    echo "║     🟢 LOW (0-29):                 Always Confirm            ║"
    echo "║                                                              ║"
    echo "║  ⚠️  IMPORTANT:                                              ║"
    echo "║     All operations now require manual approval.              ║"
    echo "║     Session auto-approval available for MEDIUM/HIGH.         ║"
    echo "║     CRITICAL operations always require individual confirm.   ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Files Modified:"
    echo "  • $CURRENT_CONFIG"
    echo "  • $CONFIG_DIR/sessions/Operate_Audit.log"
    echo ""
    echo "Backup Location:"
    if [ -f "$BACKUP_DIR/latest.txt" ]; then
        echo "  • $(cat "$BACKUP_DIR/latest.txt")"
    fi
    echo ""
    echo "To verify:   python3 $SCRIPT_DIR/policy_config.py validate"
    echo "To restore:  $0 --restore"
    echo ""
}

restore_backup() {
    print_status "Restoring configuration from backup..."
    
    if [ ! -f "$BACKUP_DIR/latest.txt" ]; then
        print_error "No backup found to restore"
        exit 1
    fi
    
    local latest_backup=$(cat "$BACKUP_DIR/latest.txt")
    
    if [ ! -f "$latest_backup" ]; then
        print_error "Backup file not found: $latest_backup"
        exit 1
    fi
    
    cp "$latest_backup" "$CURRENT_CONFIG"
    chmod 600 "$CURRENT_CONFIG"
    
    print_success "Configuration restored from: $latest_backup"
    print_status "Current security settings:"
    verify_configuration || true
}

check_mode() {
    print_banner
    print_status "Checking current security mode..."
    
    if [ ! -f "$CURRENT_CONFIG" ]; then
        print_error "No configuration found"
        exit 1
    fi
    
    verify_configuration
}

main() {
    local mode="${1:---apply}"
    
    case "$mode" in
        --check)
            check_mode
            ;;
        --restore)
            print_banner
            check_prerequisites
            restore_backup
            ;;
        --apply|*)
            print_banner
            check_prerequisites
            create_backup
            apply_hardened_config
            setup_audit_logging
            setup_log_rotation
            verify_configuration
            print_security_report
            ;;
    esac
}

main "$@"
