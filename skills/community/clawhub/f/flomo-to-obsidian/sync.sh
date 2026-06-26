#!/bin/bash
# Flomo 自动同步脚本（使用 .env 文件）

set -e  # 遇到错误立即退出

# 进入脚本所在目录
cd "$(dirname "$0")"

# 检查 .env 文件是否存在
if [ ! -f .env ]; then
    echo "❌ 错误：找不到 .env 文件"
    echo ""
    echo "请按以下步骤创建配置文件："
    echo "  1. 复制模板: cp .env.example .env"
    echo "  2. 编辑文件: nano .env"
    echo "  3. 填入你的邮箱和密码"
    echo ""
    exit 1
fi

# 加载环境变量
echo "📝 加载配置文件..."
source .env

# 检查必要的环境变量
if [ -z "$FLOMO_EMAIL" ] || [ -z "$FLOMO_PASSWORD" ]; then
    echo "❌ 错误：.env 文件中缺少必要配置"
    echo ""
    echo "请确保 .env 文件包含："
    echo "  FLOMO_EMAIL=你的邮箱"
    echo "  FLOMO_PASSWORD=你的密码"
    echo ""
    exit 1
fi

# 使用默认值
OBSIDIAN_VAULT=${OBSIDIAN_VAULT:-"/Users/ryanbzhou/mynote/flomo"}
TAG_PREFIX=${TAG_PREFIX:-"flomo/"}

echo "======================================"
echo "🚀 Flomo 自动同步"
echo "======================================"
echo "  邮箱: $FLOMO_EMAIL"
echo "  密码: ********"
echo "  输出: $OBSIDIAN_VAULT"
echo "  前缀: $TAG_PREFIX"
echo "======================================"
echo ""

# 执行同步
python scripts/auto_sync.py \
  --email "$FLOMO_EMAIL" \
  --password "$FLOMO_PASSWORD" \
  --output "$OBSIDIAN_VAULT" \
  --tag-prefix "$TAG_PREFIX" \
  "$@"  # 传递额外参数

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ 同步成功！"
else
    echo "❌ 同步失败（退出码: $EXIT_CODE）"
fi

exit $EXIT_CODE
