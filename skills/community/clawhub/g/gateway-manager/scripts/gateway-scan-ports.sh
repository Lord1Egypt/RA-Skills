#!/bin/bash
# gateway-scan-ports.sh - 智能扫描 OpenClaw 网关端口

echo "=== OpenClaw 端口扫描 ==="
echo ""

# 扫描常见 OpenClaw 端口范围
declare -A port_groups

# 扫描 18000-18999 范围
for port in $(seq 18000 18999); do
    if lsof -i :$port 2>/dev/null | grep LISTEN | grep node > /dev/null 2>&1; then
        pid=$(lsof -i :$port 2>/dev/null | grep LISTEN | grep node | awk '{print $2}' | head -1)
        
        # 检查是否是主端口（配置文件中的端口）
        is_main=false
        config_dir=""
        
        # 检查常见配置目录
        for dir in "$HOME/.jvs/.openclaw" "$HOME/.openclaw" "$HOME"/.openclaw-*; do
            if [ -f "$dir/openclaw.json" ]; then
                cfg_port=$(cat "$dir/openclaw.json" | jq -r '.gateway.port' 2>/dev/null)
                if [ "$cfg_port" = "$port" ]; then
                    is_main=true
                    config_dir="$dir"
                    break
                fi
            fi
        done
        
        if [ "$is_main" = true ]; then
            # 主端口，查找辅助端口
            browser_port=$((port + 2))
            canvas_port=$((port + 3))
            
            echo "🔹 网关实例 (主端口：$port)"
            echo "   PID: $pid"
            echo "   配置：$config_dir"
            
            # 检查辅助端口
            aux=""
            if lsof -i :$browser_port 2>/dev/null | grep LISTEN > /dev/null; then
                aux="$aux 浏览器:$browser_port"
            fi
            if lsof -i :$canvas_port 2>/dev/null | grep LISTEN > /dev/null; then
                aux="$aux Canvas:$canvas_port"
            fi
            if [ -n "$aux" ]; then
                echo "   辅助端口:$aux"
            fi
            
            # 尝试获取频道信息
            if [ -f "$config_dir/openclaw.json" ]; then
                channels=$(cat "$config_dir/openclaw.json" | jq -r '.channels | keys | join(", ")' 2>/dev/null)
                if [ -n "$channels" ] && [ "$channels" != "null" ]; then
                    echo "   频道：$channels"
                fi
            fi
            
            echo "   Dashboard: http://127.0.0.1:$port/"
            echo ""
        fi
    fi
done

echo "=== 其他 Node 进程 (可能不是 OpenClaw) ==="
lsof -i -n -P 2>/dev/null | grep LISTEN | grep node | grep -v "18[0-9]\{3\}" | awk '{print $1, $9}' | sort -u | head -10
