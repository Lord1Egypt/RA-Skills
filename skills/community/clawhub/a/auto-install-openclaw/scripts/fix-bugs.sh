#!/bin/bash
# OpenClaw Bug 自动修复脚本
# 用法：./fix-bugs.sh

set -e

echo "🔧 OpenClaw Bug 自动修复"
echo "========================"

CONFIG_DIR=~/.openclaw/config
LOGS_DIR=~/.openclaw/logs
PLUGINS_DIR=~/.openclaw/plugins

# 1. 检查网关状态
echo ""
echo "📊 检查网关状态..."
if command -v openclaw &> /dev/null; then
    STATUS=$(openclaw gateway status 2>&1 || echo "not running")
    if echo "$STATUS" | grep -q "running"; then
        echo "✅ 网关运行正常"
    else
        echo "⚠️  网关未运行，尝试启动..."
        openclaw gateway start || echo "❌ 启动失败"
    fi
else
    echo "❌ OpenClaw 未安装"
    exit 1
fi

# 2. 清理日志文件
echo ""
echo "🧹 清理日志文件..."
if [ -d "$LOGS_DIR" ]; then
    find "$LOGS_DIR" -name "*.log" -mtime +7 -delete 2>/dev/null || true
    echo "✅ 已清理 7 天前的日志"
fi

# 3. 修复权限问题
echo ""
echo "🔐 修复权限..."
chmod -R 755 ~/.openclaw 2>/dev/null || true
echo "✅ 权限已修复"

# 4. 检查模型配置
echo ""
echo "🔑 检查模型配置..."
if [ ! -f "$CONFIG_DIR/models.json" ]; then
    echo "⚠️  模型配置文件不存在"
    echo "请运行 './scripts/configure-claude.sh' 进行配置"
else
    echo "✅ 模型配置存在"
fi

# 5. 检查插件依赖
echo ""
echo "📦 检查插件依赖..."
for plugin_dir in "$PLUGINS_DIR"/*/; do
    if [ -d "$plugin_dir" ]; then
        plugin_name=$(basename "$plugin_dir")
        if [ -f "$plugin_dir/package.json" ]; then
            echo "🔧 修复插件 $plugin_name 依赖..."
            cd "$plugin_dir" && pnpm install --silent 2>/dev/null || \
            echo "⚠️  插件 $plugin_name 依赖修复失败"
        fi
    fi
done
echo "✅ 插件依赖检查完成"

# 6. 重置网关缓存
echo ""
echo "🗑️  清理网关缓存..."
openclaw gateway clean 2>/dev/null || echo "⚠️  清理缓存失败"

# 7. 测试 API 连接
echo ""
echo "🧪 测试 API 连接..."
if [ -f "$CONFIG_DIR/models.json" ]; then
    API_KEY=$(grep -o '"apiKey": "[^"]*"' "$CONFIG_DIR/models.json" | cut -d'"' -f4)
    API_URL=$(grep -o '"baseUrl": "[^"]*"' "$CONFIG_DIR/models.json" | cut -d'"' -f4)
    
    if [ -n "$API_KEY" ] && [ -n "$API_URL" ]; then
        RESPONSE=$(curl -s -X POST "${API_URL}/models" \
          -H "Authorization: Bearer ${API_KEY}" \
          -H "Content-Type: application/json" || echo '{"error":"connection failed"}')
        
        if echo "$RESPONSE" | grep -q "error"; then
            echo "⚠️  API 连接失败，请检查网络和 API Key"
        else
            echo "✅ API 连接正常"
        fi
    fi
fi

# 8. 重启网关
echo ""
echo "🔄 重启网关..."
read -p "是否重启网关？(y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    openclaw gateway restart
    echo "✅ 网关已重启"
fi

# 9. 查看最新日志
echo ""
echo "📋 最新日志（最后 20 行）："
openclaw logs --tail 20 2>/dev/null || tail -20 "$LOGS_DIR/gateway.log" 2>/dev/null || echo "无日志"

echo ""
echo "✅ Bug 自动修复完成！"
echo ""
echo "如果问题仍然存在，请查看："
echo "1. 日志文件：$LOGS_DIR/"
echo "2. 配置文件：$CONFIG_DIR/"
echo "3. 官方文档：https://docs.openclaw.ai/"
