#!/bin/bash
# =============================================================================
# OpenClaw Security Audit - Quick Check Mode
# =============================================================================
# Description: Quick security check for critical items only
# Author: Winnie.C
# Version: 1.1.0
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

# =============================================================================
# Helper Functions
# =============================================================================

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✅ 通过]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠️ 警告]${NC} $1"
}

print_error() {
    echo -e "${RED}[❌ 风险]${NC} $1"
}

print_skip() {
    echo -e "${BLUE}[⏭ 跳过]${NC} $1"
}

# =============================================================================
# Quick Check Functions (Critical Items Only)
# =============================================================================

check_network_exposure() {
    echo ""
    echo "========================================"
    echo "  1. Gateway 网络暴露检查"
    echo "========================================"
    echo ""

    # Check Gateway port binding
    local gateway_bind=$(lsof -i :18789 2>/dev/null | grep "LISTEN" || true)

    echo "📌 这个检查项的作用:"
    echo "   检查 OpenClaw Gateway 是否暴露在公网，防止他人访问您的 AI 助手"
    echo ""

    if [ -z "$gateway_bind" ]; then
        print_info "Gateway 未运行"
        echo ""
        echo "💡 如果您当前没有使用 OpenClaw，这是正常状态"
        return 0
    fi

    echo "Gateway 绑定状态: $gateway_bind"
    echo ""

    if echo "$gateway_bind" | grep -q "0.0.0.0\|\*"; then
        print_error "Gateway 暴露在公网 (0.0.0.0:18789)"
        echo ""
        echo "⚡ 对您的实际影响:"
        echo ""
        echo "   ┌─────────────────────────────────────────────────────┐"
        echo "   │ 风险: 互联网上任何人都可以访问您的 AI 助手        │"
        echo "   │ 后果: API 密钥被盗用、产生意外费用、隐私泄露      │"
        echo "   └─────────────────────────────────────────────────────┘"
        echo ""
        echo "💡 建议:"
        echo "   等级: 【🔴 必须修复】"
        echo ""
        echo "   • 这是严重的安全风险，强烈建议立即修复"
        echo "   • 修复方法: 运行 ./scripts/interactive-fix.sh --bind"
        return 1
    fi

    if echo "$gateway_bind" | grep -q "127.0.0.1\|localhost"; then
        print_success "Gateway 安全绑定在本地 (127.0.0.1)"
        echo ""
        echo "✅ 您的 Gateway 只能从本机访问，是安全的"
        return 0
    else
        print_warning "Gateway 绑定状态: $gateway_bind"
        echo ""
        echo "💡 请确认这是您预期的配置"
        return 2
    fi
}

check_token_security() {
    echo ""
    echo "========================================"
    echo "  2. Token 安全检查"
    echo "========================================"
    echo ""

    local config_path="$HOME/.openclaw/openclaw.json"

    echo "📌 这个检查项的作用:"
    echo "   检查 API Token 强度，防止被暴力破解或猜测"
    echo ""

    if [ ! -f "$config_path" ]; then
        print_info "配置文件不存在"
        echo ""
        echo "💡 如果您还没有配置 OpenClaw，这是正常状态"
        return 0
    fi

    local token_info=$(python3 -c "
import json
try:
    with open('$config_path') as f:
        cfg = json.load(f)
        token = cfg.get('gateway', {}).get('auth', {}).get('token', '')
        mode = cfg.get('gateway', {}).get('mode', 'unknown')
        print(f'{len(token)}|{mode}')
except:
    print('error|error')
" 2>/dev/null)

    local token_length=$(echo "$token_info" | cut -d'|' -f1)
    local mode=$(echo "$token_info" | cut -d'|' -f2)

    if [ "$token_length" = "error" ]; then
        print_error "无法读取配置"
        return 1
    fi

    echo "Token 长度: $token_length 字符"
    echo "运行模式: $mode"
    echo ""

    if [ "$token_length" -lt 40 ]; then
        print_error "Token 太短 ($token_length 字符，建议 >= 40)"
        echo ""
        echo "⚡ 对您的实际影响:"
        echo ""
        echo "   ┌─────────────────────────────────────────────────────┐"
        echo "   │ Token 长度      │ 破解难度       │ 适用场景         │"
        echo "   ├─────────────────────────────────────────────────────┤"
        echo "   │ < 20 字符       │ 🔴 几分钟      │ ❌ 不推荐        │"
        echo "   │ 20-39 字符      │ 🟠 几小时-几天 │ ⚠️ 临时测试可用  │"
        echo "   │ 40-63 字符      │ 🟢 几年        │ ✅ 推荐用于生产  │"
        echo "   │ >= 64 字符      │ 💚 几乎不可能  │ ✅ 最佳实践      │"
        echo "   └─────────────────────────────────────────────────────┘"
        echo ""
        echo "💡 建议:"
        echo "   等级: 【🟠 建议修复】"
        echo ""
        echo "   • 如果只是临时测试，短 Token 可以接受"
        echo "   • 如果长期使用或暴露在公网，建议使用强 Token"
        echo "   • 生成新 Token: ./scripts/interactive-fix.sh --token"
        return 1
    fi

    if [ "$mode" != "local" ]; then
        print_warning "运行模式为 '$mode' (建议使用 'local')"
        echo ""
        echo "💡 如果您需要远程访问，请确保网络环境安全"
        return 2
    fi

    print_success "Token 强度足够 ($token_length 字符)"
    echo ""
    echo "✅ 您的 Token 强度符合安全要求"
    return 0
}

check_deny_commands() {
    echo ""
    echo "========================================"
    echo "  3. 敏感命令防护检查"
    echo "========================================"
    echo ""

    local config_path="$HOME/.openclaw/openclaw.json"

    echo "📌 这个检查项的作用:"
    echo "   检查是否阻止了摄像头、屏幕截图等敏感操作，防止隐私泄露"
    echo ""

    if [ ! -f "$config_path" ]; then
        print_info "配置文件不存在"
        return 0
    fi

    local deny_list=$(python3 -c "
import json
try:
    with open('$config_path') as f:
        cfg = json.load(f)
        deny = cfg.get('gateway', {}).get('nodes', {}).get('denyCommands', [])
        print('|'.join(deny) if deny else '')
except:
    print('')
" 2>/dev/null)

    echo "当前已阻止的命令: ${deny_list:-无}"
    echo ""

    local critical_deny=("screencapture" "camera.snap" "camera.clip" "screen.record" "osascript")
    local missing=()

    for cmd in "${critical_deny[@]}"; do
        if ! echo "|$deny_list|" | grep -q "$cmd"; then
            missing+=("$cmd")
        fi
    done

    if [ ${#missing[@]} -gt 0 ]; then
        print_warning "以下敏感命令未被阻止: ${missing[*]}"
        echo ""
        echo "⚡ 对您的实际影响:"
        echo ""
        echo "   ┌─────────────────────────────────────────────────────┐"
        echo "   │ 命令              │ 可能造成的风险                   │"
        echo "   ├─────────────────────────────────────────────────────┤"
        echo "   │ screencapture    │ AI 可以截取您的屏幕              │"
        echo "   │ camera.snap      │ AI 可以调用摄像头拍照            │"
        echo "   │ screen.record    │ AI 可以录制屏幕                  │"
        echo "   │ osascript        │ AI 可以执行 AppleScript (强大)   │"
        echo "   └─────────────────────────────────────────────────────┘"
        echo ""
        echo "💡 建议:"
        echo "   等级: 【🟠 建议修复】"
        echo ""
        echo "   • 如果您信任 AI 助手且需要这些功能，可以不阻止"
        echo "   • 如果担心隐私泄露，建议添加到阻止列表"
        echo "   • 修复方法: ./scripts/interactive-fix.sh --deny"
        return 1
    fi

    print_success "所有敏感命令已阻止"
    echo ""
    echo "✅ 您的 AI 助手无法执行摄像头/屏幕截图等敏感操作"
    return 0
}

check_fda_permission() {
    echo ""
    echo "========================================"
    echo "  4. Full Disk Access (FDA) 权限检查"
    echo "========================================"
    echo ""

    echo "📌 这个检查项的作用:"
    echo "   检查 AI 助手是否拥有\"完全磁盘访问\"权限，这可能让它读取所有文件"
    echo ""

    local fda_status=$(python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('/Library/Application Support/com.apple.TCC/TCC.db')
    cursor = conn.cursor()
    cursor.execute('SELECT auth_value FROM access WHERE client LIKE \"%node%\" AND service=\"kTCCServiceSystemPolicyAllFiles\"')
    r = cursor.fetchone()
    print('granted' if r and r[0]==1 else 'not_granted')
    conn.close()
except:
    print('unknown')
" 2>/dev/null)

    case $fda_status in
        "granted")
            print_warning "FDA 已授权"
            echo ""
            echo "⚡ 对您的实际影响:"
            echo ""
            echo "   ┌─────────────────────────────────────────────────────┐"
            echo "   │ FDA 授权意味着 AI 助手可以:                       │"
            echo "   │  • 读取所有文件（包括邮件、消息、浏览历史）       │"
            echo "   │  • 访问其他应用的私有数据                         │"
            echo "   │  • 读取敏感配置文件                               │"
            echo "   └─────────────────────────────────────────────────────┘"
            echo ""
            echo "💡 建议:"
            echo "   等级: 【🟡 评估后决定】"
            echo ""
            echo "   • 如果您确实需要 AI 访问全盘文件（如文件整理、代码分析），这是合理的"
            echo "   • 如果只是日常对话，不需要 FDA，建议关闭"
            echo "   • 替代方案: 只授予特定文件夹的访问权限"
            echo "   • 关闭方法: 系统偏好设置 > 隐私与安全性 > 完全磁盘访问"
            return 1
            ;;
        "not_granted")
            print_success "FDA 未授权"
            echo ""
            echo "✅ 您的 AI 助手只能访问您明确允许的文件"
            return 0
            ;;
        *)
            print_info "无法检查 FDA 状态（需要管理员权限）"
            echo ""
            echo "💡 您可以手动检查: 系统偏好设置 > 隐私与安全性 > 完全磁盘访问"
            return 2
            ;;
    esac
}

check_firewall() {
    echo ""
    echo "========================================"
    echo "  5. 防火墙状态检查"
    echo "========================================"
    echo ""

    echo "📌 这个检查项的作用:"
    echo "   检查 macOS 防火墙是否开启，阻止未授权的网络连接"
    echo ""

    local fw_status=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null)

    echo "防火墙状态: $fw_status"
    echo ""

    if [ "$fw_status" = "enabled" ]; then
        print_success "防火墙已开启"
        echo ""
        echo "✅ 您的 Mac 受到防火墙保护"
        return 0
    else
        print_info "防火墙未开启"
        echo ""
        echo "⚡ 对您的实际影响:"
        echo ""
        echo "   ┌─────────────────────────────────────────────────────┐"
        echo "   │ 使用场景                              │ 风险程度 │"
        echo "   ├─────────────────────────────────────────────────────┤"
        echo "   │ Mac 固定在安全内网                  │ 🟢 较低  │"
        echo "   │ 经常连接公共 WiFi                   │ 🟠 较高  │"
        echo "   │ 已有路由器/企业防火墙保护            │ 🟢 可接受│"
        echo "   │ 运行需要开放端口的服务               │ ⚪ 按需   │"
        echo "   └─────────────────────────────────────────────────────┘"
        echo ""
        echo "💡 建议:"
        echo "   等级: 【🟢 可选】(根据场景决定)"
        echo ""
        echo "   • 如果 Mac 固定在安全场所，防火墙可以不开启"
        echo "   • 如果经常外出使用公共网络，建议开启"
        echo "   • 开启命令: sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on"
        return 2
    fi
}

# =============================================================================
# Main
# =============================================================================

show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --verbose    Show detailed explanations"
    echo "  --json       Output in JSON format"
    echo "  -h, --help   Show this help message"
    echo ""
    echo "This script checks 5 critical security items:"
    echo "  1. Gateway network exposure"
    echo "  2. Token strength"
    echo "  3. Sensitive command protection"
    echo "  4. Full Disk Access permission"
    echo "  5. Firewall status"
}

# Parse arguments
VERBOSE=false
JSON_OUTPUT=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --verbose)
            VERBOSE=true
            shift
            ;;
        --json)
            JSON_OUTPUT=true
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

echo "========================================"
echo "  OpenClaw 快速安全检查"
echo "========================================"

ERRORS=0
WARNINGS=0

# Run checks
check_network_exposure
RESULT=$?
if [ $RESULT -eq 1 ]; then ((ERRORS++)); fi

check_token_security
RESULT=$?
if [ $RESULT -eq 1 ]; then ((ERRORS++)); fi
if [ $RESULT -eq 2 ]; then ((WARNINGS++)); fi

check_deny_commands
RESULT=$?
if [ $RESULT -eq 1 ]; then ((WARNINGS++)); fi

check_fda_permission
RESULT=$?
if [ $RESULT -eq 1 ]; then ((WARNINGS++)); fi

check_firewall
RESULT=$?
if [ $RESULT -eq 2 ]; then ((WARNINGS++)); fi

# Summary
echo ""
echo "========================================"
echo "  检查摘要"
echo "========================================"
echo ""

if [ $ERRORS -gt 0 ]; then
    print_error "发现 $ERRORS 个高风险项需要处理"
    echo ""
    echo "🚨 建议立即运行: ./scripts/interactive-fix.sh --all"
elif [ $WARNINGS -gt 0 ]; then
    print_warning "发现 $WARNINGS 个建议关注的项"
    echo ""
    echo "📋 请根据您的实际使用场景决定是否需要修复"
else
    print_success "所有检查项均通过！"
    echo ""
    echo "✅ 您的 OpenClaw 配置是安全的"
fi

echo ""
