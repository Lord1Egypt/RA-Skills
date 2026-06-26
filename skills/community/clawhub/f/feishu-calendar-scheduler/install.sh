#!/bin/bash
# 飞书日历智能调度器安装脚本

set -e

echo "🚀 开始安装飞书日历智能调度器..."

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要 Python3，请先安装"
    exit 1
fi

# 检查 OpenClaw
if ! command -v openclaw &> /dev/null; then
    echo "❌ 需要 OpenClaw，请先安装"
    exit 1
fi

# 检查飞书插件
if ! openclaw tools list | grep -q "feishu_calendar"; then
    echo "⚠️  未检测到飞书日历插件，请确保已安装飞书插件"
    echo "   运行: openclaw plugins install feishu-openclaw-plugin"
fi

# 安装 Python 依赖
echo "📦 安装 Python 依赖..."
pip3 install pytz || {
    echo "⚠️  无法安装 pytz，尝试使用系统包管理器"
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y python3-pytz || true
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-pytz || true
    fi
}

# 创建配置目录
CONFIG_DIR="$HOME/.openclaw/feishu-calendar-scheduler"
mkdir -p "$CONFIG_DIR"

# 复制脚本文件
echo "📁 复制脚本文件..."
cp -r scripts/* "$CONFIG_DIR/" 2>/dev/null || true

# 创建配置文件
if [ ! -f "$CONFIG_DIR/config.json" ]; then
    cat > "$CONFIG_DIR/config.json" << EOF
{
  "version": "1.0.0",
  "work_hours": {
    "start": 9,
    "end": 18
  },
  "preferred_days": ["周二", "周三", "周四"],
  "avoid_days": ["周一", "周五"],
  "trial_expires": "$(date -d "+7 days" +%Y-%m-%d)",
  "license_key": null
}
EOF
fi

# 设置执行权限
chmod +x "$CONFIG_DIR/recommend.py" 2>/dev/null || true

# 创建 OpenClaw 命令别名
echo "🔧 配置 OpenClaw 命令..."
cat > "$CONFIG_DIR/openclaw-commands.json" << EOF
{
  "commands": {
    "calendar-recommend": {
      "description": "推荐会议时间",
      "script": "python3 $CONFIG_DIR/recommend.py"
    },
    "calendar-batch": {
      "description": "批量管理会议",
      "script": "echo '批量管理功能开发中...'"
    },
    "calendar-report": {
      "description": "生成会议报表",
      "script": "echo '报表功能开发中...'"
    }
  }
}
EOF

# 注册到 OpenClaw
if [ -d "$HOME/.openclaw/skills" ]; then
    echo "📝 注册到 OpenClaw 技能目录..."
    ln -sf "$(pwd)" "$HOME/.openclaw/skills/feishu-calendar-scheduler" || true
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "🎉 飞书日历智能调度器已成功安装"
echo ""
echo "📅 可用命令："
echo "   openclaw calendar-recommend --start '2026-03-17T09:00:00' --end '2026-03-17T18:00:00' --duration 60"
echo "   openclaw calendar-batch"
echo "   openclaw calendar-report"
echo ""
echo "📋 开始7天免费试用，试用期至: $(date -d "+7 days" "+%Y年%m月%d日")"
echo ""
echo "❓ 帮助：查看 https://clawhub.com/skills/feishu-calendar-scheduler"
echo "📧 支持：support@clawhub.com"
echo ""