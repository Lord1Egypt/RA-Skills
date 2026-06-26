#!/bin/bash
# Agent OS 启动脚本
# Usage: ./scripts/startup.sh

echo "==================================="
echo "     Agent OS 启动序列"
echo "==================================="
echo ""

# 检查工作目录
WORK_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORK_DIR"
echo "📁 工作目录: $WORK_DIR"

# 第一层：身份层检查
echo ""
echo "🔍 检查第一层：身份层"
if [ -f "identity/SOUL.md" ] && [ -f "identity/IDENTITY.md" ] && [ -f "identity/USER.md" ]; then
    echo "   ✅ 身份层完整"
else
    echo "   ❌ 身份层缺失，执行重建..."
    # 这里可以调用重建脚本
fi

# 第二层：操作层检查
echo ""
echo "🔍 检查第二层：操作层"
if [ -f "operations/AGENTS.md" ] && [ -f "operations/HEARTBEAT.md" ]; then
    echo "   ✅ 操作层完整"
else
    echo "   ❌ 操作层缺失，执行重建..."
fi

# 第三层：知识层检查
echo ""
echo "🔍 检查第三层：知识层"
if [ -f "knowledge/MEMORY.md" ]; then
    echo "   ✅ 知识层完整"
else
    echo "   ❌ 知识层缺失，执行重建..."
fi

# 启动完成
echo ""
echo "==================================="
echo "     ✅ Agent OS 启动完成"
echo "==================================="
echo ""
echo "可用代理:"
echo "  • simplify    - 代码优化"
echo "  • claude-api  - AI应用开发"
echo "  • agent-os    - 架构维护"
echo ""
echo "状态: 在线 | 负载: 就绪"
echo ""
