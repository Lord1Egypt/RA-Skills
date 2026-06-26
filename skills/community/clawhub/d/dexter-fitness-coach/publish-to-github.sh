#!/bin/bash
# 发布到GitHub的脚本

echo "🚀 AI健身教练 - 发布到GitHub"
echo "================================"
echo ""
echo "请在GitHub上创建仓库: https://github.com/new"
echo "- 仓库名: fitness-coach (或 dexter-fitness-coach)"
echo "- 可见性: Public (必须公开)"
echo "- 不要勾选任何初始化选项"
echo ""
echo "创建完成后，输入你的GitHub用户名:"
read GITHUB_USERNAME

echo ""
echo "正在关联远程仓库..."
git remote add origin https://github.com/${GITHUB_USERNAME}/fitness-coach.git

echo ""
echo "正在推送到GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ 发布完成！"
echo ""
echo "现在在飞书OpenClaw中，使用以下命令安装:"
echo "  /install dexter-fitness-coach"
echo ""
echo "或直接搜索: dexter-fitness-coach / 健身 / fitness"
