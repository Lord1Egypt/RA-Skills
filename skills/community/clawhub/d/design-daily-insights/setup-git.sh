#!/bin/bash

# Design Digest - GitHub 发布脚本

echo "🎨 Design Digest - GitHub 发布脚本"
echo "================================"
echo ""

# 检查是否在正确目录
if [ ! -f "SKILL.md" ]; then
  echo "❌ 错误：请在 design-digest 目录运行此脚本"
  exit 1
fi

# 初始化 git
echo "📦 初始化 Git 仓库..."
git init

# 添加所有文件
echo "📝 添加文件..."
git add .

# 首次提交
echo "✅ 首次提交..."
git commit -m "initial release: Design Digest v1.0.0

- 追踪 19 个设计/AI 信息源
- 支持双语摘要输出
- 智能去重和自动清理
- 零配置安装"

echo ""
echo "🎉 仓库初始化完成！"
echo ""
echo "下一步："
echo "1. 在 GitHub 创建新仓库：https://github.com/new"
echo "2. 运行以下命令关联远程仓库："
echo ""
echo "   git remote add origin https://github.com/你的用户名/design-digest.git"
echo ""
echo "3. 推送到 GitHub："
echo ""
echo "   git push -u origin main"
echo ""
echo "4. （可选）发布到 ClawHub："
echo ""
echo "   clawhub publish ./design-daily"
echo ""
