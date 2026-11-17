---
name: podcast-generation
description: 播客制作：选题策划、大纲设计、采访问题、后期编辑、发布与分发
source:
  type: derived
  repo: skills-repo/content-creator
  path: skills/podcast-generation/SKILL.md
  url: https://skills.sh/bytedance/deer-flow/podcast-generation
  version: 1.0.0
  updated: 2026-07-30
metadata:
  author: hope
  category: 内容创作
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-30
tags:
  - podcast
  - audio
  - content-creation
  - interview
---

# Podcast Generation — 播客制作

> 播客是建立个人品牌和专业权威的高杠杆媒体。不需要录音棚，不需要昂贵的设备——好的内容和好的结构才是核心。本技能帮你从零制作一档专业播客。

## 能力

- **选题策划**：节目定位、目标听众画像、内容类型（单人/采访/圆桌）、频次策略
- **大纲设计**：单集结构（Intro → Hook → Main → Key Insight → Outro）、时间分配
- **采访问题**：开放式问题设计、追问技巧、嘉宾调研、对话节奏控制
- **后期编辑**：降噪、音量均衡、口癖去除、音乐/音效过渡
- **Show Notes 撰写**：摘要、章节标记、资源链接、嘉宾简介
- **发布与分发**：RSS 配置、多平台分发（Apple/Spotify/小宇宙）、播客 SEO

## 使用方式

在 Claude Code 中使用 `/podcast-generation` 调用。

```
/podcast-generation 帮我策划一档面向独立开发者的播客
/podcast-generation 设计这期嘉宾采访的问题大纲
/podcast-generation 帮我写这期播客的 Show Notes
```

## 工作流

1. **节目前** — 选题 → 调研（嘉宾/话题） → 大纲 → 问题设计
2. **录制中** — 暖场 → 采访引导 → 记录精彩片段时间码
3. **后期** — 音频剪辑 → 降噪均衡 → 片头片尾
4. **发布** — Show Notes → 标题设计 → 多平台分发
5. **运营** — 数据跟踪 → 听众反馈 → 选题迭代

## 播客结构模板

```
00:00-02:00  Hook（提炼本期最精彩的一句话）
02:00-05:00  嘉宾/主题介绍
05:00-25:00  核心内容（3-4 个关键问题）
25:00-28:00  金句回顾 + 下期预告
28:00-30:00  片尾 CTA（关注/评分/留言）
```

## 适用场景

- 独立开发者用播客建立技术品牌
- 创业者用播客触达目标客户和投资人
- 内容创作者拓展音频渠道
- 公司内部知识分享的播客化

## 限制

- 聚焦内容策划和制作流程，不涉及音频工程细节
- 后期编辑覆盖基础概念，不涉及 DAW 软件操作
- 分发覆盖主流平台，不涉及小众/地区性平台
- 不涉及付费订阅和变现策略

## 相关参考（Playbook）

- 选题与平台定调（策略层）→ [references/content-strategy.md](../../references/content-strategy.md)
- 制作工作流与发布前检查清单（流程层）→ [references/production-workflow.md](../../references/production-workflow.md)