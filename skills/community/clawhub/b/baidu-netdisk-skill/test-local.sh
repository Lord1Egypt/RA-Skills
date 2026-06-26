#!/bin/bash

# 百度网盘 Skill 本地测试脚本
# 用法：./test-local.sh

set -e

echo "=========================================="
echo "🦞 百度网盘 Skill 本地测试"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# 检查依赖
echo "📦 检查依赖..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    exit 1
fi

if [ ! -d "node_modules" ]; then
    echo "⚠️  依赖未安装，正在安装..."
    npm install
fi

echo "✅ 依赖检查通过"
echo ""

# 检查配置
echo "🔧 检查配置..."
CONFIG_FILE="$HOME/.config/configstore/baidu-netdisk-skill.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "⚠️  配置文件不存在，请先运行授权："
    echo ""
    echo "   node src/auth.js"
    echo ""
    echo "   或配置 API Key："
    echo ""
    echo "   node src/index.js config -k <API_KEY> -s <SECRET_KEY>"
    echo ""
    exit 1
fi

echo "✅ 配置文件存在：$CONFIG_FILE"
echo ""

# 显示配置（隐藏敏感信息）
echo "📋 当前配置："
cat "$CONFIG_FILE" | jq -r '
  "  API Key: " + (if .apiKey then (.apiKey[0:8] + "...") else "未设置" end) +
  "\n  Secret Key: " + (if .secretKey then (.secretKey[0:8] + "...") else "未设置" end) +
  "\n  Access Token: " + (if .accessToken then (.accessToken[0:8] + "...") else "未设置" end) +
  "\n  Refresh Token: " + (if .refreshToken then (.refreshToken[0:8] + "...") else "未设置" end) +
  "\n  Token 过期时间： " + (if .tokenExpires then (.tokenExpires | tostring) else "未设置" end)
' 2>/dev/null || echo "  （无法解析 JSON）"
echo ""

# 测试 whoami
echo "=========================================="
echo "🧪 测试 1: 用户信息 (whoami)"
echo "=========================================="
node src/index.js whoami
echo ""

# 测试 list
echo "=========================================="
echo "🧪 测试 2: 列出根目录文件 (list /)"
echo "=========================================="
node src/index.js list / --limit 5
echo ""

# 测试 search
echo "=========================================="
echo "🧪 测试 3: 搜索文件 (search)"
echo "=========================================="
echo "搜索关键词：测试"
node src/index.js search "测试" || echo "（未找到匹配文件）"
echo ""

# 测试缓存
echo "=========================================="
echo "🧪 测试 4: 缓存机制"
echo "=========================================="
echo "第一次请求（可能调用 API）："
node src/index.js list / --limit 1
echo ""
echo "第二次请求（应该使用缓存）："
node src/index.js list / --limit 1
echo ""

# 测试完成
echo "=========================================="
echo "✅ 所有测试完成！"
echo "=========================================="
echo ""
echo "📊 测试结果总结："
echo "  - whoami: 请检查上方输出"
echo "  - list: 请检查上方输出"
echo "  - search: 请检查上方输出"
echo "  - cache: 请检查是否显示'使用缓存'"
echo ""
echo "如有错误，请检查："
echo "  1. API Key 和 Secret Key 是否正确"
echo "  2. Access Token 是否过期"
echo "  3. 百度应用是否已审核（未审核可能部分 API 受限）"
echo ""
