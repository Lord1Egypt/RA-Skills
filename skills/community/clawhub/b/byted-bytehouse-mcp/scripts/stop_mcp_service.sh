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

# 停止ByteHouse MCP Server

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/mcp_server.pid"

echo "=" * 80
echo "停止ByteHouse MCP Server"
echo "=" * 80

if [ ! -f "$PID_FILE" ]; then
    echo "⚠️  PID文件不存在，MCP Server可能未运行"
    exit 0
fi

PID=$(cat "$PID_FILE" 2>/dev/null)
if [ -z "$PID" ]; then
    echo "⚠️  PID文件为空"
    rm -f "$PID_FILE"
    exit 0
fi

echo "正在停止MCP Server (PID: $PID)..."

# 尝试优雅停止
kill "$PID" 2>/dev/null

# 等待进程结束
for i in {1..10}; do
    if ! kill -0 "$PID" 2>/dev/null; then
        echo "✅ MCP Server已停止"
        rm -f "$PID_FILE"
        exit 0
    fi
    sleep 1
done

# 强制停止
echo "⚠️  进程未响应，强制停止..."
kill -9 "$PID" 2>/dev/null
sleep 1

if ! kill -0 "$PID" 2>/dev/null; then
    echo "✅ MCP Server已强制停止"
else
    echo "❌ 无法停止进程 (PID: $PID)"
    exit 1
fi

rm -f "$PID_FILE"
