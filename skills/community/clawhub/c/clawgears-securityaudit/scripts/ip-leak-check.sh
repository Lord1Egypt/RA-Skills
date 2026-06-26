#!/bin/bash
# =============================================================================
# OpenClaw Security Audit - IP Leak Check
# =============================================================================
# Description: Check if your IP is exposed on openclaw.allegro.earth
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

# Configuration
ALLEGRO_URL="https://openclaw.allegro.earth"
HISTORY_DIR="$(dirname "$0")/../history"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# =============================================================================
# Helper Functions
# =============================================================================

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✅ PASS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠️ WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[❌ FAIL]${NC} $1"
}

# =============================================================================
# IP Leak Check Functions
# =============================================================================

get_public_ip() {
    # Try multiple IP detection services
    local ip=""

    # Method 1: ipify
    ip=$(curl -s https://api.ipify.org 2>/dev/null)
    if [ -n "$ip" ]; then
        echo "$ip"
        return
    fi

    # Method 2: icanhazip
    ip=$(curl -s https://icanhazip.com 2>/dev/null)
    if [ -n "$ip" ]; then
        echo "$ip"
        return
    fi

    # Method 3: ifconfig.me
    ip=$(curl -s https://ifconfig.me/ip 2>/dev/null)
    if [ -n "$ip" ]; then
        echo "$ip"
        return
    fi

    echo "unknown"
}

check_allegro_exposure() {
    local public_ip="$1"

    echo "========================================"
    echo "  Checking openclaw.allegro.earth"
    echo "========================================"
    echo ""

    if [ "$public_ip" = "unknown" ]; then
        print_error "Cannot determine public IP"
        return 1
    fi

    echo "Your Public IP: $public_ip"
    echo ""
    echo "Checking if your IP is in the exposure database..."
    echo ""

    # Query the allegro.earth database
    local result=$(curl -s "${ALLEGRO_URL}/api/check?ip=${public_ip}" 2>/dev/null)

    if [ -z "$result" ]; then
        # Fallback: search the web page
        local page_content=$(curl -s "${ALLEGRO_URL}" 2>/dev/null | grep -i "$public_ip" || true)

        if [ -n "$page_content" ] && echo "$page_content" | grep -q "$public_ip"; then
            print_error "YOUR IP IS EXPOSED!"
            echo ""
            echo "⚠️  CRITICAL SECURITY ALERT"
            echo ""
            echo "Your IP ($public_ip) appears in the OpenClaw exposure database."
            echo ""
            echo "This means your OpenClaw instance may be:"
            echo "  - Accessible from the public internet"
            echo "  - Vulnerable to attacks"
            echo "  - Potentially leaking API keys"
            echo ""
            echo "IMMEDIATE ACTIONS REQUIRED:"
            echo "  1. Close public access immediately"
            echo "  2. Enable authentication"
            echo "  3. Regenerate API keys"
            echo "  4. Check for unauthorized usage"
            echo ""
            return 1
        fi
    fi

    # Parse JSON result if available
    if echo "$result" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('exposed', False))" 2>/dev/null | grep -q "True"; then
        print_error "YOUR IP IS EXPOSED!"
        echo ""
        echo "⚠️  CRITICAL SECURITY ALERT"
        echo ""
        echo "Your IP ($public_ip) appears in the OpenClaw exposure database."
        echo ""
        echo "IMMEDIATE ACTIONS REQUIRED:"
        echo "  1. Close public access immediately"
        echo "  2. Enable authentication"
        echo "  3. Regenerate API keys"
        echo "  4. Check for unauthorized usage"
        echo ""
        return 1
    fi

    print_success "Your IP is NOT in the exposure database"
    echo ""
    echo "However, you should still:"
    echo "  - Verify Gateway is not exposed (0.0.0.0 binding)"
    echo "  - Ensure authentication is enabled"
    echo "  - Use strong, unique tokens"
    echo ""
    return 0
}

check_port_exposure() {
    echo "========================================"
    echo "  Checking Port Exposure"
    echo "========================================"
    echo ""

    # Check common OpenClaw ports
    local ports=(18789 8080 3000 5000)
    local exposed_ports=()

    for port in "${ports[@]}"; do
        local listener=$(lsof -i :$port 2>/dev/null | grep LISTEN || true)
        if [ -n "$listener" ]; then
            local bind_addr=$(echo "$listener" | awk '{print $NF}' | head -1)
            if echo "$bind_addr" | grep -q "0.0.0.0\|\*"; then
                exposed_ports="$exposed_ports $port"
                print_error "Port $port is exposed (0.0.0.0)"
            else
                print_success "Port $port is safely bound ($bind_addr)"
            fi
        fi
    done

    if [ -n "$exposed_ports" ]; then
        echo ""
        print_error "EXPOSED PORTS: $exposed_ports"
        return 1
    fi

    return 0
}

check_censys_exposure() {
    local public_ip="$1"

    echo "========================================"
    echo "  Checking Censys Database"
    echo "========================================"
    echo ""

    if [ "$public_ip" = "unknown" ]; then
        print_warning "Cannot check Censys without public IP"
        return 0
    fi

    echo "Your Public IP: $public_ip"
    echo ""
    print_info "Censys 是互联网扫描数据库，记录了所有暴露在公网的服务"
    echo ""
    echo "请访问以下链接检查您的 IP 是否被扫描到："
    echo ""
    echo "  🔗 https://search.censys.io/hosts/$public_ip"
    echo ""
    echo "如果显示您的 OpenClaw 端口 (18789) 或其他敏感服务，"
    echo "说明您的 IP 已被收录到公网扫描数据库中。"
    echo ""
    print_warning "建议手动检查上述链接"
    echo ""

    return 0
}

check_shodan_exposure() {
    local public_ip="$1"

    echo "========================================"
    echo "  Checking Shodan Database"
    echo "========================================"
    echo ""

    if [ "$public_ip" = "unknown" ]; then
        print_warning "Cannot check Shodan without public IP"
        return 0
    fi

    echo "Your Public IP: $public_ip"
    echo ""
    print_info "Shodan 是另一个互联网扫描数据库"
    echo ""
    echo "请访问以下链接检查您的 IP："
    echo ""
    echo "  🔗 https://www.shodan.io/host/$public_ip"
    echo ""
    print_warning "建议手动检查上述链接"
    echo ""

    return 0
}

save_leak_check_result() {
    local ip="$1"
    local exposed="$2"
    local result_file="$HISTORY_DIR/leak-check-$TIMESTAMP.json"

    mkdir -p "$HISTORY_DIR" 2>/dev/null

    cat > "$result_file" << EOF
{
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "public_ip": "$ip",
    "exposed": $exposed,
    "ports_checked": [18789, 8080, 3000, 5000],
    "databases_checked": [
        {
            "name": "openclaw.allegro.earth",
            "url": "https://openclaw.allegro.earth",
            "description": "OpenClaw exposure database"
        },
        {
            "name": "Censys",
            "url": "https://search.censys.io/hosts/$ip",
            "description": "Internet-wide scanning database"
        },
        {
            "name": "Shodan",
            "url": "https://www.shodan.io/host/$ip",
            "description": "IoT and service scanning database"
        }
    ],
    "recommendations": [
        "Keep Gateway binding to loopback",
        "Enable authentication with strong tokens",
        "Regularly check openclaw.allegro.earth",
        "Monitor network connections",
        "Check Censys and Shodan for IP exposure"
    ]
}
EOF

    print_info "Result saved: $result_file"
}

# =============================================================================
# Main
# =============================================================================

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --ip <IP>       Check specific IP address"
    echo "  --ports         Check port exposure"
    echo "  --all           Run all leak checks"
    echo "  -h, --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --all"
    echo "  $0 --ip 1.2.3.4"
    echo "  $0 --ports"
}

# Parse arguments
CHECK_IP=""
CHECK_PORTS=false
CHECK_ALL=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --ip)
            CHECK_IP="$2"
            shift 2
            ;;
        --ports)
            CHECK_PORTS=true
            shift
            ;;
        --all)
            CHECK_ALL=true
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

# Default to all checks if no specific option
if [ "$CHECK_IP" = "" ] && [ "$CHECK_PORTS" = false ]; then
    CHECK_ALL=true
fi

echo "========================================"
echo "  OpenClaw IP Leak Check"
echo "========================================"
echo ""

ERRORS=0

# Get public IP
if [ "$CHECK_IP" = "" ]; then
    CHECK_IP=$(get_public_ip)
fi

# Run checks
if [ "$CHECK_ALL" = true ] || [ -n "$CHECK_IP" ]; then
    check_allegro_exposure "$CHECK_IP"
    RESULT=$?
    if [ $RESULT -ne 0 ]; then
        ((ERRORS++))
    fi
    echo ""
    check_censys_exposure "$CHECK_IP"
    echo ""
    check_shodan_exposure "$CHECK_IP"
    echo ""
fi

if [ "$CHECK_ALL" = true ] || [ "$CHECK_PORTS" = true ]; then
    check_port_exposure
    RESULT=$?
    if [ $RESULT -ne 0 ]; then
        ((ERRORS++))
    fi
    echo ""
fi
# Save result
save_leak_check_result "$CHECK_IP" "$ERRORS"

# Summary
echo "========================================"
echo "  Leak Check Summary"
echo "========================================"
echo ""

if [ $ERRORS -gt 0 ]; then
    print_error "Found $ERRORS exposure(s)!"
    echo ""
    echo "🚨 IMMEDIATE ACTION REQUIRED"
    echo ""
    echo "1. Close public access: Change Gateway bind to loopback"
    echo "2. Enable authentication: Add strong token"
    echo "3. Regenerate keys: Create new API keys"
    echo "4. Check usage: Review API usage logs"
    echo ""
    echo "Run fix: ./scripts/fix-exposed-gateway.sh --all"
    exit 1
else
    print_success "No exposure detected"
    echo ""
    echo "Continue to monitor regularly and maintain security best practices."
    exit 0
fi
