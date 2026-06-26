#!/bin/bash
# email-163-com 安装脚本
# 版本：1.0.4

set -e

SKILL_DIR="$HOME/.openclaw/workspace/skills/email-163-com"
BIN_DIR="$HOME/.local/bin"
CONFIG_DIR="$HOME/.config/email-163-com"

echo "📧 Installing email-163-com v1.0.4..."

# 创建技能目录
mkdir -p "$SKILL_DIR"

# 复制文件（排除安装脚本自身）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for file in "$SCRIPT_DIR"/*; do
    filename=$(basename "$file")
    if [ "$filename" != "INSTALL.sh" ] && [ "$filename" != "install.sh" ]; then
        cp -r "$file" "$SKILL_DIR/"
    fi
done

# 创建软链接
mkdir -p "$BIN_DIR"
ln -sf "$SKILL_DIR/email-163-com" "$BIN_DIR/email-163-com"

# 设置执行权限
chmod +x "$SKILL_DIR/email-163-com"
chmod +x "$SKILL_DIR/main.py"

# 创建配置目录
mkdir -p "$CONFIG_DIR"

# 设置配置文件权限（如果存在）
if [ -f "$CONFIG_DIR/config.json" ]; then
    chmod 600 "$CONFIG_DIR/config.json"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "📁 安装位置：$SKILL_DIR"
echo "🔗 命令链接：$BIN_DIR/email-163-com"
echo "⚙️  配置文件：$CONFIG_DIR/config.json"
echo ""
echo "📋 下一步:"
echo "   1. 配置邮箱：email-163-com init"
echo "   2. 测试安装：email-163-com --help"
echo "   3. 读取邮件：email-163-com read --count 5"
echo ""
