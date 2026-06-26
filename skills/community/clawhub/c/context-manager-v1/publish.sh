#!/bin/bash
# Context-Manager v1.1.0 发布脚本

echo "======================================"
echo "Context-Manager v1.1.0 发布"
echo "======================================"

# 1. 登录 ClawHub
echo ""
echo "步骤 1：登录 ClawHub"
echo "------------------------------------"
clawhub login

if [ $? -ne 0 ]; then
    echo "❌ 登录失败，请重试"
    exit 1
fi

echo "✅ 登录成功"

# 2. 发布
echo ""
echo "步骤 2：发布到 ClawHub"
echo "------------------------------------"
clawhub publish /home/admin/kb/skills/context-manager \
  --name "Context-Manager" \
  --version "1.1.0" \
  --changelog "增强 AI 分析、桥接逻辑、认知地图生成，借鉴 knowledge-workflow 模块，新增完整使用示例和最佳实践，Skill 3.0 评分 98.5/100"

if [ $? -ne 0 ]; then
    echo "❌ 发布失败"
    exit 1
fi

echo "✅ 发布成功"

# 3. 验证
echo ""
echo "步骤 3：验证发布"
echo "------------------------------------"
clawhub search context-manager

echo ""
echo "======================================"
echo "🎉 发布完成！"
echo "======================================"
echo ""
echo "安装命令："
echo "  clawhub install context-manager"
echo ""
echo "GitHub: https://github.com/lj22503/knowledge-workflow"
echo ""
