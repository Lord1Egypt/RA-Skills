#!/bin/bash
# Clash VPN 管理脚本
# 用于启动、停止、更新配置的便捷工具

CLASH_CONFIG="/root/.config/clash/config.yaml"
CLASH_LOG="/var/log/clash.log"
CLASH_BIN="/usr/local/bin/clash"

show_help() {
    echo "Clash VPN 管理脚本"
    echo ""
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  start       启动 Clash VPN"
    echo "  stop        停止 Clash VPN"
    echo "  restart     重启 Clash VPN"
    echo "  status      查看运行状态"
    echo "  update      更新配置文件"
    echo "  test        测试代理连接"
    echo "  help        显示帮助信息"
    echo ""
    echo "代理地址:"
    echo "  HTTP:  http://127.0.0.1:7890"
    echo "  SOCKS: socks5://127.0.0.1:7891"
}

start_clash() {
    if pgrep -x "clash" > /dev/null; then
        echo "Clash 已经在运行"
        return 0
    fi
    
    if [ ! -f "$CLASH_CONFIG" ]; then
        echo "错误: 配置文件不存在: $CLASH_CONFIG"
        echo "请先更新配置"
        return 1
    fi
    
    nohup "$CLASH_BIN" -f "$CLASH_CONFIG" > "$CLASH_LOG" 2>&1 &
    sleep 2
    
    if pgrep -x "clash" > /dev/null; then
        echo "Clash 启动成功"
        echo "HTTP 代理: http://127.0.0.1:7890"
        echo "SOCKS 代理: socks5://127.0.0.1:7891"
    else
        echo "Clash 启动失败，查看日志: $CLASH_LOG"
        return 1
    fi
}

stop_clash() {
    if ! pgrep -x "clash" > /dev/null; then
        echo "Clash 未在运行"
        return 0
    fi
    
    pkill -x clash
    sleep 1
    
    if ! pgrep -x "clash" > /dev/null; then
        echo "Clash 已停止"
    else
        echo "Clash 停止失败"
        return 1
    fi
}

restart_clash() {
    stop_clash
    sleep 1
    start_clash
}

show_status() {
    if pgrep -x "clash" > /dev/null; then
        echo "Clash 运行状态: 运行中"
        echo ""
        echo "代理地址:"
        echo "  HTTP:  http://127.0.0.1:7890"
        echo "  SOCKS: socks5://127.0.0.1:7891"
        echo ""
        echo "配置文件: $CLASH_CONFIG"
        echo "日志文件: $CLASH_LOG"
    else
        echo "Clash 运行状态: 未运行"
    fi
}

update_config() {
    local config_content="$1"
    
    if [ -z "$config_content" ]; then
        echo "错误: 配置内容为空"
        echo "用法: echo '配置内容' | $0 update"
        return 1
    fi
    
    # 备份旧配置
    if [ -f "$CLASH_CONFIG" ]; then
        cp "$CLASH_CONFIG" "$CLASH_CONFIG.bak.$(date +%Y%m%d%H%M%S)"
    fi
    
    # 写入新配置
    echo "$config_content" > "$CLASH_CONFIG"
    
    if [ $? -eq 0 ]; then
        echo "配置已更新: $CLASH_CONFIG"
        
        # 验证配置格式
        if "$CLASH_BIN" -t -f "$CLASH_CONFIG" 2>&1 | grep -q "Parse config error"; then
            echo "警告: 配置格式可能有误，请检查"
        else
            echo "配置格式验证通过"
        fi
        
        # 如果正在运行，询问是否重启
        if pgrep -x "clash" > /dev/null; then
            echo "Clash 正在运行，建议重启以应用新配置"
        fi
    else
        echo "配置更新失败"
        return 1
    fi
}

test_proxy() {
    echo "测试代理连接..."
    
    # 测试 HTTP 代理
    echo -n "HTTP 代理 (Google): "
    if curl -s --connect-timeout 10 --proxy http://127.0.0.1:7890 http://www.google.com > /dev/null 2>&1; then
        echo "✓ 正常"
    else
        echo "✗ 失败"
    fi
    
    # 测试 SOCKS 代理
    echo -n "SOCKS 代理 (Google): "
    if curl -s --connect-timeout 10 --proxy socks5://127.0.0.1:7891 http://www.google.com > /dev/null 2>&1; then
        echo "✓ 正常"
    else
        echo "✗ 失败"
    fi
}

# 主逻辑
case "${1:-}" in
    start)
        start_clash
        ;;
    stop)
        stop_clash
        ;;
    restart)
        restart_clash
        ;;
    status)
        show_status
        ;;
    update)
        # 从 stdin 读取配置内容
        config=$(cat)
        update_config "$config"
        ;;
    test)
        test_proxy
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac
