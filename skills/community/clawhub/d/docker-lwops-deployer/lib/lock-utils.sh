#!/bin/bash
#
# 锁管理工具函数库
# 提供文件锁功能，防止并发部署冲突
#

# 锁文件目录
LOCK_DIR="/tmp/docker-lwops-deployer"
LOCK_FILE="$LOCK_DIR/deploy.lock"
LOCK_TIMEOUT=300  # 5分钟超时

# 初始化锁目录
init_lock() {
    if [ ! -d "$LOCK_DIR" ]; then
        mkdir -p "$LOCK_DIR" || {
            echo "无法创建锁目录: $LOCK_DIR" >&2
            return 1
        }
    fi
    return 0
}

# 获取锁（非阻塞模式）
# 返回值: 0=成功, 1=失败（锁已被占用）
acquire_lock() {
    init_lock || return 1

    # 尝试创建锁文件（原子操作）
    if ( set -o noclobber; echo "$$" > "$LOCK_FILE" ) 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# 获取锁（阻塞模式，带超时）
# 参数: $1 - 超时时间（秒），默认 300
# 返回值: 0=成功, 1=超时
acquire_lock_with_timeout() {
    local timeout="${1:-$LOCK_TIMEOUT}"
    local elapsed=0
    local interval=2  # 每 2 秒检查一次

    init_lock || return 1

    while [ $elapsed -lt $timeout ]; do
        if acquire_lock; then
            return 0
        fi

        # 获取锁的持有者信息
        local lock_pid=$(cat "$LOCK_FILE" 2>/dev/null)
        local lock_age=0
        if [ -n "$lock_pid" ]; then
            # 检查进程是否还在运行
            if ps -p "$lock_pid" >/dev/null 2>&1; then
                lock_age=$(ps -o etimes= -p "$lock_pid" 2>/dev/null | tr -d ' ')
                lock_age=${lock_age:-0}
            else
                # 进程已死，清理锁文件
                rm -f "$LOCK_FILE" 2>/dev/null
                if acquire_lock; then
                    return 0
                fi
            fi
        fi

        # 等待一段时间再试
        sleep $interval
        elapsed=$((elapsed + interval))
    done

    return 1
}

# 释放锁
release_lock() {
    rm -f "$LOCK_FILE" 2>/dev/null
    return 0
}

# 获取锁的状态信息
# 返回: JSON 格式的锁状态
get_lock_status() {
    local status="unlocked"
    local pid=""
    local age=0
    local remaining_time=0

    if [ -f "$LOCK_FILE" ]; then
        pid=$(cat "$LOCK_FILE" 2>/dev/null)
        if [ -n "$pid" ] && ps -p "$pid" >/dev/null 2>&1; then
            status="locked"
            age=$(ps -o etimes= -p "$pid" 2>/dev/null | tr -d ' ')
            age=${age:-0}
            remaining_time=$((LOCK_TIMEOUT - age))
        else
            # 僵尸锁，清理它
            rm -f "$LOCK_FILE" 2>/dev/null
        fi
    fi

    cat <<EOF
{
  "status": "$status",
  "pid": "$pid",
  "age_seconds": $age,
  "remaining_seconds": $remaining_time,
  "lock_file": "$LOCK_FILE"
}
EOF
}

# 清理锁（用于脚本退出时的清理）
cleanup_lock() {
    release_lock
}

# 显示锁状态的友好信息
show_lock_status() {
    local status=$(get_lock_status)
    local status_value=$(echo "$status" | grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*: *"\([^"]*\)".*/\1/')

    echo "========================================"
    echo "部署锁状态"
    echo "========================================"

    if [ "$status_value" = "locked" ]; then
        local pid=$(echo "$status" | grep -o '"pid"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*: *"\([^"]*\)".*/\1/')
        local age=$(echo "$status" | grep -o '"age_seconds"[[:space:]]*:[[:space:]]*[0-9]*' | sed 's/.*: *\([0-9]*\).*/\1/')
        local remaining=$(echo "$status" | grep -o '"remaining_seconds"[[:space:]]*:[[:space:]]*[0-9]*' | sed 's/.*: *\([0-9]*\).*/\1/')

        echo "状态: 已锁定"
        echo "持有者进程: $pid"
        echo "已运行时间: ${age} 秒"
        echo "预计剩余时间: ${remaining} 秒"
        echo ""
        echo "查看进程详情: ps -fp $pid"
        echo "查看部署日志: sudo docker logs lwops_rocky8_image_8.1"
    else
        echo "状态: 未锁定"
        echo "当前没有部署任务在执行"
    fi

    echo "========================================"
}
