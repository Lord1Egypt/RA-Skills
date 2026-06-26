#!/bin/bash
# 测试快手/B 站/抖音视频发布脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DATA_DIR="$SCRIPT_DIR/../test_data"
CONFIG_FILE="$TEST_DATA_DIR/描述.txt"

echo "======================================"
echo "快手/B 站/抖音视频发布脚本 - 测试"
echo "======================================"
echo ""

# 检查配置文件
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ 配置文件不存在：$CONFIG_FILE"
    exit 1
fi

echo "✅ 配置文件：$CONFIG_FILE"
cat "$CONFIG_FILE"
echo ""

# 检查视频文件
VIDEO_PATH=$(grep "视频数据路径：" "$CONFIG_FILE" | cut -d'：' -f2 | tr -d ' ')
if [ ! -f "$VIDEO_PATH" ]; then
    echo "❌ 视频文件不存在：$VIDEO_PATH"
    exit 1
fi
echo "✅ 视频文件：$VIDEO_PATH ($(du -h "$VIDEO_PATH" | cut -f1))"

# 检查封面文件
COVER_PATH=$(grep "封面：" "$CONFIG_FILE" | cut -d'：' -f2 | tr -d ' ')
if [ -n "$COVER_PATH" ] && [ -f "$COVER_PATH" ]; then
    echo "✅ 封面文件：$COVER_PATH"
else
    echo "⚠️  封面文件未配置或不存在"
fi

echo ""
echo "======================================"
echo "运行测试（只填写表单，不发布）"
echo "======================================"
echo ""

cd "$SCRIPT_DIR"

# 测试 B 站发布（只填写表单）
echo "📺 测试 B 站发布..."
python cli.py publish-bilibili \
    --config "$CONFIG_FILE" \
    --no-publish \
    --wait-timeout 60 \
    || echo "⚠️  B 站测试未完成（可能是选择器问题或页面结构变更）"

echo ""
echo "======================================"
echo "测试完成！"
echo "======================================"
echo ""
echo "下一步："
echo "1. 打开 Chrome 浏览器，确保已登录对应平台"
echo "2. 运行以下命令进行实际发布："
echo ""
echo "   # 快手发布"
echo "   python cli.py publish-kuaishou --config $CONFIG_FILE"
echo ""
echo "   # B 站发布"
echo "   python cli.py publish-bilibili --config $CONFIG_FILE"
echo ""
echo "   # 抖音发布"
echo "   python cli.py publish-douyin --config $CONFIG_FILE"
echo ""
echo "   # 一键发布到所有平台"
echo "   python cli.py publish-all --config $CONFIG_FILE"
echo ""
