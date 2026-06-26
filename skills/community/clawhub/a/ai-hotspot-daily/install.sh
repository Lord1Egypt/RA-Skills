#!/bin/bash
# hotspot-aggregator 安装脚本

set -e

echo "🦆 安装 hotspot-aggregator 技能..."

# 创建数据目录
mkdir -p ~/.openclaw/hotspot
mkdir -p "$(dirname "$0")/data"

# 创建配置文件
if [ ! -f ~/.openclaw/hotspot/config.json ]; then
  cat > ~/.openclaw/hotspot/config.json << 'EOF'
{
  "sources": ["weibo", "zhihu", "douyin", "baidu", "36kr"],
  "topN": 20,
  "notifyUser": "",
  "cron_enabled": true
}
EOF
  echo "✅ 创建配置文件：~/.openclaw/hotspot/config.json"
fi

# 设置脚本权限
chmod +x "$(dirname "$0")/scripts/"*.js

echo ""
echo "✅ 安装完成！"
echo ""
echo "使用方法:"
echo ""
echo "  # 抓取今日热点"
echo "  node $(dirname "$0")/scripts/fetch-hotspots.js"
echo ""
echo "  # 生成日报"
echo "  node $(dirname "$0")/scripts/generate-daily-report.js --send"
echo ""
echo "  # 设置定时任务（每日 7 点抓取，8 点发布）"
echo "  openclaw cron create --schedule '0 7 * * *' --command 'node $(dirname "$0")/scripts/fetch-hotspots.js'"
echo "  openclaw cron create --schedule '0 8 * * *' --command 'node $(dirname "$0")/scripts/generate-daily-report.js --send'"
echo ""
echo "详细文档：$(dirname "$0")/SKILL.md"
