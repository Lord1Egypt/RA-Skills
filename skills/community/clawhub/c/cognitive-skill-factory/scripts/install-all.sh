#!/bin/bash

# 认知 Skill 工厂 - 批量安装脚本

echo "🚀 开始安装认知 Skill 工厂..."
echo ""

# 定义 Skill 列表
SKILLS=(
  "zhang-yiming-perspective"
  "huang-zheng-perspective"
  "ma-huateng-perspective"
  "ren-zhengfei-perspective"
  "sequoia-investment-framework"
  "lei-jun-perspective"
  "wang-xing-perspective"
  "zhang-lei-perspective"
  "hillhouse-investment-framework"
  "bytedance-organization-framework"
)

# 批量安装
for skill in "${SKILLS[@]}"; do
  echo "📦 安装 $skill ..."
  clawhub install "$skill" -y
  if [ $? -eq 0 ]; then
    echo "✅ $skill 安装成功"
  else
    echo "❌ $skill 安装失败"
  fi
  echo ""
done

echo "🎉 认知 Skill 工厂安装完成！"
echo ""
echo "💡 使用示例："
echo "  用张一鸣思维分析：用张一鸣的视角分析 AI 创业"
echo "  用红杉框架评估：用红杉的视角评估这个项目"
echo ""
