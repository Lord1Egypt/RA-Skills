#!/bin/bash
# Auth Guard 快速安装脚本

set -e

echo "========================================="
echo "  Auth Guard 安装脚本"
echo "========================================="
echo ""

# 检测操作系统
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    IS_WINDOWS=true
    echo "检测到 Windows 系统"
else
    IS_WINDOWS=false
    echo "检测到 Unix/Linux 系统"
fi

# 1. 创建配置目录
echo "✓ 创建配置目录..."
if [ "$IS_WINDOWS" = true ]; then
    mkdir -p "$USERPROFILE/.auth_guard"
    mkdir -p "$USERPROFILE/.auth_guard/decisions"
else
    mkdir -p ~/.auth_guard
    mkdir -p ~/.auth_guard/decisions
fi

# 2. 复制配置文件
echo "✓ 复制配置文件..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ "$IS_WINDOWS" = true ]; then
    cp "$SCRIPT_DIR/config.example.json" "$USERPROFILE/.auth_guard/config.json"
    cp "$SCRIPT_DIR/whitelist.example.json" "$USERPROFILE/.auth_guard_whitelist.json"
else
    cp "$SCRIPT_DIR/config.example.json" ~/.auth_guard/config.json
    cp "$SCRIPT_DIR/whitelist.example.json" ~/.auth_guard_whitelist.json
fi

# 3. 安装 Python 依赖
echo "✓ 安装 Python 依赖..."
pip install requests --quiet

# 4. 设置环境变量（可选）
echo ""
echo "⚠️  可选：设置环境变量"
echo ""
echo "将以下内容添加到你的 shell 配置文件："
echo ""
echo "  export AUTH_GUARD_ENABLED=true"
echo "  export AUTH_GUARD_MODE=STRICT"
echo "  export AUTH_GUARD_TIMEOUT=300"
echo ""

# 5. 测试安装
echo "✓ 测试安装..."
cd "$SCRIPT_DIR"
python cli.py status

echo ""
echo "========================================="
echo "  ✅ 安装完成！"
echo "========================================="
echo ""
echo "下一步："
echo "1. 编辑 ~/.auth_guard/config.json 配置飞书 webhook"
echo "2. 运行 'python cli.py status' 查看状态"
echo "3. 阅读 README.md 了解使用方法"
echo ""
