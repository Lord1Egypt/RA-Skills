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

# 启动ByteHouse MCP Server的脚本

# 设置环境变量（请自行配置）
# export BYTEHOUSE_HOST="<ByteHouse-host>"
# export BYTEHOUSE_PORT="<ByteHouse-port>"
# export BYTEHOUSE_USER="<ByteHouse-user>"
# export BYTEHOUSE_PASSWORD="<ByteHouse-password>"
# export BYTEHOUSE_SECURE="true"
# export BYTEHOUSE_VERIFY="true"
# export BYTEHOUSE_CONNECT_TIMEOUT="30"
# export BYTEHOUSE_SEND_RECEIVE_TIMEOUT="30"

echo "=" * 80
echo "启动ByteHouse MCP Server"
echo "=" * 80
echo "⚠️  请确保已在脚本中配置环境变量"
echo "=" * 80
echo

# 检查环境变量是否已配置
if [ -z "$BYTEHOUSE_HOST" ] || [ -z "$BYTEHOUSE_PASSWORD" ]; then
    echo "❌ 错误: 请先配置ByteHouse连接环境变量"
    echo "   编辑此脚本，取消注释并配置环境变量部分"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/logs"
PID_FILE="$SCRIPT_DIR/mcp_server.pid"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 日志文件
LOG_FILE="$LOG_DIR/mcp_server_$(date +%Y%m%d_%H%M%S).log"

echo "=" * 80
echo "ByteHouse MCP Server - 常驻服务"
echo "=" * 80
echo "脚本目录: $SCRIPT_DIR"
echo "日志目录: $LOG_DIR"
echo "日志文件: $LOG_FILE"
echo "PID文件: $PID_FILE"
echo "=" * 80
echo

# 检查是否已经在运行
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE" 2>/dev/null)
    if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
        echo "⚠️  MCP Server已经在运行 (PID: $PID)"
        echo "   如需重启，请先运行: $SCRIPT_DIR/stop_mcp_service.sh"
        exit 1
    else
        echo "⚠️  PID文件存在但进程不存在，清理旧文件"
        rm -f "$PID_FILE"
    fi
fi

echo "🚀 启动ByteHouse MCP Server..."
echo

# 启动MCP Server（后台运行）
cd "$SCRIPT_DIR"
/root/.local/bin/uvx --from "git+https://github.com/volcengine/mcp-server@main#subdirectory=server/mcp_server_bytehouse" mcp_bytehouse -t stdio > "$LOG_FILE" 2>&1 &
MCP_PID=$!

# 保存PID
echo $MCP_PID > "$PID_FILE"

# 等待一下检查进程
sleep 2

if kill -0 "$MCP_PID" 2>/dev/null; then
    echo "✅ ByteHouse MCP Server启动成功！"
    echo "   PID: $MCP_PID"
    echo "   日志: $LOG_FILE"
    echo ""
    echo "📋 管理命令:"
    echo "   查看状态: $SCRIPT_DIR/status_mcp_service.sh"
    echo "   查看日志: tail -f $LOG_FILE"
    echo "   停止服务: $SCRIPT_DIR/stop_mcp_service.sh"
else
    echo "❌ MCP Server启动失败"
    echo "   查看日志: $LOG_FILE"
    rm -f "$PID_FILE"
    exit 1
fi
