#!/bin/bash
# =============================================================================
# OpenClaw Security Audit - System Security Checks
# =============================================================================
# Description: macOS system-level security checks (Firewall, FileVault, SIP)
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

print_skip() {
    echo -e "${BLUE}[⏭ SKIP]${NC} $1"
}

# =============================================================================
# System Security Checks
# =============================================================================

check_firewall() {
    echo "========================================"
    echo "  1. Firewall Check"
    echo "========================================"
    echo ""

    # Global firewall state
    local global_state=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null)
    echo "Firewall Status: $global_state"

    # Explain what this check does
    echo ""
    echo "📌 这个检查项的作用:"
    echo "   防火墙阻止未授权的网络连接，保护 Mac 免受外部攻击"
    echo ""

    if [ "$global_state" = "Firewall is enabled. (State = 1)" ]; then
        print_success "防火墙已开启"
    else
        print_warning "防火墙未开启"
        echo ""
        echo "⚡ 对您的实际影响:"
        echo ""
        echo "   ┌─────────────────────────────────────────────────────┐"
        echo "   │ 使用场景                              │ 风险程度 │"
        echo "   ├─────────────────────────────────────────────────────┤"
        echo "   │ Mac 仅在内网使用                    │ 🟢 较低  │"
        echo "   │ 经常连接公共 WiFi（咖啡厅/酒店）     │ 🟠 较高  │"
        echo "   │ 运行对外服务（Web服务器/数据库）      │ 🔴 很高  │"
        echo "   │ 已有路由器/企业防火墙保护          │ 🟢 可接受│"
        echo "   └─────────────────────────────────────────────────────┘"
        echo ""
        echo "💡 建议:"
        echo "   等级: 【推荐】(非强制)"
        echo ""
        echo "   • 如果您经常外出使用公共网络，建议开启"
        echo "   • 如果 Mac 固定在安全内网环境，可以保持关闭"
        echo "   • 开启命令:"
        echo "     sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on"
    fi

    echo ""

    # Check stealth mode
    local stealth_mode=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode 2>/dev/null)
    echo "Stealth Mode: $stealth_mode"

    if [ "$stealth_mode" = "Stealth mode enabled" ]; then
        print_success "隐身模式已开启（Mac 不会响应 ping 请求）"
    else
        print_info "隐身模式未开启（Mac 会响应 ping，可能被发现）"
        echo ""
        echo "💡 隐身模式可以让您的 Mac 在网络上\"不可见\""
        echo "   如果不需要隐藏设备存在，可以不开启"
    fi

    echo ""

    # List allowed apps
    echo "Allowed Applications (first 20):"
    /usr/libexec/ApplicationFirewall/socketfilterfw --listapps 2>/dev/null | head -20

    echo ""
}

check_filevault() {
    echo "========================================"
    echo "  2. FileVault Encryption Check"
    echo "========================================"
    echo ""

    # Check FileVault status
    local fv_status=$(fdesetup -status 2>/dev/null)

    echo "FileVault Status: $fv_status"
    echo ""

    # Explain what this check means
    echo "📌 这个检查项的作用:"
    echo "   FileVault 是 macOS 的磁盘加密功能，防止硬盘被盗/丢失后他人读取数据"
    echo ""

    if echo "$fv_status" | grep -q "FileVault is On"; then
        print_success "FileVault 已开启"

        # Check if using secure key
        local fv_info=$(diskutil info / 2>/dev/null | grep -A5 "FileVault")
        echo ""
        echo "加密详情:"
        echo "$fv_info"
    else
        print_warning "FileVault 未开启"
        echo ""
        echo "⚡ 对您的实际影响:"
        echo ""
        echo "   ┌─────────────────────────────────────────────────────┐"
        echo "   │ 使用场景                              │ 风险程度 │"
        echo "   ├─────────────────────────────────────────────────────┤"
        echo "   │ Mac 固定在安全场所（办公室/家中）      │ 🟢 较低  │"
        echo "   │ 经常携带外出（咖啡厅/出差）            │ 🟠 较高  │"
        echo "   │ 存储敏感数据（财务/客户信息）          │ 🔴 很高  │"
        echo "   │ 需要远程重启控制（SSH/远程管理）       │ ⚪ 可接受│"
        echo "   └─────────────────────────────────────────────────────┘"
        echo ""
        echo "💡 建议:"
        echo "   等级: 【可选】(根据实际场景决定)"
        echo ""
        echo "   • 如果您是因为远程控制需求而关闭 FileVault，这是合理的选择"
        echo "   • 可以通过其他方式补偿风险："
        echo "     - 确保物理安全（Mac 放在安全地点）"
        echo "     - 定期备份重要数据"
        echo "     - 使用强密码保护账户"
        echo ""
        echo "   • 如果需要开启 FileVault:"
        echo "     系统偏好设置 > 安全性与隐私 > FileVault > 开启 FileVault"
    fi

    echo ""
}

check_sip() {
    echo "========================================"
    echo "  3. SIP (System Integrity Protection) Check"
    echo "========================================"
    echo ""

    # Check SIP status
    local sip_status=$(csrutil status 2>/dev/null)

    echo "SIP Status: $sip_status"

    # Explain what this check does
    echo ""
    echo "📌 这个检查项的作用:"
    echo "   SIP 保护 macOS 系统核心文件不被修改，防止恶意软件获取系统权限"
    echo ""

    if echo "$sip_status" | grep -q "enabled"; then
        print_success "SIP 已开启"

        # Check specific protections
        echo ""
        echo "Protection Details:"
        csrutil status 2>/dev/null | grep -E "(enabled|disabled)" | while read line; do
            echo "  $line"
        done
    else
        print_warning "SIP 已关闭"
        echo ""
        echo "⚡ 对您的实际影响:"
        echo ""
        echo "   ┌─────────────────────────────────────────────────────┐"
        echo "   │ 使用场景                              │ 风险程度 │"
        echo "   ├─────────────────────────────────────────────────────┤"
        echo "   │ 日常使用（浏览/办公）              │ 🟢 较低  │"
        echo "   │ 安装来源不明的软件                │ 🟠 较高  │"
        echo "   │ 开发调试（需要调试系统组件）        │ ⚪ 可接受│"
        echo "   │ 运行需要 SIP 关闭的工具            │ ⚪ 可接受│"
        echo "   └─────────────────────────────────────────────────────┘"
        echo ""
        echo "💡 建议:"
        echo "   等级: 【建议开启】(除非有特殊需求)"
        echo ""
        echo "   • 如果您是因为开发/调试需要而关闭 SIP，这是合理的选择"
        echo "   • 关闭 SIP 时请注意："
        echo "     - 只安装可信来源的软件"
        echo "     - 完成调试后尽快重新开启"
        echo "   • 重新开启 SIP:"
        echo "     1. 重启 Mac 进入恢复模式 (按住 Cmd+R)"
        echo "     2. 打开终端"
        echo "     3. 运行: csrutil enable"
        echo "     4. 重启"
    fi

    echo ""
}

check_gatekeeper() {
    echo "========================================"
    echo "  4. Gatekeeper Check"
    echo "========================================"
    echo ""

    # Check Gatekeeper status
    local gk_status=$(spctl --status 2>/dev/null)

    echo "Gatekeeper Status: $gk_status"

    # Explain what this check does
    echo ""
    echo "📌 这个检查项的作用:"
    echo "   Gatekeeper 阻止未经验证的应用运行，防止恶意软件感染"
    echo ""

    if echo "$gk_status" | grep -q "assessments enabled"; then
        print_success "Gatekeeper 已开启"

        echo ""
        echo "✅ 只有经过 Apple 公证或您明确允许的应用才能运行"
    else
        print_warning "Gatekeeper 已关闭"

        echo ""
        echo "⚡ 对您的实际影响:"
        echo ""
        echo "   ┌─────────────────────────────────────────────────────┐"
        echo "   │ 使用场景                              │ 风险程度 │"
        echo "   ├─────────────────────────────────────────────────────┤"
        echo "   │ 只从 App Store 或官网下载软件        │ 🟢 较低  │"
        echo "   │ 经常安装第三方/开源软件              │ 🟠 较高  │"
        echo "   │ 开发测试未签名应用                  │ ⚪ 可接受│"
        echo "   │ 已关闭 SIP 进行系统调试              │ ⚪ 可接受│"
        echo "   └─────────────────────────────────────────────────────┘"
        echo ""
        echo "💡 建议:"
        echo "   等级: 【建议开启】(非强制)"
        echo ""
        echo "   • 如果您经常测试未签名应用，关闭 Gatekeeper 是合理的"
        echo "   • 关闭时请注意："
        echo "     - 只运行可信来源的软件"
        echo "     - 安装前先扫描病毒"
        echo "   • 重新开启命令:"
        echo "     sudo spctl --master-enable"
    fi

    echo ""

    # Check for quarantined apps
    echo "Recent Quarantine Events (最近隔离的应用):"
    xattr -l ~/Downloads/* 2>/dev/null | grep -A2 "com.apple.quarantine" | head -10

    echo ""
}

check_secure_boot() {
    echo "========================================"
    echo "  5. Secure Boot Check (Apple Silicon)"
    echo "========================================"
    echo ""

    # Check if Apple Silicon
    local chip_type=$(sysctl -n machdep.cpu.brand_string 2>/dev/null)

    if echo "$chip_type" | grep -q "Apple"; then
        echo "Chip: $chip_type"

        # Check secure boot policy
        local sb_policy=$(systemsetup -getsecureboot 2>/dev/null)

        if [ -n "$sb_policy" ]; then
            echo "Secure Boot Policy: $sb_policy"

            if echo "$sb_policy" | grep -qi "full"; then
                print_success "Full Security enabled"
            elif echo "$sb_policy" | grep -qi "reduced"; then
                print_warning "Reduced Security"
            else
                print_warning "Permissive Security"
            fi
        else
            print_info "Secure boot status not available"
        fi
    else
        print_info "Intel-based Mac - Secure Boot not applicable"
    fi

    echo ""
}

# =============================================================================
# Main
# =============================================================================

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --all           Run all system security checks"
    echo "  --firewall      Check firewall status"
    echo "  --filevault     Check FileVault encryption"
    echo "  --sip           Check System Integrity Protection"
    echo "  --gatekeeper    Check Gatekeeper status"
    echo "  --secure-boot   Check Secure Boot (Apple Silicon)"
    echo "  -h, --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --all"
    echo "  $0 --firewall --filevault"
}

# Parse arguments
RUN_ALL=false
RUN_FIREWALL=false
RUN_FILEVAULT=false
RUN_SIP=false
RUN_GATEKEEPER=false
RUN_SECURE_BOOT=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --all)
            RUN_ALL=true
            shift
            ;;
        --firewall)
            RUN_FIREWALL=true
            shift
            ;;
        --filevault)
            RUN_FILEVAULT=true
            shift
            ;;
        --sip)
            RUN_SIP=true
            shift
            ;;
        --gatekeeper)
            RUN_GATEKEEPER=true
            shift
            ;;
        --secure-boot)
            RUN_SECURE_BOOT=true
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

# If no specific checks selected, run all
if [ "$RUN_FIREWALL" = false ] && [ "$RUN_FILEVAULT" = false ] && [ "$RUN_SIP" = false ] && [ "$RUN_GATEKEEPER" = false ] && [ "$RUN_SECURE_BOOT" = false ]; then
    RUN_ALL=true
fi

echo "========================================"
echo "  macOS System Security Check"
echo "========================================"
echo ""

ERRORS=0

if [ "$RUN_ALL" = true ] || [ "$RUN_FIREWALL" = true ]; then
    check_firewall
fi

if [ "$RUN_ALL" = true ] || [ "$RUN_FILEVAULT" = true ]; then
    check_filevault
fi

if [ "$RUN_ALL" = true ] || [ "$RUN_SIP" = true ]; then
    check_sip
fi

if [ "$RUN_ALL" = true ] || [ "$RUN_GATEKEEPER" = true ]; then
    check_gatekeeper
fi

if [ "$RUN_ALL" = true ] || [ "$RUN_SECURE_BOOT" = true ]; then
    check_secure_boot
fi

# Summary
echo "========================================"
echo "  System Security Summary"
echo "========================================"
echo ""

print_success "System security check complete"
echo ""
echo "Run full OpenClaw audit: ./scripts/generate-report.sh --format html"
