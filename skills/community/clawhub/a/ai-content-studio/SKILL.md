---
name: ai-content-studio
description: AI全链路内容工坊 — 多平台内容一键创作与发布自动化工作流，涵盖选题研究、文章撰写、知识卡片生成、全平台发布。
category: AI
triggers: 全平台内容创作, 多平台发布, 选题到发布, 内容工作室, 公众号+小红书, 全链路内容
version: 1.0.0
author: OpenClaw Agent
tags:
  - content-creation
  - xiaohongshu
  - wechat-article
  - automation
  - multi-platform
  - workflow
dependencies:
  - agent-reach
  - summarize
  - wechat-article-pro
  - card-renderer
  - xiaohongshutools
---

# AI 全链路内容工坊 (AI Content Studio)

一条命令完成从**选题研究 → 深度文章撰写 → 视觉卡片生成 → 多平台发布**的完整内容工作流。

## 核心价值

- **一键多平台**：同时覆盖微信公众号 + 小红书，无需手动切换工具
- **AI 选题研究**：自动追踪热点、提取核心观点，告别"不知道写什么"
- **专业级内容**：参考刘润等头部公众号风格撰写 3000-5000 字深度文章
- **视觉化传播**：自动生成多风格知识卡片，提升小红书笔记吸引力

## 适用场景

- 内容创作者需要高效产出双平台内容
- 品牌运营需要保持公众号 + 小红书内容同步更新
- 个人 IP 打造者希望建立系统化的内容生产流程
- 企业市场部需要快速生产高质量行业内容

## 工作流程（5步）

```
Step 1 → 选题研究（agent-reach + summarize）
   ↓
Step 2 → 撰写公众号深度文章（wechat-article-pro）
   ↓
Step 3 → 生成小红书知识卡片（card-renderer）
   ↓
Step 4 → 生成小红书文案（summarize + AI生成）
   ↓
Step 5 → 发布至双平台（wechat-article-pro + xiaohongshutools）
```

## 使用方法

### 方式一：完整工作流（推荐）

触发词：
- "帮我创作全平台内容，主题是 XXX"
- "从选题到发布，帮我做一期内容"
- "AI内容工作室，主题 XXX"

执行完整流程：选题研究 → 公众号文章 → 知识卡片 → 小红书文案 → 双平台发布

### 方式二：分步执行

**Step 1：选题研究**
```
# 使用 agent-reach 搜索热点
agent-reach search --platform xiaohongshu --query "AI工具 热点"
agent-reach search --platform weibo --query "AI工具 热点"
agent-reach search --platform rss --query "https://rsshub.app/36kr/posts"
```

**Step 2：撰写公众号文章**
```
激活 wechat-article-pro skill，按刘润风格撰写深度文章
```

**Step 3：生成知识卡片**
```
# 使用 card-renderer 生成卡片
python3 scripts/render_cyber_card.py "标题" "副标题" "/tmp/content.md" "/tmp/cards/"
python3 scripts/render_mac_pro_card.py "标题" "副标题" "/tmp/content.md" "/tmp/cards/"
```

**Step 4：发布小红书**
```
激活 xiaohongshutools skill，发布图文内容
```

## 技术架构

| 层级 | 组件 | 职责 |
|------|------|------|
| 数据层 | agent-reach | 全网热点追踪，跨平台信息采集 |
| 理解层 | summarize | 内容提取、智能摘要、观点凝练 |
| 内容层 | wechat-article-pro | 公众号深度文章撰写与排版 |
| 视觉层 | card-renderer | 多风格知识卡片批量生成 |
| 发布层 | xiaohongshutools | 小红书内容发布与互动管理 |

## 示例主题

```
输入：帮我创作全平台内容，主题是"AI Agent 在企业中的落地现状与前景"
输出：
  ✅ 公众号文章（4000字，刘润风格）
  ✅ 小红书知识卡片（3张，赛博朋克风格）
  ✅ 小红书文案（800字，含热门话题标签）
  ✅ 自动发布至公众号 + 小红书
```

## 注意事项

1. 首次使用需配置各平台 API 凭证（agent-reach、xiaohongshutools）
2. 公众号发布需要微信公众号后台授权
3. 小红书发布建议配合人工审核，避免误发
4. 热点追踪建议设置每日定时任务，保持内容新鲜度
