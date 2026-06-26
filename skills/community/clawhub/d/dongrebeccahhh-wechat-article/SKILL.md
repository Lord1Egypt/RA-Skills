---
name: wechat-article
description: 微信公众号创作技能，按照傅盛写作风格指南创作口语化、故事感、有态度的文章
version: 1.0.0
author: 小帽
grade: A
category: content
tags: [公众号, 写作, 微信, 文章]
---

# 微信公众号创作技能

按照专业风格创作公众号文章。

## 安装

```bash
clawhub search wechat-article
clawhub install wechat-article
```

## 写作流程

1. 读取写作风格指南
2. 按照傅盛写作风格创作
3. 生成适合公众号的排版格式

## 写作要点

### 风格要求
- **口语化** - 像朋友聊天一样
- **故事感** - 用故事传递观点
- **有态度** - 不是AI八股文

### 标题策略
- 悬念 > 结论
- 情感 > 理性
- 30字以内最佳

### 内容技巧
- 善用类比，让复杂的事简单化
- 数据支撑但不堆砌
- 段落简短，方便手机阅读
- 每300字左右配一张图

## 文章结构

```markdown
# 标题（30字内，含悬念）

[开头：用故事或问题吸引读者]

## 第一部分
[核心观点 + 故事/案例]

## 第二部分
[深入分析]

## 第三部分
[总结 + 行动建议]

[结尾：金句收尾]
```

## 封面图生成

```bash
uv run /usr/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "公众号封面：[标题关键词]，极简科技风" \
  --filename cover.jpg \
  --resolution 2K
```

## 发布流程

1. 创作文章内容
2. 生成封面图
3. 使用 wechat-mp-toolkit 发布

---

*技能创建时间: 2026-03-17*
