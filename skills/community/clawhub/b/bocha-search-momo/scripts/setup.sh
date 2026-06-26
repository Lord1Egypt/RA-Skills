#!/bin/bash
# 博查搜索技能配置脚本
# 用法: ./setup.sh <你的APIKey>

API_KEY="${1:-}"

if [[ -z "$API_KEY" ]]; then
    echo "Usage: ./setup.sh <你的APIKey>"
    echo ""
    echo "获取 API Key: https://open.bocha.cn"
    exit 1
fi

# 保存到配置文件
CONFIG_DIR="$HOME/.openclaw/skills-config"
mkdir -p "$CONFIG_DIR"

cat > "$CONFIG_DIR/bocha-search.json" << JSON
{
  "apiKey": "$API_KEY"
}
JSON

echo "✅ 配置已保存到 $CONFIG_DIR/bocha-search.json"
echo ""
echo "使用方式:"
echo "  source ~/.openclaw/skills/bocha-search/scripts/env.sh"
echo "  bocha-search \"搜索关键词\""
