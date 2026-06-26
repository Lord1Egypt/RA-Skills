#!/bin/bash
# Feishu Multi-Agent Relay 安装脚本

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG_DIR="$HOME/.openclaw/config"
CACHE_DIR="$HOME/.openclaw/cache"
TEMPLATE="$SKILL_DIR/config/relay-config.json"
TARGET="$CONFIG_DIR/feishu-multi-agent.json"

echo "=== Feishu Multi-Agent 安装 ==="
echo ""

# 1. 创建必要目录
echo "1. 初始化目录..."
mkdir -p "$CONFIG_DIR" "$CACHE_DIR"
echo "   ✓ 目录已就绪"

# 2. 复制配置模板（若目标已存在则跳过）
echo "2. 初始化配置文件..."
if [ -f "$TARGET" ]; then
    echo "   配置文件已存在，跳过（如需重置：rm $TARGET && bash $0）"
else
    cp "$TEMPLATE" "$TARGET"
    chmod 600 "$TARGET"
    echo "   ✓ 配置文件已创建: $TARGET"
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "📌 下一步："
echo "1. 编辑唯一配置文件，填入 App ID、App Secret、chat_id 等："
echo "   nano $TARGET"
echo ""
echo "   推荐：机器人A设 starter_role=self，机器人B设 starter_role=peer"
echo "   推荐：default_rounds=50，idle_timeout_minutes=30"
echo ""
echo "2. 启动对话 daemon："
echo "   python3 $SKILL_DIR/scripts/feishu_multi_agent.py start-sync"
echo ""
echo "3. 查看状态："
echo "   python3 $SKILL_DIR/scripts/feishu_multi_agent.py status"
echo ""
echo "4. 群里可直接发送："
echo "   讨论 AI Agent 权限边界"
echo "   STOP"
echo "   继续"
echo "   再对话50轮"
echo ""
echo "5. 停止 daemon："
echo "   python3 $SKILL_DIR/scripts/feishu_multi_agent.py stop-sync"
echo ""
echo "6. 测试单次发送："
echo "   python3 $SKILL_DIR/scripts/feishu_multi_agent.py send --to peer --msg \"你好！\""
echo ""
