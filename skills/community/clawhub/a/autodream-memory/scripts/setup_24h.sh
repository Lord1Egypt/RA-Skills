#!/bin/bash
# AutoDream 定时任务设置脚本
# 用法：
#   ./setup_24h.sh           # 默认 24 小时
#   ./setup_24h.sh 12h       # 自定义间隔
#   ./setup_24h.sh 12h https://github.com/wanng-ide/autodream/issues/1 on  # 间隔 + 问题 URL + 启用发布

set -e

INTERVAL="${1:-24h}"
ISSUE_URL="${2:-}"
POST_ENABLED="${3:-off}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "🔧 设置 AutoDream 定时任务"
echo "   间隔：$INTERVAL"
echo "   工作区：$WORKSPACE_DIR"

# 确保配置目录存在
mkdir -p "$SKILL_DIR/config"

# 更新配置文件
cat > "$SKILL_DIR/config/config.json" << EOF
{
  "interval_hours": "$(echo $INTERVAL | sed 's/h$//')",
  "min_sessions": 5,
  "max_memory_lines": 200,
  "backup_enabled": true,
  "dry_run": false,
  "verbose": false,
  "issue_url": "$ISSUE_URL",
  "post_enabled": $([ "$POST_ENABLED" = "on" ] && echo "true" || echo "false")
}
EOF

# 确保 OpenClaw cron 脚本存在
python3 "$SKILL_DIR/scripts/ensure_openclaw_cron.py" --workspace "$WORKSPACE_DIR" --interval "$INTERVAL"

# 立即运行一次
echo ""
echo "🚀 立即运行一次 AutoDream..."
python3 "$SKILL_DIR/scripts/autodream_cycle.py" --workspace "$WORKSPACE_DIR"

echo ""
echo "✅ AutoDream 定时任务设置完成"
echo "   下次运行：约 $INTERVAL 后"
echo "   手动运行：python3 skills/autodream/scripts/autodream_cycle.py --workspace ."
