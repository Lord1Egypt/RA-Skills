#!/bin/bash

echo "🚀 启动 Task Management Skill..."
echo ""

# 获取端口配置（默认 8080）
PORT=${TASK_SKILL_PORT:-8080}

# 编译
echo "📦 编译中..."
go build -o task-skill .

if [ $? -ne 0 ]; then
    echo "❌ 编译失败"
    exit 1
fi

echo "✅ 编译成功"
echo ""

# 启动服务器
echo "🌐 启动 Web 服务器..."
echo "访问地址：http://localhost:${PORT}"
echo "提示：可通过环境变量 TASK_SKILL_PORT 配置端口 (当前：${PORT})"
echo "按 Ctrl+C 停止服务器"
echo ""

export TASK_SKILL_PORT=${PORT}
./task-skill --server
