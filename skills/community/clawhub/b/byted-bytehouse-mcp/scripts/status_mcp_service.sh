#!/bin/bash
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# 查看ByteHouse MCP Server状态

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/mcp_server.pid"
LOG_DIR="$SCRIPT_DIR/logs"

echo "=" * 80
echo "ByteHouse MCP Server 状态"
echo "=" * 80

if [ ! -f "$PID_FILE" ]; then
    echo "❌ MCP Server未运行 (PID文件不存在)"
    echo ""
    echo "启动命令: $SCRIPT_DIR/start_mcp_service.sh"
    exit 1
fi

PID=$(cat "$PID_FILE" 2>/dev/null)
if [ -z "$PID" ]; then
    echo "❌ MCP Server未运行 (PID文件为空)"
    rm -f "$PID_FILE"
    exit 1
fi

if ! kill -0 "$PID" 2>/dev/null; then
    echo "❌ MCP Server未运行 (进程不存在)"
    rm -f "$PID_FILE"
    exit 1
fi

echo "✅ MCP Server正在运行"
echo "   PID: $PID"
echo ""

# 查看进程信息
echo "📊 进程信息:"
ps -p "$PID" -o pid,ppid,cmd,%cpu,%mem,etime
echo ""

# 查看最新日志
if [ -d "$LOG_DIR" ]; then
    LATEST_LOG=$(ls -t "$LOG_DIR"/mcp_server_*.log 2>/dev/null | head -1)
    if [ -n "$LATEST_LOG" ]; then
        echo "📝 最新日志文件: $LATEST_LOG"
        echo ""
        echo "📋 最近20行日志:"
        echo "-" * 80
        tail -20 "$LATEST_LOG"
        echo "-" * 80
        echo ""
        echo "查看完整日志: tail -f $LATEST_LOG"
    fi
fi

echo ""
echo "📋 管理命令:"
echo "   停止服务: $SCRIPT_DIR/stop_mcp_service.sh"
echo "   重启服务: $SCRIPT_DIR/restart_mcp_service.sh"
