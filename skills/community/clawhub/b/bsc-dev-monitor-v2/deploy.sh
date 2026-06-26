#!/bin/bash

# BSC Dev Monitor Skill - 部署脚本

echo "🚀 准备部署 BSC Dev Monitor Skill 到 ClawHub..."

cd "$(dirname "$0")"

# 检查必要文件
echo "📋 检查必要文件..."

files=("SKILL.md" "index.js" "package.json" "README.md")
missing_files=()

for file in "${files[@]}"; do
  if [ ! -f "$file" ]; then
    missing_files+=("$file")
  fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
  echo "❌ 缺少必要文件:"
  printf '   - %s\n' "${missing_files[@]}"
  exit 1
fi

echo "✅ 所有必要文件检查完成"

# 检查 ClawHub CLI
if ! command -v clawhub &> /dev/null; then
  echo "⚠️  ClawHub CLI 未安装"
  echo "📦 正在安装..."
  npm install -g @clawhub/cli
fi

echo "✅ ClawHub CLI 已就绪"

# 提示用户登录
echo ""
echo "📝 准备发布到 ClawHub"
echo "请确保你已登录 ClawHub（如未登录，将提示登录）"
echo ""

# 发布 Skill
echo "🚀 正在发布..."
clawhub publish .

if [ $? -eq 0 ]; then
  echo ""
  echo "🎉 发布成功！"
  echo ""
  echo "📦 Skill 信息:"
  echo "   名称: bsc-dev-monitor"
  echo "   版本: 1.0.0"
  echo "   定价: 0.001 USDT / 次"
  echo ""
  echo "🔗 查看 Skill: https://clawhub.com/skill/bsc-dev-monitor"
  echo ""
  echo "💡 用户可以搜索 'bsc-dev-monitor' 安装使用"
else
  echo ""
  echo "❌ 发布失败，请检查错误信息"
  echo "💡 也可以手动上传到 https://clawhub.com/publish"
fi
