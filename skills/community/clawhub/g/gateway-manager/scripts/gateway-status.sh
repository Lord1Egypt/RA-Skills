#!/bin/bash
# gateway-status.sh - 跨平台 OpenClaw 网关管理器

# 检测操作系统
detect_os() {
    case "$(uname -s)" in
        Darwin*)    echo "macOS";;
        Linux*)     echo "Linux";;
        CYGWIN*|MINGW*|MSYS*) echo "Windows";;
        *)          echo "Unknown: $(uname -s)";;
    esac
}

OS=$(detect_os)
echo "=== OpenClaw Gateway Manager ==="
echo "💡 跨平台统一管理 - 支持多平台/多云部署"
echo "📊 当前系统：$OS"
echo ""

# 通过配置文件查找实例
check_instance() {
    local config_dir="$1"
    local name="$2"
    local config_file="$config_dir/openclaw.json"
    
    # 支持 Windows 路径
    if [[ "$OS" == "Windows" ]]; then
        config_file="$config_dir/openclaw.json"
    fi
    
    if [ -f "$config_file" ]; then
        local port=$(cat "$config_file" | jq -r '.gateway.port' 2>/dev/null)
        if [ -n "$port" ] && [ "$port" != "null" ]; then
            # 检查进程是否运行
            local pid=""
            if command -v lsof &> /dev/null; then
                pid=$(lsof -i :$port 2>/dev/null | grep LISTEN | grep -E "node|Claw|QClaw" | awk '{print $2}' | head -1)
            elif command -v netstat &> /dev/null; then
                pid=$(netstat -tlnp 2>/dev/null | grep ":$port " | awk '{print $7}' | cut -d'/' -f1 | head -1)
            fi
            
            local status="❌ 已停止"
            if [ -n "$pid" ]; then
                status="✅ 运行中 (PID: $pid)"
                # 查找辅助端口 (+2, +3)
                local browser_port=$((port + 2))
                local canvas_port=$((port + 3))
                local aux_ports=""
                if lsof -i :$browser_port 2>/dev/null | grep LISTEN > /dev/null; then
                    aux_ports="$aux_ports $browser_port(浏览器)"
                fi
                if lsof -i :$canvas_port 2>/dev/null | grep LISTEN > /dev/null; then
                    aux_ports="$aux_ports $canvas_port(Canvas)"
                fi
                echo "🔹 $name"
                echo "   主端口：$port"
                echo "   辅助端口：$aux_ports"
                echo "   配置：$config_dir"
                echo "   状态：$status"
                
                # 尝试获取频道信息
                local channel=$(cat "$config_file" | jq -r '.channels | keys[0]' 2>/dev/null)
                if [ -n "$channel" ] && [ "$channel" != "null" ]; then
                    echo "   频道：$channel"
                fi
                
                echo "   Dashboard: http://127.0.0.1:$port/"
                echo ""
            else
                echo "🔹 $name"
                echo "   主端口：$port"
                echo "   配置：$config_dir"
                echo "   状态：$status"
                echo "   ⚠️  进程未运行，需要重启"
                echo ""
            fi
        fi
    fi
}

# 根据操作系统检测配置路径
echo "🔍 扫描 OpenClaw 配置路径..."
echo ""

# macOS 路径
if [[ "$OS" == "macOS" ]]; then
    check_instance "$HOME/.openclaw" "OpenClaw (原始版)"
    check_instance "$HOME/.jvs/.openclaw" "JVS Claw (阿里云)"
    check_instance "$HOME/.qclaw" "QClaw (腾讯)"
    check_instance "$HOME/.claw-cloud" "Cloud Claw (云端)"
    
    # 自定义实例
    for dir in $HOME/.openclaw-*; do
        if [ -d "$dir" ] && [ -f "$dir/openclaw.json" ]; then
            case "$dir" in
                *cloud*) continue ;;
            esac
            instance_name=$(basename "$dir" | sed 's/\.openclaw-//')
            check_instance "$dir" "自定义实例：$instance_name"
        fi
    done

# Linux 路径
elif [[ "$OS" == "Linux" ]]; then
    check_instance "$HOME/.openclaw" "OpenClaw (Linux)"
    check_instance "$HOME/.config/openclaw" "OpenClaw (Config)"
    check_instance "/opt/openclaw" "OpenClaw (System)"
    
    # 自定义实例
    for dir in $HOME/.openclaw-*; do
        if [ -d "$dir" ] && [ -f "$dir/openclaw.json" ]; then
            instance_name=$(basename "$dir" | sed 's/\.openclaw-//')
            check_instance "$dir" "自定义实例：$instance_name"
        fi
    done

# Windows 路径
elif [[ "$OS" == "Windows" ]]; then
    check_instance "$USERPROFILE/.openclaw" "OpenClaw (Windows)"
    check_instance "$APPDATA/openclaw" "OpenClaw (AppData)"
    check_instance "C:/ProgramData/openclaw" "OpenClaw (ProgramData)"
fi

# 服务状态（跨平台）
echo "=== 服务状态 ==="
if [[ "$OS" == "macOS" ]]; then
    launchctl list 2>/dev/null | grep -i "claw\|gateway" | while read line; do
        status=$(echo "$line" | awk '{print $2}')
        label=$(echo "$line" | awk '{print $3}')
        if [ "$status" = "0" ] || [ "$status" = "1" ]; then
            echo "   ✅ $label (状态：$status)"
        else
            echo "   ❌ $label (状态：$status - 已停止)"
        fi
    done
elif [[ "$OS" == "Linux" ]]; then
    systemctl list-units --type=service 2>/dev/null | grep -i "claw\|gateway" | while read line; do
        echo "   $line"
    done
elif [[ "$OS" == "Windows" ]]; then
    Get-Service -Name "*claw*","*gateway*" 2>/dev/null | ForEach-Object {
        echo "   $($_.Name): $($_.Status)"
    }
fi

echo ""
echo "=== 所有 Claw 相关端口 ==="
if command -v lsof &> /dev/null; then
    lsof -i -n -P 2>/dev/null | grep LISTEN | grep -E "node|Claw|QClaw" | grep -E "18[0-9]{3}|1900[0-9]|28789|29000" | awk '{print $1, $9}' | sort -u
elif command -v netstat &> /dev/null; then
    netstat -tlnp 2>/dev/null | grep -E "18[0-9]{3}|1900[0-9]|28789|29000" | awk '{print $4, $7}'
fi

echo ""
echo "📊 统计信息："
if command -v lsof &> /dev/null; then
    total=$(lsof -i -n -P 2>/dev/null | grep LISTEN | grep -E "node|Claw|QClaw" | grep -E "18[0-9]{3}|1900[0-9]|28789|29000" | wc -l | tr -d ' ')
    echo "   检测到的端口数：$total"
fi
echo ""
echo "💡 提示：使用 gateway-scan-ports.sh 查看更详细的端口信息"
