#!/bin/bash
# 自动配置每周技能更新检查的 crontab
# 用法：./setup-cron.sh [AGENT_WORKSPACE]
#       ./setup-cron.sh --remove  # 移除定时任务

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTO_UPDATE_SCRIPT="${SCRIPT_DIR}/auto-update.sh"
AGENT_WORKSPACE="${1:-/Users/xubangbang/.openclaw/workspace}"
CRON_JOB="0 3 * * 0 ${AUTO_UPDATE_SCRIPT} ${AGENT_WORKSPACE} >> /tmp/clawhub-update.log 2>&1"

# 处理 --remove 参数
if [ "$1" = "--remove" ]; then
  echo "🗑️  移除定时任务..."
  crontab -l 2>/dev/null | grep -v -F "$AUTO_UPDATE_SCRIPT" | crontab - 2>/dev/null || true
  echo "✅ 已移除 clawhub-browser 定时任务"
  exit 0
fi

echo "🔧 配置每周自动更新检查..."
echo ""

# 检查 auto-update.sh 是否存在
if [ ! -f "$AUTO_UPDATE_SCRIPT" ]; then
  echo "❌ 错误：auto-update.sh 不存在"
  echo "   路径：$AUTO_UPDATE_SCRIPT"
  exit 1
fi

# 确保脚本可执行
chmod +x "$AUTO_UPDATE_SCRIPT"

echo "📍 工作区：${AGENT_WORKSPACE}"
echo "📝 脚本：${AUTO_UPDATE_SCRIPT}"
echo ""

# 检查 crontab 是否已存在
EXISTING_CRON=$(crontab -l 2>/dev/null | grep -F "$AUTO_UPDATE_SCRIPT" || true)

if [ -n "$EXISTING_CRON" ]; then
  echo "⚠️  定时任务已存在："
  echo "   $EXISTING_CRON"
  echo ""
  read -p "是否更新配置？(y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
  fi
  
  # 删除旧的 cron 任务
  crontab -l 2>/dev/null | grep -v -F "$AUTO_UPDATE_SCRIPT" | crontab - 2>/dev/null || true
  echo "✅ 已删除旧的定时任务"
fi

# 添加新的 cron 任务
(crontab -l 2>/dev/null | grep -v -F "$AUTO_UPDATE_SCRIPT"; echo "$CRON_JOB") | crontab - 2>/dev/null

echo ""
echo "✅ 定时任务已添加！"
echo ""
echo "📋 配置详情："
echo "   命令：$CRON_JOB"
echo "   时间：每周日 凌晨 3:00"
echo "   日志：/tmp/clawhub-update.log"
echo ""
echo "🔍 查看所有 crontab 任务："
echo "   crontab -l"
echo ""
echo "🧪 手动测试运行："
echo "   ${AUTO_UPDATE_SCRIPT} ${AGENT_WORKSPACE}"
echo ""
echo "📝 移除定时任务："
echo "   crontab -e  # 删除对应行"
echo "   或运行：./setup-cron.sh --remove"
