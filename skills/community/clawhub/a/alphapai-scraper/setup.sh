#!/bin/bash
# Alpha派爬虫 Setup 脚本
# 用法: bash setup.sh

set -e

SKILL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPTS_DIR="$SKILL_DIR/scripts"

echo "🦀 AlphaPai Skill Setup"
echo "=================================="

# 1. 检查 Python 版本
echo "🐍 检查 Python 环境..."
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 未安装，请先安装 Python 3.9+"
    exit 1
fi
PYTHON_VER=$(python3 --version 2>&1)
echo "   ✅ $PYTHON_VER"

# 2. 安装依赖
echo ""
echo "📦 安装 Python 依赖..."
pip3 install playwright --quiet && echo "   ✅ playwright 已安装"

echo ""
echo "🌐 安装 Playwright 浏览器驱动..."
python3 -m playwright install chromium
echo "   ✅ Chromium 驱动已安装"

# 3. 创建输出目录
echo ""
echo "📁 创建默认输出目录..."
mkdir -p ~/.openclaw/data/alphapai-scraper/raw
mkdir -p ~/.openclaw/data/alphapai-scraper/reports
mkdir -p ~/.openclaw/data/alphapai-scraper/normalized
mkdir -p ~/.openclaw/data/alphapai-scraper/index
mkdir -p ~/.openclaw/data/alphapai-scraper/runtime
echo "   ✅ ~/.openclaw/data/alphapai-scraper 已创建"

echo ""
echo "🧩 准备本地配置模板..."
[ -f "$SKILL_DIR/config/settings.local.json" ] || cp "$SKILL_DIR/config/settings.example.json" "$SKILL_DIR/config/settings.local.json"
[ -f "$SKILL_DIR/config/token.local.json" ] || cp "$SKILL_DIR/config/token.example.json" "$SKILL_DIR/config/token.local.json"
[ -f "$SKILL_DIR/config/cookies.local.json" ] || cp "$SKILL_DIR/config/cookies.example.json" "$SKILL_DIR/config/cookies.local.json"
[ -f "$SKILL_DIR/config/credentials.local.json" ] || cp "$SKILL_DIR/config/credentials.example.json" "$SKILL_DIR/config/credentials.local.json"
echo "   ✅ 已生成本地配置模板（不会覆盖已有文件）"

# 4. 添加 alias
echo ""
echo "⚡ 配置 update_alpha 快捷命令..."

ALIAS_LINE="alias update_alpha='ALPHAPAI_OUTPUT_DIR=~/.openclaw/data/alphapai-scraper python3 $SCRIPTS_DIR/run.py'"

# 检测 shell 类型
if [ -n "$ZSH_VERSION" ] || [ "$SHELL" = "/bin/zsh" ]; then
    RC_FILE="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ] || [ "$SHELL" = "/bin/bash" ]; then
    RC_FILE="$HOME/.bashrc"
    # macOS 默认用 .bash_profile
    [ -f "$HOME/.bash_profile" ] && RC_FILE="$HOME/.bash_profile"
else
    RC_FILE="$HOME/.profile"
fi

# 避免重复添加
if grep -q "alias update_alpha=" "$RC_FILE" 2>/dev/null; then
    # 更新已有的 alias
    sed -i.bak "s|alias update_alpha=.*|$ALIAS_LINE|g" "$RC_FILE"
    echo "   ✅ update_alpha 已更新在 $RC_FILE"
else
    echo "" >> "$RC_FILE"
    echo "# Alpha派爬虫快捷命令" >> "$RC_FILE"
    echo "$ALIAS_LINE" >> "$RC_FILE"
    echo "   ✅ update_alpha 已添加到 $RC_FILE"
fi

echo ""
echo "=================================="
echo "🎉 Setup 完成！"
echo ""
echo "使用方法："
echo "  1. 重新打开终端，或执行: source $RC_FILE"
echo "  2. 先填写 config/*.local.json 中你要使用的认证方式"
echo "  3. 输入: update_alpha 进行抓取，或 update_alpha --query 英伟达 --days 7 进行查询"
echo ""
echo "注意："
echo "  ⚠️  优先推荐配置 USER_AUTH_TOKEN，其次 cookies，再次账号密码"
echo "  📍 默认输出目录: ~/.openclaw/data/alphapai-scraper/"
echo "=================================="
