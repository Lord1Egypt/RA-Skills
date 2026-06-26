#!/bin/bash
# =============================================================================
# OpenClaw Security Audit - Report Generator
# =============================================================================
# Description: Generate HTML/JSON audit reports
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
NC='\033[0m'

# Default values
OUTPUT_DIR="./reports"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FORMAT="html"

# =============================================================================
# Helper Functions
# =============================================================================

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -f, --format FORMAT    Output format: html or json (default: html)"
    echo "  -o, --output DIR      Output directory (default: ./reports)"
    echo "  -q, --quick          Quick check mode (skip detailed checks)"
    echo "  -h, --help           Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --format html --output ./reports"
    echo "  $0 --format json --output ./reports"
    echo "  $0 --quick"
}

# =============================================================================
# Audit Functions
# =============================================================================

check_network_exposure() {
    local result="PASS"
    local details=""

    # Check Gateway port binding
    local gateway_bind=$(lsof -i :18789 2>/dev/null | grep -c "LISTEN" || true)
    if echo "$gateway_bind" | grep -q "0.0.0.0"; then
        result="FAIL"
        details="Gateway is bound to 0.0.0.0 (exposed to network)"
    fi

    # Check Tailscale status
    local tailscale_status=$(tailscale status 2>/dev/null || echo "Not running")
    if echo "$tailscale_status" | grep -q "Running"; then
        if [ "$result" = "PASS" ]; then
            result="WARN"
        fi
        details="${details}Tailscale is running"
    fi

    echo "$result|$details"
}

check_token_security() {
    local result="PASS"
    local details=""

    local config_path="$HOME/.openclaw/openclaw.json"
    if [ ! -f "$config_path" ]; then
        echo "SKIP|Config file not found"
        return
    fi

    local token_info=$(python3 -c "
import json
with open('$config_path') as f:
    cfg = json.load(f)
    token = cfg.get('gateway', {}).get('auth', {}).get('token', '')
    print(f'{len(token)}|{cfg.get(\"gateway\", {}).get(\"mode\", \"local\")}|{cfg.get(\"gateway\", {}).get(\"bind\", \"loopback\")}')
" 2>/dev/null)

    local token_length=$(echo "$token_info" | cut -d'|' -f1)
    local mode=$(echo "$token_info" | cut -d'|' -f2)
    local bind=$(echo "$token_info" | cut -d'|' -f3)

    if [ "$token_length" -lt 40 ]; then
        result="FAIL"
        details="Token length is $token_length (should be >= 40)"
    fi

    if [ "$mode" != "local" ]; then
        if [ "$result" = "PASS" ]; then
            result="WARN"
            details="Mode is $mode (should be local)"
        else
            details="${details}, Mode is $mode"
        fi
    fi

    echo "$result|$details"
}

check_deny_commands() {
    local result="PASS"
    local details=""

    local config_path="$HOME/.openclaw/openclaw.json"
    if [ ! -f "$config_path" ]; then
        echo "SKIP|Config file not found"
        return
    fi

    local deny_list=$(python3 -c "
import json
with open('$config_path') as f:
    cfg = json.load(f)
    deny = cfg.get('gateway', {}).get('nodes', {}).get('denyCommands', [])
    print('|'.join(deny) if deny else '')
" 2>/dev/null)

    local required_deny=("camera.snap|camera.clip|screen.record|contacts.add|reminders.add")

    for cmd in $(echo "$required_deny" | tr '|' '\n'); do
        if ! echo "$deny_list" | grep -q "$cmd"; then
            if [ "$result" = "PASS" ]; then
                result="WARN"
                details="Missing: $cmd"
            else
                details="${details}, $cmd"
            fi
        fi
    done

    echo "$result|$details"
}

check_tcc_permissions() {
    local result="PASS"
    local details=""

    # Check Full Disk Access
    local fda=$(python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('/Library/Application Support/com.apple.TCC/TCC.db')
    cursor = conn.cursor()
    cursor.execute('SELECT auth_value FROM access WHERE client=\"/usr/local/bin/node\" AND service=\"kTCCServiceSystemPolicyAllFiles\"')
    r = cursor.fetchone()
    print('granted' if r and r[0]==2 else 'not_granted')
    conn.close()
except:
    print('error')
" 2>/dev/null)

    if [ "$fda" = "granted" ]; then
        result="FAIL"
        details="Full Disk Access is granted (security risk)"
    fi

    echo "$result|$details"
}

check_icloud_sync() {
    local result="PASS"
    local details=""

    for dir in Documents Pictures Desktop; do
        local count=$(ls -la ~/$dir/ 2>/dev/null | grep -v "^total" | grep -v "^.localized$" | wc -l)
        if [ "$count" -gt 0 ]; then
            if [ "$result" = "PASS" ]; then
                result="WARN"
                details="~/$dir has $count items (iCloud sync risk)"
            else
                details="${details}, ~/$dir"
            fi
        fi
    done

    echo "$result|$details"
}

check_workspace_privacy() {
    local result="PASS"
    local details=""

    local workspace="$HOME/.openclaw/workspace"
    if [ ! -d "$workspace" ]; then
        echo "SKIP|Workspace not found"
        return
    fi

    # Check for symlinks
    local symlinks=$(find "$workspace" -type l 2>/dev/null | head -5)
    if [ -n "$symlinks" ]; then
        result="WARN"
        details="Found symlinks in workspace"
    fi

    echo "$result|$details"
}

check_network_connections() {
    local result="PASS"
    local details=""

    local gateway_pid=$(pgrep -f "openclaw-gateway" 2>/dev/null)
    if [ -z "$gateway_pid" ]; then
        echo "SKIP|Gateway not running"
        return
    fi

    local connections=$(lsof -p "$gateway_pid" -i 2>/dev/null | grep ESTABLISHED || true)
    local suspicious=$(echo "$connections" | grep -v "openai\|anthropic\|google\|feishu\|telegram\|whatsapp" | grep -v "^COMMAND" || true)

    if [ -n "$suspicious" ]; then
        result="WARN"
        details="Found suspicious connections"
    fi

    echo "$result|$details"
}

check_logs() {
    local result="PASS"
    local details=""

    local log_file="$HOME/.openclaw/logs/gateway.log"
    if [ ! -f "$log_file" ]; then
        echo "SKIP|Log file not found"
        return
    fi

    local errors=$(tail -50 "$log_file" | grep -i "error\|fail\|exception" | wc -l)
    if [ "$errors" -gt 5 ]; then
        result="WARN"
        details="Found $errors errors in last 50 log lines"
    fi

    echo "$result|$details"
}

# =============================================================================
# Report Generation
# =============================================================================

generate_html_report() {
    local report_file="$OUTPUT_DIR/security-audit-$TIMESTAMP.html"

    cat > "$report_file" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenClaw Security Audit Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 40px; background: #f5f5f7; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        .check-item { margin: 20px 0; padding: 15px; border-radius: 5px; }
        .pass { background: #d4edda; border-left: 4px solid #28a745; }
        .fail { background: #f8d7da; border-left: 4px solid #dc3545; }
        .warn { background: #fff3cd; border-left: 4px solid #ffc107; }
        .skip { background: #e9ecef; border-left: 4px solid #6c757d; }
        .status { font-weight: bold; text-transform: uppercase; font-size: 12px; }
        .timestamp { color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🦞 OpenClaw Security Audit Report</h1>
        <p class="timestamp">Generated: '"$(date)"'</p>
        <div id="results"></div>
        <h2>Summary</h2>
        <div id="summary"></div>
    </div>
</body>
</html>
EOF

    # Run checks and collect results
    local results=""
    local pass_count=0
    local fail_count=0
    local warn_count=0

    echo "<div id='results'>" >> "$report_file"

    for check_func in check_network_exposure check_token_security check_deny_commands check_tcc_permissions check_icloud_sync check_workspace_privacy check_network_connections check_logs; do
        local check_name=$(echo "$check_func" | sed 's/check_/g' | sed 's/_/ /g')
        local result=$($check_func)
        local status=$(echo "$result" | cut -d'|' -f1)
        local details=$(echo "$result" | cut -d'|' -f2-)

        case $status in
            PASS) ((pass_count++)); css_class="pass" ;;
            FAIL) ((fail_count++)); css_class="fail" ;;
            WARN) ((warn_count++)); css_class="warn" ;;
            SKIP) css_class="skip" ;;
        esac

        echo "<div class=\"check-item $css_class\"><span class=\"status\">$status</span>: $check_name<br><small>$details</small></div>" >> "$report_file"
    done

    echo "</div>" >> "$report_file"

    # Add summary
    echo "<div id='summary'><p>Total: $((pass_count + fail_count + warn_count)) checks</p><p>✅ Passed: $pass_count | ❌ Failed: $fail_count | ⚠️ Warnings: $warn_count</p></div>" >> "$report_file"

    # Close HTML
    echo "</div></body></html>" >> "$report_file"

    print_success "HTML report generated: $report_file"
}

generate_json_report() {
    local report_file="$OUTPUT_DIR/security-audit-$TIMESTAMP.json"

    # Run checks and collect results
    local pass_count=0
    local fail_count=0
    local warn_count=0
    local skip_count=0

    # Start JSON structure
    local checks_json=""

    for check_func in check_network_exposure check_token_security check_deny_commands check_tcc_permissions check_icloud_sync check_workspace_privacy check_network_connections check_logs; do
        local check_name=$(echo "$check_func" | sed 's/check_//g' | sed 's/_/ /g')
        local result=$($check_func)
        local status=$(echo "$result" | cut -d'|' -f1)
        local details=$(echo "$result" | cut -d'|' -f2-)

        # Escape special characters in details for JSON
        details=$(echo "$details" | sed 's/"/\\"/g' | sed 's/\\/\\\\/g')

        # Build checks JSON
        if [ -n "$checks_json" ]; then
            checks_json="${checks_json},"
        fi
        checks_json="${checks_json}\"$check_name\": {\"status\": \"$status\", \"details\": \"$details\"}"

        case $status in
            PASS) ((pass_count++)) ;;
            FAIL) ((fail_count++)) ;;
            WARN) ((warn_count++)) ;;
            SKIP) ((skip_count++)) ;;
        esac
    done

    # Generate JSON
    cat > "$report_file" << EOF
{
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "summary": {
        "total": $((pass_count + fail_count + warn_count)),
        "passed": $pass_count,
        "failed": $fail_count,
        "warnings": $warn_count,
        "skipped": $skip_count
    },
    "checks": {
        $checks_json
    }
}
EOF

    print_success "JSON report generated: $report_file"
}

# =============================================================================
# Main
# =============================================================================

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -f|--format)
            OUTPUT_FORMAT="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -q|--quick)
            QUICK_MODE=true
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Generate report
echo "========================================"
echo "  OpenClaw Security Audit Report Generator"
echo "========================================"
echo ""
echo "Format: $OUTPUT_FORMAT"
echo "Output: $OUTPUT_DIR"
echo ""

if [ "$OUTPUT_FORMAT" = "html" ]; then
    generate_html_report
else
    generate_json_report
fi

echo ""
print_success "Report generation complete!"
