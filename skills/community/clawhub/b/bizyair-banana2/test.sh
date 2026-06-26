#!/bin/bash
# 快速测试脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/scripts/bizyair_gen.py"

echo "🧪 BizyAir Banana 2 测试"
echo "======================"
echo ""

# 检查 API Key
if [ -z "$BIZYAIR_API_KEY" ]; then
    echo "⚠️  未设置 BIZYAIR_API_KEY 环境变量"
    echo ""
    echo "请先配置："
    echo "  export BIZYAIR_API_KEY=\"your_key\""
    echo ""
    echo "或创建配置文件："
    echo "  cp $SCRIPT_DIR/.env.example $SCRIPT_DIR/.env"
    echo "  编辑 .env 填入 API Key"
    echo ""
    exit 1
fi

# 测试命令
echo "运行测试命令..."
echo ""

python3 "$PYTHON_SCRIPT" \
    --prompt "测试生成，高质量，细节丰富" \
    --image "$SCRIPT_DIR/test_output.png" \
    --ar 1:1 \
    --timeout 60 \
    --json

echo ""
echo "✅ 测试完成！"
