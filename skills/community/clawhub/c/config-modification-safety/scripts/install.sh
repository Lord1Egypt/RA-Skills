#!/bin/bash
# config-modification-safety 安装脚本
# 用途：一次性安装双层守护架构，不需要手动配置

set -e

echo "🛡️  OpenClaw 配置安全守护 — 安装程序"
echo "========================================"
echo ""

WORK_DIR="$HOME/.openclaw/workspace/.lib/config-safety"
mkdir -p "$WORK_DIR"

# 1. 复制守护脚本
echo "📦 部署守护脚本..."
cp "$HOME/.openclaw/skills/config-modification-safety/scripts/guard.py" "$WORK_DIR/"
cp "$HOME/.openclaw/skills/config-modification-safety/scripts/health-check.sh" "$WORK_DIR/"
chmod +x "$WORK_DIR/health-check.sh"

# 2. 部署 launchd plist（第一层守护）
echo "🚀 注册第一层守护（launchd WatchPaths）..."
PLIST_SRC="$HOME/.openclaw/skills/config-modification-safety/scripts/com.openclaw.config-guard.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.openclaw.config-guard.plist"

# 替换路径占位符
sed "s|/Users/mingming|$HOME|g" "$PLIST_SRC" > "$PLIST_DST"
launchctl load "$PLIST_DST" 2>/dev/null || echo "  (可能已加载，跳过)"

# 3. 部署 cron 任务（第二层守护）
echo "⏰ 注册第二层守护（cron 健康巡检）..."
CRON_LINE="*/5 * * * * $HOME/.openclaw/workspace/.lib/config-safety/health-check.sh >> $HOME/.openclaw/workspace/.lib/config-safety/health-check.log 2>&1"

# 读取现有 crontab，移除旧的任务（避免重复）
(crontab -l 2>/dev/null | grep -v "config-safety/health-check"; echo "$CRON_LINE") | crontab -

# 4. 创建初始备份
echo "💾 创建初始配置备份..."
python3 "$WORK_DIR/guard.py" backup

echo ""
echo "✅ 安装完成！"
echo ""
echo "📊 架构概览："
echo "  第一层（铜墙）：launchd WatchPaths — JSON 语法错误 < 1 秒回滚"
echo "  第二层（铁壁）：cron 健康巡检 — Gateway 崩溃 5~15 分钟恢复"
echo ""
echo "📋 常用命令："
echo "  查看守护状态：launchctl list | grep config-guard"
echo "  查看守护日志：tail -f $HOME/.openclaw/workspace/.lib/config-safety/guard.log"
echo "  手动回滚：python3 $HOME/.openclaw/workspace/.lib/config-safety/guard.py rollback"
echo "  卸载：launchctl unload $HOME/Library/LaunchAgents/com.openclaw.config-guard.plist && crontab -r"
