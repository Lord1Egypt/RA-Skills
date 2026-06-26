#!/bin/bash
# Gateway Keepalive - 卸载脚本
# 作者: 康妃 (config)
# 版本: 1.1.0

echo "🦞 Gateway Keepalive 卸载"
echo "========================"
echo ""

# 确认卸载
read -p "确认卸载黄金包活机制？(y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 取消卸载"
    exit 1
fi

# 停止并卸载 LaunchAgents
echo "🛑 停止服务..."
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist 2>/dev/null || true
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.openclaw.health-check.plist 2>/dev/null || true

# 删除 LaunchAgent 配置文件
echo "🗑️ 删除 LaunchAgent 配置..."
rm -f ~/Library/LaunchAgents/ai.openclaw.gateway.plist
rm -f ~/Library/LaunchAgents/com.openclaw.health-check.plist

# 询问是否删除备份
read -p "是否删除黄金备份？(y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️ 删除黄金备份..."
    rm -rf ~/.openclaw/backups/golden-config
fi

# 询问是否删除日志
read -p "是否删除健康检测日志？(y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️ 删除日志..."
    rm -f ~/.openclaw/logs/health-recovery.log*
    rm -f ~/.openclaw/logs/health-check.log*
    rm -f ~/.openclaw/state/recovery-count
fi

echo ""
echo "✅ 卸载完成"
echo ""
echo "⚠️ 注意: Gateway 本身未卸载，只是移除了自动恢复机制"
echo "  手动启动: openclaw gateway start"
