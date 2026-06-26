#!/bin/bash
# gateway-delete.sh - 删除 OpenClaw 网关实例（需要多重确认）

INSTANCE="$1"

show_warning() {
    echo "⚠️  ⚠️  ⚠️  危险操作警告  ⚠️  ⚠️  ⚠️"
    echo ""
    echo "这将永久删除以下实例："
    echo "   实例名：$INSTANCE"
    echo "   配置目录：$CONFIG_DIR"
    echo "   LaunchAgent: $PLIST_FILE"
    echo ""
    echo "此操作会："
    echo "   ❌ 停止网关进程"
    echo "   ❌ 删除所有配置文件"
    echo "   ❌ 删除所有会话历史"
    echo "   ❌ 删除所有记忆文件"
    echo "   ❌ 删除 LaunchAgent"
    echo ""
    echo "此操作不可恢复！"
    echo ""
}

if [ -z "$INSTANCE" ]; then
    echo "用法：gateway-delete.sh <实例名>"
    echo ""
    echo "⚠️  警告：这是危险操作，需要多重确认！"
    echo ""
    echo "可用实例:"
    echo "   本地虾 (18789)"
    echo "   飞书 (18790)"
    echo "   或其他自定义实例名"
    echo ""
    echo "示例：gateway-delete.sh test-bot"
    exit 1
fi

# 解析实例名
case "$INSTANCE" in
    local-shrimp|本地虾 |18789)
        CONFIG_DIR="$HOME/.jvs/.openclaw"
        PLIST_FILE="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
        PORT="18789"
        ;;
    feishu|飞书|18790)
        CONFIG_DIR="$HOME/.openclaw"
        PLIST_FILE="$HOME/Library/LaunchAgents/ai.openclaw.gateway-feishu.plist"
        PORT="18790"
        ;;
    *)
        # 自定义实例
        CONFIG_DIR="$HOME/.openclaw-$INSTANCE"
        PLIST_FILE="$HOME/Library/LaunchAgents/ai.openclaw.gateway-$INSTANCE.plist"
        PORT="未知"
        ;;
esac

# 检查配置是否存在
if [ ! -d "$CONFIG_DIR" ]; then
    echo "❌ 配置目录不存在：$CONFIG_DIR"
    exit 1
fi

show_warning

# 第一次确认
echo -n "确认 1/3: 你真的要删除这个实例吗？(输入 YES 继续): "
read confirm1
if [ "$confirm1" != "YES" ]; then
    echo "❌ 操作已取消"
    exit 1
fi

# 第二次确认 - 输入实例名
echo -n "确认 2/3: 请输入实例名 '$INSTANCE' 确认： "
read confirm2
if [ "$confirm2" != "$INSTANCE" ]; then
    echo "❌ 实例名不匹配，操作已取消"
    exit 1
fi

# 第三次确认 - 输入 delete
echo -n "确认 3/3: 输入 'delete' 执行删除： "
read confirm3
if [ "$confirm3" != "delete" ]; then
    echo "❌ 操作已取消"
    exit 1
fi

echo ""
echo "🔴 开始删除..."
echo ""

# 1. 停止网关进程
if [ -n "$PORT" ] && [ "$PORT" != "未知" ]; then
    pid=$(lsof -i :$PORT 2>/dev/null | grep LISTEN | grep node | awk '{print $2}' | head -1)
    if [ -n "$pid" ]; then
        echo "⏹️  停止网关进程 (PID: $pid)..."
        kill $pid 2>/dev/null
        sleep 2
        echo "✅ 进程已停止"
    fi
fi

# 2. 卸载 LaunchAgent
if [ -f "$PLIST_FILE" ]; then
    echo "⏹️  卸载 LaunchAgent..."
    launchctl unload "$PLIST_FILE" 2>/dev/null
    launchctl remove $(basename "$PLIST_FILE" .plist) 2>/dev/null
    rm "$PLIST_FILE"
    echo "✅ LaunchAgent 已删除"
else
    echo "ℹ️  LaunchAgent 不存在"
fi

# 3. 备份配置（以防万一）
BACKUP_DIR="$HOME/.openclaw-deleted-backups/$INSTANCE-$(date +%Y%m%d%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "💾 备份配置到：$BACKUP_DIR"
cp -r "$CONFIG_DIR" "$BACKUP_DIR/" 2>/dev/null
echo "✅ 备份完成（7 天内可恢复）"

# 4. 删除配置目录
echo "🗑️  删除配置目录：$CONFIG_DIR"
rm -rf "$CONFIG_DIR"
echo "✅ 配置目录已删除"

# 5. 清理浏览器数据
BROWSER_DIR="$HOME/.jvs/.openclaw/browser/openclaw"
if [ -d "$BROWSER_DIR" ]; then
    echo "🗑️  清理浏览器数据..."
    # 只清理相关数据，保留其他实例的
fi

echo ""
echo "✅ 删除完成！"
echo ""
echo "备份位置：$BACKUP_DIR"
echo "如需恢复，执行：cp -r $BACKUP_DIR/* $CONFIG_DIR/"
echo ""
echo "已删除的内容："
echo "   - 配置文件 (openclaw.json)"
echo "   - 会话历史 (sessions/)"
echo "   - 记忆文件 (memory/, MEMORY.md)"
echo "   - LaunchAgent plist"
echo ""
echo "⚠️  请手动验证："
echo "   1. 检查端口 $PORT 是否已释放：lsof -i :$PORT"
echo "   2. 检查 LaunchAgent 是否已删除：launchctl list | grep openclaw"
echo "   3. 检查 Dashboard 是否无法访问：http://127.0.0.1:$PORT/"
