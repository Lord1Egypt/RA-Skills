#!/bin/bash

# OpenClaw 技能安装脚本
# 用于注册 call-aida-app 技能

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_HOME="${HOME}/.openclaw"
SKILL_NAME="call-aida-app"

echo "🦞 OpenClaw 技能安装器"
echo "================================"
echo ""
echo "技能名称: $SKILL_NAME"
echo "技能位置: $SKILL_DIR"
echo ""

# 检查 OpenClaw 是否已安装
if [ ! -d "$OPENCLAW_HOME" ]; then
    echo "❌ 错误: OpenClaw 未安装或目录不存在"
    echo "   预期位置: $OPENCLAW_HOME"
    exit 1
fi

# 确保脚本有执行权限
chmod +x "$SKILL_DIR/call_aida_app.py"
echo "✓ 脚本已设置为可执行"

# 验证 Python 3 可用
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "   请安装 Python 3.6 或更高版本"
    exit 1
fi

# 检查 Python 版本
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ 找到 Python $PYTHON_VERSION"

# 验证 Python 脚本语法
echo "验证脚本..."
if python3 -m py_compile "$SKILL_DIR/call_aida_app.py"; then
    echo "✓ Python 脚本语法正确"
else
    echo "❌ Python 脚本有错误"
    exit 1
fi

# 测试脚本可以正常执行（无参数应该返回错误消息）
echo "测试脚本..."
TEST_OUTPUT=$(python3 "$SKILL_DIR/call_aida_app.py" 2>&1)
if echo "$TEST_OUTPUT" | grep -q "success"; then
    echo "✓ 脚本执行正常"
else
    echo "⚠ 警告: 脚本输出异常"
    echo "  $TEST_OUTPUT" | head -3
fi

# 创建符号链接（可选）
read -p "是否在 OpenClaw 主目录创建符号链接？ (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    LINKS_DIR="$OPENCLAW_HOME/skills"
    if [ ! -d "$LINKS_DIR" ]; then
        mkdir -p "$LINKS_DIR"
    fi

    if [ -L "$LINKS_DIR/$SKILL_NAME" ]; then
        echo "移除现有符号链接..."
        rm "$LINKS_DIR/$SKILL_NAME"
    fi

    ln -s "$SKILL_DIR" "$LINKS_DIR/$SKILL_NAME"
    echo "✓ 符号链接已创建: $LINKS_DIR/$SKILL_NAME"
fi

echo ""
echo "================================"
echo "✅ 技能安装完成！"
echo ""
echo "下一步："
echo "1. 查看文档:"
echo "   cat $SKILL_DIR/SKILL.md"
echo ""
echo "2. 快速开始:"
echo "   cat $SKILL_DIR/README.zh.md"
echo ""
echo "3. 测试技能:"
echo "   python3 $SKILL_DIR/call_aida_app.py --help"
echo ""
echo "4. 在 OpenClaw 中使用:"
echo "   echo '{\"appid\": \"your-appid\", \"inputs\": {}}' \\"
echo "     | python3 $SKILL_DIR/call_aida_app.py"
echo ""

