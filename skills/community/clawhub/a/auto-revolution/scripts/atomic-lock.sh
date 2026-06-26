#!/bin/bash
# atomic-lock.sh - 原子锁管理脚本
# 使用 mkdir 原子操作，彻底消除 TOCTOU 竞态

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASKS_DIR="$SCRIPT_DIR/../tasks"
LOCK_TIMEOUT_MINUTES=5

usage() {
  echo "用法：$0 <command> <task-id>"
  echo ""
  echo "命令:"
  echo "  acquire   获取锁（成功返回 0，失败返回 1）"
  echo "  release   释放锁"
  echo "  check     检查锁状态"
  echo "  timeout   检查锁是否超时（超时返回 0，未超时返回 1）"
  echo ""
  echo "示例:"
  echo "  $0 acquire task-001"
  echo "  $0 release task-001"
  exit 1
}

acquire_lock() {
  local task_id=$1
  local lock_dir="$TASKS_DIR/${task_id}.lock.d"
  
  # 原子操作：mkdir 成功=获得锁，失败=已有锁
  if mkdir "$lock_dir" 2>/dev/null; then
    # 写入 PID 和时间戳
    echo $$ > "$lock_dir/pid"
    date -Iseconds > "$lock_dir/timestamp"
    echo "✅ 已获取锁：$task_id"
    return 0
  else
    echo "⚠️ 锁已存在：$task_id"
    return 1
  fi
}

release_lock() {
  local task_id=$1
  local lock_dir="$TASKS_DIR/${task_id}.lock.d"
  
  if [ -d "$lock_dir" ]; then
    rm -rf "$lock_dir"
    echo "✅ 已释放锁：$task_id"
    return 0
  else
    echo "⚠️ 锁不存在：$task_id"
    return 0
  fi
}

check_lock() {
  local task_id=$1
  local lock_dir="$TASKS_DIR/${task_id}.lock.d"
  
  if [ -d "$lock_dir" ]; then
    echo "🔒 锁存在：$task_id"
    if [ -f "$lock_dir/pid" ]; then
      echo "   PID: $(cat "$lock_dir/pid")"
    fi
    if [ -f "$lock_dir/timestamp" ]; then
      echo "   创建时间：$(cat "$lock_dir/timestamp")"
    fi
    return 0
  else
    echo "🔓 锁不存在：$task_id"
    return 1
  fi
}

check_timeout() {
  local task_id=$1
  local lock_dir="$TASKS_DIR/${task_id}.lock.d"
  local timestamp_file="$lock_dir/timestamp"
  
  if [ ! -d "$lock_dir" ]; then
    echo "⚠️ 锁不存在，无法检查超时"
    return 1
  fi
  
  if [ ! -f "$timestamp_file" ]; then
    echo "⚠️ 时间戳文件不存在，视为超时"
    return 0
  fi
  
  local timestamp=$(cat "$timestamp_file")
  local lock_epoch=$(date -d "$timestamp" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S" "$timestamp" +%s 2>/dev/null)
  local now_epoch=$(date +%s)
  local age_seconds=$((now_epoch - lock_epoch))
  local age_minutes=$((age_seconds / 60))
  
  echo "🕐 锁已存在 $age_minutes 分钟"
  
  if [ $age_minutes -ge $LOCK_TIMEOUT_MINUTES ]; then
    echo "⏰ 锁已超时（阈值：$LOCK_TIMEOUT_MINUTES 分钟）"
    return 0
  else
    echo "✅ 锁未超时"
    return 1
  fi
}

# 主程序
if [ $# -lt 2 ]; then
  usage
fi

command=$1
task_id=$2

case "$command" in
  acquire)
    acquire_lock "$task_id"
    ;;
  release)
    release_lock "$task_id"
    ;;
  check)
    check_lock "$task_id"
    ;;
  timeout)
    check_timeout "$task_id"
    ;;
  *)
    echo "❌ 未知命令：$command"
    usage
    ;;
esac
