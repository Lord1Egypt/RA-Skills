#!/bin/bash
#
# 网络和端口检测工具函数库
# 提供端口检测、IP 获取等功能
#

# 检查端口是否可用
# 参数: $1 - 端口号
# 返回值: 0=可用, 1=被占用
is_port_available() {
    local port="$1"
    local in_use=false

    # 方法1: 使用 ss 命令（推荐）
    if command -v ss &> /dev/null; then
        if ss -tuln | grep -q ":$port "; then
            in_use=true
        fi
    # 方法2: 使用 netstat 命令
    elif command -v netstat &> /dev/null; then
        if netstat -tuln 2>/dev/null | grep -q ":$port "; then
            in_use=true
        fi
    # 方法3: 使用 lsof 命令
    elif command -v lsof &> /dev/null; then
        if lsof -i ":$port" &> /dev/null; then
            in_use=true
        fi
    # 方法4: 尝试连接端口
    else
        if timeout 1 bash -c "echo >/dev/tcp/127.0.0.1/$port" 2>/dev/null; then
            in_use=true
        fi
    fi

    if [ "$in_use" = true ]; then
        return 1
    else
        return 0
    fi
}

# 查找可用端口
# 参数: $1 - 起始端口（默认 8000）
# 返回值: 可用端口号
find_available_port() {
    local start_port="${1:-8000}"
    local port="$start_port"
    local max_attempts=100
    local attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if is_port_available "$port"; then
            echo "$port"
            return 0
        fi
        port=$((port + 1))
        attempt=$((attempt + 1))
    done

    # 未找到可用端口
    return 1
}

# 智能分配端口
# 参数:
#   $1 - 容器端口1（默认 80）
#   $2 - 容器端口2（默认 8081）
#   $3 - 宿主机起始端口1（默认 8000）
#   $4 - 宿主机起始端口2（默认 8081）
# 返回: JSON 格式的端口映射
allocate_ports() {
    local container_port1="${1:-80}"
    local container_port2="${2:-8081}"
    local host_start1="${3:-8000}"
    local host_start2="${4:-8081}"

    local host_port1="$host_start1"
    local host_port2="$host_start2"

    # 检查并分配第一个端口
    if ! is_port_available "$host_port1"; then
        host_port1=$(find_available_port "$host_port1")
        if [ -z "$host_port1" ]; then
            return 1
        fi
    fi

    # 检查并分配第二个端口
    if ! is_port_available "$host_port2"; then
        host_port2=$(find_available_port "$host_port2")
        if [ -z "$host_port2" ]; then
            return 1
        fi
    fi

    cat <<EOF
{
  "container_port1": $container_port1,
  "host_port1": $host_port1,
  "container_port2": $container_port2,
  "host_port2": $host_port2
}
EOF
}

# 获取主机 IP 地址
# 返回值: 主机 IP 地址
get_host_ip() {
    local ip=""

    # 方法1: 使用 hostname -I
    if command -v hostname &> /dev/null; then
        ip=$(hostname -I 2>/dev/null | awk '{print $1}')
        if [ -n "$ip" ]; then
            echo "$ip"
            return 0
        fi
    fi

    # 方法2: 使用 ip 命令
    if command -v ip &> /dev/null; then
        ip=$(ip route get 1 2>/dev/null | awk '{print $7}' | head -1)
        if [ -n "$ip" ]; then
            echo "$ip"
            return 0
        fi
    fi

    # 方法3: 使用 ifconfig 命令
    if command -v ifconfig &> /dev/null; then
        ip=$(ifconfig 2>/dev/null | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}' | head -1)
        if [ -n "$ip" ]; then
            echo "$ip"
            return 0
        fi
    fi

    # 方法4: 解析 /proc/net/route（适用于没有 ip 命令的系统）
    if [ -f /proc/net/route ]; then
        ip=$(awk '$2 == "00000000" {print $1}' /proc/net/route | head -1)
        if [ -n "$ip" ]; then
            # 将十六进制 IP 转换为点分十进制
            ip=$(echo "$ip" | sed 's/../0x& /g' | \
                awk '{printf "%d.%d.%d.%d", and($1,0xFF), rshift(and($1,0xFF00),8), rshift(and($1,0xFF0000),16), rshift(and($1,0xFF000000),24)}')
            if [ "$ip" != "0.0.0.0" ]; then
                echo "$ip"
                return 0
            fi
        fi
    fi

    # 如果都失败，返回 localhost
    echo "127.0.0.1"
    return 0
}

# 检查网络连接
# 参数: $1 - 主机, $2 - 端口
# 返回值: 0=可连接, 1=无法连接
check_connection() {
    local host="$1"
    local port="$2"

    if timeout 5 bash -c "echo >/dev/tcp/$host/$port" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# 检查 DNS 解析
# 参数: $1 - 域名
# 返回值: 0=可解析, 1=无法解析
check_dns() {
    local domain="$1"

    if command -v nslookup &> /dev/null; then
        if nslookup "$domain" &> /dev/null; then
            return 0
        fi
    elif command -v host &> /dev/null; then
        if host "$domain" &> /dev/null; then
            return 0
        fi
    elif command -v dig &> /dev/null; then
        if dig "$domain" &> /dev/null; then
            return 0
        fi
    fi

    return 1
}
