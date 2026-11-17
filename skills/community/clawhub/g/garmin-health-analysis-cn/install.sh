#!/usr/bin/env bash
# 佳明健康数据分析 - 技能（Skill）安装脚本
# 请在将本技能克隆到技能目录后运行本脚本

set -e  # 出错即退出

echo "🏃 正在安装佳明健康数据分析技能..."
echo

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：本脚本需要 Python 3，但未找到"
    exit 1
fi

echo "✓ 检测到 Python 3：$(python3 --version)"

# 安装 Python 依赖
echo
echo "📦 正在安装 Python 依赖..."

if pip3 install --user garminconnect fitparse gpxpy 2>/dev/null; then
    echo "✓ 依赖安装完成（--user 方式）"
elif pip3 install --break-system-packages garminconnect fitparse gpxpy 2>/dev/null; then
    echo "✓ 依赖安装完成（--break-system-packages 方式）"
elif pip3 install garminconnect fitparse gpxpy 2>/dev/null; then
    echo "✓ 依赖安装完成（系统范围）"
else
    echo "❌ 安装 Python 依赖失败"
    echo "   请手动执行：pip3 install --user garminconnect fitparse gpxpy"
    exit 1
fi

# 如果不存在配置文件，则从模板创建
if [ ! -f "config.json" ] && [ -f "config.example.json" ]; then
    echo
    echo "📝 正在根据模板创建 config.json..."
    cp config.example.json config.json
    echo "✓ config.json 已创建（请编辑填入你的佳明账号信息）"
fi

# 完成
echo
echo "✅ 安装完成！"
echo
echo "接下来的步骤："
echo "  1. 填入你的佳明账号信息："
echo "     - 编辑 config.json，或者"
echo "     - 设置 GARMIN_EMAIL 和 GARMIN_PASSWORD 环境变量，或者"
echo "     - 或添加到你所用 AI 助手的技能配置中（若支持，如 OpenClaw 的 ~/.clawdbot/clawdbot.json）"
echo
echo "  2. 登录认证："
echo "     python3 scripts/garmin_auth.py login"
echo
echo "  3. 测试："
echo "     python3 scripts/garmin_data.py summary --days 7"
echo
echo "📖 完整说明请阅读 SKILL.md"
