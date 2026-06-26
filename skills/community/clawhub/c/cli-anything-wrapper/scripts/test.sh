#!/bin/bash
# CLI-Anything Wrapper 测试脚本

echo "🧪 CLI-Anything Wrapper 测试"
echo "=============================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/run.py"

# 测试 1: 帮助信息
echo -e "\n📋 测试 1: 显示帮助"
python3 "$PYTHON_SCRIPT" --help

# 测试 2: 信息展示
echo -e "\n📋 测试 2: 显示信息"
python3 "$PYTHON_SCRIPT" --info

# 测试 3: 列出软件
echo -e "\n📋 测试 3: 列出支持的软件"
python3 "$PYTHON_SCRIPT" --list

echo -e "\n=============================="
echo "✅ 测试完成"
echo ""
echo "其他测试命令:"
echo "  python3 $PYTHON_SCRIPT --list --json"
echo "  python3 $PYTHON_SCRIPT --list --category AI"
echo "  python3 $PYTHON_SCRIPT --app gimp --args '--help' --dry-run"
