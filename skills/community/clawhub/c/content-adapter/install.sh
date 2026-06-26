#!/bin/bash
# 多平台内容适配器 Skill 安装脚本
# Content Adapter

set -e

SKILL_NAME="content-adapter"
SKILL_DIR="$HOME/.openclaw/workspace/skills/$SKILL_NAME"

echo ""
echo "═══════════════════════════════════════════════════"
echo "  多平台内容适配器 Skill"
echo "  Content Adapter"
echo "═══════════════════════════════════════════════════"
echo ""
echo "  一次编写，多平台发布"
echo ""
echo "═══════════════════════════════════════════════════"
echo ""

# 检查目录是否存在
if [ -d "$SKILL_DIR" ]; then
  echo "📁 Skill 目录已存在，正在更新..."
else
  echo "📁 创建 Skill 目录..."
  mkdir -p "$SKILL_DIR"
fi

# 复制文件
echo "📄 安装 SKILL.md..."
cat > "$SKILL_DIR/SKILL.md" << 'SKILL_EOF'
---
name: content-adapter
display_name: 多平台内容适配器
description: 一次编写，多平台发布。自动将原始内容适配成小红书、公众号、知乎、微博、抖音等平台风格。
version: 1.0.0
author: 叶建国
homepage: https://github.com/openclaw/content-adapter
tags:
  - 内容创作
  - 多平台分发
  - 小红书
  - 公众号
license: MIT
compatibility:
  - openclaw
  - skillhub
---

# 多平台内容适配器

> 📝 一次编写 | 多平台发布 | 智能适配 | 风格各异

## 简介

将原始内容自动适配成不同平台的内容风格。

## 支持平台

| 平台 | 字数建议 | 特点 |
|------|----------|------|
| 小红书 | 200-1000 | 种草笔记、emoji丰富 |
| 公众号 | 1000-3000 | 长文、深度、排版 |
| 知乎 | 500-2000 | 问答、专业、结构 |
| 微博 | 50-200 | 短平快、话题标签 |
| 抖音 | 50-150 | 短视频文案、钩子 |
| B站 | 200-800 | 弹幕文化、玩梗 |
| 头条 | 300-1500 | 资讯、标题党 |

## 使用方式

输入原始内容 + 目标平台，自动生成适配版本。

SKILL_EOF

echo ""
echo "═══════════════════════════════════════════════════"
echo "  ✅ 安装完成！"
echo "═══════════════════════════════════════════════════"
echo ""
echo "📚 使用说明："
echo ""
echo "  当用户提到以下关键词时自动触发："
echo "    - 帮我改写成小红书风格"
echo "    - 适配成公众号格式"
echo "    - 生成微博版本"
echo "    - 多平台分发"
echo "    - 内容同步"
echo ""
echo "📖 完整文档请阅读："
echo "    $SKILL_DIR/SKILL.md"
echo ""
echo "═══════════════════════════════════════════════════"