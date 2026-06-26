#!/bin/bash
# ─── 心虫一键启动 ─────────────────────────────────────
# 用法: ./heartflow-start.sh
# 功能: 守护进程自动 + 引擎状态报告（一次bash调用，＜1秒）
# ──────────────────────────────────────────────────────

SOCK=/tmp/heartflow-mcp.sock
BOOT_JS="$(cd "$(dirname "$0")/.." && pwd)/bin/boot-fast.js"
DAEMON_JS="$(cd "$(dirname "$0")/.." && pwd)/daemon/mcp-daemon.js"

# ─── 第 1 步：确保守护进程在运行 ──────────────────────
if ! [ -S "$SOCK" ]; then
  # 清理残留 pid
  rm -f /tmp/heartflow-mcp.pid

  # 后台启动守护进程
  nohup node "$DAEMON_JS" >/dev/null 2>&1 &

  # 等待 socket 出现（最多等 5 秒）
  waited=0
  while [ ! -S "$SOCK" ] && [ $waited -lt 50 ]; do
    sleep 0.1
    waited=$((waited + 1))
  done

  if [ ! -S "$SOCK" ]; then
    echo '{"error":"守护进程启动超时","_startTime":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"}'
    exit 1
  fi
fi

# ─── 第 2 步：读取引擎状态 ─────────────────────────────
node "$BOOT_JS" --report-from-json
